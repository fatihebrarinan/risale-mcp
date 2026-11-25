#!/usr/bin/env bash
# Girişli taslak bölümüne (risalemcp.com/taslak/) tek tek sayfa gönderir: okuma sayfaları, masa (S5).
#
#   scripts/taslak-gonder.sh data/d1/masa/tur-21-22-D15.1.html [başka sayfa …]
#
# `deploy.sh --code` taslak bölümünün tamamını (`data/d1/masa/`) gönderir ama kodu, siteyi, servisleri ve araç çıktısı
# kaydını da çalıştırır; bir okuma sayfası için gereksiz (kullanıcının isteği, 2026-11-19). Bu betik yalnız verilen
# dosyaları `deploy.sh`'in taslak bölümündeki izin ve sahiplikle koyar; sunucudaki başka hiçbir şeye dokunmaz.
# Sayfalar `data/d1/masa/` altında olmalı (kapalı depo; site/ klasörüne girmez).
set -euo pipefail

HOST="${RISALE_HOST:-root@100.108.174.19}"   # Tailscale adresi; SSH internete kapalı
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
SSH=(ssh -i "$KEY" -o BatchMode=yes)
cd "$(dirname "$0")/.."

[[ $# -ge 1 ]] || { echo "kullanım: scripts/taslak-gonder.sh data/d1/masa/<sayfa>.html …"; exit 2; }
for f in "$@"; do
    [[ -f $f ]] || { echo "yok: $f"; exit 1; }
    [[ $(realpath "$f") == $(realpath data/d1/masa)/* || $(realpath "$f") == $(realpath data/interim/oku-masa)/* \
       || $(realpath "$f") == $(realpath -m data/interim/sohbet)/* ]] \
        || { echo "data/d1/masa/, data/interim/oku-masa/ ya da data/interim/sohbet/ altında değil: $f"; exit 1; }
done
"${SSH[@]}" "$HOST" "install -d -o root -g caddy -m 750 /var/www/ozel && install -d -o root -g caddy -m 2750 /var/www/ozel/taslak"
rsync -az --chown=root:caddy --chmod=D2750,F640 -e "${SSH[*]}" "$@" "$HOST:/var/www/ozel/taslak/"
for f in "$@"; do
    echo "https://risalemcp.com/taslak/$(basename "$f")"
done
