import json, subprocess, os, sys, hashlib
from pathlib import Path
p=Path(__file__).parent
for k in ['OPENAI_API_KEY','OPENAI_BASE_URL','PADDLE_OCR_TOKEN']:os.environ.pop(k,None)
config=p.parents[2]/'source'/'offline-config'
os.environ.update(EDITPPT_CONFIG_HOME=str(config),CODEX_AUTH_FILE=str(config/'no-auth.json'),CODEX_PPT_HOME=str(config/'no-codex-ppt'))
args=[sys.executable,'-m','editppt.cli']+sys.argv[2:]
r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
log=p/sys.argv[1];log.write_text(r.stdout+r.stderr,encoding='utf-8')
rec=p/'cli-receipts.json'; receipts=json.loads(rec.read_text()) if rec.exists() else []
receipts.append({'argv':args,'exit_code':r.returncode,'log':log.name,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
rec.write_text(json.dumps(receipts,ensure_ascii=False,indent=2),encoding='utf-8')
print(r.stdout+r.stderr);sys.exit(r.returncode)
