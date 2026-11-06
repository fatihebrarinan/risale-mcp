"""Müfessirlerin eserleri (`docs/tefsir-altyapi-plani.md`): koleksiyon `tefsir`, ad alanı `tefsir:`.

Eserler kendi metinlerinin sahibidir (`author`); muhakkik `editor`'dadır, girişi ayrı katmandır (düğümde `authority:
muhakkik`). Pilot bitene kadar hepsi `private`: genel sunucuya sonuçlar görüldükten sonra ayrı kararla çıkar.
"""

from risale_mcp.catalog.model import Collection, Group, Site, SourceRef, Work

TEFSIR_WORKS: tuple[Work, ...] = (
    Work("beyzavi", "Envârü't-Tenzîl", Group.TEFSIR, SourceRef(Site.OPENITI, "beyzavi-shamela"),
         language="ar", private=True, collection=Collection.TEFSIR,
         author="Nâsırüddîn el-Beyzâvî", editor="Muhammed Abdurrahman el-Maraşlî",
         note="Envârü't-Tenzîl ve Esrârü't-Te'vîl. OpenITI Shamela0023588 (Maraşlî tahkiki, Dâru İhyâi't-Türâsi'l-Arabî, "
              "1418). Eserin tamamı (MVP; pilot T3'te Bakara 33'e kadardı)."),
) + tuple(
    Work(slug, title, Group.TEFSIR, SourceRef(Site.OPENITI, f"{slug}-shamela"), language="ar", private=True,
         collection=Collection.TEFSIR, author=author, editor=editor,
         note=f"OpenITI {version} ({edition}); âyet birimleri altafsir.com sürümünden (MVP, `books/tefsir_openiti.py`).")
    for slug, title, author, editor, version, edition in (
        # MVP (`docs/mvp-kitaplar.md`): muhakkik yalnız üst bilginin söylediği; yoksa boş (tahmin edilmez)
        ("taberi", "Câmiu'l-Beyân", "Muhammed b. Cerîr et-Taberî", "Abdullah b. Abdülmuhsin et-Türkî",
         "Shamela0007798", "Dâru Hecr, 1422"),
        ("maturidi", "Te'vîlâtü'l-Kur'ân", "Ebû Mansûr el-Mâtürîdî", "Mecdî Bâslûm",
         "Shamela0095590", "Dâru'l-Kütübi'l-İlmiyye, 1426"),
        ("kessaf", "el-Keşşâf", "Cârullah ez-Zemahşerî", None, "Shamela0023627", "Dâru'l-Kitâbi'l-Arabî, 3. baskı 1407"),
        ("razi", "Mefâtîhu'l-Gayb", "Fahreddîn er-Râzî", None, "Shamela0023635", "Dâru İhyâi't-Türâs, 3. baskı 1420"),
        ("kurtubi", "el-Câmi' li-Ahkâmi'l-Kur'ân", "Ebû Abdullah el-Kurtubî", "Ahmed el-Berdûnî ve İbrâhîm Atfeyyiş",
         "Shamela0020855", "Dâru'l-Kütübi'l-Mısriyye, 2. baskı 1384"),
        ("nesefi", "Medâriku't-Tenzîl", "Ebü'l-Berekât en-Nesefî", "Yûsuf Ali Bedîvî",
         "Shamela0001394", "Dâru'l-Kelimi't-Tayyib, 1419"),
        ("ibnkesir", "Tefsîru'l-Kur'âni'l-Azîm", "İbn Kesîr", "Sâmî b. Muhammed Selâme",
         "Shamela0008473", "Dâru Tayyibe, 2. baskı 1420"),
        ("celaleyn", "Tefsîru'l-Celâleyn", "Celâleddîn el-Mahallî ve Celâleddîn es-Suyûtî", None,
         "Shamela0012876", "Dâru'l-Hadîs, Kahire"),
        ("durr", "ed-Dürrü'l-Mensûr", "Celâleddîn es-Suyûtî", None, "Shamela0012884", "Dâru'l-Fikr, Beyrut"),
        ("ebussuud", "İrşâdü'l-Akli's-Selîm", "Ebüssuûd Efendi", None, "Shamela0001429", "Dâru İhyâi't-Türâs, Beyrut"),
        ("bursevi", "Rûhu'l-Beyân", "İsmâil Hakkı Bursevî", None, "Shamela0023612", "Dâru'l-Fikr, Beyrut"),
        ("alusi", "Rûhu'l-Meânî", "Şihâbüddîn el-Âlûsî", "Ali Abdülbârî Atıyye",
         "Shamela0022835", "Dâru'l-Kütübi'l-İlmiyye, 1415"),
    )
)
