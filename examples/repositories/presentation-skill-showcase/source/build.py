"""Author supported outline JSON and invoke siril9's original native renderer.
No one-off PPTX generator, generated-PPTX patch, host SDK, or image fallback.
"""
from pathlib import Path
import argparse,difflib,hashlib,json,os,shutil,stat,subprocess,sys,zipfile

SCRIPT=Path(__file__).resolve();ROOT=SCRIPT.parents[1]
CASE=ROOT/'examples/repositories/presentation-skill-showcase' if SCRIPT.parent.name=='tools' else SCRIPT.parent.parent
FORK=ROOT/'skill-forks/presentation-skill-ja'
PIN='efd899c5ddf866af2ce0001c4c9340af775d4d55';REPO='siril9/presentation-skill'
TITLES=['引き継ぎメモを一枚にまとめる','情報・担当・確認をそろえる','引き継ぎは、順番を決める','期限と状態を、一枚に並べる','次に動く条件を、明らかに','次の担当が、動ける状態まで。']
PROMPT='''日本語6枚「引き継ぎメモを一枚にまとめる」を制作してください。
架空の社内運用。必要情報・担当・確認の関係、引継ぎ順、期限と状態のnative表、次に動く条件を原典native要素で示す。
siril9/presentation-skillのoriginal outline schema、Operating Grid grammar、render-plan/role-layout contracts、既定PptxGenJS生成器を実際に使用する。
大きく短い見出し、明暗の切替、図解と余白。6枚すべてを角丸カード格子にしない。Shippori明朝の見出し、BIZ UDPGothicの本文、Manropeの番号・英数字を役割別に使う。
人名・会社名・実績値を作らず、送り手・次の担当・確認役という仮の役割、相対期限・仮の状態例として明記。
原典必須engineを省略せず、汎用rendererへのラベル貼りや生成済みPPTXの手修正をしない。artifact-toolホストSDKは使わない。
原典finalizeの検査結果と全6枚の実描画を確認し、禁則、見出しの重なり、仮ラベル、文字色の不具合をsourceで修正して再生成する。独立レビューと修正を繰り返し、実施した工程と未実施を区別して記録する。
PPTX/PNG/PDF、原稿/入力/依頼、再生成コード、未変更原本/局所差分、短い日本語SKILL、SOURCE/許諾/実TTF/OFL、制作ZIPとfork ZIPを完成させる。'''
# Production history: the original author stays recorded; the repair is added, not substituted.
AUTHORING_MODEL='gpt-6.1-sol';REPAIR_MODEL='claude-opus-5-5'
REPAIR_SCOPE=['slide 1 title: two 7-glyph lines, no punctuation-only wrapped line',
              'operations-grid content header: titleTop >= 0.34in below the 0.08-0.19in top bars (addDarkTitleBar)',
              'slide 6 section: Japanese kicker, stage values and stage_labels instead of CYCLE/CONTROL placeholders (renderContractStage)',
              'renderContractStage text ink and section footer >= 4.5:1 on the actual stage background']
REVIEW_MODE='independent_review_correction_loop'
# Filled only from real reviewer receipts; the generator never invents these results.
REVIEW_KEYS=['representative_page_opened','whole_deck_detailed_review','independent_review','structure_audit','zip_reexecution','full_finalize_gate_run']

def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def udiff(old,new,fromfile,tofile):return ''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=fromfile,tofile=tofile))

