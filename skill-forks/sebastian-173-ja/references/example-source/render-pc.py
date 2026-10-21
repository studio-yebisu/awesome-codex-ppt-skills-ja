from pathlib import Path
from playwright.sync_api import sync_playwright
import json, subprocess, os
R=Path(__file__).resolve().parent.parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE',r'C:\Program Files\Google\Chrome\Application\chrome.exe'),args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 page.goto((R/'index.html').as_uri());page.evaluate('document.fonts.ready')
 initial=page.evaluate('window.deckPage()')
 page.keyboard.press('ArrowRight');next_=page.evaluate('window.deckPage()')
 page.keyboard.press('ArrowLeft');prev=page.evaluate('window.deckPage()')
 page.evaluate('document.body.classList.add("render-mode")')
 overflow=[]
 for i in range(7):
  page.evaluate(f'window.deckShow({i})')
  page.screenshot(path=str(R/f'render/slide-{i+1:02}.png'))
  overflow+=page.evaluate('''()=>[...document.querySelectorAll('.slide.active .frame > *')].filter(e=>{const r=e.getBoundingClientRect();return r.bottom>980||r.right>1820||r.left<100}).map(e=>({page:window.deckPage()+1,tag:e.tagName,class:e.className,rect:e.getBoundingClientRect().toJSON()}))''')
 page.pdf(path=str(R/'deck.pdf'),width='1920px',height='1080px',print_background=True,prefer_css_page_size=False)
 b.close()
 subprocess.run(['gs','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.4','-dPDFSETTINGS=/ebook','-dNOPAUSE','-dQUIET','-dBATCH',f'-sOutputFile={R / "deck-lite.pdf"}',str(R/'deck.pdf')],check=True)
 (R/'QA.json').write_text(json.dumps({'render_engine':'Chromium via Playwright','initial_page':initial,'arrow_right_page':next_,'arrow_left_page':prev,'page_count':7,'layout_overflow':overflow,'visual_review':'pending','upstream_full_qa':False,'audio_playback':False},ensure_ascii=False,indent=2))
