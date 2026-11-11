"""D1 provası (PLANLAR.md D1.3): sınanan birimi gizleyen prova profili, istem, yazdırma ve yan yana okuma.

    uv run python scripts/d1-prova.py hazirla 11-12        # veritabanları, ekler, istem, sızıntı testi
    uv run python scripts/d1-prova.py yazdir 11-12 [--kez 2] [--model claude-fable-5-2] [--effort high]
    uv run python scripts/d1-prova.py karsilastir 11-12    # taslaklar gizlenen metinle yan yana, ortak diziler

Gizleme kurulumda yapılır (çalışma anında süzgeç değil): yayındaki `genel` ve `tefsir` veritabanlarının kopyasından
sınanan birimin düğümleri (Türkçe ve Arapça İşârât) ve onlara bağlı her satır silinir; Osmanlıca İşârât bütünüyle
çıkar (birimleri Türkçeyle paralel değil, sınanan kısım ayrılamıyor; usul için Türkçe ve Arapça yeter). Anlamsal arama
vektörleri değişmez: dizin bölümleri veritabanından kurar, silinen bölümün vektörü kullanılmaz. Sızıntı testi gizlenen
cümlelerin 6 kelimelik dizilerini (Kur'ân'da geçenler hariç) prova veritabanlarında ve istemde arar.

Çıktılar `data/interim/d1-prova/<birim>/`: `risale.db`, `tefsir.db` (prova veritabanları), `istem.md`, `sizinti.md`,
`mcp.json`, `taslak-<n>.md` ve dökümleri, `karsilastirma.md`. Taslağı yazan oturum proje dışında, boş bir klasörde,
yerleşik araçlar kapalı çalışır (golden.py ile aynı düzen).
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from risale_mcp.normalize import search_words
from risale_mcp.paths import DIST_DIR, INTERIM_DIR, ROOT

GENEL_DB = DIST_DIR / "genel" / "risale.db"
TEFSIR_DB = DIST_DIR / "tefsir" / "risale.db"
OUT = INTERIM_DIR / "d1-prova"
PROMPT = ROOT / "docs" / "d1-prova-istemi.md"
OZET = ROOT / "docs" / "d1-usul-ozeti.md"
CIZELGE = ROOT / "docs" / "d1-birim-cizelgesi.md"
DROP_WORKS = ("isaratul-icaz-osmanlica",)
N = 6                                   # sızıntı testinde kelime dizisi uzunluğu
LEAK_MIN = 3        # bir cümle ya da istem en az bu kadar ortak dizi paylaşırsa sızıntı (≈8 ardışık kelime); 1–2 kalıp ibaredir
TIMEOUT = 2 * 60 * 60
PARENT_ENV = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_JOB_DIR")

# Birim başına: gizlenen düğümler ve eklerden çıkarılacaklar (eski, yeni). Ek düzeltmeleri yalnız sınanan birimden
# alınmış örnekleri ve bilgileri çıkarır; yerine o birim hakkında ipucu veren bir not konmaz.
UNITS = {
    "11-12": {
        "sura": 2, "ayahs": (11, 12), "sura_name": "Bakara", "olcu": "Bakara 9–10, 13, 14–15, 16",
        "nodes": ("isaratul-icaz/sure-i-bakara/11-12-ayetlerin-tefsiri",
                  "isaratul-icaz-arabi/sure-i-bakara/11-12-ayetlerin-tefsiri"),
        "ozet": [
            # 4.2: temsil örneği eserde yalnız bu birimde geçiyor; örnek de, ona dayanan "birinci araç" cümlesi de çıkar.
            # Silmeler (None) önce: değiştirmeler bloğun çevresini birleştirir.
            (None, "isaratul-icaz-arabi/sure-i-bakara/11-12-ayetlerin-tefsiri/c004"),
            (None, "isaratul-icaz/sure-i-bakara/11-12-ayetlerin-tefsiri/c011"),
            ("Cümlelerin birbirini nasıl istediği gösterilir. İki ana araç vardır. Birincisi temsildir: âyette söylenen "
             "ve söylenmeyen cümlelerin zinciri bir misalle kurulur.\n\n", "Cümlelerin birbirini nasıl istediği gösterilir. "),
            ("İkincisi dinleyenin zihnidir: her cümleden", "Ana aracı dinleyenin zihnidir: her cümleden"),
            ("| 9–10, 11–12, 13, 14–15, 16 |", "| 9–10, 13, 14–15, 16 |"),
        ],
        "cizelge": [
            (None, "| 11–12 |"),                                                       # çizelge satırı
            ("(`B/11-12-ayetlerin-tefsiri/c037`..`c050`; `B/14-15-ayetlerin-tefsiri/c035`..`c036`)",
             "(`B/14-15-ayetlerin-tefsiri/c035`..`c036`)"),
        ],
    },
}


def _like_any(cols: list[str], needles: list[str]) -> tuple[str, list[str]]:
    where = " OR ".join(f'"{c}" LIKE ?' for c in cols for _ in needles)
    return where, [f"%{n}%" for _ in cols for n in needles]


def scrub(src: Path, dst: Path, needles: list[str]) -> dict[str, int]:
    """`src`'nin kopyasından `needles`'tan birini (kimlik öneki ya da eser adı) taşıyan her satırı siler."""
    shutil.copyfile(src, dst)
    conn = sqlite3.connect(dst)
    tables = [t for (t,) in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
              if not re.search(r"_fts($|_)", t) and not t.startswith("sqlite_")]
    deleted: dict[str, int] = {}
    # FTS satırları: rowid = sentences.seq / nodes.seq (build_db)
    for fts, base in (("sentences_fts", "sentences"), ("nodes_fts", "nodes")):
        if base in tables and conn.execute("SELECT 1 FROM sqlite_master WHERE name = ?", (fts,)).fetchone():
            where, params = _like_any(["id", "work"] if base else ["id"], needles)
            seqs = [s for (s,) in conn.execute(f"SELECT seq FROM {base} WHERE {where}", params)]
            conn.executemany(f"DELETE FROM {fts} WHERE rowid = ?", [(s,) for s in seqs])
            deleted[fts] = len(seqs)
    for table in tables:
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info('{table}')")
                if (r[2] or "").upper() in ("TEXT", "") and r[1] not in ("text", "words")]
        if not cols:
            continue
        where, params = _like_any(cols, needles)
        n = conn.execute(f'DELETE FROM "{table}" WHERE {where}', params).rowcount
        if n:
            deleted[table] = n
    conn.commit()
    conn.execute("VACUUM")
    conn.close()
    return deleted


# ---------------------------------------------------------------- ekler

def apply_edits(text: str, edits: list[tuple[str | None, str]], name: str) -> str:
    for old, new in edits:
        if old is None:              # `new` geçen alıntı bloğunu ya da tablo satırını sil
            text = drop_block(text, new, name)
            continue
        if text.count(old) != 1:
            sys.exit(f"{name}: düzeltme bulunamadı ya da tek değil: {old[:60]!r}")
        text = text.replace(old, new)
    return text


def drop_block(text: str, marker: str, name: str) -> str:
    """Tablo satırı (`| …`) ya da `> "…"` alıntısı ile altındaki atıf satırı ve ardından gelen "Tercümede:" boşluğu."""
    lines = text.split("\n")
    hits = [i for i, line in enumerate(lines) if marker in line]
    if len(hits) != 1:
        sys.exit(f"{name}: {marker!r} {len(hits)} kez geçiyor")
    i = hits[0]
    if lines[i].startswith("|"):
        del lines[i]
        return "\n".join(lines)
    # atıf satırı ("— … (`kimlik`)"); üstünde boş satır ve alıntı bloğu
    start = i
    while start > 0 and (lines[start - 1].startswith(">") or lines[start - 1] == ""):
        start -= 1
        if lines[start].startswith(">") and (start == 0 or not lines[start - 1].startswith(">")):
            break
    end = i + 1
    while end < len(lines) and lines[end] in ("", "Tercümede:"):
        end += 1
    del lines[start:end]
    return "\n".join(lines)


def arabic_text(db: Path) -> str:
    """İşârât'ın Arapça aslı, prova veritabanından (gizlenen birim yok): başlık, kimlik, cümleler."""
    conn = sqlite3.connect(db)
    out = []
    nodes = conn.execute("SELECT id, ref, title, subtitle FROM nodes WHERE work = 'isaratul-icaz-arabi' ORDER BY ord")
    for node_id, ref, title, subtitle in nodes.fetchall():
        out.append(f"\n### {ref}  (`{node_id}`)" + (f"\n{subtitle}" if subtitle else ""))
        para = None
        for sid, pid, text in conn.execute("SELECT id, paragraph_id, text FROM sentences WHERE node_id = ? ORDER BY seq",
                                           (node_id,)):
            if pid != para:
                out.append("")
                para = pid
            out.append(f"[{sid[len(node_id) + 1:]}] {text}")
    return "\n".join(out).strip() + "\n"


