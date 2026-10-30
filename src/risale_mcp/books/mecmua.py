"""Mecmuaların ana ciltlere eşlenmesi: metin tek yerde durur.

Mecmua (Asâ-yı Mûsâ, Zülfikâr…) ana ciltlerdeki risalelerden derlenmiştir. Mecmuanın her
paragrafı ana ciltlerdeki karşılığına eşlenir; eşlenen paragrafın metni mecmuada saklanmaz,
yalnızca `source` (ana cilt paragraflarının kimlikleri) kalır. Eşlenemeyen paragraflar
mecmuaya özgüdür ve metinleriyle kalır.

Eşleme baskıdan bağımsızdır: metinler `match_words` ile işaretsiz kelimelere indirilir
("Risâle-i Nûr’un" = "Risale-i Nur’un"), 5 kelimelik diziler karşılaştırılır.
- En çok diziyi paylaşan ana cilt paragrafından başlanır. Baskılar paragrafları farklı
  bölebildiği için yakın komşular, kapsamı artırdıkça eklenir. Mecmua paragrafının
  dizilerinin en az %35'i (ve en az 3 dizi) bu paragraflarda geçiyorsa eşlenir. Eşik
  düşüktür, çünkü Hayrat baskısı başlığı paragrafa katar ("Dördüncü Devâ: …") ve yazımı
  farklıdır ("Çünki"); 5 kelimelik dizilerin rastlantıyla aynı yerde örtüşmesi ise çok nadirdir.
- Aynı metin ana ciltlerde birden çok yerde geçiyorsa bir önceki eşlemenin hemen ardından
  gelen yer seçilir.
- Kısa paragraflar ("Bak!") ancak bir önceki eşlemenin devamıysa ya da ana ciltlerde tek
  bir yerde geçiyorsa eşlenir.
- Mecmua bir ana cilt paragrafını birkaç paragrafa bölmüşse (Hayrat baskısı şiirin her
  satırını ayrı paragraf yapar), aynı düğümde art arda gelen ve ana ciltte örtüşen eşlemeler
  tek kayıtta birleşir; ana cilt paragrafı okunurken bir kez görünür. Kimlikler yeniden
  numaralanmaz, birleşen kaydın kimliği ilkininkidir.
"""

import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from risale_mcp.catalog import WORKS, Group
from risale_mcp.normalize import match_words

SHINGLE = 5
MIN_SCORE = 0.35         # eşlenmek için dizilerin en az bu oranı ana ciltte bulunmalı…
MIN_HITS = 3             # …ve en az bu kadar dizi (5 kelimelik dizilerin rastlantıyla örtüşmesi çok nadirdir)
GROW_UNTIL = 0.9         # komşu paragraf eklemeyi bu kapsamda bırak
GAP = 4                  # komşu sayılan en uzak sıra farkı (arada hâşiye ya da Arapça kayıt olabilir)
CANONICAL_GROUPS = {Group.ESKI_SAID, Group.ANA_CILT}


def _shingles(words: list[str]) -> list[int]:
    return [hash(" ".join(words[i:i + SHINGLE])) for i in range(len(words) - SHINGLE + 1)]


@dataclass
class CanonicalIndex:
    """Ana ciltlerin bütün paragrafları (hâşiyeler dahil), kitap sırasıyla."""
    paragraphs: list[tuple[str, str, str]] = field(default_factory=list)  # (eser, paragraf, düğüm)
    shingles: dict[int, list[int]] = field(default_factory=lambda: defaultdict(list))
    short: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list))

    @classmethod
    def load(cls, books_dir: Path) -> "CanonicalIndex":
        index = cls()
        for work in WORKS:
            path = books_dir / f"{work.slug}.json"
            # İkincil kaynaktaki (Âsâr-ı Bedîiyye) eserler ana metin sayılmaz; onlar da ana ciltlere eşlenir.
            if work.source and (work.group in CANONICAL_GROUPS or work.slug == "hizb-i-nuri") and not work.is_secondary and not work.private and path.exists():
                index.add(work.slug, json.loads(path.read_text(encoding="utf-8")))
        return index

    def add(self, work: str, book: dict) -> None:
        for p in book["paragraphs"]:
            if "text" not in p:
                continue
            i = len(self.paragraphs)
            self.paragraphs.append((work, p["id"], p["node_id"]))
            words = match_words(p["text"])
            if len(words) < SHINGLE:
                self.short[" ".join(words)].append(i)
            for h in set(_shingles(words)):
                self.shingles[h].append(i)

    def match(self, text: str, previous: int | None) -> list[int]:
        """Metnin ana ciltlerdeki karşılığı: ardışık paragraf sıraları (boşsa eşleşme yok)."""
        words = match_words(text)
        follows = lambda i: previous is not None and 0 < i - previous <= 3   # noqa: E731
        if len(words) < SHINGLE:
            candidates = self.short.get(" ".join(words), [])
            chosen = [i for i in candidates if follows(i)] or (candidates if len(candidates) == 1 else [])
            return chosen[:1]

        own = set(_shingles(words))
        hits = {h: self.shingles[h] for h in own if h in self.shingles}
        votes = Counter(i for found in hits.values() for i in found)
        if not votes:
            return []
        best = max(votes.values())
        tied = sorted(i for i, v in votes.items() if v >= best * 0.9)
        start = next((i for i in tied if follows(i)), tied[0])
        run = self._grow(start, votes, hits, len(own))
        covered = self._coverage(run, hits)
        return sorted(run) if covered >= min(MIN_HITS, len(own)) and covered / len(own) >= MIN_SCORE else []

    @staticmethod
    def _coverage(run: set[int], hits: dict[int, list[int]]) -> int:
        """Kaç dizi bu paragraflardan en az birinde geçiyor?"""
        return sum(1 for found in hits.values() if not run.isdisjoint(found))

    def _grow(self, start: int, votes: Counter, hits: dict[int, list[int]], total: int) -> set[int]:
        """Baskılar paragrafları farklı bölebilir: mecmua paragrafı ana cildin birkaç ardışık
        paragrafını kapsıyorsa, kapsamı en çok artıran yakın komşular (arada en çok 3 kayıt)
        teker teker eklenir."""
        run = {start}
        covered = self._coverage(run, hits)
        while covered / total < GROW_UNTIL:
            near = {i for i in votes if i not in run and min(abs(i - j) for j in run) <= GAP}
            gains = {i: self._coverage(run | {i}, hits) - covered for i in near}
            best = max(gains, key=gains.get, default=None)
            if best is None or gains[best] <= 0:
                break
            run.add(best)
            covered += gains[best]
        return run


