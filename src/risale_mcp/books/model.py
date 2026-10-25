"""Bir eserin kaynaktan bağımsız modeli: başlık ağacı, paragraflar, hâşiyeler.

Ayrıştırıcılar (`books/erisale.py` vb.) metni `TextBuilder` ile kurar, düğüm ve
paragrafları `Book` üzerinden ekler; `Book.to_json()` `data/books/<eser>.json` biçimidir.

Kimlikler:
    düğüm      sozler/10/on-iki-hakikat/hakikat-09
    paragraf   sozler/10/on-iki-hakikat/hakikat-09/p003
    hâşiye     sozler/10/on-iki-hakikat/hakikat-09/p003/h1   (başlıktaysa <düğüm>/h1)
"""

import re
import unicodedata
from dataclasses import dataclass, field

REF_SEPARATOR = " › "


@dataclass
class ArabicSpan:
    """Metnin içindeki Arapça (ya da Farsça, Osmanlıca) parça. `start`/`end` karakter konumudur."""
    start: int
    end: int
    kind: str              # ayet, hadis, arabi, farsi, kurdi, osmani
    meal: str | None = None
    source: str | None = None  # âyet için sûre ve âyet, ör. "Fâtiha Sûresi, 1:1"

    def to_json(self) -> dict:
        data = {"start": self.start, "end": self.end, "kind": self.kind}
        if self.meal:
            data["meal"] = self.meal
        if self.source:
            data["source"] = self.source
        return data


@dataclass
class FootnoteMark:
    """Metindeki hâşiye işareti: hâşiye, `offset` konumundaki kelimeye bağlıdır."""
    offset: int
    content: object  # kaynağa özgü hâşiye içeriği; ayrıştırıcı yorumlar


class TextBuilder:
    """Parça parça gelen metni tek satırlık düz metne çevirir; boşlukları sadeleştirir,
    Arapça parçaların ve hâşiye işaretlerinin konumlarını tutar."""

    def __init__(self) -> None:
        self._parts: list[str] = []
        self._length = 0
        self.arabic: list[ArabicSpan] = []
        self.footnotes: list[FootnoteMark] = []
        self._arabic_key: object = None  # son Arapça parçanın kaynaktaki kimliği

    def _ends_with_space(self) -> bool:
        return bool(self._parts) and self._parts[-1].endswith(" ")

    def add(self, text: str, arabic: ArabicSpan | None = None, key: object = None) -> None:
        """`arabic` verilirse parça Arapçadır; aynı `key` ile art arda gelen parçalar tek parça sayılır."""
        text = re.sub(r"\s+", " ", text)
        if not self._length or self._ends_with_space():
            text = text.lstrip()
        if not text:
            return
        start, end = self._length, self._length + len(text.rstrip())
        if arabic is None:
            if text.strip():                 # arada yalnızca boşluk varsa Arapça parça sürer
                self._arabic_key = None
        elif key is not None and key == self._arabic_key:
            self.arabic[-1].end = end
        else:
            arabic.start, arabic.end = start, end
            self.arabic.append(arabic)
            self._arabic_key = key
        self._parts.append(text)
        self._length += len(text)

    def mark_footnote(self, content: object) -> None:
        offset = self._length - 1 if self._ends_with_space() else self._length
        self.footnotes.append(FootnoteMark(max(offset, 0), content))

    def build(self) -> str:
        text = "".join(self._parts).rstrip()
        for span in self.arabic:
            span.end = min(span.end, len(text))
        for mark in self.footnotes:
            mark.offset = min(mark.offset, len(text))
        return text


@dataclass
class Text:
    """Kurulmuş metin: düz metin, Arapça parçalar, hâşiye işaretleri."""
    text: str
    arabic: list[ArabicSpan] = field(default_factory=list)
    footnotes: list[FootnoteMark] = field(default_factory=list)

    @classmethod
    def from_builder(cls, builder: TextBuilder) -> "Text":
        text = builder.build()
        return cls(text, builder.arabic, builder.footnotes)

    @classmethod
    def join(cls, texts: list["Text"], separator: str) -> "Text":
        """Satırları (şiir) ya da paragrafları (hâşiye) konumları kaydırarak birleştirir."""
        out = cls("")
        for t in texts:
            if not t.text:
                continue
            shift = len(out.text) + len(separator) if out.text else 0
            out.text = f"{out.text}{separator}{t.text}" if out.text else t.text
            out.arabic += [ArabicSpan(a.start + shift, a.end + shift, a.kind, a.meal, a.source) for a in t.arabic]
            out.footnotes += [FootnoteMark(f.offset + shift, f.content) for f in t.footnotes]
        return out

    def is_arabic(self) -> bool:
        """Boşluk ve noktalama dışındaki bütün karakterleri Arapça parçaların içinde mi?
        (Harf yerine karakter: "﷽" Unicode'da harf değil, semboldür.)"""
        inside = [False] * len(self.text)
        for span in self.arabic:
            for i in range(span.start, span.end):
                inside[i] = True
        signs = [inside[i] for i, ch in enumerate(self.text) if unicodedata.category(ch)[0] not in "PZ"]
        return bool(signs) and all(signs)


