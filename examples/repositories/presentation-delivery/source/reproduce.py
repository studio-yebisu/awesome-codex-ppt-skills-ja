"""Replay the original Visual Deck Studio HTML-first workflow over local HTTP."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import argparse, difflib, json, os, re, shutil, subprocess, sys, threading

CASE=Path(__file__).resolve().parents[1]
UP=CASE/'source/upstream/skills/visual-deck-studio'
RUNTIME=CASE/'source/runtime'

def write(p, text):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
def dump(p, v):write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def digest(p):return sha256(p.read_bytes()).hexdigest()
def command(argv, tag, env):
    started=datetime.now(timezone.utc).isoformat()
    result=subprocess.run([str(x) for x in argv],cwd=CASE,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=CASE/'review/execution'/f'{tag}.log';log.parent.mkdir(parents=True,exist_ok=True);log.write_bytes(result.stdout)
    item={'argv':[str(x) for x in argv],'cwd':str(CASE),'started_at':started,'exit_code':result.returncode,
          'log':log.relative_to(CASE).as_posix(),'log_sha256':digest(log)}
    RECEIPTS.append(item)
    dump(CASE/'review/execution/commands.json',RECEIPTS)
    print(f'{tag}: exit {result.returncode}',flush=True)
    if result.returncode:raise RuntimeError(f'{tag} failed; see {log}')
    return result.stdout

CSS="""@font-face{font-family:'BIZ UDPGothic';src:url('fonts/BIZUDPGothic-Regular.ttf') format('truetype');font-weight:400;font-display:block}
@font-face{font-family:'BIZ UDPGothic';src:url('fonts/BIZUDPGothic-Bold.ttf') format('truetype');font-weight:700;font-display:block}
*{box-sizing:border-box;margin:0;padding:0}body{width:960pt;height:540pt;overflow:hidden;position:relative;background:#f7f5ee;color:#203e31;font-family:'BIZ UDPGothic',sans-serif;font-size:18pt;line-height:1.5}
body.dark{background:#203e31;color:#f7f5ee}.masthead{position:absolute;left:52pt;top:25pt;width:856pt;border-bottom:1pt solid #708571;padding-bottom:10pt;display:flex;justify-content:space-between}.masthead p{font-size:10pt;letter-spacing:.06em}
.content{position:absolute;left:52pt;top:89pt;width:856pt;height:382pt}h1{font-size:32pt;line-height:1.35;font-weight:700;letter-spacing:-.025em}h2{font-size:26pt;line-height:1.4;font-weight:700}p{font-size:18pt;line-height:1.5}.hero{font-size:54pt;line-height:1.28}.lead{font-size:22pt;line-height:1.55;margin-top:22pt}.handoff{display:flex;gap:26pt;align-items:center;margin-top:40pt}.handoff p{font-size:24pt}.handoff .arrow{font-size:32pt;color:#b4c7af}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:24pt;margin-top:48pt}.three>div{border-top:2pt solid #708571;padding-top:20pt}.tag{font-size:14pt;color:#577258}.dark .tag{color:#b4c7af}.three h2{margin-top:12pt}.three>div>p:last-child{margin-top:17pt}.bottom-line{position:absolute;left:0;top:344pt;font-size:16pt;line-height:1.5}.filename{margin-top:24pt;padding:19pt 24pt;background:#dde6d5}.filename p{font-size:28pt;font-weight:700;line-height:1.4}.compact{margin-top:24pt}.compact>div{padding-top:12pt}.compact h2{font-size:24pt;margin-top:5pt}.compact>div>p:last-child{font-size:16pt;margin-top:8pt}
.status{display:grid;grid-template-columns:1fr 1fr;gap:34pt;margin-top:34pt}.status>div{border-top:2pt solid #b4c7af;padding-top:20pt}.status h2{margin-top:12pt}.status>div>p:last-child{margin-top:17pt}.checks{margin-top:38pt;display:grid;grid-template-columns:repeat(3,1fr);gap:28pt}.step{font-size:32pt;line-height:1.25;color:#577258}.checks h2{font-size:24pt;margin-top:15pt}.checks>div>p:last-child{font-size:17pt;margin-top:17pt}.kicker{font-size:14pt;letter-spacing:.08em}.closing{font-size:46pt;margin-top:12pt}.message{margin-top:26pt;padding:14pt 20pt;background:#dde6d5}.message p{font-size:17pt;line-height:1.7}.lead p{font-size:22pt;line-height:1.55;margin:0}.body-copy{margin-top:17pt}.body-copy p{margin:0}.filename-parts{margin-top:16pt}.filename-parts>div{display:flex;gap:18pt;align-items:center;height:52pt;border-bottom:1pt solid #708571}.filename-parts h2{font-size:23pt;width:180pt}.filename-parts p{font-size:16pt}.filename-parts .part-label{width:50pt;color:#577258}.filename-parts .part-arrow{font-size:24pt;color:#577258}.footer{position:absolute;left:52pt;top:507pt;width:856pt;display:flex;justify-content:space-between}.footer p{font-size:9pt;line-height:1.4;color:#577258}.dark .footer p{color:#b4c7af}
"""

def index(data, root):
    raw=(UP/'assets/deck_index.html').read_text(encoding='utf-8')
    manifest=[{'file':f'slides/{i+1:02}-slide.html','label':p['title'],'thumb':f'thumbs/{i+1:02}-slide.jpg'} for i,p in enumerate(data['pages'])]
    result,n=re.subn(r'window.DECK_MANIFEST = \[.*?\];','window.DECK_MANIFEST = '+json.dumps(manifest,ensure_ascii=False)+';',raw,count=1,flags=re.S)
    assert n==1
    result=result.replace('1920','1280').replace('1080','720').replace('lang="zh-CN"','lang="ja"')
    result=result.replace('<title>Deck · Multi-file Slide Index</title>',f'<title>{data["title"]}</title>')
    for a,b in [('Overview · 点击任意页进入演示','ページ一覧 · クリックして再生'),('Infinite Gallery · 悬停暂停 · 点击任意页进入演示','ギャラリー · 触れると停止 · クリックして再生'),('▶ 开始演示','再生する'),('⊞ 概览','ページ一覧')]:result=result.replace(a,b)
    bridge="""
  // Japanese catalog adapter: call the original show/setMode functions.
  function publish(){ if(parent!==window)parent.postMessage({type:'yebisu-page',index:current},location.origin); }
  window.addEventListener('message',e=>{
    if(e.origin!==location.origin || e.source!==parent)return;
    if(e.data && e.data.type==='yebisu-slide' && Number.isInteger(e.data.index)){
      current=Math.max(0,Math.min(deck.length-1,e.data.index));setMode('present');publish();
    }
  });
  const catalogFrame=new URLSearchParams(location.search).get('catalog')==='1';
  if(catalogFrame){document.body.classList.add('catalog-frame');current=0;setMode('present');}
  publish();
"""
    # Publish after the original counter / storage are updated, preserving navigation.
    result=result.replace("if (location.hash !== '#' + (idx + 1)) history.replaceState(null, '', '#' + (idx + 1));", "if (location.hash !== '#' + (idx + 1)) history.replaceState(null, '', '#' + (idx + 1));\n    publish();")
    result=result.replace('fit(); show(current);','fit(); show(current);'+bridge)
    assert bridge in result
    result=result.replace('</head>',"<style>.catalog-frame .counter,.catalog-frame .overview-btn,.catalog-frame .nav-zone{display:none}@media(prefers-reduced-motion:reduce){.breathe,.drift-layer{animation:none!important}.card{transition:none!important}}</style></head>")
    write(root/'index.html',result)
    write(CASE/'source/deck-index-adapter.diff',''.join(difflib.unified_diff(raw.splitlines(True),result.splitlines(True),fromfile='original/assets/deck_index.html',tofile='Japanese/index.html')))

def prepare_runtime():
    RUNTIME.mkdir(parents=True,exist_ok=True)
    diffs=[]
    mappings={
      'html2pptx.js':[("const launchOptions = { env: { TMPDIR: tmpDir } };","const launchOptions = { env: { ...process.env, TMPDIR: tmpDir } };"),
        ('await page.goto(`file://${filePath}`);',"if(!process.env.YEBISU_DECK_BASE_URL)throw new Error('Local HTTP base URL is required');\n      await page.goto(new URL('slides/'+path.basename(filePath),process.env.YEBISU_DECK_BASE_URL).href);\n      await page.evaluate(()=>document.fonts.ready);")],
      'export_deck_pdf.mjs':[("const url = 'file://' + path.join(slidesDir, f);","if(!process.env.YEBISU_DECK_BASE_URL)throw new Error('Local HTTP base URL is required');\n    const url = new URL('slides/'+f,process.env.YEBISU_DECK_BASE_URL).href;")],
      'gen_deck_thumbs.mjs':[("await page.goto('file://' + path.resolve(slidesDir, f), { waitUntil: 'load' });","if(!process.env.YEBISU_DECK_BASE_URL)throw new Error('Local HTTP base URL is required');\n    await page.goto(new URL('slides/'+f,process.env.YEBISU_DECK_BASE_URL).href, { waitUntil: 'load' });")],
      'export_deck_pptx.mjs':[("await html2pptx(fullPath, pres);","const { slide } = await html2pptx(fullPath, pres);\n      const input = JSON.parse(await fs.readFile(process.env.YEBISU_DECK_INPUT, 'utf8'));\n      slide.addNotes(input.pages[i].note);")]
    }
    for name,changes in mappings.items():
        raw=(UP/'scripts'/name).read_text(encoding='utf-8');adapted=raw
        for a,b in changes:
            assert adapted.count(a)==1,(name,a)
            adapted=adapted.replace(a,b)
        write(RUNTIME/name,adapted)
        diffs+=list(difflib.unified_diff(raw.splitlines(True),adapted.splitlines(True),fromfile='original/scripts/'+name,tofile='HTTP-Japanese/scripts/'+name))
    write(CASE/'source/runtime-adapter.diff',''.join(diffs))
    if not (RUNTIME/'package-lock.json').exists():
        dump(RUNTIME/'package.json',{'private':True,'dependencies':{'pdf-lib':'1.17.1','playwright':'1.60.0','pptxgenjs':'4.0.1','sharp':'0.35.5'},'overrides':{'image-size':'2.0.3'}})

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    global BUILD_STARTED
    parser=argparse.ArgumentParser();parser.add_argument('--input',default=str(CASE/'input/data.json'));parser.add_argument('--node',default=shutil.which('node'));parser.add_argument('--powerpoint',action='store_true');parser.add_argument('--showcase',action='store_true');parser.add_argument('--html-only',action='store_true');parser.add_argument('--reuse-existing-dependencies',action='store_true',help='Use existing pinned Node dependencies and browser; no install')
    args=parser.parse_args();data=json.loads(Path(args.input).read_text(encoding='utf-8'));assert len(data['pages'])==6
    BUILD_STARTED=not args.showcase
    if BUILD_STARTED:dump(CASE/'QA.json',{'status':'generation_in_progress','human_review':False,'full_page_visual_review':False})
    root=CASE/'showcase' if args.showcase else CASE
    pages=[(i,p) for i,p in enumerate(data['pages']) if not args.showcase or i in (0,3)]
    if args.showcase:shutil.copytree(CASE/'shared',root/'shared',dirs_exist_ok=True)
    write(root/'shared/tokens.css',CSS)
    for i,p in pages:
        doc='<!DOCTYPE html>\n<html lang="ja"><head><meta charset="UTF-8"><title>'+p['title']+'</title><link rel="stylesheet" href="../shared/tokens.css"></head><body class="'+p['tone']+'">\n'
        doc+='<!-- Assumption: fictional internal handoff guide; not an adopted company rule. -->\n<div class="masthead"><p>資料を渡す、その前に。</p><p>説明用の記入例</p></div><div class="content">'+p['content']+'</div><div class="footer"><p>用途・場所・次の行動</p><p>'+str(i+1)+' / 6</p></div></body></html>\n'
        write(root/f'slides/{i+1:02}-slide.html',doc)
    if not args.showcase:index(data,CASE)
    if args.html_only:print(root);return
    assert args.node,'Node.js is required; pass --node with the full executable path'
    node=Path(args.node).resolve();npm=node.parent/'node_modules/npm/bin/npm-cli.js'
    if not args.reuse_existing_dependencies:assert npm.is_file(),npm
    prepare_runtime()
    env=os.environ.copy()
    if env.get('LOCALAPPDATA') and not env.get('PLAYWRIGHT_BROWSERS_PATH'):env['PLAYWRIGHT_BROWSERS_PATH']=str(Path(env['LOCALAPPDATA'])/'ms-playwright')
    env['YEBISU_DECK_INPUT']=str(Path(args.input).resolve())
    install='ci' if (RUNTIME/'package-lock.json').exists() else 'install'
    if args.reuse_existing_dependencies:
        for name in ['playwright','pdf-lib','pptxgenjs','sharp']:
            assert (RUNTIME/'node_modules'/name/'package.json').is_file(),name+' is not installed'
    else:
        command([node,npm,install,'--prefix',RUNTIME,'--no-fund','--no-audit'],'npm-'+install,env)
        command([node,RUNTIME/'node_modules/playwright/cli.js','install','chromium','--only-shell'],'official-chromium-setup',env)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(root)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    env['YEBISU_DECK_BASE_URL']=f'http://127.0.0.1:{server.server_port}/'
    try:
        command([node,RUNTIME/'capture.mjs','--root',root],'showcase-http-capture' if args.showcase else 'html-http-capture',env)
        if not args.showcase:
            command([node,RUNTIME/'export_deck_pdf.mjs','--slides',CASE/'slides','--out',CASE/'deck.pdf','--width','1280','--height','720'],'original-pdf-http-adapter',env)
            command([node,RUNTIME/'export_deck_pptx.mjs','--slides',CASE/'slides','--out',CASE/'deck.pptx'],'original-pptx-http-adapter',env)
            command([node,RUNTIME/'gen_deck_thumbs.mjs','--slides',CASE/'slides','--out',CASE/'thumbs','--canvas-w','1280','--canvas-h','720'],'original-thumbs-http-adapter',env)
    finally:
        server.shutdown();server.server_close()
    if args.powerpoint and not args.showcase:
        command(['pwsh','-NoProfile','-File',CASE/'source/render_powerpoint.ps1','-PresentationPath',CASE/'deck.pptx','-OutputDirectory',CASE/'render'],'powerpoint-render',env)
    if not args.showcase:
        dump(CASE/'QA.json',{'case':'presentation-delivery','status':'generated_awaiting_review','human_review':False,'full_page_visual_review':False,'new_output_requires_review':True,
            'scope':'Original HTML-first instruction, original DOM conversion / validation and PDF merge, with explicit HTTP / font readiness / Japanese notes adapters. No file URL route, video, TTS, fallback variations, or owner adoption claimed.'})
    print(str(root),flush=True)

RECEIPTS=[]
BUILD_STARTED=False
if __name__=='__main__':
    try:main()
    except BaseException:
        if BUILD_STARTED:dump(CASE/'QA.json',{'status':'generation_failed','human_review':False,'full_page_visual_review':False,'previous_review_not_transferred':True})
        raise
