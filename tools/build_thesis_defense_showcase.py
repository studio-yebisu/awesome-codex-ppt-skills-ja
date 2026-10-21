"""Six-slide fictitious route study using upstream template + native clone/replace."""
from pathlib import Path
import argparse, difflib, importlib.util, json, math, os, shutil, subprocess, sys, zipfile, hashlib
from datetime import datetime

STANDALONE=Path(__file__).parent.name!='tools'
ROOT=Path(__file__).resolve().parents[1] if not STANDALONE else Path(__file__).resolve().parent
OUT=ROOT/'examples/repositories/thesis-defense-showcase' if not STANDALONE else ROOT
UP=ROOT/'.build/actual-upstreams/zouchenzhen__thesis-defense-pptx-skill' if not STANDALONE else OUT/'upstream'
SK=UP/'skills/thesis-defense-pptx'
FORK=ROOT/'skill-forks/thesis-defense-ja'
REPO='zouchenzhen/thesis-defense-pptx-skill'
PIN='7cf83b6fe264410aec39ab73d8cfa48f1c9a73bb'
TITLE='雨の日の、通学ルート。'
TITLES=[TITLE,'研究課題','経路モデル','候補の比較','仮想試算','限界と展望']
NOTES=['学部ゼミ向けの仮想研究です。地点・辺・時間は学習用設定、観測・実測ではありません。','所要時間だけでなく、雨にさらされる時間を評価する経路選択の問題を考えます。','自宅Hと学校Gの間に、交差点A、アーケードB、橋Cを置いた仮想グラフ。辺の時間はinput/routes.jsonに記録しています。','近道14分・露出14分、屋根道18分・露出3分、川沿い16分・露出16分。全て設定値からの合計です。','評価値J=移動時間+λ×露出時間。λ=0なら近道、λ=0.5なら屋根道が最小。コードでの仮想試算で、行動調査の結果ではありません。','一定速度や混雑なし等の仮定を置きました。次は仮想条件を増やし、実測する場合は時間と露出の測定設計を先に決めます。']
PROMPT='zouchenzhen/thesis-defense-pptx-skill原典のminimal_markdown/build_template.pyで生成した無地templateを、原典COM clone helperとpptx_template_toolsのnative replace/add_text/write_tableで再利用し、日本語研究発表「雨の日の、通学ルート。」を全6枚で作ってください。入力正本は自作Markdown研究メモとroutes.json。学部生ゼミ向けの架空地点・辺・所要時間を用い、関係図、候補比較、J=移動時間+λ×露出時間の仮想試算、限界と次の実験を説明。観測や調査を実施したと偽らず、設定値と仮想試算を明示。第三者写真・大学ロゴは使わない。原典templateのgeometry・濃赤・文字サイズ・native objectsを維持し、字体だけBIZ本文/Shippori見出しへ局所対応。追加の角丸カード量産は避け、既存content frame内を図・表・大きい数値で使い分ける。原典既定12〜16枚より6枚指定を優先、原典Quality gateに従い全頁PNGとcontact sheetを目視し、overflow・stale text scanを実行して修正。独立評価の合格は別記録とする。元Apache-2.0/NOTICE、使用TTF/OFL、計算コードと図allowlistを保全。共有PowerPointのApplication.Quitは呼ばず自分のdeckだけClose。'
MD='''# 雨の日の、通学ルート。

## 位置づけ
学部生向けゼミで経路評価の考え方を説明する仮想研究。地点、辺、移動時間、雨にさらされる時間は学習用の設定値。実在ルートや観測データではない。

## 研究背景
雨の日は、到着までの速さと濡れにくさが異なる選択を生む。
所要時間だけを最小にする経路と、雨にさらされる時間も考慮する経路を比べる。

## 方法設計
自宅Hと学校Gの間に、交差点A、アーケードB、橋Cを置く。
H-A-Gを近道、H-B-Gを屋根道、H-C-Gを川沿いと呼ぶ。
各辺の移動時間tと露出時間eを足し合わせ、J=t+λeで候補を比較する。λは露出1分に対して何分相当の重みを置くかを表す無次元の設定値。

## 仮想試算
近道はt=14分/e=14分、屋根道は18分/3分、川沿いは16分/16分。
λ=0では近道14、屋根道18、川沿い16。近道が最小。
λ=0.5では近道21、屋根道19.5、川沿い24。屋根道が最小。
比較の切替点は14+14λ=18+3λ、λ=4/11。これらはinput/routes.jsonと計算コードから得る仮想試算であり、観測結果ではない。

## 限界
一定速度、混雑なし、露出時間と濡れやすさの線形関係を仮定。
風、雨量、滑りやすさ、待ち時間、迂回の快適性は扱っていない。
仮想試算から実際の安全性や人の選好を保証しない。

## 次の実験
まず仮想辺の待ち時間と露出を変え、選択が変わる条件を調べる。
実測する場合は移動時間と露出の測定方法、雨量条件、比較回数を先に決める。

## 図の出所
経路ネットワーク、露出時間の棒、試算表はroutes.jsonとrebuild.pyから作るnative object。第三者写真や大学ロゴは使わない。
'''
DATA={'study_kind':'fictitious educational simulation','unit':'minutes','nodes':{'H':'自宅','A':'交差点','B':'アーケード','C':'橋','G':'学校'},'edges':[{'a':'H','b':'A','time':6,'exposure':6},{'a':'A','b':'G','time':8,'exposure':8},{'a':'H','b':'B','time':8,'exposure':2},{'a':'B','b':'G','time':10,'exposure':1},{'a':'H','b':'C','time':7,'exposure':7},{'a':'C','b':'G','time':9,'exposure':9}],'routes':[{'name':'近道','path':['H','A','G']},{'name':'屋根道','path':['H','B','G']},{'name':'川沿い','path':['H','C','G']}],'lambdas':[0,0.5]}

