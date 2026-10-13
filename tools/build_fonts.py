"""Download official OFL fonts and create renamed, content-specific Web font subsets."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote
from hashlib import sha256
from fontTools.ttLib import TTFont
from fontTools import subset
import json, subprocess
ROOT=Path(__file__).resolve().parents[1]
FONTS=[('notosansjp','NotoSansJP[wght].ttf','noto-sans-jp','Yebisu Noto Sans JP'),
       ('notoserifjp','NotoSerifJP[wght].ttf','noto-serif-jp','Yebisu Noto Serif JP'),
       ('bizudpgothic','BIZUDPGothic-Regular.ttf','biz-udpgothic-regular','Yebisu BIZ UDPGothic'),
       ('bizudpgothic','BIZUDPGothic-Bold.ttf','biz-udpgothic-bold','Yebisu BIZ UDPGothic')]
def get(url):
    with urlopen(Request(url,headers={'User-Agent':'StudioYebisu-font-build'}),timeout=60) as r:return r.read()
if __name__=='__main__':
    cache=ROOT/'.build/fonts';cache.mkdir(parents=True,exist_ok=True)
    marker=cache/'commit.txt'
    if marker.exists():commit=marker.read_text().strip()
    else:
        commit=subprocess.check_output(['gh','api','repos/google/fonts/commits/main','--jq','.sha'],text=True).strip();marker.write_text(commit)
    content=''.join(chr(i) for i in range(32,127))+'←→↑↓↗↺Ⅱ×≠①②③▶–—·…'
    for folder in ['data','assets','skills']:
        if not (ROOT/folder).exists():continue
        for file in (ROOT/folder).rglob('*'):
            if file.suffix in ['.json','.mjs','.js','.md']:content+=file.read_text(encoding='utf-8')
    for file in ROOT.glob('*.html'):content+=file.read_text(encoding='utf-8')
    records=[]
    for family,filename,stem,renamed in FONTS:
        url=f'https://raw.githubusercontent.com/google/fonts/{commit}/ofl/{family}/{quote(filename)}'
        source=cache/filename
        if not source.exists():source.write_bytes(get(url))
        license_url=f'https://raw.githubusercontent.com/google/fonts/{commit}/ofl/{family}/OFL.txt'
        license_path=ROOT/'assets/fonts'/f'{family}-OFL.txt';license_path.parent.mkdir(parents=True,exist_ok=True)
        if not license_path.exists():license_path.write_bytes(get(license_url))
        if 'SIL OPEN FONT LICENSE' not in license_path.read_text(encoding='utf-8'):raise ValueError('OFLを確認できません')
        font=TTFont(source);cmap=font.getBestCmap();missing=set(ord(c) for c in content)-set(cmap)
        options=subset.Options();options.flavor='woff2';options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
        sub=subset.Subsetter(options=options);sub.populate(text=content);sub.subset(font)
        for n in font['name'].names:
            if n.nameID in [1,4,6,16,21,25]:
                value=renamed.replace(' ','') if n.nameID in [6,25] else renamed
                n.string=value.encode(n.getEncoding(),errors='replace')
        target=ROOT/'assets/fonts'/f'{stem}.woff2';font.flavor='woff2';font.save(target)
        records.append(dict(family=family,file=str(target.relative_to(ROOT)).replace('\\','/'),license='OFL-1.1',
            source_url=url,license_url=license_url,commit=commit,source_sha256=sha256(source.read_bytes()).hexdigest(),
            subset_sha256=sha256(target.read_bytes()).hexdigest(),renamed_family=renamed,
            modification='収録本文の文字にサブセット化し、内部のファミリー名を変更。OFL原文・著作権表示を保持。',
            glyphs=len(font.getBestCmap()),source_bytes=source.stat().st_size,subset_bytes=target.stat().st_size))
        print(f'{stem}: {target.stat().st_size:,} bytes / {len(font.getBestCmap())} glyphs',flush=True)
    (ROOT/'data/fonts.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
