"""Synchronize current SVG source, honest export scope, and distribution."""
from pathlib import Path
import hashlib,json,shutil,zipfile,xml.etree.ElementTree as ET
import pymupdf
ROOT=Path(__file__).resolve().parents[1];CASE=ROOT/'examples/repositories/sebastian-188';FORK=ROOT/'skill-forks/sebastian-188-ja'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
SKILL='''---
name: ppt-svg-generator-ja
description: Markdownをページ構成とデザインに分け、文字・図形をソースで編集できるSVGへ組み立てる。
---

# MarkdownからSVGの資料を作る

原典 vigorX777/ppt-svg-generator / c873b61673ab0ada5c09f863bff89c8f1b3248fb / MIT。非公式の日本語案内。source/upstreamのSKILLとcommands/specs/stylesを読む。

1. /ppt-analyze @原稿.mdで、見出し・要点・頁型・密度をページ構成にする。目的と読み手に合わせて直す。
2. /ppt-designで、ミニマル・コンサルティング・暗色技術・Swiss・ブランド青の5プリセット、自作、AI推薦から選ぶ。配色・書体・余白・寸法を生成前に固定する。
3. /ppt-generateで、その構成と設計から頁別SVGを作る。原典のSVG互換規範に従い、UTF-8、style属性の書式、6桁色、左寄せ座標、filterなし、1920×1080を確認する。角丸が必要ならrxの代わりにpathを使う。
4. 全頁を描画して、元原稿との対応、日本語、文字・図の欠け、重なり、余白を確認し直す。PPT向けの互換規範を守ることと、実際にPowerPointへ取り込めることを区別する。
5. 必要なら/ppt-exportでPDF/PPTXを作る。PowerPointでSVGを挿入して「図形に変換」する場合は、文字位置・書体・図の編集性を実機で確認する。プリセットでまとめて進める場合は/ppt-quick @原稿.md --style=…を使う。

## この7枚の再現

架空のAI依頼例集をSwissの赤・黒・白でSVGへ組んだ。今回の修復では、原稿とinput/data.jsonから構成・目的を先に保存し、design.jsonの日本語書体・配色を生成器が読んでからSVGを作る。固定原稿用の著述コードで、Markdownを任意に自動解析するアプリではない。

原典の中国語font stackは、日本語字形を優先するNoto Sans CJK JPへ明示変更。原典PDF exporterを使用し、WindowsではSVG_CHROME_EXECUTABLEで既存Chromeを選べる1か所だけを追加。原本とdiffを同梱する。全7頁のPDF実画像とHTMLプレイヤーの7頁送り・戻りを確認した。PowerPointへの挿入・図形変換、原典PPTX export、独立再評価は未実施。

## 環境

Python＋PyMuPDF、Node.js＋playwright1.62.1/pdf-lib1.17.1、利用可能なChromeまたはPlaywright Chromium、Noto Sans CJK JP。書体は公式Noto CJKのOFL配布物を別途導入し、OSフォントを抽出しない。

キットのルートで `npm ci --prefix source`。既存Chromeなら環境変数SVG_CHROME_EXECUTABLEに実行ファイルを指定し、`python source/build.py`。構成・デザイン・SVGとPDFを作る。新出力の全頁を再確認する。修復の再現検査は既存依存を使用し、新しい環境へのnpm ciは未実施。

原典: https://github.com/vigorX777/ppt-svg-generator/tree/c873b61673ab0ada5c09f863bff89c8f1b3248fb
書体: https://github.com/notofonts/noto-cjk
'''

def package():
 for folder,name in [(CASE,'sebastian-188-example-ja.zip'),(FORK,'sebastian-188-ja.zip')]:
  with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as z:
   for p in sorted(folder.rglob('*')):
    if p.is_file() and not set(p.relative_to(folder).parts)&{'.private','.git','node_modules','__pycache__','.venv'} and p.suffix!='.pyc':z.write(p,folder.name+'/'+p.relative_to(folder).as_posix())
  with zipfile.ZipFile(ROOT/'downloads'/name) as z:assert z.testzip() is None

