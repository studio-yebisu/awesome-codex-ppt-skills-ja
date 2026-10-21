"""Package upstream implementations, rather than generic substitute skills."""
from pathlib import Path
import hashlib, json, shutil, zipfile
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams'
PINS=json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))
DEST=ROOT/'skill-forks';DEST.mkdir(exist_ok=True)
DOWNLOADS=ROOT/'downloads';DOWNLOADS.mkdir(exist_ok=True)

CONFIG=[
 ('op7418/guizang-ppt-skill','guizang-ppt-skill-ja','雑誌風・Swiss風の日本語HTMLスライドを、Guizangの実際のテンプレートで制作する。Guizangの作例や日本語版を指定されたときに使う。',
  ['SKILL.md','references','scripts','assets/template.html','assets/template-swiss.html','assets/motion.min.js'],
  '''# Guizang 日本語版

元の [SKILL.upstream.md](SKILL.upstream.md) を読む。選んだStyle A/Bに必要な参照だけを読み、**assets/template.html または assets/template-swiss.html を実際にコピーして内容を挿入する**。別の共通レンダラーへ置き換えない。Swissは元のS01–S22の登録版式を保持する。

日本語の内容を作り、langをjaにする。中国語用のNoto SC指定はNoto Sans JP / Noto Serif JPへ変更する。英字の指定フォント、テーマ色、レイアウト、WebGL、Motion、ページ制御は保持する。文の意味で改行し、長い日本語の見出しは字号とフレームを調整する。ローカルの日本語フォントはreferences/japanese-fonts.mdを参照する。

上流の「見出しだけ変えた別スタイル」を作らない。元のテンプレートとの差分と出力をSOURCE.jsonに基づいて記録する。スライドIDと講稿を一対一に対応させ、scripts/validate-presenter-mode.mjsを実行する。Swissではscripts/validate-swiss-deck.mjsも実行する。ブラウザーで実表示・翻ページ・字形を確認する。

このフォークとテンプレート派生物のコードはAGPL-3.0。LICENSEを保持し、改変ソースと対応する配布元を用意する。MotionはMIT、LucideはISC、書体はOFLの原文を個別に保持する。カタログのCC0をこのスキルへ適用しない。
'''),
 ('zarazhangrui/frontend-slides','frontend-slides-ja','Frontend Slidesのプリセットと固定ステージを使って、日本語のHTMLプレゼンテーションを作る。Frontend Slidesやそのスタイルを指定されたときに使う。',
  ['SKILL.md','STYLE_PRESETS.md','viewport-base.css','html-template.md','animation-patterns.md'],
  '''# Frontend Slides 日本語版

[SKILL.upstream.md](SKILL.upstream.md)と選択したSTYLE_PRESETS.mdの項目を読む。元の指定書体・色・署名的な配置を使う。html-template.mdのHTMLとSlidePresentationを制作の土台にして、viewport-base.cssを**全文**含める。1920×1080の固定ステージを等比縮小し、スマートフォンでスライド内を再配置しない。

英字の指定書体に日本語用Noto Sans JP等を足す。日本語だけが別のシステム書体へ落ちないよう実字形を確認する。自然な改行と異なる字重・字号を使い、内容を詰め込まない。図形は抽象的な形にする。キーボード、タッチ、ホイールを実装する。元の編集仕様に従いE編集・localStorage保存・HTML出力を整える。

指示型スキルなので、存在しない生成CLIを実行したとは言わない。適用したプリセット、参照ファイル、改変点をSOURCE.jsonと出力の制作記録に残す。ブラウザーで全ページ、編集、保存、大小画面を確認する。

LICENSEはZara ZhangのMIT。書体のOFLは別に保持する。共通レンダラーで生成したスライドを、このスキルで作った作例として扱わない。
'''),
 ('hugohe3/ppt-master','ppt-master-ja','PPT Masterの元のチェッカーとネイティブ変換器で、日本語の編集可能なPPTXを作る。PPT Master日本語版やSVGからの日本語PowerPoint制作を指定されたときに使う。',
  ['skills/ppt-master/SKILL.md','skills/ppt-master/references','skills/ppt-master/scripts','skills/ppt-master/workflows','skills/ppt-master/templates'],
  '''# PPT Master 日本語版の制作経路

上流の[SKILL.upstream.md](SKILL.upstream.md)を参照し、文字・図形を編集できるPPTXという目的を維持する。上流の通常ルートを使う場合は、そのルーティングと計画契約に従う。

この日本語版には、カタログの作例や文字・図形中心の小規模な資料を制作する専用経路を追加している。これは上流Default Generateの全工程の実行を意味しない。上流のQuick Generate変換契約を内部で使う。外部画像、アイコン、音源を要しない日本語スライド向けであり、素材ライブラリーは同梱していない。

- references/shared-standards-core.md、executor-base.md、semantic-svg.md、preset-shape-vocabulary.mdとworkflows/profiles/quick-generate.mdの技術契約を読む。
- 1280×720のSVGをsvg_outputへ作る。日本語のNoto Sans JP、自然な改行、役割別の字号を指定。意味グループのidとdata-pptx-bounds、rootのdata-pptx-page-roleを付ける。
- scripts/svg_quality_checker.py PROJECT --quick-generate --canonical-authoring --stage final --jsonを実行する。
- 講稿をnotesに保存し、scripts/svg_to_pptx.py PROJECT --quick-generate --primary-language ja-JP --with-notes -t fade -o OUTPUT.pptxで出力する。
- チェッカーと変換器は本体を無改変で使う。画像へ丸ごと変換する代替出力を成功と扱わない。PPTX内に日本語文字、図形、講稿があることを確認する。
- ブラウザーのプレビューは変換入力SVGであり、PowerPointアプリの表示検証と区別する。PPTXの受け手にもNoto Sans JPの導入が必要。警告が残った場合は制作記録に残す。

上流のMIT原文とHugo Heの著作権表示を保持する。素材を追加する場合は、その素材ごとの利用条件も確認する。
''')
]

