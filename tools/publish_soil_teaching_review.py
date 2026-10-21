"""Publish the checked teaching plan, reveal behavior and print repair."""
from pathlib import Path
import hashlib,json,subprocess,importlib.util
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/soil-teaching-showcase'
FORK=ROOT/'skill-forks/soil-teaching-ja'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    images=[CASE/f'render/slide-{n:02}.png' for n in range(1,7)];assert all(p.is_file() for p in images)
    checks=json.loads((CASE/'source/browser-checks.json').read_text(encoding='utf-8'))
    assert len(checks['captures'])==12 and all(c['active']==1 and c['revealed']==c['expected_fragments'] for c in checks['captures'])
    validator=CASE/'upstream/scripts/validate_html_deck.mjs'
    p=subprocess.run(['node',str(validator),str(CASE)],capture_output=True,text=True,encoding='utf-8');assert p.returncode==0
    dump(CASE/'source/original-validation.json',dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,validator_sha256=sha(validator),deck_sha256=sha(CASE/'index.html')))
    checks['print_pdf_pages']=6;checks['print_repair']='Original trailing break-after:page yielded a blank7th page. Local last-child break-after:auto removes it. Browser PDF now6pages; page2 rendered and viewed.'
    dump(CASE/'source/browser-checks.json',checks)
    qa={'status':'all6_visual_original_validator_and_reveal_print_checked','repair_author':'Codex','original_validator':'source/original-validation.json','original_validator_result':'VALIDATION_OK; document-language zh-Hant-TW warning retained for this Japanese adaptation.','browser_checks':'source/browser-checks.json','visual_scope':'All6 pages at1600x900 viewed. All6 captured with correct page/reveal state at1280x720 and1920x1080; repaired page2/6 additionally viewed at those sizes.','images':[dict(index=n,path=p.relative_to(CASE).as_posix(),sha256=sha(p)) for n,p in enumerate(images,1)],'checks':['Unique per-page teaching points/labels/core takeaways recorded.','Cover has10 actual sectors with3red.','Comparison arrays have equal square size/top alignment; formulas include0.3/0.15.','Page6 conclusion clear of divider.','ArrowRight/Space reveal same-page steps; ArrowLeft removes a step; Home/End and6hash routes work.','Print forces all19fragments visible and produces6PDFpages.'],'independent_review':False,'independent_recheck':'pending','not_performed':['Mode A image-first PPTX','Mode B editable PPTX','Classroom learning-effect study','Physical printer compatibility','Independent repaired-candidate review','Formal adoption']}
    if (CASE/'source/zip-replay.json').exists():qa['distribution_replay']='source/zip-replay.json'
    dump(CASE/'QA.json',qa)
    prov=json.loads((CASE/'PROVENANCE.json').read_text(encoding='utf-8'))
    prov['repair_20261015']={'author':'Codex','changes':['Make required_labels/teaching_point/core_takeaway specific to each page.','Draw10sectors in opening diagram; keep3red.','Add decimal step and space around comparison formulas.','Align equal-size tiles and fix page6 paragraph margins.','Remove trailing blank printed page with local CSS.'],'checks':'source/browser-checks.json','independent_recheck':'pending'}
    dump(CASE/'PROVENANCE.json',prov)
    readme=CASE/'README.md';s=readme.read_text(encoding='utf-8');start=s.index('生成成功と主要完成画面の初回表示を軽く確認します。') if '生成成功と主要完成画面の初回表示を軽く確認します。' in s else s.index('原典validate_html_deck.mjsはVALIDATION_OK')
    s=s[:start]+'''原典validate_html_deck.mjsはVALIDATION_OK。日本語版のため原典のzh-Hant-TW警告は保持。全6頁を1600×900で見て、1280×720と1920×1080でも全頁の対象・段階数・固定比率を確認した。2頁の式と6頁の結論の余白を修復。矢印/Space、戻る、Home/End、全hashを実操作した。

印刷は全19段階が表示され、6ページのPDFになることを確認。原典の末尾改ページで出た空白7ページ目は、最後のslideだけbreak-after:autoを指定して除いた。紙プリンターでの確認、授業での理解度、Mode A/B、修復後の独立再評価は未実施。記録はQA.jsonとsource/browser-checks.json。
'''
    readme.write_text(s,encoding='utf-8')
    steps=['教材から、各頁の教える一点・学習者の作業・図の関係・短いラベル・結論を計画する。','計画と出力Modeを確認する。HTMLを選ぶ場合は見た目も決め、原典Mode Cテンプレートへ内容を入れる。','根拠から答えへ段階表示する。図の個数・区画・式が説明と一致するように作る。','原典validatorを実行し、全頁の大小画面、段階移動、hash、印刷の全段表示を確認して直す。']
    limits=['原典は画像中心PPTX・編集可能PPTX・オフラインHTMLの3Mode。本作例はHTMLのみ。','画像版と編集PPTXはそれぞれ専用の制作環境が必要。このHTMLはブラウザーと同梱ファイルだけで開く。','SOIL方法説明・原典/派生SKILLはCC BY-NC-SA4.0。softwareはMIT、書体はOFL。','学習効果と紙プリンター互換性、Mode A/B、修復後の独立再評価は未確認。']
    rel=lambda p:p.relative_to(ROOT).as_posix()
    patch={'case_id':'soil-teaching-showcase','name':'教材を「考える順序」のスライドへ整理する','job':'','upstream_principle':'教材を、各頁の教える一点・学習者の作業・認知的役割・図・結論へ計画し、画像中心PPTX・編集可能PPTX・オフラインHTMLのいずれかに仕上げる。','change':'教材を、学習者が何に注目し、何を比べ、どんな結論へ進むかが分かるページへ分ける。','input':'教材・対象学年・教える一点・学習者の作業・必要な図や数値・出力Mode','output':'確認用のページ計画と選んだModeの教材。今回の作例は段階表示HTML。','how_to_use':steps,'constraints':limits,'demonstration':{'summary':'頁ごとの学習目標・比較/量/応用/練習の役割を計画し、原典Mode Cで6頁のHTMLにした。比較では図を先に見せ、式、結論の順に表示。原典validator、全頁表示、段階操作、全段印刷を確認した。','applied_features':['頁ごとのteaching point/learner task/role/labels/takeaway','原典Mode Cのsemantic sectionと図解','原典fragment/controllerによる根拠→答え→結論'],'not_demonstrated':['Mode A画像版・Mode B編集PPTX','授業での理解度改善','紙プリンターでの確認','修復後の独立再評価'],'pages':[dict(index=1,label='2ページ目',title='同じ6個でも、割合は変わる',skill_rule='比較する対象を先に見せ、根拠となる式と結論を後から表示する。',what_to_inspect='赤は双方6個、全体は20個/40個。同じ大きさのマスで比べ、式→結論を「進む」で順に示す。',proof_path=rel(images[1]),proof_kind='render-image'),dict(index=3,label='4ページ目',title='60個の30%は、18個',skill_rule='量を求める順序に合わせて、図と計算を分ける。',what_to_inspect='10%を一つ分6個としてから、三つ分18個へ進む。10等分の帯の3区画と計算が対応する。',proof_path=rel(images[3]),proof_kind='render-image'),dict(index=5,label='6ページ目',title='8個は、32個の何%？',skill_rule='練習頁では作業を先に提示し、答えと判断を後から示す。',what_to_inspect='32個のうち赤8個を見て式を考える。段階表示後に8÷32=0.25と25%、割合の定義を表示する。',proof_path=rel(images[5]),proof_kind='render-image')],'source_proof_paths':[rel(CASE/'input/PLAN.json'),rel(CASE/'slides.js'),rel(CASE/'source/original-validation.json'),rel(CASE/'source/browser-checks.json'),rel(CASE/'render/step-02-initial.jpg'),rel(CASE/'render/step-02-complete.jpg'),rel(CASE/'QA.json')]},'guide_patch':{'summary_ja':'教材から学習者の作業と図の関係を計画し、選んだModeの教材へ仕上げる。','steps':steps,'requirements':['この作例:モダンブラウザーのみ（offline可）','原典validator:Node.js','画像版/編集PPTXは原典の各Modeの専用環境'],'limitations':limits,'production_status':'mode_c_all6_visual_reveal_validator_print_checked_independent_pending'}}
    p=ROOT/'data/skill-effect-patches/repairs-web67.json';patches=json.loads(p.read_text(encoding='utf-8'));dump(p,[x for x in patches if x['case_id']!=patch['case_id']]+[patch])
    p=ROOT/'data/sol-soil-teaching-repository-examples.json';cases=json.loads(p.read_text(encoding='utf-8'));cases[0].update(pages=[rel(p) for p in images],pdf_download=rel(CASE/'render/deck.pdf'),preview_image_count=6,preview_image_notice='全6頁の全段表示。取得HTMLでは図→式→結論の順に表示する。',execution_status='original_mode_c_all_pages_reveal_and_print_checked');dump(p,cases)
    spec=importlib.util.spec_from_file_location('soil_build',ROOT/'tools/build_soil_teaching_showcase.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.package()
    print('SOIL:page plan,6 actual pages, original validator, reveal/print checks and2ZIPs synchronized.')
if __name__=='__main__':main()
