#!/usr/bin/env bash
# Taslak hattının uzun işlerini terminalden ve Claude Code oturumundan bağımsız çalıştırır (kullanıcının kararı,
# 2026-11-19; PLANLAR.md D5.0.1: bilgisayardan bağımsız çalışma sunucuda, bu betik ara çözüm). İş `systemd --user`
# altında geçici bir hizmet olur (`d1-<ad>`): terminal kapansa, oturum kapansa da sürer (`loginctl enable-linger`
# açık); iş sürerken bilgisayar uykuya geçmez (`systemd-inhibit`). Bilgisayar kapanırsa iş durur: `yeniden`.
#
#   scripts/d1-arka.sh baslat <ad> <komut …>     # ör. baslat h9-21-22 bash data/interim/d1-isler/h9-21-22.sh
#   scripts/d1-arka.sh liste                      # işler: durum (çalışıyor, bekliyor, bitti), günlüğün son satırı
#   scripts/d1-arka.sh log <ad> [-f]              # günlük: data/interim/d1-isler/<ad>.log
#   scripts/d1-arka.sh bekle <ad>                 # iş bitene kadar bekler (Claude Code bunu arka plan işi olarak
#                                                 # çalıştırır: iş bitince haberi gelir); çıkış işin çıkışıdır
#   scripts/d1-arka.sh yeniden <ad>               # aynı komutu yeniden başlatır (kesintiden sonra; adımlar biteni atlar)
#   scripts/d1-arka.sh durdur <ad>
#
# İş bitince `data/d1` commit ve push edilir, masaüstüne bildirim düşer (`scripts/d1-arka-is.sh`). Süreç durdurmak
# için `pkill -f` kullanılmaz (komut satırının kendisini de eşleştirir, 2026-11-19'da iki kez oldu): `durdur`.
# Model çağrıları kullanım sınırına karşı korumalıdır (`d1-prova.claude_p`): pencere doluysa iş bekler, ölmez.
# Gövde `main` işlevindedir: bu dosya değişse de çalışan bir `bekle` etkilenmez.
main() {
set -euo pipefail
cd "$(dirname "$0")/.."
local ROOT LOGS cmd ad
ROOT=$(pwd)
LOGS="$ROOT/data/interim/d1-isler"
mkdir -p "$LOGS"

cmd=${1:-}; shift || true
case "$cmd" in
  baslat)
    ad=${1:?ad gerekli}; shift
    [[ $# -ge 1 ]] || { echo "komut gerekli"; return 2; }
    if systemctl --user is-active --quiet "d1-$ad"; then echo "d1-$ad zaten çalışıyor"; return 1; fi
    systemctl --user reset-failed "d1-$ad" 2>/dev/null || true
    local log="$LOGS/$ad.log" q
    printf -v q '%q ' "$@"
    printf '%s\n' "$q" > "$LOGS/$ad.komut"              # `yeniden` için
    local inhibit=()
    if systemd-inhibit --what=sleep:idle --who=d1 --why=deneme true 2>/dev/null; then
        inhibit=(systemd-inhibit --what=sleep:idle --who="d1" --why="taslak hattı: $ad")
    else
        echo "uyarı: uyku engellenemedi; iş sürerken bilgisayarı uyutmayın"
    fi
    systemd-run --user --unit="d1-$ad" --collect --quiet --working-directory="$ROOT" \
        --setenv=PATH="$PATH" --setenv=HOME="$HOME" --setenv=LANG="${LANG:-C.UTF-8}" \
        --setenv=DISPLAY="${DISPLAY:-:0}" --setenv=DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/$(id -u)/bus}" \
        --property=StandardOutput="append:$log" --property=StandardError="append:$log" \
        "${inhibit[@]}" bash "$ROOT/scripts/d1-arka-is.sh" "$ad" "$@"
    echo "d1-$ad başladı; günlük $log"
    ;;
  yeniden)
    ad=${1:?ad gerekli}
    [[ -f $LOGS/$ad.komut ]] || { echo "kayıtlı komut yok: $LOGS/$ad.komut"; return 1; }
    local -a args
    eval "args=($(cat "$LOGS/$ad.komut"))"
    echo "== $(date '+%F %T') yeniden başlatılıyor" >> "$LOGS/$ad.log"
    "$ROOT/scripts/d1-arka.sh" baslat "$ad" "${args[@]}"
    ;;
  liste)
    local f a state last
    printf '%-18s %-26s %s\n' "İŞ" "DURUM" "SON SATIR"
    for f in $(ls -t "$LOGS"/*.log 2>/dev/null | head -15); do
        a=$(basename "$f" .log)
        last=$(grep -v '^\s*$' "$f" | grep -v 'failed with exit status' | tail -n 1 | cut -c1-90)
        if systemctl --user is-active --quiet "d1-$a"; then
            state="çalışıyor"; [[ $last == *"⏸"* ]] && state="bekliyor (kullanım sınırı)"
        elif bitti=$(grep -o 'bitti, çıkış [0-9]*' "$f" | tail -n 1) && [[ -n $bitti ]]; then
            state="${bitti}"
            [[ $(grep -c '^== .* başladı:' "$f") -gt $(grep -c '^== .* bitti, çıkış' "$f") ]] && state="yarıda kaldı (yeniden?)"
        else
            state="yarıda kaldı (yeniden?)"
        fi
        printf '%-18s %-26s %s\n' "$a" "$state" "$last"
    done
    ;;
  log)
    ad=${1:?ad gerekli}
    if [[ ${2:-} == -f ]]; then tail -f "$LOGS/$ad.log"; else tail -n 30 "$LOGS/$ad.log"; fi
    ;;
  bekle)
    ad=${1:?ad gerekli}
    while systemctl --user is-active --quiet "d1-$ad"; do sleep 60; done
    tail -n 15 "$LOGS/$ad.log"
    grep -q "bitti, çıkış 0$" <(grep 'bitti, çıkış' "$LOGS/$ad.log" | tail -n 1)
    ;;
  durdur)
    ad=${1:?ad gerekli}
    systemctl --user stop "d1-$ad" && echo "d1-$ad durduruldu"
    ;;
  *)
    sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'
    return 2
    ;;
esac
}
main "$@"; exit $?
