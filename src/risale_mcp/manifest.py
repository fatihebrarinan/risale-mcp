"""Kimlik manifestosu ve derlem sürümü (H1, `docs/tefsir-altyapi-plani.md`).

    uv run python -m risale_mcp.manifest status [--profile genel]
    uv run python -m risale_mcp.manifest release [--profile genel] [--label 2026-11-04]
    uv run python -m risale_mcp.manifest diff <eski.json.gz> <yeni.json.gz>

Atıflar cümle kimliğine dayanır; kimlik kayarsa verilmiş atıf başka cümleyi gösterir. Cümle bölücü ve ayrıştırıcılar
bütün eserlerde ortaktır: bir eser için yapılan değişiklik başka bir eserin numaralarını sessizce kaydırabilir.
Manifesto, bir profilin bütün cümle kimliklerini metin özetleriyle (`sentences.hash`) ve bütün bölüm kimliklerini
atıf yollarıyla (`ref`) tutar.

**Kurulumda denetim** (`build_db.build_profile`): yeni veritabanı geçici dosyadayken manifestosu çıkarılır ve
profilin kabul edilmiş manifestosuyla (`data/manifest/<profil>/accepted.json.gz`) karşılaştırılır:

- yeni cümle ya da bölüm (yeni eser, eksik bölüm tamamlandı): kabul edilir, manifesto güncellenir;
- bölümün atıf yolu değişti (başlık düzeltmesi): kabul edilir, raporda uyarı;
- **silinen ya da metni değişen cümle, silinen bölüm**: kurulum durur, veritabanı yazılmaz. Kasıtlıysa
  `build_db --accept-id-changes` (ya da `build --accept-id-changes`). Rapor `data/manifest/<profil>/changes/`'te:
  eser ve bölüm başına sayılar; bölümün özet dizisi kaymışsa (araya cümle girmiş ya da çıkmışsa) kaymanın
  başladığı cümle.

İlk kurulumda kabul edilmiş manifesto yoksa o kurulumun manifestosu kabul edilir.

**Derlem özeti ve sürüm:** her kurulum `meta`ya `corpus_hash` yazar (kimlik, özet ve bölüm yolu dizisinin SHA-256'sı,
12 hane; aynı metin aynı özeti verir). `release` yayına çıkacak veritabanına bir etiket verir (varsayılan bugünün
tarihi): manifestonun kopyası `releases/<etiket>.json.gz`, liste `releases.json`, önceki sürümle farklar
`releases/<etiket>.md`; veritabanının `meta`sına `corpus_version` yazılır. Yeniden kurulan veritabanının özeti
yayınlanmış bir sürümünkiyle aynıysa `corpus_version` kendiliğinden gelir. `cite` sonucu `corpus_version` taşır:
atfın hangi metin sürümüne dayandığı yıllar sonra da bilinir. Sürüm yalnız genel profil için anlamlıdır, ama
denetim iki profilde de çalışır (`private` eserlerin kimlikleri de korunur).

Manifestolar git'e eklenmez (≈250 bin cümle); `data/manifest/` silinmemeli: eski sürümlerin tek kaydıdır.
"""

import argparse
import gzip
import hashlib
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

from risale_mcp.paths import DATA_DIR, ROOT

MANIFEST_DIR = DATA_DIR / "manifest"
EXAMPLES = 5                     # raporda bölüm başına örnek


class IdChangesError(RuntimeError):
    """Kurulum var olan kimlikleri değiştirdi; veritabanı yazılmadı."""


