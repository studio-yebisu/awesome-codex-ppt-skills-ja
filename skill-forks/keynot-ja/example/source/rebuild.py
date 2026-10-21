"""Keynot example shell/CSS/inline controller + extracted local brand content."""
from pathlib import Path
import json, base64, hashlib, difflib
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/keynot-showcase' if (ROOT/'examples').exists() else ROOT


def build():
    s=CASE/'source'
    brand=json.loads((CASE/'input/brand-record.json').read_text(encoding='utf-8'))
    # This input is an explicit text brand brief, not a PDF or URL extraction demo.
    import re
    brief=(CASE/'input/BRAND.md').read_text(encoding='utf-8')
    fields={'primary':'黒','accent':'赤','cream':'紙','stone':'罫線','ink':'黒','muted':'補足','white':'黒い面の文字'}
    evidence=[]
    for key,label in fields.items():
        match=re.search(r'^- '+re.escape(label)+r': (#[0-9a-fA-F]{6})',brief,re.M)
        if not match: raise ValueError('Missing exact brand value: '+label)
        brand[key]=match.group(1)
        evidence.append({'field':key,'source_label':label,'value':match.group(1),'line':brief[:match.start()].count('\n')+1})
    (CASE/'input/brand-record.json').write_text(json.dumps(brand,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (s/'brand-extraction.json').write_text(json.dumps({'source':'input/BRAND.md','source_sha256':hashlib.sha256(brief.encode()).hexdigest(),'scope':'Structured Japanese text brief; exact color entries parsed and carried into CSS. PDF/URL recognition is not exercised.','fields':evidence,'rules':['accent is a small rule/highlight, never a whole background','own text wordmark only','paper70/black28/red2 is a target, not a measurement']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    old_js=(s/'controller.original.js').read_text(encoding='utf-8')
    bridge='''
// Japanese case adapter appended to the untouched original controller.
(function () {
  function notifyParent() {
    if (parent !== window && location.origin !== 'null')
      parent.postMessage({type:'yebisu-page',index:cur}, location.origin);
  }
  addEventListener('message', e => {
    if (e.source !== parent || e.origin !== location.origin || e.data?.type !== 'yebisu-slide') return;
    if (Number.isInteger(e.data.index) && e.data.index >= 0 && e.data.index < slides.length) go(e.data.index);
  });
  new MutationObserver(notifyParent).observe(counter, {childList:true});
  notifyParent();
})();
'''
    js=old_js+bridge
    (s/'controller.js').write_text(js,encoding='utf-8')
    (s/'controller.patch').write_text(''.join(difflib.unified_diff(old_js.splitlines(True),js.splitlines(True),fromfile='upstream/example inline controller',tofile='source/controller.js')),encoding='utf-8')
    old_chrome=(s/'chrome.original.html').read_text(encoding='utf-8')
    chrome=old_chrome.replace('aria-label="Previous"','aria-label="前のページ"').replace('aria-label="Next"','aria-label="次のページ"').replace('aria-label="Fullscreen"','aria-label="全画面"').replace('1 / 5','1 / 6').replace('Rotate your device','端末を横向きに').replace('This deck is designed for landscape viewing. Turn your phone sideways to continue.','横向きの画面でご覧ください。端末を横にすると、続きを表示します。')
    (s/'chrome.ja.html').write_text(chrome,encoding='utf-8')
    (s/'chrome.patch').write_text(''.join(difflib.unified_diff(old_chrome.splitlines(True),chrome.splitlines(True),fromfile='upstream/example navigation and rotate overlay',tofile='source/chrome.ja.html')),encoding='utf-8')
    font_css='';records=[]
    for alias,path,weight in [
        ('Holiday Serif','shipporimincho/ShipporiMincho-Regular.ttf','400'),
        ('Holiday Sans','bizudpgothic/BIZUDPGothic-Regular.ttf','400'),
        ('Holiday Sans','bizudpgothic/BIZUDPGothic-Bold.ttf','700'),
        ('Holiday Number','spacegrotesk/SpaceGrotesk[wght].ttf','300 700')]:
        content=(s/'fonts'/path).read_bytes()
        font_css+='@font-face{font-family:"'+alias+'";font-weight:'+weight+';font-style:normal;font-display:block;src:url(data:font/ttf;base64,'+base64.b64encode(content).decode()+')}\n'
        records.append({'path':'source/fonts/'+path,'family_alias':alias,'weight':weight,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'modified':False,'license':'OFL-1.1','commit':'66928797f271fed5ee428544e7229685e2d90127','source_url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+quote(path),'license_url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+path.split('/')[0]+'/OFL.txt'})
    brand_css='/* Extracted from input/BRAND.md: paper70/black28/red2 target; accent never a whole background. */\n:root{'+''.join('--'+name+':'+brand[name]+';' for name in ['primary','accent','cream','stone','ink','muted','white'])+'--blood:var(--accent);--serif:"Holiday Serif";--sans:"Holiday Sans";--numbers:"Holiday Number";}\n'
    original_css=(s/'base.original.css').read_text(encoding='utf-8')
    local_css=(s/'adaptation.css').read_text(encoding='utf-8')
    content=(s/'slides.html').read_text(encoding='utf-8')
    licenses={'repository':'shawnzam/keynot','commit':'d1f9e449ddb89da707b489cb69c520a64975b47c','copyright':'2026 Shawn Zamechek','license':(s/'upstream/LICENSE').read_text(encoding='utf-8'),'modifications':'Japanese content and brand/font/layout overrides; original inline controller retained verbatim before appended same-origin adapter','font_licenses':{family:(s/'fonts'/family/'OFL.txt').read_text(encoding='utf-8') for family in ['shipporimincho','bizudpgothic','spacegrotesk']}}
    html='<!DOCTYPE html><!-- Keynot MIT Copyright2026 Shawn Zamechek; local Japanese brand/content adaptation; full license texts embedded. --><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>紙と、インクの休日。</title><style>'+font_css+original_css+'\n'+brand_css+local_css+'</style></head><body><div class="deck" id="deck">'+content+'</div>'+chrome+'<script type="application/json" id="license-notices">'+json.dumps(licenses,ensure_ascii=False).replace('</','<'+chr(92)+'/')+'</script><script>'+js+'</script></body></html>'
    (CASE/'index.html').write_text(html,encoding='utf-8')
    (s/'FONT-SOURCE.json').write_text(json.dumps({'repository':'google/fonts','commit':'66928797f271fed5ee428544e7229685e2d90127','source':'Existing official fixed TTF/OFL distribution; no OS extraction','fonts':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (s/'brand-and-layout.patch').write_text(''.join(difflib.unified_diff(original_css.splitlines(True),(original_css+'\n'+brand_css+local_css).splitlines(True),fromfile='upstream/example inline CSS',tofile='source/CSS with appended local overrides')),encoding='utf-8')
    print('Built6-page Keynot single HTML; original example controller verbatim + appended bridge, original CSS + local brand/layout overrides.')


if __name__=='__main__':build()
