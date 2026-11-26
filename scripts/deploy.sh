#!/usr/bin/env bash
# Aşama 12: kodu ve hazır veriyi uzak sunucuya gönderir, bağımlılıkları kurar, servisi yeniden başlatır.
#
#   scripts/deploy.sh            # kod + genel profilin veritabanı ve vektörleri + quran.json
#   scripts/deploy.sh --code     # yalnızca kod, site/ ve taslak bölümü (data/d1/masa/; veri değişmediyse)
#   scripts/deploy.sh --sohbet   # yalnız sohbet sayfası (S13; ≈10 sn): değişen dosyalar gider, yalnız risale-sohbet yeniden
#                                # başlar. Sunucudakinden farklı dosyalardan biri sohbetin dışında çalışan koddaysa
#                                # (src/ altında sohbet olmayan, pyproject.toml, uv.lock, servis birimleri, Caddyfile)
#                                # durur ve --code ister: MCP araçlarına dokunmadığı için araç çıktısı kaydı gerekmez
#                                # (kullanıcının kararı, 2026-11-26)
#   scripts/deploy.sh --site     # yalnız tanıtım sitesi (site/) ve yazıların önizlemesi: kod gitmez, servis yeniden
#                                # başlamaz, araç çıktısı değişmediği için kaydı da yapılmaz (S9; zamanlı yayın bunu kullanır)
#   DEPLOY_EXPECT="cite" scripts/deploy.sh   # bu araçların çıktısındaki fark beklenen sayılır
#   scripts/deploy.sh --hadis    # ayrıca hadis sunucusu (aynı makine, 127.0.0.1:8001, hadis.risalemcp.com):
#                                # hadis.db, vektörleri ve servis birimi; `--code` ile birlikte de verilebilir
#
# Göndermeden önce (kullanıcının kuralı, `--code` dahil): veri gidecekse genel veritabanı sürüm etiketi alır
# (`manifest release`); araç çıktısı kaydedilir ve son yayın kaydıyla karşılaştırılır (`tool_snapshot`, H0).
# Beklenmeyen fark varsa hiçbir şey gönderilmez; rapor data/interim/tool_snapshot/aday-…/ altındadır.
#
# Ayrıştırma ve veritabanı kurulumu bu bilgisayarda yapılır; ham veri sunucuya gitmez. Sunucudaki `data/auth.db`
# (hesaplar, oturumlar, kullanım kaydı) asıl kopyadır, bu betik onu ezmez; sohbetin `data/sohbet.db`'si de öyle.
# `.env`'den yalnızca VOYAGE_API_KEY ve sohbetin anahtarları (ANTHROPIC_API_KEY, SCW_SECRET_KEY, SCW_PROJECT_ID), sınırsız
# hesapları (SOHBET_SINIRSIZ) ve öbür kütüphanelerin iç erişim adresleri (SOHBET_HADIS_URL, SOHBET_TEFSIR_URL,
# SOHBET_KLASIK_URL; S13.17; `.env.sunucu`'dan) gider.
# Sunucu: Hetzner CAX11 (Helsinki, Ubuntu 24.04), kullanıcı `risale`, servis `risale-mcp` (bkz. CLAUDE.md).
set -euo pipefail

HOST="${RISALE_HOST:-root@100.108.174.19}"   # Tailscale adresi; SSH internete kapalı
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
DEST=/home/risale/risale-mcp
SSH=(ssh -i "$KEY" -o BatchMode=yes)
cd "$(dirname "$0")/.."
# S11: web düzenleyici yazının aslını sunucudaki depodan okur (yazilar.py): taslaklar commit edilmeden de gitsin,
# yayımlanıp adı değişen eski dosya kalksın. Yalnız iki klasör; kod gitmez.
send_posts() {
    rsync -az --delete --chown=risale:risale -e "${SSH[*]}" docs/yenilikler docs/calismalar "$HOST:$DEST/docs/"
}
# S13.15.2: ayinedar.org ve alt alan adlarının sayfaları (Caddy /var/www/ayinedar'dan sunar, bkz. docs/Caddyfile)
send_ayinedar() {
    "${SSH[@]}" "$HOST" "mkdir -p /var/www/ayinedar"
    rsync -az --delete -e "${SSH[*]}" site-ayinedar/ "$HOST:/var/www/ayinedar/"
}
CODE_ONLY=0; HADIS=0; SITE_ONLY=0; SOHBET_ONLY=0
# Sunucuya giden .env satırları; S13.17: sohbetin öbür kütüphanelerinin iç erişim adresleri
ENV_KEYS='^(VOYAGE_API_KEY|ANTHROPIC_API_KEY|SCW_SECRET_KEY|SCW_PROJECT_ID|SOHBET_SINIRSIZ|SOHBET_HADIS_URL|SOHBET_TEFSIR_URL|SOHBET_KLASIK_URL)='
# Yalnız sunucuda geçerli satırlar `.env.sunucu`'dadır (git dışı; yerel `.env`'e konmaz, yoksa yerel denemeler de
# sunucunun adreslerini kullanırdı: hadisin 127.0.0.1:8001'i yalnız orada açık)
server_env() { grep -hE "$ENV_KEYS" .env $( [[ -f .env.sunucu ]] && echo .env.sunucu ) || true; }
for arg in "$@"; do
    case "$arg" in --code) CODE_ONLY=1 ;; --hadis) HADIS=1 ;; --site) SITE_ONLY=1 ;; --sohbet) SOHBET_ONLY=1 ;;
        *) echo "bilinmeyen seçenek: $arg"; exit 2 ;; esac
