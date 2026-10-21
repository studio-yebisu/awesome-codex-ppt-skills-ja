"""Synchronize inspected SlideSpeak engine output, reusable input and evidence."""
from pathlib import Path
import hashlib,json,shutil,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/slidespeak-showcase'
FORK=ROOT/'skill-forks/slidespeak-ja'
UP=ROOT/'.build/actual-upstreams/SlideSpeak__slide-design-skill'
SKIP={'.private','.git','.venv','node_modules','__pycache__','cache'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def package():
    for p in CASE.rglob('*'):
        if p.is_file() and not set(p.relative_to(CASE).parts)&SKIP and p.suffix not in {'.pyc','.log'} and '.occ-measure' not in p.name:
            d=FORK/'example'/p.relative_to(CASE);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
    source=json.loads((FORK/'SOURCE.json').read_text(encoding='utf-8'))
    source['files']=[dict(path=p.relative_to(FORK).as_posix(),sha256=sha(p)) for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json' and not set(p.relative_to(FORK).parts)&SKIP and p.suffix not in {'.pyc','.log'} and '.occ-measure' not in p.name]
    dump(FORK/'SOURCE.json',source)
    for folder,name in [(CASE,'slidespeak-example-ja'),(FORK,'slidespeak-ja')]:
        with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(folder.rglob('*')):
                if p.is_file() and not set(p.relative_to(folder).parts)&SKIP and p.suffix not in {'.pyc','.log'} and '.occ-measure' not in p.name:z.write(p,(Path(name)/p.relative_to(folder)).as_posix())
def main():
    images=[CASE/f'render/effect-page-{n:02}-after.jpg' for n in range(1,7)]
    assert all(p.is_file() for p in images)
    for n,p in enumerate(images,1):
        with Image.open(p) as im:im.save(CASE/f'render/slide-{n:02}.png')
    refs=['SKILL.md','docs/INTEGRATION.md','docs/SKILL-FORMAT.md','engine/index.ts','engine/renderer.ts','engine/skill-loader.ts','engine/occupancy.ts','engine/richness.ts','scripts/validate-skill.ts','scripts/measure-occupancy.mts','LICENSE']
    identities=[dict(path=p,sha256=sha(UP/p),case_sha256=sha(CASE/'upstream'/p)) for p in refs]
    assert all(r['sha256']==r['case_sha256'] for r in identities)
    dump(CASE/'source/original-source-check.json',identities)
    qa={'status':'all6_visual_and_original_gates_checked','repair_author':'Codex','all_page_visual_review':True,'visual_scope':'All6 pages at1280x720. Page3/5/6 line breaks repaired and rechecked; page4 body and rules aligned.','visual_proofs':[dict(index=n,image=p.relative_to(CASE).as_posix(),sha256=sha(p)) for n,p in enumerate(images,1)],'style_gate':'Original validate-skill:1/1 style,6types/3rules/6components passes.','dom_gate':'Original occupancy/legibility6/6 and richness4/4 content slides pass after these repairs.','dom_gate_receipt':'source/original-dom-gates.json','source_integrity':'source/original-source-check.json','engine_result':'engine-result.json','soft_notice':'Near-monochrome palette warning remains; green fields and paper surfaces are intentional.','execution_scope':'Original engine with persisted author-written slide-tree LLMClient. No external LLM/FAL/image calls.','independent_review':False,'independent_recheck':'pending','not_performed':['Live external LLMClient generation','AI/stock imagery','Native PPTX export','Independent repaired-candidate review','Formal adoption']}
    if (CASE/'source/zip-replay.json').exists():qa['distribution_replay']='source/zip-replay.json'
    dump(CASE/'QA.json',qa)
    prov=json.loads((CASE/'PROVENANCE.json').read_text(encoding='utf-8'))
    prov['repair_20261015']={'author':'Codex','changes':['Match upper/lower rule widths.','Use semantic line breaks for quotation, process explanations and closing.','Keep only the external player page count.'],'original_engine_unchanged':True,'original_dom_gate_rerun':'source/original-dom-gates.json','independent_recheck':'pending'}
    dump(CASE/'PROVENANCE.json',prov)
    text=(CASE/'README.md').read_text(encoding='utf-8')
    text=text.split('\n## 2026-10-15 修復と確認')[0]
    text+='''
## 2026-10-15 修復と確認

引用・工程・結びの文章を意味単位で改行し、上下の罫線幅を統一。全6頁を1280×720で確認した。原典style検査1/1、occupancy/legibility6/6、richness4/4を現HTMLで再実行し通過。元engineのhashはsource/original-source-check.jsonへ記録。Windowsの実行パス/file URLだけをadapterへ分け、採点関数は変更していない。

ブリーフから、この作例専用の6ファイルstyleとslide-treeを作者が用意し、原典APIへ渡した。外部LLMへ原稿生成を依頼する部分、AI/stock画像、編集可能PPTXは実行していない。独立再評価は未了。ZIP再実行の結果はQA.jsonを参照。
'''
    (CASE/'README.md').write_text(text,encoding='utf-8')
    skill=(FORK/'SKILL.md').read_text(encoding='utf-8').replace('# 日本語の編集誌スライド','# ブリーフから独自デザインを作る')
    skill=skill.replace('技能本文だけではengineを含みません。一式ZIPのupstream sourceと作品ZIPのstyle/入力/build.mtsを使用。','同梱 `example/` のstyle/入力/build.mtsと原典engineを使う。今回のslide-treeは作者が用意してLLMClientへ渡したもの。ライブLLM呼出しの実行例とは区別する。自分の資料ではbriefとstyleを作り直し、原典gate・全ページ確認を行う。')
    (FORK/'SKILL.md').write_text(skill,encoding='utf-8');shutil.copy2(FORK/'SKILL.md',CASE/'SKILL.md')
    f=ROOT/'data/sol-slidespeak-repository-examples.json';cases=json.loads(f.read_text(encoding='utf-8'));c=cases[0];rel=lambda p:p.relative_to(ROOT).as_posix()
    c.update(pages=[rel(CASE/f'render/slide-{n:02}.png') for n in range(1,7)],interior=rel(CASE/'render/slide-04.png'),preview_image_count=6,preview_image_notice='全6頁を実ブラウザーで確認。修復後の独立再評価は未了。',status='all_pages_visual_checked',execution_status='original_engine_all_pages_and_gates_checked')
    dump(f,cases)
    limits=['主出力は1920×1080のHTML。編集可能PPTXの出力例ではない。','原典engineへ、作者が用意したslide-treeをLLMClientで渡した。ライブLLMの生成は未実行。','FAL/AI画像/stock画像は未使用。コード図形だけで制作した。','全6頁と原典検査を確認。独立再評価は修復後に実施予定。']
    steps=['題材・聴衆・内容と、色/ブランド/参考画像など見た目の手掛かりを渡す。','briefからtokens/chrome/components/layout grammar/image-style/SKILLの6ファイルを設計する。','原典loadSkill/generateDeck/rendererを使い、原典のstyle・内容・見た目の検査を通す。','全頁を実表示し、文字・改行・図・空白・移動を確認して直す。']
    patch={'case_id':'slidespeak-showcase','name':'ブリーフから独自デザインのHTMLを作る','job':'','upstream_principle':'内容と見た目のブリーフから専用のtokens・レイアウト・固定テンプレートを設計し、ホストLLMが本文を埋め、原典engineが1920×1080のHTMLへ変換・検査する。','change':'題材と見た目の条件から、その資料専用の書体・配色・レイアウトを持つHTMLへ組む。','input':'題材・原稿・聴衆と、見た目の説明・ブランドURL・参考画像などの手掛かり','output':'専用styleの6ファイル、slide-treeと1920×1080 HTML','how_to_use':steps,'constraints':limits,'demonstration':{'summary':'書店の仮ブリーフから専用6ファイルstyleを作り、保存したslide-treeを原典engineでHTML化。全6頁を確認し、原典style/occupancy/legibility/richness検査を通した。','applied_features':['brief由来の専用tokens・6種のテンプレート','原典loadSkill/generateDeck/renderer','原典のstyleと実DOM品質検査'],'not_demonstrated':['ライブLLMによるslide-tree生成','AI/stock画像','編集可能PPTX','修復後の独立再評価'],'pages':[dict(index=1,label='2ページ目',title='探していた本と、まだ知らない自分に。',skill_rule='題材に合わせた固定テンプレートで、本文をslotsへ入れる。',what_to_inspect='statementテンプレートの大きな見出しと本文。slide-treeのtitle/bodyが専用の配置へ入る。',proof_path=rel(images[1]),proof_kind='render-image'),dict(index=3,label='4ページ目',title='緑は、街の目印。',skill_rule='専用styleの色・書体・余白を、複数レイアウトへ通す。',what_to_inspect='生成り/緑、和文見出し、上下の長い罫線を共通化し、本文と開いた本の図を左右へ分ける。',proof_path=rel(images[3]),proof_kind='render-image'),dict(index=4,label='5ページ目',title='言葉から、店先まで。',skill_rule='layout grammarに沿う工程テンプレートへ本文を割り当て、実DOMを検査する。',what_to_inspect='3工程の順序・番号・説明を見る。文章を意味単位で改行し、原典検査と実表示の両方で確認した。',proof_path=rel(images[4]),proof_kind='render-image')],'source_proof_paths':[rel(CASE/'input/slide-tree.json'),rel(CASE/'build.mts'),rel(CASE/'styles/green-book-editorial/layout-grammar.md'),rel(CASE/'source/original-dom-gates.json'),rel(CASE/'source/original-source-check.json'),rel(CASE/'QA.json')]},'guide_patch':{'summary_ja':'内容と見た目のbriefから専用のデザインを設計し、原典engineでHTMLへ変換・検査する。','requirements':['Node20+とnpm依存','原典engineと6ファイルstyle','新規制作時はホストLLM。画像APIは任意。'],'steps':steps,'limitations':limits,'production_status':'original_engine_all6_visual_and_gates_complete_independent_pending'}}
    f=ROOT/'data/skill-effect-patches/repairs-web67.json';patches=json.loads(f.read_text(encoding='utf-8'));dump(f,[x for x in patches if x['case_id']!=patch['case_id']]+[patch])
    package();print('SlideSpeak:6 images, original source/gates and2 ZIPs synchronized.')
if __name__=='__main__':main()
