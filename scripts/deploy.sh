#!/usr/bin/env bash
# Aşama 12: kodu ve hazır veriyi uzak sunucuya gönderir, bağımlılıkları kurar, servisi yeniden başlatır.
#
#   scripts/deploy.sh            # kod + genel profilin veritabanı ve vektörleri + quran.json
#   scripts/deploy.sh --code     # yalnızca kod ve site/ (veri değişmediyse)
#   DEPLOY_EXPECT="cite" scripts/deploy.sh   # bu araçların çıktısındaki fark beklenen sayılır
#   scripts/deploy.sh --hadis    # ayrıca hadis sunucusu (aynı makine, 127.0.0.1:8001, mcp.risalemcp.com/hadis):
#                                # hadis.db, vektörleri ve servis birimi; `--code` ile birlikte de verilebilir
#
# Göndermeden önce (kullanıcının kuralı, `--code` dahil): veri gidecekse genel veritabanı sürüm etiketi alır
# (`manifest release`); araç çıktısı kaydedilir ve son yayın kaydıyla karşılaştırılır (`tool_snapshot`, H0).
# Beklenmeyen fark varsa hiçbir şey gönderilmez; rapor data/interim/tool_snapshot/aday-…/ altındadır.
#
# Ayrıştırma ve veritabanı kurulumu bu bilgisayarda yapılır; ham veri sunucuya gitmez. Sunucudaki `data/auth.db`
# (hesaplar, oturumlar, kullanım kaydı) asıl kopyadır, bu betik onu ezmez. `.env`'den yalnızca VOYAGE_API_KEY gider.
# Sunucu: Hetzner CAX11 (Helsinki, Ubuntu 24.04), kullanıcı `risale`, servis `risale-mcp` (bkz. CLAUDE.md).
set -euo pipefail

HOST="${RISALE_HOST:-root@100.108.174.19}"   # Tailscale adresi; SSH internete kapalı
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
DEST=/home/risale/risale-mcp
SSH=(ssh -i "$KEY" -o BatchMode=yes)
cd "$(dirname "$0")/.."
CODE_ONLY=0; HADIS=0
for arg in "$@"; do
    case "$arg" in --code) CODE_ONLY=1 ;; --hadis) HADIS=1 ;; *) echo "bilinmeyen seçenek: $arg"; exit 2 ;; esac
done

if [[ $CODE_ONLY == 0 ]]; then
    uv run python -m risale_mcp.manifest release --profile genel
fi
STAMP=$(date +%Y%m%d-%H%M%S)
SNAPSHOTS=data/interim/tool_snapshot
PREV=$(ls -d "$SNAPSHOTS"/yayin-* 2>/dev/null | sort | tail -1 | xargs -r basename)
uv run python -m risale_mcp.tool_snapshot record "aday-$STAMP"
if [[ -n "$PREV" ]]; then
    # shellcheck disable=SC2086
    uv run python -m risale_mcp.tool_snapshot compare "$PREV" "aday-$STAMP" --expect ${DEPLOY_EXPECT:-} \
        || { echo "araç çıktısında beklenmeyen fark: gönderilmedi (rapor $SNAPSHOTS/aday-$STAMP/diff-$PREV.md)"; exit 1; }
else
    echo "önceki yayın kaydı yok: karşılaştırılmadı"
fi

echo "kod gönderiliyor…"
git ls-files -z | rsync -az --from0 --files-from=- -e "${SSH[*]}" ./ "$HOST:$DEST/"
# Tanıtım sitesi (risalemcp.com; Caddy /var/www/risalemcp'den sunar, bkz. docs/Caddyfile)
"${SSH[@]}" "$HOST" "mkdir -p /var/www/risalemcp"
rsync -az --delete -e "${SSH[*]}" site/ "$HOST:/var/www/risalemcp/"
# Caddy yapılandırması (docs/Caddyfile) değiştiyse yeniden yüklenir
rsync -az -e "${SSH[*]}" docs/Caddyfile "$HOST:/etc/caddy/Caddyfile.new"
"${SSH[@]}" "$HOST" "cmp -s /etc/caddy/Caddyfile.new /etc/caddy/Caddyfile && rm /etc/caddy/Caddyfile.new \
    || { caddy validate --config /etc/caddy/Caddyfile.new --adapter caddyfile >/dev/null 2>&1 \
         && mv /etc/caddy/Caddyfile.new /etc/caddy/Caddyfile && systemctl reload caddy && echo 'Caddy yeniden yüklendi'; }"