done

if [[ $SITE_ONLY == 1 ]]; then
    "${SSH[@]}" "$HOST" "mkdir -p /var/www/risalemcp"
    rsync -az --delete -e "${SSH[*]}" site/ "$HOST:/var/www/risalemcp/"
    send_ayinedar
    if [[ -f data/interim/onizleme/index.html ]]; then
        "${SSH[@]}" "$HOST" "install -d -o root -g caddy -m 2750 /var/www/ozel/taslak/onizleme"
        rsync -az --delete --chown=root:caddy --chmod=D2750,F640 -e "${SSH[*]}" data/interim/onizleme/ "$HOST:/var/www/ozel/taslak/onizleme/"
    fi
    send_posts
    echo "site gönderildi"
    exit 0
fi

if [[ $SOHBET_ONLY == 1 ]]; then
    # Sunucudakinden içeriği farklı izlenen dosyalar (rsync'in sağlama karşılaştırması; ≈3 sn)
    changed=$(git ls-files -z | rsync -az --from0 --files-from=- --dry-run --checksum --itemize-changes \
        -e "${SSH[*]}" ./ "$HOST:$DEST/" | awk '$1 ~ /^<f/ {print $2}')
    # .env'in sunucuya giden satırları değiştiyse (S13.17: kütüphane adresleri) dosya değişmese de gönderilir
    env_same=$([[ "$(server_env | sha1sum)" == "$("${SSH[@]}" "$HOST" "sha1sum < $DEST/.env")" ]] && echo 1 || echo 0)
    [[ -n "$changed" || $env_same == 0 ]] || { echo "sunucudakiyle aynı: gönderilecek bir şey yok"; exit 0; }
    # Çalışan kodu etkileyen ama sohbetin olmayan dosya: tam yol (--code), araç çıktısı kaydıyla
    other=$(grep -E '^(src/|pyproject\.toml$|uv\.lock$|docs/.*\.service$|docs/Caddyfile$)' <<<"$changed" \
        | grep -vE '^src/risale_mcp/(sohbet\.py|sohbet_hesap\.py|sohbet_dene\.py|dosya\.py|kipler\.py|kutuphaneler\.py|ayet_dosyasi\.py|sohbet_assets/)' || true)
    if [[ -n "$other" ]]; then
        echo "sohbetin dışında çalışan kod değişmiş; --code ile gönderin (araç çıktısı kaydıyla):"
        sed 's/^/  /' <<<"$other"
        exit 1
    fi
    [[ $env_same == 1 ]] || echo "anahtarlar değişmiş: .env gönderiliyor"
    [[ -z "$changed" ]] || { echo "gönderiliyor:"; sed 's/^/  /' <<<"$changed"; }
    [[ -z "$changed" ]] || tr '\n' '\0' <<<"$changed" | rsync -az --from0 --files-from=- --chown=risale:risale -e "${SSH[*]}" ./ "$HOST:$DEST/"
    server_env \
        | "${SSH[@]}" "$HOST" "cat > $DEST/.env.new && chmod 600 $DEST/.env.new && chown risale:risale $DEST/.env.new && mv $DEST/.env.new $DEST/.env"
    # Servis açılırken birkaç saniye 502 verir: cevap verene kadar beklenir (en çok 30 sn)
    "${SSH[@]}" "$HOST" "systemctl restart risale-sohbet; for i in \$(seq 30); do \
        curl -sf -o /dev/null http://127.0.0.1:8010/giris && { echo \"sohbet: açık (\$i sn)\"; exit 0; }; sleep 1; done; \
        echo 'sohbet: 30 sn içinde açılmadı'; journalctl -u risale-sohbet -n 20 --no-pager; exit 1"
    exit 0
fi

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

