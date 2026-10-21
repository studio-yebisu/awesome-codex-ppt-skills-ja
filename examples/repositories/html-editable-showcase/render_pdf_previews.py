"""Mechanically rasterize an actual PowerPoint PDF; do not repaint slides."""
from pathlib import Path
import argparse,hashlib,json
import pypdfium2 as pdfium
def main():
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);p.add_argument('--pdf-name',default='deck.pdf');p.add_argument('--single-output');p.add_argument('--page',type=int,default=1);a=p.parse_args();pdf=a.directory/a.pdf_name;doc=pdfium.PdfDocument(pdf);rows=[]
    assert 1<=a.page<=len(doc)
    for i in ([a.page-1]if a.single_output else range(len(doc))):
        page=doc[i];bitmap=page.render(scale=900/page.get_height());im=bitmap.to_pil().convert('RGB')
        if im.size!=(1600,900):im=im.resize((1600,900))
        out=a.directory/(a.single_output if a.single_output else f'slide-{i+1:02}.png');im.save(out);rows.append({'index':i,'path':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()});bitmap.close();page.close()
    doc.close();(a.directory/(Path(a.single_output).stem+'-render.json'if a.single_output else 'pdf-preview.json')).write_text(json.dumps({'source_pdf':a.pdf_name,'source_pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'method':'Actual PowerPoint PDF -> PDFium RGB1600x900','pages':rows},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
