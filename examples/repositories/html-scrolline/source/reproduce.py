"""Build the actual Scrolline engine and optionally run its browser smoke test."""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, socket, subprocess, sys, time

CASE=Path(__file__).resolve().parents[1]
UP=CASE/'source/upstream'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,default=CASE/'input/data.json')
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--chrome',type=Path,help='Installed Chrome/Edge or chrome-headless-shell executable')
    args=ap.parse_args();data=json.loads(args.input.resolve().read_text('utf-8'))
    if data.get('id')!='exhibit-ja':raise SystemExit('Keep id=exhibit-ja or adapt the deck folder and build selector together.')
    save(UP/'decks/exhibit-ja/deck.yaml',data)
    node=shutil.which('node');npm=shutil.which('npm.cmd') or shutil.which('npm')
    if not node or not npm:raise SystemExit('Node.js 22+ and npm are required.')
    review=CASE/'review/replay';review.mkdir(parents=True,exist_ok=True);receipts=[]
    def run(argv,name,env=None,allowed=(0,)):
        result=subprocess.run([str(a) for a in argv],cwd=UP,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        log=review/(name+'.log');log.write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
        receipts.append({'argv':[str(a) for a in argv],'cwd':str(UP),'exit_code':result.returncode,'log':log.relative_to(CASE).as_posix(),'log_sha256':sha(log)})
        save(review/'execution-receipts.json',receipts)
        if result.returncode not in allowed:raise SystemExit(result.stdout+'\n'+result.stderr)
        return result
    if not (UP/'node_modules/vite').exists():run([npm,'ci','--ignore-scripts'],'npm-ci')
    run([node,'tools/cli.mjs','plan','exhibit-ja'],'original-plan')
    env=dict(os.environ);env['SCROLLINE_DECK']='exhibit-ja';env['SCROLLINE_OUT']=str(CASE/'presentation')
    run([npm,'run','build'],'original-vite-build',env)
    # Vite minification drops license comments by default. Restore the original
    # notices in every distributed JS bundle before creating the single HTML.
    notices='/*!\n'+(UP/'LICENSE').read_text('utf-8')+'\n'+(UP/'node_modules/lenis/LICENSE').read_text('utf-8')+'\n*/\n'
    for name in ['gsap-core','CSSPlugin','ScrollTrigger','Observer','CustomEase','DrawSVGPlugin','Flip','MorphSVGPlugin','SplitText']:
        content=(UP/f'node_modules/gsap/{name}.js').read_text('utf-8')
        match=re.search(r'/\*!.*?\*/',content,re.S)
        if not match:raise SystemExit('Missing upstream license header: '+name)
        notices+=match.group(0)+'\n'
    (CASE/'licenses').mkdir(exist_ok=True)
    (CASE/'licenses/bundled-runtime-notices.txt').write_text(notices,encoding='utf-8')
    for bundle in (CASE/'presentation/assets').glob('*.js'):
        bundle.write_text(notices+bundle.read_text('utf-8'),encoding='utf-8')
    # Inline the original Vite bundle; no layout or animation is reconstructed here.
    root=CASE/'presentation';page=(root/'index.html').read_text('utf-8')
    def js(m):return '<script type="module">'+(root/m.group(1)).read_text('utf-8').replace('</script','<\\/script')+'</script>'
    def css(m):return '<style>'+(root/m.group(1)).read_text('utf-8')+'</style>'
    page=re.sub(r'<script[^>]+src="\./([^"]+)"[^>]*></script>',js,page)
    page=re.sub(r'<link[^>]+href="\./([^"]+\.css)"[^>]*>',css,page)
    bridge='''<script id="yebisu-scrolline-bridge">
(() => {
  if (parent === window) return;
  let pending = null;
  let lastIndex = -1;
  const sync = () => {
    const api = window.__deck;
    if (!api || typeof api.stops !== 'function' || typeof api.goto !== 'function') return;
    const stops = api.stops();
    if (!stops.length) return;
    if (pending !== null) {
      const index = pending;
      pending = null;
      if (index < stops.length) api.goto(stops[index].name);
    }
    const time = api.time();
    if (!Number.isFinite(time)) return;
    let index = 0;
    for (let n = 1; n < stops.length; n++) {
      if (Math.abs(stops[n].t - time) < Math.abs(stops[index].t - time)) index = n;
    }
    if (index !== lastIndex) {
      lastIndex = index;
      parent.postMessage({ type: 'yebisu-page', index }, location.origin);
    }
  };
  addEventListener('message', e => {
    if (e.source !== parent || e.origin !== location.origin) return;
    if (e.data?.type !== 'yebisu-slide' || !Number.isInteger(e.data.index) || e.data.index < 0) return;
    const stops = window.__deck?.stops();
    if (stops && e.data.index >= stops.length) return;
    pending = e.data.index;
    sync();
  });
  addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    e.preventDefault();
    e.stopImmediatePropagation();
    parent.postMessage({ type: 'yebisu-close' }, location.origin);
  }, true);
  const timer = setInterval(sync, 100);
  addEventListener('pagehide', () => clearInterval(timer), { once: true });
  sync();
})();
</script>'''
    page=page.replace('</body>',bridge+'</body>')
    (CASE/'deck.html').write_text(page,encoding='utf-8')
    save(CASE/'QA.json',{'status':'generated_awaiting_review','page_count':6,'all_pages_visually_reviewed':False,'artifact_sha256':sha(CASE/'deck.html'),'input_sha256':sha(args.input.resolve()),'human_adoption':'pending','production_adoption':False,'publication':False,'original_gate_not_passed':True,'note':'A new artifact was generated. Previous visual QA does not transfer to this output.'})
    if args.render:
        chrome=args.chrome
        if chrome is None:
            choices=[os.environ.get('SCROLLINE_CHROME',''),'C:/Program Files/Google/Chrome/Application/chrome.exe','C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',shutil.which('google-chrome') or '',shutil.which('chromium') or '']
            chrome=next((Path(p) for p in choices if p and Path(p).is_file()),None)
        if chrome is None or not chrome.is_file():raise SystemExit('Set --chrome to an installed Chrome/Edge executable.')
        with socket.socket() as probe:
            probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
        env=dict(os.environ);env['SCROLLINE_CHROME']=str(chrome.resolve());env['SCROLLINE_URL']=f'http://127.0.0.1:{port}/deck.html'
        env.pop('SCROLLINE_OFFLINE',None)
        serverlog=(review/'localhost-server.log').open('w',encoding='utf-8')
        server=subprocess.Popen([sys.executable,'-m','http.server',str(port),'--bind','127.0.0.1','--directory',str(CASE)],stdout=serverlog,stderr=serverlog,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        try:
            for _ in range(50):
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=0.2):break
                except OSError:time.sleep(0.1)
            # Original probe, measurement and screenshot code; only its executable
            # discovery and HTTP URL are adapted. No file:// browser operation.
            run([node,'tools/smoke.windows.mjs','exhibit-ja','--driver','chrome','--shots','--out',CASE/'render'],'original-smoke-portable-adapter',env)
        finally:
            server.terminate();server.wait(timeout=10);serverlog.close()
        report=json.loads((CASE/'render/report.json').read_text('utf-8'));summary=report['summary']
        if any(summary[k] for k in ['errors','empty','overlaps','clipped','tinyText','mediaPending']):raise SystemExit('Smoke quality gate failed: '+json.dumps(summary))
    save(review/'result.json',{'input_sha256':sha(args.input.resolve()),'artifact_sha256':sha(CASE/'deck.html'),'render_requested':args.render,'visual_review':'required_for_changed_input'})
    print('Built '+str(CASE/'deck.html'))
if __name__=='__main__':main()