def main():
 export=load(CASE/'source/original-export-receipt.json');assert export['exit_code']==0
 doc=pymupdf.open(CASE/'deck.pdf');assert len(doc)==7
 svg=[]
 for p in sorted((CASE/'svg').glob('*.svg')):
  tree=ET.fromstring(p.read_text(encoding='utf-8'));assert tree.attrib['viewBox']=='0 0 1920 1080';assert all(not k.startswith('{http://www.w3.org/2000/svg}filter') for k in [x.tag for x in tree.iter()]);assert 'Microsoft YaHei' not in p.read_text(encoding='utf-8');svg.append(dict(path=p.relative_to(CASE).as_posix(),sha256=sha(p)))
 qa={'status':'all7_pdf_visual_and_original_export_checked','scope':'Technical and author visual QA; independent review pending.','plan_before_svg':'source/plan-before-svg.json','original_export':'source/original-export-receipt.json','adaptation':'Only optional Chrome executable selection in exporter; Japanese font stack in authored SVG.','svg_parse':7,'svg_files':svg,'pdf_pages':7,'all7_actual_images_viewed':True,'browser_runtime':'source/browser-runtime.json','powerpoint_svg_insertion_or_shape_conversion':False,'original_pptx_export':False,'independent_review':'pending_after_repair'}
 if (CASE/'source/zip-replay.json').exists():qa['distribution_replay']='source/zip-replay.json'
 dump(CASE/'QA.json',qa)
 prov=load(CASE/'PROVENANCE.json')
 if 'initial_record' not in prov:prov={'initial_record':prov,'repository':'vigorX777/ppt-svg-generator','commit':'c873b61673ab0ada5c09f863bff89c8f1b3248fb','license':'MIT'}
 prov.update(repair_author='Codex',current_route='Pre-existing structure/design → authored SVG → original PDF exporter with one Chrome-path adapter → all7page visual review.',font='Noto Sans CJK JP first; explicit Japanese adaptation',not_executed=['PowerPoint SVG insertion/shape conversion','Original PPTX export','Independent repaired-candidate grading']);dump(CASE/'PROVENANCE.json',prov)
 for folder in [CASE,FORK]:(folder/'SKILL.md').write_text(SKILL,encoding='utf-8')
 (CASE/'README.md').write_text('''# MarkdownをSVGのページへ組む

原稿を「ページ構成→デザイン→SVG」に分けるスキルです。本作例はSwissの赤・黒・白を使った架空例集7頁。文字・図形はsvg/で編集でき、PDFは固定レイアウトです。

今回の修復では構成と設計を先に保存し、生成器が日本語font stackと配色を読みます。全7頁の実PDFを見て、HTMLでも全7頁の送り戻りを確認。原典PDF exporterを実行し、既存Chromeを選ぶ1行のadapterを加えました。原本・diff・実行記録はsource/にあります。PowerPointへの挿入・図形変換と原典PPTX exportは未確認です。

再現: Python＋PyMuPDF、Node.jsとsource/package-lock.jsonの依存、Chrome/Chromium、Noto Sans CJK JPを用意。`npm ci --prefix source` → 必要ならSVG_CHROME_EXECUTABLEを設定 → `python source/build.py`。新しい環境へのnpm ciは未実施。現在の固定7頁を作り直すコードであり、題材変更時は構成・デザイン・著述内容を変更します。再生成後は全頁を確認してください。

初回は構成と設計を生成後に書き出し、InkscapeでPDF化していました。その履歴はPROVENANCE.jsonに保持。今回の検査と混同しません。独立再評価・正式採用は別です。原典MITと帰属を保持し、OSの書体ファイルは同梱しません。
''',encoding='utf-8')
 (CASE/'PROMPT.txt').write_text('Markdownを頁別の構成・目的へ分け、Swiss配色と日本語font stackを生成前に固定し、SVGへ著述する。架空例の入力を正本にし、事実を加えない。原典PDF exporterを実行して全7頁を確認する。Windowsで既存Chromeを選ぶadapterの差分を保持する。PowerPoint図形変換を未検証のまま成功と書かない。\n',encoding='utf-8')
 for p in CASE.rglob('*'):
  if p.is_file() and not set(p.relative_to(CASE).parts)&{'.private','node_modules','__pycache__'}:
   q=FORK/p.relative_to(CASE);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
 source=load(FORK/'SOURCE.json');source['repair_scope']='Structure/design precede authored SVG; original PDF exporter used with explicit Chrome adapter; all7PDF pages and browser navigation checked.';source['files']=[dict(path=p.relative_to(FORK).as_posix(),sha256=sha(p)) for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json' and not set(p.relative_to(FORK).parts)&{'.private','node_modules','__pycache__'}];dump(FORK/'SOURCE.json',source)
 p=ROOT/'data/skill-effect-patches/native-03.json';old=next(r for r in load(p) if r['case_id']=='sebastian-188');patch=json.loads(json.dumps(old))
 steps=['Markdownを目的・見出し・要点・頁型・密度へ分け、構成を保存する。','5プリセット・自作・AI推薦からデザインを決め、構成と設計からSVGを著述する。','SVGを全頁描画して直す。必要なら原典exportを使う。PowerPointの図形変換は実機で確認する。']
 limits=['今回の出力はSVGとPDF。PowerPointへの挿入・図形変換と原典PPTX exportは未確認。','固定7頁の著述コード。任意Markdownの自動解析器ではない。','原典PDF exporterへChrome実行ファイルを選ぶadapterを追加。原本と差分を同梱。','原典の中国語字体順を、日本語字形を優先するNoto Sans CJK JPへ変更。書体は別途導入。','修復後の独立再評価と新環境へのnpm ciは未実施。']
 patch.update(name='Markdownを、編集できるSVGのページへ',change='原稿をページ構成とデザインに分け、文字・図形をソースで調整できるSVG資料へ組める。',how_to_use=steps,constraints=limits)
 patch['demonstration']['summary']='原稿から7頁の構成・目的とSwissデザインを先に保存し、生成器がそれを読んでSVGへ著述。日本語書体を優先し、原典PDF exporterと全7頁の実表示を確認した。'
 patch['demonstration']['not_demonstrated']=['PowerPointへの挿入・図形変換','原典PPTX export','修復後の独立再評価','新環境への依存導入']
 patch['demonstration']['source_proof_paths']+=['examples/repositories/sebastian-188/source/'+f for f in ['plan-before-svg.json','original-export-receipt.json','export_pdf.js.diff','original-script-identity.json','browser-runtime.json']]
 patch['guide_patch'].update(summary_ja=patch['change'],steps=steps,limitations=limits,requirements=['Python＋PyMuPDF','Node.js＋playwright1.62.1/pdf-lib1.17.1','Chrome/ChromiumとNoto Sans CJK JP'],production_status='plan_before_svg_original_pdf_export_all7_checked_independent_pending')
 p=ROOT/'data/skill-effect-patches/repairs-native-root.json';rows=load(p);dump(p,[r for r in rows if r['case_id']!='sebastian-188']+[patch])
 p=ROOT/'data/sol-sebastian-batch2-repository-examples.json';rows=load(p)
 for r in rows:
  if r['id']=='sebastian-188':r.update(preview_image_notice='原典PDF exporterで出力した全7頁。構成・設計を先に保存してSVG生成。PowerPoint図形変換は未確認。',execution_status='original_pdf_export_all7_visual_checked',sample_notice='架空例。SVGとPDFを全7頁確認。PPTXと図形変換は未実施。',prompt_text=(CASE/'PROMPT.txt').read_text(encoding='utf-8').strip())
 dump(p,rows);package();print('SVG generator: ordered plans, Japanese font, original PDF export,7 actual pages, current guide and2ZIPs synchronized.')
if __name__=='__main__':main()
