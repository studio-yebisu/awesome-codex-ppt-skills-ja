"""Author supported outline JSON and invoke siril9's original native renderer.
No one-off PPTX generator, generated-PPTX patch, host SDK, or image fallback.
"""
from pathlib import Path
import argparse,difflib,hashlib,json,os,shutil,subprocess,sys,zipfile

SCRIPT=Path(__file__).resolve();ROOT=SCRIPT.parents[1]
CASE=ROOT/'examples/repositories/presentation-skill-showcase' if SCRIPT.parent.name=='tools' else SCRIPT.parent.parent
FORK=ROOT/'skill-forks/presentation-skill-ja'
PIN='efd899c5ddf866af2ce0001c4c9340af775d4d55';REPO='siril9/presentation-skill'
TITLES=['仕事の引き継ぎを、迷わない一枚に。','情報・担当・確認をそろえる','引き継ぎは、順番を決める','期限と状態を、一枚に並べる','次に動く条件を、明らかに','次の担当が、動ける状態まで。']
PROMPT='''日本語6枚「仕事の引き継ぎを、迷わない一枚に。」を制作してください。
架空の社内運用。必要情報・担当・確認の関係、引継ぎ順、期限と状態のnative表、次に動く条件を原典native要素で示す。
siril9/presentation-skillのoriginal outline schema、Operating Grid grammar、render-plan/role-layout contracts、既定PptxGenJS生成器を実際に使用する。
大きく短い見出し、明暗の切替、図解と余白。6枚すべてを角丸カード格子にしない。Shippori明朝の見出し、BIZ UDPGothicの本文、Manropeの番号・英数字を役割別に使う。
人名・会社名・実績値を作らず、送り手・次の担当・確認役という仮の役割、相対期限・仮の状態例として明記。
原典必須engineを省略せず、汎用rendererへのラベル貼りや生成済みPPTXの手修正をしない。artifact-toolホストSDKは使わない。
原典生成・必要buildと代表完成物の初回表示だけ確認。全ページ詳細目視、独立レビュー、構造監査、ZIP再実行を追加しない。
PPTX/PNG/PDF、原稿/入力/依頼、再生成コード、未変更原本/局所差分、短い日本語SKILL、SOURCE/許諾/実TTF/OFL、制作ZIPとfork ZIPを完成させる。'''

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def outline(brief):
    chosen=brief['route_candidates'][0]
    style={'style_preset':chosen['style_preset'],'composition_grammar':chosen['grammar_id'],'style_seed':'ja-handoff-six-pages','font_pair':'handoff_ja_v1','visual_density':'medium','emoji_mode':'none','footer_mode':'source-line','footer_page_numbers':True,'header_variant':'plain','title_motif':'none','comparison_mode':'open-columns','table_treatment':'compact-ledger','readability_contract':brief['outline_contract']['deck_style']['readability_contract']}
    # Role/variant are the original schema's structures, not arbitrary coordinates.
    pages=[
      {'type':'title','role':'title','theme':'dark','title':'仕事の引き継ぎを、\n迷わない一枚に。','subtitle':'必要情報・担当・確認を、一枚にそろえる。','notes':'架空の社内運用を説明する6枚。実際の引継ぎメモを一枚に整える例。実在の会社・社員・実測値ではない。'},
      {'type':'content','role':'evidence','variant':'flow','visual_intent':'flow','slide_intent':'components','title':'情報・担当・確認をそろえる','subtitle':'三つがそろって、次の担当が判断できる。','flow_layout':'bands','flow_steps':[{'title':'必要情報','detail':'目的・資料の場所・完了条件'},{'title':'担当','detail':'送り手・次の担当・確認役'},{'title':'確認','detail':'受け取った内容と期限を合わせる'}],'summary_callout':'資料だけを渡さず、「誰が何を確認するか」まで書く。','caption':'関係を整理した仮想例。実際の担当分担ではありません。'},
      {'type':'content','role':'evidence','variant':'timeline','slide_intent':'handoff-order','title':'引き継ぎは、順番を決める','subtitle':'渡す前に、受け手と同じ認識をつくる。','timeline_mode':'open-events','milestones':[{'label':'01 WRITE','title':'書く','body':'目的・資料\n期限を一枚へ'},{'label':'02 MATCH','title':'合わせる','body':'内容を\n読み返す'},{'label':'03 CONFIRM','title':'確認する','body':'不明点を\n送り手へ'},{'label':'04 HANDOFF','title':'渡す','body':'確認後に\n担当を変更'}],'caption':'順序を説明する仮の運用案。実際の承認手続ではありません。'},
      {'type':'content','role':'table','variant':'table','slide_intent':'one-page-register','title':'期限と状態を、一枚に並べる','subtitle':'空欄を残さず、次の行動も一緒に書く。','table_treatment':'compact-ledger','table':{'headers':['項目','担当','期限（仮）','状態例','次に動く条件'],'rows':[['必要資料','送り手','前日','準備済み','保存先を確認'],['手順の確認','次の担当','開始前','確認待ち','不明点を解消'],['担当の変更','確認役','開始前','未実施','確認記録を残す'],['作業の開始','次の担当','当日','未着手','担当変更を確認']],'column_weights':[1.5,1.1,1.2,1.2,2.2],'caption':'すべて架空の記入例。期限は相対的な仮案、状態は説明用です。'},'notes':'このnative表が引継ぎメモの一枚の例。実在案件の進捗報告ではない。'},
      {'type':'content','role':'comparison','variant':'comparison-2col','slide_intent':'action-conditions','title':'次に動く条件を、明らかに','subtitle':'判断に必要な情報を、着手前に確かめる。','left':{'title':'着手できる','bullets':['目的が一文で分かる','資料の保存先がある','期限と担当を記載','確認記録が残っている']},'right':{'title':'送り手へ戻す','bullets':['資料が見つからない','期限が空欄','担当が重複・未定','完了条件が曖昧']},'verdict':'不明点を推測で埋めず、確認してから担当を切り替える。'},
      {'type':'section','role':'section','theme':'dark','section_number':'06','title':'次の担当が、\n動ける状態まで。','subtitle':'資料・期限・着手条件を、短い一枚に。','notes':'企画上の目標。運用効果を測定した結果ではない。'},
    ]
    for i,s in enumerate(pages):s.update(slide_id=f'handoff-{i+1:02}',footer='仮想の社内運用 / 人名・会社・実績値は使用していません')
    return {'title':TITLES[0],'subtitle':'架空の社内運用を図と表で説明する6枚','document_metadata':{'author':'Presentation Team','company':''},'deck_style':style,'metadata':{'synthetic':True,'external_assets':False,'authoring_model':'gpt-6.1-sol','chosen_original_route':chosen['grammar_id'],'review':'user_requested_minimal','python_data_pipeline':'not used; original default Node renderer selected'},'compliance':{'require_attribution':False,'auto_image_sources':False},'slides':pages}

