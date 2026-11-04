"""Müfessirlerin eserleri (`docs/tefsir-altyapi-plani.md`): OpenITI sürümleri, sabit commit'ten.

    uv run python -m risale_mcp.fetch tefsir        # data/raw/openiti/<anahtar>.txt ve .yml

Pilot Beyzâvî'nin Envârü't-Tenzîl'idir (T0). OpenITI'de beş sürümü var; hepsi indirilir, karşılaştırma ve nüsha
seçimi `docs/tefsir-altyapi-plani.md`'de (T0). Lisans CC BY-NC-SA 4.0 (`docs/izinler.md`, OpenITI satırı).
"""

from pathlib import Path

from risale_mcp.sources import openiti
from risale_mcp.sources.http import PoliteClient

COMMIT_0700 = "3d8ff4e7b035aaa4ca5dda52c7322645f3401dcf"          # OpenITI/0700AH, 2025-11-28
_BEYZAVI = "0685NasirDinBaydawi/0685NasirDinBaydawi.AnwarTanzil/0685NasirDinBaydawi.AnwarTanzil"
TEXTS = {
    "beyzavi-jk": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.JK000128-ara1"),
    "beyzavi-shamay": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.ShamAY0034065-ara1"),
    "beyzavi-shamela": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.Shamela0023588-ara1"),
    "beyzavi-shia": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.Shia002637Vols-ara1"),
    "beyzavi-tafsir": openiti.Text("0700AH", COMMIT_0700, f"{_BEYZAVI}.Tafsir01006-ara1"),
}


def fetch(root: Path, client: PoliteClient, *, refresh: bool = False) -> None:
    openiti.fetch(TEXTS, root, client, refresh=refresh)
