"""Read fonts actually embedded/referenced in the exported PDF (PyMuPDF)."""
from pathlib import Path
import hashlib,json
import fitz
CASE=Path(__file__).resolve().parents[1]
pdf=CASE/'render/deck.pdf'
with fitz.open(pdf) as d:
    rows=[{'page':i+1,'fonts':[{'xref':f[0],'extension':f[1],'type':f[2],'basefont':f[3],'resource':f[4],'encoding':f[5]} for f in p.get_fonts(full=True)]} for i,p in enumerate(d)]
(CASE/'source/pdf-fonts.json').write_text(json.dumps({'source':'render/deck.pdf','source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'method':'PyMuPDF get_fonts(full=True); actual exported PDF, not requested font names','pages':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Read actual PDF fonts for',len(rows),'pages')
