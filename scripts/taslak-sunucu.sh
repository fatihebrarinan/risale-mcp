#!/usr/bin/env bash
# D5'in taslak hattı sunucuda (kullanıcının kararı, 2026-11-20: bilgisayar bir ay açık kalmasın; yer tefsir makinesi,
# "A" yolu). Ayrı kullanıcı `taslak`: genel hizmetin kullanıcısından (`risale`) ayrı; aboneliğin giriş anahtarı
# (`claude setup-token`) ve özel taslak deposunun yazma anahtarı yalnız onun ev klasöründe durur. İşler düşük
# öncelikle (`d1-arka.sh`, Nice=10) döner; genel tefsir ve klasik hizmetleri önce gelir.
#
#   scripts/taslak-sunucu.sh kur        # kullanıcı, uv, claude komutu, linger, data/d1 için anahtar (bir kez)
#   scripts/taslak-sunucu.sh gonder     # kod (git ls-files) ve VOYAGE anahtarı (evden; küçük)
#   scripts/taslak-sunucu.sh veri       # D5'in veritabanları, vektörleri, quran.json: sunucudan sunucuya
#   scripts/taslak-sunucu.sh ozet       # yerel ve sunucudaki verinin özetleri aynı mı
#   scripts/taslak-sunucu.sh giris      # aboneliğin giriş anahtarı (kullanıcı, kendi terminalinde; bir kez)
#   scripts/taslak-sunucu.sh d1         # data/d1'i özel depodan klonlar ya da çeker (deploy anahtarı eklendikten sonra)
#   scripts/taslak-sunucu.sh calistir <komut …>   # sunucuda, taslak kullanıcısıyla, depo kökünde (ör. scripts/d1-arka.sh liste)
#   scripts/taslak-sunucu.sh durum      # bellek, disk, d1 işleri, kullanım penceresi
#
# Kullanıcının bir kez yapacağı: `giris` (tarayıcı onayı; anahtar sohbete girmez, `~/.claude-token`'a yazılır,
# `d1-arka-is.sh` oradan okur). `kur`'un yazdığı açık anahtar özel depoya yazma izinli "deploy key" olarak eklendi
# (2026-11-20, `gh repo deploy-key add`).
set -euo pipefail
HOST="${TASLAK_HOST:-root@100.98.98.62}"   # tefsir-mcp (Hetzner CAX21, 8 GB; Tailscale)
KEY="${RISALE_KEY:-$HOME/.ssh/risale_hetzner}"
U=taslak
DEST=/home/$U/risale-mcp
SSH=(ssh -i "$KEY" -o BatchMode=yes)
cd "$(dirname "$0")/.."
as_u() { "${SSH[@]}" "$HOST" "su - $U -c $(printf '%q' "$1")"; }

case "${1:-}" in
kur)
    "${SSH[@]}" "$HOST" "set -e
        id $U >/dev/null 2>&1 || useradd -m -s /bin/bash $U
        loginctl enable-linger $U
        mkdir -p $DEST && chown -R $U:$U /home/$U"
    as_u "set -e
        command -v ~/.local/bin/uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null
        command -v ~/.local/bin/claude >/dev/null || curl -fsSL https://claude.ai/install.sh | bash >/dev/null
        ~/.local/bin/claude --version
        mkdir -p ~/.ssh && chmod 700 ~/.ssh
        [ -f ~/.ssh/d1_deploy ] || ssh-keygen -q -t ed25519 -N '' -C 'risale-mcp-taslak deploy (tefsir-mcp)' -f ~/.ssh/d1_deploy
        grep -q 'Host github.com' ~/.ssh/config 2>/dev/null || printf 'Host github.com\n  IdentityFile ~/.ssh/d1_deploy\n  IdentitiesOnly yes\n' >> ~/.ssh/config
        ssh-keyscan -T 20 github.com >> ~/.ssh/known_hosts 2>/dev/null || true; sort -u -o ~/.ssh/known_hosts ~/.ssh/known_hosts
        git config --global user.name 'risale-mcp taslak (sunucu)'
        git config --global user.email 'taslak@risalemcp.invalid'
        echo 'data/d1 için deploy anahtarı (açık):'; cat ~/.ssh/d1_deploy.pub"
    ;;