@dataclass
class Manifest:
    sentences: list[tuple[str, str, str]]        # (kimlik, düğüm, özet), okuma sırasıyla
    nodes: list[tuple[str, str]]                 # (kimlik, atıf yolu)
    meta: dict = field(default_factory=dict)

    @classmethod
    def from_db(cls, conn: sqlite3.Connection) -> "Manifest":
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        if "lib_units" in tables:
            # hadis sunucusu (`hadis_db.py`): atıf birimi hadistir, bölüm kitap ve bâb ağacıdır; özet metnin kendisinden
            sentences = [(id_, node, hashlib.sha1(text.encode("utf-8")).hexdigest()[:12])
                         for id_, node, text in conn.execute("SELECT id, node_id, text FROM lib_units ORDER BY seq")]
            nodes = [tuple(r) for r in conn.execute("SELECT id, title FROM lib_nodes ORDER BY seq")]
            return cls(sentences, nodes)
        sentences = [tuple(r) for r in conn.execute("SELECT id, node_id, hash FROM sentences ORDER BY seq")]
        nodes = [tuple(r) for r in conn.execute("SELECT id, ref FROM nodes ORDER BY seq")]
        return cls(sentences, nodes)

    @property
    def corpus_hash(self) -> str:
        digest = hashlib.sha256()
        for sid, _, h in self.sentences:
            digest.update(f"s\t{sid}\t{h}\n".encode())
        for nid, ref in self.nodes:
            digest.update(f"n\t{nid}\t{ref}\n".encode())
        return digest.hexdigest()[:12]

    def save(self, path: Path, **meta) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"meta": {"corpus_hash": self.corpus_hash, "sentences": len(self.sentences), "nodes": len(self.nodes),
                         **self.meta, **meta},
                "nodes": self.nodes, "sentences": self.sentences}
        tmp = path.with_name(path.name + ".tmp")
        with gzip.open(tmp, "wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        tmp.replace(path)

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        with gzip.open(path, "rt", encoding="utf-8") as f:
            data = json.load(f)
        return cls([tuple(s) for s in data["sentences"]], [tuple(n) for n in data["nodes"]], data["meta"])


@dataclass
class Changes:
    added_sentences: list[str] = field(default_factory=list)
    removed_sentences: list[str] = field(default_factory=list)
    changed_sentences: list[str] = field(default_factory=list)     # aynı kimlik, başka metin
    added_nodes: list[str] = field(default_factory=list)
    removed_nodes: list[str] = field(default_factory=list)
    renamed_nodes: list[tuple[str, str, str]] = field(default_factory=list)   # (kimlik, eski yol, yeni yol)
    shifts: dict[str, str] = field(default_factory=dict)           # düğüm -> kaymanın başladığı cümle
    node_of: dict[str, str] = field(default_factory=dict)          # rapordaki cümlelerin düğümü

    @property
    def breaking(self) -> bool:
        return bool(self.removed_sentences or self.changed_sentences or self.removed_nodes)

    @property
    def empty(self) -> bool:
        return not (self.breaking or self.added_sentences or self.added_nodes or self.renamed_nodes)

    def summary(self) -> str:
        parts = [f"{len(v)} {k}" for k, v in (
            ("cümle silindi", self.removed_sentences), ("cümlenin metni değişti", self.changed_sentences),
            ("bölüm silindi", self.removed_nodes), ("cümle eklendi", self.added_sentences),
            ("bölüm eklendi", self.added_nodes), ("bölümün yolu değişti", self.renamed_nodes)) if v]
        return ", ".join(parts) or "fark yok"

    def report(self, title: str) -> str:
        lines = [f"# {title}", "", self.summary() + ".", ""]
        if self.breaking:
            lines += ["**Var olan kimlikler değişti:** bu kimliklere verilmiş atıflar başka metni gösterebilir.", ""]

        def by_node(ids: list[str]) -> dict[str, list[str]]:
            out = defaultdict(list)
            for sid in ids:
                out[self.node_of.get(sid) or _node_of(sid)].append(sid)
            return out

        for label, ids in (("Silinen cümleler", self.removed_sentences), ("Metni değişen cümleler", self.changed_sentences),
                           ("Eklenen cümleler", self.added_sentences)):
            if not ids:
                continue
            works = Counter(sid.split("/", 1)[0] for sid in ids)
            lines += [f"## {label} ({len(ids)})", "", "Eser başına: " + ", ".join(f"{w} {n}" for w, n in works.most_common()), ""]
            for node, items in sorted(by_node(ids).items()):
                shift = f"; kayma {self.shifts[node]}'den başlıyor" if node in self.shifts else ""
                more = f" (+{len(items) - EXAMPLES})" if len(items) > EXAMPLES else ""
                lines.append(f"- `{node}` {len(items)}{shift}: " + ", ".join(f"`{s.rsplit('/', 1)[-1]}`" for s in items[:EXAMPLES]) + more)
            lines.append("")
        for label, ids in (("Silinen bölümler", self.removed_nodes), ("Eklenen bölümler", self.added_nodes)):
            if ids:
                lines += [f"## {label} ({len(ids)})", ""] + [f"- `{n}`" for n in ids[:200]] + [""]
        if self.renamed_nodes:
            lines += [f"## Yolu değişen bölümler ({len(self.renamed_nodes)})", ""]
            lines += [f"- `{n}`: {old} → {new}" for n, old, new in self.renamed_nodes[:200]] + [""]
        return "\n".join(lines)


def _node_of(sentence_id: str) -> str:
    """Cümlenin düğümü (hâşiye cümlesinde ana cümlenin düğümü): kimlikten, veritabanına bakmadan."""
    parts = sentence_id.split("/")
    while parts and not (parts[-1].startswith("c") and parts[-1][1:].isdigit()):
        parts.pop()
    while parts and (parts[-1].startswith(("c", "h", "s")) and parts[-1][1:].isdigit()):
        parts.pop()
    return "/".join(parts)


def diff(old: Manifest, new: Manifest) -> Changes:
    changes = Changes()
    old_s = {sid: h for sid, _, h in old.sentences}
    new_s = {sid: h for sid, _, h in new.sentences}
    changes.removed_sentences = [sid for sid, _, _ in old.sentences if sid not in new_s]
    changes.added_sentences = [sid for sid, _, _ in new.sentences if sid not in old_s]
    changes.changed_sentences = [sid for sid, _, h in old.sentences if sid in new_s and new_s[sid] != h]
    old_n, new_n = dict(old.nodes), dict(new.nodes)
    changes.removed_nodes = [n for n, _ in old.nodes if n not in new_n]
    changes.added_nodes = [n for n, _ in new.nodes if n not in old_n]
    changes.renamed_nodes = [(n, ref, new_n[n]) for n, ref in old.nodes if n in new_n and new_n[n] != ref]
    listed = set(changes.removed_sentences) | set(changes.changed_sentences) | set(changes.added_sentences)
    changes.node_of = {sid: node for sid, node, _ in (*old.sentences, *new.sentences) if sid in listed}
    touched = {s[1] for s in old.sentences if s[0] in set(changes.removed_sentences) | set(changes.changed_sentences)}
    if touched:
        old_seq, new_seq = defaultdict(list), defaultdict(list)
        for sid, node, h in old.sentences:
            if node in touched:
                old_seq[node].append((sid, h))
        for sid, node, h in new.sentences:
            if node in touched:
                new_seq[node].append((sid, h))
        for node in touched:
            a, b = [h for _, h in old_seq[node]], [h for _, h in new_seq[node]]
            ops = SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
            at = next((i for i, op in enumerate(ops) if op[0] != "equal"), None)
            first = ops[at] if at is not None else None
            # Kayma: değişiklikten sonra eski dizinin geri kalanı yeni dizide başka konumdan sürüyorsa
            if first and any(op[0] == "equal" and op[1] != op[3] for op in ops[at + 1:]):
                changes.shifts[node] = old_seq[node][first[1]][0].rsplit("/", 1)[-1] if first[1] < len(a) else "son"
    return changes


# --- profil başına dosyalar ---

def profile_dir(profile: str) -> Path:
    return MANIFEST_DIR / profile


def releases(profile: str) -> list[dict]:
    path = profile_dir(profile) / "releases.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def release_for(profile: str, corpus_hash: str) -> str | None:
    return next((r["label"] for r in reversed(releases(profile)) if r["corpus_hash"] == corpus_hash), None)


def check_build(conn: sqlite3.Connection, profile: str, accept: bool = False) -> Changes:
    """`build_db` geçici veritabanında çağırır: `meta`ya özet ve sürümü yazar, kabul edilmiş manifestoyla
    karşılaştırır. Var olan kimlik değiştiyse ve `accept` yoksa `IdChangesError` (veritabanı yazılmaz)."""
    manifest = Manifest.from_db(conn)
    corpus_hash = manifest.corpus_hash
    rows = [("corpus_hash", corpus_hash)]
    if label := release_for(profile, corpus_hash):
        rows.append(("corpus_version", label))
    conn.executemany("INSERT OR REPLACE INTO meta VALUES (?, ?)", rows)
    accepted_path = profile_dir(profile) / "accepted.json.gz"
    if not accepted_path.exists():
        manifest.save(accepted_path, accepted_at=_now(), note="ilk manifesto")
        return Changes()
    accepted = Manifest.load(accepted_path)
    if accepted.meta.get("corpus_hash") == corpus_hash:
        return Changes()
    changes = diff(accepted, manifest)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    report = profile_dir(profile) / "changes" / f"{stamp}.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    status = "kabul edildi" if accept or not changes.breaking else "REDDEDİLDİ (veritabanı yazılmadı)"
    report.write_text(changes.report(f"Kimlik değişiklikleri: {profile}, {stamp}, {status}") + "\n", encoding="utf-8")
    if changes.breaking and not accept:
        shown = report.relative_to(ROOT) if report.is_relative_to(ROOT) else report
        raise IdChangesError(f"{profile}: var olan kimlikler değişti ({changes.summary()}); rapor: {shown}. "
                             "Kasıtlıysa --accept-id-changes ile yeniden kurun.")
    manifest.save(accepted_path, accepted_at=_now(), previous=accepted.meta.get("corpus_hash"))
    return changes


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def release(db: Path, profile: str, label: str | None = None) -> str:
    """Veritabanına sürüm etiketi verir; manifestonun kopyasını ve önceki sürümle farkları saklar."""
    conn = sqlite3.connect(db)
    try:
        meta = dict(conn.execute("SELECT key, value FROM meta"))
        corpus_hash = meta.get("corpus_hash")
        if not corpus_hash:
            raise SystemExit(f"{db}: corpus_hash yok; veritabanını `build_db --profile {profile}` ile yeniden kurun.")
        accepted_path = profile_dir(profile) / "accepted.json.gz"
        accepted = Manifest.load(accepted_path) if accepted_path.exists() else None
        if accepted is None or accepted.meta.get("corpus_hash") != corpus_hash:
            raise SystemExit("Veritabanı kabul edilmiş manifestoyla tutmuyor; önce `build_db` ile yeniden kurun.")
        listed = releases(profile)
        if existing := release_for(profile, corpus_hash):
            label = existing
        else:
            label = label or datetime.now().strftime("%Y-%m-%d")
            taken = {r["label"] for r in listed}
            base, n = label, 2
            while label in taken:
                label, n = f"{base}-{n}", n + 1
            out = profile_dir(profile) / "releases"
            accepted.save(out / f"{label}.json.gz", label=label, released_at=_now())
            if listed:
                previous = Manifest.load(out / f"{listed[-1]['label']}.json.gz")
                changes = diff(previous, accepted)
                (out / f"{label}.md").write_text(
                    changes.report(f"Sürüm {label} ({profile}): {listed[-1]['label']} sürümünden farklar") + "\n",
                    encoding="utf-8")
            listed.append({"label": label, "corpus_hash": corpus_hash, "released_at": _now(),
                           "built_at": meta.get("built_at"), "sentences": len(accepted.sentences),
                           "nodes": len(accepted.nodes)})
            (profile_dir(profile) / "releases.json").write_text(
                json.dumps(listed, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        with conn:
            conn.execute("INSERT OR REPLACE INTO meta VALUES ('corpus_version', ?)", (label,))
    finally:
        conn.close()
    return label


def status(db: Path, profile: str) -> list[str]:
    meta = dict(sqlite3.connect(db).execute("SELECT key, value FROM meta")) if db.exists() else {}
    accepted_path = profile_dir(profile) / "accepted.json.gz"
    accepted = Manifest.load(accepted_path).meta if accepted_path.exists() else {}
    listed = releases(profile)
    return [f"profil: {profile}",
            f"veritabanı: corpus_hash {meta.get('corpus_hash', '-')}, sürüm {meta.get('corpus_version', 'yayınlanmadı')}, "
            f"kuruluş {meta.get('built_at', '-')}",
            f"kabul edilmiş manifesto: {accepted.get('corpus_hash', 'yok')} ({accepted.get('sentences', 0)} cümle)",
            "sürümler: " + (", ".join(f"{r['label']} ({r['corpus_hash']})" for r in listed[-5:]) or "yok")]


def main() -> None:
    from risale_mcp.profiles import PROFILES

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "release"):
        p = sub.add_parser(name)
        p.add_argument("--profile", choices=PROFILES, default="genel")
        if name == "release":
            p.add_argument("--label", help="sürüm etiketi (varsayılan bugünün tarihi)")
    d = sub.add_parser("diff")
    d.add_argument("old", type=Path)
    d.add_argument("new", type=Path)
    args = parser.parse_args()
    if args.command == "diff":
        changes = diff(Manifest.load(args.old), Manifest.load(args.new))
        print(changes.report(f"{args.old.name} → {args.new.name}"))
        sys.exit(1 if changes.breaking else 0)
    profile = PROFILES[args.profile]
    if args.command == "status":
        print("\n".join(status(profile.db, profile.name)))
    else:
        label = release(profile.db, profile.name, args.label)
        print(f"{profile.name}: sürüm {label}")


if __name__ == "__main__":
    main()