def prompt_text(unit: str, cfg: dict, ozet: str, cizelge: str, arabic: str) -> str:
    body = PROMPT.read_text(encoding="utf-8").split("---- İSTEM ----", 1)[1].strip()
    ayahs = "–".join(map(str, cfg["ayahs"]))
    body = body.format(sura_name=cfg["sura_name"], ayahs=ayahs, olcu=cfg["olcu"])
    return (f"{body}\n\n---\n\n# Ek 1: Usul özeti (prova kopyası)\n\n{ozet}\n\n---\n\n"
            f"# Ek 2: Birim çizelgesi (prova kopyası)\n\n{cizelge}\n\n---\n\n"
            f"# Ek 3: İşârâtü'l-İ'câz'ın Arapça aslı (prova kopyası)\n\n"
            "Her bölüm başlığı, eklentilerde kullanılabilecek kimliğiyle; her cümlenin başında bölüm içindeki kimliği "
            "(`[c004]` → `<bölüm kimliği>/c004`).\n\n" + arabic)


# ---------------------------------------------------------------- sızıntı testi

def shingles(text: str) -> set[tuple[str, ...]]:
    w = search_words(text)
    return {tuple(w[i:i + N]) for i in range(len(w) - N + 1)}


def hidden_sentences(cfg: dict) -> list[tuple[str, str]]:
    conn = sqlite3.connect(GENEL_DB)
    out = []
    for node in cfg["nodes"]:
        out += conn.execute("SELECT id, text FROM sentences WHERE node_id = ? OR node_id LIKE ? ORDER BY seq",
                            (node, node + "/%")).fetchall()
    return out


