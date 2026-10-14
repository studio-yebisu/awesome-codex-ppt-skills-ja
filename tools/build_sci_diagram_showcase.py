"""Build/package SciDiagram's official PptxGenJS portable template adaptation.

Native Japanese concept diagrams; Apache-2.0 derived template, PptxGenJS MIT.
This developer builder is invoked from the catalog; user kits execute build.mjs.
"""
from pathlib import Path
import argparse, json, shutil, subprocess, os, hashlib, zipfile, re

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'data/repository-guides.json').exists())
CASE=ROOT/'examples/repositories/sci-diagram-showcase'
FORK=ROOT/'skill-forks/sci-diagram-ja'
UP=ROOT/'.build/actual-upstreams/HututuWorks__sci-diagram-pptx'
SKILL=UP/'skills/sci-diagram-pptx'
COMMIT='cc8f0030edf80eeab6e52849b8c39fe638466776'
NODE=os.environ.get('SCI_DIAGRAM_NODE') or 'C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
PKG=Path('C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pptxgenjs')

def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def template_build():
    code=(SKILL/'assets/pptxgenjs-build-template.mjs').read_text(encoding='utf-8')
    code=code.replace('// Portable SciDiagram PPTX build template.','// Apache-2.0 derivative of HututuWorks/sci-diagram-pptx portable template.\n// Pinned commit cc8f0030edf80eeab6e52849b8c39fe638466776.\n// Five new scientific concept diagrams, not source-image reconstruction.\n// Runtime: Node.js 24.19.0 / PptxGenJS 4.0.1 (MIT).')
    code=code.replace('"editable.pptx"','"deck.pptx"')
    code=re.sub(r'const SOURCE = \{.*?\};','const SOURCE = { file: "input.json", width: 1280, height: 720 };',code,count=1,flags=re.S)
    start=code.index('// Standard editable objects')
    end=code.index('const SHAPE_TYPES')
    code=code[:start]+'''// Explicit semantic map, supplied by the original concept-model input.
const DIAGRAMS = JSON.parse(fs.readFileSync(path.join(BUILD_DIR, "input.json"), "utf8"));
let NODES = [], EDGES = [], INSETS = [];

'''+code[end:]
    code=code.replace('  rect: "rect",','  textbox: "textbox",\n  rect: "rect",')
    start=code.index('function addNode(')
    end=code.index('async function main()',start)
    code=code[:start]+'''function addNode(slide, node) {
  const box=toSlideBox(node.box);
  if(node.type !== "textbox") {
    slide.addShape(SHAPE_TYPES[node.type], {
      ...box, objectName:`Node:${node.id}`,
      fill:{color:node.fill}, line:{color:node.fill, width:0},
    });
  }
  if(node.text) slide.addText(node.text, {
    ...box, objectName:`Node-label:${node.id}`,
    fontFace:node.fontFace??"Zen Kaku Gothic New",fontSize:node.fontSize??21,
    bold:node.bold??false,color:node.color??"12384C",margin:0,
    align:"left",valign:"top",breakLine:false,paraSpaceAfterPt:0,
  });
}

'''+code[end:]
    code=code.replace('  validatePortableMap();','')
    code=code.replace('pptx.author = "SciDiagram PPTX";','pptx.author = "Studio Yebisu / SciDiagram portable adaptation";')
    code=code.replace('pptx.title = "SciDiagram portable reconstruction";','pptx.title = "雨が、地下水になるまで。";')
    code=code.replace('"en-US"','"ja-JP"').replace('headFontFace: "Arial"','headFontFace: "Zen Kaku Gothic New"').replace('bodyFontFace: "Arial"','bodyFontFace: "Zen Kaku Gothic New"')
    start=code.index('  const slide = pptx.addSlide();')
    end=code.index('  await pptx.writeFile',start)
    code=code[:start]+'''  for(const diagram of DIAGRAMS) {
    // One source-to-slide transform. Stable IDs and explicit edge topology.
    NODES=diagram.NODES;EDGES=diagram.EDGES;INSETS=diagram.INSETS;
    validatePortableMap();
    const slide=pptx.addSlide();slide.background={color:diagram.bg};
    // Native earth/water plates are scientific regions, not endpoint boxes.
    // Draw regions first, then original template's directed paths, then labels
    // so earth fills cannot obscure arrows inside the conceptual section.
    for(const node of NODES.filter(n=>n.type!=="textbox"))addNode(slide,node);
    for(const edge of EDGES) {
      if(edge.direction==="forward")connectOneWay(slide,edge);
      else if(edge.direction==="both")connectBothWays(slide,edge);
      else connectExactPath(slide,edge,"none");
      addEdgeLabel(slide,edge);
    }
    for(const inset of INSETS)addInset(slide,inset);
    for(const node of NODES.filter(n=>n.type==="textbox"))addNode(slide,node);
  }

'''+code[end:]
    code=code.replace('slides: 1','slides: DIAGRAMS.length')
    return code

