"""D12.4 üslûp belgesi (PLANLAR.md D12): İşârâtü'l-İ'câz'ın Arapça aslından, programla çıkarılan anlatım kalıpları.

    uv run python scripts/d1-uslup.py                 # docs/d1/uslup-belgesi.md (bütün eser; D5 için)
    uv run python scripts/d1-uslup.py --prova 31-33   # data/interim/d1-prova/31-33/ek-uslup.md (sınanan birim hariç) + sızıntı testi

Kararlar (kullanıcı, 2026-11-16): üslûp belgesi İşârât'ın kendi Arapçasından **mekanik** çıkarılır: kalıp, sıklık,
cümle kimlikli örnek; yorum yok, yorum gereken yer "[Çıkarım]" diye ayrılır. Belge yazımın biçimine yardım eder
(D8: biçim kuralları tutuyor, düşünme kuralları tutmuyor); düşünmeyi yapılı akış (D12.5) üstlenir. İkinci işi
nakil ile istinbatın oranını göstermek: eserin cümlelerinin kaçında bir âlimin ya da eserin adı geçer (D12.1'in dersi:
kaynağa bağlılık kuralı müellifin kendi nüktelerini caydırıyordu).

Sayım: Arapça asıl (`isaratul-icaz-arabi`), hareke ve tatvil atılarak; bir kalıp bir cümlede bir kez sayılır.
"Birim" Fâtiha'da kelime bölümü, Bakara'da âyet birimidir (yolun ilk iki parçası). Örnekler sabit tohumla, farklı
birimlerden seçilir; prova kopyasında sınanan birimin düğümleri hem sayımdan hem örneklerden çıkar.
"""

import argparse
import importlib.util
import random
import re
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

from risale_mcp.paths import ROOT

_spec = importlib.util.spec_from_file_location("d1_prova", ROOT / "scripts" / "d1-prova.py")
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)

WORK = "isaratul-icaz-arabi"
OUT = ROOT / "docs" / "d1" / "uslup-belgesi.md"
HAR = re.compile(r"[ً-ٰٟۖ-ۭـ]")
SAMPLES = 2

