"""Refresh atelier counts without restoring the superseded 209-task policy."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
product=json.loads((ROOT/'data/product-collection.json').read_text(encoding='utf-8'))
cases=json.loads((ROOT/'data/case-studies.json').read_text(encoding='utf-8'))
active=[c for c in cases if c['id'] in product['active_case_ids']]
path=ROOT/'README.md'
text=path.read_text(encoding='utf-8')
pages=sum(c['page_count'] for c in active if c.get('page_unit')!='段階')
steps=sum(c['page_count'] for c in active if c.get('page_unit')=='段階')
summary=f'厳選{len(product["entries"])}スキルと、日本語の作例{len(active)}冊・{pages}枚'+(f'、{steps}段階の演出' if steps else '')+'。'
text=re.sub(r'厳選\d+スキルと、日本語の作例\d+冊・\d+枚(?:、\d+段階の演出)?。',summary,text)
text=re.sub(r'制作履歴は\d+リポ・\d+冊',f'制作履歴は{len(set(c["repository"] for c in cases))}リポ・{len(cases)}冊',text)
path.write_text(text,encoding='utf-8',newline='\n')
print('Atelier README counts refreshed; historical QA unchanged')