def copy(source,dest):
    if source.is_dir():shutil.copytree(source,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    else:dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
def zip_folder(folder,path):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(folder.rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts:z.write(f,(Path(folder.name)/f.relative_to(folder)).as_posix())

for repo,name,description,paths,body in CONFIG:
    source=UP/repo.replace('/','__');dest=DEST/name;dest.mkdir(exist_ok=True)
    pin=next(p for p in PINS if p['repository']==repo)
    for relative in paths:
        p=source/relative
        target=dest/(relative.removeprefix('skills/ppt-master/'))
        if target.name=='SKILL.md':target=dest/'SKILL.upstream.md'
        if repo=='hugohe3/ppt-master' and p.name=='templates':
            # Do not redistribute unrelated branding, media or unreviewed icon libraries.
            for child in p.iterdir():
                if child.name not in ['brands','decks','icons','sounds']:copy(child,target/child.name)
        else:copy(p,target)
    copy(source/'LICENSE',dest/'LICENSE')
    attribution=f"  license: {pin['github_license']}\n"
    if repo=='hugohe3/ppt-master':
        for f in ['SPONSORS.md','SPONSORS_CN.md']:copy(source/'skills/ppt-master'/f,dest/f)
        attribution='  copyright: "Copyright (c) 2025-2026 Hugo He"\n  license: "MIT"\n  official_repository: "https://github.com/hugohe3/ppt-master"\n  sponsors:\n    - "SPONSORS.md"\n    - "SPONSORS_CN.md"\n'
        body+='\n元の帰属ガードを保持する。制作前に `python3 "${SKILL_DIR}/scripts/attribution_guard.py"` を実行する。元の著作権・ライセンス・スポンサーの表示は削除しない。\n'
    metadata=f"---\nname: {name}\ndescription: {description}\nmetadata:\n"+attribution+f"  upstream: https://github.com/{repo}\n  upstream_commit: {pin['commit']}\n---\n\n"
    (dest/'SKILL.md').write_text(metadata+body,encoding='utf-8')
    (dest/'references').mkdir(exist_ok=True)
    (dest/'references/japanese-fonts.md').write_text('日本語書体はNoto Sans JP / Noto Serif JP / BIZ UDPGothicから用途で選ぶ。ウェブ版はこのフォルダーのfonts.cssを使える。サブセットは収録文字のみなので、未収録の日本語を追加するときは元フォントから再生成する。改変時は内部名とOFLのReserved Font Nameを確認する。PowerPointでは受け手側の書体も確認する。\n',encoding='utf-8')
    for f in (ROOT/'assets/fonts').glob('*'):
        if f.is_file():copy(f,dest/'references/fonts'/f.name)
    css=(ROOT/'assets/studio.css').read_text(encoding='utf-8').split(':root')[0]
    (dest/'references/fonts.css').write_text(css,encoding='utf-8')
    if repo=='op7418/guizang-ppt-skill':
        for f in (ROOT/'sources/browser-dependencies').glob('*'):copy(f,dest/'assets'/f.name)
    source_files=[]
    for f in sorted(dest.rglob('*')):
        if f.is_file() and f.name not in ['SOURCE.json'] and '__pycache__' not in f.parts and f.suffix!='.pyc':
            source_files.append(dict(path=f.relative_to(dest).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    record=dict(repository=repo,commit=pin['commit'],license=pin['github_license'],modified_on='2026-10-13',maintainer='八百万図AIツールボックス',scope='source-based Japanese entrypoint; original implementation retained',files=source_files)
    (dest/'SOURCE.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    zip_folder(dest,DOWNLOADS/(name+'.zip'))
    pin['derived_skill']=name;pin['status']='upstream_implementation_packaged_japanese_entrypoint'
    print(name,len(source_files),'source files')

for pin in PINS:
    if pin['repository']=='JimLiu/baoyu-skills':pin['derived_skill']=None;pin['status']='license_reviewed_not_executed'
(ROOT/'data/upstreams.json').write_text(json.dumps(PINS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

for name in ['guizang-magazine','frontend-bold-signal']:
    folder=ROOT/'examples/actual'/name
    for f in (ROOT/'assets/fonts').rglob('*'):
        if f.is_file() and f.name.endswith(('OFL.txt','LICENSE.txt')):copy(f,folder/'font-licenses'/f.name)
    zip_folder(folder,DOWNLOADS/(name+'-ja.zip'))
print('Packaged 3 genuine forks and 2 HTML source bundles; not installed globally')
