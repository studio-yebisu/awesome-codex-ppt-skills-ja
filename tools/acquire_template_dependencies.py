"""Pin Guizang's existing browser dependencies and preserve their licenses."""
from pathlib import Path
import json, hashlib, urllib.request
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'sources/browser-dependencies';OUT.mkdir(parents=True,exist_ok=True)
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Studio-Yebisu-slide-catalog'}),timeout=60) as r:return r.read()
records=[]
for name,version,js_path in [('motion','11.11.17',None),('lucide','0.468.0','dist/umd/lucide.min.js')]:
    package=json.loads(get(f'https://cdn.jsdelivr.net/npm/{name}@{version}/package.json'))
    license_path='LICENSE.md' if name=='motion' else 'LICENSE'
    terms=get(f'https://cdn.jsdelivr.net/npm/{name}@{version}/{license_path}')
    if b'permission' not in terms.lower():raise RuntimeError('Unexpected license for '+name)
    (OUT/(name+'-LICENSE.txt')).write_bytes(terms)
    record=dict(package=name,version=version,license=package['license'],license_url=f'https://cdn.jsdelivr.net/npm/{name}@{version}/{license_path}',license_sha256=hashlib.sha256(terms).hexdigest())
    if js_path:
        js=get(f'https://cdn.jsdelivr.net/npm/{name}@{version}/{js_path}');(OUT/(name+'.min.js')).write_bytes(js);record['sha256']=hashlib.sha256(js).hexdigest()
    records.append(record);print(name,version,package['license'])
(ROOT/'data/browser-dependencies.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
