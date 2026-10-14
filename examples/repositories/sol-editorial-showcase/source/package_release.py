"""Package the two owned editorial kits only; never edits shared catalogs."""
from pathlib import Path
import json, shutil, hashlib, zipfile

ROOT=Path(__file__).resolve().parents[4]
CASE=ROOT/'examples/repositories/sol-editorial-showcase'
FORK=ROOT/'skill-forks/sol-editorial-ja'
UP=ROOT/'.build/actual-upstreams/likaku__Mck-ppt-design-skill'

def dump(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for dst in [CASE,FORK]:
    for d in ['mck_ppt','references']:
        shutil.copytree(UP/d,dst/'upstream'/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for name in ['LICENSE','NOTICE','SKILL.md']:
        shutil.copy2(UP/name,dst/'upstream'/name)
    for family in ['zenkakugothicnew','shipporimincho','spacegrotesk']:
        shutil.copytree(ROOT/'downloads/fonts'/family,dst/'fonts'/family,dirs_exist_ok=True)
    shutil.copy2(ROOT/'tools/build_sol_editorial_showcase.py',dst/'source/build_sol_editorial_showcase.py')
shutil.copy2(CASE/'source/rebuild.py',FORK/'source/rebuild.py')
shutil.copytree(CASE/'input',FORK/'input',dirs_exist_ok=True)
shutil.copy2(CASE/'PROMPT.txt',FORK/'PROMPT.txt')
shutil.copy2(CASE/'README.md',FORK/'README.md')
shutil.copy2(ROOT/'tools/render_powerpoint.ps1',CASE/'source/render_powerpoint.ps1')
shutil.copy2(ROOT/'tools/render_powerpoint.ps1',FORK/'source/render_powerpoint.ps1')
for dst in [CASE,FORK]:
    files=[f for f in sorted(dst.rglob('*')) if f.is_file() and not any(p in {'__pycache__','.build','cache'} for p in f.parts) and f.suffix!='.pyc' and f.name!='SOURCE.json']
    dump(dst/'SOURCE.json',{'repository':'likaku/Mck-ppt-design-skill','commit':'e190e083b715b63172e1c4fea01bc5f9bb21a021','license':'Apache-2.0','case_studies':['sol-editorial-showcase'],'modified':True,'changes':'Six explicit native MckEngine layout overrides and Japanese editorial content; upstream source unmodified.','files':[{'path':f.relative_to(dst).as_posix(),'sha256':sha(f)} for f in files]})
    name='sol-editorial-example-ja' if dst==CASE else 'sol-editorial-ja'
    target=ROOT/'downloads'/f'{name}.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(dst.rglob('*')):
            if f.is_file() and not any(p in {'__pycache__','.build','cache'} for p in f.parts) and f.suffix!='.pyc':
                z.write(f,Path(name)/f.relative_to(dst))
    print(f'{target.name}: {target.stat().st_size} bytes; SHA256 {sha(target)}')
fragment=ROOT/'data/sol-editorial-repository-examples.json'
records=json.loads(fragment.read_text(encoding='utf-8-sig'))
records[0]['source_download']='downloads/sol-editorial-example-ja.zip'
records[0]['fork_download']='downloads/sol-editorial-ja.zip'
dump(fragment,records)
