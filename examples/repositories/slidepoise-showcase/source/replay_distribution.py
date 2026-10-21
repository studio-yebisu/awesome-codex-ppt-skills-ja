"""Replay a published example ZIP through the original reconstruction runtime."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,zipfile
CASE=Path(__file__).resolve().parents[1];ROOT=CASE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 archive=ROOT/'downloads/slidepoise-example-ja.zip';target=CASE/'.private/distribution-replay-20261015';target.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None;assert all(not(set(Path(n).parts)&{'.private','node_modules','.git','.venv','__pycache__'}) for n in z.namelist());z.extractall(target)
 extracted=target/'slidepoise-example-ja';result=subprocess.run([sys.executable,str(extracted/'rebuild.py')],env=os.environ.copy(),capture_output=True,text=True,encoding='utf-8',check=True)
 with zipfile.ZipFile(CASE/'deck.pptx') as a,zipfile.ZipFile(extracted/'deck.pptx') as b:
  slides=[n for n in a.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')];different=[n for n in slides if a.read(n)!=b.read(n)]
 assert len(slides)==3 and not different
 record={'archive_sha256':sha(archive),'actual_route':'ZIP extraction, original normalizer/reconstruct-slide/OpenCV/contract/constructor/render-deck','exit_code':result.returncode,'native_slide_xml_compared':3,'native_slide_xml_differences':different,'dependency_scope':'Existing locked Python/OpenCV and Node dependencies; dependencies are not shipped in ZIP.','current_source_pptx_sha256':sha(CASE/'deck.pptx')}
 (CASE/'source/zip-replay.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(record))
if __name__=='__main__':main()