def outline(brief):
    chosen=brief['route_candidates'][0]
    style={'style_preset':chosen['style_preset'],'composition_grammar':chosen['grammar_id'],'style_seed':'ja-handoff-six-pages','font_pair':'editorial_serif_v1','visual_density':'medium','emoji_mode':'none','footer_mode':'source-line','footer_page_numbers':True,'header_variant':'plain','title_motif':'none','comparison_mode':'open-columns','table_treatment':'compact-ledger','readability_contract':brief['outline_contract']['deck_style']['readability_contract']}
    # Role/variant are the original schema's structures, not arbitrary coordinates.
    pages=[
      # Two 7-glyph lines fit the title role headline width without a lone '、' line.
      {'type':'title','role':'title','theme':'dark','title':'引き継ぎメモを\n一枚にまとめる','subtitle':'必要情報・担当・確認を、一枚にそろえる。','notes':'架空の社内運用を説明する6枚。実際の引継ぎメモを一枚に整える例。実在の会社・社員・実測値ではない。'},
      {'type':'content','role':'evidence','variant':'flow','visual_intent':'flow','slide_intent':'components','title':'情報・担当・確認をそろえる','subtitle':'三つがそろって、次の担当が判断できる。','flow_layout':'bands','flow_steps':[{'title':'必要情報','detail':'目的・資料の場所・完了条件'},{'title':'担当','detail':'送り手・次の担当・確認役'},{'title':'確認','detail':'受け取った内容と期限を合わせる'}],'summary_callout':'資料だけを渡さず、「誰が何を確認するか」まで書く。','caption':'関係を整理した仮想例。実際の担当分担ではありません。'},
      {'type':'content','role':'evidence','variant':'timeline','slide_intent':'handoff-order','title':'引き継ぎは、順番を決める','subtitle':'渡す前に、受け手と同じ認識をつくる。','timeline_mode':'open-events','milestones':[{'label':'01 WRITE','title':'書く','body':'目的・資料\n期限を一枚へ'},{'label':'02 MATCH','title':'合わせる','body':'内容を\n読み返す'},{'label':'03 CONFIRM','title':'確認する','body':'不明点を\n送り手へ'},{'label':'04 HANDOFF','title':'渡す','body':'確認後に\n担当を変更'}],'caption':'順序を説明する仮の運用案。実際の承認手続ではありません。'},
      {'type':'content','role':'table','variant':'table','slide_intent':'one-page-register','title':'期限と状態を、一枚に並べる','subtitle':'空欄を残さず、次の行動も一緒に書く。','table_treatment':'compact-ledger','table':{'headers':['項目','担当','期限（仮）','状態例','次に動く条件'],'rows':[['必要資料','送り手','前日','準備済み','保存先を確認'],['手順の確認','次の担当','開始前','確認待ち','不明点を解消'],['担当の変更','確認役','開始前','未実施','確認記録を残す'],['作業の開始','次の担当','当日','未着手','担当変更を確認']],'column_weights':[1.5,1.1,1.2,1.2,2.2],'caption':'すべて架空の記入例。期限は相対的な仮案、状態は説明用です。'},'notes':'このnative表が引継ぎメモの一枚の例。実在案件の進捗報告ではない。'},
      {'type':'content','role':'comparison','variant':'comparison-2col','slide_intent':'action-conditions','title':'次に動く条件を、明らかに','subtitle':'判断に必要な情報を、着手前に確かめる。','left':{'title':'着手できる','bullets':['目的が一文で分かる','資料の保存先がある','期限と担当を記載','確認記録が残っている']},'right':{'title':'送り手へ戻す','bullets':['資料が見つからない','期限が空欄','担当が重複・未定','完了条件が曖昧']},'verdict':'不明点を推測で埋めず、確認してから担当を切り替える。'},
      # cycle/control are the canonical section-operating-cycle slot IDs; stage_labels
      # only replaces their visible labels (see renderContractStage adaptation).
      {'type':'section','role':'section','theme':'dark','section_number':'06','kicker':'最終確認','title':'次の担当が、\n動ける状態まで。','subtitle':'資料・期限・着手条件を、短い一枚に。','cycle':'担当変更前','control':'記録を確認','stage_labels':{'cycle':'確認時点','control':'着手条件'},'notes':'企画上の目標。運用効果を測定した結果ではない。'},
    ]
    for i,s in enumerate(pages):s.update(slide_id=f'handoff-{i+1:02}',footer='仮想の社内運用 / 人名・会社・実績値は使用していません')
    return {'title':TITLES[0],'subtitle':'架空の社内運用を図と表で説明する6枚','document_metadata':{'author':'Presentation Team','company':''},'deck_style':style,'metadata':{'synthetic':True,'external_assets':False,'authoring_model':AUTHORING_MODEL,'repair_authoring_model':REPAIR_MODEL,'repair_scope':REPAIR_SCOPE,'chosen_original_route':chosen['grammar_id'],'original_review_mode':'user_requested_minimal (superseded)','review':REVIEW_MODE,'python_data_pipeline':'not used; original default Node renderer selected'},'compliance':{'require_attribution':False,'auto_image_sources':False},'slides':pages}

# --- Scoped legibility adaptation of the original slides.js -------------------
# Each edit must match exactly once inside its own original function; a miss is
# an error, never a silent no-op.

TITLE_TOP_OLD='''  const titleTop = v2 && headerMode !== 'bar'
    && compositionGrammar(preset, slideData) === 'editorial-spread' ? 0.26 : 0;
'''
TITLE_TOP_NEW='''  // Studio Yebisu local adaptation (operations-grid only): the Operating Grid
  // frame paints its top bars from y=0.08in to y=0.19in. Start the measured
  // header at the grammar's 0.34in top inset; headerMetrics then moves the body.
  const headerGrammar = compositionGrammar(preset, slideData);
  const operationsGridTitleTop = headerGrammar === 'operations-grid' && headerMode !== 'bar'
    ? Math.max(0.34, grammarFrameContract(preset, slideData).top)
    : 0;
  const titleTop = v2 && headerMode !== 'bar'
    && headerGrammar === 'editorial-spread' ? 0.26 : operationsGridTitleTop;
'''

