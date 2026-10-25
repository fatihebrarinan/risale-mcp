"""Proje klasörleri. Bütün komutlar yollarını buradan alır."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"          # ham kaynak yanıtları
INTERIM_DIR = DATA_DIR / "interim"  # ara çıktılar
BOOKS_DIR = DATA_DIR / "books"      # her eserin nihai JSON'u
