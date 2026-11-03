"""Proje klasörleri. Bütün komutlar yollarını buradan alır (düzen: `data/README.md`)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"          # ham kaynak yanıtları, kaynak başına: bir site birkaç alanı besleyebilir
INTERIM_DIR = DATA_DIR / "interim"  # ara çıktılar

LIBRARY_DIR = DATA_DIR / "library"                  # asıl veri, alan ve koleksiyon başına (`catalog.Collection`)
KULLIYAT_DIR = LIBRARY_DIR / "risale" / "kulliyat"  # eşleme ve kaynak karşılaştırmaları bu koleksiyona bakar
QURAN_PATH = LIBRARY_DIR / "kuran" / "quran.json"   # Kur'ân katmanı
HADIS_PATH = LIBRARY_DIR / "hadis" / "matches.json" # Risale'deki hadislerin rivayetlerle eşlemesi (`hadis.py`)
LINKS_DIR = DATA_DIR / "links"                      # bağlar: alan/yöntem.jsonl (`links.py`); profiller ortak okur

DIST_DIR = DATA_DIR / "dist"        # profil başına kurulan veritabanı ve vektörler (`profiles.py`)
DB_PATH = DIST_DIR / "kisisel" / "risale.db"        # yerel veritabanı: hepsi
VECTORS_DIR = DIST_DIR / "kisisel" / "vectors"      # vektörlerin asıl deposu (ücretli çıkarılır, silinmemeli)
PUBLIC_DB_PATH = DIST_DIR / "genel" / "risale.db"   # genel sunucuya giden kopya: `private` eserler yok
PUBLIC_VECTORS_DIR = DIST_DIR / "genel" / "vectors" # asıl depodan süzülür (`embeddings export-public`)
