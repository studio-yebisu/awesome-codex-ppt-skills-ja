"""PPTX conversion through aws-html-slides extractor + actual Neon controller/template."""
from pathlib import Path
from xml.sax.saxutils import escape
import argparse,base64,difflib,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,zipfile
from pptx import Presentation

ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='tools' else Path(__file__).resolve().parent
OUT=ROOT/'examples/repositories/aws-html-showcase' if Path(__file__).parent.name=='tools' else ROOT
UP=ROOT/'.build/aws-html-original' if Path(__file__).parent.name=='tools' else OUT/'upstream'
FORK=ROOT/'skill-forks/aws-html-ja'
INPUT=ROOT/'examples/repositories/ppt-agent-showcase' if Path(__file__).parent.name=='tools' else OUT/'input'
REPO='lanceli93/aws-html-slides';PIN='5ae3d68b66277e8a0d0b6ceea479a4b5117f16b2';TITLE='小さな展示を、ひとつの体験に。'
TITLES=[TITLE,'作品・場所・言葉を、つなぐ','入口から、余韻まで。','準備は、四つの区切りで。','開く前に、一度だけ歩く。']
PROMPT='既存の自作PPTX「小さな展示を、ひとつの体験に。」5枚を、lanceli93/aws-html-slides原典のPPT conversion経路で日本語の動くWebスライドへ変換してください。元extract-pptx.pyを実行し、抽出した全テキスト/画像/notes、元native OOXMLの円・四角・三角・辺のgeometryと色を保全する。原典Neon Cyberの100vh viewport CSS、controller/IntersectionObserver/nav dots/keyboard/wheel/touchとreveal animation、native SVG edge choreographyをStudio Yebisuの仮想展示案へ適用。Akxan/ppt-agent-skillの制作元作例を入力として用いた出所/commit/MITも保持。2枚目の3ラベルと3枚目の番号・見出し・説明12個は出力SVGだけで対応する図形の中心へ揃え、表示する頁番号を1か所にし、元座標と変更内容を記録する。入力PPTXは原本保全。AWSロゴや公式性/提携表示は使わず、派生footerへ置換し明記。日本語大見出し/短い明朝説明/英数字のOSS字体を役割別に、実TTF/OFLを同梱。HTML/SVG編集可能であり、新規PPTX生成と表示しない。原典の機能と作例で実行した範囲を区別し、実画面で位置と読みやすさを確認する。Kimi K3とOpus5.5の独立評価は別記録に残し、未評価を合格扱いしない。'

def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def jwrite(p,s):write(p,json.dumps(s,ensure_ascii=False,indent=2)+'\n')
def color(el,default='none'):
 v=el.xpath('./a:solidFill/a:srgbClr')
 return '#'+v[0].get('val') if v else default
