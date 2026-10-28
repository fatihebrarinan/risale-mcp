#!/usr/bin/env bash
# Aşama 12: kodu ve hazır veriyi uzak sunucuya gönderir, bağımlılıkları kurar, servisi yeniden başlatır.
#
#   scripts/deploy.sh            # kod + risale.db + vektörler + quran.json
#   scripts/deploy.sh --code     # yalnızca kod (veri değişmediyse)
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

echo "kod gönderiliyor…"
git ls-files -z | rsync -az --from0 --files-from=- -e "${SSH[*]}" ./ "$HOST:$DEST/"

if [[ "${1:-}" != "--code" ]]; then
    echo "veri gönderiliyor…"
    "${SSH[@]}" "$HOST" "mkdir -p $DEST/data/vectors"
    rsync -az --info=progress2 -e "${SSH[*]}" data/risale.db data/quran.json "$HOST:$DEST/data/"
    rsync -az --delete -e "${SSH[*]}" data/vectors/ "$HOST:$DEST/data/vectors/"
    grep '^VOYAGE_API_KEY=' .env | "${SSH[@]}" "$HOST" "cat > $DEST/.env && chmod 600 $DEST/.env"
fi

"${SSH[@]}" "$HOST" "chown -R risale:risale $DEST && su - risale -c 'cd $DEST && ~/.local/bin/uv sync --no-dev --frozen -q' \
    && systemctl restart risale-mcp 2>/dev/null; systemctl is-active risale-mcp || true"