def prepare():
    up=ROOT/'.build/actual-upstreams/siril9__presentation-skill'
    # Full original template modules and canonical role contracts are mandatory.
    for rel in ['LICENSE','SKILL.md','package.json','scripts/build_deck_pptxgenjs.js','scripts/present.py','scripts/runtime_doctor.py','scripts/requirements-runtime.txt','references/outline_schema.md','references/renderer_role_contracts_v2.json','references/pptxgenjs.md','templates/pptxgenjs/README.md']:
        out=CASE/'upstream'/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(up/rel,out)
    shutil.copytree(up/'templates/pptxgenjs',CASE/'upstream/templates/pptxgenjs',dirs_exist_ok=True)
    shutil.copytree(up/'schemas',CASE/'upstream/schemas',dirs_exist_ok=True)
    for name in ['scripts','templates','references','schemas']:(CASE/'runtime'/name).mkdir(parents=True,exist_ok=True)
    shutil.copytree(up/'templates/pptxgenjs',CASE/'runtime/templates/pptxgenjs',dirs_exist_ok=True)
    shutil.copytree(up/'schemas',CASE/'runtime/schemas',dirs_exist_ok=True)
    shutil.copy2(up/'references/renderer_role_contracts_v2.json',CASE/'runtime/references/renderer_role_contracts_v2.json')
    shutil.copy2(up/'LICENSE',CASE/'LICENSE');shutil.copy2(up/'LICENSE',CASE/'runtime/LICENSE')
    renderer=(up/'scripts/build_deck_pptxgenjs.js').read_text(encoding='utf-8');original=renderer
    renderer=renderer.replace('const FONT_PAIRS = {',"const FONT_PAIRS = {\n  handoff_ja_v1: { font_heading: 'Shippori Mincho', font_body: 'BIZ UDPGothic', font_number: 'Manrope', font_table_header: 'BIZ UDPGothic' },",1)
    renderer=renderer.replace('preset.font_caption = fontPair.font_body;','preset.font_caption = fontPair.font_body;\n    preset.font_number = fontPair.font_number || fontPair.font_body;\n    preset.font_table_header = fontPair.font_table_header || fontPair.font_body;',1)
    write(CASE/'runtime/scripts/build_deck_pptxgenjs.js',renderer)
    write(CASE/'source/font-pair.diff',''.join(difflib.unified_diff(original.splitlines(True),renderer.splitlines(True),fromfile='upstream/scripts/build_deck_pptxgenjs.js',tofile='runtime/scripts/build_deck_pptxgenjs.js')))
    slides=(up/'templates/pptxgenjs/slides.js').read_text(encoding='utf-8');oldslides=slides
    slides=slides.replace("fontFace: preset.font_body,\n        fontSize: roleMetadataFont(preset, 8.4)","fontFace: preset.font_number || preset.font_body,\n        fontSize: roleMetadataFont(preset, 8.4)")
    slides=slides.replace('fontSize: captionFont, fontFace: preset.font_heading, bold: true,','fontSize: captionFont, fontFace: preset.font_number || preset.font_heading, bold: true,')
    slides=slides.replace('fontSize: labelFont, color, bold: true, objectName: `metadata:timeline-label-${index}`','fontSize: labelFont, fontFace: preset.font_number || preset.font_body, color, bold: true, objectName: `metadata:timeline-label-${index}`')
    slides=slides.replace('bold: true,\n    fontFace: preset.font_title,\n    fontSize: headerFont,','bold: true,\n    fontFace: preset.font_table_header || preset.font_title,\n    fontSize: headerFont,',1)
    slides=slides.replace("'TABLE INDEX'","'引き継ぎメモ'").replace('${table.rows.length} rows','${table.rows.length}項目')
    write(CASE/'runtime/templates/pptxgenjs/slides.js',slides)
    write(CASE/'source/numeric-font.diff',''.join(difflib.unified_diff(oldslides.splitlines(True),slides.splitlines(True),fromfile='upstream/templates/pptxgenjs/slides.js',tofile='runtime/templates/pptxgenjs/slides.js')))
    brief=json.loads((CASE/'input/agent-brief.json').read_text(encoding='utf-8'));source_outline=outline(brief)
    dump(CASE/'input/outline.json',source_outline)
    dump(CASE/'input/design-decisions.json',{'chosen_candidate':brief['route_candidates'][0],'source_style':'lavender-ops','source_grammar':'operations-grid','geometry':'original supported role/variant/flow/table systems; no arbitrary coordinates','font_roles':{'heading':'Shippori Mincho','body':'BIZ UDPGothic','native flow indexes / footer page numbers':'Manrope'},'changes':['local font_pair adapter','native numeric metadata font mapping'],'plan':['dark title','native bands for required relations','native open timeline','native status table','comparison conditions','dark section conclusion'],'images':'not required: official native flow_steps and native table route','python_doctor':'source/python-doctor.log records missing optional scientific data runtime; not declared ready','review':'User requested minimal generation and first display'})
    write(CASE/'input/BRIEF.md','# 仕事の引き継ぎを、迷わない一枚に。\n\n引継ぎメモを一枚に整理する考え方を説明する6枚の教材。架空の社内運用で、人名・会社名・実績値は使用しない。必要情報・担当・確認、引継ぎ順、期限と状態、次の着手条件を示す。期限は相対的な仮案、状態は説明用の例。\n')
    write(CASE/'PROMPT.md',PROMPT+'\n')
    write(CASE/'MANUSCRIPT.md','\n\n'.join(f'## {i+1}. {s["title"]}\n\n'+str(s.get('subtitle',''))+'\n\n'+str(s.get('notes','仮想の社内運用例。')) for i,s in enumerate(source_outline['slides']))+'\n')
    want={'shipporimincho':['ShipporiMincho-Regular.ttf','ShipporiMincho-Bold.ttf'],'bizudpgothic':['BIZUDPGothic-Regular.ttf','BIZUDPGothic-Bold.ttf'],'manrope':['Manrope[wght].ttf']}
    for family,names in want.items():
        for name in names+['OFL.txt']:
            dest=CASE/'fonts'/family/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'downloads/fonts'/family/name,dest)
    kit=json.loads((ROOT/'data/oss-font-kit.json').read_text(encoding='utf-8'));dump(CASE/'fonts/SOURCE.json',{'families':[f for f in kit['families'] if f['id'] in want],'used_files':want,'modified':False,'os_font_extraction':False})
    dump(CASE/'package.json',{'private':True,'dependencies':{'pptxgenjs':'4.0.1','jszip':'3.10.1'}})
    for dep in ['pptxgenjs','jszip']:
        path=ROOT/'.build/node_modules'/dep
        for f in path.iterdir():
            if f.is_file() and f.name.lower().startswith(('license','notice','copying')):
                dest=CASE/'dependencies'/dep/f.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
    write(CASE/'source/render_powerpoint.ps1',(ROOT/'tools/render_powerpoint.ps1').read_text(encoding='utf-8').replace('if ($existingPowerPoint.Count -eq 0 -and $powerPoint.Presentations.Count -eq 0) { $powerPoint.Quit() }','# Shared application: close only this opened presentation; never Quit.'))
    shutil.copy2(SCRIPT,CASE/'source/build.py')

