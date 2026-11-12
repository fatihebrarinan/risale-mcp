"""D1 provası (PLANLAR.md D1.3): sınanan birimi gizleyen prova profili, istem, yazdırma ve yan yana okuma.

    uv run python scripts/d1-prova.py hazirla 11-12 [--istem tam|ince] [--db-yenile]   # veritabanları, ekler, istem, sızıntı testi
    uv run python scripts/d1-prova.py yazdir 11-12 [--istem tam|ince] [--kez 2] [--model claude-fable-5-2] [--effort high]
    uv run python scripts/d1-prova.py karsilastir 11-12    # taslaklar gizlenen metinle yan yana, ortak diziler
    uv run python scripts/d1-prova.py okuma 11-12          # okuma sayfası: Arapça ve Türkçe ayrı, vecih vecih yan yana

Gizleme kurulumda yapılır (çalışma anında süzgeç değil): yayındaki `genel` ve `tefsir` veritabanlarının kopyasından
sınanan birimin düğümleri (Türkçe ve Arapça İşârât) ve onlara bağlı her satır silinir; Osmanlıca İşârât bütünüyle
çıkar (birimleri Türkçeyle paralel değil, sınanan kısım ayrılamıyor; usul için Türkçe ve Arapça yeter). Anlamsal arama
vektörleri değişmez: dizin bölümleri veritabanından kurar, silinen bölümün vektörü kullanılmaz. Sızıntı testi gizlenen
cümlelerin 6 kelimelik dizilerini (Kur'ân'da geçenler hariç) prova veritabanlarında ve istemde arar.

İstemin iki biçimi (`--istem`): `tam` Ek 3'te İşârât'ın Arapça aslının tamamını verir (`istem.md`, `sizinti.md`), `ince`
yalnız birimin `ince` listesindeki bölümlerini (`istem-ince.md`, `sizinti-ince.md`); kalanı eklentidedir. Veritabanları
iki biçimde ortaktır: varsa yeniden kurulmaz (`--db-yenile` ile kurulur), taslaklar aynı gizlemeyle karşılaştırılsın.

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

from risale_mcp.normalize import search_words, tr_lower
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
        # ince istemin Ek 3'ü: komşu birimler ve Bakara 17–20'nin nazarî girişi (tam bölüm kimlikleri, alt bölümsüz)
        "ince": ("isaratul-icaz-arabi/sure-i-bakara/8", "isaratul-icaz-arabi/sure-i-bakara/9-10-ayetlerin-tefsiri",
                 "isaratul-icaz-arabi/sure-i-bakara/13", "isaratul-icaz-arabi/sure-i-bakara/14-15-ayetlerin-tefsiri",
                 "isaratul-icaz-arabi/sure-i-bakara/16", "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri",
                 "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/fasil",
                 "isaratul-icaz-arabi/sure-i-bakara/17-20-ayetlerin-tefsiri/fasil-2"),
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
        # okuma sayfası: gizlenen metnin vecihleri (ilk cümle; `son` sonrası sonraki âyetin satırıdır)
        "sections": {
            "isaratul-icaz-arabi": {"V1": "c001", "V2": "c004", "V3": "c014", "son": "c051"},
            "isaratul-icaz": {"Âyet": "c001", "V1": "c002", "V2": "c011", "V3": "c023", "son": "c080"},
        },
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


ISTEM = {"tam": ("istem.md", "sizinti.md"), "ince": ("istem-ince.md", "sizinti-ince.md")}


def arabic_text(db: Path, only: tuple[str, ...] | None = None) -> str:
    """İşârât'ın Arapça aslı, prova veritabanından (gizlenen birim yok): başlık, kimlik, cümleler. `only` verilirse
    yalnız o bölümler (kitap sırasıyla)."""
    conn = sqlite3.connect(db)
    out = []
    nodes = conn.execute("SELECT id, ref, title, subtitle FROM nodes WHERE work = 'isaratul-icaz-arabi' ORDER BY ord")
    rows = [r for r in nodes.fetchall() if only is None or r[0] in only]
    if only is not None and len(rows) != len(only):
        sys.exit(f"ince Ek 3: bulunamayan bölüm: {sorted(set(only) - {r[0] for r in rows})}")
    for node_id, ref, title, subtitle in rows:
        out.append(f"\n### {ref}  (`{node_id}`)" + (f"\n{subtitle}" if subtitle else ""))
        para = None
        for sid, pid, text in conn.execute("SELECT id, paragraph_id, text FROM sentences WHERE node_id = ? ORDER BY seq",
                                           (node_id,)):
            if pid != para:
                out.append("")
                para = pid
            out.append(f"[{sid[len(node_id) + 1:]}] {text}")
    return "\n".join(out).strip() + "\n"


def variant_lines(text: str, istem: str) -> str:
    """`@tam ` / `@ince ` önekli satırlar yalnız o biçimde kalır (önek atılır)."""
    out = []
    for line in text.split("\n"):
        if m := re.match(r"@(tam|ince) ", line):
            if m.group(1) == istem:
                out.append(line[m.end():])
            continue
        out.append(line)
    return "\n".join(out)


def prompt_text(unit: str, cfg: dict, ozet: str, cizelge: str, arabic: str, istem: str = "tam") -> str:
    body = PROMPT.read_text(encoding="utf-8").split("---- İSTEM ----", 1)[1].strip()
    body = variant_lines(body, istem)
    ayahs = "–".join(map(str, cfg["ayahs"]))
    body = body.format(sura_name=cfg["sura_name"], ayahs=ayahs, olcu=cfg["olcu"])
    if istem == "tam":
        ek3 = ("# Ek 3: İşârâtü'l-İ'câz'ın Arapça aslı (prova kopyası)\n\n"
               "Her bölüm başlığı, eklentilerde kullanılabilecek kimliğiyle; her cümlenin başında bölüm içindeki kimliği "
               "(`[c004]` → `<bölüm kimliği>/c004`).\n\n")
    else:
        ek3 = ("# Ek 3: İşârâtü'l-İ'câz'ın Arapça aslından seçme bölümler (prova kopyası)\n\n"
               "Burada yalnız sınanan âyetlere komşu birimler ve Bakara 17–20'nin nazarî girişi var; İşârât'ın öbür "
               "bölümleri `risale` eklentisinde (`read_section`, `get_passage`, `search`, `semantic_search`). Her bölüm "
               "başlığı, eklentilerde kullanılabilecek kimliğiyle; her cümlenin başında bölüm içindeki kimliği "
               "(`[c004]` → `<bölüm kimliği>/c004`).\n\n")
    return (f"{body}\n\n---\n\n# Ek 1: Usul özeti (prova kopyası)\n\n{ozet}\n\n---\n\n"
            f"# Ek 2: Birim çizelgesi (prova kopyası)\n\n{cizelge}\n\n---\n\n" + ek3 + arabic)


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


def leak_report(unit: str, cfg: dict, out: Path, prompt: str, report: str = "sizinti.md") -> bool:
    hidden_rows = hidden_sentences(cfg)
    quran = quran_shingles()
    hidden = set().union(*(shingles(t) for _, t in hidden_rows)) - quran
    lines = [f"# Sızıntı testi: {unit} ({report.removesuffix('.md')})", "",
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
    (out / report).write_text("\n".join(lines), encoding="utf-8")
    return ok


# ---------------------------------------------------------------- komutlar

def hazirla(unit: str, istem: str = "tam", db_yenile: bool = False) -> None:
    cfg = UNITS[unit]
    out = OUT / unit
    out.mkdir(parents=True, exist_ok=True)
    needles = list(cfg["nodes"]) + list(DROP_WORKS)
    if db_yenile or not (out / "risale.db").exists() or not (out / "tefsir.db").exists():
        t = time.monotonic()
        print("risale:", scrub(GENEL_DB, out / "risale.db", needles))
        print("tefsir:", scrub(TEFSIR_DB, out / "tefsir.db", needles))
        print(f"  {time.monotonic() - t:.0f} sn")
    else:
        print("veritabanları var, yeniden kurulmadı (--db-yenile)")
    prompt_name, report = ISTEM[istem]
    ozet = apply_edits(OZET.read_text(encoding="utf-8"), cfg["ozet"], "özet")
    cizelge = apply_edits(CIZELGE.read_text(encoding="utf-8"), cfg["cizelge"], "çizelge")
    (out / "ek-ozet.md").write_text(ozet, encoding="utf-8")
    (out / "ek-cizelge.md").write_text(cizelge, encoding="utf-8")
    only = cfg["ince"] if istem == "ince" else None
    prompt = prompt_text(unit, cfg, ozet, cizelge, arabic_text(out / "risale.db", only), istem)
    (out / prompt_name).write_text(prompt, encoding="utf-8")
    uv = shutil.which("uv") or "uv"
    base = [uv, "--directory", str(ROOT), "run", "risale-mcp"]
    servers = {"risale": base + ["--profile", "genel", "--db", str(out / "risale.db")],
               "tefsir": base + ["--profile", "tefsir", "--db", str(out / "tefsir.db")],
               "hadis": base + ["--profile", "hadis"]}
    (out / "mcp.json").write_text(json.dumps({"mcpServers": {n: {"type": "stdio", "command": a[0], "args": a[1:]}
                                                             for n, a in servers.items()}}, indent=2), encoding="utf-8")
    print(f"istem: {len(prompt):,} karakter, {len(prompt.split()):,} kelime")
    ok = leak_report(unit, cfg, out, prompt, report)
    print(f"sızıntı testi: {'temiz' if ok else 'SORUN'} → {(out / report).relative_to(ROOT)}")
    if not ok:
        sys.exit(1)


def yazdir(unit: str, times: int, model: str, effort: str, istem: str = "tam") -> None:
    out = OUT / unit
    prompt = (out / ISTEM[istem][0]).read_text(encoding="utf-8")
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
            print(f"taslak {n}: {model}, {effort}, istem {istem} ({datetime.now():%H:%M})", flush=True)
            with log.open("w", encoding="utf-8") as stdout:
                done = subprocess.run(command, input=prompt, cwd=tmp, env=env, stdout=stdout, stderr=subprocess.PIPE,
                                      text=True, timeout=TIMEOUT, check=False)
            if done.returncode or done.stderr.strip():
                (out / f"taslak-{n}.stderr.txt").write_text(done.stderr, encoding="utf-8")
            answer, calls, cost = transcript(log)
            meta = {"model": model, "effort": effort, "istem": istem, "prompt_sha": _sha(prompt), "seconds": round(time.monotonic() - started),
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
                  f"{meta['model']}, {meta['effort']}, istem {meta.get('istem', 'tam')}, {meta['seconds']} sn, "
                  f"araçlar: {meta['calls']}", "",
                  f"Gizlenen Arapça metinle ortak {N} kelimelik dizi: {len(common)} (müfessirlerin bu âyetlerdeki "
                  f"birimlerinde de bulunmayan: {len(own)}; ezber şüphesi bunlardır)", ""]
        w = search_words(text)
        own_s = sorted({" ".join(w[i:i + N]) for i in range(len(w) - N + 1) if tuple(w[i:i + N]) in own})
        lines += [f"- {s}" for s in own_s] + [""]
    lines += ["## Gizlenen metin: İşârât'ın Arapça aslı", "", arabic, "",
              "## Gizlenen metin: Abdülmecid Nursî tercümesi", "", turkish, ""]
    (out / "karsilastirma.md").write_text("\n".join(lines), encoding="utf-8")
    print((out / "karsilastirma.md").relative_to(ROOT))


# ---------------------------------------------------------------- okuma sayfası

SECTION_TITLES = {"Âyet": "Âyet", "Mukaddime": "Mukaddime", "V1": "Birinci vecih: öncesiyle nazım",
                  "V2": "İkinci vecih: cümleler arasındaki nazım", "V3": "Üçüncü vecih: hey'etler ve kelimeler"}
DRAFT_HEADINGS = {"âyet": "Âyet", "mukaddime": "Mukaddime", "birinci vecih": "V1", "ikinci vecih": "V2",
                  "üçüncü vecih": "V3"}


def _arabic_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    return sum("\u0600" <= c <= "\u06ff" for c in letters) / max(1, len(letters))


def parse_draft(text: str) -> tuple[dict, dict]:
    """Taslak: başlık başına bloklar [(dil, tür, metin)] ve kaynakça {n: satır}."""
    sections: dict[str, list] = defaultdict(list)
    sources: dict[str, str] = {}
    current = None
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        if lines[0].startswith("## "):
            name = lines[0][3:].strip()
            key = tr_lower(name)
            current = DRAFT_HEADINGS.get(key, "Kaynaklar" if key == "kaynaklar" else name)
            block = "\n".join(lines[1:]).strip()
            if not block:
                continue
        if current is None:
            continue
        if current == "Kaynaklar":
            last = None
            for line in block.split("\n"):
                if m := re.match(r"\[(\d+)\]\s*(.*)", line):
                    last = m.group(1)
                    sources[last] = m.group(2)
                elif last and line.strip():
                    sources[last] += " · " + line.strip().lstrip("- ")
            continue
        kind = "quote" if block.startswith(">") else "para"
        body = re.sub(r"^>\s?", "", block, flags=re.M) if kind == "quote" else block
        if body.startswith("Yapay zekâ tercümesi:"):
            sections[current].append(("tr", kind, body.removeprefix("Yapay zekâ tercümesi:").strip()))
        else:
            sections[current].append(("ar" if _arabic_ratio(body) > 0.5 else "tr", kind, body))
    # alıntının tercümesi alıntı gibi görünsün
    for blocks in sections.values():
        for i in range(1, len(blocks)):
            if blocks[i][0] == "tr" and blocks[i - 1][1] == "quote" and blocks[i - 1][0] == "ar":
                blocks[i] = ("tr", "quote", blocks[i][2])
    return dict(sections), sources


def hidden_sections(cfg: dict, work: str) -> dict[str, list[str]]:
    """Gizlenen metnin vecihleri: {vecih: [paragraf metni]}."""
    conn = sqlite3.connect(GENEL_DB)
    node = next(n for n in cfg["nodes"] if n.startswith(work + "/"))
    bounds = cfg["sections"][work]
    order = [(k, v) for k, v in bounds.items() if k != "son"]
    out: dict[str, list] = defaultdict(list)
    current, para, last = None, None, None
    for sid, pid, text in conn.execute("SELECT id, paragraph_id, text FROM sentences WHERE node_id = ? ORDER BY seq",
                                       (node,)):
        local = sid[len(node) + 1:]
        if last == bounds["son"]:
            break
        for key, first in order:
            if local == first:
                current, para = key, None
        last = local
        if current is None:
            continue
        if pid != para:
            out[current].append(text)
            para = pid
        else:
            out[current][-1] += " " + text
    return dict(out)


ARABIC_RUN = re.compile(r"[\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeff][\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeff\s\-]*")


def _inline(text: str, sources: dict, lang: str = "ar") -> str:
    import html
    s = html.escape(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    if lang == "tr":            # Türkçe içindeki Arapça: sağdan sola yalıtılır (ayraçlar ters dönmesin)
        s = ARABIC_RUN.sub(lambda m: f'<bdi class="arw" dir="rtl">{m.group(0).strip()}</bdi>'
                           + (" " if m.group(0).endswith(" ") else ""), s)

    def mark(m: re.Match) -> str:
        inner = m.group(1)
        if re.fullmatch(r"[\d,\s]+", inner):
            nums = [n.strip() for n in inner.split(",")]
            title = html.escape(" | ".join(f"[{n}] {sources.get(n, '')}" for n in nums), quote=True)
            return f'<span class="ref" title="{title}">[{inner}]</span>'
        cls = "own" if "kendi tespiti" in inner else "src"
        nums = re.findall(r"\b\d+\b", inner)
        title = html.escape(" | ".join(f"[{n}] {sources.get(n, '')}" for n in nums), quote=True)
        return f'<span class="mk {cls}" title="{title}">[{inner}]</span>'
    return re.sub(r"\[([^\]\n]{1,80})\]", mark, s).replace("\n", "<br>")


def _blocks_html(blocks: list, lang: str, sources: dict) -> str:
    out = []
    for blang, kind, text in blocks:
        if blang != lang:
            continue
        cls = ("ar" if lang == "ar" else "tr") + (" q" if kind == "quote" else "")
        out.append(f'<p class="{cls}">{_inline(text, sources, lang)}</p>')
    return "\n".join(out) or '<p class="empty">—</p>'


def _hidden_html(paras: list[str], lang: str) -> str:
    import html
    if not paras:
        return '<p class="empty">—</p>'
    cls = "ar" if lang == "ar" else "tr"
    return "\n".join(f'<p class="{cls}">{_inline(p, {}, lang) if lang == "tr" else html.escape(p)}</p>' for p in paras)


def okuma(unit: str) -> None:
    import html
    cfg = UNITS[unit]
    out = OUT / unit
    drafts = []
    for path in sorted(out.glob("taslak-*.md"), key=lambda p: int(p.stem.split("-")[1])):
        meta = json.loads((out / f"{path.stem}.json").read_text())
        sections, sources = parse_draft(path.read_text(encoding="utf-8"))
        ar_chars = sum(len(t) for blocks in sections.values() for lang, kind, t in blocks
                       if lang == "ar" and kind == "para" and blocks is not sections.get("Âyet"))
        drafts.append((path.stem, meta, sections, sources, ar_chars))
    hidden = {"ar": hidden_sections(cfg, "isaratul-icaz-arabi"), "tr": hidden_sections(cfg, "isaratul-icaz")}
    hidden_ar_chars = sum(len(p) for p in sum(hidden["ar"].values(), []))
    keys = ["Âyet", "Mukaddime", "V1", "V2", "V3"]
    ayahs = "–".join(map(str, cfg["ayahs"]))
    tabs, panes = [], []
    for d_i, (name, meta, sections, sources, ar_chars) in enumerate(drafts):
        for lang, label, right in (("ar", "Arapça", "İşârâtü'l-İ'câz (Arapça asıl)"),
                                   ("tr", "Türkçe", "Abdülmecid Nursî tercümesi")):
            pane_id = f"{name}-{lang}"
            tabs.append(f'<button role="tab" data-pane="{pane_id}">{name.replace("taslak-", "Taslak ")} · {label}</button>')
            rows = []
            for key in keys:
                left = sections.get(key, [])
                right_paras = hidden[lang].get(key, [])
                if not left and not right_paras:
                    continue
                rows.append(f'<h2>{SECTION_TITLES[key]}</h2><div class="row">'
                            f'<div class="col">{_blocks_html(left, lang, sources)}</div>'
                            f'<div class="col">{_hidden_html(right_paras, lang)}</div></div>')
            src_html = "".join(f"<li><b>[{n}]</b> {html.escape(s)}</li>" for n, s in sources.items())
            heads = (f'<div class="row heads"><div class="col"><h3>Yapay zekâ taslağı ({name.split("-")[1]})</h3></div>'
                     f'<div class="col"><h3>{right} <span class="muted">gizlenen metin</span></h3></div></div>')
            info = (f'<p class="meta">{meta["model"]}, {meta["effort"]}, istem {meta.get("istem", "tam")}, '
                    f'{meta["seconds"] // 60} dk, '
                    f'{sum(meta["calls"].values())} araç çağrısı. Taslağın Arapçası {ar_chars:,} karakter, '
                    f'İşârât\'ın bu birimi {hidden_ar_chars:,} karakter.</p>').replace(",", ".")
            panes.append(f'<section class="pane" id="{pane_id}" hidden>{info}{heads}{"".join(rows)}'
                         f'<details><summary>Taslağın kaynakçası ({len(sources)})</summary><ol class="src">{src_html}'
                         f'</ol></details></section>')
    page = PAGE.replace("{title}", f"Prova {unit}").replace("{h1}", f"Prova: {cfg['sura_name']} {ayahs}") \
        .replace("{tabs}", "".join(tabs)).replace("{panes}", "".join(panes))
    (out / "okuma.html").write_text(page, encoding="utf-8")
    print((out / "okuma.html").relative_to(ROOT))


PAGE = """<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root { --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --line: #dcd8cf; --card: #ffffff; --accent: #1f5c3f;
        --own: #8a4b00; --own-bg: #fdf0dc; --src: #1f4f7a; --src-bg: #e3eef8; --quote: #f2efe8; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f; --card: #1f1e1b; --accent: #7cc49d;
  --own: #f0b46a; --own-bg: #3a2a14; --src: #8cc0ef; --src-bg: #18293a; --quote: #26251f; } }
:root[data-theme="dark"] { --bg: #161614; --fg: #e8e6e1; --muted: #9c9a94; --line: #34332f; --card: #1f1e1b;
  --accent: #7cc49d; --own: #f0b46a; --own-bg: #3a2a14; --src: #8cc0ef; --src-bg: #18293a; --quote: #26251f; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.65 "Noto Serif", "DejaVu Serif", Georgia, serif; }
header { position: sticky; top: 0; z-index: 2; background: var(--bg); border-bottom: 1px solid var(--line); padding: 10px 16px; }
h1 { font-size: 1.15rem; margin: 0 0 6px; }
.stamp { color: var(--muted); font-size: .85rem; margin: 0 0 8px; }
[role=tablist] { display: flex; flex-wrap: wrap; gap: 6px; }
[role=tab] { font: inherit; font-size: .9rem; padding: 4px 12px; border: 1px solid var(--line); border-radius: 999px;
             background: var(--card); color: var(--fg); cursor: pointer; }
[role=tab][aria-selected=true] { background: var(--accent); border-color: var(--accent); color: var(--bg); }
main { max-width: 1500px; margin: 0 auto; padding: 8px 16px 60px; }
.meta { color: var(--muted); font-size: .85rem; }
h2 { font-size: 1rem; margin: 28px 0 8px; padding-bottom: 4px; border-bottom: 2px solid var(--accent); }
h3 { font-size: .9rem; margin: 0; color: var(--muted); font-weight: 600; }
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.heads { position: sticky; top: 86px; background: var(--bg); padding: 6px 0; border-bottom: 1px solid var(--line); z-index: 1; }
.col { min-width: 0; }
.col + .col { border-left: 1px solid var(--line); padding-left: 24px; }
p { margin: 0 0 12px; }
p.ar { direction: rtl; text-align: right; font-family: "Noto Naskh Arabic", "Amiri", "Scheherazade New", serif;
       font-size: 1.3rem; line-height: 2.05; }
p.q { background: var(--quote); padding: 6px 12px; border-radius: 4px; font-size: .95em; }
p.ar.q { border-right: 3px solid var(--muted); font-size: 1.2rem; } p.tr.q { border-left: 3px solid var(--muted); }
p.empty { color: var(--muted); }
.arw { font-family: "Noto Naskh Arabic", "Amiri", "Scheherazade New", serif; font-size: 1.12em; }
.muted { color: var(--muted); font-weight: 400; }
.mk { font-family: system-ui, sans-serif; font-size: .72rem; padding: 0 4px; border-radius: 3px; white-space: nowrap;
      direction: ltr; unicode-bidi: isolate; cursor: help; }
.mk.own { color: var(--own); background: var(--own-bg); } .mk.src { color: var(--src); background: var(--src-bg); }
.ref { font-family: system-ui, sans-serif; font-size: .72rem; color: var(--src); cursor: help; direction: ltr; unicode-bidi: isolate; }
details { margin-top: 32px; } summary { cursor: pointer; color: var(--muted); }
ol.src { list-style: none; padding: 0; font-size: .85rem; } ol.src li { margin: 4px 0; }
.legend { font-size: .8rem; color: var(--muted); margin: 6px 0 0; }
@media (max-width: 800px) { .row { grid-template-columns: 1fr; } .col + .col { border-left: 0; padding-left: 0;
  border-top: 1px dashed var(--line); padding-top: 12px; } .heads { display: none; } }
</style></head><body>
<header><h1>{h1}</h1>
<p class="stamp">Yapay zekâ taslağı, tefsir değildir; yayımlanmaz. Sağ sütun İşârâtü'l-İ'câz'ın taslağı yazan modelden gizlenen metnidir.</p>
<div role="tablist">{tabs}</div>
<p class="legend"><span class="mk own">[kendi tespiti]</span> modelin kendi tespiti ·
<span class="mk src">[belâgat; 14]</span> kaynağa dayanan iddia · <span class="ref">[14]</span> kaynak (üzerine gelince adı)</p>
</header>
<main>{panes}</main>
<script>
const tabs = [...document.querySelectorAll('[role=tab]')];
function show(id) {
  tabs.forEach(t => t.setAttribute('aria-selected', t.dataset.pane === id));
  document.querySelectorAll('.pane').forEach(p => p.hidden = p.id !== id);
  try { localStorage.setItem('prova-tab', id); } catch (e) {}
}
tabs.forEach(t => t.addEventListener('click', () => show(t.dataset.pane)));
let saved = null; try { saved = localStorage.getItem('prova-tab'); } catch (e) {}
show(tabs.some(t => t.dataset.pane === saved) ? saved : tabs[0].dataset.pane);
</script></body></html>
"""


def _has(conn: sqlite3.Connection, table: str) -> bool:
    return bool(conn.execute("SELECT 1 FROM sqlite_master WHERE name = ?", (table,)).fetchone())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("hazirla")
    p.add_argument("unit", choices=UNITS)
    p.add_argument("--istem", choices=ISTEM, default="tam")
    p.add_argument("--db-yenile", action="store_true")
    p = sub.add_parser("yazdir")
    p.add_argument("unit", choices=UNITS)
    p.add_argument("--istem", choices=ISTEM, default="tam")
    p.add_argument("--kez", type=int, default=1)
    p.add_argument("--model", default="claude-fable-5-2")
    p.add_argument("--effort", default="high")
    p = sub.add_parser("karsilastir")
    p.add_argument("unit", choices=UNITS)
    p = sub.add_parser("okuma")
    p.add_argument("unit", choices=UNITS)
    args = parser.parse_args()
    if args.command == "hazirla":
        hazirla(args.unit, args.istem, args.db_yenile)
    elif args.command == "yazdir":
        yazdir(args.unit, args.kez, args.model, args.effort, args.istem)
    elif args.command == "okuma":
        okuma(args.unit)
    else:
        karsilastir(args.unit)


if __name__ == "__main__":
    main()
