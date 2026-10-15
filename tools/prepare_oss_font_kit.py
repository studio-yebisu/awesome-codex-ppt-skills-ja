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
    ('notosanscjkjp', 'Noto Sans CJK JP', ['NotoSansCJKjp-Regular.otf', 'NotoSansCJKjp-Bold.otf'], '研究資料・図表・CJKを含む日本語本文'),
    ('jetbrainsmono', 'JetBrains Mono', ['JetBrainsMono[wght].ttf'], 'コード・変数・端末出力の等幅英数字。日本語説明はBIZ UDPGothicと組み合わせる')
]
FAMILIES += [
    ('notosansjp','Noto Sans JP',['NotoSansJP[wght].ttf'],'本文・図のラベル・小さい注釈を同じゴシックで揃える'),
    ('notoserifjp','Noto Serif JP',['NotoSerifJP[wght].ttf'],'研究発表や文書の見出しと長い文章に使う明朝'),
    ('ibmplexsansjp','IBM Plex Sans JP',['IBMPlexSansJP-Regular.ttf','IBMPlexSansJP-Bold.ttf'],'技術資料・UI説明・業務資料の日本語'),
    ('mplus1','M PLUS 1',['MPLUS1[wght].ttf'],'図解・表・サービス紹介の日本語を幅広い太さで組む'),
    ('kiwimaru','Kiwi Maru',['KiwiMaru-Regular.ttf','KiwiMaru-Medium.ttf'],'教材や親しみのある案内の丸みのある日本語'),
    ('zenoldmincho','Zen Old Mincho',['ZenOldMincho-Regular.ttf','ZenOldMincho-Bold.ttf'],'文化・歴史・出版の見出しに使う明朝'),
    ('kaiseitokumin','Kaisei Tokumin',['KaiseiTokumin-Regular.ttf','KaiseiTokumin-Bold.ttf'],'文化施設や編集資料の題名に使う明朝'),
    ('kleeone','Klee One',['KleeOne-Regular.ttf','KleeOne-SemiBold.ttf'],'手書きに近い説明・学習ノート。表の小文字には使わない'),
    ('yuseimagic','Yusei Magic',['YuseiMagic-Regular.ttf'],'短い見出し・イベント案内。長文本文には別の書体を使う'),
    ('zenkurenaido','Zen Kurenaido',['ZenKurenaido-Regular.ttf'],'教材や展示案内の短い手書き調見出し'),
    ('inter','Inter',['Inter[opsz,wght].ttf'],'UIの英数字・図表のラベル・数値'),
    ('sourcesans3','Source Sans 3',['SourceSans3[wght].ttf'],'欧文の本文・注釈・複数行の説明'),
    ('sourceserif4','Source Serif 4',['SourceSerif4[opsz,wght].ttf'],'欧文の研究資料・本文・引用'),
    ('ibmplexsans','IBM Plex Sans',['IBMPlexSans[wdth,wght].ttf'],'日本語IBM Plexと組み合わせる技術資料の英数字'),
    ('ibmplexserif','IBM Plex Serif',['IBMPlexSerif-Regular.ttf','IBMPlexSerif-Bold.ttf'],'欧文の見出し・引用・長文'),
    ('ibmplexmono','IBM Plex Mono',['IBMPlexMono-Regular.ttf','IBMPlexMono-Bold.ttf'],'コード・端末出力・桁を揃える英数字。和文は別書体'),
    ('firacode','Fira Code',['FiraCode[wght].ttf'],'コード・変数・端末出力。合字の有無を指定し、和文は別書体'),
    ('barlowcondensed','Barlow Condensed',['BarlowCondensed-Regular.ttf','BarlowCondensed-Bold.ttf'],'横幅の狭い英字見出しと大きな数値。和文には使わない'),
    ('nunito','Nunito',['Nunito[wght].ttf'],'丸ゴシックと組み合わせる英字・数値'),
    ('librebaskerville','Libre Baskerville',['LibreBaskerville[wght].ttf'],'明朝と組み合わせる欧文の題名・短い引用')
]
JAPANESE_IDS={'zenkakugothicnew','shipporimincho','zenmarugothic','delagothicone','bizudpgothic','bizudpmincho','notosanscjkjp','notosansjp','notoserifjp','ibmplexsansjp','mplus1','kiwimaru','zenoldmincho','kaiseitokumin','kleeone','yuseimagic','zenkurenaido'}
SERIF_IDS={'shipporimincho','bizudpmincho','notoserifjp','zenoldmincho','kaiseitokumin','sourceserif4','ibmplexserif','librebaskerville'}
MONO_IDS={'jetbrainsmono','ibmplexmono','firacode'}
DISPLAY_IDS={'delagothicone','kleeone','yuseimagic','zenkurenaido'}
ROUNDED_IDS={'zenmarugothic','kiwimaru','nunito'}
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
        return decorate({**old, 'use_ja': use})
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
    return decorate({'id':folder, 'family':family, 'license':'OFL-1.1', 'commit':source['commit'], 'source_repository':source['repository'], 'license_url':license_url, 'license_file':(target/'OFL.txt').relative_to(ROOT).as_posix(), 'download':archive.relative_to(ROOT).as_posix(), 'use_ja':use, 'files':entries})

