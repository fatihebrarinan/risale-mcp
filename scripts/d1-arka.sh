#!/usr/bin/env bash
# Taslak hattının uzun işlerini terminalden ve Claude Code oturumundan bağımsız çalıştırır (kullanıcının kararı,
# 2026-11-19; PLANLAR.md D5.0.1: bilgisayardan bağımsız çalışma sunucuda, bu betik ara çözüm). İş `systemd --user`
# altında geçici bir hizmet olur (`d1-<ad>`): terminal kapansa, oturum kapansa da sürer (`loginctl enable-linger`
# açık); iş sürerken bilgisayar uykuya geçmez (`systemd-inhibit`). Bilgisayar kapanırsa iş durur.
#
#   scripts/d1-arka.sh baslat <ad> <komut …>     # ör. baslat h9-21-22 bash -c 'uv run … && uv run …'
#   scripts/d1-arka.sh liste                      # d1-* işleri (çalışan, biten, düşen)
#   scripts/d1-arka.sh log <ad> [-f]              # günlük: data/interim/d1-isler/<ad>.log
#   scripts/d1-arka.sh durdur <ad>
#
# Model çağrıları kullanım sınırına karşı korumalıdır (`d1-prova.claude_p`): pencere doluysa iş bekler, ölmez.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
LOGS="$ROOT/data/interim/d1-isler"
mkdir -p "$LOGS"

cmd=${1:-}; shift || true
case "$cmd" in
  baslat)
    ad=${1:?ad gerekli}; shift
    [[ $# -ge 1 ]] || { echo "komut gerekli"; exit 2; }
    if systemctl --user is-active --quiet "d1-$ad"; then echo "d1-$ad zaten çalışıyor"; exit 1; fi
    systemctl --user reset-failed "d1-$ad" 2>/dev/null || true
    log="$LOGS/$ad.log"
    printf -v q '%q ' "$@"
    body="echo \"== \$(date '+%F %T') başladı: $q\"; $q; rc=\$?; echo \"== \$(date '+%F %T') bitti, çıkış \$rc\"; exit \$rc"
    inhibit=()
    if systemd-inhibit --what=sleep:idle --who=d1 --why=deneme true 2>/dev/null; then
        inhibit=(systemd-inhibit --what=sleep:idle --who="d1" --why="taslak hattı: $ad")
    else
        echo "uyarı: uyku engellenemedi; iş sürerken bilgisayarı uyutmayın"
    fi
    systemd-run --user --unit="d1-$ad" --collect --quiet --working-directory="$ROOT" \
        --setenv=PATH="$PATH" --setenv=HOME="$HOME" --setenv=LANG="${LANG:-C.UTF-8}" \
        --property=StandardOutput="append:$log" --property=StandardError="append:$log" \
        "${inhibit[@]}" bash -c "$body"
    echo "d1-$ad başladı; günlük $log"
    ;;
  liste)
    systemctl --user list-units --all --no-legend 'd1-*' | sed 's/^[●* ]*//' | awk '{print $1, $3, $4}'
    ls -t "$LOGS" 2>/dev/null | head -10 | sed 's/^/günlük: /'
    ;;
  log)
    ad=${1:?ad gerekli}
    if [[ ${2:-} == -f ]]; then tail -f "$LOGS/$ad.log"; else tail -n 30 "$LOGS/$ad.log"; fi
    ;;
  durdur)
    ad=${1:?ad gerekli}
    systemctl --user stop "d1-$ad" && echo "d1-$ad durduruldu"
    ;;
  *)
    sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
    exit 2
    ;;
esac