# Kalıplar: (ad, düzenli ifade harekesiz metinde, açıklama). Gruplar anlatımdaki işleve göre (derleyenin tasnifi).
GROUPS = [
    ("Açılış ve geçiş", "Bir bahsin ve bir vechin nasıl açıldığı.", [
        ("اعلم أن", r"^\s*(?:ثم\s+)?اعلم\s+أن", "bahsin açılışı"),
        ("لهذه الآية … الوجوه الثلاثة", r"الوجوه\s+الثلاثة", "üç vechin anılması"),
        ("أما نظمها/نظم … بسابقتها/بما قبلها", r"(?:نظمها|نظم\s+\S+)\s+(?:ب|مع\s+)(?:سابق|ما\s+قبل)", "birinci vecih: öncesiyle nazım"),
        ("وأما نظم الجمل", r"نظم\s+(?:ال)?جمل", "ikinci vecih: cümlelerin nazmı"),
        ("وأما … الهيئات / جملة جملة", r"(?:هيئات|كيفية\s+جملة|جملة\s+جملة|نظم\s+هيئات)", "üçüncü vecih: hey'etler"),
        ("وأما ﴿…﴾", r"^\s*وأما\s*﴿", "üçüncü vecihte bir lafzın ele alınışı"),
    ]),
    ("Delâlet derecesi", "Bir nüktenin lafızdan ne kuvvette çıktığı (usul özeti 2.3).", [
        ("إشارة / يشير", r"(?:إشارة|يشير|أشار|تشير)", "işaret"),
        ("رمز / يرمز", r"(?:رمز|يرمز|ترمز)", "remiz"),
        ("إيماء / يومئ", r"(?:إيماء|يومئ|تومئ|أومأ)", "îmâ"),
        ("تلويح / يلوح", r"(?:تلويح|يلوح|تلوح|لوّح|لوح\s+إلى)", "telvih"),
        ("تعريض", r"تعريض", "ta'rîz"),
        ("صريح / تصريح / نص", r"(?:صريح|تصريح|صرّح|صرح\s+ب|بالنص)", "sarih"),
        ("كناية", r"كناية", "kinaye"),
    ]),
    ("Takdir ve mukadder sual", "Söylenmeyenin açılışı (usul özeti 2.4; Muhâkemât On Birinci Mes'ele).", [
        ("كأنه قيل", r"كأنه\s+قيل|كأن(?:ه|ها)?\s+(?:يقول|قال|تقول)", "dinleyenin sorusu"),
        ("فإن قلت / قلت / قيل لك", r"(?:فإن\s+قلت|إن\s+قلت|قيل\s+لك|^\s*قلت)", "mukadder itiraz ve cevap"),
        ("سؤال مقدر / جواب سؤال", r"سؤال\s+مقدر|جواب\s+(?:ل)?سؤال|جواب\s+عن\s+سؤال", "sualin adıyla"),
        ("تقديره / أي", r"(?:تقديره|والتقدير|التقدير|^\s*أي\b|\sأي\s)", "takdir ve izah"),
        ("مقدّر / محذوف", r"(?:مقدر|محذوف|المحذوف|حذف)", "hazif ve takdir"),
    ]),
    ("Hey'et ve harf", "Bir lafzın neden öyle geldiği (usul özeti 4.3).", [
        ("التنكير / التعريف", r"(?:تنكير|التعريف|تعريف)", "ta'rif ve tenkir"),
        ("التقديم / التأخير", r"(?:تقديم|التأخير|تأخير|قدّم|قدم\s)", "takdim ve te'hir"),
        ("الحصر / القصر", r"(?:الحصر|حصر|القصر|قصر)", "hasr"),
        ("العطف / الفصل", r"(?:العطف|عطف|الفصل|ترك\s+العطف)", "atf ve fasl"),
        ("صيغة / الجمع / الإفراد", r"(?:صيغة|الجمع|الإفراد|الافراد)", "sîga"),
        ("حرف … (الواو، الفاء، ثم، إنّ، قد)", r"(?:لفظ|حرف|كلمة)\s+[«\"]?(?:الواو|الفاء|ثم|إن|قد|لام|الباء|على|في|من)", "harfin adıyla"),
    ]),
    ("Garaz ve toplayış", "Kayıtların asıl maksada bağlanışı (usul özeti 3.2; Muhâkemât Dördüncü Mes'ele).", [
        ("الغرض / المقصود / المقصد", r"(?:الغرض|المقصود|المقصد|مقصد)", "asıl maksat"),
        ("المقام / يقتضي / مقتضى", r"(?:المقام|مقام|يقتضي|مقتضى|اقتضاء)", "makam ve iktiza"),
        ("فتأمل / فانظر / وقس", r"(?:فتأمل|تأمل|فانظر|وقس|فقس|قس\s+عليه)", "okura bırakılan"),
        ("الحاصل / فالحاصل", r"(?:الحاصل|حاصله|فحاصل)", "toplayış"),
    ]),
    ("İhtimal ve çekince", "Hükmün kuvveti; tek vecih mi, vecihlerden biri mi.", [
        ("يحتمل / ويحتمل", r"(?:يحتمل|احتمال|محتمل)", "ihtimal"),
        ("لعل / ولا يبعد / يمكن", r"(?:لعل|لا\s+يبعد|يمكن|يجوز)", "imkân"),
        ("أو … (وجهان، وجوه)", r"(?:وجهان|وجوه|الوجه\s+(?:الأول|الثاني|الثالث))", "birden çok vecih"),
    ]),
    ("Temsil ve benzetme", "Soyut bağın misalle gösterilmesi (usul özeti 2.5; Muhâkemât Üçüncü ve Yedinci Mes'ele).", [
        ("كما / مثل / كأن", r"(?:^\s*كما\s|\sكمثل|كأن(?!ه\s+قيل))", "benzetme"),
        ("مثال / تمثيل", r"(?:مثال|تمثيل|مثلاً)", "misal ve temsil"),
    ]),
]

# Nakil: bir âlimin ya da eserin adı (usul özeti 7'deki liste ve tefsir eklentisinin müfessirleri)
NAMES = [r"الزمخشري", r"الكشاف", r"السكاكي", r"المفتاح", r"عبد\s+القاهر", r"الجرجاني", r"دلائل\s+الإعجاز",
         r"أسرار\s+البلاغة", r"البيضاوي", r"الرازي", r"فخر\s+الدين", r"سيبويه", r"التفتازاني", r"السعد\b",
         r"السيد\s+(?:الشريف|الجرجاني)", r"ابن\s+عباس", r"المفسر(?:ين|ون)", r"أهل\s+التفسير", r"الأشعري",
         r"المعتزلة", r"أهل\s+السنة", r"قال\s+بعض", r"قال\s+بعضهم", r"بعض\s+المفسرين", r"(?<!لما )(?<!لمّا )قيل\s*:\s*(?!\s*﴿)"]