def decorate(family):
    fid=family['id']
    family['language']='ja' if fid in JAPANESE_IDS else 'latin'
    family['category']='mono' if fid in MONO_IDS else 'serif' if fid in SERIF_IDS else 'display' if fid in DISPLAY_IDS else 'rounded' if fid in ROUNDED_IDS else 'sans'
    family['official_url']=('https://github.com/notofonts/noto-cjk/tree/'+family['commit'] if fid=='notosanscjkjp' else 'https://fonts.google.com/specimen/'+quote(family['family']).replace('%20','+'))
    return family

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
        {'id':'research','title':'研究と図表','heading':'Noto Sans CJK JP','body':'Noto Sans CJK JP','latin':'Manrope','instruction':'Noto Sans CJK JPの太字で主張、標準ウェイトで図のラベルと説明を組む。白地と墨紺を基調に、青は比較する系列だけに使う。図・式・出典を近くに置き、単位と仮定を明記する。Noto Sans JPとNoto Sans CJK JPはフォント名が異なるため、原稿とPPTXに指定した名前を揃える。'},
        {'id':'technical','title':'コードと技術発表','heading':'BIZ UDPMincho','body':'BIZ UDPGothic','latin':'Manrope','code':'JetBrains Mono','instruction':'明朝の短い主張、ゴシックの日本語説明、JetBrains Monoのコードと変数を使い分ける。白地と青を基調に、コード・図・実行結果を順に見せる。コードは重要な数行に絞り、字幅を揃える。合字で演算子を省略せず、読み上げる記号を見せる。JetBrains Monoには日本語を任せず、コード内の日本語コメントにはBIZ UDPGothicをフォールバックする。学習用データと実測値を区別し、実行していないコードを結果として扱わない。'}
    ]
    presets += [
        {'id':'office-sans','title':'業務・UI説明','heading':'IBM Plex Sans JP','body':'IBM Plex Sans JP','latin':'Inter','instruction':'太字で結論、標準の太さで説明を組む。UI名・操作・結果を近くに置く。数値の桁と単位を揃える。'},
        {'id':'academic-serif','title':'学術・長い説明','heading':'Noto Serif JP','body':'Noto Sans JP','latin':'Source Serif 4','instruction':'明朝の見出しとゴシックの図ラベルを使い分ける。引用・変数・単位を原典と揃える。欧文書体は日本語へ流用しない。'},
        {'id':'rounded-lesson','title':'子ども向け教材','heading':'Kiwi Maru','body':'M PLUS 1','latin':'Nunito','instruction':'丸みのあるKiwi Maruを短い見出しに使い、説明はM PLUS 1にする。問題文・図・答えを分け、同じ文字を同じ役割で使う。'},
        {'id':'handwritten-note','title':'手書き調の説明','heading':'Klee One','body':'BIZ UDPGothic','latin':'Source Sans 3','instruction':'手書き調は短い題名と書き込みだけに使う。長い本文や表はBIZ UDPGothicで組む。小さい文字へ装飾書体を使わない。'},
        {'id':'culture-serif','title':'文化・出版','heading':'Zen Old Mincho','body':'Noto Sans JP','latin':'Libre Baskerville','instruction':'和文題名は明朝、本文と図の説明はゴシックで組む。欧文の引用はLibre Baskerville。見出しを改行するときは意味の区切りに合わせる。'},
        {'id':'plex-code','title':'コード・端末出力','heading':'IBM Plex Sans JP','body':'IBM Plex Sans JP','latin':'IBM Plex Sans','code':'Fira Code','instruction':'コードと変数はFira Code、日本語説明はIBM Plex Sans JP。演算子を説明するときはコードの合字を無効にする。日本語コメントに和文フォールバックを指定する。'},
        {'id':'compact-data','title':'数値・比較表','heading':'Noto Sans JP','body':'BIZ UDPGothic','latin':'Barlow Condensed','instruction':'大きな数値はBarlow Condensed、和文ラベルと表の本文はBIZ UDPGothic。幅の狭い書体を理由に情報を詰め込まない。桁と単位を揃える。'}
    ]
    bundle_specs=[('japanese-sans','日本語ゴシック・丸ゴシック',[f['id'] for f in families if f['language']=='ja' and f['category'] in {'sans','rounded'}]),('japanese-serif','日本語明朝',[f['id'] for f in families if f['language']=='ja' and f['category']=='serif']),('japanese-display','日本語の見出し・手書き調',[f['id'] for f in families if f['language']=='ja' and f['category']=='display']),('latin-code','欧文・数字・コード',[f['id'] for f in families if f['language']=='latin'])]
    bundles=[]
    for bid,title,ids in bundle_specs:
        archive=ROOT/'downloads/fonts'/('yebisu-'+bid+'.zip')
        with ZipFile(archive,'w',ZIP_DEFLATED) as z:
            for f in families:
                if f['id'] in ids:
                    for item in f['files']:z.write(ROOT/item['file'],f['id']+'/'+Path(item['file']).name)
                    z.write(ROOT/f['license_file'],f['id']+'/OFL.txt')
        if archive.stat().st_size>=95*1024*1024: raise ValueError('Font bundle is too large; split it: '+bid)
        bundles.append({'id':bid,'title':title,'families':ids,'download':archive.relative_to(ROOT).as_posix(),'bytes':archive.stat().st_size})
    MANIFEST.write_text(json.dumps({'updated_on':'2026-10-15','families':families,'presets':presets,'bundles':bundles,'legacy_bundle':{'download':'downloads/yebisu-oss-font-kit.zip','family_count':10}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    guide='''# AIへ渡す日本語スライドの書体指示\n\n30ファミリーを用途別の4セットと個別ZIPで配布しています。従来の `yebisu-oss-font-kit.zip` は初期10ファミリーの互換セットです。\n\n見出し・本文・英数字・コードの役割を分けます。日本語は意味の区切りで改行し、装飾書体は短い見出しに使います。Google FontsとNoto CJK公式リポジトリの固定commitから取得した未改変TTF/OTFに、OFL原文を同梱しています。\n\n'''
    guide+='## 用途別セット\n\n'+''.join('- ['+b['title']+'（'+str(len(b['families']))+'ファミリー）]('+Path(b['download']).name+')\n' for b in bundles)+'\n'
    for p in presets:
        code=' / コード: '+p['code'] if p.get('code') else ''
        guide+='## '+p['title']+'\n\n見出し: '+p['heading']+' / 本文: '+p['body']+' / 英数字: '+p['latin']+code+'\n\n'+p['instruction']+'\n\n'
    guide+='PowerPointでは使う書体を作成者と受け手の両方へ導入。Webでは配布元フォントを同梱し、font-faceで読ませる。未改変TTF/OTFとOFLを同じフォルダーに保持する。Noto Sans CJK JPは研究発表の取り込み3作例にも指定されている書体。環境だけにあった書体をコピーせず、公式配布のRegular/Boldを取得できる。\n'
    (ROOT/'downloads/fonts/AI-FONT-GUIDE.md').write_text(guide,encoding='utf-8')
    css=[]
    for f in families:
        for entry in f['files']:
            font=TTFont(ROOT/entry['file'])
            weight=next((str(int(a.minValue))+' '+str(int(a.maxValue)) for a in font['fvar'].axes if a.axisTag=='wght'),'400') if 'fvar' in font else str(font['OS/2'].usWeightClass)
            fmt='opentype' if entry['file'].endswith('.otf') else 'truetype'
            css.append('@font-face{font-family:'+json.dumps('Atelier '+f['family'])+';src:url('+json.dumps('../'+quote(entry['file'],safe='/'))+') format('+json.dumps(fmt)+');font-weight:'+weight+';font-display:swap}')
    (ROOT/'assets/font-atelier-files.css').write_text('\n'.join(css)+'\n','utf-8')
    # Preserve the earlier ten-family download for existing incoming links.
    with ZipFile(ROOT/'downloads/yebisu-oss-font-kit.zip','w',ZIP_DEFLATED) as z:
        for f in families[:10]:
            for item in f['files']:z.write(ROOT/item['file'],'fonts/'+f['id']+'/'+Path(item['file']).name)
            z.write(ROOT/f['license_file'],'fonts/'+f['id']+'/OFL.txt')
        z.write(ROOT/'downloads/fonts/AI-FONT-GUIDE.md','fonts/AI-FONT-GUIDE.md')
    print('OSS font kit and AI guide packaged')
