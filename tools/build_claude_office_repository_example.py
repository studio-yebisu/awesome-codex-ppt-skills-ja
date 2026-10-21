"""Local-only trial of pinned tfriedel/claude-office-skills; no redistribution grant found."""
from pathlib import Path
import argparse, difflib, hashlib, html, json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/tfriedel__claude-office-skills'
OUT=ROOT/'.build/local-trials/claude-office'
DOC=OUT/'outputs/book-exchange'
REPO='tfriedel/claude-office-skills';COMMIT='d4241e43b60e8f96b0a80c3b1eb75fe8858437c0'
NODE=Path('C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
MODULES=NODE.parent.parent/'node_modules'
DATA={'title':'小さな図書交換会','subtitle':'1回だけ試す、地域の本の持ち寄り会','notice':'架空の企画案。人数・冊数・時間は計画値で、実績ではありません。','capacity':18,'books_per_person':2,'book_limit':36,'categories':['小説','暮らし','児童書'],'allocations':[16,10,10],'titles':['小さな図書交換会','本は36冊を上限に','90分の進行案','実施後に確かめること'],'notes':['地域の集会室で、少人数の図書交換会を1回試す架空の企画です。会場の確保や募集はまだ行っていません。人数、冊数、時間はいずれも計画値です。','参加者18人、1人2冊なら合計36冊です。小説16冊、暮らし10冊、児童書10冊は卓上の置き場所を考えるための仮配分で、実際の持込比率ではありません。','準備20分、交換50分、片付け20分の合計90分を計画します。担当者や会場条件に合わせて進行を見直します。会場使用の許可や募集案内は別途必要です。','実施後は交換できた冊数、待ち時間、準備と片付けの負担を記録します。人数を増やす前に、今回の運営で無理がなかったかを確認し、継続、条件変更、終了を決めます。'],'schedule':[['時間','内容','確認事項'],['0–20分','受付・陳列','持込は1人2冊まで'],['20–70分','本を選ぶ・交換','残った本も記録'],['70–90分','片付け・振り返り','持ち帰りを確認']]}
PROMPT='tfriedel/claude-office-skills固定原典のpublic/pptx工程とhtml2pptx-local.cjsで、架空の図書交換会の試行計画を日本語4枚にする。HTMLからnative文字・図形へ変換し、placeholderを用いて編集可能なグラフと表を追加する。実績でない計画値を明示し、日本語講稿を付ける。第三者AI APIは使わず、PowerPoint16で全頁確認。ライセンス許諾が見当たらないため、成果物・原典コードはローカルだけに保管する。'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def call(args,name,allow_fail=False):
 env=os.environ.copy();env['NODE_PATH']=str(MODULES);env['PYTHONIOENCODING']='utf-8'
 proc=subprocess.run(list(map(str,args)),cwd=OUT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
 log=OUT/'logs'/name
 if log.exists():
  idx=1
  while log.with_name(log.stem+'-'+str(idx)+log.suffix).exists():idx+=1
  log=log.with_name(log.stem+'-'+str(idx)+log.suffix)
 write(log,json.dumps(list(map(str,args)),ensure_ascii=False)+'\n'+proc.stdout+'\n'+proc.stderr)
 receipt={'argv':list(map(str,args)),'exit_code':proc.returncode,'log':log.relative_to(OUT).as_posix(),'log_sha256':sha(log)};save(log.with_suffix('.receipt.json'),receipt)
 if proc.returncode and not allow_fail:raise RuntimeError(proc.stdout+'\n'+proc.stderr)
 return proc.returncode

def setup():
 OUT.mkdir(parents=True,exist_ok=True);DOC.mkdir(parents=True,exist_ok=True)
 refs=['public/pptx/ooxml.md','README.md','CLAUDE.md','package.json','package-lock.json','html2pptx-local.cjs','public/pptx/SKILL.md','public/pptx/html2pptx.md','public/pptx/scripts/html2pptx.js','public/pptx/scripts/inventory.py','public/pptx/scripts/thumbnail.py']
 refs+= [f.relative_to(UP).as_posix()for f in (UP/'public/pptx/ooxml').rglob('*')if f.is_file()and f.suffix in ['.py','.xsd','.json']and '__pycache__'not in f.parts]
 for name in refs:
  dest=OUT/'source/upstream'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UP/name,dest)
 shutil.copy2(UP/'ACQUISITION.json',OUT/'source/ACQUISITION.json')
 save(OUT/'source/references.json',[{'path':n,'sha256':sha(UP/n),'url':f'https://github.com/{REPO}/blob/{COMMIT}/{n}'}for n in refs])
 save(OUT/'input/data.json',DATA);write(OUT/'PROMPT.txt',PROMPT+'\n')
 save(OUT/'LICENSE-REVIEW.json',{'repository':REPO,'commit':COMMIT,'license_files_found':[],'package_license_field':load(UP/'package.json').get('license'),'explicit_redistribution_grant_found':False,'status':'local_trial_only_no_distribution','observations':[{'source':'README.md','section':'Attribution','summary':'Author says most scripts/workflows come verbatim from Claude and offers removal at Anthropic request; this is not a stated redistribution grant.'},{'source':'README.md','section':'update 2026-04-01','summary':'Recommends official Anthropic skills for updates; this trial does not substitute that repository.'}],'distribution':'Generated PPTX/PNG/PDF, original code and derived runtime remain under ignored .build only. Public ATTEMPT is metadata only.','resume_publication_condition':'Confirm an explicit applicable redistribution permission/license for this pinned code and intended package before publishing artifacts or a skill fork.'})
 write(OUT/'DESIGN.md','紙の交換会に合わせ、生成り #F5F0E7、えんじ #6B283C、墨色 #302A2B。4ページ、主見出し42pt、ページ見出し30pt、本文18–20pt。グラフと表は編集可能。日本語文字を安定させるためYu Gothicを使用し、原典のweb-safe英字フォント指定からの局所変更として記録する。画像や装飾アイコンは使わない。')
 save(OUT/'source/local-changes.json',{'converter_changed':False,'original_converter_sha256':sha(UP/'html2pptx-local.cjs'),'changes':[{'kind':'content_font_exception','original':'html2pptx.md: web-safe fonts only','local':'Yu Gothic in authored HTML and chart/table fontFace','reason':'Japanese glyph coverage; verified in Chromium and PowerPoint on this Windows host.'},{'kind':'runtime_dependency_resolution','original':'npm install in repository','local':'NODE_PATH selects bundled installed Node dependencies; no original source modification','reason':'Reuse known local runtime without global installation.'},{'kind':'render_verification','original':'LibreOffice via thumbnail.py','local':'Microsoft PowerPoint16 PNG/PDF, then original thumbnail.create_grids','reason':'User requested actual PowerPoint rendering.'}]})

CSS='''html{background:#F5F0E7}body{width:720pt;height:405pt;margin:0;padding:0;display:flex;position:relative;background:#F5F0E7;color:#302A2B;font-family:'Yu Gothic',sans-serif}*{box-sizing:border-box}h1,h2,p{margin:0}h1{font-size:42pt;font-weight:700;line-height:1.3;color:#6B283C}h2{font-size:30pt;font-weight:700;line-height:1.4;color:#6B283C}p{font-size:19pt;line-height:1.5}.tag{font-size:14pt;color:#726768}.foot{font-size:12pt;color:#726768}.big{font-size:58pt;color:#6B283C;font-weight:700}.line{border-top:1pt solid #B5A5A7}'''
def box(x,y,w,h,body,cls=''):return f'<div class="{cls}" style="position:absolute;left:{x}pt;top:{y}pt;width:{w}pt;height:{h}pt">{body}</div>'
def sources():
 d=DATA;e=html.escape
 slides=[
 box(42,48,636,34,'<p class="tag">地域の集会室で試す、小さな企画</p>')+box(42,118,636,70,f'<h1>{e(d["title"])}</h1>')+box(44,203,620,50,f'<p>{e(d["subtitle"])}</p>')+box(44,310,630,45,'<p class="foot">架空の企画案。会場確保・募集は未実施。</p><p class="foot">人数・冊数・時間は計画値です。</p>'),
 box(38,32,644,50,'<h2>本は36冊を上限に</h2>')+box(40,112,230,92,'<p class="big">18人</p>')+box(42,203,232,76,'<p>1人2冊まで</p><p>合計36冊の計画</p>')+box(42,303,248,43,'<p class="foot">種類別の数は仮配分。</p><p class="foot">持込の実績ではありません。</p>')+'<div id="books-chart" class="placeholder" style="position:absolute;left:302pt;top:102pt;width:375pt;height:225pt;background:#ddd"></div>',
 box(38,32,644,50,'<h2>90分の進行案</h2>')+box(40,96,630,34,'<p>準備20分・交換50分・片付け20分</p>')+'<div id="schedule" class="placeholder" style="position:absolute;left:40pt;top:151pt;width:640pt;height:162pt;background:#ddd"></div>'+box(40,333,640,28,'<p class="foot">計画値。会場の条件と担当者に合わせて調整します。</p>'),
 box(38,32,644,50,'<h2>実施後に確かめること</h2>')+box(42,115,284,80,'<p><b>交換できた冊数</b></p><p>残った本も数える</p>')+box(383,115,292,80,'<p><b>運営の負担</b></p><p>待ち時間と片付けを記録</p>')+box(42,219,634,2,'','line')+box(42,249,628,64,'<p>参加者を増やす前に、</p><p>続ける・条件を変える・終了を決める。</p>')+box(42,337,630,26,'<p class="foot">開催結果はまだありません。1回の記録から判断します。</p>')
 ]
 for i,b in enumerate(slides,1):write(DOC/f'slide-{i:02}.html','<!doctype html><html lang="ja"><meta charset="utf-8"><style>'+CSS+'</style><body>'+b+'</body></html>')
 write(DOC/'build.cjs',r'''const fs=require('fs');const path=require('path');const pptxgen=require('pptxgenjs');
const html2pptx=require(process.argv[2]);const root=__dirname;const data=JSON.parse(fs.readFileSync(path.resolve(root,'../../input/data.json'),'utf8'));
(async()=>{const pptx=new pptxgen();pptx.defineLayout({name:'BOOKS',width:10,height:5.625});pptx.layout='BOOKS';pptx.author='八百万図AIツールボックス local trial';pptx.subject='Fictional planning example; no observed results';pptx.title=data.title;pptx.lang='ja-JP';pptx.theme={headFontFace:'Yu Gothic',bodyFontFace:'Yu Gothic',lang:'ja-JP'};
const result=[];for(let i=1;i<=4;i++){const file=path.join(root,`slide-${String(i).padStart(2,'0')}.html`);const {slide,placeholders}=await html2pptx(file,pptx,{tmpDir:path.join(root,'tmp')});
if(i===2){const p=placeholders.find(x=>x.id==='books-chart');slide.addChart(pptx.ChartType.bar,[{name:'仮配分',labels:data.categories,values:data.allocations}],{...p,barDir:'bar',showLegend:false,showTitle:false,showValue:true,showCatName:false,showCatAxisTitle:false,showValAxisTitle:true,valAxisTitle:'冊数（計画値）',valAxisMinVal:0,valAxisMaxVal:20,valAxisMajorUnit:5,catAxisLabelFontFace:'Yu Gothic',catAxisLabelFontSize:17,valAxisLabelFontFace:'Yu Gothic',valAxisLabelFontSize:12,valAxisTitleFontFace:'Yu Gothic',valAxisTitleFontSize:14,dataLabelColor:'6B283C',dataLabelFormatCode:'0',dataLabelPosition:'outEnd',dataLabelBkgrdColor:'F5F0E7',dataLabelFontSize:17,chartColors:['6B283C'],showCatName:false,showBorder:false,showMarker:false,showCatName:false,catAxisLineShow:false,valAxisLineShow:false,showTitle:false,chartArea:{fill:{color:'F5F0E7'}},plotArea:{fill:{color:'F5F0E7'}},showValue:true,gapSize:65});}
if(i===3){const p=placeholders.find(x=>x.id==='schedule');const rows=data.schedule.map((row,n)=>row.map(t=>({text:t,options:{bold:n===0,fill:{color:n===0?'6B283C':'F5F0E7'},color:n===0?'FFFFFF':'302A2B'}})));slide.addTable(rows,{...p,fontFace:'Yu Gothic',fontSize:17,border:{type:'solid',color:'CDBDBF',pt:0.7},margin:0.1,rowH:0.53,colW:[1.45,3.35,4.09],autoPage:false,valign:'middle'});}
slide.addNotes(data.notes[i-1]);result.push({page:i,html:path.basename(file),placeholders});}
await pptx.writeFile({fileName:path.join(root,'deck.pptx')});fs.writeFileSync(path.join(root,'conversion.json'),JSON.stringify({converter:process.argv[2],pages:result},null,2));console.log('Generated 4 pages via original html2pptx function');})().catch(e=>{console.error(e.stack||e);process.exit(1)});
''')

def normalize_package():
 # Normalize an absolute chart target to the relative form understood by original validator.
 from datetime import datetime
 unpacked=DOC/('unpacked-final-'+datetime.now().strftime('%Y%m%d%H%M%S'))
 raw=DOC/'html2pptx-before-normalization.pptx';shutil.copy2(DOC/'deck.pptx',raw)
 call([sys.executable,UP/'public/pptx/ooxml/scripts/unpack.py',raw,unpacked],'unpack-final.log')
 patch=[]
 for rel in (unpacked/'ppt/slides/_rels').glob('*.rels'):
  before=rel.read_text(encoding='utf-8');after=before.replace('Target="/ppt/charts/','Target="../charts/')
  if before!=after:
   patch.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='original/'+rel.relative_to(unpacked).as_posix(),tofile='local/'+rel.relative_to(unpacked).as_posix()));write(rel,after)
 write(OUT/'source/package-changes.diff',''.join(patch))
 call([sys.executable,UP/'public/pptx/ooxml/scripts/validate.py',unpacked,'--original',raw],'validate-final.log')
 call([sys.executable,UP/'public/pptx/ooxml/scripts/pack.py',unpacked,DOC/'deck.pptx'],'pack-final.log')
 changes=load(OUT/'source/local-changes.json');changes['package_changes']={'path':'source/package-changes.diff','reason':'Normalize absolute /ppt/charts target to ../charts target for original validator; chart content preserved. This alone did not fix the initial PowerPoint error.','raw_sha256':sha(raw),'final_sha256':sha(DOC/'deck.pptx')};changes['authoring_repair']='Table valign changed from invalid mid to documented middle; this resolved PowerPoint open failure.';save(OUT/'source/local-changes.json',changes)