# Servis birimi (docs/risale-mcp.server.service) değiştiyse kurulur; yeniden başlatma aşağıda
rsync -az -e "${SSH[*]}" docs/risale-mcp.server.service "$HOST:/etc/systemd/system/risale-mcp.service.new"
"${SSH[@]}" "$HOST" "cmp -s /etc/systemd/system/risale-mcp.service.new /etc/systemd/system/risale-mcp.service \
    && rm /etc/systemd/system/risale-mcp.service.new \
    || { mv /etc/systemd/system/risale-mcp.service.new /etc/systemd/system/risale-mcp.service \
         && systemctl daemon-reload && echo 'servis birimi güncellendi'; }"

if [[ $CODE_ONLY == 0 ]]; then
    echo "veri gönderiliyor…"
    # Eski düzenden taşıma (bir kez çalışır, sonra boşa geçer): aktarım yalnız farkı gönderir.
    "${SSH[@]}" "$HOST" "cd $DEST/data && mkdir -p dist/genel/vectors library/kuran \
        && { [ ! -f risale.db ] || mv risale.db dist/genel/risale.db; } \
        && { [ ! -d vectors ] || { rmdir dist/genel/vectors && mv vectors dist/genel/vectors; }; } \
        && { [ ! -f quran.json ] || mv quran.json library/kuran/quran.json; }"
    # `private` eserler (Esasat, harekeli Mesnevî…) ve vektörleri yalnızca yereldedir: sunucuya `genel` profili gider.
    rsync -az --info=progress2 -e "${SSH[*]}" data/dist/genel/risale.db "$HOST:$DEST/data/dist/genel/risale.db"
    rsync -az --info=progress2 -e "${SSH[*]}" data/library/kuran/quran.json "$HOST:$DEST/data/library/kuran/"
    uv run python -m risale_mcp.embeddings export-public
    rsync -az --delete -e "${SSH[*]}" data/dist/genel/vectors/ "$HOST:$DEST/data/dist/genel/vectors/"
    grep '^VOYAGE_API_KEY=' .env | "${SSH[@]}" "$HOST" "cat > $DEST/.env && chmod 600 $DEST/.env"
fi

if [[ $HADIS == 1 ]]; then
    # Hadis sunucusu (MVP M5, kullanıcının kararı 2026-11-07: risale ile aynı makine, tefsir ayrı makine).
    # Veritabanı yerelde `hadis_db` ile, vektörleri `hadis_vectors` ile kurulur; yalnız açık lisanslı kitaplar.
    echo "hadis sunucusu gönderiliyor…"
    "${SSH[@]}" "$HOST" "mkdir -p $DEST/data/dist/hadis/vectors"
    rsync -az --info=progress2 -e "${SSH[*]}" data/dist/hadis/hadis.db "$HOST:$DEST/data/dist/hadis/hadis.db"
    rsync -az --delete -e "${SSH[*]}" data/dist/hadis/vectors/ "$HOST:$DEST/data/dist/hadis/vectors/"
    rsync -az -e "${SSH[*]}" docs/risale-mcp-hadis.server.service "$HOST:/etc/systemd/system/risale-mcp-hadis.service.new"
    "${SSH[@]}" "$HOST" "cmp -s /etc/systemd/system/risale-mcp-hadis.service.new /etc/systemd/system/risale-mcp-hadis.service \
        && rm /etc/systemd/system/risale-mcp-hadis.service.new \
        || { mv /etc/systemd/system/risale-mcp-hadis.service.new /etc/systemd/system/risale-mcp-hadis.service \
             && systemctl daemon-reload && systemctl enable risale-mcp-hadis -q && echo 'hadis servis birimi kuruldu'; }"
fi

"${SSH[@]}" "$HOST" "chown -R risale:risale $DEST && su - risale -c 'cd $DEST && ~/.local/bin/uv sync --no-dev --frozen -q' \
    && systemctl restart risale-mcp 2>/dev/null; systemctl is-active risale-mcp || true"
# Hadis servisi kuruluysa kodla birlikte yeniden başlar
"${SSH[@]}" "$HOST" "systemctl is-enabled -q risale-mcp-hadis 2>/dev/null \
    && { systemctl restart risale-mcp-hadis; echo -n 'hadis: '; systemctl is-active risale-mcp-hadis; } || true"

# Gönderilen hâl bir sonraki deploy'un karşılaştırma tabanıdır
mv "$SNAPSHOTS/aday-$STAMP" "$SNAPSHOTS/yayin-$STAMP"
echo "araç çıktısı kaydı: $SNAPSHOTS/yayin-$STAMP"
