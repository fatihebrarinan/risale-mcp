"""Kaynak alınmayacak yazarlar ve eserler (kullanıcının kararı, 2026-11-06).

Bu listedeki bir yazarın ya da eserin metni hiçbir koleksiyona, hiçbir profile girmez: OpenITI'den indirilemez
(`sources.openiti.Text` kurulurken durur) ve katalogda yazarı olarak geçemez (`catalog` yüklenirken durur). Liste
`docs/mvp-kitaplar.md`'deki kararın koddaki karşılığıdır; bir kayıt yalnız kullanıcının kararıyla eklenir ya da çıkar.
"""

# OpenITI yolunun başı (yazar klasörü ya da `yazar.eser`) -> gerekçe
OPENITI: dict[str, str] = {
    "1323MuhammadCabduh": "Muhammed Abduh: kaynak alınmaz",
    "1354RashidRida.Manar": "Tefsîru'l-Menâr: Abduh'un derslerine dayanır, kaynak alınmaz",
}

# Katalogdaki `Work.author` içinde geçemeyecek adlar (küçük harfle, işaretsiz karşılaştırılır)
AUTHORS: dict[str, str] = {
    "abduh": "Muhammed Abduh: kaynak alınmaz",
    "menar": "Tefsîru'l-Menâr: kaynak alınmaz",
}


def openiti_reason(path: str) -> str | None:
    """OpenITI yolunun (`data/` sonrası) yasak listesinde olup olmadığı; varsa gerekçesi."""
    parts = path.split("/")
    for prefix, reason in OPENITI.items():
        if any(p == prefix or p.startswith(prefix + ".") or p.startswith(prefix + "/") for p in parts):
            return reason
    return None
