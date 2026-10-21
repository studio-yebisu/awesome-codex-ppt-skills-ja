"""Fill the original HTML template; --render checks the result over local HTTP."""
from pathlib import Path
import argparse,functools,hashlib,http.server,json,os,re,shutil,subprocess,threading
CASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=Path,default=CASE/'input/data.json');ap.add_argument('--render',action='store_true');ap.add_argument('--chrome');args=ap.parse_args()
 data=json.loads(args.input.read_text('utf-8'));pages=data['pages']
 if len(pages)!=6 or data['theme']!='Forest Ink':raise SystemExit('This example requires six pages and the Forest Ink theme.')
 original=(CASE/'source/upstream/assets/template.html').read_text('utf-8');html=original.replace('lang="zh-CN"','lang="ja"')
 html=re.sub(r'<title>.*?</title>','<title>'+data['title']+'</title>',html)
 html=re.sub(r'<link[^>]+>\n?','',html)
 for a,b in {'#0a1f3d':'#1a2e1f','10,31,61':'26,46,31','#f1f3f5':'#f5f1e8','241,243,245':'245,241,232','#e4e8ec':'#ece7da','#152a4a':'#253d2c','#3b82f6':'#2d8a4e','59,130,246':'45,138,78',"'Noto Serif SC','Source Han Serif SC',serif":"'Yu Mincho','Hiragino Mincho ProN',serif","'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif":"'Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif","'Inter',-apple-system,sans-serif":"'Yu Gothic',sans-serif","'IBM Plex Mono','Cascadia Code',monospace":"'Consolas','Yu Gothic',monospace"}.items():html=html.replace(a,b)
 # Original layout classes are retained. These explicit Japanese readability changes are additive.
 css='''\n/* Japanese adaptation: local fonts, line spacing, larger metadata, equal comparison weight. */
 .h-hero{line-height:1.38;font-size:clamp(36px,5vw,80px)}.h-xl{line-height:1.4}
 .lead{font-size:clamp(18px,1.4vw,27px);font-weight:400;max-width:80vw;opacity:.85}
 .chrome,.foot{font-size:clamp(12px,.9vw,18px);opacity:.7}.foot{padding-bottom:2vh}
 .kicker,.meta-row,.stat-label,.stat-note,.col-header{font-size:clamp(14px,1.1vw,22px);opacity:.75}
 .stat-unit{opacity:.85}.stat-nb{font-size:clamp(32px,3vw,56px)}.stat-note{margin-top:1vh}
 .callout{max-width:80vw;font-size:clamp(18px,1.5vw,28px);line-height:1.8}
 .compare{margin-top:5vh}.before-col{opacity:1}.col-list li,.after-col .col-list li{font-size:clamp(17px,1.3vw,25px);opacity:.85;line-height:1.8;padding:1.2vh 0}
 .closing{font-family:var(--serif-zh);font-size:clamp(25px,2.7vw,45px);font-weight:600}
 #nav{color:var(--accent);bottom:1.8vh}#nav .dot{width:10px;height:10px}
 '''
 html=html.replace('</style>',css+'</style>')
 from html import escape
 slides='\n'.join(f'<section class="slide {p["tone"]}" aria-label="{escape(p["title"])}"><div class="chrome"><div>みどり図書館 · 参加案内の例</div><div>{i+1:02d} / 06</div></div><div class="frame"><div class="kicker anim">{escape(p["kicker"])}</div>{p["body"]}</div><div class="foot"><div>図書館・催し・日時は架空の設定</div><div>雨の日の読書会</div></div></section>' for i,p in enumerate(pages))
 start=html.index('<div class="deck-wrapper" id="deck">')+len('<div class="deck-wrapper" id="deck">');end=html.index('\n</div>\n<div id="nav">',start);html=html[:start]+'\n'+slides+'\n'+html[end:]
 bridge='''<script id="catalog-bridge">
 (()=>{const slides=[...document.querySelectorAll('.slide')],deck=document.getElementById('deck');let last=-1;
 const current=()=>Math.max(0,Math.min(slides.length-1,Math.round(deck.scrollLeft/innerWidth)));
 const notify=()=>{const i=current();if(i!==last){last=i;if(parent!==window)parent.postMessage({type:'yebisu-page',index:i},location.origin)}};
 addEventListener('message',e=>{if(e.source!==parent||parent===window||e.origin!==location.origin||e.data?.type!=='yebisu-slide')return;const i=e.data.index;if(Number.isInteger(i)&&i>=0&&i<slides.length)slides[i].scrollIntoView({behavior:'smooth'})});
 addEventListener('keydown',e=>{if(e.key==='Escape'&&parent!==window)parent.postMessage({type:'yebisu-close'},location.origin)});
 deck.addEventListener('scroll',notify);notify();})();
 </script>'''
 html=html.replace('</body>',bridge+'\n</body>');html=html.replace('<head>','<head>\n<!-- Original template: Copyright (c) 2026 att6113. MIT; see licenses/LICENSE-upstream.txt. -->')
 (CASE/'deck.html').write_text(html,encoding='utf-8');shutil.copy2(CASE/'deck.html',CASE/'index.html')
 original_js=re.search(r'<script>(.*?)</script>',original,re.S).group(1);output_js=re.search(r'<script>(.*?)</script>',html,re.S).group(1)
 if original_js!=output_js:raise SystemExit('Original navigation JS was changed.')
 proof={'original_navigation_js_preserved':True,'template_sha256':sha(CASE/'source/upstream/assets/template.html'),'artifact_sha256':sha(CASE/'deck.html'),'theme':'Forest Ink','page_count':6}
 save(CASE/'review/template-proof.json',proof)
 qa={'status':'generated_awaiting_review','page_count':6,'all_pages_visually_reviewed':False,'artifact_sha256':sha(CASE/'deck.html'),'input_sha256':sha(args.input),'human_adoption':'pending','production_adoption':False,'publication':False,'original_template_proof':proof}
 save(CASE/'QA.json',qa)
 if args.render:
  chrome=args.chrome or next((p for p in [r'C:\Program Files\Google\Chrome\Application\chrome.exe',r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',shutil.which('google-chrome'),shutil.which('chromium')] if p and Path(p).exists()),None)
  if not chrome:raise SystemExit('Pass --chrome with an installed Chrome/Edge executable.')
  class Quiet(http.server.SimpleHTTPRequestHandler):
   def log_message(self,*a):pass
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(CASE)));threading.Thread(target=server.serve_forever,daemon=True).start()
  argv=[shutil.which('node') or 'node',str(CASE/'source/render.mjs'),f'http://127.0.0.1:{server.server_port}/',chrome]
  try:r=subprocess.run(argv,cwd=CASE,capture_output=True,text=True,encoding='utf-8',errors='replace')
  finally:server.shutdown();server.server_close()
  log=CASE/'review/render-command.log';log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');save(CASE/'review/render-receipt.json',{'argv':argv,'cwd':str(CASE),'exit_code':r.returncode,'log':log.relative_to(CASE).as_posix(),'log_sha256':sha(log)})
  if r.returncode:raise SystemExit(log.read_text('utf-8'))
  qa['browser_checks']=json.loads((CASE/'render/report.json').read_text('utf-8'));save(CASE/'QA.json',qa)
 print(json.dumps(proof))
if __name__=='__main__':main()
