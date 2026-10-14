"""Apply ABYR1206's chapter-divider PptxGenJS recipe and original SVG library."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'examples/repositories/hand-drawn-showcase'
UP=ROOT/'.build/actual-upstreams/ABYR1206__claude-skill-hand-drawn-slides'
FORK=ROOT/'skill-forks/hand-drawn-ja'
REPO='ABYR1206/claude-skill-hand-drawn-slides'
COMMIT='322a265344e73cd54f77f3f07b6a9f15bb7d2d99'
TITLE='チームのアイデアを、育てる。'
PROMPT='ABYR1206のhand-drawn-chapter-slides原典SKILL、PptxGenJSコード雛形、illustrations.mdの原SVGを使い、日本語の章扉5枚「チームのアイデアを、育てる。」を制作。表紙＋見つける／話してみる／試してみる／振り返る。フル業務資料ではなく章扉の作例。紙の暖色と鮮やかな朱赤、Zen Maru Gothic・Dela Gothic One・Manropeで、短い大見出しと余白、黒い手描き線とオフ白の象徴図形。背景、原SVG、左下章題、右下ページという原典の骨格を保つ。指示による和文書体/朱赤の変更を記録。架空のチームワークショップ導入案、実績・効果の主張なし。'
DATA={'title':TITLE,'sample_notice':'架空のワークショップ用章扉サンプル。フル業務資料、実績・効果の説明ではありません。','slides':[
 {'title':'チームのアイデアを、\n育てる。','label':'IDEAS / GROW TOGETHER','caption':'ひとつの気づきから、次の一歩へ。','topic':37,'background':'F4EADC','notes':'章扉だけの作例です。ここから先の活動内容はチームで組み立てます。'},
 {'title':'見つける。','label':'CHAPTER 01 / NOTICE','caption':'「ちょっと気になる」を、置き去りにしない。','topic':1,'background':'EEE0D0','notes':'小さな違和感やよかった場面を探す章。虫眼鏡は観察の入口を示します。'},
 {'title':'話してみる。','label':'CHAPTER 02 / SHARE','caption':'まだ答えにならない言葉にも、耳を澄ます。','topic':2,'background':'F7E6DE','notes':'考えを話し、違う見方を聴く章。原典の吹き出しで対話を示します。'},
 {'title':'試してみる。','label':'CHAPTER 03 / TRY','caption':'大きく決める前に、小さく手を動かす。','topic':20,'background':'E5E6D8','notes':'小さな試作へ進む章。階段は一歩ずつ進める試行を示します。'},
 {'title':'振り返る。','label':'CHAPTER 04 / LEARN','caption':'うまくいったことも、迷ったことも、次の種に。','topic':27,'background':'EFE6CE','notes':'試して気づいたことを持ち帰る章。循環矢印は次の試行へつなぐ学びを示します。'}]}

JS=r'''/* Direct adaptation of the original SKILL's PptxGenJS + sharp template. */
const fs=require('fs'),path=require('path');
const here=__dirname;
function load(name){try{return require(name)}catch{return require(path.resolve(here,'../../../.build/node_modules',name))}}
const pptxgen=load('pptxgenjs'),sharp=load('sharp');
async function svgToBase64Png(svgString,width,height){const pngBuffer=await sharp(Buffer.from(svgString)).resize(width,height,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toBuffer();return 'image/png;base64,'+pngBuffer.toString('base64')}
async function main(){const data=JSON.parse(fs.readFileSync(path.join(here,'input/data.json'),'utf8'));const pres=new pptxgen();pres.defineLayout({name:'CUSTOM_16x9',width:13.333,height:7.5});pres.layout='CUSTOM_16x9';pres.author='Studio Yebisu';pres.subject='日本語の手描き章扉サンプル';pres.title=data.title;pres.company='Studio Yebisu';pres.lang='ja-JP';
for(let i=0;i<data.slides.length;i++){const item=data.slides[i],slide=pres.addSlide();slide.background={color:item.background};
 const frame=`<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="950" viewBox="0 0 1800 950"><path d="M55 60 Q 885 48 1740 65 Q1753 450 1740 885 Q 900 896 55 881 Q43 430 55 60" fill="none" stroke="#DE4634" stroke-width="3" stroke-linejoin="round"/></svg>`;
 slide.addImage({data:await svgToBase64Png(frame,1800,950),x:.25,y:.2,w:12.82,h:6.76});
 const svg=fs.readFileSync(path.join(here,'illustrations',`chapter-${String(i).padStart(2,'0')}.svg`),'utf8');
 slide.addImage({data:await svgToBase64Png(svg,900,750),x:i===0?7.0:5.0,y:i===0?.65:.4,w:i===0?5.5:8.0,h:i===0?4.9:5.5});
 if(i===0){slide.addText(item.label,{x:.9,y:.75,w:6.5,h:.35,fontFace:'Manrope',fontSize:14,color:'141413',margin:0,charSpacing:2});slide.addText(item.title,{x:.88,y:2.0,w:7.0,h:2.15,fontFace:'Dela Gothic One',fontSize:42,color:'141413',bold:false,margin:0,breakLine:false});slide.addText(item.caption,{x:.95,y:5.65,w:9.5,h:.5,fontFace:'Zen Maru Gothic',fontSize:20,color:'141413',margin:0});}
 else{slide.addText(item.label,{x:1.0,y:4.96,w:6.5,h:.3,fontFace:'Manrope',fontSize:14,color:'141413',margin:0,valign:'bottom',charSpacing:1.5});slide.addText(item.title,{x:1.0,y:5.3,w:9.0,h:.8,fontFace:'Zen Maru Gothic',fontSize:44,color:'141413',bold:true,margin:0,valign:'top'});slide.addText(item.caption,{x:1.02,y:6.26,w:10.8,h:.5,fontFace:'Zen Maru Gothic',fontSize:18,color:'141413',margin:0});}
 slide.addText(String(i+1).padStart(2,'0'),{x:12.0,y:7.0,w:.65,h:.25,fontFace:'Manrope',fontSize:14,color:'141413',align:'right',margin:0,valign:'bottom'});
 slide.addText(i===0?'架空のチームワークショップ / 章扉の作例':'チームのアイデアを、育てる。 / 章扉サンプル',{x:.8,y:7.03,w:10.5,h:.22,fontFace:'Zen Maru Gothic',fontSize:9,color:'645D53',margin:0});slide.addNotes(item.notes);
}await pres.writeFile({fileName:path.join(here,'deck.pptx')});console.log('Generated original-recipe chapter dividers: 5 slides');}
main().catch(e=>{console.error(e);process.exit(1)});
'''

def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
 OUT.mkdir(parents=True,exist_ok=True);FORK.mkdir(parents=True,exist_ok=True)
 library=(UP/'hand-drawn-chapter-slides/scripts/illustrations.md').read_text(encoding='utf-8')
 blocks={int(n):svg for n,svg in re.findall(r'### (\d+)\.[^\n]*\n.*?```svg\s*(.*?)```',library,re.S)}
 for i,item in enumerate(DATA['slides']):write(OUT/f'illustrations/chapter-{i:02}.svg',blocks[item['topic']].strip())
 write(OUT/'build.cjs',JS);write(OUT/'input/data.json',json.dumps(DATA,ensure_ascii=False,indent=2));write(OUT/'input/BRIEF.md','# 章扉の制作依頼\n\n'+PROMPT);write(OUT/'PROMPT.txt',PROMPT+'\n')
 write(OUT/'package.json',json.dumps({'private':True,'scripts':{'build':'node build.cjs'},'dependencies':{'pptxgenjs':'^4.0.1','sharp':'^0.34.0'}},indent=2))
 write(OUT/'.gitignore','node_modules/\ncache/\n__pycache__/\n*.log\n')
 for folder,files in [('zenmarugothic',['ZenMaruGothic-Bold.ttf','ZenMaruGothic-Regular.ttf']),('delagothicone',['DelaGothicOne-Regular.ttf']),('manrope',['Manrope[wght].ttf'])]:
  (OUT/'fonts').mkdir(exist_ok=True)
  for f in files:shutil.copy2(ROOT/'downloads/fonts'/folder/f,OUT/'fonts'/f)
  shutil.copy2(ROOT/'downloads/fonts'/folder/'OFL.txt',OUT/'fonts'/f'{folder}-OFL.txt')
 for name in ['LICENSE','README.md','hand-drawn-chapter-slides/SKILL.md','hand-drawn-chapter-slides/scripts/illustrations.md','examples/demo-chapter-slides.pptx']:
  target=OUT/'upstream'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UP/name,target)
 shutil.copy2(UP/'LICENSE',OUT/'LICENSE')
 if not args.prepare_only:subprocess.run(['node',str(OUT/'build.cjs')],cwd=ROOT,check=True)
 finish(args.prepare_only)

def finish(prepared):
 source={'repository':REPO,'commit':COMMIT,'license':'MIT','scope':'Japanese chapter-divider implementation using original PptxGenJS recipe and SVG library','upstream_preserved':True,'case_studies':['hand-drawn-showcase']}
 write(OUT/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 refs=[{'path':p,'sha256':hashlib.sha256((UP/p).read_bytes()).hexdigest(),'url':f'https://github.com/{REPO}/blob/{COMMIT}/{p}'} for p in ['hand-drawn-chapter-slides/SKILL.md','hand-drawn-chapter-slides/scripts/illustrations.md','examples/demo-chapter-slides.pptx','LICENSE']]
 write(OUT/'PROVENANCE.json',json.dumps(dict(source,source_refs=refs,method='Instruction-driven original SKILL PptxGenJS+sharp authoring pattern applied directly; original SVGs 37/1/2/20/27 extracted unchanged; original 13.333×7.5 lower-left chapter title and bottom-right page recipe retained.',applied=['Original svgToBase64Png sharp rasterization and addImage path.','Original fill #FAF8F2, thick irregular stroke #141413.','Original left-bottom chapter hierarchy and right-side illustration.','Original demo provided and viewed as composition reference, not a replaced runtime.'],modifications=['User-directed Japanese type roles: Dela Gothic One / Zen Maru Gothic / Manrope replace Georgia/Calibri.','User-directed warm paper with vermilion irregular frame replaces fully muted palette.','Cover seedling and short supporting line added.'],fonts='Original full TTF/OFL packaged. No embedded font or OS installation; recipient can install original fonts manually.'),ensure_ascii=False,indent=2))
 write(OUT/'README.md','''# チームのアイデアを、育てる。

表紙＋「見つける／話してみる／試してみる／振り返る」の5枚。架空のワークショップ用の**章扉サンプル**です。フル業務資料ではありません。

原典 ABYR1206/claude-skill-hand-drawn-slides の SKILL にあるPptxGenJS＋sharp雛形と原SVGを直接適用。13.333×7.5、オフ白の図形、太い黒線、右側イラスト、左下章題、右下ページを保持。原demoも参照として同梱。日本語書体と朱赤の手描き枠は今回の指定による変更です。

再生成: `npm install` → `npm run build`。依存はPptxGenJS（MIT）とsharp（Apache-2.0、libvips等の個別条件を含む）。原典MIT・利用SVGの帰属はLICENSE/upstream、依存の原文条件はdependency-licenses/を参照。依存バイナリやnode_modulesはZIPに含めません。

PPTXの文字は編集可能、手描き図形は原典方式のSVG→PNG。書体は埋込みません。指定書体で編集・表示するには fonts/ の原TTFを手動導入してください。SIL OFL同梱。

閲覧素材はPowerPointから書き出したPNG/PDF。生成と主画面の初回確認のみ実施し、全ページ詳細検査・構造監査・ZIP再実行は行いません。
''')
 write(FORK/'SKILL.md','''---
name: hand-drawn-ja
description: 原典の手描きSVGとPptxGenJS雛形で日本語の章扉PPTXを作る。
---

# チーム向け手描き章扉

1. `upstream/hand-drawn-chapter-slides/SKILL.md` と `scripts/illustrations.md` を読む。章扉5枚など、タイトルと章の役割を先に決める。フル資料とは区別する。
2. 原典PptxGenJS＋sharp雛形を使う。13.333×7.5、オフ白の図形、太い墨線、右側の象徴、左下の章題、右下の番号を保つ。
3. 観察には虫眼鏡、対話には吹き出し、試行には階段など意味に合う原SVGを選ぶ。新しい図形も不均一なBezier線と単色塗りで。
4. 日本語見出しZen Maru Gothic、表紙Dela Gothic One、英数字Manropeなど役割を分ける。意味のまとまりで改行し、説明を詰め込まない。書体・配色を変更したら原典との差分を短く記す。
5. 同梱 `references/build.cjs` と入力を参考に `npm install pptxgenjs sharp` → `node build.cjs`。原MITと使用SVGの帰属、フル書体TTFのOFLを残す。

本文だけで生成器は付属しません。一式ZIPの原典・build.cjs・inputを利用してください。フォントは手動導入が必要。確認は生成成功と代表画面の初回表示に絞り、採用とは区別します。
''')
 if not (FORK/'upstream').exists():shutil.copytree(OUT/'upstream',FORK/'upstream')
 shutil.copy2(UP/'LICENSE',FORK/'LICENSE');write(FORK/'references/build.cjs',JS);write(FORK/'references/input/data.json',json.dumps(DATA,ensure_ascii=False,indent=2))
 (FORK/'references/illustrations').mkdir(exist_ok=True)
 for i,item in enumerate(DATA['slides']):shutil.copy2(OUT/f'illustrations/chapter-{i:02}.svg',FORK/'references/illustrations'/f'chapter-{i:02}.svg')
 source['files']=[{'path':p.relative_to(FORK).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json']
 write(FORK/'SOURCE.json',json.dumps(source,ensure_ascii=False,indent=2))
 case={'id':'hand-drawn-showcase','title':TITLE,'repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':'hand-drawn-ja','page_count':5,'format':'pptx','preview_kind':'powerpoint-render','preview_canvas':{'width':1600,'height':900},'style':'暖色の紙 × 朱赤 / 手描き章扉','use_case':'ワークショップ・章扉サンプル','preview':'examples/repositories/hand-drawn-showcase/index.html','cover':'examples/repositories/hand-drawn-showcase/render/slide-01.png','interior':'examples/repositories/hand-drawn-showcase/render/slide-03.png','pages':[f'examples/repositories/hand-drawn-showcase/render/slide-{i:02}.png' for i in range(1,6)],'artifact_download':'examples/repositories/hand-drawn-showcase/deck.pptx','pdf_download':'examples/repositories/hand-drawn-showcase/render/deck.pdf','source_download':'downloads/hand-drawn-example-ja.zip','fork_download':'downloads/hand-drawn-ja.zip','input':'examples/repositories/hand-drawn-showcase/input/BRIEF.md','input_data':'examples/repositories/hand-drawn-showcase/input/data.json','prompt':'examples/repositories/hand-drawn-showcase/PROMPT.txt','prompt_text':PROMPT,'provenance':'examples/repositories/hand-drawn-showcase/PROVENANCE.json','qa':'examples/repositories/hand-drawn-showcase/QA.json','guide':'examples/repositories/hand-drawn-showcase/README.md','titles':[s['title'].replace('\n','') for s in DATA['slides']],'notes':[s['notes'] for s in DATA['slides']],'sample_notice':DATA['sample_notice'],'method':'Original instruction-driven PptxGenJS + sharp template and original SVG library; author implementation, Japanese font/color adaptation.','editability':'native_pptx_text_with_raster_doodles','navigation':'native-runtime-bridge','status':'prepared' if prepared else 'generated','execution_status':'prepared' if prepared else 'generated'}
 write(ROOT/'data/sol-hand-drawn-repository-examples.json',json.dumps([case],ensure_ascii=False,indent=2))
 guide={'repository':REPO,'production_status':case['status'],'execution_status':case['execution_status'],'execution_type':'original_instruction_recipe_pptxgenjs','case_ids':[case['id']],'summary_ja':'原典の手描きSVGとPptxGenJS雛形で日本語章扉5枚。フル業務資料ではなく表紙＋4章のサンプル。','requirements':['Node.js','PptxGenJS','sharp','任意:指定TTFの手動導入'],'steps':['章の役割を決める','原SVGを選ぶ','原典雛形へ和文コピーを適用','PowerPointから閲覧PNG/PDFを出す'],'commands':['npm install','npm run build'],'source_refs':refs,'upstream_commit':COMMIT,'license':'MIT','skill':'skill-forks/hand-drawn-ja/SKILL.md','guide':case['guide']}
 write(ROOT/'data/sol-hand-drawn-repository-guides.json',json.dumps([guide],ensure_ascii=False,indent=2))

def package():
 for folder,name in [(OUT,'hand-drawn-example-ja'),(FORK,'hand-drawn-ja')]:
  with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.parts)&{'node_modules','cache','__pycache__'} and p.suffix!='.log':z.write(p,(Path(name)/p.relative_to(folder)).as_posix())
if __name__=='__main__':main()
