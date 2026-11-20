#!/usr/bin/env bash
# Sunucuda, `taslak` kullanıcısıyla çalışır (`scripts/taslak-sunucu.sh giris` çağırır; doğrudan çağrılmaz).
# Aboneliğin uzun ömürlü anahtarını alır, ~/.claude-token'a yazar ve bir model çağrısıyla sınar. Anahtar ekranda iki
# satıra bölünebilir (2026-11-21: yalnız ilk satır alınmıştı, 79 harf): boş satıra kadar okunur, boşluklar atılır.
~/.local/bin/claude setup-token
echo
echo "Anahtarı yapıştırın (iki satıra bölünmüşse ikisini de), sonra boş bir satırda Enter:"
t=""
while IFS= read -rs line; do [[ -z $line ]] && break; t="$t$line"; done
t=$(printf '%s' "$t" | tr -d ' \t\r\n')
umask 077
printf '%s' "$t" > ~/.claude-token
echo "kaydedildi (${#t} harf); sınanıyor…"
if CLAUDE_CODE_OAUTH_TOKEN="$t" timeout 120 ~/.local/bin/claude -p --model haiku "Yalnız 'tamam' yaz." 2>&1 | grep -qi tamam; then
    echo "GİRİŞ ÇALIŞIYOR"
else
    echo "GİRİŞ ÇALIŞMADI: yeniden deneyin"
fi