# "قيل لك" takdir kalıbıdır (mukadder itirazın cevabı), nakil sayılmaz
NAME_EXCLUDE = re.compile(r"قيل\s+لك")
NAME_RE = re.compile("|".join(NAMES))


def plain(t: str) -> str:
    return HAR.sub("", t).replace("أ", "أ")


def unit_of(nid: str) -> str:
    parts = nid.split("/")
    return "/".join(parts[1:3]) if len(parts) > 2 else parts[1] if len(parts) > 1 else nid


def load(exclude: list[str]) -> list[tuple[str, str, str, str]]:
    conn = sqlite3.connect(f"file:{P.GENEL_DB}?mode=ro", uri=True)
    rows = conn.execute("SELECT id, node_id, paragraph_id, text FROM sentences WHERE id LIKE ? ORDER BY seq",
                        (WORK + "/%",)).fetchall()
    return [r for r in rows if not any(r[1] == x or r[1].startswith(x + "/") for x in exclude)]


def short(t: str, n: int = 170) -> str:
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"


def build(exclude: list[str], label: str) -> str:
    rows = load(exclude)
    rng = random.Random("d12-uslup")
    L = ["# İşârâtü'l-İ'câz'ın anlatım kalıpları: Arapça aslından sayım (D12.4)", "",
         "> **Bu belge nedir.** İşârâtü'l-İ'câz'ın Arapça aslında tekrar eden anlatım kalıplarının programla çıkarılmış "
         "dökümüdür (`scripts/d1-uslup.py`, `PLANLAR.md` D12.4). Usul özeti (`usul-ozeti.md`) eserin **ne yaptığını**, bu "
         "belge **nasıl söylediğini** gösterir. Sayılar kelime taramasıdır (hareke atılarak; bir kalıp bir cümlede bir kez), "
         "yaklaşık okunmalıdır; kalıpların gruplanması derleyenindir. Örnekler veritabanındaki cümlelerdir, kimlikleriyle; "
         "uzun olanlar kısaltılmıştır (\" …\"). Tercüme verilmez.",
         f"> **Kapsam.** {label}", ""]
    n_sent = len(rows)
    units = {unit_of(nid) for _, nid, _, _ in rows}
    words = [len(plain(t).split()) for _, _, _, t in rows]
    paras = defaultdict(int)
    for _, _, pid, _ in rows:
        paras[pid] += 1
    q = statistics.quantiles(words, n=4)
    L += ["## 1. Ölçüler", "",
          f"- {n_sent:,} cümle, {len(units)} birim, {len(paras):,} paragraf.".replace(",", "."),
          f"- Cümle uzunluğu (kelime): ortanca {statistics.median(words):.0f}, çeyrekler {q[0]:.0f}–{q[2]:.0f}, en uzun {max(words)}.",
          f"- Paragraf başına cümle: ortanca {statistics.median(paras.values()):.0f}, ortalama {statistics.mean(paras.values()):.1f}.",
          "- **[Çıkarım]** Bir nükte çoğunlukla bir iki cümledir: îcâz cümle sayısında değil, cümlenin yükündedir; kayıtlar "
          "\"..\" ve \"؛\" ile aynı cümlede dizilir.", ""]
    named = [r for r in rows if NAME_RE.search(NAME_EXCLUDE.sub("", plain(r[3])))]
    L += ["## 2. Nakil ve istinbat", "",
          f"Cümlelerin **{len(named)}**'inde (%{100 * len(named) / n_sent:.1f}) bir âlimin, bir eserin, bir mezhebin ya da "
          "\"قيل:\", \"قال بعض\" ile bir kavlin adı geçer (\"قيل لك\" takdir kalıbıdır, sayılmaz); geri kalanında müellif "
          "kaynak anmadan konuşur. Ad aramadır, yaklaşık okunmalı. Ad geçen birimler: "
          f"{len({unit_of(r[1]) for r in named})}/{len(units)}.", "",
          "- **[Çıkarım]** Eserin nükteleri büyük çoğunlukla **istinbattır**: âyetin lafzından, hey'etinden ve makamından "
          "kaynak anmadan çıkarılır (usul özeti 1.4: me'hazsiz yazıldı; 2.7: \"harice boykotaj\"). Nakil azdır ve adıyla "
          "yapılır. Taslakta da nakil kaynağa bağlı ve numaralı olmalı; istinbat ise kaynak aranmadan, etiketiyle ve "
          "gerekçesi lafza bağlı yazılabilmeli.", "",
          "Ad geçen cümlelerden örnek:", ""]
    for sid, _, _, t in rng.sample(named, min(3, len(named))):
        L.append(f"- `{sid}`: {short(t)}")
    L.append("")
    sec = 3
    for gname, gdesc, pats in GROUPS:
        L += [f"## {sec}. {gname}", "", gdesc, "", "| Kalıp | İşi | Cümle | Birim |", "|---|---|---:|---:|"]
        examples = []
        for name, rx, what in pats:
            r = re.compile(rx)
            hits = [x for x in rows if r.search(plain(x[3]))]
            L.append(f"| {name} | {what} | {len(hits)} | {len({unit_of(h[1]) for h in hits})} |")
            by_unit = defaultdict(list)
            for h in hits:
                if len(h[3]) <= 400:
                    by_unit[unit_of(h[1])].append(h)
            picked_units = rng.sample(sorted(by_unit), min(SAMPLES, len(by_unit)))
            examples.append((name, [rng.choice(by_unit[u]) for u in picked_units]))
        L += ["", "Örnekler:", ""]
        for name, ex in examples:
            for sid, _, _, t in ex:
                L.append(f"- *{name}* · `{sid}`: {short(t)}")
        L.append("")
        sec += 1
    # bir lafzın ele alınışı: "وأما ﴿…﴾" ile açılan kısa paragraflar (üçüncü vecihten), bütün olarak
    starts = defaultdict(list)
    for sid, nid, pid, t in rows:
        starts[pid].append((sid, t))
    cand = [v for v in starts.values() if re.match(r"\s*وأما\s*﴿", plain(v[0][1])) and 180 <= sum(len(t) for _, t in v) <= 520]
    by_u = defaultdict(list)
    for v in cand:
        by_u[unit_of(v[0][0].rsplit("/", 1)[0])].append(v)
    L += [f"## {sec}. Bir lafzın ele alınışı: üç paragraf", "",
          "Üçüncü vecihte bir lafzı \"وأما ﴿…﴾\" ile açan kısa paragraflar, farklı birimlerden, bütün olarak. Bir "
          "paragraf: lafız, hey'eti ya da kaydı, onun mânâya kattığı ve çoğu zaman garaza bağlanışı.", ""]
    for u in rng.sample(sorted(by_u), min(3, len(by_u))):
        v = rng.choice(by_u[u])
        L += [f"`{v[0][0]}` … ({len(v)} cümle)", "", "> " + " ".join(t for _, t in v), ""]
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", choices=P.UNITS)
    a = ap.parse_args()
    if a.prova:
        cfg = P.UNITS[a.prova]
        nodes = [n for n in cfg["nodes"] if n.startswith(WORK + "/")]
        text = build(nodes, f"Arapça asıl, Fâtiha ve Bakara 1–33; prova kopyası: sınanan birim ({cfg['sura_name']} "
                            f"{'–'.join(map(str, cfg['ayahs']))}) sayımdan ve örneklerden çıkarıldı.")
        out = P.OUT / a.prova / "ek-uslup.md"
        out.write_text(text, encoding="utf-8")
        ok = P.leak_report(a.prova, cfg, P.OUT / a.prova, text, "sizinti-uslup.md")
        print(f"{out.relative_to(ROOT)}: {len(text):,} harf; sızıntı testi: {'temiz' if ok else 'SORUN'}")
    else:
        text = build([], "Arapça asıl, Fâtiha ve Bakara 1–33 (eserin tamamı).")
        OUT.write_text(text, encoding="utf-8")
        print(f"{OUT.relative_to(ROOT)}: {len(text):,} harf")


if __name__ == "__main__":
    main()