def quran_shingles() -> set[tuple[str, ...]]:
    conn = sqlite3.connect(GENEL_DB)
    out: set = set()
    for col in ("text", "text_simple"):
        for (t,) in conn.execute(f"SELECT {col} FROM quran_ayahs"):
            out |= shingles(t)
    # âyet sınırını aşan alıntılar için ardışık âyetler birlikte
    texts = [t for (t,) in conn.execute("SELECT text_simple FROM quran_ayahs ORDER BY sura, ayah")]
    for a, b in zip(texts, texts[1:]):
        out |= shingles(a + " " + b)
    return out


def leak_scan(hidden: set, db: Path) -> dict[str, int]:
    conn = sqlite3.connect(db)
    hits: dict[str, int] = {}
    for sid, text in conn.execute("SELECT id, text FROM sentences"):
        n = len(shingles(text) & hidden)
        if n:
            hits[sid] = n
    return hits


def leak_report(unit: str, cfg: dict, out: Path, prompt: str) -> bool:
    hidden_rows = hidden_sentences(cfg)
    quran = quran_shingles()
    hidden = set().union(*(shingles(t) for _, t in hidden_rows)) - quran
    lines = [f"# Sızıntı testi: {unit}", "",
             f"Gizlenen {len(hidden_rows)} cümlenin Kur'ân dışı {N} kelimelik dizileri: {len(hidden)}. "
             "Bir satır, o cümlede bu dizilerden kaçının geçtiğidir. "
             f"Risale veritabanında ve istemde {LEAK_MIN} ve üstü sızıntı sayılır (1–2 kalıp ibare olur); tefsirde "
             "ortak ibare İşârât'ın kaynaklarından gelebilir, yalnız bilgi içindir.", ""]
    ok = True
    prompt_hits = len(shingles(prompt) & hidden)
    lines += [f"## İstem (ekler dahil): {prompt_hits} ortak dizi", ""]
    if prompt_hits >= LEAK_MIN:
        ok = False
    if prompt_hits:
        w = search_words(prompt)
        found = sorted({" ".join(w[i:i + N]) for i in range(len(w) - N + 1) if tuple(w[i:i + N]) in hidden})
        lines += [f"- {s}" for s in found[:50]] + [""]
    for name, db in (("risale", out / "risale.db"), ("tefsir", out / "tefsir.db")):
        hits = leak_scan(hidden, db)
        lines += [f"## {name}: {len(hits)} cümle", ""]
        conn = sqlite3.connect(db)
        for sid, n in sorted(hits.items(), key=lambda kv: -kv[1])[:60]:
            text = conn.execute("SELECT text FROM sentences WHERE id = ?", (sid,)).fetchone()[0]
            lines.append(f"- {n} · `{sid}` · {text[:160]}")
        if name == "risale" and any(n >= LEAK_MIN for n in hits.values()):
            ok = False
        lines.append("")
    (out / "sizinti.md").write_text("\n".join(lines), encoding="utf-8")
    return ok


