"""Assemble Watermelon4000's sketch-note authoring route; no slide engine."""
from pathlib import Path
import base64, json, hashlib, difflib
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/sketch-note-showcase' if (ROOT / 'examples').exists() else ROOT
SOURCE = CASE / 'source'


def build():
    original = (SOURCE / 'controller.original.js').read_text(encoding='utf-8')
    controller = original.replace('  function go(idx) {', '''  function notifyParent() {
    if (parent !== window && location.origin !== 'null') {
      parent.postMessage({type:'yebisu-page',index:current}, location.origin);
    }
  }
  function go(idx) {''')
    controller = controller.replace('counter.textContent = `${current + 1} / ${total}`;', 'counter.textContent = `${current + 1} / ${total}`;\n    notifyParent();')
    controller += '''
  // Local adapter: preserve the original go() bounds and active-slide transition.
  addEventListener('message', e => {
    if (e.source !== parent || e.origin !== location.origin || e.data?.type !== 'yebisu-slide') return;
    if (Number.isInteger(e.data.index)) go(e.data.index);
  });
  window.deckPage = () => current;
  go(0);
'''
    (SOURCE / 'controller.js').write_text(controller, encoding='utf-8')
    (SOURCE / 'controller.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True), controller.splitlines(True), fromfile='upstream/demo/controller', tofile='source/controller.js')), encoding='utf-8')
    fonts = [
        ('Note Maru','zenmarugothic/ZenMaruGothic-Regular.ttf','400'),
        ('Note Maru','zenmarugothic/ZenMaruGothic-Bold.ttf','700'),
        ('Note Kaku','bizudpgothic/BIZUDPGothic-Regular.ttf','400'),
        ('Note Kaku','bizudpgothic/BIZUDPGothic-Bold.ttf','700'),
        ('Note Number','manrope/Manrope[wght].ttf','200 800'),
    ]
    font_css = ''
    font_records = []
    for name, path, weight in fonts:
        content = (SOURCE / 'fonts' / path).read_bytes()
        font_css += '@font-face{font-family:"'+name+'";font-style:normal;font-weight:'+weight+';font-display:block;src:url(data:font/ttf;base64,'+base64.b64encode(content).decode()+')}\n'
        font_records.append({'path':'source/fonts/'+path,'family_alias':name,'weight':weight,'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content),'source_url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+quote(path),'license_url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+path.split('/')[0]+'/OFL.txt','modified':False,'license':'OFL-1.1','commit':'66928797f271fed5ee428544e7229685e2d90127'})
    base = (SOURCE / 'upstream/style/sketch-notes-base.css').read_text(encoding='utf-8')
    reveal = (SOURCE / 'reveal.original.css').read_text(encoding='utf-8')
    local = (SOURCE / 'adaptation.css').read_text(encoding='utf-8')
    slides = (SOURCE / 'slides.html').read_text(encoding='utf-8')
    page = '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>文字のかたちを、観察する。</title><style>'+font_css+'\n'+base+'\n'+reveal+'\n'+local+'</style></head><body><div class="halftone"></div><div class="deck">'+slides+'</div><nav class="nav" aria-label="スライド操作"><button id="prev" title="前のページ" aria-label="前のページ">←</button><span class="counter" id="counter">1 / 6</span><button id="next" title="次のページ" aria-label="次のページ">→</button></nav><script>'+controller+'</script></body></html>'
    (CASE / 'index.html').write_text(page, encoding='utf-8')
    (SOURCE / 'FONT-SOURCE.json').write_text(json.dumps({'repository':'google/fonts','commit':'66928797f271fed5ee428544e7229685e2d90127','source':'Existing official pinned TTF files from downloads/fonts; no system font extraction','fonts':font_records},ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    print('Built single HTML: 6 pages, original sketch-notes CSS + demo go() controller + SKILL reveal rules.')


if __name__ == '__main__':
    build()
