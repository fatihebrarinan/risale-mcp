#!/usr/bin/env bash
# Uzak sunucuyu bu bilgisayardan yönetir (Aşama 12). SSH yalnızca Tailscale ağından açıktır.
#
#   scripts/sunucu.sh auth add-user <ad> --generate   # hesap aç (parolayı gösterir)
#   scripts/sunucu.sh auth users | sessions | usage [--user <ad>] [--params] | revoke --user <ad> | passwd <ad> | remove-user <ad>
#   scripts/sunucu.sh auth debug <ad> on|off              # hesabın ayrıntılı kaydı (araç girdileri, 7 gün)
#   scripts/sunucu.sh status | restart | stop | start  # servis
#   scripts/sunucu.sh logs                             # canlı günlük (Ctrl+C ile çık)
#   scripts/sunucu.sh ssh                              # sunucuya bağlan
set -euo pipefail

HOST="${RISALE_HOST:-root@100.108.174.19}"
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
SSH=(ssh -i "$KEY")

case "${1:-}" in
    auth)
        shift
        args=$(printf ' %q' "$@")
        "${SSH[@]}" -t "$HOST" "su - risale -c 'cd risale-mcp && .venv/bin/risale-mcp auth$args'" ;;
    status|restart|stop|start)
        "${SSH[@]}" "$HOST" "systemctl $1 risale-mcp; systemctl --no-pager status risale-mcp | head -5" ;;
    logs)
        "${SSH[@]}" -t "$HOST" "journalctl -u risale-mcp -f" ;;
    ssh)
        "${SSH[@]}" "$HOST" ;;
    *)
        sed -n '2,10p' "$0"; exit 1 ;;
esac