def portable_input():
    old=json.loads((CASE/'input/diagram-map.json').read_text(encoding='utf-8'))
    if old[0]['NODES'][0].get('box'):return old
    data=[]
    for page in old:
        nodes=[]
        for n in page['NODES']:
            if n['type']=='polygon':raise RuntimeError('Portable phase-one rejects custom polygons; use explicit standard native region geometry.')
            x1,y1,x2,y2=n['bounds']
            nodes.append(dict(id=n['id'],type='textbox' if n['type']=='text' else n['type'],text=n['text'],box={'x':x1,'y':y1,'w':x2-x1,'h':y2-y1},fill=n.get('fill','#EEE5D4').lstrip('#'),fontFace=n.get('font','Zen Kaku Gothic New'),fontSize=n.get('size',28)*.75,color=n.get('color','#12384C').lstrip('#'),bold=n.get('bold',False)))
        edges=[{**e,'points':[{'x':p[0],'y':p[1]} for p in e['points']],'color':e['color'].lstrip('#')} for e in page['EDGES']]
        data.append(dict(title=page['title'],bg=page['bg'].lstrip('#'),NODES=nodes,EDGES=edges,INSETS=[]))
    return data

def package(folder,name):
    files=[]
    for base,dirs,names in os.walk(folder,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'node_modules','__pycache__','.build','cache'}]
        for filename in names:
            if filename=='SOURCE.json' or filename.endswith(('.pyc','.inspect.ndjson')):continue
            if filename in {'migrate_portable.py','portable_kit_builder.py'}:continue
            files.append(Path(base)/filename)
    dump(folder/'SOURCE.json',dict(repository='HututuWorks/sci-diagram-pptx',commit=COMMIT,license='Apache-2.0',modified=True,case_studies=['sci-diagram-showcase'],runtime='PptxGenJS 4.0.1 (MIT)',files=[{'path':f.relative_to(folder).as_posix(),'sha256':sha(f)} for f in sorted(files)]))
    target=ROOT/'downloads'/f'{name}.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files+[folder/'SOURCE.json']):z.write(f,Path(name)/f.relative_to(folder))
    print(f'{name}.zip: {target.stat().st_size} bytes, SHA256 {sha(target)}')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--render',action='store_true');parser.add_argument('--package-only',action='store_true');parser.add_argument('--overwrite',action='store_true');args=parser.parse_args()
    data=portable_input()
    if not args.package_only:
        dump(CASE/'source/input.json',data);dump(CASE/'input/diagram-map.json',data)
        write(CASE/'source/build.mjs',template_build())
        result=subprocess.run([NODE,str(CASE/'source/build.mjs')]+(['--overwrite'] if args.overwrite else []),capture_output=True,text=True,encoding='utf-8',errors='replace')
        write(CASE/'source/build.log',result.stdout+result.stderr)
        if result.returncode:raise RuntimeError(result.stdout+result.stderr)
        shutil.copy2(CASE/'source/deck.pptx',CASE/'deck.pptx')
        if args.render:subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'tools/render_powerpoint.ps1'),'-PresentationPath',str(CASE/'deck.pptx'),'-OutputDirectory',str(CASE/'render')],check=True)
        dump(CASE/'QA.json',dict(status='light_check_complete',runtime='pptxgenjs',runtime_version='4.0.1',slide_count=5,public_portable_generation_success=True,powerpoint_render_count=1 if args.render else 0,main_slide_visual_check='pending',all_page_detailed_review=False,independent_review=False,structure_audit=False,zip_replay=False,history='Earlier proprietary-host internal trial and its QA were preserved under .build/sci-diagram-internal-trial-20261014; they are not the distributed version.'))
    sources=json.loads((CASE/'input/science-sources.json').read_text(encoding='utf-8'))
    dump(CASE/'PROVENANCE.json',dict(repository='HututuWorks/sci-diagram-pptx',upstream_commit=COMMIT,license='Apache-2.0',runtime='PptxGenJS 4.0.1 (MIT)',read_files=['skills/sci-diagram-pptx/SKILL.md','skills/sci-diagram-pptx/references/reconstruction.md','skills/sci-diagram-pptx/references/runtime-pptxgenjs.md','skills/sci-diagram-pptx/assets/pptxgenjs-build-template.mjs','skills/sci-diagram-pptx/scripts/probe_runtime.mjs'],applied_rules={'official_template':'source/build.mjs adapts original pptxgenjs-build-template.mjs directly, retaining validation, one source-to-slide transform, and connectExactPath/connectOneWay/connectBothWays helpers.','ownership':'Every plate, label and relation is native; INSETS empty. No bitmap background or tracing layer.','topology':'NODES/EDGES/INSETS per page; from/to/direction and explicit path; final segment endArrowType targets destination.','native_geometry':'Standard editable rectangles, ellipses, textboxes and exact native line-arrow paths. No freeform path clouds.','z_order':'Earth/water region plates first -> exact path relations -> standard textboxes; prevents filled scientific regions hiding arrows.'},changes='Original single-image reconstruction explicitly extended to five new Japanese concept diagrams. Concept labels and scientific relationships retained. Final terrain simplified to standard rectangular region plates with a river-channel notch, under original portable phase-one geometry limits; not a calibrated landscape section. Source map is adjacent input.json. Locked dependency manifest included for a normal Node installation.',runtime_probe='Original probe passed with bundled Python3.12 ahead of LibreOffice3.8 Python on local PATH and LibreOffice24.2.5.2 executable available. PptxGenJS4.0.1 resolves from the source task directory.',science_sources=sources,commands=['node source/build.mjs','pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath source/deck.pptx -OutputDirectory render'],pptx_sha256=sha(CASE/'deck.pptx'),history='Prior host-specific internal trial lives only under .build/sci-diagram-internal-trial-20261014. It is not the published runtime or source kit.'))
    skill='''---
name: sci-diagram-ja
description: 原典SciDiagramの公式portable templateで科学の関係を日本語のnative図形・矢印としてPPTX化する。
---

# 日本語の科学概念図

1. 一次資料で概念を確認。量を示すデータがない図は「縮尺のない概念モデル」と明記する。
2. upstream/SKILL.md、references/reconstruction.md、runtime-pptxgenjs.mdを読む。SCI_DIAGRAM_RUNTIME=pptxgenjsを選ぶ。全要素のnative/raster所有と矢印方向を先に決める。
3. source/input.jsonのNODES/EDGES/INSETSを編集。EDGESのfrom/to/directionとpointsが関係を定義する。INSETSはこの例では空。配置から関係を推測しない。
4. Node20+を用意。source/で `npm ci --ignore-scripts --no-audit --no-fund`。公式templateが要求するPptxGenJS4.0.1をpin済み。Zen Kaku Gothic NewとSpace Groteskをfonts/の公式TTFから導入。
5. 展開先で `node source/build.mjs`。出力はsource/deck.pptx。意図的な再生成だけ`--overwrite`を指定する。
6. Windows PowerPointで開いて主ページを確認。PNG/PDFはsource/render_powerpoint.ps1、または原典upstream/scripts/render_pptx.pyとLibreOffice/pdftoppmを使う。実施範囲だけ記録。

原典の単図再構成を新規概念図5枚へ明示拡張した例。SKILL本文だけでは生成できず、同梱build.mjs・input.json・MITのPptxGenJSが必要。原典Apache-2.0、commit cc8f0030edf80eeab6e52849b8c39fe638466776。原作者の公式日本語版ではありません。
'''
    readme='''# 雨が、地下水になるまで。

USGSの一次解説に基づく、日本語5ページの科学概念図。縮尺・定量値・実験結果は示しません。

## 原典方式

HututuWorks/sci-diagram-pptxの公式`assets/pptxgenjs-build-template.mjs`を直接使ったPptxGenJS4.0.1経路です。原典のsource-to-slide座標変換、NODES/EDGES/INSETS、native所有、map検証、connectExactPath/connectOneWay/connectBothWaysを保持しています。意味を持つ断面、砂粒、注釈、矢印は全てnativeで編集可能です。

ユーザー指定の新作に合わせ、単一画像の忠実再構成から新規概念図5枚へ拡張。地表の模式形状は標準長方形と河道の切り欠きで表現し、地形の実測を意味しません。科学的関係と矢印の方向はinput.jsonに明示しています。地層のnative plateを先に描き、線・矢印、文字の順に重ねます。

## 再制作

Node.js20+を用意。ZIP展開先で実行します。PptxGenJSはMIT、4.0.1をpackage-lock.jsonに固定。ホスト専用・専有runtimeは不要です。

```powershell
cd source
npm ci --ignore-scripts --no-audit --no-fund
node build.mjs
# 既存の生成物を意図的に置き換える場合だけ
node build.mjs --overwrite
```

実際の入力はsource/input.json、実行コードはsource/build.mjs。出力はsource/deck.pptx。rootのdeck.pptxは完成例、render/は公開プレビューです。Windows Microsoft PowerPointで描画する場合:

```powershell
pwsh -NoProfile -File source/render_powerpoint.ps1 -PresentationPath source/deck.pptx -OutputDirectory render-new
```

原典のportable rendererを使う場合はPython3.10+、LibreOffice/soffice、pdftoppmを用意し、upstream/scripts/render_pptx.pyへ`--soffice`で実exeを渡します。LibreOffice付属の古いPythonがPATHで先にならないよう注意します。

## 書体と条件

fonts/のZen Kaku Gothic NewとSpace GroteskをTTFからインストールし、PowerPointを開き直します。前者は和文、後者は英数字。受け手にも導入してください。Google Fonts公式未改変TTFとOFLを同梱。WindowsFontsからの抽出はありません。PPTXに書体自体は埋め込んでいません。

原典Apache-2.0のLICENSEと、PptxGenJSの原文MIT条件をdependencies/pptxgenjs/LICENSEに保持。原典取得物にNOTICEはありません。原作者の公式日本語版ではありません。専有runtimeのコード・条件ファイルは配布版に含めません。

## 出典・確認

- https://water.usgs.gov/ogw/unsaturated.html
- https://water.usgs.gov/outreach/Posters/groundwater/middle_school/Page2.html

図は新規制作し、USGS画像のコピーは含みません。公開portable版は生成後のPowerPoint描画1回と主ページ確認のみ。全ページ詳細目視、構造監査、独立レビュー、ZIP再実行は未実施。古いホスト専用試用物とQAは内部履歴に退避済みで、現行版の確認結果には数えません。
'''
    for folder in [CASE,FORK]:
        write(folder/'SKILL.md',skill);write(folder/'README.md',readme)
        shutil.copy2(UP/'LICENSE',folder/'LICENSE')
        # Only original portable route documentation and implementation.
        for src in ['SKILL.md','LICENSE','references/reconstruction.md','references/runtime-pptxgenjs.md','assets/pptxgenjs-build-template.mjs','scripts/probe_runtime.mjs','scripts/render_pptx.py','scripts/check_pptx.py']:
            dst=folder/'upstream'/src;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SKILL/src,dst)
        for name in ['build.mjs','input.json']:shutil.copy2(CASE/'source'/name,folder/'source'/name) if folder!=CASE else None
        shutil.copy2(ROOT/'tools/render_powerpoint.ps1',folder/'source/render_powerpoint.ps1')
        shutil.copy2(UP/'package.json',folder/'source/package.json');shutil.copy2(UP/'package-lock.json',folder/'source/package-lock.json')
        dep=folder/'dependencies/pptxgenjs';dep.mkdir(parents=True,exist_ok=True);shutil.copy2(PKG/'LICENSE',dep/'LICENSE')
        for family in ['zenkakugothicnew','spacegrotesk']:shutil.copytree(ROOT/'downloads/fonts'/family,folder/'fonts'/family,dirs_exist_ok=True)
    # Refresh maintained fragments without touching shared catalogs.
    fragment=ROOT/'data/sol-sci-diagram-repository-examples.json'
    records=json.loads(fragment.read_text(encoding='utf-8-sig'))
    records[0]['method']='原典公式PptxGenJS portable templateを直接拡張。NODES/EDGES/INSETSとnative矢印・断面図による5枚の新規科学概念図。'
    records[0]['runtime']='PptxGenJS 4.0.1 (MIT)';records[0]['titles']=[d['title'] for d in data]
    dump(fragment,records)
    guides_path=ROOT/'data/sol-sci-diagram-repository-guides.json'
    guides=json.loads(guides_path.read_text(encoding='utf-8-sig'))
    guides[0]['requirements']=['Node.js20+ / PptxGenJS4.0.1 (MIT)','書体: Zen Kaku Gothic New / Space Grotesk','描画: Windows Microsoft PowerPoint、またはLibreOffice/pdftoppm/Python3.10+']
    guides[0]['commands']=['cd source','npm ci --ignore-scripts --no-audit --no-fund','node build.mjs']
    guides[0]['limitations']=['新規概念図5枚への明示拡張。画像の忠実再構成ではない','全ページ詳細検査、構造監査、ZIP再実行は未実施']
    dump(guides_path,guides)
    for folder,name in [(CASE,'sci-diagram-example-ja'),(FORK,'sci-diagram-ja')]:package(folder,name)
    print('Official portable-template generation/package complete.')

if __name__=='__main__':main()
