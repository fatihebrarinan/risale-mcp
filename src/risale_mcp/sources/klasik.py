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
}
TEXTS = {key: openiti.Text(repo, COMMITS[repo], f"{folder}/{folder.rsplit('/', 1)[1]}.{version}")
         for key, (repo, folder, version) in VERSIONS.items()}


def fetch(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    openiti.fetch(TEXTS, root, client, refresh=refresh)
