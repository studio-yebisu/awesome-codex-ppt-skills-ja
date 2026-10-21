"""Bounded real proof of the pinned CLI, separate from the MCP-authored main sample."""
from pathlib import Path
import argparse,subprocess,json,os,hashlib
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 c=a.case.resolve();work=c/'.private/cli-round5';work.mkdir(parents=True,exist_ok=False)
 env=os.environ.copy();env['MARP_CLI_JS']=str(a.marp_cli.resolve());commands=[]
 def run(args):
  p=subprocess.run([str(a.node),str(a.runtime.resolve()/'build/index.js')]+args,env=env,cwd=c,capture_output=True,text=True,encoding='utf-8');p.check_returncode()
  commands.append({'arguments':[s.replace(str(work),'<test-work>')for s in args],'exit_code':p.returncode,'stdout':p.stdout.replace(str(work),'<test-work>'),'stderr':p.stderr.replace(str(work),'<test-work>')});return p.stdout
 run(['--version']);run(['-t','default','-s','minimal','list-layouts']);file=str(work/'cli-deck.md')
 run(['-s','minimal','create',file,'--title','ページをIDで更新する','--subtitle','元CLIの独立操作確認'])
 run(['-s','minimal','set-frontmatter',file,'--header','操作確認','--paginate'])
 run(['-s','minimal','manage',file,'-l','content','-p',json.dumps({'heading':'更新前','body':'最初の本文'},ensure_ascii=False)])
 run(['generate-ids',file]);first=json.loads(run(['read',file]));target=first['slides'][1]['slideId']
 run(['-s','minimal','manage',file,'--mode','replace','--slide-id',target,'-l','content','-p',json.dumps({'heading':'更新後','body':'IDで指定した本文だけを変更'},ensure_ascii=False)])
 after=json.loads(run(['read',file,'--slide-id',target]));assert after['slideId']==target
 before_ids=[x['slideId']for x in json.loads(run(['read',file]))['slides']]
 run(['generate-ids',file]);after_ids=[x['slideId']for x in json.loads(run(['read',file]))['slides']];assert before_ids==after_ids
 run(['export',file,'-f','html','-o',str(work/'cli-deck.html')])
 run(['export',file,'-f','pdf','-o',str(work/'cli-deck.pdf')])
 result={'author':'Codex','source_skill':'source/upstream/skills/marp/SKILL.md','runtime_index_byte_identical_to_distributed':sha(a.runtime.resolve()/'build/index.js')==sha(c/'source/runtime/build/index.js'),'commands':commands,'id_retained_after_replace':True,'generate_ids_idempotent':True,'target_slide_id':target,'before_heading':'更新前','after_heading':'更新後','html_bytes':(work/'cli-deck.html').stat().st_size,'pdf_bytes':(work/'cli-deck.pdf').stat().st_size,'scope':'This is an independent two-page CLI exercise. The full six-page sample is produced through the same repository MCP implementation. Agenda/image transition are not exercised.'}
 (c/'source/round5-cli-proof.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print('Original CLI list/create/set-frontmatter/manage/read/generate-ids/export HTML/PDF passed')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--case',type=Path,required=True);p.add_argument('--runtime',type=Path,required=True);p.add_argument('--node',type=Path,required=True);p.add_argument('--marp-cli',type=Path,required=True);main(p.parse_args())
