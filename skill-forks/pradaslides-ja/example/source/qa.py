from pathlib import Path
import threading,http.server,functools,argparse,shutil
from reproduce import run,ROOT
def main():
 parser=argparse.ArgumentParser(description='Run PradaSlides presenter QA over local HTTP.')
 parser.add_argument('--node',default=shutil.which('node'),help='Absolute path to Node.js; defaults to node on PATH')
 args=parser.parse_args()
 if not args.node:parser.error('Node.js was not found on PATH; specify --node with its absolute path.')
 node=Path(args.node)
 if not node.is_absolute() or not node.is_file():parser.error('--node must point to an existing absolute Node.js executable path.')
 class Handler(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 try:return run('html-qa',[str(node),'source/qa_http.mjs','--entry','presenter/index.html','--url',f'http://127.0.0.1:{server.server_port}/presenter/index.html','--count','6','--output','review/html-qa.json','--deck-plan','project/deck-plan.json','--render-dir','review/html-render','--console-shot','review/console.png'])
 finally:server.shutdown();server.server_close()
if __name__=='__main__':raise SystemExit(main())
