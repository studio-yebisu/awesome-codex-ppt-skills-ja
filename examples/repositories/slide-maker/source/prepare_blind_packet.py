"""Copy actual render pixels to filenames recognized by the original blind_read CLI."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
C=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=C/'qa/original-blind-render';out.mkdir(parents=True,exist_ok=True);rows=[]
 for i in range(1,6):
  a=C/f'render/slide-{i:02}.png';b=out/f'slide{i:02}.png';shutil.copy2(a,b);assert sha(a)==sha(b);rows.append({'source':a.relative_to(C).as_posix(),'alias':b.relative_to(C).as_posix(),'sha256':sha(a)})
 (out/'sources.json').write_text(json.dumps({'scope':'Filename compatibility only; all pixels identical to current PowerPoint-PDF render','pages':rows},indent=2)+'\n',encoding='utf-8')
 r=subprocess.run([sys.executable,str(C/'source/upstream/skills/slide-maker/scripts/blind_read.py'),'packet',str(C),'--render-dir','qa/original-blind-render'],capture_output=True,text=True,encoding='utf-8')
 if r.returncode:raise SystemExit(r.stderr)
 (C/'qa/blind-packet.json').write_text(r.stdout,encoding='utf-8');print(r.stdout)
if __name__=='__main__':main()
