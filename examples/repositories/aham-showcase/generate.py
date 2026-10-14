from pathlib import Path
import json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'upstream/assets/components'))
sys.path.insert(0,str(HERE/'upstream/assets'))
import components as c,layouts,themes,structures
from svg_to_pptx_wrapper import svg_to_native_pptx
data=json.loads((HERE/'input/data.json').read_text(encoding='utf-8'))
def skin(svg,page):
 svg=re.sub(r'font-family="[^"]*"',lambda m:'font-family="Manrope"' if 'JetBrains' in m[0] else 'font-family="Zen Kaku Gothic New"',svg)
 svg=re.sub(r'\s+rx="[^"]*"','',svg)
 svg=re.sub(r'font-size="([\d.]+)"',lambda m:f'font-size="{max(16,float(m[1])):g}"',svg)
 mapping={'#336EE8':'#3156C5','#262626':'#151B1D','#F3F3F3':'#F1EACF','#E7E7E7':'#151B1D'}
 if page==1:mapping.update({'#FFFFFF':'#3156C5','#262626':'#F5DC49','#6E6E6E':'#F3F0E3','#9B9B9B':'#F5DC49','#336EE8':'#F5DC49','#E7E7E7':'#F5DC49'})
 if page==3:mapping.update({'#FFFFFF':'#F5DC49','#6E6E6E':'#3156C5','#C8C8C8':'#F1EACF','#C4C4C4':'#F3F0E3'})
 if page==4:mapping.update({'#FFFFFF':'#1A2546','#262626':'#F3F0E3','#6E6E6E':'#F3F0E3','#9B9B9B':'#F5DC49','#C4C4C4':'#F5DC49','#E7E7E7':'#A8B4D5','#F3F3F3':'#243454'})
 svg=re.sub(r'#[0-9a-fA-F]{6}',lambda m:mapping.get(m[0].upper(),m[0]),svg)
 for old,new in [('目录　CONTENTS','この案で試すこと'),('本册导览','この案で試すこと'),('IN THIS DECK','サンプル行程'),('月','週')]:svg=svg.replace(old,new)
 if page==4:svg=re.sub(r'(<text x="1240\.0"[^>]*?)text-anchor="middle"',r'\1text-anchor="end"',svg)
 return svg
def page(i,body):return themes.chrome('A',data['layout_ids'][i-1],data['titles'][i-1],'架空企画 / 試行のための提案',i,4,body,brand='MORNING / WORKSHOP',tsize=38)
svgs=[]
svgs.append(themes.cover('A','MORNING / WORKSHOP',data['titles'][0],'ひとつ選ぶ。取り組む。次を残す。',[('01','時間を並べる','',''),('02','作業を置く','',''),('03','四週間で試す','','')],meta_left='架空のワークショップ案。実績・健康効果の主張なし。',meta_right='01 / 04'))
flow=layouts.stage_flow([('03 min','一つ選ぶ'),('10 min','取り組む'),('05 min','メモする'),('02 min','次を残す')])
flow+=c.T(80,470,'20分の、サンプル行程。',39,c.INK1,700)+c.T(80,525,'時間配分は目安。仕事内容に合わせて、長さと順番を変える。',23,c.INK2)
flow+=c.L(80,580,1150,580,c.INK1,1.5)+c.T(80,624,'改善の実績を示す図ではありません。',19,c.INK2)
svgs.append(page(2,flow))
layer=layouts.tri_layer([('前日','手をつける場所を、一つ決める'),('朝','その一つから、始めてみる'),('最後','続きがわかる一言を、残す')])
svgs.append(page(3,layer))
lanes=[('取組',[('観察',0,1,'proposed'),('一つ試す',1,2,'proposed'),('続け方',3,1,'proposed')]),('記録',[('その日の一言を残す',0,4,'proposed')]),('相談',[('途中の相談',1,1,'proposed'),('振り返り',3,1,'proposed')])]
road=structures.swimlane_roadmap(40,190,1200,390,lanes,4,unit_label='週',legend=False)
road+=c.T(40,625,'試して合わなければ、時間や作業を変える。',28,c.INK1,700)
svgs.append(page(4,road))
(HERE/'svg_final').mkdir(exist_ok=True)
paths=[]
for i,s in enumerate(svgs,1):
 p=HERE/'svg_final'/f'slide-{i:02}.svg';p.write_text(skin(s,i),encoding='utf-8');paths.append(p)
notes={p.stem:data['notes'][i] for i,p in enumerate(paths)}
if not svg_to_native_pptx(paths,HERE/'deck.pptx',canvas_format='auto',notes=notes):raise SystemExit('Original conversion failed')
