"""E7 (a) ön çalışma: Kütüb-i Sitte ve Muvatta'da aynı hadisin rivayetleri, lafızla (deneme; bağ yazılmaz)."""
import sqlite3, sys, json, collections, random, time
sys.path.insert(0, '/home/fatih/Belgeler/Coding/Projects/risale-mcp/src')
from risale_mcp.normalize import search_words
t0 = time.time()
c = sqlite3.connect('/home/fatih/Belgeler/Coding/Projects/risale-mcp/data/dist/hadis/hadis.db')
rows = c.execute("SELECT id, book, matn FROM lib_units WHERE matn IS NOT NULL AND matn != ''").fetchall()
K = 5
units, sh = [], []
for uid, book, matn in rows:
    w = search_words(matn)
    s = {tuple(w[i:i + K]) for i in range(len(w) - K + 1)}
    if len(s) >= 2:                      # 6 kelimeden kısa metin gruplanmaz
        units.append((uid, book, len(w), matn)); sh.append(s)
df = collections.Counter(x for s in sh for x in s)
MAXDF = 40                               # çok yaygın diziler (kalıplar) aday üretmez
inv = collections.defaultdict(list)
for i, s in enumerate(sh):
    for x in s:
        if df[x] <= MAXDF:
            inv[x].append(i)
pairs = collections.Counter()
for lst in inv.values():
    for a in range(len(lst)):
        for b in range(a + 1, len(lst)):
            pairs[(lst[a], lst[b])] += 1
res = []
for (a, b), n in pairs.items():
    if n < 2:
        continue
    inter = len(sh[a] & sh[b])
    cont = inter / min(len(sh[a]), len(sh[b]))
    jac = inter / len(sh[a] | sh[b])
    res.append((a, b, cont, jac))
print(f"birim {len(units)}, aday çift {len(res)}, {time.time()-t0:.0f} sn", file=sys.stderr)

def groups(th, key=2):
    parent = list(range(len(units)))
    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b, cont, jac in res:
        if (cont if key == 2 else jac) >= th:
            parent[f(a)] = f(b)
    g = collections.defaultdict(list)
    for i in range(len(units)):
        g[f(i)].append(i)
    return [v for v in g.values() if len(v) > 1]

out = {"units": len(units), "books": dict(collections.Counter(u[1] for u in units)), "thresholds": {}}
random.seed(3)
for th in (0.9, 0.8, 0.6, 0.4):
    G = groups(th)
    sizes = sorted((len(x) for x in G), reverse=True)
    cross = sum(1 for x in G if len({units[i][1] for i in x}) > 1)
    grouped = sum(sizes)
    out["thresholds"][th] = {"groups": len(G), "grouped_units": grouped, "share": round(grouped / len(units), 3),
                             "cross_book_groups": cross, "largest": sizes[:8],
                             "size_hist": dict(collections.Counter(min(s, 10) for s in sizes))}
# sınırdaki çiftler (0.4–0.6 ve 0.6–0.8) ve en büyük grup örneği
def sample(lo, hi, n=6):
    cand = [r for r in res if lo <= r[2] < hi]
    return [{"a": units[a][0], "b": units[b][0], "cont": round(cn, 2), "jac": round(j, 2),
             "a_text": units[a][3][:160], "b_text": units[b][3][:160]} for a, b, cn, j in random.sample(cand, min(n, len(cand)))]
out["samples"] = {"0.4-0.6": sample(0.4, 0.6), "0.6-0.8": sample(0.6, 0.8), "0.8-1": sample(0.8, 1.01, 4)}
G = groups(0.6); big = max(G, key=len)
out["largest_0.6"] = [{"id": units[i][0], "text": units[i][3][:120]} for i in big[:12]]
json.dump(out, open('/home/fatih/Belgeler/Coding/Projects/risale-mcp/data/interim/hadis/e7-gruplar-deneme.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out["thresholds"], ensure_ascii=False, indent=1))
