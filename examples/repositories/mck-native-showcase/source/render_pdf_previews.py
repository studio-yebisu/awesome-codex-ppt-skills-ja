"""RGB PNG previews from actual PowerPoint-exported PDF; direct PNGs retained."""
from pathlib import Path
import json,hashlib,shutil,sys
import pypdfium2 as pdfium
def render(directory):
 pdf=directory/'deck.pdf'
 if not pdf.is_file():return
 raw=directory/'direct-png';raw.mkdir(exist_ok=True)
 previous={x['image']:x['sha256'] for x in json.loads((directory/'pdf-preview.json').read_text(encoding='utf-8')).get('images',[])} if (directory/'pdf-preview.json').exists() else {}
 for p in directory.glob('slide-??.png'):
  if hashlib.sha256(p.read_bytes()).hexdigest()!=previous.get(p.name):shutil.copy2(p,raw/p.name)
 doc=pdfium.PdfDocument(pdf);rows=[]
 for i in range(len(doc)):
  pg=doc[i];bitmap=pg.render(scale=900/pg.get_height());im=bitmap.to_pil().convert('RGB')
  if im.size!=(1600,900):im=im.resize((1600,900))
  out=directory/f'slide-{i+1:02}.png';im.save(out)
  rows.append({'index':i,'image':out.name,'size':[1600,900],'mode':'RGB','sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
  bitmap.close();pg.close()
 doc.close()
 (directory/'pdf-preview.json').write_text(json.dumps({'source':'deck.pdf','source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'method':'PowerPoint16 exported PDF rasterized via PDFium; direct PowerPoint PNGs retained in direct-png/','pptx_modified':False,'images':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
 for value in sys.argv[1:]:render(Path(value).resolve())
