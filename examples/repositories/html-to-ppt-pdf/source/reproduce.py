"""Run the unmodified converter and add Japanese speaker notes as explicit postprocessing."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,struct,subprocess,sys,zipfile,xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
CASE=Path(__file__).resolve().parents[1]
ADAPTER='<script id="conversion-static-navigation">/* Export-only: bypass the original 700ms input debounce after a navigation dot click. Original layout and content retained. */ document.querySelectorAll("#nav .dot").forEach((dot,i)=>{dot.onclick=()=>go(i,{force:true});});</script>'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def postprocess():
 notes=re.split(r'^## \d+\. ',(CASE/'input/port-town/NOTES.md').read_text('utf-8'),flags=re.M)[1:]
 if len(notes)!=7:raise ValueError('Seven source notes required')
 original=CASE/'original/deck.pptx';out=CASE/'deck.pptx'
 changed=[]
 with zipfile.ZipFile(original) as src,zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as dst:
  for info in src.infolist():
   data=src.read(info.filename);m=re.fullmatch(r'ppt/notesSlides/notesSlide(\d+)\.xml',info.filename)
   if m:
    text=data.decode('utf-8');marker='<a:t></a:t>'
    if marker not in text:raise ValueError('Expected empty notes placeholder')
    text=text.replace(marker,'<a:t>'+escape(notes[int(m[1])-1].strip())+'</a:t>',1).replace('lang="en-US"','lang="ja-JP"');data=text.encode('utf-8');changed.append(info.filename)
   dst.writestr(info,data)
 with zipfile.ZipFile(original) as a,zipfile.ZipFile(out) as b:
  diffs=[n for n in a.namelist() if a.read(n)!=b.read(n)]
  if sorted(diffs)!=sorted(changed):raise ValueError('Unexpected PPTX changes')
  pics=[];ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
  for i in range(1,8):
   tree=ET.fromstring(b.read(f'ppt/slides/slide{i}.xml'));pics.append({'page':i,'pictures':len(tree.findall('.//p:pic',ns)),'text_shapes':len(tree.findall('.//p:sp',ns))})
  assert all(p['pictures']==1 and p['text_shapes']==0 for p in pics)
 shutil.copy2(CASE/'original/deck.pdf',CASE/'deck.pdf')
 proof={'source_pptx_sha256':sha(original),'output_pptx_sha256':sha(out),'changed_zip_entries':diffs,'all_slide_xml_and_media_byte_identical':True,'pages':pics,'notes_editable':True,'body_text_editable':False}
 save(CASE/'review/postprocess-proof.json',proof)
 return proof
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--node',help='Node.js 22+ executable');ap.add_argument('--browser-cache',help='PLAYWRIGHT_BROWSERS_PATH');ap.add_argument('--scale',type=int,choices=[2,3],default=3);ap.add_argument('--powerpoint',action='store_true');args=ap.parse_args()
 runtime=CASE/'source/runtime';node=Path(args.node or shutil.which('node') or 'node');npm=node.parent/'node_modules/npm/bin/npm-cli.js';env=dict(os.environ);env['PATH']=str(node.parent)+os.pathsep+env.get('PATH','')
 if args.browser_cache:env['PLAYWRIGHT_BROWSERS_PATH']=args.browser_cache
 receipts=[]
 def run(argv,name,cwd=runtime):
  argv=[str(x) for x in argv];r=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');log=CASE/'review/replay'/(name+'.log');log.parent.mkdir(parents=True,exist_ok=True);log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');receipts.append({'argv':argv,'cwd':str(cwd),'exit_code':r.returncode,'log':log.relative_to(CASE).as_posix(),'log_sha256':sha(log),'env_overrides':{'PLAYWRIGHT_BROWSERS_PATH':env.get('PLAYWRIGHT_BROWSERS_PATH')}});save(CASE/'review/replay/receipts.json',receipts)
  if r.returncode:raise RuntimeError(log.read_text('utf-8'))
  return r
 qa={'status':'generated_awaiting_review','page_count':7,'all_pages_visually_reviewed':False,'human_adoption':'pending','production_adoption':False,'publication':False};save(CASE/'QA.json',qa)
 if not (runtime/'node_modules/playwright').exists():
  if not npm.exists():raise SystemExit('Use --node pointing to a Node installation with sibling node_modules/npm/bin/npm-cli.js')
  run([node,npm,'ci','--ignore-scripts','--no-fund'],'npm-ci')
 # Native Playwright installation command checks the expected revision and downloads only if absent.
 run([node,runtime/'node_modules/playwright/cli.js','install','chromium'],'chromium-install')
 raw=CASE/'input/port-town/index.html';adapted=CASE/'input/port-town/export.html';adapted.write_text(raw.read_text('utf-8').replace('</body>',ADAPTER+'\n</body>'),encoding='utf-8')
 assert sha(runtime/'build.mjs')==sha(CASE/'source/upstream/scripts/build.mjs')
 result=run([node,runtime/'build.mjs',adapted,'--out',CASE/'original','--scale',str(args.scale)],'original-converter')
 if len(re.findall(r'✓ \d+/7',result.stdout))!=7 or '✗' in result.stdout:raise RuntimeError('Not every page captured successfully')
 pngs=[CASE/'original/frames'/f'slide-{i:02d}.png' for i in range(1,8)]
 if len({sha(p) for p in pngs})!=7:raise RuntimeError('Duplicate captured pages')
 dimensions=[struct.unpack('>II',p.read_bytes()[16:24]) for p in pngs]
 assert all(x==(1920*args.scale,1080*args.scale) for x in dimensions)
 proof=postprocess();run([node,CASE/'source/verify-pdf.mjs'],'pdf-check')
 qa.update({'artifact_sha256':sha(CASE/'deck.pptx'),'pdf_sha256':sha(CASE/'deck.pdf'),'input_sha256':sha(raw),'adapted_input_sha256':sha(adapted),'scale':args.scale,'image_dimensions':dimensions[0],'all_seven_captured':True,'postprocess':proof})
 if args.powerpoint:
  run([shutil.which('pwsh') or 'powershell','-NoProfile','-File',CASE/'source/render_powerpoint.ps1','-PresentationPath',CASE/'deck.pptx','-OutputDirectory',CASE/'render'],'native-powerpoint',CASE)
  qa['native_powerpoint_report']='render/powerpoint-render.json'
 save(CASE/'QA.json',qa);print(json.dumps({'status':qa['status'],'pages':7,'artifact':str(CASE/'deck.pptx'),'scale':args.scale}))
if __name__=='__main__':main()