def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def jwrite(p,s):write(p,json.dumps(s,ensure_ascii=False,indent=2)+'\n')
def loadmod(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def main(case_only=False):
 OUT.mkdir(parents=True,exist_ok=True)
 if (OUT/'deck.pptx').exists():
  (OUT/'.private/backups').mkdir(parents=True,exist_ok=True)
  shutil.copy2(OUT/'deck.pptx',OUT/'.private/backups'/('deck-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.pptx'))
 if not STANDALONE:
  # Preserve a useful, scoped subset of the actual source tree; exclude university binaries/logos.
  shutil.copytree(SK/'scripts',OUT/'upstream/skills/thesis-defense-pptx/scripts',dirs_exist_ok=True)
  for f in ['SKILL.md','requirements.txt']:
   shutil.copy2(SK/f,OUT/'upstream/skills/thesis-defense-pptx'/f)
  (OUT/'upstream/skills/thesis-defense-pptx/references').mkdir(parents=True,exist_ok=True)
  shutil.copy2(SK/'references/pptx_quality_gate.md',OUT/'upstream/skills/thesis-defense-pptx/references/pptx_quality_gate.md')
  for f in ['build_template.py','build_deck.py','thesis.md','README.md']:
   (OUT/'upstream/examples/minimal_markdown').mkdir(parents=True,exist_ok=True);shutil.copy2(UP/'examples/minimal_markdown'/f,OUT/'upstream/examples/minimal_markdown'/f)
  for f in ['LICENSE','NOTICE']:shutil.copy2(UP/f,OUT/f)
  shutil.copytree(OUT/'upstream/skills/thesis-defense-pptx/scripts',OUT/'runtime/scripts',dirs_exist_ok=True)
  for helper_name in ['export_pptx_png.ps1','inspect_pptx_overflow.ps1']:
   original=(SK/'scripts'/helper_name).read_text(encoding='utf-8')
   adapted=original.replace('try { $pp.Quit() } catch {}','# Shared PowerPoint: close this presentation only; keep Application running.')
   write(OUT/'runtime/scripts'/helper_name,adapted)
   write(OUT/'source'/f'{helper_name}.diff',''.join(difflib.unified_diff(original.splitlines(keepends=True),adapted.splitlines(keepends=True),fromfile='upstream/'+helper_name,tofile='runtime/'+helper_name)))
  write(OUT/'runtime/export_case.ps1',(ROOT/'tools/render_powerpoint.ps1').read_text(encoding='utf-8').replace('if ($existingPowerPoint.Count -eq 0 -and $powerPoint.Presentations.Count -eq 0) { $powerPoint.Quit() }','# Parallel case work: leave Application running; close only this openedDeck.'))
  jwrite(OUT/'input/routes.json',DATA);write(OUT/'input/research.md',MD);write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT+'\n');write(OUT/'PROMPT.md',PROMPT+'\n')
  for folder,file in [('bizudpgothic','BIZUDPGothic-Regular.ttf'),('bizudpgothic','BIZUDPGothic-Bold.ttf'),('shipporimincho','ShipporiMincho-Bold.ttf')]:
   (OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(ROOT/'downloads/fonts'/folder/file,OUT/'fonts'/file);shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt')
  shutil.copy2(Path(__file__),OUT/'rebuild.py');write(OUT/'.gitignore','**/__pycache__/\n*.pyc\n')
 # Use the original generator unmodified, then adapt the generated font names only.
 source_root=OUT/'upstream';minimal=source_root/'examples/minimal_markdown'
 subprocess.run([sys.executable,str(minimal/'build_template.py')],check=True)
 from pptx import Presentation
 from pptx.util import Inches,Pt
 from pptx.dml.color import RGBColor
 from pptx.enum.shapes import MSO_SHAPE,MSO_CONNECTOR
 from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
 tpl=Presentation(minimal/'sample_template.pptx')
 for n,s in enumerate(tpl.slides):
  for sh in s.shapes:
   if sh.has_text_frame:
    for p in sh.text_frame.paragraphs:
     for r in p.runs:r.font.name='Shippori Mincho' if r.font.size and r.font.size.pt>=24 else 'BIZ UDPGothic'
 tpl.save(OUT/'template-ja.pptx')
 clone=OUT/'runtime/scripts/clone_template_deck.ps1'
 code=(source_root/'skills/thesis-defense-pptx/scripts/clone_template_deck.ps1').read_text(encoding='utf-8')
 code=code.replace('try { $pp.Quit() } catch {}','# Parallel work: do not call Application.Quit; Close only dest above.')
 write(clone,code)
 subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(clone),'-Template',str(OUT/'template-ja.pptx'),'-Output',str(OUT/'skeleton.pptx'),'-SlideSequence','1,2,3,4,4,3'],check=True)
 helpers=loadmod('thesis_case_tools',OUT/'runtime/scripts/pptx_template_tools.py')
 # Reuse the original Markdown section parser on the Japanese source.
 example=loadmod('thesis_case_original_builder',minimal/'build_deck.py')
 text=(OUT/'input/research.md').read_text(encoding='utf-8')
 sections={name:example.section(text,name) for name in ['研究背景','方法設計','仮想試算','限界','次の実験']}
 assert all(sections.values()),'Required Japanese Markdown sections are missing'
 data=json.loads((OUT/'input/routes.json').read_text(encoding='utf-8'))
 edge={(e['a'],e['b']):e for e in data['edges']};results=[]
 for route in data['routes']:
  path=route['path'];es=[edge[(a,b)] for a,b in zip(path,path[1:])];t=sum(e['time'] for e in es);e=sum(e['exposure'] for e in es)
  results.append(dict(route,time=t,exposure=e,scores={str(l):t+l*e for l in data['lambdas']}))
 jwrite(OUT/'input/calculation-results.json',{'formula':'J=t+lambda*e','results':results,'kind':'仮想試算','switch_lambda':4/11})
 jwrite(OUT/'input/figure-allowlist.json',{'policy':'Only original native diagrams from the authored input. No third-party photographs, university logos or institutional template binaries.','figures':[{'id':'route-network','source':'input/routes.json','generator':'rebuild.py: graph()','output':'slide 3 native shapes/connectors/text'},{'id':'exposure-bars','source':'input/calculation-results.json','generator':'rebuild.py: candidate comparison','output':'slide 4 native rectangle/text'},{'id':'score-table','source':'input/calculation-results.json','generator':'rebuild.py: simulation','output':'slide 5 native table'}]})
 prs=Presentation(OUT/'skeleton.pptx');RED=helpers.RED;NAVY=RGBColor(0x1B,0x25,0x3D);WHITE=RGBColor(255,255,255);PALE=RGBColor(0xEC,0xEC,0xEE)
 def tx(s,t,x,y,w,h,size=18,bold=False,color=NAVY,align=PP_ALIGN.LEFT):
  sh=helpers.add_text(s,t,x,y,w,h,size,bold,color,align)
  for p in sh.text_frame.paragraphs:
   for r in p.runs:r.font.name='Shippori Mincho' if size>=24 else 'BIZ UDPGothic'
  return sh
 def bar(s,x,y,w,h,color):return helpers.rect(s,x,y,w,h,line=color,fill=color,radius_shape=MSO_SHAPE.RECTANGLE)
 def graph(s):
  positions={'H':(1.5,4.1),'A':(3.6,2.9),'B':(3.6,4.1),'C':(3.6,5.35),'G':(5.7,4.1)}
  for ed in data['edges']:
   a,b=positions[ed['a']],positions[ed['b']];line=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(a[0]),Inches(a[1]),Inches(b[0]),Inches(b[1]));line.line.color.rgb=RED if 'B' in (ed['a'],ed['b']) else NAVY;line.line.width=Pt(2.3)
   mx=(a[0]+b[0])/2;my=(a[1]+b[1])/2+(-.58 if ed['b']=='A' or ed['a']=='A' else .08)
   tx(s,f"{ed['time']}分",mx-.28,my,.7,.29,14,bold=True,color=RED if 'B' in (ed['a'],ed['b']) else NAVY)
  for code,(x,y) in positions.items():
   circle=helpers.rect(s,x-.21,y-.21,.42,.42,line=RED if code=='B' else NAVY,fill=WHITE,radius_shape=MSO_SHAPE.OVAL)
   tx(s,code,x-.19,y-.18,.38,.35,14,True,align=PP_ALIGN.CENTER)
  for code,label,x,y in [('H','自宅',1.08,4.6),('G','学校',5.31,4.6),('A','交差点',3.02,2.32),('B','屋根のある道',2.83,4.45),('C','橋',3.27,5.76)]:tx(s,label,x,y,1.5,.36,14,color=RED if code=='B' else NAVY)
 def table(s,rows,x,y,w,h,size=16):
  sh=s.shapes.add_table(len(rows),len(rows[0]),Inches(x),Inches(y),Inches(w),Inches(h));helpers.write_table(sh.table,rows,font_size=size)
  for ri,row in enumerate(sh.table.rows):
   for cell in row.cells:
    cell.fill.solid();cell.fill.fore_color.rgb=RED if ri==0 else WHITE
    cell.margin_left=Inches(.08);cell.margin_right=Inches(.04);cell.vertical_anchor=MSO_ANCHOR.MIDDLE
    for p in cell.text_frame.paragraphs:
     for r in p.runs:r.font.name='BIZ UDPGothic';r.font.color.rgb=WHITE if ri==0 else NAVY;r.font.bold=ri==0
  return sh
 # Exact replacements retain native placeholder geometry/size/style from the cloned template.
 maps=[{'学校/实验室模板标题区':'ゼミ研究発表 / 仮想試算','毕业论文答辩':'通学ルートの選択','题目占位：请替换为论文题目':TITLE,'作者 / 专业 / 指导教师 / 日期':'学部ゼミ向け / 学習用の仮想研究'}, {'研究背景':'研究課題','左侧内容占位':'近道 H–A–G','右侧内容占位':'屋根道 H–B–G'}, {'方法设计':'経路モデル','左侧内容占位':'架空の5地点と6本の辺','右侧内容占位':'辺の時間を足して比較'}, {'实验结果':'候補の比較','左侧内容占位':'移動時間と露出時間','右侧内容占位':'露出時間だけを比べる'}, {'实验结果':'仮想試算','左侧内容占位':'重みを変えると選択が変わる','右侧内容占位':'λ = 0.5 の評価値'}, {'方法设计':'限界と展望','左侧内容占位':'今回置いた仮定','右侧内容占位':'次の実験へ'}]
 for n,s in enumerate(prs.slides):
  helpers.replace_exact_text(s,maps[n]);helpers.replace_exact_text(s,{'结果':'結果','总结':'まとめ'})
  if n:
   active=['','背景','方法','結果','結果','まとめ'][n]
   for sh in s.shapes:
    if sh.has_text_frame and sh.text.strip() in ['背景','方法','結果','まとめ']:
     label=sh.text.strip();color=WHITE if label==active else RED
     for p in sh.text_frame.paragraphs:
      for r in p.runs:r.font.color.rgb=color
   # Native rounded nav background shapes are inherited, not redrawn.
   for i,label in enumerate(['背景','方法','結果','まとめ']):
    for sh in s.shapes:
     if (not sh.has_text_frame or not sh.text.strip()) and abs(sh.left-Inches(.7+i*1.35))<2000 and abs(sh.top-Inches(.25))<2000:
      sh.fill.solid();sh.fill.fore_color.rgb=RED if label==active else RGBColor(0xF7,0xF3,0xF1)
  tx(s,'学習用の設定値 / 仮想試算。実在地点・観測結果ではありません。',.77,7.02,11.9,.25,11,color=NAVY)
  tx(s,f'{n+1:02} / 06',11.55,6.55,1,.3,12,color=RED)
  s.notes_slide.notes_text_frame.text=NOTES[n]
 # Cover preserves the existing band/title/subtitle geometry; one native route cue uses the whitespace.
 s=prs.slides[0]
 for y,w in [(2.7,2.4),(3.55,3.1),(4.4,2.75)]:bar(s,9.4,y,w,.1,RED if y==3.55 else NAVY)
 tx(s,'速さと濡れにくさを比べる',.95,5.35,8.4,.5,24,True,color=NAVY)
 # Problem: one contrast per inherited content frame.
 s=prs.slides[1];tx(s,'14分',1.1,2.62,4.7,.76,34,True,color=RED);tx(s,'雨にさらされる時間',1.1,3.65,4.7,.45,18);tx(s,'移動14分＝露出14分。\n全区間で雨にさらされる。',1.1,4.55,4.7,1.08,18)
 tx(s,'3分',7.2,2.62,4.7,.76,34,True,color=RED);tx(s,'雨にさらされる時間',7.2,3.65,4.7,.45,18);tx(s,'移動18分のうち露出3分。\n移動は長いが露出は短い。',7.2,4.55,4.7,1.08,18)
 # Graph and equation source are the authored Markdown/routes only.
 s=prs.slides[2];graph(s);tx(s,'HからGまでの3候補',7.15,2.55,4.9,.48,24,True,color=NAVY);tx(s,'近道：H–A–G\n屋根道：H–B–G\n川沿い：H–C–G',7.15,3.4,4.8,1.7,18);tx(s,'移動時間 t と露出時間 e を\n別々に足し合わせる。',7.15,5.2,4.9,.75,15)
 s=prs.slides[3];table(s,[['候補','移動 t','露出 e']]+[[r['name'],str(r['time'])+'分',str(r['exposure'])+'分'] for r in results],1.05,2.55,5.1,2.65)
 for i,r in enumerate(results):
  y=2.7+i*.92;tx(s,r['name'],7.15,y,1.35,.36,15);bar(s,8.65,y+.03,r['exposure']/16*3.05,.28,RED if i==1 else NAVY);tx(s,str(r['exposure'])+'分',8.65,y+.36,3.05,.32,15,color=RED if i==1 else NAVY)
 tx(s,'屋根道は4分長いが、露出は11分短い。',1.05,5.55,11.1,.38,18,True,color=RED)
 s=prs.slides[4];tx(s,'J = t + λ e',1.05,2.65,5.1,.62,24,True,color=NAVY);tx(s,'λ = 0　　近道が最小\nλ = 0.5　 屋根道が最小',1.05,3.65,5.1,1.14,18);tx(s,'λ は露出時間への重み。\n単位は分にそろえて比較。',1.05,5.05,5.1,.85,15)
 table(s,[['候補','評価値 J']]+[[r['name'],str(r['scores']['0.5'])] for r in results],7.15,2.55,5.1,2.65);tx(s,'最小値 19.5：屋根道',7.15,5.55,5.1,.38,18,True,color=RED)
 s=prs.slides[5];tx(s,'一定速度・混雑なし\n露出の影響は線形\n安全性や選好は未検証',1.05,2.7,5.1,2.2,18);tx(s,'風・雨量・待ち時間を\n次の条件へ加える。',1.05,5.05,5.1,.85,15)
 for i,(a,b) in enumerate([('01','待ち時間を変える'),('02','露出時間を変える'),('03','測定方法を決める')]):
  y=2.65+i*1.08;tx(s,a,7.15,y,.75,.4,20,True,color=RED);tx(s,b,8.12,y,4.1,.4,18);bar(s,7.18,y+.69,4.9,.018,PALE)
 tx(s,'実測は今後の計画。まだ実施していません。',7.15,5.89,5.1,.26,11,color=NAVY)
 prs.save(OUT/'deck.pptx')
 print('Built native template-copy six-slide PPTX:',OUT/'deck.pptx')
 if not STANDALONE:metadata(results,write_catalog=not case_only)

