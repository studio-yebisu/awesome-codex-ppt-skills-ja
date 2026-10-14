"""Compile the extracted Design DNA and Page Specs into original-rule HTML."""
from pathlib import Path
from html import escape
import json, base64, hashlib
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/design-dna-showcase' if (ROOT / 'examples').exists() else ROOT


def build():
    src = CASE / 'source'
    dna = json.loads((CASE / 'input/design-dna.json').read_text(encoding='utf-8'))
    specs = json.loads((CASE / 'specs/page-specs.json').read_text(encoding='utf-8'))
    font_css = ''
    fonts = []
    for alias, path, weight in [
        ('DNA Heading','zenkakugothicnew/ZenKakuGothicNew-Black.ttf','900'),
        ('DNA Sans','zenkakugothicnew/ZenKakuGothicNew-Regular.ttf','400'),
        ('DNA Body','bizudpmincho/BIZUDPMincho-Regular.ttf','400'),
        ('DNA Number','manrope/Manrope[wght].ttf','200 800'),
    ]:
        raw=(src/'fonts'/path).read_bytes()
        font_css+='@font-face{font-family:"'+alias+'";font-style:normal;font-weight:'+weight+';font-display:block;src:url(data:font/ttf;base64,'+base64.b64encode(raw).decode()+')}\n'
        fonts.append({'path':'source/fonts/'+path,'family_alias':alias,'weight':weight,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'source_url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+quote(path),'license_url':'https://raw.githubusercontent.com/google/fonts/66928797f271fed5ee428544e7229685e2d90127/ofl/'+path.split('/')[0]+'/OFL.txt','modified':False,'license':'OFL-1.1','commit':'66928797f271fed5ee428544e7229685e2d90127'})
    tokens=':root{'+''.join('--'+key+':'+str(value)+';' for key,value in dna['tokens'].items())+'}\n'
    slides=[]
    for spec in specs:
        parts=[]
        for zone in spec['zones']:
            box=zone['box']
            style='position:absolute;left:'+str(box['x'])+'px;top:'+str(box['y'])+'px;width:'+str(box['w'])+'px;height:'+str(box['h'])+'px;'
            role=zone['role']
            if role=='title':
                inner='<h1 class="headline" style="font-size:'+str(zone['font_size'])+'px;line-height:'+str(zone['line_height'])+'">'+escape(zone['text']).replace('\n','<br>')+'</h1>'
            elif role in ['eyebrow','body','lead','footer'] and 'html' not in zone:
                cl={'eyebrow':'eyebrow','body':'copy','lead':'lead','footer':'foot'}[role]
                inner='<p class="'+cl+'" style="font-size:'+str(zone['font_size'])+'px;line-height:'+str(zone['line_height'])+'">'+escape(zone['text']).replace('\n','<br>')+'</p>'
            else:inner=zone['html']
            parts.append('<header class="zone '+zone.get('class','')+'" data-zone="'+role+'" style="'+style+'">'+inner+'</header>')
        slides.append('<section class="slide'+(' active' if spec['page_number']==1 else '')+'" data-page="'+str(spec['page_number']).zfill(2)+'" data-layout="'+spec['layout']['archetype']+'" data-density="balanced">'+''.join(parts)+'</section>')
    css=(src/'fixed-stage.original.css').read_text(encoding='utf-8')+'\n'+(src/'adaptation.css').read_text(encoding='utf-8')
    controller=(src/'controller.js').read_text(encoding='utf-8')
    budgets=[{'page_number':x['page_number'],'layout_box_budget':x['layout_box_budget'],'mechanical_layout_preflight':x['mechanical_layout_preflight']} for x in specs]
    licenses={'upstream':{'repository':'dakjdakd/PPT-Design-DNA','commit':'5d1d84cf952f16920d893b6c04bd7cb7cff9d155','copyright':'2026 dakjdakd','license':(src/'upstream/LICENSE').read_text(encoding='utf-8'),'changes':'Japanese extraction/specs/layout/navigation authored locally; original guard preserved unchanged'},'fonts':{family:(src/'fonts'/family/'OFL.txt').read_text(encoding='utf-8') for family in ['zenkakugothicnew','bizudpmincho','manrope']}}
    doc='<!doctype html><!-- Derived under Apache-2.0 from PPT-Design-DNA, Copyright 2026 dakjdakd. Local Japanese adaptation; license texts embedded below. --><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>町の道具を、借り合う。</title><style>'+font_css+tokens+css+'</style></head><body><div class="viewport"><main class="stage">'+''.join(slides)+'<nav class="navigation" aria-label="スライド操作"><button id="prev" aria-label="前のページ">←</button><span id="counter">01 / 06</span><button id="next" aria-label="次のページ">→</button></nav></main></div><script type="application/json" id="layout-contract">'+json.dumps(budgets,ensure_ascii=False).replace('</','<' + chr(92) + '/')+'</script><script type="application/json" id="license-notices">'+json.dumps(licenses,ensure_ascii=False).replace('</','<' + chr(92) + '/')+'</script><script>'+controller+'</script></body></html>'
    (CASE/'index.html').write_text(doc,encoding='utf-8')
    (src/'FONT-SOURCE.json').write_text(json.dumps({'repository':'google/fonts','commit':'66928797f271fed5ee428544e7229685e2d90127','source':'Existing official fixed TTF distribution, not extracted from OS','fonts':fonts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Built 6 HTML slides from extracted DNA tokens and Page Specs. Run the original Node layout guard next.')


if __name__=='__main__':build()
