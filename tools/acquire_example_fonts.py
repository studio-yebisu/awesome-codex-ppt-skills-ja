"""Download original preset typefaces from pinned Google Fonts, with OFL texts."""
from pathlib import Path
import json, hashlib, urllib.request
ROOT=Path(__file__).resolve().parents[1]
COMMIT='66928797f271fed5ee428544e7229685e2d90127'
FAMILIES={'archivoblack':'Archivo Black','spacegrotesk':'Space Grotesk','playfairdisplay':'Playfair Display','sourceserif4':'Source Serif 4','ibmplexmono':'IBM Plex Mono','jetbrainsmono':'JetBrains Mono','inter':'Inter'}
OUT=ROOT/'assets/fonts/presets';OUT.mkdir(parents=True,exist_ok=True)
records=[]
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Studio-Yebisu-slide-catalog'}),timeout=60) as r:return r.read()
for folder,name in FAMILIES.items():
    listing=json.loads(get(f'https://api.github.com/repos/google/fonts/contents/ofl/{folder}?ref={COMMIT}'))
    fonts=[f for f in listing if f['name'].endswith('.ttf') and 'Italic' not in f['name'] and ('Regular' in f['name'] or '[' in f['name'])]
    if not fonts:raise RuntimeError(f'No font for {folder}')
    chosen=sorted(fonts,key=lambda f:('[' not in f['name'],f['name']))[0]
    font_url=chosen['download_url'];license_url=next(f['download_url'] for f in listing if f['name']=='OFL.txt')
    blob=get(font_url);license_blob=get(license_url)
    if b'SIL OPEN FONT LICENSE' not in license_blob:raise RuntimeError('Unexpected license')
    file=OUT/(folder+'.ttf');file.write_bytes(blob);(OUT/(folder+'-OFL.txt')).write_bytes(license_blob)
    records.append(dict(family=name,file=file.relative_to(ROOT).as_posix(),commit=COMMIT,source_url=font_url,license_url=license_url,license='OFL-1.1',sha256=hashlib.sha256(blob).hexdigest(),modified=False))
    print(name,len(blob),'OFL-1.1')
(ROOT/'data/preset-fonts.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
