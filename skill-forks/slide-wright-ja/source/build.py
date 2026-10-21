"""Grow the pinned slide-wright template in one actual HTML file: two slides, then append."""
from pathlib import Path
import argparse,base64,hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
BRIDGE='''
// Same-origin 0-based catalog bridge; original engine remains the controller.
const sendPage = () => { if(parent!==window) parent.postMessage({type:'yebisu-page',index:Reveal.getIndices().h,total:Reveal.getTotalSlides()},location.origin); };
Reveal.on('ready',sendPage); Reveal.on('slidechanged',sendPage);
addEventListener('message', e => {
  if(e.source!==parent || e.origin!==location.origin || e.data?.type!=='yebisu-slide' || !Number.isInteger(e.data.index)) return;
  if(e.data.index>=0 && e.data.index<Reveal.getTotalSlides()) Reveal.slide(e.data.index);
});
'''

def digest(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()

def build(args):
 c=args.case.resolve();u=args.upstream.resolve();file=c/'night-observatory.html'
 receipt=c/'source/stages.json';receipt.parent.mkdir(parents=True,exist_ok=True)
 if args.stage=='preview':
  ref=(u/'slide-wright/references/deck-template.md').read_text(encoding='utf-8')
  html=re.search(r'```html\n(.*?)\n```',ref,re.S).group(1)
  css=(c/'source/night-theme.css').read_text(encoding='utf-8')
  for family,name,weight in [('NightDisplay','delagothicone/DelaGothicOne-Regular.ttf','400'),('NightBody','zenkakugothicnew/ZenKakuGothicNew-Regular.ttf','400'),('NightBody','zenkakugothicnew/ZenKakuGothicNew-Bold.ttf','700'),('NightNumber','spacegrotesk/SpaceGrotesk[wght].ttf','100 900')]:
   encoded=base64.b64encode((c/'fonts'/name).read_bytes()).decode('ascii')
   css=f'@font-face{{font-family:{family};src:url(data:font/ttf;base64,{encoded}) format("truetype");font-weight:{weight};font-display:swap;}}\n'+css
  html=html.replace('<html lang="en">','<html lang="ja">').replace('<!-- DECK TITLE -->','星を待つ、夜の天文台。')
  html=re.sub(r'  <!-- Fonts:.*?<link rel="stylesheet" href="https://api.fontshare.com[^\n]+\n','  <!-- Official Google Fonts TTF embedded locally; original CDN engine retained. -->\n',html,flags=re.S)
  html=re.sub(r'  <style>.*?</style>','  <style>\n'+css+'\n  </style>',html,count=1,flags=re.S)
  start=html.index('      <!-- Every slide:')
  end=html.index('\n    </div>\n  </div>',start)
  slides=(c/'source/slides-first-two.html').read_text(encoding='utf-8')
  html=html[:start]+slides+'\n<!-- APPEND_SLIDES -->\n'+html[end:]
  html=html.replace("transition: 'slide'", "transition: 'fade'")
  html=html.replace("      plugins: [ RevealNotes ],", "      autoAnimateDuration: 0.8,\n      autoAnimateEasing: 'ease-out',\n      plugins: [ RevealNotes ],")
  insert='''
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const applyReduced = () => Reveal.configure({transition:reduced.matches?'none':'fade',autoAnimate:!reduced.matches});
    applyReduced(); reduced.addEventListener('change',applyReduced);
'''+BRIDGE
  html=html.replace('  </script>\n</body>',insert+'  </script>\n</body>')
  file.write_text(html,encoding='utf-8')
  receipt.write_text(json.dumps({'preview':{'file':'night-observatory.html','pages':2,'first_two_sha256':digest(slides),'html_sha256':digest(html)},'design_gate':{'original_new_deck_rule':'Show two real pages and stop for human approval before continuing.','human_art_approval_received':False,'case_mode':'Existing six-page deck maintenance and reproducible assembly; not a demonstration of the new-deck approval stop.'},'preview_opened':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('Two real slides written to',file)
 else:
  state=json.loads(receipt.read_text(encoding='utf-8'))
  if not state['preview_opened']:raise RuntimeError('Open the real two-slide file before appending.')
  if not args.existing_deck_repair:raise RuntimeError('This sample has no human design approval. Use --existing-deck-repair only to reproduce the authorized existing deck, not to bypass a new-deck approval gate.')
  state['continuation_basis']='Explicit existing-deck repair/reproduction; no human design approval is claimed.'
  html=file.read_text(encoding='utf-8');first=(c/'source/slides-first-two.html').read_text(encoding='utf-8')
  if first not in html or digest(first)!=state['preview']['first_two_sha256']:raise RuntimeError('Two-slide source changed before append')
  remaining=(c/'source/slides-append-four.html').read_text(encoding='utf-8')
  html=html.replace('<!-- APPEND_SLIDES -->',remaining,1)
  file.write_text(html,encoding='utf-8')
  state['append']={'same_file':'night-observatory.html','additional_pages':4,'total_pages':6,'first_two_preserved_byte_for_byte':True,'first_two_sha256':digest(first),'final_html_sha256':digest(html)}
  receipt.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('Four slides appended; original two preserved.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['preview','append'],required=True)
 p.add_argument('--case',type=Path,default=ROOT/'examples/repositories/slide-wright-showcase')
 p.add_argument('--upstream',type=Path,default=ROOT/'.build/slide-wright-upstream')
 p.add_argument('--existing-deck-repair',action='store_true',help='Authorized existing-case maintenance only; this does not attest human design approval.')
 build(p.parse_args())
