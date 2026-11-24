"""Klasik eserler (E2, `docs/e2-adaylar.md`): OpenITI sürümleri, sabit commit'ten.

    uv run python -m risale_mcp.fetch klasik        # data/raw/openiti/<anahtar>.txt ve .yml

Birinci dilim (kullanıcının seçimi, 2026-11-13): belâgat ve terim eserleri. Her eserin seçilen sürümü (`<eser>`) ve
baskısını doğrulamak için bir karşılaştırma sürümü (`<eser>-<kaynak>`) indirilir; metin yalnız seçilenden alınır.
Anahtar eserin kimliğidir: `data/raw/openiti/` alanlar arasında ortaktır (`delail` Beyhakî'nin Delâil'idir).
Lisans CC BY-NC-SA 4.0 (`docs/izinler.md`, OpenITI satırı).
"""

from pathlib import Path

from risale_mcp.sources import openiti
from risale_mcp.sources.http import PoliteClient

COMMITS = {                                      # 2026-11-13'te depoların son commit'i
    "0475AH": "cc9beb0d9645e8cdce892556423b9926a127054f",
    "0525AH": "6290621b58e063ed1aa47ffd0a6fc1630191e7cb",
    "0650AH": "15542bc9cc4373c7d7132735050ca1335060fd26",
    "0825AH": "bae1fba53712c020fe43e3e60b37dfe61f2b64a8",
    # E5 (2026-11-25'te depoların son commit'i)
    "0150AH": "f9a52b5bbc3a65673fc73fb32331e7f33811c480",
    "0775AH": "61b0c7891699554aeff8dffdb8b1a2a59d2d22ab",
    "0800AH": "5510794124fa4810c19e67582b38260e98b6baea",
    "0925AH": "4f0f4562d1e13083c593e3a0ca6a19a3eb33805e",
}
# anahtar -> (depo, yazar/eser klasörü, sürüm)
VERSIONS = {
    "delailul-icaz": ("0475AH", "0471CabdQahirJurjani/0471CabdQahirJurjani.DalailIcjaz", "Shamela0012055-ara1"),
    "delailul-icaz-jk": ("0475AH", "0471CabdQahirJurjani/0471CabdQahirJurjani.DalailIcjaz", "JK001019-ara1"),
    "esrarul-belaga": ("0475AH", "0471CabdQahirJurjani/0471CabdQahirJurjani.AsrarBalagha", "Shamela0008187-ara1"),
    "esrarul-belaga-shamay": ("0475AH", "0471CabdQahirJurjani/0471CabdQahirJurjani.AsrarBalagha", "ShamAY0032338-ara1"),
    "miftahul-ulum": ("0650AH", "0626IbnMuhammadKhwarazmiSakkaki/0626IbnMuhammadKhwarazmiSakkaki.MiftahCulum",
               "Shamela0026581-ara1"),
    "miftahul-ulum-jk": ("0650AH", "0626IbnMuhammadKhwarazmiSakkaki/0626IbnMuhammadKhwarazmiSakkaki.MiftahCulum",
                  "JK010081-ara1"),
    # Ta'rîfât: Shamela sürümü (DKİ 1403/1983) noktalamalı ve temiz; JK sürümünde (Ebyârî) OCR artıkları var
    "tarifat": ("0825AH", "0816IbnMuhammadSharifJurjani/0816IbnMuhammadSharifJurjani.Tacrifat", "Shamela0007312-ara1"),
    "tarifat-jk": ("0825AH", "0816IbnMuhammadSharifJurjani/0816IbnMuhammadSharifJurjani.Tacrifat", "JK000768-ara1"),
    # Müfredât: JK sürümü (Kîlânî) her maddeyi "kök : …" paragrafıyla verir, âyetleri işaretler; Shamela sürümünde
    # (Dâvûdî) madde başlığı işareti yer yer kelimelerin içine girmiş ("[الح|شر|/ 14]"): metin kurulamıyor
    "mufredat": ("0525AH", "0502RaghibIsbahani/0502RaghibIsbahani.Mufradat", "JK001150-ara1"),
    "mufredat-shamela": ("0525AH", "0502RaghibIsbahani/0502RaghibIsbahani.Mufradat", "Shamela0023636-ara1"),
    # E5 (2. dilim ve el-Mevâhib, kullanıcının seçimi 2026-11-24; `docs/e5-risalede-anilan-eserler.md`).
    # Şerhu'l-Mevâkıf: OpenITI'de Îcî'nin adı altında "المواقف" diye durur, içi Seyyid Şerîf'in şerhidir (Umeyre,
    # Dâru'l-Cîl 1997); metin "# المتن #" ile ayrılır. Şârihin adıyla duran tek sürüm OCR'dır (Kraken).
    # Aynı baskının iki sürümü: ShamAY başlıklı (Şâmile'nin içindekilerinden, "AUTO"), JK başlıksız; metin ShamAY'den.
    "serhul-mevakif": ("0775AH", "0756CadudDinIji/0756CadudDinIji.Mawaqif", "ShamAY0033881-ara1"),
    "serhul-mevakif-jk": ("0775AH", "0756CadudDinIji/0756CadudDinIji.Mawaqif", "JK001335-ara1"),
    "serhul-makasid": ("0800AH", "0792IbnCumarTaftazani/0792IbnCumarTaftazani.SharhMaqasid", "JK001157-ara1"),
    "serhul-makasid-shamay": ("0800AH", "0792IbnCumarTaftazani/0792IbnCumarTaftazani.SharhMaqasid",
                              "ShamAY0033884-ara1"),
    # Telvîh: JK sürümü yalnız Teftâzânî'nin şerhidir (Tavzîh karışmamış), başlıksız; ShamAY sürümü aynı baskıda
    # (Umeyrât) Tavzîh'le sayfa sayfa iç içe, başlıklı: başlıklar ondan, metin eşleştirilerek alınır.
    "telvih": ("0800AH", "0792IbnCumarTaftazani/0792IbnCumarTaftazani.TalwihCalaTawdih", "JK007110-ara1"),
    "telvih-shamela": ("0800AH", "0792IbnCumarTaftazani/0792IbnCumarTaftazani.TalwihCalaTawdih",
                       "Shamela0009508-ara1"),
    "telvih-shamay": ("0800AH", "0792IbnCumarTaftazani/0792IbnCumarTaftazani.SharhTalwih", "ShamAY0034200-ara1"),
    # Munkız: ShamAY (Câbir) baskının paragraflarıyla; JK aynı baskı, 23 uzun paragraf.
    "munkiz": ("0525AH", "0505Ghazali/0505Ghazali.Munqidh", "ShamAY0033739-ara1"),
    "munkiz-jk": ("0525AH", "0505Ghazali/0505Ghazali.Munqidh", "JK009330-ara1"),
    "fikhul-ekber": ("0150AH", "0150AbuHanifa/0150AbuHanifa.FiqhAkbar", "Shamela0006388-ara1"),
    "mevahib": ("0925AH", "0923AhmadQastallani/0923AhmadQastallani.MawahibLaduniyya", "Shamela0023685-ara1"),
    "ihya": ("0525AH", "0505Ghazali/0505Ghazali.IhyaCulumDin", "JK000001-ara1"),
    "ihya-shamela": ("0525AH", "0505Ghazali/0505Ghazali.IhyaCulumDin", "Shamela0009472-ara1.completed"),
}
TEXTS = {key: openiti.Text(repo, COMMITS[repo], f"{folder}/{folder.rsplit('/', 1)[1]}.{version}")
         for key, (repo, folder, version) in VERSIONS.items()}


def fetch(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    openiti.fetch(TEXTS, root, client, refresh=refresh)
