"""D1 provası (PLANLAR.md D1, D4): sınanan birimi gizleyen prova profili, istem, yazdırma, okuma sayfası, notlar.

    uv run python scripts/d1-prova.py hazirla 11-12 [--istem tam|ince] [--db-yenile]   # veritabanları, ekler, istem, sızıntı testi
    uv run python scripts/d1-prova.py yazdir 11-12 [--istem tam|ince] [--kez 2] [--model claude-fable-5-2] [--effort high]
    uv run python scripts/d1-prova.py karsilastir 11-12    # taslaklar gizlenen metinle, ortak diziler
    uv run python scripts/d1-prova.py okuma                # okuma ve not sayfası: bütün birimler, data/d1/okuma.html
    uv run python scripts/d1-prova.py notlar [dosya.json…] # okuyucuların notlarını al, birim başına notlar.md

Gizleme kurulumda yapılır (çalışma anında süzgeç değil): yayındaki `genel` ve `tefsir` veritabanlarının kopyasından
sınanan birimin düğümleri (Türkçe ve Arapça İşârât) ve onlara bağlı her satır silinir; Osmanlıca İşârât bütünüyle
çıkar (birimleri Türkçeyle paralel değil, sınanan kısım ayrılamıyor; usul için Türkçe ve Arapça yeter). Anlamsal arama
vektörleri değişmez: dizin bölümleri veritabanından kurar, silinen bölümün vektörü kullanılmaz. Sızıntı testi gizlenen
cümlelerin 6 kelimelik dizilerini (Kur'ân'da geçenler hariç) prova veritabanlarında ve istemde arar.

İstemin iki biçimi (`--istem`): `tam` Ek 3'te İşârât'ın Arapça aslının tamamını verir (`istem.md`, `sizinti.md`), `ince`
yalnız birimin `ince` listesindeki bölümlerini (`istem-ince.md`, `sizinti-ince.md`); kalanı eklentidedir. Veritabanları
iki biçimde ortaktır: varsa yeniden kurulmaz (`--db-yenile` ile kurulur), taslaklar aynı gizlemeyle karşılaştırılsın.

Çıktılar iki yerde (D4, 2026-11-12):
- `data/interim/d1-prova/<birim>/`: yeniden üretilebilenler (`risale.db`, `tefsir.db`, ekler, istem, sızıntı raporları,
  `mcp.json`).
- `data/d1/` (kendi git deposu, uzak kopyası özel depoda; README): yeniden üretilemeyenler. `provalar/<birim>/`
  `taslak-<n>.md`, `.json`, `.jsonl` (döküm), `karsilastirma.md`, `notlar.md`; `notlar/` okuyucuların dışa aktardığı
  dosyalar; `okuma.html` okuma ve not sayfası (taslakları taşır: açık adreste durmaz, dosya olarak paylaşılır).
Taslağı yazan oturum proje dışında, boş bir klasörde, yerleşik araçlar kapalı çalışır (golden.py ile aynı düzen).
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
from risale_mcp.paths import DATA_DIR, DIST_DIR, INTERIM_DIR, ROOT

GENEL_DB = DIST_DIR / "genel" / "risale.db"
TEFSIR_DB = DIST_DIR / "tefsir" / "risale.db"
OUT = INTERIM_DIR / "d1-prova"                # yeniden üretilebilenler: prova veritabanları, ekler, istem, sızıntı
KEEP = DATA_DIR / "d1"                         # yeniden üretilemeyenler: kendi git deposu (README)
DRAFTS = KEEP / "provalar"                     # taslaklar, dökümler, karşılaştırma, okuma notları
HADIS_DB = DIST_DIR / "hadis" / "hadis.db"
PROMPT = ROOT / "docs" / "d1" / "prova-istemi.md"
OZET = ROOT / "docs" / "d1" / "usul-ozeti.md"
CIZELGE = ROOT / "docs" / "d1" / "birim-cizelgesi.md"
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
    work = OUT / unit
    out = DRAFTS / unit
    out.mkdir(parents=True, exist_ok=True)
    prompt = (work / ISTEM[istem][0]).read_text(encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in PARENT_ENV}
    existing = [int(m.group(1)) for p in out.glob("taslak-*.jsonl") if (m := re.match(r"taslak-(\d+)", p.stem))]
    first = max(existing, default=0) + 1
    for n in range(first, first + times):
        with tempfile.TemporaryDirectory(prefix="d1-prova-") as tmp:
            command = ["claude", "-p", "--model", model, "--effort", effort, "--output-format", "stream-json",
                       "--verbose", "--mcp-config", str(work / "mcp.json"), "--strict-mcp-config", "--tools", "",
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
    out = DRAFTS / unit
    rows = hidden_sentences(cfg)
    by_work = defaultdict(list)
    for sid, text in rows:
        by_work[sid.split("/", 1)[0]].append(text)
    arabic = "\n\n".join(by_work["isaratul-icaz-arabi"])
    turkish = "\n\n".join(by_work["isaratul-icaz"])
    hidden = shingles(arabic) - quran_shingles()
    tefsir = sqlite3.connect(OUT / unit / "tefsir.db")
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


def _blocks_plain(text: str) -> str:
    """Notun alıntısı: işaretsiz düz metin, ilk 200 harf."""
    return re.sub(r"\s+", " ", re.sub(r"\*\*|\[[^\]\n]{1,80}\]", "", text)).strip()[:200]


# ---------------------------------------------------------------- kaynakların metni

def draft_sources(log: Path) -> dict[str, tuple[str, str]]:
    """Taslağın kaynak numarası -> (sunucu, kimlik): her sunucunun son `cite` çağrısından (`first` + sıra)."""
    last: dict[str, dict] = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "assistant":
            continue
        for block in event["message"].get("content", []):
            if block.get("type") == "tool_use" and block["name"].endswith("__cite"):
                last[block["name"].split("__")[1]] = block.get("input") or {}
    out = {}
    for server, inp in last.items():
        first = int(inp.get("first") or 1)
        items = inp.get("sources") or inp.get("ids") or []
        for i, item in enumerate(items):
            out[str(first + i)] = (server, item["id"] if isinstance(item, dict) else item)
    return out


class SourceTexts:
    """Kaynak kimliğinden metin: Risale ve tefsir prova veritabanlarından, hadis kütüphanesinden, Kur'ân'dan."""

    def __init__(self, unit: str):
        work = OUT / unit
        self.dbs = {"risale": [work / "risale.db", GENEL_DB], "tefsir": [work / "tefsir.db", TEFSIR_DB],
                    "hadis": [HADIS_DB]}
        self.conns: dict[Path, sqlite3.Connection] = {}

    def _conn(self, path: Path) -> sqlite3.Connection | None:
        if path not in self.conns:
            self.conns[path] = sqlite3.connect(f"file:{path}?mode=ro", uri=True) if path.exists() else None
        return self.conns[path]

    def sentences(self, conn: sqlite3.Connection, sid: str) -> str | None:
        first, _, last = sid.partition("..")
        row = conn.execute("SELECT seq, node_id FROM sentences WHERE id = ?", (first,)).fetchone()
        if not row:
            return None
        if not last:
            return conn.execute("SELECT text FROM sentences WHERE id = ?", (first,)).fetchone()[0]
        end_id = first.rsplit("/", 1)[0] + "/" + last if "/" not in last else last
        end = conn.execute("SELECT seq FROM sentences WHERE id = ?", (end_id,)).fetchone()
        rows = conn.execute("SELECT text FROM sentences WHERE seq BETWEEN ? AND ? ORDER BY seq",
                            (row[0], end[0] if end else row[0])).fetchall()
        return " ".join(t for (t,) in rows)

    def hadith(self, conn: sqlite3.Connection, hid: str) -> str | None:
        for table, col in (("lib_units", "text"),):                    # hadis_db.py
            if _has(conn, table):
                row = conn.execute(f"SELECT {col} FROM {table} WHERE id = ?", (hid,)).fetchone()
                if row:
                    return row[0]
        return self.sentences(conn, hid) if _has(conn, "sentences") else None

    def quran(self, cite: str) -> str | None:
        m = re.search(r"(\d+):(\d+)(?:[-–](\d+))?", cite)
        conn = self._conn(GENEL_DB)
        if not m or "Sûresi" not in cite or conn is None:
            return None
        sura, a, b = int(m[1]), int(m[2]), int(m[3] or m[2])
        rows = conn.execute("SELECT ayah, text FROM quran_ayahs WHERE sura = ? AND ayah BETWEEN ? AND ? ORDER BY ayah",
                            (sura, a, b)).fetchall()
        return " ".join(f"{t} ﴿{n}﴾" for n, t in rows) or None

    def text(self, server: str | None, sid: str | None, cite: str) -> str | None:
        if sid is None:
            return self.quran(cite)
        for path in self.dbs.get(server, []):
            conn = self._conn(path)
            if conn is None:
                continue
            try:
                found = self.hadith(conn, sid) if server == "hadis" else self.sentences(conn, sid)
            except sqlite3.Error:
                found = None
            if found:
                return found
        return None


# ---------------------------------------------------------------- ortak diziler

def _marked(text: str, shared: set) -> str:
    """Paylaşılan 6'lı diziye giren kelimeleri \\x01…\\x02 ile çevirir (işaretleme kaçışlamadan sonra <mark> olur)."""
    if not shared:
        return text
    tokens = re.split(r"(\s+)", text)
    seq = [(w, i) for i, tok in enumerate(tokens) if tok.strip() for w in search_words(tok)]
    covered: set[int] = set()
    for j in range(len(seq) - N + 1):
        if tuple(w for w, _ in seq[j:j + N]) in shared:
            covered |= {i for _, i in seq[j:j + N]}
    return "".join(f"\x01{t}\x02" if i in covered else t for i, t in enumerate(tokens))