@dataclass
class MappingReport:
    mapped: int = 0
    unique: int = 0
    unique_hasiye: int = 0
    sources: Counter = field(default_factory=Counter)        # ana cilt -> eşlenen paragraf sayısı
    unique_samples: list[str] = field(default_factory=list)
    merged: int = 0                                          # öncekiyle birleşen eşlenmiş paragraf


def _fill_short_backwards(mains: list[dict], found: list[list[int]], index: CanonicalIndex) -> None:
    """Eşlenmemiş kısa paragraf ("﷽", "Bak!"), sonraki paragrafın ana cilt karşılığından hemen
    önce aynı metin duruyorsa oraya bağlanır. Sondan başa gidilir ki art arda kısalar da bağlansın."""
    for k in range(len(mains) - 2, -1, -1):
        nxt = found[k + 1]
        if found[k] or not nxt:
            continue
        key = " ".join(match_words(mains[k]["text"]))
        if len(key.split()) < SHINGLE and nxt[0] - 1 in index.short.get(key, ()):
            found[k] = [nxt[0] - 1]


def map_to_canonical(book: dict, index: CanonicalIndex, kinds: frozenset[str] | None = None) -> MappingReport:
    """Mecmua JSON'unu yerinde değiştirir: eşlenen paragrafların metni yerine `source`,
    düğümlerde `sources` (karşılık gelen ana cilt düğümleri) yazılır. `kinds` verilirse yalnızca bu
    türdeki paragraflar eşlenir."""
    report = MappingReport()
    mains = [p for p in book["paragraphs"] if p["kind"] != "hasiye"]
    found: list[list[int]] = []
    previous: int | None = None
    for p in mains:
        found.append(index.match(p["text"], previous) if kinds is None or p["kind"] in kinds else [])
        previous = found[-1][-1] if found[-1] else previous
    _fill_short_backwards(mains, found, index)
    found_by_id = {p["id"]: f for p, f in zip(mains, found)}

    mapped_ids: set[str] = set()
    merged_into: dict[str, str] = {}            # birleşen paragraf -> birleştiği kayıt
    node_sources: dict[str, list[str]] = defaultdict(list)
    kept = []
    for p in book["paragraphs"]:
        if p["kind"] == "hasiye":
            if p["parent_id"] in merged_into:
                p = p | {"parent_id": merged_into[p["parent_id"]]}
            if p["parent_id"] in mapped_ids:
                if index.match(p["text"], None):
                    continue                    # hâşiye de ana ciltte: metniyle orada duruyor
                report.unique_hasiye += 1
            kept.append(p)
            continue
        if not found_by_id[p["id"]]:
            report.unique += 1
            if len(report.unique_samples) < 12:
                report.unique_samples.append(f"{p['id']}: {p['text'][:70]}")
            kept.append(p)
            continue
        canonical = [index.paragraphs[i] for i in found_by_id[p["id"]]]
        mapped_ids.add(p["id"])
        report.mapped += 1
        report.sources[canonical[0][0]] += 1
        for _, _, node in canonical:
            if node not in node_sources[p["node_id"]]:
                node_sources[p["node_id"]].append(node)
        source = [pid for _, pid, _ in canonical]
        previous = kept[-1] if kept else None
        if previous and "source" in previous and previous["node_id"] == p["node_id"] \
                and not set(previous["source"]).isdisjoint(source):
            previous["source"] += [pid for pid in source if pid not in previous["source"]]
            merged_into[p["id"]] = previous["id"]
            mapped_ids.add(previous["id"])
            report.merged += 1
            continue
        kept.append({"id": p["id"], "node_id": p["node_id"], "kind": p["kind"], "source": source})
    book["paragraphs"] = kept
    for node in book["outline"]:
        if node["id"] in node_sources:
            node["sources"] = node_sources[node["id"]]
    return report
