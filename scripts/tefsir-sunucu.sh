#!/usr/bin/env bash
# Tefsir sunucusunun ayrı makinesi (kullanıcının kararı, 2026-11-07: risale ve hadis bir makinede, tefsir ileride
# büyüyeceği için ayrı makinede). Makine yalnız Tailscale'den erişilir; dışarıya ana makinenin Caddy'si açar
# (mcp.risalemcp.com/tefsir → <tailscale adresi>:8002/mcp). Sertifika, alan adı ve site ana makinede kalır.
#
# Önce (kullanıcı, Hetzner panelinde): Ubuntu 24.04, en az 4 GB bellek (CAX11 ya da CX22; tefsir süreci ≈1,5 GB),
# SSH anahtarı ~/.ssh/risale_hetzner.pub; makinede `tailscale up` (giriş bağlantısı kullanıcının hesabıyla).
#
#   TEFSIR_HOST=root@<tailscale adresi> scripts/tefsir-sunucu.sh kur      # ilk kurulum: kullanıcı, uv, güvenlik duvarı
#   TEFSIR_HOST=root@<tailscale adresi> scripts/tefsir-sunucu.sh gonder   # kod, tefsir profilinin verisi, servis
#
# Sonra ana makinede docs/Caddyfile'a /tefsir bloğu (adresle) eklenir ve scripts/deploy.sh --code çalışır.
# Kullanım kaydı (auth.db) bu makinede ayrı tutulur.
set -euo pipefail

HOST="${TEFSIR_HOST:?TEFSIR_HOST=root@<tailscale adresi> verin}"
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
DEST=/home/risale/risale-mcp
SSH=(ssh -i "$KEY" -o BatchMode=yes)
cd "$(dirname "$0")/.."

case "${1:-}" in
kur)
    "${SSH[@]}" "$HOST" "set -e; export DEBIAN_FRONTEND=noninteractive
        apt-get update -q >/dev/null && apt-get install -y -q rsync ufw >/dev/null
        id risale >/dev/null 2>&1 || useradd -m -s /bin/bash risale
        su - risale -c 'command -v ~/.local/bin/uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null'
        ufw default deny incoming >/dev/null; ufw default allow outgoing >/dev/null
        ufw allow in on tailscale0 >/dev/null; ufw --force enable >/dev/null
        mkdir -p $DEST/data/dist/tefsir/vectors $DEST/data/library/kuran && chown -R risale:risale /home/risale
        echo kuruldu; ufw status | head -5"
    ;;
gonder)
    git ls-files -z | rsync -az --from0 --files-from=- -e "${SSH[*]}" ./ "$HOST:$DEST/"
    rsync -az --info=progress2 -e "${SSH[*]}" data/dist/tefsir/risale.db "$HOST:$DEST/data/dist/tefsir/risale.db"
    rsync -az --delete -e "${SSH[*]}" data/dist/tefsir/vectors/ "$HOST:$DEST/data/dist/tefsir/vectors/"
    rsync -az -e "${SSH[*]}" data/library/kuran/quran.json "$HOST:$DEST/data/library/kuran/"
    grep '^VOYAGE_API_KEY=' .env | "${SSH[@]}" "$HOST" "cat > $DEST/.env && chmod 600 $DEST/.env"
    rsync -az -e "${SSH[*]}" docs/risale-mcp-tefsir.server.service "$HOST:/etc/systemd/system/risale-mcp-tefsir.service"
    "${SSH[@]}" "$HOST" "chown -R risale:risale $DEST && su - risale -c 'cd $DEST && ~/.local/bin/uv sync --no-dev --frozen -q' \
        && systemctl daemon-reload && systemctl enable -q risale-mcp-tefsir && systemctl restart risale-mcp-tefsir \
        && sleep 5 && systemctl is-active risale-mcp-tefsir && free -m | head -2"
    ;;
*)
    echo "kullanım: TEFSIR_HOST=root@<adres> $0 kur|gonder"; exit 2 ;;
esac
