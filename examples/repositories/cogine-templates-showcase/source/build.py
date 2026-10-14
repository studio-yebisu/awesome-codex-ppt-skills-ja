"""Clone one pinned Cogine template folder, map its DOM slots, replace the demos."""
from pathlib import Path
import argparse,base64,json,re,shutil,difflib

ROOT=Path(__file__).resolve().parents[1]
SLUG='editorial-luxury'
PIN='8a7a59d39f059a7e58da9c3471014ba7fe3b98eb'

def replace_once(text,before,after):
 if text.count(before)!=1:raise ValueError('Expected exactly one demo slot: '+before[:100])
 return text.replace(before,after,1)

def build(case,upstream):
 case=case.resolve();upstream=upstream.resolve()
 # Original workflow: folder clone first, then edit this exact template.html.
 shutil.copytree(upstream/'templates'/SLUG,case,dirs_exist_ok=True)
 original=(case/'template.html').read_text(encoding='utf-8')
 metadata=json.loads((case/'template.json').read_text(encoding='utf-8'))
 original_metadata=(case/'template.json').read_text(encoding='utf-8')
 inp=json.loads((case/'input/content.json').read_text(encoding='utf-8'))
 sections=re.findall(r'<section\b.*?</section>',original,re.S)
 assets={name:(case/'assets'/f'{name}.svg').read_text(encoding='utf-8') for name in ['leaf','wrap','knot']}
 filled=[]
 for page in inp['slides']:
  s=sections[page['source_slide']-1]
  for demo,content in page['replacements']:
   s=replace_once(s,demo,content)
  for name,art in assets.items():s=s.replace('{{SVG:'+name+'}}',art)
  filled.append(s)
 html=original[:original.index('<section')]+ '\n      '.join(filled)+original[original.rindex('</section>')+len('</section>'):]
 html=html.replace('<html lang="en">','<html lang="ja">')
 html=html.replace('Editorial Luxury Presentation Template','香りを、贈る。')
 html=re.sub(r'  <link[^\n]+fonts[^\n]+\n','',html)
 html=html.replace("content:'IMAGE / CAMPAIGN'","content:'包みのイメージ / 説明用図形'")
 html=html.replace('<span id="total">8</span>','<span id="total">6</span>')
 html=html.replace('Use arrow keys to navigate','矢印キーでページを移動')
 html=html.replace('aria-label="Previous slide"','aria-label="前のページ"').replace('aria-label="Next slide"','aria-label="次のページ"')
 css=(case/'source/japanese-fonts.css').read_text(encoding='utf-8')
 for family,path,weight in [('GiftHeading','shipporimincho/ShipporiMincho-Bold.ttf','700'),('GiftBody','zenkakugothicnew/ZenKakuGothicNew-Regular.ttf','400'),('GiftNumber','manrope/Manrope[wght].ttf','100 900')]:
  data=base64.b64encode((case/'fonts'/path).read_bytes()).decode('ascii')
  css=f'@font-face{{font-family:{family};src:url(data:font/ttf;base64,{data}) format("truetype");font-weight:{weight};}}\n'+css
 html=html.replace('</style>', '\n/* Authorized Japanese font adaptation; original palette/layout rules retained. */\n'+css+'\n</style>',1)
 # Hook the original controller, retaining its handlers and visible 1-based counter.
 html=replace_once(html,'nextBtn.disabled=current===total-1}',"nextBtn.disabled=current===total-1;if(parent!==window)parent.postMessage({type:'yebisu-page',index:current,total},location.origin)}")
 bridge='''\n// Same-origin 0-based input; the original updateSlide remains the controller.\naddEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;if(e.data.index>=0&&e.data.index<total){current=e.data.index;updateSlide()}});\n'''
 html=html.replace('  </script>',bridge+'  </script>',1)
 (case/'template.html').write_text(html,encoding='utf-8')
 metadata['slide_count']=6
 metadata['typography']={'display':'Shippori Mincho Bold','body':'Zen Kaku Gothic New Regular','numbers':'Manrope','style':'Authorized Japanese adaptation; original editorial serif/sans roles preserved.'}
 metadata['adaptation']={'upstream_commit':PIN,'original_slide_count':8,'chosen_source_slides':[s['source_slide'] for s in inp['slides']],'font_change_authorized':True,'layout_slots_in_original':False}
 (case/'template.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (case/'source/template-json-local.diff').write_text(''.join(difflib.unified_diff(original_metadata.splitlines(keepends=True),(case/'template.json').read_text(encoding='utf-8').splitlines(keepends=True),fromfile='upstream/templates/editorial-luxury/template.json',tofile='template.json')),encoding='utf-8')
 normalized=re.sub(r'data:font/ttf;base64,[A-Za-z0-9+/=]+','data:font/ttf;base64,<OFFICIAL_TTF_PAYLOAD_OMITTED>',html)
 diff='Font payloads normalized for this human-readable diff only; full data is in template.html and actual TTF files.\n'+''.join(difflib.unified_diff(original.splitlines(keepends=True),normalized.splitlines(keepends=True),fromfile='upstream/templates/editorial-luxury/template.html',tofile='template.html (font payload normalized)'))
 (case/'source/template-local.diff').write_text(diff,encoding='utf-8')
 limits=json.loads((upstream/'templates'/SLUG/'template.json').read_text(encoding='utf-8'))['content_limits']
 mapping={'chosen_template':SLUG,'upstream_commit':PIN,'selection':'medium-low density, composed/editorial/premium, restrained gift narrative, recommended6–10 pages. Warm stone/gold frame composition avoids repeated card rows.','other_candidates':{'earthy-handmade':'warm/handmade but card-led medium density; no original content_limits/layout_slots','matisse-collage':'artful/handmade but recommended9–15 pages; stronger art-school emphasis','elegant-product-launch':'refined but recommended8–16 pages and launch-oriented'},'content_limits':limits,'layout_slots_in_original':None,'layout_slots_note':'原典JSONにlayout_slots未定義。以下は実template.htmlのDOMから作った局所mappingであり、原典schemaが提供したslotsとは称さない。','slides':[{'number':i+1,'source_slide':s['source_slide'],'layout':s['layout'],'slots':s['slots'],'title_chars':len(s['title']),'body_chars':len(s['body_text']),'cards':s['cards'],'within_original_title_body_limits':len(s['title'])<=limits['max_title_chars'] and len(s['body_text'])<=limits['max_body_chars_per_slide']} for i,s in enumerate(inp['slides'])],'font_preserve_exception':'ユーザーは日本語派生と字体変更を承認済み。Playfair Display→Shippori、Inter→Zen Kaku、英数字→Manrope。日本語line-heightだけ調整、palette/major grid/decoration/navigationは保持。'}
 (case/'input/template-selection-and-slots.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Cloned editorial-luxury folder; mapped and replaced six real slide layouts.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--case',type=Path,default=ROOT/'examples/repositories/cogine-templates-showcase');p.add_argument('--upstream',type=Path,default=ROOT/'.build/actual-upstreams/cogine-ai__ai-slide-templates');a=p.parse_args();build(a.case,a.upstream)
