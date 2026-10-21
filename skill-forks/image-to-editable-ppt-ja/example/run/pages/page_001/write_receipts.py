import json,hashlib
from pathlib import Path
p=Path(__file__).parent
sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest()
py='M:/Codex/Projects/awesome-codex-ppt-skills-ja/.build/ppt-master-venv/Scripts/python.exe'
out='M:/Codex/home/generated_images/01a13676-80b6-77c0-9cab-7642d16bb48d/exec-a8b58b27-f2bf-47fa-be55-334185e401be.png'
r={'tool':'image_gen.imagegen','arguments':{'prompt':(p/'asset-sheet.prompt.txt').read_text(encoding='utf-8-sig').strip(),'referenced_image_paths':[str(p/'source.png')],'transparent_background':False},'input_sha256':sha(p/'source.png'),'returned_output_path':out,'returned_output_sha256':sha(out),'imported_output':'assets/icon-sheet.png','imported_output_sha256':sha(p/'assets/icon-sheet.png')}
(p/'builtin-imagegen-receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
commands=[('import.log',0,['image','import',str(p),'--job-id','icon-sheet','--source-image',out,'--dest','assets/icon-sheet.png','--role','asset_sheet','--backend','builtin-imagegen']),('process-sheet.log',1,['image','process-sheet',str(p),'--job-id','icon-sheet','--asset-sheet-source','assets/icon-sheet.png','--regions','assets/asset-regions.json','--assets-dir','assets/icons']),('process-sheet-repair.log',0,['image','process-sheet',str(p),'--job-id','icon-sheet','--skip-chroma','--regions','assets/asset-regions.json','--assets-dir','assets/icons']),('build.log',0,['page','build',str(p)]),('contact-sheet.log',0,['page','contact-sheet',str(p)]),('validate.log',0,['page','validate',str(p),'--report',str(p/'validation.json')])]
(p/'cli-receipts.json').write_text(json.dumps([{'argv':[py,'-m','editppt.cli']+args,'exit_code':code,'log':log,'log_sha256':sha(p/log)} for log,code,args in commands],ensure_ascii=False,indent=2),encoding='utf-8')
