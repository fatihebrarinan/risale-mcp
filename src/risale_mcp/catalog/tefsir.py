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
              "1418). Pilot: muhakkikin girişi, hutbe, Fâtiha ve Bakara 1–33 (T3); gerisi ayrıştırılmadı."),
)
