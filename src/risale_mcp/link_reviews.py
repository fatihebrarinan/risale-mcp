"""Denetim kaydı: bağlar üzerine isimli denetçilerin kararları (H5, `docs/tefsir-altyapi-plani.md`).

    uv run python -m risale_mcp.link_reviews check [--db yol]    # kararları denetler, bağlarıyla eşler
    uv run python -m risale_mcp.link_reviews list                # denetçiler ve kararların sayısı
    uv run python -m risale_mcp.link_reviews add <alan/yöntem.jsonl> --source S --target T --type relation \
        --status reviewed --strength strong --reviewer <kimlik> [--part P] [--reason …] [--date YYYY-MM-DD] [--db yol]

`add` kararı dosyanın sonuna ekler (T4): bağ veritabanında anahtarıyla bulunmalı (yerel profil; `--db`), kararın
verildiği andaki hâli (`seen`: ilişki türü, güç, kapsam) veriden yazılır; geri çekme yalnız aynı denetçinin önceki
kararına, itiraz yalnız gerekçeyle. Model denetçi değildir: komutu bir insan çalıştırır.

Bağlar kurallardan ya da üreten işlerden her kurulumda yeniden çıkar; karar bağın içine yazılamaz. Kararlar ayrı,
yalnız eklenen dosyalardadır: `data/links/reviews/<alan>/<yöntem>.jsonl` (bağ dosyasının adıyla; ör.
`reviews/kuran/relation.jsonl` âyet ilişkilerinin kararları). Kararlar insan emeğidir, yeniden üretilemez; ama
denetçilerin adları ve kararları herkese açık değildir (kullanıcının kararı, 2026-11-05): bu klasör açık depoda
değil, kendi ayrı git deposundadır (`data/links/reviews/.git`), uzak kopyası özel depo `fatihebrarinan/risale-mcp-denetim`. Denetçiler
`reviewers.json`'dadır; listede olmayan denetçinin kararı kurulumu durdurur. Her denetçinin sabit bir numarası
vardır (`number`; bir kez verilir, başkasına geçmez): araçlar ve veritabanı yalnız onu taşır, ad ve kimlik
yayımlanmaz (kullanıcının kararı, 2026-11-05). Okuyan kişiyi değil gerekçeyi tartar; aynı denetçinin kararlarının
tutarlılığını numaradan görür.

Bir satır bir karardır:

    {"link": {"source": "sozler/33/pencere-17", "target": "quran:45:3", "type": "relation"},
     "status": "reviewed", "strength": "strong", "reviewer": "…", "date": "2026-10-27",
     "reason": "…", "seen": {"relation": "acilis", "strength": "strong", "scope": "section"},
     "origin": {"round": 1, "no": 4}}

    link      bağın anahtarı (`links.Link.key`): kaynak (öneksiz yerel kimlik), hedef, tür, parça. Güç ve ilişki
              türü anahtarda değildir: kurallar değişince onlar değişir, kararın konusu da çoğu zaman onlardır
    match     `link` yerine, yalnız eski kararlar için: {"node_prefix", "verse"}. 1. turun örneklemi saklanmadığı
              için bazı kararlar hangi bağa verildiği bilinmeden, bölüm ve âyetle kayıtlıdır; bunlar araçlara
              gitmez, yalnız testi kilitler (kullanıcı bağı seçerse `link`'e çevrilir)
    status    reviewed  denetçi baktı; `strength` onun hükmüdür (kuralınkinden farklı olabilir; araç ikisini de verir)
              disputed  itiraz: bağ yanlış (olmamalı ya da türü yanlış); `reason` zorunlu
              metinden metne lafız ve ilişki bağlarında (tefsir – tefsir, Risale – tefsir) `reason` her kararda
              zorunludur: kararın değeri neden verildiğindedir (kullanıcının kararı, 2026-11-05)
              withdrawn denetçi aynı bağdaki önceki kararını geri çeker
    strength  denetçinin hükmü: strong | weak; weak "zayıf olmalı ya da hiç olmamalı" demektir
    seen      karar verildiğinde bağın hâli (tarih için; anahtar değil)
    origin    kararın geldiği yer (örneklem turu ve numarası)

Hiçbir satır silinmez ve değiştirilmez: itiraz ve geri çekme yeni satırdır. Bir denetçinin bir bağdaki geçerli
kararı dosyadaki son satırıdır; geri çekilen karar geçersizdir ama satırı durur. Farklı denetçilerin kararları yan
yana durur, biri öbürünü silmez. Model önerisi bir karar değildir: denetçi yalnız insandır.

`build_db` geçerli kararları (`link` anahtarlı) `link_reviews` tablosuna yükler; bağı bu profilde bulunmayan
karar yüklenmez ve sayılır (`reviews_unmatched`). Araçlar bağın yanında kararları verir (`find_ayah` links).
"""

