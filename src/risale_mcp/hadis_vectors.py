"""Hadis sunucusunun anlamsal araması için vektörler (MVP M5, kullanıcının kararı 2026-11-06).

    uv run python -m risale_mcp.hadis_vectors build [--max-tokens 30]   # data/dist/hadis/vectors/, eksikleri çıkarır
    uv run python -m risale_mcp.hadis_vectors status                    # eksik sayısı ve metin seçiminin dağılımı

Birim hadistir (atıf birimi). Vektöre yalnız metin (matn) girer: senet râvi adlarıyla dolu olduğu için anlamı ezer
("sabır" arayan aynı râvileri bulur), başkasının katmanları (Zehebî, Elbânî) hiç girmez. Metin:
    matn       baskı senedi ayırmışsa (Kütüb-i Sitte JK) metin kısmı
    quote      «…» içindeki söz (ilk açılıştan sonrası)
    after_said "قال رسول الله صلى الله عليه وسلم" (ya da "عن النبي صلى الله عليه وسلم") gibi bir ifadenin son geçişinden sonrası
    whole      ayrılamadı: bütünü (Kenz, Keşfü'l-Hafâ, Feyzü'l-Kadîr senetsiz; eş-Şifâ ve Delâil paragrafları)
Model `voyage-context-4` (sunucunun modeli, int8): bir bâbın hadisleri bir belgedir (≈8 bin tokenlık parçalar),
her hadisin vektörü bâbın bağlamını taşır. Anahtar `<hadis kimliği>|<metnin özeti>`: metin değişirse yeniden çıkar.
"""

import argparse
import hashlib
import re
import sqlite3
import sys
import time
from collections import Counter

import numpy as np

from risale_mcp.embeddings import (MODELS, SEARCH_MODEL, Unit, VectorStore, _document_batches, _tokens, embed_documents,
                                   DOCUMENT_TOKENS)
from risale_mcp.env import load_env
from risale_mcp.profiles import PROFILES

VARIANT = "hadis"
_SAID = re.compile(r"(?:قال|يقول|فقال|سمعت|عن)\s*:?\s*(?:رسول الله|النبي|نبي الله)\s*(?:صلى الله عليه وسلم|ﷺ)?\s*:?\s*(?:قال\s*:?)?")


def embedded_text(text: str, matn: str | None) -> tuple[str, str]:
    """Vektöre girecek metin ve nasıl seçildiği."""
    if matn and matn.strip():
        return matn.strip(), "matn"
    if (i := text.find("«")) >= 0 and len(text) - i > 15:
        return text[i:].strip(), "quote"
    last = None
    for last in _SAID.finditer(text):
        pass
    if last is not None and len(text) - last.end() > 15:
        return text[last.end():].strip(), "after_said"
    return text.strip(), "whole"


def _key(unit_id: str, text: str) -> str:
    return f"{unit_id}|{hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]}"


def units(conn: sqlite3.Connection) -> tuple[list[list[Unit]], Counter]:
    """Bâb başına belgeler (≈8 bin tokenı aşmayan ardışık parçalar) ve metin seçiminin dağılımı."""
    docs: list[list[Unit]] = []
    how: Counter = Counter()
    current = None
    for unit_id, node, text, matn in conn.execute("SELECT id, node_id, text, matn FROM lib_units ORDER BY seq"):
        body, method = embedded_text(text, matn)
        how[method] += 1
        unit = Unit(_key(unit_id, body), body)
        if node != current or _tokens([u.text for u in docs[-1]] + [body]) > DOCUMENT_TOKENS:
            docs.append([])
            current = node
        docs[-1].append(unit)
    return docs, how


def store() -> VectorStore:
    return VectorStore(SEARCH_MODEL, VARIANT, PROFILES["hadis"].vectors, dtype=np.int8)


def build(max_tokens: int | None = None) -> None:
    model = MODELS[SEARCH_MODEL]
    conn = sqlite3.connect(PROFILES["hadis"].db)
    docs, how = units(conn)
    vectors = store()
    vectors.path.parent.mkdir(parents=True, exist_ok=True)
    wanted = {u.key for d in docs for u in d}
    if removed := vectors.keep(wanted):
        print(f"artık {removed} vektör silindi", flush=True)
    todo_docs = [d for d in docs if any(u.key not in vectors for u in d)]
    todo = sum(len(d) for d in todo_docs)
    print(f"hadis vektörleri: {len(vectors.keys)} var, {todo} eksik; metin seçimi {dict(how)}", flush=True)
    started, spent, done = time.monotonic(), 0, 0
    for n, batch in enumerate(_document_batches(todo_docs, model), 1):
        out, tokens = embed_documents(model, [[u.text for u in d] for d in batch])
        vectors.add([u.key for d in batch for u in d], np.concatenate(out))
        spent += tokens
        done += sum(len(d) for d in batch)
        if max_tokens and spent >= max_tokens:
            vectors.save()
            print(f"sınır: {spent / 1e6:.2f} M token; {done}/{todo}, kalanı sonraki çalıştırmada", flush=True)
            return
        if n % 20 == 0:
            vectors.save()
            print(f"  {done}/{todo} · {spent / 1e6:.2f} M token · {time.monotonic() - started:.0f} sn", flush=True)
    vectors.save()
    print(f"bitti: {done} vektör, {spent / 1e6:.2f} M token, {time.monotonic() - started:.0f} sn", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("build", "status"))
    parser.add_argument("--max-tokens", type=float, help="token sınırı (milyon)")
    args = parser.parse_args()
    load_env()
    if args.command == "build":
        build(int(args.max_tokens * 1e6) if args.max_tokens else None)
        return
    docs, how = units(sqlite3.connect(PROFILES["hadis"].db))
    vectors = store()
    missing = sum(u.key not in vectors for d in docs for u in d)
    print(f"birim {sum(len(d) for d in docs)}, eksik {missing}, tahmini token (M) "
          f"{_tokens([u.text for d in docs for u in d if u.key not in vectors]) / 1e6:.1f}; metin seçimi {dict(how)}")


if __name__ == "__main__":
    sys.exit(main())