# ---------------------------------------------------------------- komutlar

def hazirla(unit: str) -> None:
    cfg = UNITS[unit]
    out = OUT / unit
    out.mkdir(parents=True, exist_ok=True)
    needles = list(cfg["nodes"]) + list(DROP_WORKS)
    t = time.monotonic()
    print("risale:", scrub(GENEL_DB, out / "risale.db", needles))
    print("tefsir:", scrub(TEFSIR_DB, out / "tefsir.db", needles))
    print(f"  {time.monotonic() - t:.0f} sn")
    ozet = apply_edits(OZET.read_text(encoding="utf-8"), cfg["ozet"], "özet")
    cizelge = apply_edits(CIZELGE.read_text(encoding="utf-8"), cfg["cizelge"], "çizelge")
    (out / "ek-ozet.md").write_text(ozet, encoding="utf-8")
    (out / "ek-cizelge.md").write_text(cizelge, encoding="utf-8")
    prompt = prompt_text(unit, cfg, ozet, cizelge, arabic_text(out / "risale.db"))
    (out / "istem.md").write_text(prompt, encoding="utf-8")
    uv = shutil.which("uv") or "uv"
    base = [uv, "--directory", str(ROOT), "run", "risale-mcp"]
    servers = {"risale": base + ["--profile", "genel", "--db", str(out / "risale.db")],
               "tefsir": base + ["--profile", "tefsir", "--db", str(out / "tefsir.db")],
               "hadis": base + ["--profile", "hadis"]}
    (out / "mcp.json").write_text(json.dumps({"mcpServers": {n: {"type": "stdio", "command": a[0], "args": a[1:]}
                                                             for n, a in servers.items()}}, indent=2), encoding="utf-8")
    print(f"istem: {len(prompt):,} karakter, {len(prompt.split()):,} kelime")
    ok = leak_report(unit, cfg, out, prompt)
    print(f"sızıntı testi: {'temiz' if ok else 'SORUN'} → {(out / 'sizinti.md').relative_to(ROOT)}")
    if not ok:
        sys.exit(1)