STAGE_INK_OLD='''  const muted = dark
    ? firstReadableColor(background, [preset.text_muted, 'CBD5E1', 'FFFFFF'], 3.0)
    : cleanHex(preset.text_muted, '64748B');
  const accent = cleanHex(preset.accent_primary, '1493A4');
  const secondary = cleanHex(preset.accent_secondary, accent);
'''
STAGE_INK_NEW='''  // Studio Yebisu local adaptation: stage text must reach 4.5:1 on the actual
  // stage background. Original accent/secondary remain decorative strokes;
  // text uses the first readable tint (dark) or shade (light) of the same hue.
  const muted = dark
    ? firstReadableColor(background, [preset.text_muted, 'CBD5E1', 'FFFFFF'], 4.5)
    : firstReadableColor(background, [preset.text_muted, '64748B', text], 4.5);
  const accent = cleanHex(preset.accent_primary, '1493A4');
  const secondary = cleanHex(preset.accent_secondary, accent);
  const stageInkMix = (color, amount) => {
    const target = dark ? 255 : 0;
    return [0, 2, 4].map((start) => {
      const channel = parseInt(color.slice(start, start + 2), 16);
      return Math.round(channel + (target - channel) * amount).toString(16).padStart(2, '0');
    }).join('').toUpperCase();
  };
  const readableStageInk = (color) => firstReadableColor(
    background,
    [color, stageInkMix(color, 0.45), stageInkMix(color, 0.65), text],
    4.5,
  );
  const accentInk = readableStageInk(accent);
  const secondaryInk = readableStageInk(secondary);
  // Optional visible labels per canonical slot ID; the slot name stays the fallback.
  const stageLabels = slideData.stage_labels && typeof slideData.stage_labels === 'object'
    ? slideData.stage_labels
    : {};
'''
STAGE_EDITS=[
    (STAGE_INK_OLD,STAGE_INK_NEW),
    ('''    color: accent,
    charSpacing: 1.1,
''','''    color: accentInk,
    charSpacing: 1.1,
'''),
    ('''    const label = name.replace(/_/g, ' ').toUpperCase();
''','''    const label = safeText(stageLabels[name]) || name.replace(/_/g, ' ').toUpperCase();
'''),
    ('''      fontSize: valueFont,
      bold: true,
      color: index % 2 ? secondary : accent,
''','''      fontSize: valueFont,
      bold: true,
      color: index % 2 ? secondaryInk : accentInk,
'''),
    ('''  if (hasFooterChrome(slideData, preset)) {
    addFooter(slide, preset, slideData);
  } else {
''','''  if (hasFooterChrome(slideData, preset)) {
    addFooter(slide, preset, slideData, { dark, background });
  } else {
'''),
]

def patch_function(source,start_marker,end_marker,edits,label):
    """Apply exact edits only between one function marker and the end marker."""
    if source.count(start_marker)!=1:raise RuntimeError(f'{label}: function marker found {source.count(start_marker)} times')
    start=source.index(start_marker);end=source.find(end_marker,start+len(start_marker))
    if end<0:raise RuntimeError(f'{label}: end marker not found after function marker')
    body=source[start:end]
    for old,new in edits:
        count=body.count(old)
        if count!=1:raise RuntimeError(f'{label}: expected exactly one original match, found {count}:\n{old}')
        body=body.replace(old,new,1)
    return source[:start]+body+source[end:]

def legibility_adaptation(slides):
    slides=patch_function(slides,'function addDarkTitleBar(slide, preset, title, subtitle, slideData = {}) {','\nfunction ',[(TITLE_TOP_OLD,TITLE_TOP_NEW)],'addDarkTitleBar titleTop')
    return patch_function(slides,'function renderContractStage(slide, slideData, preset, contract, kind) {','function renderTitle(pptx, slide, slideData, preset) {',STAGE_EDITS,'renderContractStage')