if [[ $HADIS == 1 ]]; then
    # Hadis sunucusunun kendi H0/H1'i: sürüm etiketi ve kendi çağrı setiyle (tests/golden/tool_calls_hadis.json)
    # son `hadis-yayin-*` kaydına karşı araç çıktısı; beklenen fark HADIS_EXPECT ile
    [[ $CODE_ONLY == 1 ]] || uv run python -m risale_mcp.manifest release --profile hadis
    HPREV=$(ls -d "$SNAPSHOTS"/hadis-yayin-* 2>/dev/null | sort | tail -1 | xargs -r basename || true)
    uv run python -m risale_mcp.tool_snapshot record "hadis-aday-$STAMP" --profile hadis
    if [[ -n "$HPREV" ]]; then
        # shellcheck disable=SC2086
        uv run python -m risale_mcp.tool_snapshot compare "$HPREV" "hadis-aday-$STAMP" --expect ${HADIS_EXPECT:-} \
            || { echo "hadis araç çıktısında beklenmeyen fark: gönderilmedi"; exit 1; }
    else
        echo "hadis: önceki yayın kaydı yok (ilk yayın)"
    fi
fi

echo "kod gönderiliyor…"
git ls-files -z | rsync -az --from0 --files-from=- -e "${SSH[*]}" ./ "$HOST:$DEST/"
# Tanıtım sitesi (risalemcp.com; Caddy /var/www/risalemcp'den sunar, bkz. docs/Caddyfile)
"${SSH[@]}" "$HOST" "mkdir -p /var/www/risalemcp"
rsync -az --delete -e "${SSH[*]}" site/ "$HOST:/var/www/risalemcp/"
send_ayinedar
# S5: girişli taslak bölümü (risalemcp.com/taslak/): âyet masası kapalı depodan (data/d1, `scripts/d1-masa.py`)
# /var/www/ozel/taslak/'a; site/ klasörüne girmez, yalnız Caddy okur, giriş servisi (aşağıda) kapıdır
# Birim başına bir sayfa (<birim>.html; index.html son birim)
if [[ -d data/d1/masa ]]; then
    "${SSH[@]}" "$HOST" "install -d -o root -g caddy -m 750 /var/www/ozel && install -d -o root -g caddy -m 2750 /var/www/ozel/taslak"
    # -u: sunucudaki daha yeni dosya ezilmez (kuyruk D5 sayfalarını taslak sunucusundan da gönderir)
    rsync -azu --chown=root:caddy --chmod=D2750,F640 -e "${SSH[*]}" data/d1/masa/ "$HOST:/var/www/ozel/taslak/"
fi
# Okuma platformu (/oku/) ve masa (ayet.html, masa-veri/, pano…) burada GÖNDERİLMEZ (S10, 2026-11-23): ikisini de
# taslak sunucusundaki D5 kuyruğu her birimden sonra kurup gönderir; yereldeki data/interim/oku{,-masa}/ eski kalır ve
# eskiden her deploy masanın yeni dosyalarını 21 Kasım kopyasıyla eziyordu. Elle: `scripts/oku-veri.py --gonder`
# (önce `git -C data/d1 pull`; yerelden yalnız platformu gönderir).
# S9: Yenilikler ve Çalışmalar taslaklarının önizlemesi (girişli /taslak/onizleme/; `scripts/site-uret.py` üretir).
# --delete: yayımlanan taslağın önizlemesi kalkar
if [[ -f data/interim/onizleme/index.html ]]; then
    "${SSH[@]}" "$HOST" "install -d -o root -g caddy -m 2750 /var/www/ozel/taslak/onizleme"
    rsync -az --delete --chown=root:caddy --chmod=D2750,F640 -e "${SSH[*]}" data/interim/onizleme/ "$HOST:/var/www/ozel/taslak/onizleme/"
fi
send_posts
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
fi
# Anahtarlar (`--code`'da da: S12'nin sohbeti yeni anahtar ister); başka satır gitmez
server_env \
    | "${SSH[@]}" "$HOST" "cat > $DEST/.env.new && chmod 600 $DEST/.env.new && mv $DEST/.env.new $DEST/.env"

