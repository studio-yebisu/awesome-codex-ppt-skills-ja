"""One-page workshop concept using mpuig/agent-slides' actual native ops CLI.

MIT upstream commit820782a5fb8cb8f251d7c0750e4299c321cd068c.
Self-authored styled template layouts are extracted; semantic text inherits
placeholder formatting through original plan+ops -> preflight/dry-run/render/qa CLI.
"""
from pathlib import Path
import argparse, importlib.util, json, sys, subprocess, os, shutil, hashlib, zipfile
import importlib.metadata
from pptx import Presentation
from pptx.util import Inches

ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/mpuig__agent-slides'
CASE=ROOT/'examples/repositories/agent-slides-showcase'
FORK=ROOT/'skill-forks/agent-slides-ja'
PROJECT=CASE/'input/project'
COMMIT='820782a5fb8cb8f251d7c0750e4299c321cd068c'
NAVY='102D45'; ORANGE='FF6A13'; WHITE='FFFFFF'; PALE='D9E7F1'
JP='Zen Kaku Gothic New'; EN='Manrope'

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cli(args,log,cwd=CASE):
    env={**os.environ,'PYTHONPATH':str(UP/'src'),'PYTHONIOENCODING':'utf-8'}
    if args[0] in {'extract','preflight','render','qa'} and '--verbose' not in args:args=[*args,'--verbose']
    r=subprocess.run([sys.executable,'-m','slides_cli.cli',*map(str,args)],env=env,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    write(CASE/'.private/runtime-logs'/log,r.stdout+r.stderr)
    public=(r.stdout+r.stderr).replace(str(CASE),'case').replace(str(UP),'runtime').replace(str(CASE).replace('\\','/'),'case').replace(str(UP).replace('\\','/'),'runtime')
    write(CASE/'source'/(Path(log).stem+'-report.txt'),public)
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    return r.stdout

def ops():
    o=[dict(op='add_slide',layout_name='Workshop Split')]
    def rect(x,y,w,h,color):o.append(dict(op='add_rectangle',slide_index=0,left=x,top=y,width=w,height=h,fill_color=color))
    def oval(x,y,w,h,color):o.append(dict(op='add_oval',slide_index=0,left=x,top=y,width=w,height=h,fill_color=color))
    def line(x1,y1,x2,y2,color=WHITE,width=1.5):o.append(dict(op='add_line_shape',slide_index=0,x1=x1,y1=y1,x2=x2,y2=y2,color=color,line_width=width))
    def text(t,x,y,w,h,size=22,color=WHITE,bold=False,font=JP):o.append(dict(op='add_text',slide_index=0,text=t,left=x,top=y,width=w,height=h,font_size=size,font_name=font,font_color=color,bold=bold))
    # Palette, split-panel, fixed label and placeholder typography come from the extracted layout.
    o.append(dict(op='set_semantic_text',slide_index=0,role='title',text='土曜日を、\n街の作業場に。'))
    o.append(dict(op='set_semantic_text',slide_index=0,role='body',text='つくる人も、見る人も。\n一日だけ、同じ作業台に集まる。'))
    text('一日の流れ（仮のプログラム）',.68,4.64,8.4,.42,15,PALE)
    line(1.16,5.3,7.71,5.3,PALE,1.7)
    for x,time,head,desc in [(1.05,'10:00','見つける','素材とアイデアに触れる'),(4.34,'12:00','つくる','試しながら、手を動かす'),(7.6,'15:00','見せる','途中も完成も、持ち寄る')]:
        oval(x,5.19,.22,.22,ORANGE)
        text(time,x-.12,5.58,2.6,.42,20,ORANGE,True,EN)
        text(head,x-.12,6.06,2.65,.46,23,WHITE,True)
        text(desc,x-.12,6.6,2.67,.4,13,PALE)
    text('架空の企画 / 開催日時・人数・会場・参加条件は未定',.68,7.03,8.95,.28,10,PALE)
    text('SATURDAY\nWORKSHOP',10.43,.75,2.6,1.08,24,NAVY,True,EN)
    text('街に、ひらく。',10.45,2.03,2.55,.56,22,NAVY,True)
    text('人・道具・街が\n出会う一日。',10.45,2.72,2.65,.87,20,NAVY)
    # Explicit unordered center relationships: line operations, then node plates.
    # They do not form a flow or a cycle. The left timeline is a different semantic unit.
    line(11.63,5.03,10.79,4.22,NAVY,1.8)
    line(11.63,5.03,12.52,4.22,NAVY,1.8)
    line(11.63,5.03,11.63,6.23,NAVY,1.8)
    oval(11.06,4.52,1.14,1.14,NAVY)
    oval(10.43,3.86,.73,.73,WHITE)
    oval(12.13,3.86,.73,.73,WHITE)
    oval(11.27,5.87,.73,.73,WHITE)
    text('場',11.3,4.79,.66,.6,27,WHITE,True)
    text('人',10.57,4.04,.52,.42,18,NAVY,True)
    text('道具',12.2,4.06,.65,.35,13,NAVY,True)
    text('街',11.41,6.04,.52,.42,18,NAVY,True)
    text('PLAN / NOT AN ACTUAL EVENT',10.44,6.92,2.55,.3,8,NAVY,font=EN)
    note='架空の一日ワークショップ企画。原典の1枚企画書として生成。午前10時・正午・午後3時は仮の行程案で開催実績や確定予定ではない。開催日時、人数、会場、材料、安全管理、参加条件は未定。右の関係図は、人・道具・街が場に関わる概念で、時系列や相互契約を意味しない。'
    o.append(dict(op='add_notes',slide_index=0,text=note))
    o.append(dict(op='set_core_properties',title='土曜日を、街の作業場に。',subject='架空の一日ワークショップ企画',author='Studio Yebisu',keywords='fictional concept; original agent-slides native operations'))
    return o,note

PROMPT='''架空の一日ワークショップ企画「土曜日を、街の作業場に。」を、企画の意図がすぐ伝わる完成1枚のネイティブ編集可能なPowerPointにしてください。紺、鮮やかな橙、白。巨大な日本語見出し、短い企画の約束、仮の一日の流れ、人・道具・街と場の関係図を組みます。原典mpuig/agent-slidesのtemplate extract→preflight→plan+ops→dry-run→render CLIを実際に使い、別の汎用rendererへ名前を貼らないでください。自作の紺/橙templateに書式付きtitle/body placeholderと複数layoutを用意し、元extractで契約化。Workshop Splitの背景・位置・字体をset_semantic_textで継承し、残りの要素は元native operationで生成。1枚指定を優先して表紙・免責・終頁を追加しない。日時・人数・会場・参加条件は未定、行程は仮案と表示し、実績を捏造しない。原典slides qaを実行しok:true、全1頁の実描画を確認する。独立評価は別記録とし、未確認を合格扱いしない。入力、依頼文、原典source/license、短い日本語SKILL、PPTX、PNG/PDF、2ZIPを完成させてください。'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');p.add_argument('--package-only',action='store_true');p.add_argument('--case-only',action='store_true');args=p.parse_args()
    if not args.package_only:
        CASE.mkdir(parents=True,exist_ok=True)
        spec=importlib.util.spec_from_file_location('workshop_template',CASE/'source/build_styled_template.py');template_builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(template_builder)
        (CASE/'input').mkdir(exist_ok=True)
        inventory=template_builder.build_template(CASE/'input/self-authored-workshop-template.pptx');dump(CASE/'source/template-inventory.json',inventory)
        cli(['docs','schema:slides-document'],'slides-document.schema.json')
        cli(['docs','schema:design-profile'],'design-profile.schema.json')
        cli(['docs','method:render'],'render-contract.json')
        cli(['extract',CASE/'input/self-authored-workshop-template.pptx','--output-dir',PROJECT,'--base-template-out',PROJECT/'base_template.pptx','--compact'],'extract.log')
        # Live extract uses content_layout_catalog.json and template_catalog.json.
        manifest=json.loads((PROJECT/'resolved_manifest.json').read_text('utf-8'));primary=manifest['theme']['palette']['accent1']
        if primary!=ORANGE:raise ValueError('Extracted template accent1 differs from authored template')
        profile=dict(name='saturday-workshop',template_path='base_template.pptx',content_layout_catalog_path='content_layout_catalog.json',archetypes_catalog_path='archetypes.json',primary_color_hex=primary,allowed_fonts=[JP,EN],allowed_colors_hex=[NAVY,ORANGE,WHITE,PALE],min_font_size_pt=8,max_font_size_pt=54,default_font_size_pt=22)
        dump(PROJECT/'design-profile.json',profile)
        cli(['preflight','--project-dir',PROJECT,'--profile',PROJECT/'design-profile.json','--compact'],'preflight.log')
        operations,note=ops()
        document=dict(plan=dict(deck_title='土曜日を、街の作業場に。',brief='一日の制作体験を街へひらく、架空のワークショップ企画。',audience='地域の運営者・つくり手・参加に関心のある人',objective='企画の入口と仮の体験構成を、1枚から話し合う。',assumptions=['架空企画','仮の行程','会場・人数・開催日未定'],slides=[dict(slide_number=1,story_role='recommendation',archetype_id='big_statement',action_title='土曜日を、街の作業場に。',key_points=['つくる人も見る人も集まる','見つける→つくる→見せる','人・道具・街が場を介して出会う'],source_note='架空の企画・仮のプログラム')]),ops=dict(operations=operations))
        dump(CASE/'input/slides.json',document)
        cli(['render','--slides-json','@'+str(CASE/'input/slides.json'),'--profile',PROJECT/'design-profile.json','--dry-run','--compact'],'dry-run.log')
        cli(['render','--slides-json','@'+str(CASE/'input/slides.json'),'--profile',PROJECT/'design-profile.json','--output',CASE/'deck.pptx','--compact'],'render.log')
        cli(['qa',CASE/'deck.pptx','--profile',PROJECT/'design-profile.json','--slides-json','@'+str(CASE/'input/slides.json'),'--out',CASE/'reviews/original-qa.json','--compact'],'original-qa.log')
        write(CASE/'PROMPT.txt',PROMPT);write(CASE/'NOTES.md',note)
        write(CASE/'input/BRIEF.md','# 土曜日を、街の作業場に。\n\n1枚で企画の入口を伝える。地域の運営者、つくり手、参加に関心のある人へ、街で一日ものづくりをする場を提案。架空企画。行程は仮、日時・人数・会場・参加条件は未定。関係図と行程の意味を混ぜない。\n')
        if args.render:subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'tools/render_powerpoint.ps1'),'-PresentationPath',str(CASE/'deck.pptx'),'-OutputDirectory',str(CASE/'render')],check=True)
        dump(CASE/'QA.json',dict(status='light_check_complete' if args.render else 'native_generated',page_count=1,original_extract_preflight_dry_run_render=True,powerpoint_render_count=1 if args.render else 0,main_slide_visual_check='pending',full_deck_review=False,native_audit=False,independent_review=False,zip_replay=False))
    package(write_catalog=not args.case_only)

def package(write_catalog=True):
    _,note=ops()
    applied={'WWWH':'Who=local operators/makers, Why=shared concept, What=open one day of making, How=one statement+journey+hub relation','native_ops':'Original add_slide/set_semantic_text/add_text/add_rectangle/add_oval/add_line_shape/add_notes/set_core_properties through actualCLI; layout owns background/sidebar/fixedlabel.','layout_patterns':'Original split-panel hierarchy and number-badge/time-line primitives adapted without repeated cards','process':'Left directed schedule is separate from right unordered center relationships','template_contract':'Self-authored styled16:9 template with Workshop Cover/Split layouts; original extract supplies actual palette, placeholder geometry and formatting; set_semantic_text inherits title/body format.','user_overrides':'One finished slide, no automatic cover/disclaimer/ending. Giant Japanese headline and requested palette override standard 24pt business defaults. Original required slides qa gate executed; independent review tracked separately.'}
    dump(CASE/'PROVENANCE.json',dict(repository='mpuig/agent-slides',upstream_commit=COMMIT,license='MIT',runtime='Original agent-slides Python3.12+ CLI / python-pptx',read_files=['LICENSE','README.md','pyproject.toml','skills/slides-build/SKILL.md','skills/slides-full/SKILL.md','skills/slides-extract/SKILL.md','skills/slides-build/references/storytelling.md','skills/slides-build/references/content-density.md','skills/slides-build/references/layout-patterns.md','skills/slides-build/references/operations.md','skills/slides-build/references/process-patterns.md','skills/slides-build/references/common-mistakes.md','src/slides_cli/api.py','src/slides_cli/model.py'],applied_rules=applied,commands=['python -m slides_cli.cli extract input/self-authored-workshop-template.pptx --output-dir input/project --base-template-out input/project/base_template.pptx --compact','python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact','python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact','python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --output deck-rebuilt.pptx --compact','python -m slides_cli.cli qa deck.pptx --profile input/project/design-profile.json --slides-json @input/slides.json --out reviews/original-qa.json --compact'],pptx_sha256=sha(CASE/'deck.pptx'),font_embedding=False))
    skill='''---
name: agent-slides-ja
description: 既存PPTXの書式・配置を抽出し、planとnative編集操作からPowerPointを生成・検査する。
---

# 1枚で企画を伝える

1. 読者、話し合う目的、核となる提案、架空条件を決める。原典slides-buildとstorytelling/layout-patterns/operationsを読む。
2. Python3.12+で `pip install ./runtime`。原典extract→preflight契約を保持する。input/projectに完成例の抽出契約とbase_template.pptxを同梱。
3. input/slides.jsonのplanとopsを編集。巨大な提案文、短い約束、仮の行程、 unorderedな関係図を分ける。数値は実績と計画を区別。
4. `python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact`。
5. `python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact`、続けて同コマンドのdry-runを`--output deck-rebuilt.pptx`へ置換。
6. 原典必須gate `python -m slides_cli.cli qa deck-rebuilt.pptx --profile input/project/design-profile.json --slides-json @input/slides.json --out qa.json --compact` を実行しok:trueを確認。問題を直して再実行する。
7. 指定字体を導入してPowerPointで全頁PNG/PDFを描画し、文字・図・配置・継承書式を目視する。本例は1頁で、左の仮行程と右の関係図を区別する。作者検査と指定済み独立評価は別記録とする。

原典MIT、commit820782a5fb8cb8f251d7c0750e4299c321cd068c。1枚指定に合わせ自動構造ページ追加を省いた明示派生。SKILL本文だけでは生成できず、原典runtime・ops・template契約が必要。原作者の公式日本語版ではありません。
'''
    readme='''# 土曜日を、街の作業場に。

架空の一日ワークショップを伝える、独立1ページのnative企画書です。複数ページを1枚扱いにしていません。日時・人数・会場・参加条件は未定。10:00/12:00/15:00は仮のプログラムで、開催予定の確定や実績を示しません。

## 原典方式

mpuig/agent-slidesの元CLIとplan+ops形式を使用。自作の実書式templateにWorkshop Cover/Split layoutとtitle/body placeholder、紺背景と橙panelを持たせ、元extractで契約化。元preflight、dry-run、render、qaを実行します。背景・位置・字体はlayoutから、主題と説明はset_semantic_textで継承し、その他は元native操作です。templateはこの作例のための自作で、会社や第三者のtemplateではありません。左の行程は順序、右の人・道具・街は場との関係を表し、循環を捏造しません。

原典のWWWH、結論先行、split-panel、階層、badge/timelineパターンを反映。1枚指定と巨大和文の美術指示を優先して、元skillの自動構造ページ追加・24pt標準サイズ・反復カードを採用しない明示派生です。PPTXを別rendererで偽装していません。

## 再制作

Python3.12+を用意。認証/API/key/専有writer/global skill installは不要です。

```powershell
python -m pip install ./runtime
python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact
python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --dry-run --compact
python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --output deck-rebuilt.pptx --compact
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath deck-rebuilt.pptx -OutputDirectory render-rebuilt
```

input/slides.jsonが実際の入力、input/project/design-profile.jsonが配色・書体・契約の入口です。抽出から再実行する場合はPROVENANCEのextract commandを使用。source/build_agent_slides_showcase.pyは元カタログ内の制作用記録で、ZIPの利用者は上記の元CLIを直接使用します。

## 書体と条件

fonts/のZen Kaku Gothic New（和文）とManrope（英数字）をTTFから導入し、PowerPointを開き直してください。受け手にも導入します。公式Google Fontsの未改変TTFとOFLを同梱。WindowsFonts抽出なし、PPTX内のフォント埋め込みなし。

原典MITのLICENSE、Python依存の原文条件を保持。原作者の公式日本語版ではありません。node_modules、cache、秘密情報は配布しません。

## 確認範囲

元extract/preflight/dry-run/renderと必須slides qaを実行し、実描画を目視します。source/template-inventory.json、入力templateと抽出manifest、継承の照合記録、reviews/original-qa.jsonを参照。独立評価の合格とZIP再実行は別記録で、未実施を完了扱いにしません。
'''
    for folder in [CASE,FORK]:
        write(folder/'SKILL.md',skill);write(folder/'README.md',readme)
        shutil.copy2(UP/'LICENSE',folder/'LICENSE')
        shutil.copytree(UP/'src',folder/'runtime/src',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        for f in ['pyproject.toml','README.md','LICENSE','uv.lock']:shutil.copy2(UP/f,folder/'runtime'/f)
        for directory in ['slides-build','slides-extract']:
            shutil.copytree(UP/'skills'/directory,folder/'upstream'/directory,dirs_exist_ok=True)
        if folder!=CASE:
            shutil.copytree(CASE/'input',folder/'input',dirs_exist_ok=True)
            for f in ['PROMPT.txt','NOTES.md']:shutil.copy2(CASE/f,folder/f)
        (folder/'source').mkdir(exist_ok=True)
        shutil.copy2(__file__,folder/'source/build_agent_slides_showcase.py')
        shutil.copy2(ROOT/'tools/render_powerpoint.ps1',folder/'source/render_powerpoint.ps1')
        for family in ['zenkakugothicnew','manrope']:shutil.copytree(ROOT/'downloads/fonts'/family,folder/'fonts'/family,dirs_exist_ok=True)
        for name in ['python-pptx','lxml','pydantic','pydantic-core','typing-extensions']:
            dist=importlib.metadata.distribution(name)
            for item in dist.files or []:
                if any(str(item).lower().split('/')[-1].startswith(x) for x in ['license','notice','copying']):
                    f=Path(dist.locate_file(item))
                    if f.is_file():
                        target=folder/'dependencies'/name/f.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
        files=[]
        for base,dirs,names in os.walk(folder,followlinks=False):
            dirs[:]=[d for d in dirs if d not in {'node_modules','__pycache__','.build','cache','.private','.git'}]
            files += [Path(base)/n for n in names if n!='SOURCE.json' and not n.endswith(('.pyc','.log'))]
        dump(folder/'SOURCE.json',dict(repository='mpuig/agent-slides',commit=COMMIT,license='MIT',modified=True,case_studies=['agent-slides-showcase'],files=[dict(path=f.relative_to(folder).as_posix(),sha256=sha(f)) for f in sorted(files)]))
        name='agent-slides-example-ja' if folder==CASE else 'agent-slides-ja'
        with zipfile.ZipFile(ROOT/'downloads'/f'{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
            for f in sorted(files+[folder/'SOURCE.json']):z.write(f,Path(name)/f.relative_to(folder))
    p='examples/repositories/agent-slides-showcase/'
    record=dict(id='agent-slides-showcase',title='土曜日を、街の作業場に。',use_case='1枚のワークショップ企画書',repository='mpuig/agent-slides',skill_repository='mpuig/agent-slides',upstream_commit=COMMIT,fork_id='agent-slides-ja',page_count=1,format='pptx',preview_kind='powerpoint-render',style='紺・橙・白 / 大和文 / split-panel timeline・関係図',cover=p+'render/slide-01.png',interior=p+'render/slide-01.png',preview=p+'index.html',artifact_download=p+'deck.pptx',pdf_download=p+'render/deck.pdf',source_download='downloads/agent-slides-example-ja.zip',fork_download='downloads/agent-slides-ja.zip',input=p+'input/BRIEF.md',input_data=p+'input/slides.json',prompt=p+'PROMPT.txt',prompt_text=PROMPT,provenance=p+'PROVENANCE.json',qa=p+'QA.json',guide=p+'README.md',titles=['土曜日を、街の作業場に。'],notes=[note],method='実書式を持つ自作templateを原典extractし、native placeholderの書式をset_semantic_textで継承。plan+ops dry-run/renderと必須qaを実行した独立1ページ。',sample_notice='架空の企画。行程は仮、日時・人数・会場・参加条件は未定。',pages=[p+'render/slide-01.png'])
    if write_catalog:dump(ROOT/'data/sol-agent-slides-repository-examples.json',[record])
    if write_catalog:dump(ROOT/'data/sol-agent-slides-repository-guides.json',[dict(repository='mpuig/agent-slides',summary_ja='原典template契約とnative opsで企画を1枚へ完成する日本語派生。',example_ids=['agent-slides-showcase'],upstream_commit=COMMIT,license='MIT',license_paths=[p+'LICENSE'],skill_paths=['skill-forks/agent-slides-ja/SKILL.md'],production_status='light_check_complete' if (CASE/'render/slide-01.png').exists() else 'native_generated',requirements=['Python3.12+ / agent-slides native runtime','Zen Kaku Gothic New / Manrope','PNG/PDF: Windows Microsoft PowerPoint'],commands=['python -m pip install ./runtime','python -m slides_cli.cli preflight --project-dir input/project --profile input/project/design-profile.json --compact','python -m slides_cli.cli render --slides-json @input/slides.json --profile input/project/design-profile.json --output deck-rebuilt.pptx --compact'],guide=p+'README.md',source_download=record['source_download'],fork_download=record['fork_download'],limitations=['独立1ページの企画書','仮行程、会場・日時・人数未定','原典qa実行済み。独立合格・ZIP再実行は別記録'])])
    write(CASE/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>土曜日を、街の作業場に。</title><style>body{margin:0;background:#102d45;color:white;font-family:sans-serif}header,main{padding:25px 5vw}a{color:#ff6a13}img{width:100%;display:block}</style><header><h1>土曜日を、街の作業場に。</h1><p>1枚で伝える架空ワークショップ企画 / 原典agent-slides native PPTX</p><a href="deck.pptx">PowerPoint</a> · <a href="render/deck.pdf">PDF</a> · <a href="SKILL.md">日本語SKILL</a> · <a href="../../../downloads/agent-slides-example-ja.zip">制作ZIP</a></header><main><img src="render/slide-01.png" alt="紺と橙の1枚ワークショップ企画書"></main></html>')
    print('One-page agent-slides showcase and two source kits ready.')

if __name__=='__main__':main()
