"""Reassemble the frozen, actually generated images through the unmodified upstream CLI.

This does not generate images, obtain approvals, or fabricate worker receipts.
The temporary project directory satisfies the original filename/stem contract.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
CASE=Path(__file__).resolve().parents[1]
def main():
 cli=CASE/'source/upstream/skills/codex-ppt/scripts/assemble_ppt.py'
 images=sorted((CASE/'origin_image').glob('slide_*.png'))
 assert len(images)==3
 with tempfile.TemporaryDirectory(prefix='codex-image-replay-') as tmp:
  base=Path(tmp).resolve();project=base/'codex-image-ppt';project.mkdir();shutil.copytree(CASE/'origin_image',project/'origin_image');shutil.copy2(CASE/'speech.md',project/'speech.md')
  argv=[sys.executable,str(cli),str(base),'codex-image-ppt.pptx','--aspect-ratio','16:9']
  r=subprocess.run(argv,cwd=CASE,capture_output=True,text=True,encoding='utf-8',errors='replace')
  (CASE/'source/current-assemble.log').write_text(r.stdout+r.stderr,encoding='utf-8')
  if r.returncode:raise SystemExit(r.returncode)
  shutil.copy2(project/'codex-image-ppt.pptx',CASE/'codex-image-ppt.pptx')
 receipt={'command':['python','source/upstream/skills/codex-ppt/scripts/assemble_ppt.py','<temporary-parent>','codex-image-ppt.pptx','--aspect-ratio','16:9'],'exit_code':r.returncode,'temporary_project_contract':'Frozen images/speech copied unchanged into a temporary codex-image-ppt folder; original CLI output copied to delivered filename without postprocessing','artifact_sha256':hashlib.sha256((CASE/'codex-image-ppt.pptx').read_bytes()).hexdigest(),'image_generation_repeated':False,'new_output_requires_visual_review':True}
 (CASE/'source/current-assemble.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (CASE/'QA.json').write_text(json.dumps({'status':'generated_awaiting_review','artifact_sha256':receipt['artifact_sha256'],'prior_review_not_transferred':True},indent=2)+'\n',encoding='utf-8')
 print(r.stdout)
if __name__=='__main__':main()
