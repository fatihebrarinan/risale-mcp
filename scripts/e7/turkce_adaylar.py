import json, sys, collections
sys.path.insert(0, '/home/fatih/Belgeler/Coding/Projects/risale-mcp/src')
from pathlib import Path
from risale_mcp.env import load_env; load_env()
from risale_mcp.hadis_library import HadisLibrary
L = HadisLibrary(Path('/home/fatih/Belgeler/Coding/Projects/risale-mcp/data/dist/hadis/hadis.db'))
d = json.load(open('/home/fatih/Belgeler/Coding/Projects/risale-mcp/data/interim/hadis/turkce.json'))['sentences']
out = []
for x in d:
    q = x.get('quote') or x['text']
    r = L.semantic(q, limit=3)['results']
    out.append({"id": x['id'], "form": x['form'], "quote": q,
                "top": [{"id": h['id'], "sim": h['similarity'], "text": (h.get('matn') or h.get('text') or '')[:140]} for h in r]})
json.dump(out, open('/home/fatih/Belgeler/Coding/Projects/risale-mcp/data/interim/hadis/e7-turkce-adaylar.json', 'w'), ensure_ascii=False, indent=1)
sims = [o['top'][0]['sim'] for o in out if o['top']]
import statistics
print('n', len(out), 'top1 sim median', statistics.median(sims), 'max', max(sims), 'min', min(sims))
print(collections.Counter(round(s, 1) for s in sims))
for o in sorted(out, key=lambda o: -o['top'][0]['sim'])[:5] + sorted(out, key=lambda o: o['top'][0]['sim'])[:3]:
    t = o['top'][0]; print(f"{t['sim']:.2f} {o['quote'][:70]}\n      -> {t['id']}: {t['text'][:110]}")
