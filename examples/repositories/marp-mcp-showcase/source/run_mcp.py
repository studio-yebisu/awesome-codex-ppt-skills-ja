"""Reproduce this case through the pinned marp-mcp stdio server, not a substitute renderer."""
from pathlib import Path
import argparse, base64, json, os, queue, subprocess, threading, time

ROOT = Path(__file__).resolve().parents[1]

class MCP:
    def __init__(self, node, runtime, marp_cli, log_dir):
        self.seq = 0
        self.events = []
        self.q = queue.Queue()
        env = os.environ.copy()
        env['MARP_CLI_JS'] = str(marp_cli)
        self.err = (log_dir/'mcp-stderr.jsonl').open('w', encoding='utf-8')
        self.p = subprocess.Popen([str(node),str(runtime/'build/index.js'),'-s','minimal','serve'],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,
            cwd=str(runtime),env=env,text=True,encoding='utf-8')
        threading.Thread(target=self._reader,daemon=True).start()
        self.request('initialize', {'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'yebisu-case-builder','version':'1.0'}})
        self.send({'jsonrpc':'2.0','method':'notifications/initialized'})
    def _reader(self):
        for line in self.p.stdout:
            self.q.put(json.loads(line))
    def send(self, obj):
        self.events.append({'direction':'client','message':obj})
        self.p.stdin.write(json.dumps(obj,ensure_ascii=False)+'\n')
        self.p.stdin.flush()
    def request(self, method, params):
        self.seq += 1
        self.send({'jsonrpc':'2.0','id':self.seq,'method':method,'params':params})
        deadline=time.monotonic()+90
        while time.monotonic()<deadline:
            obj=self.q.get(timeout=max(1,deadline-time.monotonic()))
            self.events.append({'direction':'server','message':obj})
            if obj.get('id')==self.seq:
                if 'error' in obj: raise RuntimeError(obj['error'])
                return obj['result']
        raise TimeoutError(method)
    def call(self,name,args):
        result=self.request('tools/call',{'name':name,'arguments':args})
        if result.get('isError'): raise RuntimeError(result)
        return result
    def close(self,log_dir):
        self.p.stdin.close()
        try:self.p.wait(timeout=3)
        except subprocess.TimeoutExpired:self.p.terminate()
        self.err.close()
        (log_dir/'mcp-operations.json').write_text(json.dumps(self.events,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

BRIDGE = '''<script id="yebisu-marp-bridge">
(() => {
  const total = 6;
  const current = () => Math.max(0, Math.min(total-1, Number(location.hash.replace('#','') || 1)-1));
  const report = () => { if(parent !== window) parent.postMessage({type:'yebisu-page',index:current(),total},location.origin); };
  addEventListener('message',e => {
    if(e.origin!==location.origin || e.source!==parent || !e.data || e.data.type!=='yebisu-slide') return;
    const i=Number(e.data.index); if(Number.isInteger(i) && i>=0 && i<total) location.hash=String(i+1);
    setTimeout(report,80);
  });
  addEventListener('hashchange',report); addEventListener('load',report); report();
})();
</script>'''

def build(args):
    case=args.case.resolve()
    log_dir=case/'source/logs'; log_dir.mkdir(parents=True,exist_ok=True)
    client=MCP(args.node,args.runtime.resolve(),args.marp_cli.resolve(),log_dir)
    try:
        client.call('list_themes_and_styles',{})
        layouts=client.call('list_layouts',{'theme':'default','style':'minimal'})
        (log_dir/'layouts.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding='utf-8')
        if args.probe:
            print('Pinned MCP initialized; style/layout discovery successful.')
            return
        spec=json.loads((case/'input/content.json').read_text(encoding='utf-8'))
        deck=case/'deck.md'
        if deck.exists():
            # Keep a previous local source before an explicitly requested rebuild.
            (log_dir/'deck-before-rebuild.md').write_bytes(deck.read_bytes())
            deck.unlink()
        client.call('create_presentation',{'filePath':str(deck),'title':spec['title'],'subtitle':spec['subtitle'],'paginate':True})
        client.call('set_frontmatter',{'filePath':str(deck),'header':'','paginate':True,'theme':'default','style':'minimal'})
        for s in spec['slides']:
            client.call('manage_slide',{'filePath':str(deck),'layoutType':s['layout'],'params':s['params'],'note':s['note']})
        client.call('generate_slide_ids',{'filePath':str(deck)})
        client.call('read_slide',{'filePath':str(deck)})
        # Japanese typography and case artwork are a local CSS extension of the original layouts.
        css=(case/'source/workshop.css').read_text(encoding='utf-8')
        for family,file,weight in [('WorkshopBody','bizudpgothic/BIZUDPGothic-Regular.ttf','400'),('WorkshopBody','bizudpgothic/BIZUDPGothic-Bold.ttf','700'),('WorkshopHeading','shipporimincho/ShipporiMincho-Bold.ttf','700'),('WorkshopNumber','manrope/Manrope[wght].ttf','100 900')]:
            data=base64.b64encode((case/'fonts'/file).read_bytes()).decode('ascii')
            css=f'@font-face{{font-family:{family};src:url(data:font/ttf;base64,{data}) format("truetype");font-weight:{weight};}}\n'+css
        text=deck.read_text(encoding='utf-8')
        text += '\n\n<style>\n'+css+'\n</style>\n'
        deck.write_text(text,encoding='utf-8')
        (log_dir/'local-extensions.json').write_text(json.dumps({'css':'source/workshop.css','font_embedding':'unmodified official TTF as data URLs; fonts/OFL retained','bridge':'same-origin 0-based yebisu-slide / yebisu-page appended after MCP HTML export'},ensure_ascii=False,indent=2),encoding='utf-8')
        for fmt,name in [('html','index.html'),('pdf','deck.pdf'),('pptx','deck.pptx')]:
            print('MCP export:',fmt,flush=True)
            client.call('export_slide',{'filePath':str(deck),'format':fmt,'outputPath':str(case/name),'allowLocalFiles':True})
        html=(case/'index.html').read_text(encoding='utf-8')
        (case/'index.html').write_text(html.replace('</body>',BRIDGE+'\n</body>'),encoding='utf-8')
        import fitz
        render=case/'render';render.mkdir(exist_ok=True)
        with fitz.open(case/'deck.pdf') as pdf:
            for i,page in enumerate(pdf):page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(render/f'slide-{i+1:02}.png')
            print('MCP exports successful; PDF pages:',len(pdf),flush=True)
    finally:client.close(log_dir)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--case',type=Path,default=ROOT/'examples/repositories/marp-mcp-showcase')
    p.add_argument('--runtime',type=Path,default=ROOT/'.build/marp-mcp-runtime')
    p.add_argument('--node',type=Path,default=Path('C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'))
    p.add_argument('--marp-cli',type=Path,default=ROOT/'.build/repository-runtime/node_modules/@marp-team/marp-cli/marp-cli.js')
    p.add_argument('--probe',action='store_true')
    build(p.parse_args())
