"""Download complete pinned skill sources for genuine workflow execution, not a replacement renderer."""
from pathlib import Path
from hashlib import sha256
from urllib.request import Request,urlopen
import json,zipfile,io
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))
for repo in ['hugohe3/ppt-master','zarazhangrui/frontend-slides','op7418/guizang-ppt-skill']:
    source=next(s for s in records if s['repository']==repo)
    dest=ROOT/'.build/actual-upstreams'/repo.replace('/','__')
    if (dest/'ACQUISITION.json').exists():print(f'Pinned checkout already available: {repo}',flush=True);continue
    url=f'https://codeload.github.com/{repo}/zip/{source["commit"]}'
    with urlopen(Request(url,headers={'User-Agent':'StudioYebisu-skill-catalog'}),timeout=90) as response:content=response.read()
    dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        prefix=z.namelist()[0].split('/')[0]+'/'
        for member in z.infolist():
            if member.is_dir():continue
            name=member.filename.removeprefix(prefix)
            target=(dest/name).resolve()
            if not target.is_relative_to(dest.resolve()):raise ValueError('Invalid archive path')
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(member))
    record={'repository':repo,'commit':source['commit'],'archive_url':url,'archive_sha256':sha256(content).hexdigest(),'bytes':len(content),'root':str(dest)}
    (dest/'ACQUISITION.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'{repo}: full source {len(content):,} bytes / {source["commit"][:12]}',flush=True)
