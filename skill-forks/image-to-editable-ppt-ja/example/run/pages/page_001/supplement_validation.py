import json
from pathlib import Path
p=Path(__file__).parent
v=json.loads((p/'validation.json').read_text(encoding='utf-8'))
m=json.loads((p/'manifest.json').read_text(encoding='utf-8'))
v['visual_review']={'completed':True,'warnings':m['warnings'],'evidence':m['quality_checks']['evidence'],'application_render_verified':False}
(p/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