def yazdir(unit: str, times: int, model: str, effort: str) -> None:
    out = OUT / unit
    prompt = (out / "istem.md").read_text(encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in PARENT_ENV}
    existing = [int(m.group(1)) for p in out.glob("taslak-*.jsonl") if (m := re.match(r"taslak-(\d+)", p.stem))]
    first = max(existing, default=0) + 1
    for n in range(first, first + times):
        with tempfile.TemporaryDirectory(prefix="d1-prova-") as tmp:
            command = ["claude", "-p", "--model", model, "--effort", effort, "--output-format", "stream-json",
                       "--verbose", "--mcp-config", str(out / "mcp.json"), "--strict-mcp-config", "--tools", "",
                       "--allowedTools", "mcp__risale,mcp__tefsir,mcp__hadis", "--no-session-persistence"]
            log = out / f"taslak-{n}.jsonl"
            started = time.monotonic()
            print(f"taslak {n}: {model}, {effort} ({datetime.now():%H:%M})", flush=True)
            with log.open("w", encoding="utf-8") as stdout:
                done = subprocess.run(command, input=prompt, cwd=tmp, env=env, stdout=stdout, stderr=subprocess.PIPE,
                                      text=True, timeout=TIMEOUT, check=False)
            if done.returncode or done.stderr.strip():
                (out / f"taslak-{n}.stderr.txt").write_text(done.stderr, encoding="utf-8")
            answer, calls, cost = transcript(log)
            meta = {"model": model, "effort": effort, "prompt_sha": _sha(prompt), "seconds": round(time.monotonic() - started),
                    "returncode": done.returncode, "calls": calls, "cost_usd": cost, "at": datetime.now().isoformat()}
            (out / f"taslak-{n}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
            (out / f"taslak-{n}.md").write_text(answer, encoding="utf-8")
            print(f"  {meta['seconds']} sn, {sum(calls.values())} araç çağrısı, çıkış {done.returncode}", flush=True)


def _sha(text: str) -> str:
    import hashlib
    return hashlib.sha1(text.encode()).hexdigest()[:12]


def transcript(log: Path) -> tuple[str, dict, float | None]:
    answer, calls, cost = "", Counter(), None
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event["message"].get("content", []):
                if block.get("type") == "tool_use":
                    calls[block["name"].removeprefix("mcp__")] += 1
        if event.get("type") == "result":
            answer = event.get("result") or ""
            cost = event.get("total_cost_usd")
    return answer, dict(calls), cost


def karsilastir(unit: str) -> None:
    cfg = UNITS[unit]
    out = OUT / unit
    rows = hidden_sentences(cfg)
    by_work = defaultdict(list)
    for sid, text in rows:
        by_work[sid.split("/", 1)[0]].append(text)
    arabic = "\n\n".join(by_work["isaratul-icaz-arabi"])
    turkish = "\n\n".join(by_work["isaratul-icaz"])
    hidden = shingles(arabic) - quran_shingles()
    tefsir = sqlite3.connect(out / "tefsir.db")
    sura, (a, b) = cfg["sura"], cfg["ayahs"]
    # müfessirlerin bu âyetlerdeki birimleri: İşârât'la ortak ibare oradan da gelebilir
    units = []
    for source, target in tefsir.execute("SELECT source, target FROM links WHERE relation = 'verse_unit' AND target LIKE ?",
                                         (f"quran:{sura}:%",)):
        lo, _, hi = target.split(":")[2].partition("-")
        if int(lo) <= b and int(hi or lo) >= a:
            units.append(source)
    shared_src: set = set()
    for node in units:
        for (t,) in tefsir.execute("SELECT text FROM sentences WHERE node_id = ? OR node_id LIKE ?", (node, node + "/%")):
            shared_src |= shingles(t)
    lines = [f"# Prova {unit}: taslaklar ve gizlenen metin", ""]
    for draft in sorted(out.glob("taslak-*.md")):
        text = draft.read_text(encoding="utf-8")
        common = shingles(text) & hidden
        own = common - shared_src
        meta = json.loads((out / f"{draft.stem}.json").read_text())
        lines += [f"## {draft.stem}", "",
                  f"{meta['model']}, {meta['effort']}, {meta['seconds']} sn, araçlar: {meta['calls']}", "",
                  f"Gizlenen Arapça metinle ortak {N} kelimelik dizi: {len(common)} (müfessirlerin bu âyetlerdeki "
                  f"birimlerinde de bulunmayan: {len(own)}; ezber şüphesi bunlardır)", ""]
        w = search_words(text)
        own_s = sorted({" ".join(w[i:i + N]) for i in range(len(w) - N + 1) if tuple(w[i:i + N]) in own})
        lines += [f"- {s}" for s in own_s] + [""]
    lines += ["## Gizlenen metin: İşârât'ın Arapça aslı", "", arabic, "",
              "## Gizlenen metin: Abdülmecid Nursî tercümesi", "", turkish, ""]
    (out / "karsilastirma.md").write_text("\n".join(lines), encoding="utf-8")
    print((out / "karsilastirma.md").relative_to(ROOT))


def _has(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE name = ?", (table,)).fetchone())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("hazirla")
    p.add_argument("unit", choices=UNITS)
    p = sub.add_parser("yazdir")
    p.add_argument("unit", choices=UNITS)
    p.add_argument("--kez", type=int, default=1)
    p.add_argument("--model", default="claude-fable-5-2")
    p.add_argument("--effort", default="high")
    p = sub.add_parser("karsilastir")
    p.add_argument("unit", choices=UNITS)
    args = parser.parse_args()
    if args.command == "hazirla":
        hazirla(args.unit)
    elif args.command == "yazdir":
        yazdir(args.unit, args.kez, args.model, args.effort)
    else:
        karsilastir(args.unit)


if __name__ == "__main__":
    main()