def _unmark(html_text: str) -> str:
    return html_text.replace("\x01", '<mark class="ez">').replace("\x02", "</mark>")


# ---------------------------------------------------------------- okuma sayfası

TEMPLATE = Path(__file__).with_name("d1-okuma-sablon.html")
PAGE_OUT = KEEP / "okuma.html"
NOTE_TYPES = {"dogru": "doğru, iyi", "yanlis": "yanlış", "eksik": "eksik", "fazla": "fazla", "uydurma": "uydurma",
              "irab": "i'râb, dil", "belagat": "belâgat", "usul": "usul", "kaynak": "kaynak, atıf",
              "uslup": "üslûp, tercüme", "diger": "diğer"}
# D1.4: usul özetinin 4. ve 8. bölümleri. Kimlikler değişmez (notlar ve rapor onlarla birleşir).
CRITERIA = [
    ("sira", "Sıra ve düzen", "Âyet, gerekirse mukaddime, V1, V2, V3 (özet 4, 8.4)"),
    ("v1", "Birinci vecih: öncesiyle nazım", "Âyetin mâkabliyle irtibatı doğru ve yeterli mi (4.1)"),
    ("v2", "İkinci vecih: cümleler arası nazım", "Cümlelerin birbirini nasıl istediği (4.2)"),
    ("v3", "Üçüncü vecih: hey'et ve kelimeler", "Hey'et, kayıt ve kelime nükteleri; tercih soruları (4.3)"),
    ("maksat", "Dört maksat kuralı", "Asıl maksat söylenmiş; öbürleri yalnız lafza dayanınca, derecesiyle (8.5)"),
    ("mukaddime", "Mukaddime kuralı", "Yalnız dört durumdan biri varsa, kısa, lafza bağlı (8.6)"),
    ("kabul", "Kabul ölçüsü ve delâlet derecesi", "Nükte dile, belâgate ve şeriatin maksatlarına uygun; derecesi belli (8.7)"),
    ("dil", "Dil ve i'râb doğruluğu", "Arapçanın doğruluğu (ehline)"),
    ("belagat", "Belâgat doğruluğu", "Belâgat iddialarının doğruluğu (ehline)"),
    ("kaynak", "Kaynağa bağlılık", "Her iddia bir kaynağa ya da âyetin lafzına bağlı (8.3)"),
    ("uydurma", "Uydurma yok", "Olmayan söz, yanlış atıf, yanlış nakil yok (2: en iyi)"),
    ("uslup", "Üslûp ve tercüme", "Îcâz; Türkçe tercüme Abdülmecid Nursî tarzına yakın (D1.2c)"),
]


