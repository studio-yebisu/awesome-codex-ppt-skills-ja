"""Native deck made with liustack/pptwise's original v5 CLI and theme engine.

Original engine MIT, fixed commit 65690bc705c1b5db41b5593015675945673da542.
No post-processing, external API, or generic substitute renderer.
"""
from pathlib import Path
import argparse, json, subprocess, shutil, hashlib, os, zipfile

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/liustack__pptwise'
CASE=ROOT/'examples/repositories/pptwise-showcase'
FORK=ROOT/'skill-forks/pptwise-ja'
COMMIT='65690bc705c1b5db41b5593015675945673da542'
NODE='C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
CLI=UP/'dist/cli.js'

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,name):
    result=subprocess.run([NODE,str(CLI),*map(str,args)],capture_output=True,text=True,encoding='utf-8',errors='replace',cwd=ROOT)
    write(CASE/'source'/name,result.stdout+result.stderr)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    return result.stdout

PROMPT='''架空のものづくり拠点「街の作業場」の提案を、日本語6ページで完成させてください。表題は「ひらく、街の作業場。」、副題は「架空のものづくり拠点の提案」。地域の運営者とつくり手が、この場所の入口・体験・関係・空間構成を話せる資料にします。橙・墨・紙色、大きな和文、静かな宣言と関係図で組版を変化させ、角丸カードや管理系チェックリストを避けます。実績・人数・面積・予算を捏造しません。liustack/pptwiseの元CLI、IR v5、nativeなtyped componentsとテーマを実際に使用。Rallyから命名済みの色とOSS書体へテーマを派生させ、原典validate→renderでPPTXを作ってください。全ページの詳細検査は不要で、生成と主出力の軽い確認、入力・依頼文・コード・短い日本語SKILL・利用ZIPを残してください。'''

SLIDES=[
 dict(id='open',type='cover',heading='ひらく、\n街の作業場。',subheading='架空のものづくり拠点の提案',notes='架空の拠点企画。設備、利用条件、実績を確定する資料ではなく、場所のあり方を提案する。'),
 dict(id='promise',type='content',kind='statement',heading='道具より先に、\n入口をつくる。',components=[dict(type='paragraph',text='見るだけの日も、手を動かす日も。\nものづくりに近づける場所を、街の中へ。')],background=dict(kind='color',value='#171716'),notes='高度な道具の保有より、見学や相談から入りやすいことを企画の約束とする。成果を保証する説明ではない。'),
 dict(id='journey',type='content',kind='process',heading='見る。試す。つくる。',components=[dict(type='flowchart',direction='LR',nodes=[dict(id='look',label='ひとまず見る'),dict(id='try',label='小さく試す'),dict(id='make',label='相談して作る'),dict(id='show',label='作品を見せる')],edges=[dict(from_='look',to='try'),dict(from_='try',to='make'),dict(from_='make',to='show')])],notes='来訪者の体験の一例。必ずこの順を通る制度ではなく、見学だけ、制作だけの参加も想定する。'),
 dict(id='network',type='content',kind='hierarchy',heading='制作を、ひとりにしない。',components=[dict(type='hub_spoke',center='街の作業場',items=[dict(label='つくる人',description='経験を持ち寄る'),dict(label='道具と材料',description='試せる環境'),dict(label='地域のお店',description='相談と展示'),dict(label='近隣の人',description='見に来る入口')])],notes='拠点を中心とする関係の概念図。実在の協力者や契約を表していない。'),
 dict(id='space',type='content',kind='hierarchy',heading='作業も、会話も、同じ屋根に。',components=[dict(type='architecture',direction='top_down',layers=[dict(title='ひらく',items=['入口の展示','見学する場所']),dict(title='つくる',items=['共同作業台','予約する工具']),dict(title='交わる',items=['相談の席','小さな発表'])])],notes='空間の概念構成。建築図、縮尺、動線の確定、安全設計や営業条件を示すものではない。'),
 dict(id='close',type='ending',heading='つくった先に、\n街がある。',subheading='完成品も、途中の手も、街へひらく。',notes='次の具体化では地域の利用者と場所の条件を確かめる。ここでは架空企画の約束を締めくくる。')
]
for s in SLIDES:
    for c in s.get('components',[]):
        for e in c.get('edges',[]):e['from']=e.pop('from_')

