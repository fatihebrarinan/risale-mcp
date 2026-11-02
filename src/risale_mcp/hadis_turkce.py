"""Yalnız Türkçe aktarılan hadisler için daraltılmış aday listesi (`docs/hadis-plani.md`, Adım 4).

    uv run python -m risale_mcp.hadis_turkce      # data/interim/hadis/turkce.{md,json}

Bu cümlelerde işaretlenecek Arapça yoktur: `arabic` ve kaynağın işareti değişmez, liste veritabanına girmez. Kural metne
bakar, hüküm vermez: "hadîs" diyen cümle hadisin kendisi olmayabilir, metnin hadis dediği şeyin rivayette bulunduğu
da gösterilmiş olmaz. Kapsam: müellifin külliyattaki Türkçe eserleri, ana cilt ve Eski Said. Mecmualar (özgü kısımları
Fihrist özetleri ve derlemedir) ve tercümeler (Arapça aslında metin zaten var) dışarıda.

Yazım ham metinde aranır: `search_words` "hadîs" ile "hâdise"yi aynı kelimeye indirir. Seviye (`form`), güçlüden:

    quoted_hadith   tırnaklı söz ve hemen ardından "hadîs" ya da "rivâyet": “…” meâlindeki hadîs
    quoted_prophet  tırnaklı söz, önünde ya da ardında Peygamber ve söyleme fiili: Resûl-i Ekrem dedi: “…”
    reported        tırnak yok; "rivâyette var ki": içerik aktarılıyor, "rivâyetlerde var" gibi genel söz sayılmaz

Cümlede ya da hemen önceki cümlede Arapça hadis parçası varsa elenir: Türkçesi o parçanın izahıdır, Adım 0–3'ün işidir.
Aynı metin başka bir yerde geçiyorsa liste tek kayıt tutar.
"""

import json
import re
from collections import Counter
from pathlib import Path

from risale_mcp.db import connect
from risale_mcp.paths import DB_PATH, INTERIM_DIR

_HADITH = r"(?:ehâd[iî]s|ehad[iî]s|[Hh]ad[iî]s(?!at|ât|e\b|el|el?er|el?i|en)|[Rr]iv[âa]yet)"
_QUOTE = r"“[^”]{12,}”"
QUOTED_HADITH = re.compile(rf"{_QUOTE}[\s,]*(?:\([^)]*\)\s*)?(?:\S+\s+){{0,3}}?{_HADITH}"
                           rf"|{_HADITH}\S*(?:\s+\S+){{0,5}}?\s*(?:gibi|ki|:|'?t[ae]\s)[\s:;,]*{_QUOTE}")
PROPHET = r"(?:Res[ûu]l|Peygamber|Fahr-?[iı]?-?\s?K[âa]in[âa]t|Zât[‑-]ı Ahmed|Aleyhissal[âa]t|\(asm\)|\(A\.S\.M\.\))"
SAY = r"(?:dedi|demiş|buyur|ferm[âa]n|söyle|ihb[âa]r|haber ver)"
SPOKEN_TO = re.compile(r"(?:Vessel[âa]m|\(asm\)|Ekrem|Peygamber\S*)['’]?(?:a|ya|e|ye)\b.{0,40}?(?:dedi|demiş|söyle)")
QUOTED_PROPHET = re.compile(rf"{PROPHET}.{{0,160}}?{SAY}\S*.{{0,40}}?{_QUOTE}"
                            rf"|{PROPHET}.{{0,60}}?{_QUOTE}.{{0,30}}?{SAY}")
REPORTED = re.compile(rf"{_HADITH}\S*(?:[-‑]i\s+\S+)?\s+(?:gelmiş(?:tir)?|var(?:dır)?|denilmiş(?:tir)?)\s+ki")
FORMS = (("quoted_hadith", QUOTED_HADITH), ("quoted_prophet", QUOTED_PROPHET), ("reported", REPORTED))


def form(text: str) -> str | None:
    for name, pattern in FORMS:
        if pattern.search(text) and not (name == "quoted_prophet" and SPOKEN_TO.search(text)):
            return name
    return None


def quote(text: str) -> str | None:
    """En uzun tırnaklı söz: Arapça aranacak olan odur."""
    return max(re.findall(rf"“([^”]+)”", text), key=len, default=None)


def collect(db: Path = DB_PATH) -> tuple[list[dict], Counter]:
    conn, counts, entries, seen = connect(db), Counter(), [], set()
    hadith = {r[0] for r in conn.execute("SELECT sentence_id FROM arabic WHERE kind = 'hadis' AND sentence_id IS NOT NULL")}
    previous = None
    for r in conn.execute(
            "SELECT s.id, s.text, s.ref, s.node_id FROM sentences s JOIN works w ON w.slug = s.work"
            " WHERE w.language = 'tr' AND w.authority = 'muellif' AND w.translation = 0"
            " AND w.collection = 'risale/kulliyat' AND w.group_name IN ('ana-cilt', 'eski-said') ORDER BY s.seq"):
        near = r["id"] in hadith or previous == (r["node_id"], True)
        previous = (r["node_id"], r["id"] in hadith)
        if not (kind := form(r["text"])):
            continue
        counts[f"{kind} bulunan"] += 1
        if near:
            counts[f"{kind} Arapçası yanında"] += 1
        elif r["text"] in seen:
            counts[f"{kind} yinelenen"] += 1
        else:
            seen.add(r["text"])
            counts[f"{kind} liste"] += 1
            entries.append({"id": r["id"], "ref": r["ref"], "form": kind, "text": r["text"], "quote": quote(r["text"])})
    return entries, counts


def main(out_dir: Path = INTERIM_DIR / "hadis") -> None:
    entries, counts = collect()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "turkce.json").write_text(json.dumps({"counts": counts, "sentences": entries}, ensure_ascii=False, indent=1), "utf-8")
    lines = ["# Yalnız Türkçe aktarılan hadis adayları\n", "| | sayı |", "|---|---|", *(f"| {k} | {v} |" for k, v in sorted(counts.items()))]
    for name, _ in FORMS:
        chosen = [e for e in entries if e["form"] == name]
        lines.append(f"\n## {name} ({len(chosen)})\n")
        lines += [f"- `{e['id']}`: {e['text']}" for e in chosen]
    (out_dir / "turkce.md").write_text("\n".join(lines) + "\n", "utf-8")
    print("\n".join(lines[1:4 + len(counts)]))


if __name__ == "__main__":
    main()
