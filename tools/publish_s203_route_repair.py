"""Publish the two actual native route/band repairs; no reviewer score is assigned."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,shutil,subprocess,sys,zipfile
import pymupdf
from pptx import Presentation
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/sebastian-203';FORK=ROOT/'skill-forks/sebastian-203-ja'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 prs=Presentation(CASE/'deck.pptx');assert len(prs.slides)==8
 stats=[]
 for n,s in enumerate(prs.slides):
  stats.append({'index':n,'native_shapes':len(s.shapes),'pictures':sum(x.shape_type==13 for x in s.shapes),'native_charts':sum(x.has_chart for x in s.shapes),'native_tables':sum(x.has_table for x in s.shapes),'texts':[x.text for x in s.shapes if x.has_text_frame and x.text.strip()]})
 assert all(x['pictures']==0 for x in stats)
 dump(CASE/'source/native-elements.json',{'pptx_sha256':sha(CASE/'deck.pptx'),'slides':stats})
 doc=pymupdf.open(CASE/'render/deck.pdf');fonts={'scope':'Actual PowerPoint-exported PDF font resources','pages':[{'index':n,'fonts':[{'base_font':f[3],'type':f[2]} for f in pg.get_fonts(full=True)]} for n,pg in enumerate(doc)]};doc.close();dump(CASE/'source/pdf-fonts.json',fonts)
 before=CASE/'.private/round4-before-route-fix'
 unchanged=[n for n in range(1,9) if sha(CASE/f'render/slide-{n:02}.png')==sha(before/f'render/slide-{n:02}.png')]
 assert unchanged==[1,4,5,6,7,8]
 proof={'author':'Codex','pptx_sha256':sha(CASE/'deck.pptx'),'changed_pages':[2,3],'changed_pages_fullsize_visually_checked':True,'unchanged_pages_pixel_identical_to_previously_checked':unchanged,'native_routes':['本を探す','集中席へ：活動域を通らない経路'],'limitations':['Conceptual routes, no scale or measured acoustic claim.','Independent current version review pending.']};dump(CASE/'source/route-repair.json',proof)
 scan=subprocess.run([sys.executable,'source/upstream/scripts/scan_ppt_text.py','deck.pptx'],cwd=CASE,capture_output=True,text=True);(CASE/'source/original-text-scan.txt').write_text(scan.stdout+scan.stderr,encoding='utf-8');scan.check_returncode()
 dump(CASE/'source/current-check-receipts.json',{'scope':'Current original text scanner execution','receipts':[{'command':['python','source/upstream/scripts/scan_ppt_text.py','deck.pptx'],'exit_code':scan.returncode,'log':'source/original-text-scan.txt','log_sha256':sha(CASE/'source/original-text-scan.txt')}]})
 retain=[]
 with zipfile.ZipFile(CASE/'source/academic-template.pptx') as a,zipfile.ZipFile(CASE/'deck.pptx') as b:
  for n in a.namelist():
   if n.startswith(('ppt/theme/','ppt/slideMasters/','ppt/slideLayouts/')):
    retain.append({'path':n,'byte_identical':a.read(n)==b.read(n)})
 assert all(x['byte_identical'] for x in retain);dump(CASE/'source/template-retention.json',{'source':'source/academic-template.pptx','source_sha256':sha(CASE/'source/academic-template.pptx'),'parts':retain,'all_retained':True})
 qa=load(CASE/'QA.json');qa.update(artifact_sha256=sha(CASE/'deck.pptx'),structure={k:sum(x[k] for x in stats) for k in ['native_shapes','pictures','native_charts','native_tables']},images=[{'page':n,'file':f'render/slide-{n:02}.png','sha256':sha(CASE/f'render/slide-{n:02}.png')} for n in range(1,9)],current_route_repair='source/route-repair.json',independent_current_version_review='pending')
 replay=CASE/'source/distribution-replay.json'
 if replay.exists() and load(replay).get('current_pptx_sha256')==sha(CASE/'deck.pptx'):qa['zip_replay']=load(replay)
 else:qa['zip_replay']={'status':'pending_current_route_repair','prior_version':'private preserved record'}
 dump(CASE/'QA.json',qa)
 prov=load(CASE/'PROVENANCE.json');prov['artifact_sha256']=sha(CASE/'deck.pptx');prov['repair']={'author':'Codex','source':'source/route-repair.json','method':'Original academic template and python-pptx authoring; two native-page corrections, original scan, all8 PowerPoint PDF; six unchanged PNGs exact to prior reviewed version.'};prov['current_distribution_replay']=qa['zip_replay'];dump(CASE/'PROVENANCE.json',prov)
 # Normalize the public render receipt; retain raw execution report privately.
 report=load(CASE/'render/powerpoint-render.json');report['source']='deck.pptx';dump(CASE/'render/powerpoint-render.json',report)
 rows=load(ROOT/'data/skill-effect-patches/repairs-native4.json');r=deepcopy(next(x for x in rows if x['case_id']=='sebastian-203'))
 r.update(input='論文・研究概要・文献レビューなどの元資料と、優先して使うPowerPointテンプレート。',output='学術テンプレートを引き継ぎ、出典・図の読み方・話者ノートを持つ編集可能なPPTXと確認記録。',font_download='downloads/fonts/bizudpgothic.zip',font_families=['BIZ UDPGothic'],preview_kind='powerpoint-render')
 r['how_to_use'][0]='研究概要・論文・レビューのうち実際に渡せる元資料と、優先するテンプレートを用意する。'
 r['how_to_use'][-1]='原典テンプレートで資料を生成し、禁止語スキャンと全頁の実描画で図・書体・注記を確認する。'
 titles=load(CASE/'input/data.json')['titles'];r['titles']=titles;r['notes']=load(CASE/'input/data.json')['notes'];r['pages']=[f'examples/repositories/sebastian-203/render/slide-{n:02}.png' for n in range(1,9)]
 for page in r['demonstration']['pages']:page['title']=titles[page['index']]
 r['demonstration']['pages'][0]['what_to_inspect']='一続きの3区分へ活動を並べ、下に音の希望を対応させる。下段で設計仮説と実測尺度の違いを示す。'
 r['demonstration']['pages'].append({'index':2,'label':'3ページ目','title':titles[2],'what_to_inspect':'白い「本を探す」と下の「集中席へ」を分ける。集中席への経路は会話の活動域を横切らない。縮尺のない概念図。','skill_rule':'原稿の経路と接続関係を図に残し、計画と実証済みの結果を区別する。','proof_path':'examples/repositories/sebastian-203/render/slide-03.png','proof_kind':'powerpoint-render'})
 r['demonstration']['source_proof_paths']=list(dict.fromkeys([*r['demonstration']['source_proof_paths'],'examples/repositories/sebastian-203/source/route-repair.json']))
 r['guide_patch']['steps']=r['how_to_use']
 patch=ROOT/'data/skill-effect-patches/zz-root-consistency.json';allrows=load(patch);dump(patch,[x for x in allrows if x['case_id']!='sebastian-203']+[r])
 for f in [CASE/'README.md',FORK/'SKILL.md',FORK/'README.md']:
  s=f.read_text(encoding='utf-8').replace('左の利用目的と右の席の希望、下段の「分類は設計仮説」を読む。',r['demonstration']['pages'][0]['what_to_inspect']);f.write_text(s,encoding='utf-8')
 excluded={'.private','.build','.git','node_modules','.venv','__pycache__'}
 for f in CASE.rglob('*'):
  if f.is_file() and not set(f.relative_to(CASE).parts)&excluded and f.suffix not in {'.log','.pyc'}:
   to=FORK/f.relative_to(CASE);to.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,to)
 source=load(FORK/'SOURCE.json');source['files']=[{'path':f.relative_to(FORK).as_posix(),'sha256':sha(f)} for f in sorted(FORK.rglob('*')) if f.is_file() and f.name!='SOURCE.json' and not set(f.relative_to(FORK).parts)&excluded and f.suffix not in {'.log','.pyc'}];dump(FORK/'SOURCE.json',source)
 for folder,name in [(CASE,'sebastian-203-example-ja.zip'),(FORK,'sebastian-203-ja.zip')]:
  with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as z:
   for f in sorted(folder.rglob('*')):
    if f.is_file() and not set(f.relative_to(folder).parts)&excluded and f.suffix not in {'.log','.pyc'}:z.write(f,folder.name+'/'+f.relative_to(folder).as_posix())
 print('S203: original scan0; native8pages/fonts/template retention and two labelled routes;2ZIPs synchronized; current independent review pending.')
if __name__=='__main__':main()
