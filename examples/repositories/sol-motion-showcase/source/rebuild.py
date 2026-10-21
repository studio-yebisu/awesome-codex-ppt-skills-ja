"""Rebuild the offline single HTML with Python standard library only."""
from pathlib import Path
import base64, json
root=Path(__file__).resolve().parents[1]
src=root/'source'
font_css=[]
for item in json.loads((src/'font-map.json').read_text(encoding='utf-8')):
    data=base64.b64encode((root/'fonts'/item['file']).read_bytes()).decode()
    font_css.append("@font-face{font-family:"+item['family']+";src:url(data:font/ttf;base64,"+data+") format('truetype');font-weight:100 900;font-display:block}")
html=(src/'document-template.html').read_text(encoding='utf-8')
for token,value in [('FONTS',''.join(font_css)),('BASE',(src/'viewport-base.css').read_text(encoding='utf-8')),('CSS',(src/'adaptation.css').read_text(encoding='utf-8')),('SLIDES',(src/'slides.html').read_text(encoding='utf-8')),('EDITOR',(src/'editor-ui.html').read_text(encoding='utf-8')),('JS',(src/'controller.js').read_text(encoding='utf-8'))]:
    html=html.replace('__'+token+'__',value)
(root/'index.html').write_text(html,encoding='utf-8')
print(root/'index.html')
