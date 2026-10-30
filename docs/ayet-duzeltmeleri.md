# Âyet adresi düzeltmeleri

Kullanıcının kararı (2026-10-30): Kur'ân esastır, ama müellifin sözü değiştirilmez. Her kayıt aşağıdakilerden biridir.

- **Yanlış numara:** metin başka bir âyete tam oturuyor; yalnız adres düzeltilir, metin aynen kalır.
  `arabic_kinds.AYAH_FIXES` (9 kayıt).
- **Aralık:** kaynak birkaç âyet saymış ("2:19, 20"), ilki alınıyordu; aralık tam yazıldı (4 kayıt, aynı tablo).
- **İktibas ya da tekrar:** müellif âyeti uyarlamış, kısaltmış ya da tekrarlamış ("يَٓا اَهْلَ الْكِتَابِ يَٓا اَهْلَ الْكِتَابِ").
  Metin aynen kalır, `ayah_check = iktibas`; araç âyetin tam metnini ayrıca verir. Liste: `data/interim/quran/ayah_check.md`.
- **İmlâ ve hat farkı:** Türk mushafı ile Medine hattı farkına dokunulmaz, harf iskeleti tutuyorsa tam eşleşmedir.

## Potansiyel hatalılar

Kullanıcının kararı (2026-10-30): `ayah_check = dizgi_suphesi` (`arabic_kinds.AYAH_SUSPECTS`), metin değişmez, araç modele
uyarı verir. Karşılaştırılan öbür baskılarda da aynı yazılıdır.

| Yer | Metindeki | Kur'ân | Not |
|---|---|---|---|
| `muhakemat/makale-01/mukaddeme-08/p015` | قَدْ جَٓاءَ الْحَقُّ وَزَهَقَ الْبَاطِلُ | İsrâ 17:81 قُلْ جَٓاءَ الْحَقُّ | Âsâr-ı Bediiyye'de de "قد" |
| `lemalar/28/nukte-26/p003` | وَخَلَقَ لَكُمْ مِنَ الْاَنْعَامِ | Zümer 39:6 وَاَنْزَلَ لَكُمْ | Aynı cildin öbür yerlerinde "اَنْزَلَ"; Osmanlıca baskıda burada da "خَلَقَ" |
| `sozler/fihrist/soz-33/pencere-20/p002` | مَٓاءً مُبَارَكًا فَاَسْقَيْنَاكُمُوهُ | Hicr 15:22 مَٓاءً فَاَسْقَيْنَاكُمُوهُ | "مُبَارَكًا" Kâf 50:9'dan; iki âyetin birleşmesi olabilir; Osmanlıca baskıda da aynı |