@dataclass
class Node:
    id: str
    title: str
    parent: "Node | None"
    type: str | None = None
    number: int | None = None
    heading: str | None = None      # "H1"…"H6" ya da satır içi başlıkta "inline"
    subtitle: str = ""
    toc_title: str | None = None    # kaynağın içindekiler listesindeki adı, basılı başlıktan farklıysa
    url: str | None = None          # kaynaktaki bölüm sayfası (doğrulama için)
    children: list["Node"] = field(default_factory=list)
    paragraph_count: int = 0

    def path(self) -> list[str]:
        return [] if self.parent is None else self.parent.path() + [self.title]

    def ref(self, book_title: str) -> str:
        return REF_SEPARATOR.join([book_title] + self.path())

    def child_id(self, local: str) -> str:
        base = f"{self.id}/{local}"
        taken = {c.id for c in self.children}
        candidate, k = base, 2
        while candidate in taken:
            candidate, k = f"{base}-{k}", k + 1
        return candidate


@dataclass
class Book:
    slug: str
    title: str
    meta: dict                        # grup, kaynak vb.
    root: Node = field(init=False)
    paragraphs: list[dict] = field(default_factory=list)
    notes: list[dict] = field(default_factory=list)  # kaynağın editör notları; metne girmez
    gaps: list[dict] = field(default_factory=list)   # kaynakta bulunamayan metin
    renamed: list[str] = field(default_factory=list) # kardeşiyle aynı adı taşıdığı için ek alan kimlikler
    _hasiye_counts: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.root = Node(self.slug, self.title, None)

    def add_node(self, parent: Node, local: str, title: str, **fields) -> Node:
        node = Node(parent.child_id(local), title, parent, **fields)
        if node.id != f"{parent.id}/{local}":
            self.renamed.append(node.id)
        parent.children.append(node)
        return node

    def add_paragraph(self, node: Node, kind: str, text: Text, **extra) -> dict:
        node.paragraph_count += 1
        record = {"id": f"{node.id}/p{node.paragraph_count:03d}", "node_id": node.id,
                  "kind": kind, "text": text.text, **extra}
        if text.arabic:
            record["arabic"] = [a.to_json() for a in text.arabic]
        self.paragraphs.append(record)
        return record

    def add_hasiye(self, parent_id: str, node: Node, offset: int, text: Text) -> dict:
        """Hâşiye kaydı. `parent_id` bir paragraf, bir hâşiye ya da (başlıktaki hâşiyede) düğümdür."""
        k = self._hasiye_counts[parent_id] = self._hasiye_counts.get(parent_id, 0) + 1
        record = {"id": f"{parent_id}/h{k}", "node_id": node.id, "kind": "hasiye",
                  "parent_id": parent_id, "offset": offset, "text": text.text}
        if text.arabic:
            record["arabic"] = [a.to_json() for a in text.arabic]
        self.paragraphs.append(record)
        return record

    def nodes(self) -> list[Node]:
        out: list[Node] = []

        def walk(node: Node) -> None:
            out.append(node)
            for child in node.children:
                walk(child)
        walk(self.root)
        return out

    def outline(self) -> list[dict]:
        records = []
        for node in self.nodes():
            record = {"id": node.id, "parent_id": node.parent.id if node.parent else None,
                      "title": node.title, "ref": node.ref(self.title)}
            for key in ("subtitle", "toc_title", "type", "number", "heading", "url"):
                value = getattr(node, key)
                if value not in (None, ""):
                    record[key] = value
            records.append(record)
        return records

    def to_json(self) -> dict:
        return {"work": self.slug, "title": self.title, **self.meta,
                "outline": self.outline(), "paragraphs": self.paragraphs,
                "notes": self.notes, "gaps": self.gaps}