def execute(node):
    modules=ROOT/'.build/node_modules' if SCRIPT.parent.name=='tools' else CASE/'node_modules'
    env={**os.environ,'NODE_PATH':str(modules),'PPTX_NODE_MODULES':str(modules)}
    deps={name:json.loads((modules/name/'package.json').read_text(encoding='utf-8'))['version'] for name in ['pptxgenjs','jszip']}
    if deps!={'pptxgenjs':'4.0.1','jszip':'3.10.1'}:raise RuntimeError('Original Node pinned dependencies mismatch: '+str(deps))
    cmd=[str(Path(node).resolve()),str(CASE/'runtime/scripts/build_deck_pptxgenjs.js'),'--outline',str(CASE/'input/outline.json'),'--output',str(CASE/'deck.pptx'),'--style-preset','lavender-ops','--render-plan-diagnostics']
    r=subprocess.run(cmd,cwd=CASE/'runtime',env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');write(CASE/'source/build.log',r.stdout+r.stderr)
    if r.returncode:raise RuntimeError((r.stdout+r.stderr)[-6500:])
    dump(CASE/'source/BUILD.json',{'exit_code':r.returncode,'original_node_builder':'runtime/scripts/build_deck_pptxgenjs.js','template_modules':'runtime/templates/pptxgenjs','canonical_role_contracts':'runtime/references/renderer_role_contracts_v2.json','input':'input/outline.json','preset':'lavender-ops','grammar':'operations-grid','node_dependencies':deps,'output':'deck.pptx','render_plan_diagnostics':'source/build.log','images_used':False,'artifact_tool_used':False,'one_off_generator':False,'full_python_data_pipeline_ready':False,'python_doctor':'source/python-doctor.log'})
    print('Original outline/render-plan/role-contract/PptxGenJS build succeeded.')

def finish():
    write(CASE/'SKILL.md',f'''---
name: presentation-skill-ja
description: 原典outline/role-contract/native PptxGenJSで日本語引継ぎ資料を作る。
---

# 日本語Presentation Skill

siril9/presentation-skill `{PIN}` / MIT。原典の既定rendererは `scripts/build_deck_pptxgenjs.js`。汎用generatorに名前だけ貼らず、outline schema、render-plan、canonical role-contract、templateを実行する。

1. 原典present.py briefで内容・style/grammarを選び、そのreadability contractと候補をoutlineへ引き継ぐ。今回の候補はlavender-ops / operations-grid。入力はsourceであり、生成PPTXを直接patchしない。
2. 原典schemaのnative flow_steps、timeline、table、comparisonを使う。図の内容を画像へ黙って代替しない。画像が必要な内容では原典asset pipelineを別途整える。
3. 短い日本語見出し・native図表・明暗・余白。font_pairの局所adapterだけでShippori / BIZ UDPGothic / Manropeを役割別に対応し、差分を保存。字体は公式TTF/OFLのみ。
4. 原典Node engineをPptxGenJS4.0.1/jszip3.10.1で実行。Python data pipelineのdoctor不足はログへ記録し、整備済みと称しない。この作例は原典既定Nodeのnative要素だけで完成する。
5. PowerPoint16でPNG/PDFを描画。Application.Quitは禁止、自deckだけClose。ユーザー指定を優先し、原典finalizeの包括QA/全ページレビュー/独立reviewを追加しない。生成と代表初回表示のみを記録。
6. PPTX/PNG/PDF、JSON/原稿/依頼/再生成コード/未変更原本/局所差分/許諾/日本語ガイドを渡す。人名・会社・実績を捏造しない。

## quick_validate

`node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops` を実行し、PowerPointで代表完成物を一度表示。
''')
    write(CASE/'README.md',f'''# 仕事の引き継ぎを、迷わない一枚に。

架空の社内運用を説明する6枚。引継ぎメモそのものを一枚に整える方法を、関係・順番・表・判断条件に分けて説明します。人名・会社名・実測値を使用せず、期限は相対的な仮案、状態は説明用の例です。

## 使用した原典と編集範囲

[siril9/presentation-skill](https://github.com/siril9/presentation-skill/tree/{PIN}) / MIT / `{PIN}`。
原典 `present.py brief` で選んだ `lavender-ops / operations-grid` 候補とreadability contractをJSONへ引き継ぎ、原典 `build_deck_pptxgenjs.js` に入力します。原典のrender-plan、role-layout contracts、templates/pptxgenjsを実際に実行したnative PPTXです。Python-pptxの別generatorやホストartifact-tool SDKは使っていません。

`flow_steps` は原典schemaが対応するnative図解、timelineはnative図形、状態表はnative table、比較はnative文字/形状。PowerPoint内で本文・図形・線・表を直接編集できます。native chart/数式は使用していません。PDF/PNGは閲覧用です。原稿を直して再生成するなら `input/outline.json` を編集します。

原典のOperating Gridを一貫したdesign systemとして使い、暗い表紙・結論、関係のbands、開いたtimeline、表、判断条件の2列を選択。手書き座標や生成後PPTX修正を避けています。原典未変更原本は `upstream/`、字体roleと表の注記を日本語化したruntime差分は `source/*.diff`。

見出しShippori Mincho、本文とnative表の見出しBIZ UDPGothic、native flow/timeline番号とページ番号Manrope。初回PowerPoint表示でShipporiの表見出しだけ和文が欠けたため、表見出しはBIZのboldに割り当てました。公式未変更TTF/OFLを `fonts/` に同梱。OS/Office字体を抽出していません。PowerPointの表示時にはこれらの字体をWindowsへ登録してください。

## 再生成

原典が既定と明記するNode/PptxGenJS route。Node.js、PptxGenJS4.0.1、jszip3.10.1、PowerPoint16（プレビュー生成用）が必要です。

```powershell
npm install
node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops
powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render
```

`source/build.py --node C:/path/to/node.exe` は同じ原典Node CLIを呼び出す補助入口で、PPTXを描画する別generatorではありません。原典・字体・依存のLICENSEを保持。Node_modules、Office、venv/cacheをZIPへ含めません。共有PowerPoint ApplicationをQuitせず、自分が開いたdeckだけCloseします。

## 実行環境と確認範囲

原典Python doctorも一度実行し、科学データ依存（pandas/pyarrow等）の不足とpin違いを `source/python-doctor.log` に保存しています。Python data/asset/finalize pipelineは準備完了とは報告しません。今回の原典既定Node rendererのnative flow/table/comparisonには、それらのPython科学依存は不要です。画像や実データの解析を追加する場合は原典のpinned Python環境を整備してください。

原典の生成・内蔵enum/role contract/text fit解決、PowerPoint16の6枚PNG/PDF生成、代表完成物の初回表示まで。ユーザー指定により全ページ詳細目視、独立review、包括finalize/構造監査、ZIP再実行は未実施。包括QA合格やProduction採用とは称しません。
''')
    for directory in ['upstream','runtime','source','input','fonts','dependencies']:shutil.copytree(CASE/directory,FORK/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.log','*.pptx','__pycache__','*.pyc'))
    for filename in ['SKILL.md','README.md','LICENSE','PROMPT.md','MANUSCRIPT.md','package.json']:shutil.copy2(CASE/filename,FORK/filename)
    meta={'repository':REPO,'commit':PIN,'license':'MIT','modified':True,'renderer':'original build_deck_pptxgenjs.js','grammar':'operations-grid','preset':'lavender-ops','editable_features':['text','shapes','tables'],'local_changes':['font_pair handoff_ja_v1','Manrope native numeric metadata mapping'],'source':'input/outline.json','example':'examples/repositories/presentation-skill-showcase','full_python_data_pipeline_ready':False,'review':'User-requested generation plus representative first display only'}
    dump(CASE/'SOURCE.json',meta);dump(FORK/'SOURCE.json',meta)
    dump(CASE/'PROVENANCE.json',{'repository':REPO,'upstream_commit':PIN,'license':'MIT','route':'present.py brief -> original outline schema -> build_deck_pptxgenjs.js -> original render-plan/role-layout/template modules -> native PowerPoint','originals':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'upstream').rglob('*') if p.is_file()},'source':'input/outline.json','style_decisions':'input/design-decisions.json','local_changes':'source/font-pair.diff, source/numeric-font.diff','node_dependencies':{'pptxgenjs':'4.0.1','jszip':'3.10.1'},'fonts':'fonts/SOURCE.json','font_files':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'fonts').rglob('*.ttf')},'build_receipt':'source/BUILD.json','render_receipt':'render/powerpoint-render.json','content_status':'hypothetical handoff operations, relative deadlines and example states','artifact_tool_used':False})
    dump(CASE/'QA.json',{'status':'ready_for_first_display','original_node_generation_success':True,'page_count':6,'powerpoint_render_success':(CASE/'render/deck.pdf').exists(),'representative_page_opened':False,'whole_deck_detailed_review':False,'independent_review':False,'structure_audit':False,'zip_reexecution':False,'full_finalize_gate_run':False,'python_doctor_passed':False,'node_pinned_requirements_checked':True,'review_mode':'user_requested_minimal'})
    images=''.join(f'<figure><img src="render/slide-{i+1:02}.png" alt="{tt}"><figcaption>{i+1}. {tt}</figcaption></figure>' for i,tt in enumerate(TITLES))
    write(CASE/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+TITLES[0]+'</title><style>body{margin:0;background:#f5f3ff;color:#2e1065;font-family:sans-serif}header,main{max-width:1200px;padding:24px;margin:auto}a{color:#6d28d9}figure{margin:0 0 30px}img{display:block;width:100%}figcaption{font-size:14px;padding-top:10px}</style><header><h1>'+TITLES[0]+'</h1><p>架空の社内運用 / 6枚 / native flow・table・timeline</p><a href="deck.pptx">PowerPoint</a> · <a href="render/deck.pdf">PDF</a> · <a href="README.md">日本語ガイド</a> · <a href="../../../downloads/presentation-skill-example-ja.zip">制作ZIP</a></header><main>'+images+'</main></html>')
    b='examples/repositories/presentation-skill-showcase'
    ex={'id':'presentation-skill-showcase','title':TITLES[0],'use_case':'native図解・表で整える引継ぎの6枚教材','repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'presentation-skill-ja','page_count':6,'format':'pptx','preview_kind':'powerpoint-render','preview_notice':'原典outline/role contracts/PptxGenJSによるnative文字・形状・表。PowerPoint内で編集可能。','editability':'native_tables','editable_features':['text','shapes','tables'],'style':'原典lavender-ops / Operating Grid / 明暗・明朝・native flowと表','cover':b+'/render/slide-01.png','interior':b+'/render/slide-04.png','preview':b+'/index.html','artifact_download':b+'/deck.pptx','pdf_download':b+'/render/deck.pdf','source_download':'downloads/presentation-skill-example-ja.zip','fork_download':'downloads/presentation-skill-ja.zip','input':b+'/input/BRIEF.md','input_data':b+'/input/outline.json','prompt':b+'/PROMPT.md','prompt_text':PROMPT,'provenance':b+'/PROVENANCE.json','qa':b+'/QA.json','guide':b+'/README.md','titles':TITLES,'notes':['架空の運用例。人名・会社・実測値なし。期限は相対案、状態は説明用。']*6,'method':'原典present.py briefのOperating Grid候補/readabilityをoutlineへ継承。原典既定PptxGenJS builder・render-plan・role-layout/template modulesでnative flow/timeline/table/comparison生成。PowerPoint16 PNG/PDF実描画。','sample_notice':'架空の社内運用。Python data pipelineは未整備、原典既定Nodeのnative要素で生成。','pages':[b+f'/render/slide-{i:02}.png' for i in range(1,7)]}
    dump(ROOT/'data/sol-presentation-skill-repository-examples.json',[ex]);dump(ROOT/'data/sol-presentation-skill-repository-guides.json',[{'repository':REPO,'summary_ja':'原典のoutline/Operating Grid/role contractsを通してnative引継ぎ図解と表を作る。','example_ids':['presentation-skill-showcase'],'upstream_commit':PIN,'license':'MIT','license_paths':[b+'/LICENSE'],'skill_paths':['skill-forks/presentation-skill-ja/SKILL.md'],'production_status':'light_check_complete','requirements':['Node.js / PptxGenJS4.0.1 / jszip3.10.1','Microsoft PowerPoint16 for PNG/PDF','Shippori Mincho / BIZ UDPGothic / Manrope (OFL)'],'commands':['npm install','node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops','powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render'],'guide':b+'/README.md','source_download':ex['source_download'],'fork_download':ex['fork_download'],'limitations':['架空の運用・期限相対案・実績なし','Full Python scientific data pipeline未整備。原典既定Node routeのみ実行','全ページ詳細目視・独立review・包括finalize/構造監査・ZIP再実行なし']}]);package()

def package():
    for folder,name in [(CASE,'presentation-skill-example-ja.zip'),(FORK,'presentation-skill-ja.zip')]:
        with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as z:
            for p in folder.rglob('*'):
                if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.build']) and p.suffix!='.pyc':z.write(p,folder.name+'/'+p.relative_to(folder).as_posix())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--node');ap.add_argument('--finish',action='store_true');args=ap.parse_args()
    if args.finish:finish()
    else:
        if not args.node:ap.error('--node required')
        if SCRIPT.parent.name=='tools':prepare()
        execute(args.node)
