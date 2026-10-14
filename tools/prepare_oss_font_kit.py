"""Get unmodified, pinned OFL fonts for slide production and direct downloads."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from zipfile import ZipFile, ZIP_DEFLATED
from fontTools.ttLib import TTFont
import json

ROOT = Path(__file__).resolve().parents[1]
COMMIT = '66928797f271fed5ee428544e7229685e2d90127'
FAMILIES = [
    ('zenkakugothicnew', 'Zen Kaku Gothic New', ['ZenKakuGothicNew-Regular.ttf', 'ZenKakuGothicNew-Bold.ttf', 'ZenKakuGothicNew-Black.ttf'], '端正な本文と強い和文見出し'),
    ('shipporimincho', 'Shippori Mincho', ['ShipporiMincho-Regular.ttf', 'ShipporiMincho-Bold.ttf'], 'ブランド提案や誌面の明朝'),
    ('zenmarugothic', 'Zen Maru Gothic', ['ZenMaruGothic-Regular.ttf', 'ZenMaruGothic-Bold.ttf'], '親しみのある教材・サービス紹介'),
    ('delagothicone', 'Dela Gothic One', ['DelaGothicOne-Regular.ttf'], '短い表紙・ポスターの強い見出し'),
    ('manrope', 'Manrope', ['Manrope[wght].ttf'], '英数字と大きな数字'),
    ('spacegrotesk', 'Space Grotesk', ['SpaceGrotesk[wght].ttf'], 'モーション資料の英数字'),
    ('bizudpgothic', 'BIZ UDPGothic', ['BIZUDPGothic-Regular.ttf', 'BIZUDPGothic-Bold.ttf'], '業務資料・表・教材の日本語本文'),
    ('bizudpmincho', 'BIZ UDPMincho', ['BIZUDPMincho-Regular.ttf', 'BIZUDPMincho-Bold.ttf'], '説明資料の明朝見出しと和文本文'),
    ('notosanscjkjp', 'Noto Sans CJK JP', ['NotoSansCJKjp-Regular.otf', 'NotoSansCJKjp-Bold.otf'], '研究資料・図表・CJKを含む日本語本文')
]
SOURCE_OVERRIDES = {
    'notosanscjkjp': {'repository': 'notofonts/noto-cjk', 'commit': 'f8d157532fbfaeda587e826d4cd5b21a49186f7c',
                      'font_dir': 'Sans/OTF/Japanese', 'license_path': 'Sans/LICENSE'},
}
MANIFEST = ROOT/'data/oss-font-kit.json'
EXISTING = {f['id']: f for f in json.loads(MANIFEST.read_text(encoding='utf-8'))['families']} if MANIFEST.exists() else {}

def fetch(path, repository='google/fonts', commit=COMMIT):
    url = f'https://raw.githubusercontent.com/{repository}/{commit}/{path}'
    with urlopen(Request(url, headers={'User-Agent':'Yebisu-Slides-OSS-Fonts'}), timeout=60) as response:
        return response.read(), url

def build_family(spec):
    folder, family, files, use = spec
    source = SOURCE_OVERRIDES.get(folder, {'repository': 'google/fonts', 'commit': COMMIT,
        'font_dir': 'ofl/'+folder, 'license_path': 'ofl/'+folder+'/OFL.txt'})
    target = ROOT / 'downloads/fonts' / folder
    old = EXISTING.get(folder)
    if (old and old.get('commit') == source['commit']
            and [Path(f['file']).name for f in old['files']] == files
            and (ROOT/old['license_file']).is_file()
            and (ROOT/old['download']).is_file()
            and all((ROOT/f['file']).is_file() and sha256((ROOT/f['file']).read_bytes()).hexdigest() == f['sha256'] for f in old['files'])):
        print(f'{family}: existing pinned font files retained', flush=True)
        return {**old, 'use_ja': use}
    target.mkdir(parents=True, exist_ok=True)
    license_bytes, license_url = fetch(source['license_path'], source['repository'], source['commit'])
    if b'SIL OPEN FONT LICENSE' not in license_bytes:
        raise ValueError('OFL missing: '+family)
    (target/'OFL.txt').write_bytes(license_bytes)
    entries=[]
    for name in files:
        local=target/name
        data, url=fetch(source['font_dir']+'/'+quote(name), source['repository'], source['commit'])
        local.write_bytes(data)
        font=TTFont(local)
        if not font.getBestCmap(): raise ValueError('Invalid font: '+name)
        entries.append({'file':local.relative_to(ROOT).as_posix(), 'source_url':url, 'sha256':sha256(data).hexdigest(), 'bytes':len(data), 'modified':False})
    archive=ROOT/'downloads/fonts'/(folder+'.zip')
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for file in target.iterdir():z.write(file,folder+'/'+file.name)
    print(f'{family}: {len(entries)} original fonts ready', flush=True)
    return {'id':folder, 'family':family, 'license':'OFL-1.1', 'commit':source['commit'], 'source_repository':source['repository'], 'license_url':license_url, 'license_file':(target/'OFL.txt').relative_to(ROOT).as_posix(), 'download':archive.relative_to(ROOT).as_posix(), 'use_ja':use, 'files':entries}

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=6) as pool:
        families=list(pool.map(build_family,FAMILIES))
    presets=[
        {'id':'editorial','title':'誌面とブランド','heading':'Shippori Mincho','body':'Zen Kaku Gothic New','latin':'Manrope','instruction':'アイボリーと墨黒を基調に、赤橙を一点。明朝の大見出しと短い本文、大きな余白、縦横のグリッドで誌面を作る。'},
        {'id':'motion','title':'夜とモーション','heading':'Zen Kaku Gothic New','body':'Zen Kaku Gothic New','latin':'Space Grotesk','instruction':'墨紺に蛍光ライム。短い見出しを大きく置き、SVG図形と段階表示で視線を導く。動きは220〜450ms、ページごとに一つの主張。'},
        {'id':'friendly','title':'やさしい教材','heading':'Zen Maru Gothic','body':'Zen Kaku Gothic New','latin':'Manrope','instruction':'丸ゴシックは見出しに、端正なゴシックは本文に。図解と余白を優先し、読み手が次にすることを一つずつ伝える。'},
        {'id':'poster','title':'強い表紙','heading':'Dela Gothic One','body':'Zen Kaku Gothic New','latin':'Space Grotesk','instruction':'Delaは短い見出しのみ。大胆な一色と大きな文字・図形で表紙を作る。本文に太い装飾書体を使わず、ページで構図を変える。'},
        {'id':'work','title':'業務と数字','heading':'BIZ UDPGothic','body':'BIZ UDPGothic','latin':'Manrope','instruction':'BIZ UDPGothicの太字で結論、標準ウェイトで説明を組む。数字の単位と比較対象を明記し、表は罫線を減らして列を揃える。白地と墨紺に赤橙を一点。見出しを大きく、本文は短い段落にする。'},
        {'id':'explain','title':'説明と教材','heading':'BIZ UDPMincho','body':'BIZ UDPGothic','latin':'Manrope','instruction':'BIZ UDPMinchoの太字で題名、BIZ UDPGothicで説明と図のラベルを組む。紙色と深緑を基調に、赤橙は注目する量だけに使う。式・図・説明を対応させ、学習用の設定と実測値を区別する。'},
        {'id':'research','title':'研究と図表','heading':'Noto Sans CJK JP','body':'Noto Sans CJK JP','latin':'Manrope','instruction':'Noto Sans CJK JPの太字で主張、標準ウェイトで図のラベルと説明を組む。白地と墨紺を基調に、青は比較する系列だけに使う。図・式・出典を近くに置き、単位と仮定を明記する。Noto Sans JPとNoto Sans CJK JPはフォント名が異なるため、原稿とPPTXに指定した名前を揃える。'}
    ]
    MANIFEST.write_text(json.dumps({'families':families,'presets':presets},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    guide='''# AIへ渡す日本語スライドの書体指示\n\n見出し・本文・英数字の役割を分け、同じ書体を漫然と並べない。日本語は意味の区切りで改行し、強い表紙と余白を作る。装飾書体は短い見出しに限る。Google FontsとNoto CJK公式リポジトリの固定commitから取得した未改変原配布物に、OFL原文を同梱。フォント単体販売をしない。\n\n'''
    for p in presets:
        guide+='## '+p['title']+'\n\n見出し: '+p['heading']+' / 本文: '+p['body']+' / 英数字: '+p['latin']+'\n\n'+p['instruction']+'\n\n'
    guide+='PowerPointでは使う書体を作成者と受け手の両方へ導入。Webでは配布元フォントを同梱し、font-faceで読ませる。未改変TTF/OTFとOFLを同じフォルダーに保持する。Noto Sans CJK JPは研究発表の取り込み3作例にも指定されている書体。環境だけにあった書体をコピーせず、公式配布のRegular/Boldを取得できる。\n'
    (ROOT/'downloads/fonts/AI-FONT-GUIDE.md').write_text(guide,encoding='utf-8')
    with ZipFile(ROOT/'downloads/yebisu-oss-font-kit.zip','w',ZIP_DEFLATED) as z:
        for f in (ROOT/'downloads/fonts').rglob('*'):
            if f.is_file() and f.suffix!='.zip':z.write(f,f.relative_to(ROOT/'downloads').as_posix())
    print('OSS font kit and AI guide packaged')
