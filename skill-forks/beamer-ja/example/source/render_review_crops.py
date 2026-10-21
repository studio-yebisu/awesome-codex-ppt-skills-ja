"""Re-render the recorded review regions from the current PDF; no compilation or QA scoring."""
from pathlib import Path
import hashlib,json
import pymupdf
case=Path(__file__).resolve().parents[1]
p=case/'reviews/crop-index.json';index=json.loads(p.read_text('utf-8'));pdf=case/'deck.pdf'
with pymupdf.open(pdf) as doc:
 for item in index['crops']:
  dest=case/item['file'];dest.parent.mkdir(parents=True,exist_ok=True)
  doc[item['page']-1].get_pixmap(dpi=item['dpi'],clip=pymupdf.Rect([v*72/2.54 for v in item['clip_cm']])).save(dest)
  item['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
index['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest();p.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n','utf-8')
print('Rendered',len(index['crops']),'review crops from current PDF.')