def _inline(text: str, sources: dict, lang: str = "ar") -> str:
    import html
    s = html.escape(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    if lang == "tr":            # Türkçe içindeki Arapça: sağdan sola yalıtılır (ayraçlar ters dönmesin)
        s = ARABIC_RUN.sub(lambda m: f'<bdi class="arw" dir="rtl">{m.group(0).strip()}</bdi>'
                           + (" " if m.group(0).endswith(" ") else ""), s)

    def mark(m: re.Match) -> str:
        inner = m.group(1)
        clean = inner.replace("\x01", "").replace("\x02", "")
        if re.fullmatch(r"[\d,\s]+", clean):
            nums = [n.strip() for n in clean.split(",")]
            title = html.escape(" | ".join(f"[{n}] {sources.get(n, '')}" for n in nums), quote=True)
            return f'<span class="ref" data-n="{",".join(nums)}" title="{title}">[{clean}]</span>'
        cls = "own" if "kendi tespiti" in clean else "src"
        nums = re.findall(r"\b\d+\b", clean)
        title = html.escape(" | ".join(f"[{n}] {sources.get(n, '')}" for n in nums), quote=True)
        data = f' data-n="{",".join(nums)}"' if nums else ""
        return f'<span class="mk {cls}"{data} title="{title}">[{clean}]</span>'
    return _unmark(re.sub(r"\[([^\]\n]{1,80})\]", mark, s).replace("\n", "<br>"))


def _hidden_paragraphs(cfg: dict) -> dict[str, dict[str, list[str]]]:
    return {"ar": hidden_sections(cfg, "isaratul-icaz-arabi"), "tr": hidden_sections(cfg, "isaratul-icaz")}


def unit_data(unit: str, quran: set) -> dict | None:
    cfg = UNITS[unit]
    keep = DRAFTS / unit
    paths = sorted(keep.glob("taslak-*.md"), key=lambda p: int(p.stem.split("-")[1]))
    if not paths:
        return None
    hidden = _hidden_paragraphs(cfg)
    hidden_sh = {lang: set().union(*(shingles(p) for ps in secs.values() for p in ps)) - quran
                 for lang, secs in hidden.items()}
    texts = SourceTexts(unit)
    drafts = {}
    for path in paths:
        meta = json.loads((keep / f"{path.stem}.json").read_text())
        raw = path.read_text(encoding="utf-8")
        sections, cites = parse_draft(raw)
        ids = draft_sources(keep / f"{path.stem}.jsonl") if (keep / f"{path.stem}.jsonl").exists() else {}
        sources = {}
        for n, cite in cites.items():
            server, sid = ids.get(n, (None, None))
            sources[n] = {"c": cite, "i": sid, "t": texts.text(server, sid, cite.split(" · ")[0])}
        draft_sh = {lang: set().union(*(shingles(t) for blocks in sections.values() for bl, _, t in blocks if bl == lang))
                    - quran for lang in ("ar", "tr")}
        blocks: dict = {}
        for key, items in sections.items():
            if key not in SECTION_TITLES:
                continue
            for lang in ("ar", "tr"):
                rows = [(kind, text) for bl, kind, text in items if bl == lang]
                blocks.setdefault(key, {})[lang] = [
                    {"a": f"{key}/{lang}/{i}", "q": kind == "quote", "x": _blocks_plain(text),
                     "h": _inline(_marked(text, hidden_sh[lang] if key != "Âyet" else set()), cites, lang)}
                    for i, (kind, text) in enumerate(rows)]
        hidden_html = {lang: {key: [{"a": f"{key}/{lang}/h{i}", "x": _blocks_plain(p),
                                     "h": (_inline(_marked(p, draft_sh[lang]), {}, "tr") if lang == "tr"
                                           else _unmark(__import__("html").escape(_marked(p, draft_sh[lang]))))}
                                    for i, p in enumerate(paras)]
                              for key, paras in secs.items()} for lang, secs in hidden.items()}
        n = path.stem.split("-")[1]
        cost = f", ≈{meta['cost_usd']:.2f} $" if meta.get("cost_usd") else ""
        drafts[path.stem] = {
            "label": f"Taslak {n}", "short": f"istem {meta.get('istem', 'tam')}",
            "meta": (f"{meta['model']}, {meta['effort']}, istem {meta.get('istem', 'tam')} ({meta.get('prompt_sha', '')}), "
                     f"{meta['seconds'] // 60} dk{cost}, {sum(meta['calls'].values())} araç çağrısı, "
                     f"{len(cites)} kaynak, ortak dizi: Arapça {len(draft_sh['ar'] & hidden_sh['ar'])}"),
            "blocks": blocks, "sources": sources, "hidden": hidden_html}
    ayahs = "–".join(map(str, cfg["ayahs"]))
    return {"title": f"{cfg['sura_name']} {ayahs}", "sections": SECTION_TITLES, "drafts": drafts,
            "hidden_titles": {"ar": "İşârâtü'l-İ'câz (Arapça asıl)", "tr": "Abdülmecid Nursî tercümesi"}}


def okuma() -> None:
    quran = quran_shingles()
    units = {u: d for u in UNITS if (d := unit_data(u, quran))}
    data = {"units": units, "note_types": NOTE_TYPES, "criteria": CRITERIA}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    PAGE_OUT.write_text(TEMPLATE.read_text(encoding="utf-8").replace("{data}", blob), encoding="utf-8")
    counts = ", ".join(f"{u}: {len(d['drafts'])} taslak" for u, d in units.items())
    print(f"{PAGE_OUT.relative_to(ROOT)} ({counts})")


# ---------------------------------------------------------------- notlar

NOTES_DIR = KEEP / "notlar"


def notlar(files: list[Path]) -> None:
    """Dışa aktarılan not dosyalarını `data/d1/notlar/`a alır; bütün dosyalardan birim başına `notlar.md` yazar."""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    for f in files:
        payload = json.loads(f.read_text(encoding="utf-8"))
        if payload.get("app") != "d1-okuma":
            sys.exit(f"{f}: okuma sayfasının dışa aktarma dosyası değil")
        target = NOTES_DIR / f.name
        if not target.exists():
            shutil.copyfile(f, target)
            print(f"alındı: {target.relative_to(ROOT)}")
    notes: dict[str, dict] = {}
    rubric: dict[tuple, dict] = {}
    for f in sorted(NOTES_DIR.glob("*.json")):
        payload = json.loads(f.read_text(encoding="utf-8"))
        for n in payload.get("notes", []):
            if n["id"] not in notes or n["at"] > notes[n["id"]]["at"]:
                notes[n["id"]] = n
        for r in payload.get("rubric", []):
            rubric[(r["unit"], r["draft"], r["reader"])] = r["scores"]
    for unit in UNITS:
        mine = [n for n in notes.values() if n["unit"] == unit]
        scores = {k: v for k, v in rubric.items() if k[0] == unit}
        if not mine and not scores:
            continue
        path = DRAFTS / unit / "notlar.md"
        path.write_text(notes_report(unit, mine, scores), encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {len(mine)} not, {len(scores)} çizelge")


def notes_report(unit: str, notes: list[dict], scores: dict) -> str:
    drafts = sorted({n["draft"] for n in notes} | {k[1] for k in scores}, key=lambda d: int(d.split("-")[1]))
    readers = sorted({n["reader"] for n in notes} | {k[2] for k in scores})
    lines = [f"# Prova {unit}: okuma notları", "",
             f"`uv run python scripts/d1-prova.py notlar` ile `data/d1/notlar/` dosyalarından üretilir; elle "
             f"düzenlenmez. Okuyucular: {', '.join(readers)}.", ""]
    lines += ["## Sayılar", "", "| Taslak | " + " | ".join(NOTE_TYPES.values()) + " | ehline sor |",
              "|---|" + "---:|" * (len(NOTE_TYPES) + 1)]
    for d in drafts:
        c = Counter(n["type"] for n in notes if n["draft"] == d)
        e = sum(1 for n in notes if n["draft"] == d and n.get("expert"))
        lines.append(f"| {d} | " + " | ".join(str(c.get(k, 0) or "") for k in NOTE_TYPES) + f" | {e or ''} |")
    if scores:
        cols = sorted(scores, key=lambda k: (int(k[1].split("-")[1]), k[2]))
        lines += ["", "## Ölçüt çizelgesi", "", "0 yok ya da yanlış, 1 kısmen, 2 iyi; boş: bakılmadı.", "",
                  "| Ölçüt | " + " | ".join(f"{d} · {r}" for _, d, r in cols) + " |",
                  "|---|" + "---:|" * len(cols)]
        for key, label, _ in CRITERIA:
            vals = [scores[c].get(key, {}).get("score") for c in cols]
            lines.append(f"| {label} | " + " | ".join("" if v is None else str(v) for v in vals) + " |")
        totals = [sum(v.get("score") or 0 for v in scores[c].values()) for c in cols]
        lines.append("| **Toplam** | " + " | ".join(f"**{t}**" for t in totals) + " |")
        reasons = [(c, key, scores[c][key]["note"]) for c in cols for key, _, _ in CRITERIA
                   if scores[c].get(key, {}).get("note")]
        if reasons:
            labels = {k: lab for k, lab, _ in CRITERIA}
            lines += ["", "Gerekçeler:", ""] + [f"- {d} · {r} · {labels[k]}: {t}" for (_, d, r), k, t in reasons]
    expert = [n for n in notes if n.get("expert")]
    if expert:
        lines += ["", "## Ehline sorulacaklar", ""]
        for n in sorted(expert, key=lambda n: (n["draft"], n["anchor"])):
            lines += [f"- **{n['draft']} · {SECTION_TITLES.get(n['anchor'].split('/')[0], n['anchor'])}** "
                      f"({n['reader']}): {n['text']}", f"  > {n.get('excerpt', '')}"]
    side_name = {"taslak": "taslakta", "isarat": "İşârât'ın metninde", "bolum": "bölüme"}
    for d in drafts:
        lines += ["", f"## {d}", ""]
        for key in SECTION_TITLES:
            ns = sorted((n for n in notes if n["draft"] == d and n["anchor"].split("/")[0] == key),
                        key=lambda n: (n["side"], n["anchor"], n["at"]))
            if not ns:
                continue
            lines += [f"### {SECTION_TITLES[key]}", ""]
            for n in ns:
                lines += [f"- **{NOTE_TYPES.get(n['type'], n['type'])}, {['', 'küçük', 'orta', 'önemli'][n['severity']]}**"
                          f"{' · ehline sor' if n.get('expert') else ''} · {side_name.get(n['side'], n['side'])} "
                          f"({n.get('lang', '')}) · {n['reader']}: {n['text']}"]
                if n.get("excerpt") and n["side"] != "bolum":
                    lines.append(f"  > {n['excerpt']}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


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
    sub.add_parser("okuma")
    p = sub.add_parser("notlar")
    p.add_argument("files", nargs="*", type=Path, help="okuyucuların dışa aktardığı not dosyaları")
    args = parser.parse_args()
    if args.command == "hazirla":
        hazirla(args.unit, args.istem, args.db_yenile)
    elif args.command == "yazdir":
        yazdir(args.unit, args.kez, args.model, args.effort, args.istem)
    elif args.command == "okuma":
        okuma()
    elif args.command == "notlar":
        notlar(args.files)
    else:
        karsilastir(args.unit)


if __name__ == "__main__":
    main()
