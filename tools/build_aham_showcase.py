"""Use Aham's frozen layout IDs and SVG→native PPTX wrapper directly."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'examples/repositories/aham-showcase';FORK=ROOT/'skill-forks/aham-ja';UP=ROOT/'.build/actual-upstreams/Aham-AIAPP__aham-ppt'
REPO='Aham-AIAPP/aham-ppt';COMMIT='c2b4ece69bbac777557934f981457c1f98c2b73f'
TITLE='朝の20分を、組み直す。'
PROMPT='Aham原典の39layoutID体系からSPC/E-03/E-04/A-90を選び、固有themes/layouts/structuresの凍結座標とsvg_to_native_pptx経路で日本語4枚「朝の20分を、組み直す。」を制作。架空の働き方ワークショップ案。20分のサンプル配置は3+10+5+2分、4週間は試行計画で実績ではない。健康・生産性改善の保証なし。コバルト・黄色・墨、大きな和文、編集できる図解と大胆な面の切替。Zen Kaku Gothic New/Manropeの原TTF/OFL同梱。原版式の座標・接続を保持し、和文化・角丸削除・配色変更だけ記録。'
TITLES=[TITLE,'朝は一つ選んで、次を残す。','作業を始める前に、入口を用意する。','四週間で、続け方を確かめる。']
NOTES=['架空の働き方ワークショップ案です。朝の20分は例示の配置で、効果を実証した方法ではありません。','3分で一つ選び、10分取り組み、5分でメモし、2分で次を残す案です。合計20分。仕事の条件に合わせて調整します。','前日に入口を用意し、朝は一つの作業に取り組み、最後に続きを残す三層の配置案です。','一週目に観察、二・三週目に一つ試し、四週目に続け方を話す例示計画。記録と相談を並行させ、負担があれば変更します。']
AUTHOR=r'''from pathlib import Path
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
'''
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def main():
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True)
 (OUT/'upstream').mkdir(exist_ok=True)
 for name in ['assets','references']:
  dest=OUT/'upstream'/name
  if not dest.exists():shutil.copytree(UP/name,dest,ignore=shutil.ignore_patterns('shots','social-preview*','wechat-qr*','__pycache__'))
 for name in ['SKILL.md','README.md','LICENSE','NOTICE.md','ORIGIN.md','requirements.txt']:shutil.copy2(UP/name,OUT/'upstream'/name)
 shutil.copy2(UP/'LICENSE',OUT/'LICENSE');shutil.copy2(UP/'NOTICE.md',OUT/'NOTICE.md')
 data={'title':TITLE,'titles':TITLES,'notes':NOTES,'layout_ids':['SPC cover','E-03','E-04','A-90'],'sample_notice':'架空のワークショップ案。20分と四週間はサンプル行程・試行期間で、効果の実績や健康主張ではありません。','durations_minutes':[3,10,5,2]}
 write(OUT/'input/data.json',json.dumps(data,ensure_ascii=False,indent=2));write(OUT/'input/BRIEF.md','# 制作依頼\n\n'+PROMPT);write(OUT/'PROMPT.txt',PROMPT);write(OUT/'generate.py',AUTHOR);write(OUT/'.gitignore','.venv/\n**/__pycache__/\n*.log\n')
 for folder,files in [('zenkakugothicnew',['ZenKakuGothicNew-Regular.ttf','ZenKakuGothicNew-Bold.ttf']),('manrope',['Manrope[wght].ttf'])]:
  (OUT/'fonts').mkdir(exist_ok=True)
  for filename in files:shutil.copy2(ROOT/'downloads/fonts'/folder/filename,OUT/'fonts'/filename)
  shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt')
 py=OUT/'.venv/Scripts/python.exe'
 subprocess.run([str(py),str(OUT/'generate.py')],check=True,cwd=ROOT)
 subprocess.run([str(py),str(OUT/'upstream/assets/tools/lint_svg.py'),str(OUT/'svg_final')],check=True,cwd=ROOT)
 finish(data)
def finish(data):
 source={'repository':REPO,'commit':COMMIT,'license':'MIT','scope':'Original 39-layout-ID system: SPC/E-03/E-04/A-90 functions and original SVG native converter','case_studies':['aham-showcase'],'upstream_preserved':True}
 write(OUT/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 refs=[{'path':p,'sha256':hashlib.sha256((UP/p).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{COMMIT}/{p}'} for p in ['SKILL.md','references/layout-library.md','assets/components/layouts.py','assets/components/themes.py','assets/components/structures.py','assets/svg_to_pptx_wrapper.py','assets/svg_to_pptx/LICENSE_NOTE.md','LICENSE']]
 write(OUT/'PROVENANCE.json',json.dumps(dict(source,source_refs=refs,method='Original themes.cover and themes.chrome; frozen E-03 stage_flow, E-04 tri_layer, A-90 swimlane_roadmap; original svg_to_native_pptx wrapper → bundled ppt-master native DrawingML converter.',modifications=['Post-SVG font-family replaces Chinese/Inter stacks with Zen Kaku Gothic New and Manrope.','Color skin: cobalt/yellow/ink surfaces; square corners; default labels translated into Japanese.','No layout coordinate edits: component function coordinates and connectors preserved. Supplemental lines use original T/L atoms.','User-directed colors and typography differ from original restrained A/B/C style rules; no engine replacement.'],font_delivery='Original TTF/OFL packaged; fonts not embedded or installed automatically.',api_calls=0),ensure_ascii=False,indent=2))
 write(OUT/'README.md','''# 朝の20分を、組み直す。

架空の働き方ワークショップ案、4枚。20分は3+10+5+2分の例示行程、四週間は試行の計画です。改善効果の実績や健康主張はありません。

原典 Aham-AIAPP/aham-ppt の39 layoutID体系から SPC/E-03/E-04/A-90を実使用。themesの表紙・chrome、layouts.stage_flow/tri_layer、structures.swimlane_roadmapの凍結座標・接続をそのまま呼び、SVG唯一原稿から原典svg_to_native_pptxで編集可能なPPTXへ変換。汎用rendererへの置換ではありません。

変更は和文コピー、原TTFの書体指定、コバルト/黄色/墨への色置換、角丸除去。原典の白・単色を中心とするA/B/C規則とは異なるユーザー指定のskinです。

再生成: Python環境へ `pip install -r upstream/requirements.txt` → `python generate.py`。SVGはsvg_final/、完成ファイルdeck.pptx。原典lintは `python upstream/assets/tools/lint_svg.py svg_final`。PNG/PDFはPowerPointで書き出した閲覧用素材です。

原典MIT/NOTICE/ORIGINを保持。原典同梱のppt-master派生変換器は assets/svg_to_pptx/LICENSE_NOTE.md のMIT全文と帰属を保持。Python依存はpython-pptx(MIT)、CairoSVG(LGPL-3.0)、その依存の個別条件。依存バイナリ・venvはZIPへ含めません。TTFは公式原配布物・OFL同梱、端末への導入は手動です。

生成と表紙初回表示だけを確認し、全ページ詳細目視・独立レビュー・構造監査・ZIP再実行は行いません。
''')
 write(FORK/'SKILL.md','''---
name: aham-ja
description: Aham固有layoutIDと凍結座標のSVG部品を使い、編集可能な日本語PPTXを作る。
---

# 日本語の編集できる図解PPTX

1. upstream/SKILL.md、references/layout-library.mdと必要な骨格を読み、原39layoutIDから目的に合うものを選ぶ。例はSPC/E-03/E-04/A-90。
2. 原典themes/layouts/structuresの関数と定義済み座標を使い、SVGを唯一原稿にする。数字は入力正本から、試行案と実績を分ける。
3. 日本語の見出しを大きく、図内は短く。見出し・本文Zen Kaku Gothic New、英数字Manropeなど役割を指定。意味のまとまりで改行し、過密なら枚数を分ける。
4. 配色・書体のskin変更を記録。関数の座標と接続を保ち、原典svg_to_native_pptx_wrapperの経路でnative PPTXへ変換する。
5. `pip install -r upstream/requirements.txt` → `python generate.py`。原典lintと主画面初回表示だけ確認。技能本文だけでは変換器と入力は付属しないため、一式ZIPと作品ZIPの生成ソースを使用。

原MIT・NOTICE・ppt-master派生のLICENSE_NOTE・使用TTF/OFLを保持。OSへの書体導入は手動。API keyは不要。
''')
 if not (FORK/'upstream').exists():shutil.copytree(OUT/'upstream',FORK/'upstream',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 shutil.copy2(UP/'LICENSE',FORK/'LICENSE');shutil.copy2(UP/'NOTICE.md',FORK/'NOTICE.md')
 write(FORK/'references/generate.py',AUTHOR);write(FORK/'references/input/data.json',json.dumps(data,ensure_ascii=False,indent=2))
 source['files']=[{'path':p.relative_to(FORK).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json'];write(FORK/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 case={'id':'aham-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':'aham-ja','page_count':4,'format':'pptx','preview_kind':'powerpoint-render','preview_canvas':{'width':1600,'height':900},'style':'コバルト × 黄色 × 墨 / 凍結座標のnative図解','use_case':'働き方ワークショップ案','preview':'examples/repositories/aham-showcase/index.html','cover':'examples/repositories/aham-showcase/render/slide-01.png','interior':'examples/repositories/aham-showcase/render/slide-03.png','pages':[f'examples/repositories/aham-showcase/render/slide-{i:02}.png' for i in range(1,5)],'artifact_download':'examples/repositories/aham-showcase/deck.pptx','pdf_download':'examples/repositories/aham-showcase/render/deck.pdf','source_download':'downloads/aham-example-ja.zip','fork_download':'downloads/aham-ja.zip','input':'examples/repositories/aham-showcase/input/BRIEF.md','input_data':'examples/repositories/aham-showcase/input/data.json','prompt':'examples/repositories/aham-showcase/PROMPT.txt','prompt_text':PROMPT,'provenance':'examples/repositories/aham-showcase/PROVENANCE.json','qa':'examples/repositories/aham-showcase/QA.json','guide':'examples/repositories/aham-showcase/README.md','titles':TITLES,'notes':NOTES,'sample_notice':data['sample_notice'],'method':'Original frozen SPC/E-03/E-04/A-90 SVG functions and original native converter. Japanese color/font skin only.','navigation':'native-runtime-bridge','editability':'native_pptx_text_and_diagrams','status':'generated','execution_status':'generated'}
 write(ROOT/'data/sol-aham-repository-examples.json',json.dumps([case],ensure_ascii=False,indent=2))
 guide={'repository':REPO,'production_status':'generated','execution_status':'generated','execution_type':'original_layout_functions_svg_native_conversion','case_ids':[case['id']],'summary_ja':'原典の凍結座標layoutIDとSVG-native converterで日本語4枚の架空ワークショップ案。','requirements':['Python','python-pptx','CairoSVG（native経路ではPNG fallback不要）'],'steps':['入力とlayoutIDを決める','原典部品でSVGを生成する','native wrapperでPPTXへ変換','初回表示と閲覧PNG/PDFを出す'],'commands':['pip install -r upstream/requirements.txt','python generate.py'],'source_refs':refs,'upstream_commit':COMMIT,'license':'MIT','skill':'skill-forks/aham-ja/SKILL.md','guide':case['guide']};write(ROOT/'data/sol-aham-repository-guides.json',json.dumps([guide],ensure_ascii=False,indent=2))
def package():
 for folder,name in [(OUT,'aham-example-ja'),(FORK,'aham-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.parts)&{'.venv','__pycache__','cache'} and p.suffix not in {'.pyc','.log'}:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())
if __name__=='__main__':main()
