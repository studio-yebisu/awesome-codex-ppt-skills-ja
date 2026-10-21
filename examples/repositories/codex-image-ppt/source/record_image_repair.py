"""Record one selected built-in image repair with original state/dispatch/result APIs."""
from pathlib import Path
import argparse,sys,json,shutil,subprocess
CASE=Path(__file__).resolve().parents[1];SCRIPTS=CASE/'source/upstream/skills/codex-ppt/scripts'
sys.path.insert(0,str(SCRIPTS))
from slide_run_state import locked_jobs,find_slide,update_jobs_run_status
p=argparse.ArgumentParser();p.add_argument('--selected-source',type=Path,required=True);p.add_argument('--agent-id',required=True);a=p.parse_args();a.selected_source=a.selected_source.resolve()
repair=CASE/'source/imagegen-repair';repair.mkdir(exist_ok=True)
before=repair/'previous-slide-jobs.json'
if not before.exists():shutil.copy2(CASE/'slide_jobs.json',before)
job=json.loads((CASE/'prompts/slide_03.json').read_text(encoding='utf-8'));info=json.loads((CASE/'source/imagegen-repair.json').read_text(encoding='utf-8'));job['prompt']=info['prompt'];job['input_images']=[{'path':'source/imagegen-repair/slide-03-before.png','role':'edit-target'}]
prompt=repair/'slide-03-repair-job.json';prompt.write_text(json.dumps(job,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# There is no public reset CLI. Use original locked state APIs, preserving old
# dispatch/results before reopening exactly this completed job for repair.
with locked_jobs(CASE) as jobs:
 slide=find_slide(jobs,'slide_03');slide['status']='pending';slide['dispatch']=None;slide['result']=None;update_jobs_run_status(jobs)
receipts=json.loads((repair/'state-receipts.json').read_text(encoding='utf-8')) if (repair/'state-receipts.json').exists() else []
for argv in [[sys.executable,SCRIPTS/'record_slide_dispatch.py',CASE,'--slide','slide_03','--agent-id',a.agent_id,'--agent-nickname','Codex native5 repair worker','--prompt-file',prompt],[sys.executable,SCRIPTS/'record_slide_result.py',CASE,'--slide','slide_03','--agent-id',a.agent_id,'--backend-used','built-in image_gen.imagegen','--selected-source',a.selected_source,'--qa-note','One local spacing edit made with the built-in image tool. Exact text/commands retained and source/output visually inspected. The candidate was generated before the repair dispatch receipt was refreshed; full chronological generation/approval-gate compliance is not claimed.']]:
 r=subprocess.run(list(map(str,argv)),cwd=CASE,capture_output=True,text=True,encoding='utf-8',errors='replace');receipts.append({'argv':list(map(str,argv)),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});(repair/'state-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(r.stdout+r.stderr);assert r.returncode==0