def prepare():
    theme=json.loads((CASE/'input/theme.json').read_text(encoding='utf-8-sig'))
    theme['style']['fonts']={'heading':['Zen Kaku Gothic New','Space Grotesk'],'body':['Zen Kaku Gothic New','Space Grotesk'],'figure':['Space Grotesk','Zen Kaku Gothic New']}
    theme['style']['shape']={'radius':0,'surfaces':'ruled','gapScale':1}
    theme['style']['allowCustomBackground']=True
    theme['style']['colors']['chartPalette']=['#FF6A00','#171716','#A64718','#D5C9B7']
    theme['style']['colors']['muted']='#2B2A26'
    for role,color in [('cover','#FF6A00'),('chapter','#171716'),('content','#F4F0E8'),('ending','#FF6A00')]:theme['style']['defaultBackgrounds'][role]={'kind':'color','value':color}
    theme['story']={'name':'街の作業場','story':'橙・墨・紙色、宣言と関係図で街の制作拠点を語る。','positioning':'架空の拠点の入口と体験を提案する。','audience':'地域の運営者とつくり手。','notFor':'実績報告や確定した建築・収支計画。','lineage':'原典Rallyのmarquee menuを保持し、色と書体、表面を派生。'}
    dump(CASE/'input/theme.json',theme)
    ir=dict(version='5',filename='deck.pptx',narrative=dict(strategy='storytelling',pacing='spacious',audience='public'),theme={'id':'machi-kobo'},footer=dict(page_number=True,notice='架空の企画 / 概念モデル'),slides=SLIDES)
    dump(CASE/'input/deck.json',ir)
    write(CASE/'PROMPT.txt',PROMPT)
    write(CASE/'input/BRIEF.md','# ひらく、街の作業場。\n\n読者：地域の運営者、つくり手、場所に関心のある人。目的：拠点の入口、体験、人の関係、空間構成を具体化する話し合い。6分の口頭提案、6ページ。組織、拠点、協力関係は架空。実績、面積、人数、予算を作らない。\n')
    write(CASE/'NOTES.md','\n\n'.join(f'## {i}. {s["heading"]}\n\n{s["notes"]}' for i,s in enumerate(SLIDES,1)))

def main():
    p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--package-only',action='store_true');args=p.parse_args()
    if not args.package_only:
        prepare()
        run(['validate',CASE/'input/deck.json'],'validate.log')
        run(['render',CASE/'input/deck.json','-o',CASE/'deck.pptx','--no-git-ignore'],'render.log')
        if args.render:subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'tools/render_powerpoint.ps1'),'-PresentationPath',str(CASE/'deck.pptx'),'-OutputDirectory',str(CASE/'render')],check=True)
        dump(CASE/'QA.json',dict(status='light_check_complete' if args.render else 'generated',native_pptx_created=True,slide_count=6,original_cli_validate_passed=True,original_cli_render_passed=True,powerpoint_render_count=1 if args.render else 0,main_slide_visual_check='pending',all_page_detailed_review=False,independent_review=False,native_structure_audit=False,zip_replay=False))
    package()