def metadata(results,write_catalog=True):
 refs=[{'path':f,'sha256':hashlib.sha256((UP/f).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{PIN}/{f}'} for f in ['skills/thesis-defense-pptx/SKILL.md','examples/minimal_markdown/build_template.py','examples/minimal_markdown/build_deck.py','skills/thesis-defense-pptx/scripts/clone_template_deck.ps1','skills/thesis-defense-pptx/scripts/pptx_template_tools.py','LICENSE','NOTICE']]
 source={'repository':REPO,'commit':PIN,'license':'Apache-2.0','author':'zouchenzhen','official':False,'method':'Original minimal Markdown build_template creates the native blank template; original COM Duplicate/MoveTo helper clones 1,2,3,4,4,3; original Markdown section parser, replace_exact_text/set_text_preserve_style/add_text/rect/write_table fill the Japanese native deck.','template_geometry_and_font_sizes_preserved':True,'upstream_originals_preserved':True,'modifications':['Generated template typefaces changed Microsoft YaHei to BIZ UDPGothic / Shippori Mincho; geometry, sizes, red band, navigation and content frames retained.','Local clone and local export helper never call Application.Quit: close only this case presentation for parallel COM work.','Japanese source content and original native diagrams/tables added inside existing template areas.','User-requested six-slide scope replaces12–16slide default; original visual/overflow/stale-text quality gate restored for the current revision.'],'editability':'native_elements','editable_features':['text','shapes','tables'],'inputs':['input/research.md','input/routes.json','input/calculation-results.json','input/figure-allowlist.json'],'source_refs':refs,'fonts':[{'family':'BIZ UDPGothic','files':['BIZUDPGothic-Regular.ttf','BIZUDPGothic-Bold.ttf'],'license':'OFL-1.1'},{'family':'Shippori Mincho','files':['ShipporiMincho-Bold.ttf'],'license':'OFL-1.1'}],'font_source_commit':'66928797f271fed5ee428544e7229685e2d90127','font_embedding':False,'dependencies':'python-pptx, Pillow; original Markdown module imported; Windows PowerPoint COM used for native clone/export. Extraction/PDF dependencies in original requirements retained but not used for this Markdown case.','third_party_images_or_logos':False,'artifact_tool_used':False}
 jwrite(OUT/'SOURCE.json',source);jwrite(OUT/'PROVENANCE.json',source)
 write(OUT/'README.md','''# 雨の日の、通学ルート。

学部生向けゼミの仮想研究発表、全6枚。地点・辺・移動時間・露出時間は学習用設定です。input/research.mdが入力正本、routes.jsonが計算データ。実在ルート、行動調査、雨天実測ではありません。

原典minimal_markdown/build_template.pyを未変更で実行し、生成した無地templateの文字・図形・geometry・サイズを使います。日本語の字体だけBIZ/Shipporiへ対応。原典COM clone helperで1,2,3,4,4,3を複製し、元pptx_template_toolsのreplace_exact_text/set_text_preserve_style/add_text/rect/write_tableを実使用しました。元build_deck.pyのMarkdown section parserも日本語メモに使っています。大学ロゴや既存大学のbinary templateは配布していません。

図と表もnativeです。文字、図形、connector、経路ノード、棒、native tableを編集できます。頁を画像として再利用していません。既存navとcontent framesは保持し、追加の角丸cardを量産せず、図/表/試算/仮定で役割を変えました。

近道14分/露出14分、屋根道18分/露出3分、川沿い16分/露出16分。J=t+λeでλ=0なら近道、λ=0.5なら屋根道が最小です。calculation-results.jsonはこのコードから計算します。図出所のallowlistに入力と生成箇所を記録しています。

再生成: Python3.10+、python-pptx/Pillow、Windows PowerPointを用意し、展開folderで `python rebuild.py`。続いて `powershell -NoProfile -File runtime/export_case.ps1 -PresentationPath deck.pptx -OutputDirectory render`。index.htmlはPowerPoint表示のPNGを見せます。日本語依頼文はPROMPT.mdで、題材を置き換えて使えます。

原典Apache-2.0のLICENSEとNOTICE、未変更原本を保持。非公式作例で大学との提携や公認を意味しません。共有PowerPointを守るためlocal clone/exportはApplication.Quitを呼ばず、自分で開いたdeckだけCloseします。残る無文書PowerPointはユーザーが終了できます。

使ったGoogle Fontsの未改変実TTF/OFLだけ同梱。PPTXはフォント未埋込、別端末ではfonts/を手動導入。原典Quality gateとしてPowerPointで全6頁をPNG/PDFへ描画し、contact sheetと全頁画像、overflowとstale text scanを確認します。2頁の比較は両候補の露出時間にそろえ、3頁の辺ラベルを線から離しました。実施結果はreviews/quality-gate.jsonとQA.json。独立評価は別記録とし、未実施を完了扱いにしません。
''')
 FORK.mkdir(parents=True,exist_ok=True);shutil.copytree(OUT/'upstream',FORK/'upstream',dirs_exist_ok=True);shutil.copytree(OUT/'runtime',FORK/'runtime',dirs_exist_ok=True)
 for f in ['LICENSE','NOTICE']:shutil.copy2(OUT/f,FORK/f)
 write(FORK/'SKILL.md','''---
name: thesis-defense-ja
description: 原典Thesis Defense PPTXの無地native template、clone/replace helperとMarkdown入力で日本語の編集可能研究発表を作る。
---

# Thesis Defense 日本語版（非公式）

1. Markdown/PDF/LaTeXなど実際の研究入力を読み、問題・方法・比較・限界・展望へ絞る。仮想研究なら設定と仮想試算を明示し、観測結果へ読み替えない。
2. 入力に由来する図のallowlistを先に記録。第三者写真や大学ロゴを勝手に持ち込まない。本例は自作JSONとnative diagramだけ。
3. 同梱upstreamのminimal_markdown/build_template.pyを実行して無地templateを作る。原典clone_template_deck.ps1のDuplicate/MoveToを使い、native template pagesを必要な順で再利用する。
4. 原典pptx_template_toolsのreplace_exact_text/set_text_preserve_style/add_text/rect/write_tableで内容を入れる。templateのgeometry・サイズ・濃赤・nav/content framesは保持し、日本語字体を局所対応する。文字やnative tableを画像にしない。
5. ユーザー指定の6枚を保ち、原典Quality gateは省略しない。scripts/export_pptx_png.ps1で全頁PNG、make_contact_sheet.pyで一覧を作り、inspect_pptx_overflow.ps1とscan_pptx_text.pyを実行。contact sheetと全頁を目視し、文字切れ・枠/線との接触・数値や指標の不一致・古いtemplate文字を直す。変更後は再描画・再検査し、reviews/へ記録する。
6. Quality gateの作者検査とKimi K3/Opus5.5の独立評価を区別し、独立合格前に満点扱いしない。COMのQuit抑止だけの局所adapterはsource/*.diffで示し、検査の閾値や内容を弱めない。

共有PowerPointの保全のためlocal runtime clone/exportはApplication.Quitを呼ばず、このcaseのdeckだけClose。未変更原本をupstreamに保持。example/rebuild.pyとexample/PROMPT.mdが具体的な入力→生成の入口。

原作者zouchenzhen、Apache-2.0。https://github.com/zouchenzhen/thesis-defense-pptx-skill 。LICENSE/NOTICEを保持。公式・大学の公認ではない。書体は同梱原TTFとOFL、PPTXフォント未埋込時は別端末で導入する。
''')
 write(FORK/'README.md','# Thesis Defense 日本語キット\n\n非公式改変。原典Apache-2.0/NOTICE、使用書体OFLを保持。example/input/research.mdとroutes.jsonが入力正本、example/rebuild.pyで原典template/clone/replaceを再実行できます。学習用仮想試算です。\n');jwrite(FORK/'SOURCE.json',source)
 jwrite(OUT/'QA.json',{'status':'generated','checks':['Original template generator and COM clone executed; six-slide native replacement saved.'],'limitations':['PowerPoint export/main first display pending','No extensive QA.']})
 base='examples/repositories/thesis-defense-showcase/'
 case={'id':'thesis-defense-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':PIN,'fork_id':'thesis-defense-ja','page_count':6,'format':'pptx','preview_kind':'powerpoint-render','preview_canvas':{'width':1600,'height':900},'style':'原典template保持 / 白・濃赤・墨紺の仮想研究','use_case':'研究発表・仮想試算','preview':base+'index.html','cover':base+'render/slide-01.png','interior':base+'render/slide-03.png','pages':[base+f'render/slide-{n:02}.png' for n in range(1,7)],'artifact_download':'downloads/thesis-defense-example-ja.zip','source_download':'downloads/thesis-defense-example-ja.zip','fork_download':'downloads/thesis-defense-ja.zip','pptx_download':base+'deck.pptx','pdf_download':base+'render/deck.pdf','input':base+'input/research.md','input_data':base+'input/routes.json','prompt':base+'PROMPT.md','prompt_text':PROMPT,'provenance':base+'PROVENANCE.json','qa':base+'QA.json','guide':base+'README.md','titles':TITLES,'notes':NOTES,'sample_notice':'地点・辺・時間は学習用設定、結果は仮想試算。観測・調査・実在ルートではありません。','method':source['method'],'navigation':'native-runtime-bridge','editability':'native_elements','editable_features':['text','shapes','tables'],'status':'generated','execution_status':'generated','preview_notice':'原典native templateをclone/replace。文字・経路図形・表を編集できます。全数値は仮想設定。','representative_previews':[base+'render/slide-01.png',base+'render/slide-03.png'],'preview_image_notice':'6枚のPowerPoint初回書き出しPNG。代表完成物のみ初回表示、全詳細目視なし。'}
 guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_minimal_template_com_clone_native_replace','case_ids':[case['id']],'summary_ja':'原典無地template/COM clone/helperで日本語6枚。Markdownから架空経路とコード上の仮想試算をnative図表へ。','requirements':['Python3.10+ / python-pptx / Pillow','Windows PowerPoint COM','BIZ UDPGothic/Shippori Mincho（同梱TTF/OFL）'],'steps':['Markdown研究メモとJSONを読み、図allowlistを作る','元build_templateで無地templateを作る','原典COM helperで6枚cloneし元native helperで置換','完成PPTXを初回export/表示'],'commands':['python rebuild.py','powershell -NoProfile -File runtime/export_case.ps1 -PresentationPath deck.pptx -OutputDirectory render'],'source_refs':refs,'upstream_commit':PIN,'license':'Apache-2.0','license_notice_ja':'原典Apache-2.0とNOTICEを保持。使用書体はOFL。大学ロゴ・既存大学templateは含みません。','caveats':['Fictitious educational calculations, no observational data or real route guidance.','PPTX fonts not embedded; full original TTF/OFL provided.','Local COM scripts close only this case document and do not quit shared PowerPoint.'],'skill':'skill-forks/thesis-defense-ja/SKILL.md','guide':case['guide']}
 if write_catalog:jwrite(ROOT/'data/sol-thesis-defense-repository-examples.json',[case]);jwrite(ROOT/'data/sol-thesis-defense-repository-guides.json',[guide])

def viewer():
 html='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雨の日の、通学ルート。</title><style>body{margin:0;background:#1B253D;height:100vh;display:grid;place-items:center}img{width:min(100vw,177.777vh);aspect-ratio:16/9;object-fit:contain}nav{position:fixed;bottom:12px;right:16px;background:#830604;color:white;display:flex;align-items:center;gap:14px;padding:9px;font-family:sans-serif}button{font:inherit;background:none;border:1px solid white;color:white;padding:8px 15px}.embed nav{display:none}</style><img id="slide" src="render/slide-01.png" alt="雨の日の、通学ルート。"><nav aria-label="スライド操作"><button id="prev">戻る</button><span id="counter">1 / 6</span><button id="next">進む</button></nav><script>const titles=TITLES;let n=0;function show(i){n=Math.max(0,Math.min(5,i));document.querySelector('#slide').src='render/slide-'+String(n+1).padStart(2,'0')+'.png';document.querySelector('#slide').alt=titles[n];document.querySelector('#counter').textContent=(n+1)+' / 6';if(parent!==window)parent.postMessage({type:'yebisu-page',index:n,total:6},location.origin)}document.querySelector('#prev').onclick=()=>show(n-1);document.querySelector('#next').onclick=()=>show(n+1);addEventListener('keydown',e=>{if(e.key==='ArrowRight')show(n+1);if(e.key==='ArrowLeft')show(n-1)});addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))show(e.data.index)});if(parent!==window)document.body.classList.add('embed');show(0)</script></html>'''
 write(OUT/'index.html',html.replace('const titles=TITLES;',f'const titles={json.dumps(TITLES,ensure_ascii=False)};'))

def package():
 excluded={'.private','backups','.build','.git','__pycache__','node_modules','cache'}
 def ignore(folder,names):return [n for n in names if n in excluded or n.endswith(('.pyc','.log')) or (Path(folder)/n).is_symlink() or ((Path(folder)/n).is_dir() and os.path.isjunction(Path(folder)/n))]
 viewer();shutil.copytree(OUT,FORK/'example',dirs_exist_ok=True,ignore=ignore)
 for folder,name in [(OUT,'thesis-defense-example-ja'),(FORK,'thesis-defense-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for current,dirs,files in os.walk(folder,followlinks=False):
    dirs[:]=[d for d in dirs if d not in ignore(current,dirs)]
    for file in sorted(files):
     p=Path(current)/file
     if file not in ignore(current,[file]):z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--package-only',action='store_true');parser.add_argument('--case-only',action='store_true');args=parser.parse_args()
 if args.package_only:package()
 else:main(case_only=args.case_only)