if [[ $HADIS == 1 ]]; then
    # Hadis sunucusu (MVP M5, kullanıcının kararı 2026-11-07: risale ile aynı makine, tefsir ayrı makine).
    # Veritabanı yerelde `hadis_db` ile, vektörleri `hadis_vectors` ile kurulur; yalnız açık lisanslı kitaplar.
    echo "hadis sunucusu gönderiliyor…"
    "${SSH[@]}" "$HOST" "mkdir -p $DEST/data/dist/hadis/vectors"
    rsync -az --info=progress2 -e "${SSH[*]}" data/dist/hadis/hadis.db "$HOST:$DEST/data/dist/hadis/hadis.db"
    rsync -az --delete -e "${SSH[*]}" data/dist/hadis/vectors/ "$HOST:$DEST/data/dist/hadis/vectors/"
    # Künye dizini (find_by_citation'ın bâb künyeleri; kitapların tam metni yerelde kalır): her gönderimde yeniden yazılır
    uv run python -m risale_mcp.hadis_kutub index
    rsync -az -e "${SSH[*]}" data/dist/hadis/kutub-index.json.gz "$HOST:$DEST/data/dist/hadis/kutub-index.json.gz"
    rsync -az -e "${SSH[*]}" docs/risale-mcp-hadis.server.service "$HOST:/etc/systemd/system/risale-mcp-hadis.service.new"
    "${SSH[@]}" "$HOST" "cmp -s /etc/systemd/system/risale-mcp-hadis.service.new /etc/systemd/system/risale-mcp-hadis.service \
        && rm /etc/systemd/system/risale-mcp-hadis.service.new \
        || { mv /etc/systemd/system/risale-mcp-hadis.service.new /etc/systemd/system/risale-mcp-hadis.service \
             && systemctl daemon-reload && systemctl enable risale-mcp-hadis -q && echo 'hadis servis birimi kuruldu'; }"
fi

# Taslak bölümünün giriş servisi (S5; docs/risale-taslak.service): birim değiştiyse kurulur, kodla yeniden başlar
rsync -az -e "${SSH[*]}" docs/risale-taslak.service "$HOST:/etc/systemd/system/risale-taslak.service.new"
"${SSH[@]}" "$HOST" "cmp -s /etc/systemd/system/risale-taslak.service.new /etc/systemd/system/risale-taslak.service \
    && rm /etc/systemd/system/risale-taslak.service.new \
    || { mv /etc/systemd/system/risale-taslak.service.new /etc/systemd/system/risale-taslak.service \
         && systemctl daemon-reload && systemctl enable risale-taslak -q && echo 'taslak servis birimi kuruldu'; }"

# S12: sohbet sayfasının servisi (docs/risale-sohbet.service, 127.0.0.1:8010): birim değiştiyse kurulur; ntfy konusu
# (harcama uyarısı, `sohbet.notify`) yoksa açılır ve bir kez yazdırılır (telefonda abone olunur)
rsync -az -e "${SSH[*]}" docs/risale-sohbet.service "$HOST:/etc/systemd/system/risale-sohbet.service.new"
"${SSH[@]}" "$HOST" "cmp -s /etc/systemd/system/risale-sohbet.service.new /etc/systemd/system/risale-sohbet.service \
    && rm /etc/systemd/system/risale-sohbet.service.new \
    || { mv /etc/systemd/system/risale-sohbet.service.new /etc/systemd/system/risale-sohbet.service \
         && systemctl daemon-reload && systemctl enable risale-sohbet -q && echo 'sohbet servis birimi kuruldu'; }"
"${SSH[@]}" "$HOST" "[ -f $DEST/data/sohbet-ntfy ] || { mkdir -p $DEST/data \
    && echo \"risale-sohbet-\$(head -c 12 /dev/urandom | od -An -tx1 | tr -d ' \\n')\" > $DEST/data/sohbet-ntfy \
    && chmod 600 $DEST/data/sohbet-ntfy && echo \"ntfy konusu (telefonda abone olun): \$(cat $DEST/data/sohbet-ntfy)\"; }"

"${SSH[@]}" "$HOST" "chown -R risale:risale $DEST && su - risale -c 'cd $DEST && ~/.local/bin/uv sync --no-dev --frozen --extra sohbet -q' \
    && systemctl restart risale-mcp 2>/dev/null; systemctl is-active risale-mcp || true"
"${SSH[@]}" "$HOST" "systemctl restart risale-taslak; echo -n 'taslak: '; systemctl is-active risale-taslak || true"
"${SSH[@]}" "$HOST" "systemctl restart risale-sohbet; echo -n 'sohbet: '; systemctl is-active risale-sohbet || true"
# Hadis servisi kuruluysa kodla birlikte yeniden başlar
"${SSH[@]}" "$HOST" "systemctl is-enabled -q risale-mcp-hadis 2>/dev/null \
    && { systemctl restart risale-mcp-hadis; echo -n 'hadis: '; systemctl is-active risale-mcp-hadis; } || true"

# Gönderilen hâl bir sonraki deploy'un karşılaştırma tabanıdır
mv "$SNAPSHOTS/aday-$STAMP" "$SNAPSHOTS/yayin-$STAMP"
[[ $HADIS == 1 ]] && mv "$SNAPSHOTS/hadis-aday-$STAMP" "$SNAPSHOTS/hadis-yayin-$STAMP"
echo "araç çıktısı kaydı: $SNAPSHOTS/yayin-$STAMP"