def package():
    read_files=['LICENSE','README.md','skills/pptwise/SKILL.md','skills/pptwise/references/spec.md','skills/pptwise/references/components.md','skills/pptwise/references/validate.md','docs/ir.md','docs/themes.md','tsup.config.ts','package.json']
    dump(CASE/'PROVENANCE.json',dict(repository='liustack/pptwise',upstream_commit=COMMIT,license='MIT',runtime='pptwise 0.44.0 original source-built CLI / Node24',read_files=read_files,original_cli_live_truth=['schema --spec','narratives --json','themes --json','schema --component flowchart/hub_spoke/architecture/paragraph','doctor'],theme_method='Original CLI theme fork rally with exact primary/accent/bg/text/surface anchors; original marquee menu retained. Deck-local theme sets Zen Kaku Gothic New/Space Grotesk, ruled surfaces and radius0. No PPTX post-processing.',concept_method='Typed original flowchart, hub_spoke and architecture components; direction/relations written in v5 input. Original themes/layout/export engine owns all geometry.',source_acquisition='Fixed Git commit with sparse checkout src/skills/docs/scripts/themes; common archive acquisition stopped above200MB, so giant media/gallery were excluded. Original source tsup ESM+DTS build succeeded, no full test run.',commands=['npx --no-install tsup','node runtime/dist/cli.js validate input/deck.json','node runtime/dist/cli.js render input/deck.json -o deck-rebuilt.pptx --no-git-ignore'],pptx_sha256=sha(CASE/'deck.pptx')))
    skill='''---
name: pptwise-ja
description: 原典pptwise CLIとIR v5で、企画の関係をnative図形と大きな日本語見出しのPPTXへ制作する。
---

# 日本語の拠点提案

1. 読者、提案の目的、時間、架空条件を決める。実績や予算を作らない。
2. upstream/SKILL.mdと必要なspec/components/validate referenceを読む。schema、narratives、themesの元CLI出力から始める。
3. input/deck.jsonはv5。kindとtyped componentsを意味で選び、flowchartは方向、hub_spokeは中心との関係、architectureは構成を表す。
4. input/theme.jsonは原典Rallyからの明示派生。色・OSS書体・ruled surfacesを設定。IRに座標やface指定を加えず、PPTXを後加工しない。
5. Node22.19+を用意しruntime/でnpm ci。展開rootで `node runtime/dist/cli.js validate input/deck.json`、次に `node runtime/dist/cli.js render input/deck.json -o deck-rebuilt.pptx --no-git-ignore`。
6. fonts/のZen Kaku Gothic NewとSpace Groteskを導入。PowerPointで主出力が開くことを確認し、PNG/PDFはsource/render_powerpoint.ps1を使う。

SKILL本文だけでは生成できず、input、theme、原典runtimeが必要。原典MIT、commit65690bc705c1b5db41b5593015675945673da542。原作者の公式日本語版ではありません。
'''
    readme='''# ひらく、街の作業場。

架空のものづくり拠点を提案する日本語6ページ。利用者数、収支、面積、実績を作らず、入口・体験・関係・空間の概念構成を語ります。

## 原典方式

liustack/pptwise0.44.0を固定source commitからbuildし、IR v5を原典validate→render CLIへ渡しました。原典Rallyをtheme forkで橙・墨・紙色へ派生。元marquee menuを保ち、日本語OSS書体、角のないruled surfacesを設定しています。元のflowchart/hub_spoke/architectureのtyped componentsとtheme/layout/export engineがnative図形と文字を生成。共通rendererへ名前を貼る方式やPPTX後加工ではありません。

## 再制作

Node22.19+が必要。runtime/は元MITのbuilt CLIと必要source、元package.json/lockです。画像API・認証・有料pack・global skill installは不要です。

```powershell
cd runtime
npm ci --ignore-scripts --no-audit --no-fund
cd ..
node runtime/dist/cli.js validate input/deck.json
node runtime/dist/cli.js render input/deck.json -o deck-rebuilt.pptx --no-git-ignore
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck-rebuilt.pptx -OutputDirectory render-rebuilt
```

原典sourceからbuildし直す場合はruntime/で`npx --no-install tsup`。元tsup.configとsrcを同梱しています。通常の制作ではbuilt CLIをそのまま使います。

input/deck.jsonを編集し、同じフォルダーのtheme.jsonがtheme bindingを解決します。PROMPT.txtはAI依頼文、NOTES.mdは講稿。完成deck.pptxは元CLIが指定パスへ直接書いたものです。

## 書体と条件

fonts/のZen Kaku Gothic NewとSpace GroteskをTTFから導入し、PowerPointを開き直してください。Zenは和文、Space Groteskは英数字。受け手にも導入します。公式Google Fonts未改変TTFとOFLを同梱し、WindowsFontsから抽出していません。書体そのものはPPTXへ埋め込んでいません。

原典MITのLICENSEを保持。runtimeが外部importする依存の原文条件はdependencies/に保持。node_modules、cache、秘密情報は配布しません。原作者の公式日本語版ではありません。

## 確認

元sourceのESM+DTS build、doctorのself-test、元CLI validate/render、PowerPoint必要な1回描画、主出力1枚が開くことのみ。全テスト、全ページ詳細目視、独立レビュー、native監査、ZIP再実行は未実施。QA.jsonに実際の状態を記録。
'''
    for folder in [CASE,FORK]:
        write(folder/'SKILL.md',skill);write(folder/'README.md',readme)
        shutil.copy2(UP/'LICENSE',folder/'LICENSE')
        shutil.copytree(UP/'skills/pptwise',folder/'upstream',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        for directory in ['dist','src']:
            shutil.copytree(UP/directory,folder/'runtime'/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.map','*.test.ts','*.test.tsx','__pycache__','*.pyc'))
        for filename in ['package.json','package-lock.json','tsup.config.ts','tsconfig.json','LICENSE']:
            shutil.copy2(UP/filename,folder/'runtime'/filename)
        if folder!=CASE:
            shutil.copytree(CASE/'input',folder/'input',dirs_exist_ok=True)
            for f in ['PROMPT.txt','NOTES.md']:shutil.copy2(CASE/f,folder/f)
        (folder/'source').mkdir(exist_ok=True)
        shutil.copy2(__file__,folder/'source/build_pptwise_showcase.py')
        shutil.copy2(ROOT/'tools/render_powerpoint.ps1',folder/'source/render_powerpoint.ps1')
        for family in ['zenkakugothicnew','spacegrotesk']:shutil.copytree(ROOT/'downloads/fonts'/family,folder/'fonts'/family,dirs_exist_ok=True)
        pkg=json.loads((UP/'package.json').read_text(encoding='utf-8'))
        for name in pkg['dependencies']:
            installed=UP/'node_modules'/name
            for f in installed.iterdir():
                if f.is_file() and f.name.lower().startswith(('license','notice','copying')):
                    target=folder/'dependencies'/name/f.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
        files=[]
        for base,dirs,names in os.walk(folder,followlinks=False):
            dirs[:]=[d for d in dirs if d not in {'node_modules','__pycache__','.build','cache'}]
            files += [Path(base)/n for n in names if n!='SOURCE.json' and not n.endswith('.pyc')]
        dump(folder/'SOURCE.json',dict(repository='liustack/pptwise',commit=COMMIT,license='MIT',modified=True,case_studies=['pptwise-showcase'],files=[dict(path=f.relative_to(folder).as_posix(),sha256=sha(f)) for f in sorted(files)]))
        name='pptwise-example-ja' if folder==CASE else 'pptwise-ja'
        target=ROOT/'downloads'/f'{name}.zip'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for f in sorted(files+[folder/'SOURCE.json']):z.write(f,Path(name)/f.relative_to(folder))
    p='examples/repositories/pptwise-showcase/'
    pages=[p+f'render/slide-{i:02d}.png' for i in range(1,7)]
    record=dict(id='pptwise-showcase',title='ひらく、街の作業場。— 架空のものづくり拠点の提案',use_case='地域拠点の企画提案',repository='liustack/pptwise',skill_repository='liustack/pptwise',upstream_commit=COMMIT,fork_id='pptwise-ja',page_count=6,format='pptx',preview_kind='powerpoint-render',style='橙・墨・紙 / 大きな日本語 / native関係図',cover=pages[0],interior=pages[3],preview=p+'index.html',artifact_download=p+'deck.pptx',pdf_download=p+'render/deck.pdf',source_download='downloads/pptwise-example-ja.zip',fork_download='downloads/pptwise-ja.zip',input=p+'input/BRIEF.md',input_data=p+'input/deck.json',prompt=p+'PROMPT.txt',prompt_text=PROMPT,provenance=p+'PROVENANCE.json',qa=p+'QA.json',guide=p+'README.md',titles=[s['heading'] for s in SLIDES],notes=[s['notes'] for s in SLIDES],method='原典pptwise0.44.0のv5 schema/validate/render CLI、派生Rally themeとnative typed componentsを使用。',sample_notice='拠点・協力関係・空間構成は架空の企画です。',pages=pages)
    dump(ROOT/'data/sol-pptwise-repository-examples.json',[record])
    dump(ROOT/'data/sol-pptwise-repository-guides.json',[dict(repository='liustack/pptwise',summary_ja='原典v5 typed componentsとテーマを使う編集可能な日本語拠点提案。',example_ids=['pptwise-showcase'],upstream_commit=COMMIT,license='MIT',license_paths=[p+'LICENSE'],skill_paths=['skill-forks/pptwise-ja/SKILL.md'],production_status='light_check_complete',requirements=['Node22.19+','PPTX生成に認証/API不要','Zen Kaku Gothic New / Space Grotesk','PNG/PDF: Windows Microsoft PowerPoint'],commands=['cd runtime','npm ci --ignore-scripts --no-audit --no-fund','node runtime/dist/cli.js validate input/deck.json','node runtime/dist/cli.js render input/deck.json -o deck-rebuilt.pptx --no-git-ignore'],guide=p+'README.md',source_download=record['source_download'],fork_download=record['fork_download'],limitations=['図はnative shapes/textで、データchart/table objectとは異なる','全ページ詳細目視・独立レビュー・native監査・ZIP再実行は未実施'])])
    write(CASE/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ひらく、街の作業場。</title><style>body{margin:0;background:#171716;color:#f4f0e8;font-family:sans-serif}header{padding:28px 5vw}a{color:#ff6a00}main{padding:0 5vw 50px;display:grid;gap:28px}img{width:100%;display:block}figure{margin:0}figcaption{padding:10px}</style><header><h1>ひらく、街の作業場。</h1><p>架空のものづくり拠点の提案 / 原典pptwise native PPTX</p><a href="deck.pptx">PowerPoint</a> · <a href="render/deck.pdf">PDF</a> · <a href="SKILL.md">日本語SKILL</a> · <a href="../../../downloads/pptwise-example-ja.zip">制作ZIP</a></header><main>'+''.join(f'<figure><img src="render/slide-{i:02d}.png" alt="{s["heading"]}"><figcaption>{i:02d} / 06</figcaption></figure>' for i,s in enumerate(SLIDES,1))+'</main></html>')
    print('Pptwise showcase, maintained fragments and kits completed.')

if __name__=='__main__':main()
