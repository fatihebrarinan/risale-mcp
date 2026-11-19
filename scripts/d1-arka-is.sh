#!/usr/bin/env bash
# `d1-arka.sh baslat`ın hizmet içinde çalıştırdığı koşturucu (doğrudan çağrılmaz):
#   bash scripts/d1-arka-is.sh <ad> <komut …>
# Komutu çalıştırır, başlangıç ve bitişi günlüğe yazar; iş bitince (başarılı ya da değil) `data/d1`'de değişiklik
# varsa commit ve push eder (kullanıcının kuralı, 2026-11-19: yeniden üretilemeyen çıktılar her adımda depoya;
# yarıda kalan işin ödenmiş çıktıları da), masaüstüne bildirim düşer.
# Bütün gövde `main` işlevindedir: bash işlevi baştan sona okuyup çalıştırır, iş sürerken bu dosya değişse de
# çalışan iş etkilenmez.
main() {
    local ad=$1; shift
    echo "== $(date '+%F %T') başladı: $*"
    "$@"
    local rc=$?
    echo "== $(date '+%F %T') bitti, çıkış $rc"
    if [[ -d data/d1/.git && -n $(git -C data/d1 status --porcelain) ]]; then
        if git -C data/d1 add -A && git -C data/d1 commit -qm "d1-arka: $ad (çıkış $rc)" && git -C data/d1 push -q; then
            echo "== data/d1 commit ve push edildi"
        else
            echo "== UYARI: data/d1 commit ya da push edilemedi"
        fi
    fi
    command -v notify-send >/dev/null && notify-send -a d1 "Taslak hattı: $ad" "bitti, çıkış $rc" || true
    return $rc
}
main "$@"; exit $?