import json
import re
import sqlite3
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

from risale_mcp.links import STRENGTHS, TYPES, Link, local_id, text_endpoint
from risale_mcp.paths import DB_PATH, LINKS_DIR

REVIEWS_DIR = LINKS_DIR / "reviews"
REVIEWERS = "reviewers.json"
STATUSES = ("reviewed", "disputed", "withdrawn")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Denetçinin ihtisas alanları (Y1.2, `docs/denetci-olcutu.md` 2). `metin` bağ alanı değildir (cümle bölmesi,
# başlıklar: ayrıştırıcıya döner), kayıtta durur ama hiçbir bağın gerektirdiği alan olmaz.
FIELDS = ("kuran", "hadis", "tefsir", "risale", "metin")


def end_field(value: str, namespace: str | None = None) -> str | None:
    """Bağ ucunun alanı: Kur'ân `kuran`, hadis `hadis`, metin kendi ad alanı (`risale`, `tefsir`). Öneksiz yerel
    kimliğin ad alanı veritabanından gelir (`namespace`); bilinmiyorsa None."""
    if value.startswith("quran:"):
        return "kuran"
    if value.startswith(("hadis:", "hadis-derlem:")):
        return "hadis"
    end = text_endpoint(value)
    return (end[0] or namespace) if end else None


def needed_fields(type_: str, source: str | None, target: str | None) -> tuple[str, ...]:
    """Bağın "denetlendi" sayılması için gereken alanlar (hepsi; `docs/denetci-olcutu.md` 2, kullanıcının kararları
    2026-11-05). Lafız: hedefin alanı. İlişki: iki ucun alanı; ama Kur'ân ile müfessir arasında yalnız `tefsir` (tefsir
    alanı Kur'ân'ı okumayı içerir; Risale alanı Arapça istemediği için Kur'ân – Risale ilişkisi `kuran` ve `risale`
    ister). Gönderme: gönderenin alanı, hedef bir müfessirse `tefsir` de."""
    if type_ == "quote":
        need = {target}
    elif type_ == "relation":
        need = {source, target}
        if need == {"kuran", "tefsir"}:
            need = {"tefsir"}
    else:
        need = {source} | ({"tefsir"} if target == "tefsir" else set())
    return tuple(sorted(f for f in need if f))


def fields_on(person: dict, date: str) -> set[str]:
    """Denetçinin o tarihte kayıtlı olduğu alanlar: alanın `since`'inden sonra, kaydın ve alanın `until`'inden önce."""
    if (until := person.get("until")) and date > until:
        return set()
    return {f for f, d in (person.get("fields") or {}).items()
            if d.get("since", "9999") <= date and not (d.get("until") and date > d["until"])}


@dataclass(frozen=True)
class Review:
    status: str
    reviewer: str
    date: str
    link: dict | None = None
    match: dict | None = None
    strength: str | None = None
    reason: str | None = None
    seen: dict | None = None
    origin: dict | None = None
    file: str = field(default="", compare=False)

    @property
    def key(self) -> tuple | None:
        if not self.link:
            return None
        return local_id(self.link["source"]), self.link["target"], self.link["type"], self.link.get("part") or ""

    def problems(self, reviewers: dict) -> list[str]:
        out = []
        if self.status not in STATUSES:
            out.append(f"status {self.status!r}")
        if self.reviewer not in reviewers:
            out.append(f"denetçi listede yok: {self.reviewer!r}")
        if not _DATE.match(self.date or ""):
            out.append(f"date {self.date!r}")
        if bool(self.link) == bool(self.match):
            out.append("link ya da match (yalnız biri)")
        if self.link and (set(self.link) - {"source", "target", "type", "part"} or self.link.get("type") not in TYPES
                          or not self.link.get("source") or not self.link.get("target")):
            out.append(f"link {self.link!r}")
        if self.strength is not None and self.strength not in STRENGTHS:
            out.append(f"strength {self.strength!r}")
        if self.status == "disputed" and not self.reason:
            out.append("itirazın gerekçesi yok")
        elif self.status == "reviewed" and not self.reason and needs_reason(self.link):
            out.append("metinden metne bağın kararı gerekçesiz olmaz")
        return out

    def to_json(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v not in (None, "", {}) and k != "file"}


def needs_reason(link: dict | None) -> bool:
    """Gerekçe her kararda zorunlu mu: iki ucu da metin olan lafız ve ilişki bağları (tefsir – tefsir, Risale –
    tefsir; kullanıcının kararı, 2026-11-05). Kur'ân ve hadis hedefli bağlarda kanıt veridedir; göndermede kanıt
    metnin kendi sözüdür."""
    return bool(link) and link.get("type") in ("quote", "relation") and text_endpoint(link.get("target", "")) is not None


def link_key(link: Link) -> dict:
    """Bağdan kararın `link` alanı."""
    source, target, type_, part = link.key
    return {"source": source, "target": target, "type": type_, **({"part": part} if part else {})}


def reviewers(root: Path = REVIEWS_DIR) -> dict:
    """Denetçiler; her birinin sabit numarası olmalı (eksik ya da tekrarlanan numara hatadır)."""
    path = root / REVIEWERS
    people = json.loads(path.read_text(encoding="utf-8"))["reviewers"] if path.exists() else {}
    if problems := number_problems(people) + field_problems(people):
        raise ValueError(f"{path}: {'; '.join(problems)}")
    return people


def number_problems(people: dict) -> list[str]:
    """Sabit numaralar: her denetçide 1'den büyük ya da eşit bir tamsayı, ikisi aynı olmaz. Numara bir kez verilir,
    denetçi ayrılsa da başkasına verilmez (kayıt silinmediği için tekrar kendiliğinden yakalanır)."""
    out, seen = [], {}
    for rid, person in people.items():
        n = person.get("number")
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            out.append(f"denetçinin sabit numarası yok: {rid!r}")
        elif n in seen:
            out.append(f"aynı numara iki denetçide: {seen[n]!r}, {rid!r} ({n})")
        else:
            seen[n] = rid
    return out


def field_problems(people: dict) -> list[str]:
    """Alanlar: bilinen adlar, her alanda `since` tarihi (`trial`, `until` isteğe bağlı, tarih)."""
    out = []
    for rid, person in people.items():
        fields = person.get("fields") or {}
        if not isinstance(fields, dict):
            out.append(f"alanlar sözlük olmalı: {rid!r}")
            continue
        for name, d in fields.items():
            if name not in FIELDS:
                out.append(f"bilinmeyen alan {name!r}: {rid!r}")
            elif not isinstance(d, dict) or not _DATE.match(d.get("since") or ""):
                out.append(f"alanın tarihi yok ({name}): {rid!r}")
            elif any(d.get(k) and not _DATE.match(d[k]) for k in ("trial", "until")):
                out.append(f"alanın tarihi geçersiz ({name}): {rid!r}")
        if person.get("until") and not _DATE.match(person["until"]):
            out.append(f"until geçersiz: {rid!r}")
    return out


def competence(review: Review, person: dict, needs: tuple[str, ...]) -> tuple[str, ...]:
    """Kararın bağın gerektirdiği alanlardan hangilerini karşıladığı (denetçinin karar tarihindeki alanlarıyla);
    boşsa karar kaydedilir ama "denetlendi" saymaz (`competent: false`)."""
    return tuple(sorted(fields_on(person, review.date) & set(needs)))


def read(root: Path = REVIEWS_DIR) -> list[Review]:
    """Bütün kararlar, dosya ve satır sırasıyla."""
    out = []
    for path in sorted(root.glob("**/*.jsonl")):
        name = str(path.relative_to(root))
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(Review(**json.loads(line), file=name))
    return out


def append(path: Path, review: Review, root: Path = REVIEWS_DIR) -> None:
    """Yeni karar: dosyanın sonuna eklenir (hiçbir satır değişmez)."""
    if problems := review.problems(reviewers(root)):
        raise ValueError(f"geçersiz karar: {'; '.join(problems)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(review.to_json(), ensure_ascii=False) + "\n")


def current(reviews: list[Review]) -> list[Review]:
    """Geçerli kararlar: denetçi ve bağ başına son satır; geri çekilenler düşer."""
    last: dict[tuple, Review] = {}
    for r in reviews:
        target = r.key or json.dumps(r.match, sort_keys=True)
        last[(r.file, target, r.reviewer)] = r
    return [r for r in last.values() if r.status != "withdrawn"]


def validate(reviews: list[Review], people: dict) -> list[tuple[Review, str]]:
    """Kaydın kendi hataları ve sırası: geri çekme yalnız aynı denetçinin önceki kararına."""
    out, seen = [], set()
    for r in reviews:
        out += [(r, p) for p in r.problems(people)]
        target = (r.file, r.key or json.dumps(r.match, sort_keys=True), r.reviewer)
        if r.status == "withdrawn" and target not in seen:
            out.append((r, "geri çekilecek önceki karar yok"))
        seen.add(target)
    return out


def summary(reviews: list[Review], people: dict) -> list[dict]:
    """Araçların gösterdiği biçim: denetçinin sabit numarasıyla (ad yayımlanmaz), tarih sırasıyla."""
    return [{"status": r.status, **({"strength": r.strength} if r.strength else {}),
             "reviewer": people[r.reviewer]["number"], "date": r.date,
             **({"reason": r.reason} if r.reason else {})} for r in sorted(reviews, key=lambda r: r.date)]


def match_status(conn: sqlite3.Connection, match: dict) -> str | None:
    """Eski biçimli kararın (bölüm öneki ve âyet) bugünkü gücü: âyet ilişkilerinde, varsa güçlüsü."""
    sura, ayah = (int(x) for x in match["verse"].removeprefix("quran:").split(":"))
    row = conn.execute(
        "SELECT strength FROM ayah_links WHERE sura = ? AND ? BETWEEN ayah_start AND ayah_end AND node_id LIKE ?"
        " ORDER BY strength = 'weak' LIMIT 1", (sura, ayah, match["node_prefix"] + "%")).fetchone()
    return row[0] if row else None


def link_strength(conn: sqlite3.Connection, key: tuple) -> str | None:
    """Anahtarın bağı bu veritabanında varsa gücü (aynı anahtarlı birden çok bağdan güçlüsü)."""
    row = conn.execute("SELECT strength FROM links WHERE source = ? AND target = ? AND type = ? AND COALESCE(part, '') = ?"
                       " ORDER BY strength = 'weak' LIMIT 1", key).fetchone()
    return row[0] if row else None


def disagreements(conn: sqlite3.Connection, reviews: list[Review]) -> list[tuple[Review, str | None]]:
    """Geçerli `reviewed` kararlarından bugünkü bağla tutmayanlar: güçlü denilen bağ yok ya da zayıf, zayıf denilen
    bağ güçlü. Bu liste boş olmalıdır (test); dolu ise kural ya da kimlik kaymıştır."""
    out = []
    for r in current(reviews):
        if r.status != "reviewed" or not r.strength:
            continue
        now = link_strength(conn, r.key) if r.key else match_status(conn, r.match)
        if (now == "strong") != (r.strength == "strong"):
            out.append((r, now))
    return out


def add(conn: sqlite3.Connection, file: str, key: dict, status: str, reviewer: str, date: str,
        strength: str | None = None, reason: str | None = None, root: Path = REVIEWS_DIR,
        origin: dict | None = None) -> Review:
    """Kararı denetler ve ekler: bağ var mı, kayıt ve sıra geçerli mi."""
    source, target, type_ = local_id(key["source"]), key["target"], key["type"]
    row = conn.execute("SELECT relation, strength, scope FROM links WHERE source = ? AND target = ? AND type = ?"
                       " AND COALESCE(part, '') = ? ORDER BY strength = 'weak' LIMIT 1",
                       (source, target, type_, key.get("part") or "")).fetchone()
    if row is None:
        raise ValueError(f"bu anahtarla bağ yok: {source} -> {target} ({type_})")
    review = Review(status, reviewer, date, link={"source": source, "target": target, "type": type_,
                                                  **({"part": key["part"]} if key.get("part") else {})},
                    strength=strength, reason=reason, file=file, origin=origin,
                    seen={k: v for k, v in zip(("relation", "strength", "scope"), row) if v})
    if bad := validate(read(root) + [review], reviewers(root)):
        raise ValueError("; ".join(problem for _, problem in bad))
    append(root / file, review, root)
    return review


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "add":
        import argparse
        from datetime import date
        parser = argparse.ArgumentParser(prog="link_reviews add")
        parser.add_argument("file")
        for name in ("--source", "--target", "--type", "--status", "--reviewer"):
            parser.add_argument(name, required=True)
        for name in ("--part", "--strength", "--reason", "--db"):
            parser.add_argument(name)
        parser.add_argument("--date", default=date.today().isoformat())
        a = parser.parse_args(args[1:])
        conn = sqlite3.connect(Path(a.db) if a.db else DB_PATH)
        try:
            review = add(conn, a.file, {"source": a.source, "target": a.target, "type": a.type, "part": a.part},
                         a.status, a.reviewer, a.date, a.strength, a.reason)
        except ValueError as error:
            sys.exit(f"eklenmedi: {error}")
        print(f"eklendi ({a.file}): {json.dumps(review.to_json(), ensure_ascii=False)}")
        return
    if not args or args[0] not in ("check", "list"):
        sys.exit("kullanım: python -m risale_mcp.link_reviews check|list|add [--db yol]")
    people, reviews = reviewers(), read()
    if args[0] == "list":
        for rid, person in people.items():
            fields = ", ".join(f"{f} {d['since']}" for f, d in (person.get("fields") or {}).items()) or "alan yok"
            print(f"{rid} [{person.get('number')}]: {person.get('name')} ({person.get('role', '')}; {fields})")
        for (name, status), n in sorted(Counter((r.file, r.status) for r in reviews).items()):
            print(f"  {name}: {status} {n}")
        return
    bad = validate(reviews, people)
    for r, problem in bad:
        print(f"geçersiz ({r.file}): {problem}: {r.to_json()}")
    conn = sqlite3.connect(Path(args[args.index("--db") + 1]) if "--db" in args else DB_PATH)
    live = current(reviews)
    unmatched = [r for r in live if r.key and link_strength(conn, r.key) is None]
    wrong = disagreements(conn, reviews)
    print(f"karar {len(reviews)}, geçerli {len(live)}, bağı bulunmayan {len(unmatched)}, tutmayan {len(wrong)},"
          f" eski biçimli {sum(1 for r in live if r.match)}")
    for r, now in wrong:
        print(f"  tutmuyor: {r.link or r.match} karar {r.strength}, bugün {now}")
    if bad or wrong:
        sys.exit(1)


if __name__ == "__main__":
    main()