def layout_adapter():
 spec=importlib.util.spec_from_file_location('aws_example_layout_adapter',OUT/'source/layout_adapter.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module

def native_svg(prs,slide,idx,apply_alignment=True):
 alignment=layout_adapter().label_alignment(prs,slide,idx) if apply_alignment else {}
 scale=1600/prs.slide_width;svg=['<svg class="native-diagram converted-vector" viewBox="0 0 1600 900" role="img" aria-label="'+escape(TITLES[idx])+'">'];facts=[]
 for n,sh in enumerate(slide.shapes):
  x,y,w,h=[round(v*scale,3) for v in [sh.left,sh.top,sh.width,sh.height]]
  el=sh._element;sppr=el.xpath('./p:spPr');sp=sppr[0] if sppr else None
  rec={'id':sh.name,'type':str(sh.shape_type),'bbox_px':[x,y,w,h],'text':sh.text if sh.has_text_frame else ''}
  reveal='reveal d'+str(min(7,1+n//3));cls='vector-object '+reveal;kind=''
  if sh.has_text_frame and sh.text.strip():
   cls+=' native-text';pieces=[];baseline=y
   for p in sh.text_frame.paragraphs:
    runs=[r for r in p.runs if r.text];r=runs[0] if runs else None
    if not r:continue
    fontsize=(r.font.size.pt if r.font.size else 18)*1600/(prs.slide_width/914400*72)
    family=r.font.name or 'Zen Kaku Gothic New';ishead=fontsize>55
    weight=900 if ishead and 'Zen Kaku' in family else 700 if r.font.bold else 400
    fill=color(r._r.xpath('./a:rPr')[0], '#1A1A1A') if r._r.xpath('./a:rPr') else '#1A1A1A'
    # Reconstruct source text in independent SVG text objects; native extracted text stays unchanged.
    placement=alignment.get(sh.name);render_x=placement['render_x_px'] if placement else x;anchor=' text-anchor="middle"' if placement else ''
    tx=''.join(r.text for r in runs);pieces.append(f'<text x="{render_x}" y="{baseline}"{anchor} dominant-baseline="text-before-edge" fill="{fill}" font-family="{escape(family)}" font-weight="{weight}" font-size="{fontsize:.2f}">{escape(tx)}</text>');baseline+=fontsize*1.15
    rec.update(font_family=family,font_size_px=fontsize,font_weight=weight)
   if sh.name in alignment:rec['output_layout_adapter']=alignment[sh.name]
   svg.append(f'<g class="{cls}" data-source-shape="{escape(sh.name)}">'+''.join(pieces)+'</g>')
  elif sp is not None:
   fill=color(sp);lines=sp.xpath('./a:ln');ln=lines[0] if lines else None;stroke=color(ln) if ln is not None else 'none';sw=float(ln.get('w','12700'))*scale if ln is not None else 0
   prst=sp.xpath('./a:prstGeom');geom=prst[0].get('prst') if prst else ''
   attrs=f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:.3f}"'
   if geom=='ellipse':kind='circle';drawing=f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" {attrs}/>'
   elif geom in ['rect','roundRect']:kind='square';drawing=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {attrs}/>'
   elif geom=='line':kind='edge';drawing=f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" pathLength="1" {attrs}/>'
   else:
    paths=sp.xpath('./a:custGeom/a:pathLst/a:path');commands=[]
    if not paths:raise ValueError('Unsupported source native geometry: '+sh.name+'/'+geom)
    for path in paths:
     pw=float(path.get('w','100000'));ph=float(path.get('h','100000'))
     for c in path:
      local=c.tag.split('}')[-1];pts=c.xpath('./a:pt');positions=[(x+float(p.get('x'))/pw*w,y+float(p.get('y'))/ph*h) for p in pts]
      if local in ['moveTo','lnTo']:commands.append(('M' if local=='moveTo' else 'L')+f'{positions[0][0]:.3f},{positions[0][1]:.3f}')
      elif local=='cubicBezTo':commands.append('C'+' '.join(f'{a:.3f},{b:.3f}' for a,b in positions))
      elif local=='quadBezTo':commands.append('Q'+' '.join(f'{a:.3f},{b:.3f}' for a,b in positions))
      elif local=='close':commands.append('Z')
      else:raise ValueError('Unsupported native path '+local)
    kind='triangle';drawing=f'<path d="'+ ' '.join(commands)+f'" {attrs}/>';rec['svg_path']=' '.join(commands)
   rec.update(kind=kind,fill=fill,stroke=stroke);svg.append(f'<g class="{cls} geometry {kind}" data-source-shape="{escape(sh.name)}">{drawing}</g>')
  facts.append(rec)
 svg.append('</svg>');return '\n'.join(svg),facts

CSS='''
:root{--bg-primary:#081421;--text-primary:#F3F1E8;--text-secondary:#A7B6C6;--accent-cyan:#00FFCC;--accent-magenta:#FF3C52;--accent-blue:#28A5FF;--font-display:"Zen Kaku Gothic New",sans-serif;--font-body:"BIZ UDPMincho",serif;--font-mono:"Manrope",sans-serif;--title-size:clamp(1.5rem,5vw,5rem);--slide-padding:clamp(1rem,3vw,3rem);--content-gap:clamp(.5rem,1.5vw,1.5rem);--ease-out-expo:cubic-bezier(.16,1,.3,1);--duration-normal:.65s}
*{box-sizing:border-box;margin:0;padding:0}body{background:var(--bg-primary);color:var(--text-primary);font-family:var(--font-display)}.slide{background:radial-gradient(ellipse at 30% 80%,rgba(40,165,255,.1),transparent 60%),var(--bg-primary)}.slide::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(0,255,204,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,204,.035) 1px,transparent 1px);background-size:clamp(2rem,4vw,4rem) clamp(2rem,4vw,4rem);pointer-events:none}.slide-content{align-items:center;padding-top:clamp(2rem,5vh,4rem);padding-bottom:clamp(2rem,6vh,4rem)}.diagram-figure{width:min(94vw,1600px);max-height:86vh;aspect-ratio:16/9;position:relative}.converted-vector{width:100%;height:100%;max-height:86vh;overflow:visible;background:#F7F5EE;box-shadow:0 0 0 1px rgba(0,255,204,.16),0 0 55px rgba(40,165,255,.09)}.converted-vector .reveal{opacity:0;transform:translateY(20px);transition:opacity .65s var(--ease-out-expo),transform .65s var(--ease-out-expo);transform-box:fill-box;transform-origin:center}.slide.visible .converted-vector .reveal{opacity:1;transform:translateY(0)}.d1{transition-delay:.10s!important}.d2{transition-delay:.25s!important}.d3{transition-delay:.40s!important}.d4{transition-delay:.55s!important}.d5{transition-delay:.70s!important}.d6{transition-delay:.85s!important}.d7{transition-delay:1s!important}
.slide.visible .circle>*{animation:circleBreath 5s ease-in-out infinite;transform-box:fill-box;transform-origin:center}.slide.visible .triangle>*{animation:triangleNudge 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}.slide.visible .square>*{animation:squareLight 6s ease-in-out infinite}.slide .edge line{stroke-dasharray:1;stroke-dashoffset:1}.slide.visible .edge line{animation:edgeDraw 1.4s .45s var(--ease-out-expo) forwards}.slide:nth-of-type(3) .circle>*{animation-delay:.8s}.slide:nth-of-type(4) .square>*{animation-delay:1.2s}.slide:nth-of-type(5) .triangle>*{animation-delay:.4s}
@keyframes circleBreath{0%,100%{transform:scale(1)}50%{transform:scale(1.028)}}@keyframes triangleNudge{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}@keyframes squareLight{0%,100%{filter:brightness(1)}50%{filter:brightness(1.07)}}@keyframes edgeDraw{to{stroke-dashoffset:0}}
.progress-track{position:fixed;left:0;right:0;top:0;height:clamp(2px,.35vh,4px);z-index:80;background:rgba(255,255,255,.08)}.progress-bar{height:100%;width:20%;background:linear-gradient(90deg,var(--accent-cyan),var(--accent-blue));transition:width .4s}.nav-dots{position:fixed;right:clamp(.5rem,1.5vw,1.5rem);top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:clamp(.3rem,.8vh,.7rem);z-index:80}.nav-dot{width:clamp(7px,.65vw,12px);height:clamp(7px,.65vw,12px);border:1px solid #7B91A5;border-radius:50%;background:transparent;cursor:pointer}.nav-dot.active{background:#00FFCC;border-color:#00FFCC;box-shadow:0 0 10px rgba(0,255,204,.5)}.slide-footer{position:fixed;left:clamp(1rem,3vw,3rem);bottom:clamp(.3rem,1.4vh,1rem);font-family:var(--font-mono);font-size:clamp(.65rem,.95vw,1rem);color:#9DB2C4;z-index:80}.page-number{position:fixed;right:clamp(1rem,3vw,3rem);bottom:clamp(.3rem,1.4vh,1rem);font-family:var(--font-mono);font-size:clamp(.7rem,1vw,1.1rem);color:#00FFCC;z-index:80}.hud-bar{position:absolute;top:clamp(.35rem,1.3vh,1rem);left:clamp(1rem,3vw,3rem);right:clamp(1rem,3vw,3rem);display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:clamp(.6rem,.8vw,.9rem);letter-spacing:.1em;color:#A8BCD1;z-index:2}.hud-index{color:#FFD60A}.embed .slide-footer,.embed .nav-dots,.embed .page-number{opacity:.7}
.overview{position:fixed;inset:0;z-index:100;background:#081421;padding:clamp(1rem,3vw,3rem);display:none;grid-template-columns:repeat(3,1fr);gap:clamp(.5rem,1vw,1rem);overflow:auto}.overview.open{display:grid}.overview button{background:#102234;border:1px solid #2D6275;color:#F3F1E8;padding:clamp(.4rem,1vw,1rem);font-family:var(--font-display);font-size:clamp(.7rem,1vw,1.1rem);cursor:pointer}.overview svg{width:100%;height:auto;background:#F7F5EE}.overview .reveal{opacity:1!important;transform:none!important}.overview .geometry>*{animation:none!important}.overview .edge line{stroke-dashoffset:0!important}
@media(max-height:700px){.diagram-figure,.converted-vector{max-height:83vh}}@media(max-height:600px){.diagram-figure,.converted-vector{max-height:80vh}.hud-bar{display:none}}@media(max-height:500px){.diagram-figure,.converted-vector{max-height:76vh}}@media(prefers-reduced-motion:reduce){.geometry>*{animation:none!important}.reveal{opacity:1!important;transform:none!important}.edge line{stroke-dashoffset:0!important}html{scroll-behavior:auto}}
'''

def main(case_only=False):
 OUT.mkdir(parents=True,exist_ok=True)
 if Path(__file__).parent.name=='tools' and not case_only:
  shutil.copytree(UP,OUT/'upstream',dirs_exist_ok=True);(OUT/'input').mkdir(exist_ok=True)
  # This case keeps the actual conversion input snapshot, even if the source case is revised later.
  if not (OUT/'input/deck.pptx').exists():shutil.copy2(INPUT/'deck.pptx',OUT/'input/deck.pptx')
  for f in ['LICENSE','PROVENANCE.json','SOURCE.json','MANUSCRIPT.md']:
   if (INPUT/f).is_file() and not (OUT/'input'/('AKXAN-'+f)).exists():shutil.copy2(INPUT/f,OUT/'input'/('AKXAN-'+f))
  for folder,file in [('zenkakugothicnew','ZenKakuGothicNew-Black.ttf'),('bizudpmincho','BIZUDPMincho-Regular.ttf'),('manrope','Manrope[wght].ttf')]:
   (OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(ROOT/'downloads/fonts'/folder/file,OUT/'fonts'/file);shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt')
 subprocess.run([sys.executable,str(OUT/'upstream/aws-html-slides/scripts/extract-pptx.py'),str(OUT/'input/deck.pptx'),str(OUT/'extraction')],check=True)
 extracted=json.loads((OUT/'extraction/extracted-slides.json').read_text(encoding='utf-8'));prs=Presentation(OUT/'input/deck.pptx');slide_html=[];allfacts=[]
 for idx,(slide,data) in enumerate(zip(prs.slides,extracted)):
  art,facts=native_svg(prs,slide,idx);allfacts.append({'page':idx+1,'title':TITLES[idx],'shapes':facts})
  if idx==2:
   before,_=native_svg(prs,slide,idx,apply_alignment=False)
   write(OUT/'source/slide-03-before-label-alignment.svg',before)
   write(OUT/'source/label-alignment.diff',''.join(difflib.unified_diff(before.splitlines(keepends=True),art.splitlines(keepends=True),fromfile='source/slide-03-before-label-alignment.svg',tofile='source/slide-03.svg')))
  write(OUT/f'source/slide-{idx+1:02}.svg',art)
  note=data.get('notes','').replace('--','—')
  slide_html.append(f'<section class="slide" data-slide-id="s{idx+1}" aria-label="{escape(TITLES[idx])}"><div class="hud-bar"><span>STUDIO YEBISU　展示をひとつの体験に</span><span class="hud-index"></span></div><div class="slide-content"><figure class="diagram-figure">{art}</figure></div><!-- Input PPTX notes: {note} --></section>')
 jwrite(OUT/'extraction/native-shapes.json',{'source':'input/deck.pptx','source_sha256':hashlib.sha256((OUT/'input/deck.pptx').read_bytes()).hexdigest(),'dimensions_px':[1600,900],'slides':allfacts})
 audit=layout_adapter().audit_document(prs);audit['input_sha256']=hashlib.sha256((OUT/'input/deck.pptx').read_bytes()).hexdigest();audit['rendered_svg']='source/slide-03.svg'
 jwrite(OUT/'source/svg-label-alignment.json',audit)
 # The real preview's controller and FX code are used, not the template's pseudo-methods.
 preview=(OUT/'upstream/aws-html-slides/preview/01-neon-cyber.html').read_text(encoding='utf-8')
 js=preview.split('/* === SLIDE CONTROLLER === */',1)[1].split('/* === Subtle',1)[0]
 # End exactly at the FX engine; omit particles/WebGL demos irrelevant to the exhibition.
 end=js.index("document.querySelectorAll('.slide.visible').forEach")
 js=js[:js.index('})();',end)+5]
 write(OUT/'source/original-controller.js','/* === SLIDE CONTROLLER === */'+js)
 patched=js.replace("'Slide ' + (i + 1)","'スライド ' + (i + 1)").replace("'IDX '","'頁 '")
 patched=patched.replace("if (window.runFX) window.runFX(e.target);","if (window.runFX) window.runFX(e.target);\n            } else { e.target.classList.remove('visible');")
 patched=patched.replace("dots.forEach(function (d, i) { d.classList.toggle('active', i === current); });","dots.forEach(function (d, i) { d.classList.toggle('active', i === current); });\n        document.getElementById('pageNumber').textContent=(current+1)+' / '+total;\n        if(parent!==window)parent.postMessage({type:'yebisu-page',index:current,total:total},location.origin);")
 patched=patched.replace("    document.addEventListener('keydown', function (e) {","    window.awsDeck={go:go,get index(){return current;}};\n    document.addEventListener('keydown', function (e) {")
 adapter='''
/* === LOCAL SAME-ORIGIN PLAYER ADAPTER + OVERVIEW === */
addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))window.awsDeck.go(e.data.index)});
if(parent!==window)document.body.classList.add('embed');
const overview=document.getElementById('overview');document.querySelectorAll('.slide').forEach((s,i)=>{const b=document.createElement('button');b.innerHTML=s.querySelector('svg').outerHTML+'<p>'+String(i+1)+' / 5　'+s.getAttribute('aria-label')+'</p>';b.onclick=()=>{overview.classList.remove('open');window.awsDeck.go(i)};overview.appendChild(b)});addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();overview.classList.toggle('open')}});
'''
 write(OUT/'source/local-controller.js',patched+adapter);write(OUT/'source/controller.diff',''.join(difflib.unified_diff(js.splitlines(keepends=True),(patched+adapter).splitlines(keepends=True),fromfile='original-controller.js',tofile='local-controller.js')))
 fontcss=''
 for file,family,weight in [('ZenKakuGothicNew-Black.ttf','Zen Kaku Gothic New',900),('BIZUDPMincho-Regular.ttf','BIZ UDPMincho',400),('Manrope[wght].ttf','Manrope','200 800')]:
  fontcss+=f'@font-face{{font-family:"{family}";src:url(data:font/ttf;base64,{base64.b64encode((OUT/"fonts"/file).read_bytes()).decode()});font-weight:{weight};font-display:block}}\n'
 base=(OUT/'upstream/aws-html-slides/viewport-base.css').read_text(encoding='utf-8')
 write(OUT/'source/theme.css',CSS)
 html='<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+TITLE+' / 動く展示案内</title><style>/* === ORIGINAL COMPLETE VIEWPORT BASE === */\n'+base+'\n/* === LOCAL FONTS / THEME / SVG MOTION === */\n'+fontcss+CSS+'\n/* Codex: retain source slide number as the sole numeric page indicator. */\n.page-number,.hud-index{display:none!important}\n'+'</style></head><body><div class="progress-track"><div class="progress-bar" id="progressBar"></div></div><nav class="nav-dots" id="navDots" aria-label="スライドを選ぶ"></nav><div class="slide-footer">Studio Yebisu / 仮想展示企画・日時など未定</div><div class="page-number" id="pageNumber"></div>'+''.join(slide_html)+'<div class="overview" id="overview" aria-label="スライド一覧"></div><script>/* === ORIGINAL CONTROLLER / FX WITH LOCAL ADAPTER === */'+patched+adapter+'</script></body></html>'
 write(OUT/'index.html',html)
 write(OUT/'MANUSCRIPT.md','\n\n'.join(f"## {i+1}. {TITLES[i]}\n\n"+'\n'.join(c['content'] for c in s['content'] if c.get('content','').strip()) for i,s in enumerate(extracted)))
 if Path(__file__).parent.name=='tools' and not case_only:finish(extracted,allfacts)
 print('Converted original input PPTX to animated HTML:',OUT/'index.html')

def finish(extracted,facts):
 shutil.copy2(OUT/'upstream/LICENSE',OUT/'LICENSE');write(OUT/'PROMPT.md',PROMPT+'\n');write(OUT/'input/BRIEF.md','# 変換依頼\n\n'+PROMPT+'\n');jwrite(OUT/'input/data.json',{'title':TITLE,'titles':TITLES,'page_count':5,'sample_notice':'自作仮想展示企画。日時・会場・参加条件は未定。相対的な準備日程。','input_format':'existing PPTX','output_format':'animated HTML / SVG','input_provenance':'Akxan/ppt-agent-skill native PPTX, MIT, 01825dee2ad40a8c719824252605396b9a570d57'})
 refs=[{'path':f,'sha256':hashlib.sha256((OUT/'upstream'/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{PIN}/{f}'} for f in ['aws-html-slides/SKILL.md','aws-html-slides/scripts/extract-pptx.py','aws-html-slides/scripts/gen-content.py','aws-html-slides/html-template.md','aws-html-slides/viewport-base.css','aws-html-slides/preview/01-neon-cyber.html','aws-html-slides/animation-patterns.md','aws-html-slides/diagram-reference.md','LICENSE']]
 source={'repository':REPO,'commit':PIN,'license':'MIT','copyright':'2025 Zara Zhang, retained original MIT','method':'Original PPT conversion route: unmodified extract-pptx.py extracts all 5 slide texts/media/notes; source-specific native OOXML supplement maps actual input shape coordinates/colors/paths to editable SVG; original Neon preview controller/FX, whole viewport-base.css, reveal stagger and SVG edge choreography drive HTML playback.','input_repository':'Akxan/ppt-agent-skill','input_commit':'01825dee2ad40a8c719824252605396b9a570d57','input_license':'MIT','input_pptx_sha256':hashlib.sha256((OUT/'input/deck.pptx').read_bytes()).hexdigest(),'page_count':5,'pptx_generated_here':False,'editability':'HTML / SVG text, geometry, colors and animations','source_refs':refs,'upstream_preserved':True,'modifications':['Original extractor does not export non-picture native geometry or recognize Akxan free text boxes as title placeholders; separate native-shapes.json records actual OOXML geometry/font data and generates SVG without guessing shapes.','Original complete viewport CSS and real Neon preview navigation/FX are retained; footer/HUD/dot labels localized to Japanese and Studio Yebisu.','Mandatory AWS affiliation-looking footer replaced under explicit no-officiality instruction. No AWS logo/brand/service icons used.','Full local TTF embedded in single HTML instead of remote fonts/Lucide CDN; input contains no raster images, icons or new licensed assets.','Original intersection observer additionally clears visible on leave to replay geometry explanation; same-origin minimal player adapter and page counter recorded in source/controller.diff.','Original gen-content.py is a new-presentation-only path and is not executed for this PPT conversion.','PPT shape geometry remains inside a fixed SVG viewBox, scaled by viewport; page3 has a declared output-only center alignment adapter for12 labels, with raw bbox preserved in extraction and source/svg-label-alignment.json.'],'fonts':{'families':['Zen Kaku Gothic New','BIZ UDPMincho','Manrope'],'license':'OFL-1.1','commit':'66928797f271fed5ee428544e7229685e2d90127','TTF_and_OFL_included':True},'source_shape_counts':[len(s['shapes']) for s in facts],'extracted_picture_counts':[len(s['images']) for s in extracted]}
 jwrite(OUT/'PROVENANCE.json',source);jwrite(OUT/'SOURCE.json',source)
 write(OUT/'README.md','''# 小さな展示を、ひとつの体験に。 動く展示案内

既存の自作PPTX5枚を動くHTMLへ変換。元資料はAkxan/ppt-agent-skillのHTML→native PPTXで作った、MITの仮想展示企画です。新しいPPTXを生成した作例ではありません。日時・会場・参加条件は未定、準備日程は相対的な仮案です。

原典aws-html-slidesのPPT conversion経路で、extract-pptx.pyを実行して全テキスト・画像・speaker notesを抽出。原典extractorはnative円/四角/三角を含めないので補助native-shapes.jsonで実OOXMLの位置・色・path/fontを保全し、同じ構成をSVG text/ellipse/rect/path/lineへ変換しました。抽出済み文字とnotesから原稿/HTML commentsを作り、元の形にbreath/slide/path drawを加えています。同じ文章を別の画面へ貼り直しただけではありません。

原典Neon previewの実controller（IntersectionObserver、keyboard、wheel、touch、nav dots、progress）とFXコード、viewport-base.css全文、reveal stagger、native SVG diagramのedge choreographyを使用。各ページは100vh/100dvh、SVGのfixed viewBoxを画面へ縮尺。元三原色のBauhaus図を暗いNeon frameへ入れた派生です。AWSのlogo/公式性/提携を主張しないStudio Yebisu表示へfooterを置換しています。未変更原本とMITを保持。

index.htmlはfontを含めた単一HTMLで、ネット接続なしに開けます。矢印/Space/PageUp/PageDown、wheel、swipe、nav dotsでページ送り、Escで一覧。Reduce motionにも対応。文字・vector geometry・motionをsource/のSVG/CSSとindex.htmlで編集できます。PPTX編集の例ではなく、入力PPTXはinput/deck.pptxに原本保全。

再変換: Python3.10+とpython-pptxを用意し `python rebuild.py`。原典extract→実OOXML補助抽出→元controller/templateでindex.htmlを再生成。別のPPTXへ適用する場合はinput/deck.pptx、題名/枚数とsource/layout_adapter.pyの対応表を更新してください。本例の12ラベル用adapterは保存入力を検証し、異なる入力なら停止します。原典gen-content.pyは新規制作のみなので、本変換でStep4/5は実行しません。入力出所とhashはSOURCE/PROVENANCE、原稿はMANUSCRIPT.md、依頼文はPROMPT.md、controller局所差分はsource/controller.diff。

元MIT著作権©2025 Zara Zhang（lanceli93/aws-html-slides固定版）をLICENSEへ保持。Akxan原典のMIT/commit/provenanceもinput/に添付。書体はGoogle Fonts固定pinの未改変TTFと各OFLをfonts/へ添付、Windows fontsから抽出していません。原典のCDNはこの派生の再生に不要です。

原典extractと初回表示・ページ送りに加え、3枚目の12ラベルを各図形の中心へ揃えました。元の座標はextraction/native-shapes.json、出力変更はsource/svg-label-alignment.jsonとsource/label-alignment.diffを参照。保存入力は制作元Akxan作例の修正前版で、現在のAkxan作例と同じ版ではありません。実行した検査と実画面の確認はQA.jsonに記録し、独立評価は別記録に残します。SVG textのbaseline/line metricsはPowerPointと完全一致を保証しません。
''')
 FORK.mkdir(parents=True,exist_ok=True);shutil.copytree(OUT/'upstream',FORK/'upstream',dirs_exist_ok=True);shutil.copy2(OUT/'LICENSE',FORK/'LICENSE');jwrite(FORK/'SOURCE.json',source)
 write(FORK/'SKILL.md','''---
name: aws-html-ja
description: aws-html-slides原典のPPT conversion extractorとNeon HTML/controller/animationで、既存PPTXを日本語の動くWebスライドへ変換する。
---

# 日本語PPTX→動くWebスライド（非公式）

1. 入力PPTXを正本にし、原典upstream/aws-html-slides/SKILL.mdのPPT conversion経路を読む。言語/style/編集範囲が指定済みなら再質問しない。本例は日本語・Neon派生・HTML/SVG編集。
2. 元scripts/extract-pptx.pyを実行し、文字/画像/notes/順序を保持。原典gen-content.pyは新規制作専用で、変換ではStep4/5を飛ばす。勝手に新内容を補わない。
3. Native形状が入力の意味を担う場合は実OOXMLのgeometry/path/色を別JSONへ補助抽出。元情報をSVGとして保全し、動きの順序を役割に合わせて加える。
4. 元Neon previewのcontroller/FXとviewport-base.css全文、100vh/100dvh・clamp・height breakpoints・reduce motionを保持。SVGはfixed viewBoxで縮尺。多ページをgeneric rendererへ置き換えない。
5. 最小のsame-origin player adapterは別diffへ記録。AWS非公式の展示案にAWSlogo/著作権主体を持ち込まず、明示の派生footerへ置換。本例はStudio Yebisu表示、元MITは保持。
6. 原典extractと実画面のページ送りを確認。文字・図の対応に問題があれば出力だけの配置変更を記録する。本例は3枚目の12ラベルを図形の中心に揃えた。元座標と新anchorはexample/source/svg-label-alignment.jsonを参照。技術検査と独立評価は分け、未確認範囲もQAに残す。HTML/SVG編集とPPTX入力保全を区別する。

example/rebuild.py、input/deck.pptx、extraction/、source/*.svgが具体例。source/controller.diffに局所変更。書体は元TTF/OFLを添付し、fontをsingle HTMLへembedしてoffline再生。

原典 https://github.com/lanceli93/aws-html-slides 、MIT ©2025 Zara Zhang。固定pinとAkxan由来の入力出所はSOURCE.json。AWS/原作者の公認・提携ではない。
''')
 write(FORK/'README.md','# 日本語PPTX→HTML kit\n\n元MITとOFLを保持、非公式派生。example/の入力PPTXを原典extractし、実OOXML geometry→SVG、元controller/animationでWeb化。PPTX新規生成ではありません。\n')
 jwrite(OUT/'QA.json',{'status':'generated','checks':['Original extract-pptx.py succeeded for five input slides.','Actual source text/native geometry/font/path supplement converted to SVG; HTML generated with original controller/viewport CSS.'],'limitations':['Main first display/navigation pending','No all-page detailed visual QA, structural audit, independent review or ZIP re-execution.']})
 base='examples/repositories/aws-html-showcase/'
 case={'id':'aws-html-showcase','title':TITLE+' / 動く展示案内','repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'aws-html-ja','page_count':5,'format':'html','preview_kind':'html','preview_canvas':{'width':1600,'height':900},'style':'原典Neon motion frame × 入力Bauhaus geometry','use_case':'PPTX変換・仮想展示案内','preview':base+'index.html','cover':base+'render/slide-01.png','interior':base+'render/slide-02.png','artifact_download':base+'index.html','source_download':'downloads/aws-html-example-ja.zip','fork_download':'downloads/aws-html-ja.zip','input':base+'input/deck.pptx','input_data':base+'extraction/extracted-slides.json','prompt':base+'PROMPT.md','prompt_text':PROMPT,'provenance':base+'PROVENANCE.json','qa':base+'QA.json','guide':base+'README.md','titles':TITLES,'notes':[s.get('notes','') or '仮想展示企画。日時・会場・参加条件は未定。' for s in extracted],'sample_notice':'既存Akxan由来PPTXをHTMLへ変換。新規PPTX生成ではありません。日時・会場・参加条件は未定。','method':source['method'],'navigation':'native-runtime-bridge','editability':'html_svg','editable_features':['html_text','svg','css_motion'],'status':'generated','execution_status':'generated','preview_notice':'原典PPT conversionで動くHTML化。編集対象はHTML/SVG/CSS、入力PPTXは原本保全。AWS公式/提携ではありません。','representative_previews':[base+'render/slide-01.png',base+'render/slide-02.png'],'preview_image_notice':'主要2枚のWeb代表PNG。全ページ詳細目視は未実施。'}
 guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_pptx_extract_native_geometry_svg_neon_runtime_conversion','case_ids':[case['id']],'summary_ja':'既存Akxan自作PPTX5枚を原典extract→native geometry SVG→元Neon controller/FXへ変換。','requirements':['Python3.10+ / python-pptx（再生成のみ）','Browser（single HTMLでoffline）'],'steps':['既存PPTXを原本保全','原典PPT conversion extractorを実行','Native geometryを補助抽出し元viewport/controllerでWeb化','主要出力とページ送りを初回表示'],'commands':['python rebuild.py'],'source_refs':refs,'upstream_commit':PIN,'license':'MIT','license_notice_ja':'原典MIT ©2025 Zara Zhang、入力Akxan MIT、書体OFLを保持。AWS公式性・提携表示は使いません。','caveats':['Conversion output is editable HTML/SVG, not a newly generated PPTX.','PPTX text baseline and motion HTML are not pixel-identical.','Akxan original input is a fictitious exhibition concept.'],'skill':'skill-forks/aws-html-ja/SKILL.md','guide':case['guide']}
 jwrite(ROOT/'data/sol-aws-html-repository-examples.json',[case]);jwrite(ROOT/'data/sol-aws-html-repository-guides.json',[guide]);shutil.copy2(Path(__file__),OUT/'rebuild.py');write(OUT/'.gitignore','**/__pycache__/\n*.pyc\n')

def package():
 excluded={'.private','node_modules','__pycache__','.build','.git'}
 def ignore(folder,names):
  return [name for name in names if name in excluded or name.endswith(('.pyc','.log')) or (Path(folder)/name).is_symlink() or ((Path(folder)/name).is_dir() and os.path.isjunction(Path(folder)/name))]
 shutil.copytree(OUT,FORK/'example',dirs_exist_ok=True,ignore=ignore)
 for folder,name in [(OUT,'aws-html-example-ja'),(FORK,'aws-html-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for current,dirs,files in os.walk(folder,followlinks=False):
    dirs[:]=[d for d in dirs if d not in ignore(current,dirs)]
    for file in sorted(files):
     p=Path(current)/file
     if file not in ignore(current,[file]):z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--package-only',action='store_true');parser.add_argument('--case-only',action='store_true',help='Rebuild the saved input without replacing input, provenance, QA or global catalog fragments');args=parser.parse_args()
 if args.package_only:package()
 else:main(case_only=args.case_only)