def thumbnail():
 script=DOC/'make-thumbnails.py';write(script,"from pathlib import Path\nimport sys\nsys.path.insert(0,sys.argv[1])\nfrom thumbnail import create_grids\nr=Path(sys.argv[2])\ncreate_grids([r/f'slide-{i:02}.png' for i in range(1,5)],2,640,r/'thumbnails.jpg')\n")
 call([sys.executable,script,UP/'public/pptx/scripts',DOC/'render'],'thumbnail-original-library.log')

def report(reviewed=False):
 artifact=DOC/'deck.pptx';digest=sha(artifact)if artifact.exists()else None
 review=load(OUT/'visual-review.json')if(OUT/'visual-review.json').exists()else None
 if reviewed and(not review or review['artifact_sha256']!=digest or review['pages_reviewed']!=[1,2,3,4]):raise RuntimeError('Current all-page review required')
 commands=[load(p)for p in sorted((OUT/'logs').glob('*.receipt.json'))]
 for item in commands:
  if item['exit_code']!=0:
   if item['log']=='logs/validate-original.log':
    item['resolved_by_log']='logs/validate-final.log';item['resolution_reason']='Original validator rejected absolute /ppt/charts relationship; original unpack/validate/pack with relative chart target passed.'
   elif item['log']in ['logs/powerpoint-render.log','logs/render-relative-chart.log','logs/render-nochart.log']:
    item['resolved_by_log']='logs/render-final.log';item['resolution_reason']='Initial authored table used invalid valign mid. Changing to documented middle fixed PowerPoint open; chart relationship normalization alone did not. Final artifact retains both native chart and table.'
 p={'repository':REPO,'commit':COMMIT,'status':'local_trial_generated_and_reviewed'if reviewed else'local_trial_awaiting_review','distribution':'withheld_no_license_grant_found','input_sha256':sha(OUT/'input/data.json'),'artifact_sha256':digest,'source_refs':load(OUT/'source/references.json'),'commands_executed':commands,'local_changes':load(OUT/'source/local-changes.json'),'page_count':4,'external_ai_api':False,'artifact':'outputs/book-exchange/deck.pptx'}
 save(OUT/'PROVENANCE.json',p);save(OUT/'QA.json',{'status':'qa_complete'if reviewed else'awaiting_visual_review','artifact_sha256':digest,'page_count':4,'editability':'22 native text elements plus editable native chart and 4x3 table; no full-slide raster images','visual_review':review if reviewed else{'pages_reviewed':[],'method':'pending','result':'pending'},'distribution':'local_only','human_adoption':'pending'})
 summary={'repository':REPO,'upstream_commit':COMMIT,'status':p['status'],'generated_page_count':4 if artifact.exists()else 0,'distribution_status':'withheld_no_license_grant_found','artifact_distributed':False,'source_distributed':False,'local_trial':'.build/local-trials/claude-office','entrypoint':'html2pptx-local.cjs + public/pptx workflow','artifact_sha256':digest,'input_sha256':p['input_sha256'],'license_review':'No LICENSE or explicit redistribution grant found at pinned commit; README attribution is not a license.','resume_condition':'Explicit applicable redistribution permission required before publishing artifacts or fork. Local reproduction uses pinned source, Node dependencies and Windows PowerPoint.'}
 save(ROOT/'examples/repositories/claude-office/ATTEMPT.json',summary)
 save(ROOT/'data/claudeoffice-repository-examples.json',[])
 save(ROOT/'data/claudeoffice-repository-guides.json',[{'repository':REPO,'execution_type':'original_html2pptx_local_trial','execution_status':'local_trial_generated_not_packaged'if reviewed else p['status'],'production_status':'blocked','local_qa_complete':reviewed,'case_ids':[],'summary_ja':'固定原典html2pptxで日本語4頁をローカル生成。配布許諾未確認のため作例・原典コードは公開対象外。','requirements':['Node.js / pptxgenjs / playwright / sharp / Chromium','Microsoft PowerPoint 16（最終表示の確認）','Python仮想環境（原典の構造・サムネイル検査）'],'steps':['原典固定版と条件確認','日本語HTML→原典html2pptx-local.cjs','予約領域へ編集可能なグラフ・表と発表ノートを追加','PowerPoint全頁表示QA'],'commands':['python tools/build_claude_office_repository_example.py'],'source_refs':p['source_refs'],'limitations':['LICENSEや明示的な再配布許諾が見当たらないためローカル試行のみ。','READMEの公式版案内へ置き換えず、この固定版を実行。','Yu Gothicへ局所変更。別環境では再表示確認が必要。'],'attempt':'examples/repositories/claude-office/ATTEMPT.json','evidence':'examples/repositories/claude-office/ATTEMPT.json'}])
 write(OUT/'README.md','''# Claude Office 固定版のローカル試行

固定原典html2pptx-local.cjsとpublic/pptxのHTML工程を使う架空の図書交換会4頁。本文・図形・chart/tableはnative、4頁の日本語講稿付き。LICENSEや明示的な再配布許諾が見当たらないため、PPTX/PNG/PDFと原典・派生コードは.build/local-trials/claude-office内のみ。公開カタログには実行状態と原典hashのmetadataだけを渡す。

原典READMEは公式Anthropic版を推奨するが、この試行は指定固定版で実行。原典converter自体は無変更。補助コードの表valignをmidから原典ガイドのmiddleへ修正し、PowerPoint open失敗を解消。さらに原典validatorへ合わせてchart relationshipを絶対指定から相対指定へ正規化し、原典unpack/validate/packで検査した。差分はsource/package-changes.diff。日本語対応のYu Gothic、bundled Node依存、PowerPoint描画の差をsource/local-changes.jsonへ記録。失敗した実行はlogsに実終了コードで保持する。

再現: tools/acquire_repository.py tfriedel/claude-office-skillsで固定原典を取得し、依存付きPythonでtools/build_claude_office_repository_example.pyを実行。新出力は再レビューが必要。閲覧はoutputs/book-exchange/deck.pptx、PNG/PDFはrender。公開再開には当該コードと配布対象への明示的な許諾を確認する。
''')

def main():
 a=argparse.ArgumentParser();a.add_argument('--finalize-only',action='store_true');a.add_argument('--reviewed',action='store_true');v=a.parse_args()
 if not v.finalize_only:
  setup();sources();(DOC/'tmp').mkdir(exist_ok=True)
  call([NODE,DOC/'build.cjs',UP/'html2pptx-local.cjs'],'convert-original.log')
  normalize_package()
  call([sys.executable,UP/'public/pptx/scripts/inventory.py',DOC/'deck.pptx',DOC/'inventory.json'],'inventory.log')
  call(['pwsh','-NoProfile','-File',ROOT/'tools/render_powerpoint.ps1','-PresentationPath',DOC/'deck.pptx','-OutputDirectory',DOC/'render'],'powerpoint-render.log')
  thumbnail()
 report(v.reviewed)
if __name__=='__main__':main()
