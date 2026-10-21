from pathlib import Path
import subprocess,sys,os,json,hashlib
P=Path(__file__).parent
args=[sys.executable,'-m','editppt.cli']+sys.argv[2:]
r=subprocess.run(args,cwd=P,capture_output=True,text=True,encoding='utf8',errors='replace');log=P/sys.argv[1];log.write_text(r.stdout+r.stderr,'utf8');p=P/'cli-receipts.json';d=json.loads(p.read_text('utf8'))if p.exists()else[];d.append({'argv':args,'exit_code':r.returncode,'log':log.name,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()});p.write_text(json.dumps(d,indent=2),'utf8');print(r.stdout+r.stderr);raise SystemExit(r.returncode)