def prepare():
    up=ROOT/'.build/actual-upstreams/siril9__presentation-skill'
    # Full original template modules and canonical role contracts are mandatory.
    for rel in ['LICENSE','SKILL.md','package.json','scripts/build_deck_pptxgenjs.js','scripts/present.py','scripts/runtime_doctor.py','scripts/render_cache.py','scripts/render_slides.py','scripts/requirements-runtime.txt','references/outline_schema.md','references/renderer_role_contracts_v2.json','references/pptxgenjs.md','templates/pptxgenjs/README.md']:
        out=CASE/'upstream'/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(up/rel,out)
    shutil.copytree(up/'templates/pptxgenjs',CASE/'upstream/templates/pptxgenjs',dirs_exist_ok=True)
    shutil.copytree(up/'schemas',CASE/'upstream/schemas',dirs_exist_ok=True)
    for name in ['scripts','templates','references','schemas']:(CASE/'runtime'/name).mkdir(parents=True,exist_ok=True)
    shutil.copytree(up/'templates/pptxgenjs',CASE/'runtime/templates/pptxgenjs',dirs_exist_ok=True)
    shutil.copytree(up/'schemas',CASE/'runtime/schemas',dirs_exist_ok=True)
    shutil.copy2(up/'references/renderer_role_contracts_v2.json',CASE/'runtime/references/renderer_role_contracts_v2.json')
    shutil.copy2(up/'LICENSE',CASE/'LICENSE');shutil.copy2(up/'LICENSE',CASE/'runtime/LICENSE')
    renderer=(up/'scripts/build_deck_pptxgenjs.js').read_text(encoding='utf-8');original=renderer
    font_pair_original="  editorial_serif_v1: {\n    font_heading: 'Georgia',\n    font_body: 'Calibri',\n  },"
    font_pair_japanese="  editorial_serif_v1: {\n    font_heading: 'Shippori Mincho',\n    font_body: 'BIZ UDPGothic',\n    font_number: 'Manrope',\n    font_table_header: 'BIZ UDPGothic',\n  },"
    if renderer.count(font_pair_original)!=1:raise RuntimeError('Original editorial_serif_v1 font mapping changed')
    renderer=renderer.replace(font_pair_original,font_pair_japanese,1)
    renderer=renderer.replace('preset.font_caption = fontPair.font_body;','preset.font_caption = fontPair.font_body;\n    preset.font_number = fontPair.font_number || fontPair.font_body;\n    preset.font_table_header = fontPair.font_table_header || fontPair.font_body;',1)
    write(CASE/'runtime/scripts/build_deck_pptxgenjs.js',renderer)
    write(CASE/'source/font-pair.diff',udiff(original,renderer,'upstream/scripts/build_deck_pptxgenjs.js','runtime/scripts/build_deck_pptxgenjs.js'))
    slides=(up/'templates/pptxgenjs/slides.js').read_text(encoding='utf-8');oldslides=slides
    slides=slides.replace("fontFace: preset.font_body,\n        fontSize: roleMetadataFont(preset, 8.4)","fontFace: preset.font_number || preset.font_body,\n        fontSize: roleMetadataFont(preset, 8.4)")
    slides=slides.replace('fontSize: captionFont, fontFace: preset.font_heading, bold: true,','fontSize: captionFont, fontFace: preset.font_number || preset.font_heading, bold: true,')
    slides=slides.replace('fontSize: labelFont, color, bold: true, objectName: `metadata:timeline-label-${index}`','fontSize: labelFont, fontFace: preset.font_number || preset.font_body, color, bold: true, objectName: `metadata:timeline-label-${index}`')
    slides=slides.replace('bold: true,\n    fontFace: preset.font_title,\n    fontSize: headerFont,','bold: true,\n    fontFace: preset.font_table_header || preset.font_title,\n    fontSize: headerFont,',1)
    slides=slides.replace("'TABLE INDEX'","'引き継ぎメモ'").replace('${table.rows.length} rows','${table.rows.length}項目')
    write(CASE/'source/numeric-font.diff',udiff(oldslides,slides,'upstream/templates/pptxgenjs/slides.js','runtime/templates/pptxgenjs/slides.js'))
    # Diffs compose: upstream -> numeric-font.diff -> legibility.diff -> runtime.
    fontslides=slides;slides=legibility_adaptation(slides)
    # Codex follow-up: avoid repeating five table headers above the real native table.
    before_table=slides
    old_detail="    const detail = `${table.rows.length}項目${horizontal ? ' | ' : '\\n'}${table.headers.map((text) => safeText(text)).join(horizontal ? ' | ' : '\\n')}`;"
    new_detail="    const detail = `${table.rows.length}件の記入例`;"
    if slides.count(old_detail)!=1:raise RuntimeError('Measured table index detail changed')
    slides=slides.replace(old_detail,new_detail,1)
    old_caption="      italic: true, color: firstReadableColor(preset.bg, [preset.text_muted, preset.text]), wrap: true,"
    if slides.count(old_caption)!=1:raise RuntimeError('Measured table caption changed')
    slides=slides.replace(old_caption,old_caption.replace('italic: true','italic: false'),1)
    write(CASE/'source/table-legibility.diff',udiff(before_table,slides,'runtime/templates/pptxgenjs/slides.js (after legibility.diff)','runtime/templates/pptxgenjs/slides.js'))
    write(CASE/'runtime/templates/pptxgenjs/slides.js',slides)
    write(CASE/'source/legibility.diff',udiff(fontslides,before_table,'runtime/templates/pptxgenjs/slides.js (after numeric-font.diff)','runtime/templates/pptxgenjs/slides.js'))
    # Windows Python3.12 exposes legacy st_ctime differently through fstat/stat.
    # Compare explicit creation time there, retaining dev/inode/size/mtime and
    # before/after/path identity checks. No QA threshold or content rule changes.
    cache_original=(up/'scripts/render_cache.py').read_text(encoding='utf-8')
    old_signature='        return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)'
    new_signature='''        creation_ns = getattr(stat, "st_birthtime_ns", stat.st_ctime_ns) if os.name == "nt" else stat.st_ctime_ns
        return (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, creation_ns)'''
    if cache_original.count(old_signature)!=1:raise RuntimeError('Original render_cache hash signature changed')
    cache_adapter=cache_original.replace(old_signature,new_signature,1)
    write(CASE/'runtime/scripts/render_cache.py',cache_adapter)
    write(CASE/'source/windows-hash-guard.diff',udiff(cache_original,cache_adapter,'upstream/scripts/render_cache.py','runtime/scripts/render_cache.py'))
    # Native pdfinfo can put CP932 Japanese PDF metadata in stdout on Windows.
    # Decode diagnostics tolerantly; return codes, hashes, image/page counts and
    # every QA rule remain unchanged. Pages: remains the same ASCII field.
    render_original=(up/'scripts/render_slides.py').read_text(encoding='utf-8')
    if render_original.count('text=True')!=4:raise RuntimeError('Original native render capture sites changed')
    render_adapter=render_original.replace('text=True','text=True, encoding="utf-8", errors="replace"')
    write(CASE/'runtime/scripts/render_slides.py',render_adapter)
    write(CASE/'source/windows-native-output.diff',udiff(render_original,render_adapter,'upstream/scripts/render_slides.py','runtime/scripts/render_slides.py'))
    brief=json.loads((CASE/'input/agent-brief.json').read_text(encoding='utf-8'));source_outline=outline(brief)
    dump(CASE/'input/outline.json',source_outline)
    dump(CASE/'input/design-decisions.json',{'chosen_candidate':brief['route_candidates'][0],'source_style':'lavender-ops','source_grammar':'operations-grid','geometry':'original supported role/variant/flow/table systems; no arbitrary coordinates','font_roles':{'heading':'Shippori Mincho','body':'BIZ UDPGothic','native flow indexes / footer page numbers':'Manrope'},'changes':['local font_pair adapter','native numeric metadata font mapping','operations-grid content header top inset 0.34in (source/legibility.diff)','renderContractStage stage_labels, 4.5:1 text ink and section footer background (source/legibility.diff)','Codex follow-up: concise table count, upright Japanese caption (source/table-legibility.diff)'],'plan':['dark title','native bands for required relations','native open timeline','native status table','comparison conditions','dark section conclusion'],'images':'not required: official native flow_steps and native table route','python_doctor':'QA.json records the current scientific-data runtime limitations; raw diagnostics are private','authoring_model':AUTHORING_MODEL,'repair_authoring_model':REPAIR_MODEL,'repair_scope':REPAIR_SCOPE,'review':'Independent review and correction loop required by the current user; results are recorded in QA.json only after real execution'})
    write(CASE/'input/BRIEF.md',f'# {TITLES[0]}\n\n引継ぎメモを一枚に整理する考え方を説明する6枚の教材。架空の社内運用で、人名・会社名・実績値は使用しない。必要情報・担当・確認、引継ぎ順、期限と状態、次の着手条件を示す。期限は相対的な仮案、状態は説明用の例。\n')
    write(CASE/'PROMPT.md',PROMPT+'\n')
    # Visible line breaks belong to the slide; Markdown headings stay on one line.
    write(CASE/'MANUSCRIPT.md','\n\n'.join(f'## {i+1}. {s["title"].replace(chr(10),"")}\n\n'+str(s.get('subtitle',''))+'\n\n'+str(s.get('notes','仮想の社内運用例。')) for i,s in enumerate(source_outline['slides']))+'\n')
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
    r=subprocess.run(cmd,cwd=CASE/'runtime',env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');write(CASE/'.private/build.log',r.stdout+r.stderr)
    if r.returncode:raise RuntimeError((r.stdout+r.stderr)[-6500:])
    dump(CASE/'source/BUILD.json',{'exit_code':r.returncode,'original_node_builder':'runtime/scripts/build_deck_pptxgenjs.js','template_modules':'runtime/templates/pptxgenjs','canonical_role_contracts':'runtime/references/renderer_role_contracts_v2.json','local_diffs':['source/font-pair.diff','source/numeric-font.diff','source/legibility.diff','source/table-legibility.diff','source/windows-hash-guard.diff','source/windows-native-output.diff'],'input':'input/outline.json','preset':'lavender-ops','grammar':'operations-grid','node_dependencies':deps,'output':'deck.pptx','render_plan_diagnostics':'private runtime diagnostics; not distributed','images_used':False,'artifact_tool_used':False,'one_off_generator':False,'full_python_data_pipeline_ready':False,'python_doctor':'QA.json runtime_doctor'})
    print('Original outline/render-plan/role-contract/PptxGenJS build succeeded.')

def qa_record():
    """Generator-known facts plus reviewer receipts; review results stay None until recorded."""
    path=CASE/'QA.json';previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    # Only receipts written under the current review mode are carried over.
    carry=previous.get('review_mode')==REVIEW_MODE
    build=CASE/'source/BUILD.json'
    built=json.loads(build.read_text(encoding='utf-8')).get('exit_code')==0 if build.exists() else False
    return {'status':(previous.get('status') if carry else None) or 'pending_independent_review','original_node_generation_success':built,'page_count':6,'powerpoint_render_success':(CASE/'render/deck.pdf').exists(),**{k:(previous.get(k) if carry else None) for k in REVIEW_KEYS},'review_receipts':previous.get('review_receipts') if carry else None,'python_doctor_passed':False,'node_pinned_requirements_checked':True,'review_mode':REVIEW_MODE,'authoring_model':AUTHORING_MODEL,'repair_authoring_model':REPAIR_MODEL}

def finish(write_catalog=True):
    write(CASE/'SKILL.md',f'''---
name: presentation-skill-ja
description: 原典outline/role-contract/native PptxGenJSで日本語引継ぎ資料を作る。
---

# 日本語Presentation Skill

siril9/presentation-skill `{PIN}` / MIT。原典の既定rendererは `scripts/build_deck_pptxgenjs.js`。汎用generatorに名前だけ貼らず、outline schema、render-plan、canonical role-contract、templateを実行する。

1. 原典present.py briefで内容・style/grammarを選び、そのreadability contractと候補をoutlineへ引き継ぐ。今回の候補はlavender-ops / operations-grid。入力はsourceであり、生成PPTXや画像を直接patchしない。
2. 原典schemaのnative flow_steps、timeline、table、comparisonを使う。図の内容を画像へ黙って代替しない。画像が必要な内容では原典asset pipelineを別途整える。
3. 短い日本語見出し・native図表・明暗・余白。表紙見出しは役割幅に収まる短い行で明示改行し、句読点だけの行を作らない。font_pairの局所adapterだけでShippori / BIZ UDPGothic / Manropeを役割別に対応し、差分を保存。字体は公式TTF/OFLのみ。
4. 可読性の不具合はsourceで直す。Operating Gridの上端barと見出しを離す、section補助枠にCYCLE/CONTROLなどの仮ラベルを残さず日本語の値とstage_labelsを入れる、文字色は実際の背景に対し4.5:1以上。template変更は対象関数内に限定し `source/legibility.diff` に残す。
5. 原典Node engineをPptxGenJS4.0.1/jszip3.10.1で実行。Python data/asset pipelineのdoctor不足はログへ記録し、整備済みと称しない。この作例は原典既定Nodeのnative要素だけで完成する。
6. PowerPoint16でPNG/PDFを描画。Application.Quitは禁止、自deckだけClose。全ページを目視し、独立reviewの指摘はoutline/template adapterへ戻して再生成する。原典finalizeなどの確認は実行後に結果を `QA.json` へ記録し、記録前に合格と書かない。
7. PPTX/PNG/PDF、JSON/原稿/依頼/再生成コード/未変更原本/局所差分/許諾/日本語ガイドを渡す。人名・会社・実績を捏造しない。

## quick_validate

`node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops` を実行し、PowerPointで6枚を描画して全ページを確認する。
''')
    write(CASE/'README.md',f'''# {TITLES[0]}

架空の社内運用を説明する6枚。引継ぎメモそのものを一枚に整える方法を、関係・順番・表・判断条件に分けて説明します。人名・会社名・実測値を使用せず、期限は相対的な仮案、状態は説明用の例です。

## 使用した原典と編集範囲

[siril9/presentation-skill](https://github.com/siril9/presentation-skill/tree/{PIN}) / MIT / `{PIN}`。
原典 `present.py brief` で選んだ `lavender-ops / operations-grid` 候補とreadability contractをJSONへ引き継ぎ、原典 `build_deck_pptxgenjs.js` に入力します。原典のrender-plan、role-layout contracts、templates/pptxgenjsを実際に実行したnative PPTXです。Python-pptxの別generatorやホストartifact-tool SDKは使っていません。

`flow_steps` は原典schemaが対応するnative図解、timelineはnative図形、状態表はnative table、比較はnative文字/形状。PowerPoint内で本文・図形・線・表を直接編集できます。native chart/数式は使用していません。PDF/PNGは閲覧用です。原稿を直して再生成するなら `input/outline.json` を編集します。

原典のOperating Gridを一貫したdesign systemとして使い、暗い表紙・結論、関係のbands、開いたtimeline、表、判断条件の2列を選択。手書き座標や生成後PPTX修正を避けています。原典未変更原本は `upstream/`、字体roleと表の注記を日本語化したruntime差分は `source/font-pair.diff` と `source/numeric-font.diff`。

可読性の修正もsource側だけで行い、`source/legibility.diff` に記録しています（`source/numeric-font.diff` 適用後のslides.jsとの差分）。operations-gridの本文見出しを上端bar（0.08〜0.19in）から離して0.34inから開始し、本文も測定した見出し高さに合わせて下げます。`renderContractStage` 内だけで、section補助枠の表示ラベル（`stage_labels`、未指定時は原典のslot名）と、背景に対し4.5:1以上の文字色・footer色を選びます。紫と青緑の線は装飾として残します。表紙見出しは「引き継ぎメモを／一枚にまとめる」の2行に改めました。

原典が許可する `editorial_serif_v1`（serif見出しとsans本文）を日本語の対応書体へ割り当てています。独自のfont_pair列挙値は使いません。Windows Python3.12のctime差を明示的birthtimeで比較し、native pdfinfoの日本語診断を置換付きで読み取る互換修正を加えています。差分は `source/windows-hash-guard.diff` と `source/windows-native-output.diff`。file identity・size・mtime・前後比較、return code、ページ数、QA閾値は維持します。

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

原典Python doctorによる科学データ依存の不足とpin差は `QA.json` に記録します。原文ログは公開物に含めません。科学データ・asset依存一式の準備完了とは報告しません。native作例のfinalize結果は `qa/finalize/finalize_receipt.json` が正本です。今回の原典既定Node rendererのnative flow/table/comparisonには、それらのPython科学依存は不要です。画像や実データの解析を追加する場合は原典のpinned Python環境を整備してください。

確認は二層に分けて記録します。source確認は、`input/outline.json`、再生成コード、`source/*.diff` に上記の修正が入っていることです。実行確認は、原典Node builderでの再生成、PowerPoint16での6枚PNG/PDF描画、全ページ目視、独立review、原典finalizeです。現在の依頼では独立reviewと修正loopが必須です。実行確認の結果は実行後に `QA.json`、`source/BUILD.json`、`render/powerpoint-render.json` へ記録され、記録前の項目は未確認として扱います。包括QA合格やProduction採用とは、記録された結果が示すまで称しません。
''')
    for directory in ['upstream','runtime','source','input','fonts','dependencies']:shutil.copytree(CASE/directory,FORK/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.log','*.pptx','__pycache__','*.pyc'))
    for filename in ['SKILL.md','README.md','LICENSE','PROMPT.md','MANUSCRIPT.md','package.json']:shutil.copy2(CASE/filename,FORK/filename)
    qa=qa_record()
    meta={'repository':REPO,'commit':PIN,'license':'MIT','modified':True,'renderer':'original build_deck_pptxgenjs.js','grammar':'operations-grid','preset':'lavender-ops','editable_features':['text','shapes','tables'],'codex_followup_repair':{'author':'Codex','scope':'Measured table count-only index and upright Japanese caption','diff':'source/table-legibility.diff'},'local_changes':['editorial_serif_v1 Japanese font adapter','Manrope native numeric metadata mapping','operations-grid content header titleTop 0.34in (addDarkTitleBar)','renderContractStage stage_labels / 4.5:1 text ink / section footer on actual background'],'source':'input/outline.json','example':'examples/repositories/presentation-skill-showcase','full_python_data_pipeline_ready':False,'authoring_model':AUTHORING_MODEL,'repair_authoring_model':REPAIR_MODEL,'review':'Independent review and correction loop required; results only from QA.json receipts'}
    dump(CASE/'SOURCE.json',meta);dump(FORK/'SOURCE.json',meta)
    dump(CASE/'PROVENANCE.json',{'repository':REPO,'upstream_commit':PIN,'license':'MIT','route':'present.py brief -> original outline schema -> build_deck_pptxgenjs.js -> original render-plan/role-layout/template modules -> native PowerPoint','originals':{p.relative_to(CASE).as_posix():sha(p) for p in package_files(CASE/'upstream')},'source':'input/outline.json','style_decisions':'input/design-decisions.json','local_changes':'source/font-pair.diff, source/numeric-font.diff, source/legibility.diff, source/table-legibility.diff, source/windows-hash-guard.diff, source/windows-native-output.diff','authoring_model':AUTHORING_MODEL,'repair_authoring_model':REPAIR_MODEL,'repair_scope':REPAIR_SCOPE,'repair_record':'source/OPUS-F05-REPAIR.md','codex_followup_repair':{'author':'Codex','scope':'Measured table count-only index and upright Japanese caption','diff':'source/table-legibility.diff'},'node_dependencies':{'pptxgenjs':'4.0.1','jszip':'3.10.1'},'fonts':'fonts/SOURCE.json','font_files':{p.relative_to(CASE).as_posix():sha(p) for p in (CASE/'fonts').rglob('*.ttf')},'build_receipt':'source/BUILD.json','render_receipt':'render/powerpoint-render.json','qa_receipt':'QA.json','content_status':'hypothetical handoff operations, relative deadlines and example states','artifact_tool_used':False})
    dump(CASE/'QA.json',qa)
    images=''.join(f'<figure><img src="render/slide-{i+1:02}.png" alt="{tt}"><figcaption>{i+1}. {tt}</figcaption></figure>' for i,tt in enumerate(TITLES))
    write(CASE/'index.html','<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+TITLES[0]+'</title><style>body{margin:0;background:#f5f3ff;color:#2e1065;font-family:sans-serif}header,main{max-width:1200px;padding:24px;margin:auto}a{color:#6d28d9}figure{margin:0 0 30px}img{display:block;width:100%}figcaption{font-size:14px;padding-top:10px}</style><header><h1>'+TITLES[0]+'</h1><p>架空の社内運用 / 6枚 / native flow・table・timeline</p><a href="deck.pptx">PowerPoint</a> · <a href="render/deck.pdf">PDF</a> · <a href="README.md">日本語ガイド</a> · <a href="../../../downloads/presentation-skill-example-ja.zip">制作ZIP</a></header><main>'+images+'</main></html>')
    if write_catalog:
        b='examples/repositories/presentation-skill-showcase'
        ex={'id':'presentation-skill-showcase','title':TITLES[0],'use_case':'native図解・表で整える引継ぎの6枚教材','repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'presentation-skill-ja','page_count':6,'format':'pptx','preview_kind':'powerpoint-render','preview_notice':'原典outline/role contracts/PptxGenJSによるnative文字・形状・表。PowerPoint内で編集可能。','editability':'native_tables','editable_features':['text','shapes','tables'],'style':'原典lavender-ops / Operating Grid / 明暗・明朝・native flowと表','cover':b+'/render/slide-01.png','interior':b+'/render/slide-04.png','preview':b+'/index.html','artifact_download':b+'/deck.pptx','pdf_download':b+'/render/deck.pdf','source_download':'downloads/presentation-skill-example-ja.zip','fork_download':'downloads/presentation-skill-ja.zip','input':b+'/input/BRIEF.md','input_data':b+'/input/outline.json','prompt':b+'/PROMPT.md','prompt_text':PROMPT,'provenance':b+'/PROVENANCE.json','qa':b+'/QA.json','guide':b+'/README.md','titles':TITLES,'notes':['架空の運用例。人名・会社・実測値なし。期限は相対案、状態は説明用。']*6,'method':'原典present.py briefのOperating Grid候補/readabilityをoutlineへ継承。原典既定PptxGenJS builder・render-plan・role-layout/template modulesでnative flow/timeline/table/comparison生成。PowerPoint16 PNG/PDF実描画。','sample_notice':'架空の社内運用。Python data pipelineは未整備、原典既定Nodeのnative要素で生成。','pages':[b+f'/render/slide-{i:02}.png' for i in range(1,7)]}
        dump(ROOT/'data/sol-presentation-skill-repository-examples.json',[ex]);dump(ROOT/'data/sol-presentation-skill-repository-guides.json',[{'repository':REPO,'summary_ja':'原典のoutline/Operating Grid/role contractsを通してnative引継ぎ図解と表を作る。','example_ids':['presentation-skill-showcase'],'upstream_commit':PIN,'license':'MIT','license_paths':[b+'/LICENSE'],'skill_paths':['skill-forks/presentation-skill-ja/SKILL.md'],'production_status':qa['status'],'requirements':['Node.js / PptxGenJS4.0.1 / jszip3.10.1','Microsoft PowerPoint16 for PNG/PDF','Shippori Mincho / BIZ UDPGothic / Manrope (OFL)'],'commands':['npm install','node runtime/scripts/build_deck_pptxgenjs.js --outline input/outline.json --output deck.pptx --style-preset lavender-ops','powershell -File source/render_powerpoint.ps1 -PresentationPath deck.pptx -OutputDirectory render'],'guide':b+'/README.md','source_download':ex['source_download'],'fork_download':ex['fork_download'],'limitations':['架空の運用・期限相対案・実績なし','Full Python scientific data pipeline未整備。原典既定Node routeのみ実行','独立review・修正loop・原典finalizeの結果はQA.jsonの実行記録のみを根拠とする']}])
    package()

# --- Packaging ------------------------------------------------------------------
PACKAGE_EXCLUDED_DIRS={'node_modules','.private','.build','.git','__pycache__','logs','cache','.cache','venv','.venv'}

def is_link_or_junction(path):
    """True for symlinks and Windows junctions/reparse points (not followed when packaging)."""
    try:
        if path.is_symlink():return True
        is_junction=getattr(path,'is_junction',None)
        if is_junction and is_junction():return True
        return bool(getattr(os.lstat(path),'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except OSError:return True

def package_files(folder):
    """Yield regular files without descending into links, junctions or excluded build/private dirs."""
    for current,dirs,files in os.walk(folder,followlinks=False):
        here=Path(current)
        dirs[:]=sorted(d for d in dirs if d not in PACKAGE_EXCLUDED_DIRS and not is_link_or_junction(here/d))
        for name in sorted(files):
            path=here/name
            if path.suffix not in {'.pyc','.log'} and not is_link_or_junction(path):yield path

def package():
    for folder,name in [(CASE,'presentation-skill-example-ja.zip'),(FORK,'presentation-skill-ja.zip')]:
        target=ROOT/'downloads'/name;partial=target.with_name(name+'.partial');target.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(partial,'w',zipfile.ZIP_DEFLATED) as z:
            for p in package_files(folder):z.write(p,folder.name+'/'+p.relative_to(folder).as_posix())
        os.replace(partial,target)
    print('Packaged case and fork ZIPs.')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--node',help='Node.js executable for the original builder')
    ap.add_argument('--finish',action='store_true',help='write SKILL/README/SOURCE/PROVENANCE/QA, sync fork, rebuild ZIPs')
    ap.add_argument('--case-only',action='store_true',help='with --finish: skip the two ROOT/data catalog writes')
    ap.add_argument('--package-only',action='store_true',help='rebuild only the case and fork ZIPs (e.g. after real QA/provenance updates)')
    args=ap.parse_args()
    if args.case_only and not args.finish:ap.error('--case-only requires --finish')
    if args.package_only and args.finish:ap.error('--package-only cannot be combined with --finish')
    if args.package_only:package()
    elif args.finish:finish(write_catalog=not args.case_only)
    else:
        if not args.node:ap.error('--node required')
        if SCRIPT.parent.name=='tools':prepare()
        execute(args.node)
