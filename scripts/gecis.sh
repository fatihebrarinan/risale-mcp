#!/usr/bin/env bash
# Tek seferlik geçiş (2026-10-29): sunucuyu Tailscale Funnel'dan kendi alan adına (risalemcp.com) taşır.
# Önce Hetzner Cloud güvenlik duvarında 80/tcp ve 443/tcp gelen bağlantılarını açın (Caddy sertifikayı
# Let's Encrypt'ten 80/443 üzerinden alır). Sonra:
#
#   scripts/gecis.sh
#
# Yaptıkları: Caddy'yi kurar (Ubuntu paketi), docs/Caddyfile'ı ve site/'yi yerleştirir, ufw'de 80/443'ü açar,
# servisi yeni adresle (--public-url https://mcp.risalemcp.com) yeniden başlatır, Funnel'ı kapatır ve
# yeni adresi dener. Eski bağlayıcı adresi (risale.taile0138b.ts.net) çalışmaz; bağlayıcı yeni adresle eklenir.
set -euo pipefail

HOST="${RISALE_HOST:-root@100.108.174.19}"
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
SSH=(ssh -i "$KEY" -o BatchMode=yes)
cd "$(dirname "$0")/.."

echo "Caddy kuruluyor…"
"${SSH[@]}" "$HOST" "DEBIAN_FRONTEND=noninteractive apt-get install -y -q caddy >/dev/null && mkdir -p /var/www/risalemcp"
rsync -az -e "${SSH[*]}" docs/Caddyfile "$HOST:/etc/caddy/Caddyfile"
rsync -az --delete -e "${SSH[*]}" site/ "$HOST:/var/www/risalemcp/"
rsync -az -e "${SSH[*]}" docs/risale-mcp.server.service "$HOST:/etc/systemd/system/risale-mcp.service"

echo "güvenlik duvarı, servis, Caddy…"
"${SSH[@]}" "$HOST" "ufw allow 80/tcp >/dev/null && ufw allow 443/tcp >/dev/null \
    && systemctl daemon-reload && systemctl restart risale-mcp \
    && caddy validate --config /etc/caddy/Caddyfile >/dev/null && systemctl reload caddy \
    && tailscale funnel reset"

echo "deneniyor (sertifika ilk seferde birkaç saniye sürebilir)…"
for i in 1 2 3 4 5 6; do
    if curl -sf -o /dev/null https://mcp.risalemcp.com/.well-known/oauth-protected-resource/mcp; then break; fi
    sleep 5
done
curl -s -o /dev/null -w "site            %{http_code}\n" https://risalemcp.com/
curl -s -o /dev/null -w "OAuth üst verisi %{http_code}\n" https://mcp.risalemcp.com/.well-known/oauth-protected-resource/mcp
curl -s -o /dev/null -w "ikon            %{http_code}\n" https://mcp.risalemcp.com/icon.png
echo "Bağlayıcı adresi: https://mcp.risalemcp.com/mcp"
