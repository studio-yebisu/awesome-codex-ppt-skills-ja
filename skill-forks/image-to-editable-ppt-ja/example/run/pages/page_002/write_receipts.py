import json,hashlib
from pathlib import Path
p=Path(__file__).parent
sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest()
out='M:/Codex/home/generated_images/01a13676-80b6-77c0-9cab-7642d16bb48d/exec-cf36825b-4100-4fdf-95ee-fea101ae7a2f.png'
r={'tool':'image_gen.imagegen','arguments':{'prompt':(p/'asset-sheet.prompt.txt').read_text(encoding='utf-8-sig').strip(),'referenced_image_paths':[str(p/'source.png')],'transparent_background':False},'input_sha256':sha(p/'source.png'),'returned_output_path':out,'returned_output_sha256':sha(out),'imported_output':'assets/icon-sheet.png','imported_output_sha256':sha(p/'assets/icon-sheet.png')}
(p/'builtin-imagegen-receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
v=json.loads((p/'validation.json').read_text(encoding='utf-8'));m=json.loads((p/'manifest.json').read_text(encoding='utf-8'))
v['visual_review']={'completed':True,'warnings':m['warnings'],'evidence':m['quality_checks']['evidence'],'application_render_verified':False}
(p/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