gonder)
    # Evden yalnız kod gider (≈6 MB): ev bağlantısı sunucuya yavaş (2026-11-20: ≈15 KB/s, %30 yeniden gönderim).
    "${SSH[@]}" "$HOST" "mkdir -p $DEST && chown $U:$U $DEST"
    git ls-files -z | rsync -az --from0 --files-from=- -e "${SSH[*]}" ./ "$HOST:$DEST/"
    grep '^VOYAGE_API_KEY=' .env | "${SSH[@]}" "$HOST" "cat > $DEST/.env && chmod 600 $DEST/.env"
    "${SSH[@]}" "$HOST" "chown -R $U:$U $DEST"
    as_u "cd $DEST && ~/.local/bin/uv sync --frozen -q && echo kod hazır"
    ;;
veri)
    # Veri sunucudan sunucuya: tefsir, klasik ve quran.json bu makinedeki genel hizmetten (risale kullanıcısı), genel
    # ve hadis ana makineden (Tailscale `risale`; ssh anahtarı yerel ajandan, -A). Yayındaki kopyalar yereldekiyle
    # aynı olmalı: önce özetler karşılaştırılır (`ozet`), farklıysa yerelden gönderilir.
    "${SSH[@]}" -A "$HOST" "set -e; mkdir -p $DEST/data/dist $DEST/data/library/kuran
        for d in tefsir klasik; do rsync -a --delete /home/risale/risale-mcp/data/dist/\$d/ $DEST/data/dist/\$d/; done
        cp /home/risale/risale-mcp/data/library/kuran/quran.json $DEST/data/library/kuran/
        for d in genel hadis; do rsync -az --delete -e 'ssh -o StrictHostKeyChecking=accept-new' root@${ANA:-100.108.174.19}:/home/risale/risale-mcp/data/dist/\$d/ $DEST/data/dist/\$d/; done
        chown -R $U:$U $DEST/data; du -sh $DEST/data/dist/*"
    ;;
ozet)
    # D5'in verisinin özetleri: yerel ve bu sunucudaki kopya (aynı olmalı)
    L='data/dist/genel/risale.db data/dist/genel/vectors/* data/dist/hadis/hadis.db data/dist/hadis/vectors/* data/dist/tefsir/risale.db data/dist/tefsir/vectors/* data/dist/klasik/risale.db data/dist/klasik/vectors/* data/library/kuran/quran.json'
    diff <(bash -c "for f in $L; do echo \$(sha1sum < \$f | cut -c1-12) \$f; done") \
         <("${SSH[@]}" "$HOST" "cd $DEST && for f in $L; do echo \$(sha1sum < \$f | cut -c1-12) \$f; done") \
        && echo "veri aynı"
    ;;
giris)
    # Kullanıcı kendi terminalinde çalıştırır (Claude Code'da `!` ile değil: anahtar sohbete girmesin). Tarayıcıda onay,
    # sonra komutun yazdığı anahtar yapıştırılır; ekrana basılmadan ~/.claude-token'a (yalnız taslak okur) yazılır.
    ssh -i "$KEY" -t "$HOST" "su - $U -c '~/.local/bin/claude setup-token; umask 077; read -rsp \"Yukarıdaki anahtarı yapıştırıp Enter: \" t; echo; printf %s \"\$t\" > ~/.claude-token; echo kaydedildi'"
    ;;
d1)
    as_u "set -e; cd $DEST
        if [ -d data/d1/.git ]; then git -C data/d1 pull -q --ff-only && echo 'data/d1 çekildi';
        else git clone -q git@github.com:fatihebrarinan/risale-mcp-taslak.git data/d1 && echo 'data/d1 klonlandı'; fi
        git -C data/d1 log --oneline -1"
    ;;
calistir)
    shift
    as_u "cd $DEST && export PATH=\$HOME/.local/bin:\$PATH XDG_RUNTIME_DIR=/run/user/\$(id -u) && $(printf '%q ' "$@")"
    ;;
durum)
    "${SSH[@]}" "$HOST" "free -m | sed -n 2p; df -h / | tail -1; uptime"
    as_u "cd $DEST && export PATH=\$HOME/.local/bin:\$PATH XDG_RUNTIME_DIR=/run/user/\$(id -u) && (scripts/d1-arka.sh liste 2>/dev/null | head -8 || true)"
    ;;
*)
    sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
esac
