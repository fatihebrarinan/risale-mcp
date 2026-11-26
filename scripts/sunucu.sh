#!/usr/bin/env bash
# Uzak sunucuyu bu bilgisayardan yönetir (Aşama 12). SSH yalnızca Tailscale ağından açıktır.
#
#   scripts/sunucu.sh auth add-user <ad> --generate   # hesap aç (parolayı gösterir)
#   scripts/sunucu.sh auth users | sessions | usage [--user <ad>] [--params] | revoke --user <ad> | passwd <ad> | remove-user <ad>
#   scripts/sunucu.sh auth debug-url --new | --revoke    # gizli hata ayıklama adresi (açık kip; araç girdileri, 7 gün)
#   scripts/sunucu.sh auth --server hadis debug-url --new  # hadis bağdaştırıcısının ayrı adresi (hadis.risalemcp.com/mcp/<anahtar>)
#   scripts/sunucu.sh auth usage --user '(debug)' --params [--only genel|hadis]  # o adresten gelen isteklerin kaydı
#   (tefsir ayrı makinede: scripts/tefsir-sunucu.sh auth debug-url --new)
#   scripts/sunucu.sh taslak add-user <e-posta> --generate [--name <ad>] | set-name <e-posta> <ad> | passwd <e-posta> | remove-user <e-posta> | users | sessions | revoke <e-posta>
#                                                     # read. ve lab.ayinedar.org hesapları (MCP hesapları değil)
#   scripts/sunucu.sh auth debug <ad> on|off              # hesabın ayrıntılı kaydı (OAuth kipi; askıda)
#   scripts/sunucu.sh openai-challenge <jeton> [hadis|tefsir|klasik]  # OpenAI'nin alan adı doğrulama jetonu
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
    taslak)
        # S5: read. ve lab.ayinedar.org hesapları (MCP hesapları değil; src/risale_mcp/site_auth.py, data/site_auth.db)
        shift
        args=$(printf ' %q' "$@")
        "${SSH[@]}" -t "$HOST" "su - risale -c 'cd risale-mcp && .venv/bin/python -m risale_mcp.site_auth$args'" ;;
    openai-challenge)
        # Alan adı başına bir jeton: ikinci argüman yoksa mcp.risalemcp.com (Risale), varsa o alt alan adı
        [[ -n "${2:-}" ]] || { echo "jeton gerekli"; exit 1; }
        case "${3:-}" in "") dir=/var/www/mcp-challenge; host=mcp ;;
            hadis|tefsir|klasik) dir=/var/www/mcp-challenge-$3; host=$3 ;; *) echo "hadis, tefsir ya da klasik"; exit 2 ;; esac
        printf '%s' "$2" | "${SSH[@]}" "$HOST" "mkdir -p $dir/.well-known && cat > $dir/.well-known/openai-apps-challenge"
        curl -s "https://$host.risalemcp.com/.well-known/openai-apps-challenge"; echo ;;
    status|restart|stop|start)
        "${SSH[@]}" "$HOST" "systemctl $1 risale-mcp; systemctl --no-pager status risale-mcp | head -5" ;;
    logs)
        "${SSH[@]}" -t "$HOST" "journalctl -u risale-mcp -f" ;;
    ssh)
        "${SSH[@]}" "$HOST" ;;
    *)
        sed -n '2,15p' "$0"; exit 1 ;;
esac
