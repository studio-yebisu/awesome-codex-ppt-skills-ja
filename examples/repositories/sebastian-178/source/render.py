from playwright.sync_api import sync_playwright
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':900},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
 page.goto('http://127.0.0.1:8178/index.html?export=1');page.evaluate('document.fonts.ready');page.wait_for_timeout(300)
 nav=[];fits=[]
 for i in range(7):
  page.evaluate('(i)=>window.goToSlide(i)',i);page.wait_for_timeout(250)
  page.screenshot(path=str(P/f'render/slide-{i+1:02d}.png'))
  fits.append(page.evaluate('''()=>{let s=document.querySelector('.slide.active'), r=s.getBoundingClientRect(); return {title:s.dataset.title,overflow:[...s.querySelectorAll('header,.content,footer')].filter(e=>{let q=e.getBoundingClientRect();return q.bottom>r.bottom+1||q.right>r.right+1}).map(e=>e.className)}}'''))
 page.evaluate('window.goToSlide(0)');page.keyboard.press('ArrowRight');nav.append(page.locator('.slide.active').get_attribute('data-title'))
 page.keyboard.press('o');overview=page.evaluate('document.body.classList.contains("is-overview")');page.keyboard.press('Escape')
 page.goto('http://127.0.0.1:8178/index.html?print=1');page.evaluate('document.fonts.ready');page.pdf(path=str(P/'deck.pdf'),width='1600px',height='900px',print_background=True,prefer_css_page_size=True)
 (P/'QA.json').write_text(json.dumps({'scope':'初回browser表示・全頁PNG・arrow/overview・最小境界確認','browser':'system Chromium via Playwright','page_count':7,'page_errors':errors,'fits':fits,'arrow_next_title':nav,'overview_toggle':overview,'upstream_scripts_executed':False,'full_upstream_audits':False,'pdf_visual_review':'PNGと同じHTMLからChromium出力、別PDF全頁精査は未実施'},ensure_ascii=False,indent=2))
 b.close()
