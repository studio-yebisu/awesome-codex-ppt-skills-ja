"""Publish the actual six-page and text-edit/save checks for Frontend Slides."""
from pathlib import Path
import hashlib, json, shutil, zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/sol-motion-showcase'
FORK=ROOT/'skill-forks/sol-motion-ja'
SKIP={'.private','.git','.venv','node_modules','__pycache__','cache'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def package():
    for path in CASE.rglob('*'):
        if path.is_file() and not set(path.relative_to(CASE).parts)&SKIP and path.suffix!='.pyc':
            target=FORK/'example'/path.relative_to(CASE);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
    source=json.loads((FORK/'SOURCE.json').read_text(encoding='utf-8'))
    source['files']=[dict(path=p.relative_to(FORK).as_posix(),sha256=sha(p)) for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json' and not set(p.relative_to(FORK).parts)&SKIP and p.suffix!='.pyc']
    dump(FORK/'SOURCE.json',source)
    for folder,name in [(CASE,'sol-motion-example-ja'),(FORK,'sol-motion-ja')]:
        with zipfile.ZipFile(ROOT/f'downloads/{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(folder.rglob('*')):
                if p.is_file() and not set(p.relative_to(folder).parts)&SKIP and p.suffix!='.pyc':z.write(p,(Path(name)/p.relative_to(folder)).as_posix())

def main():
    images=[CASE/f'render/effect-page-{n:02}-after.jpg' for n in range(1,7)]
    assert all(p.is_file() for p in images)
    for n,p in enumerate(images,1):
        with Image.open(p) as im:im.save(CASE/f'render/slide-{n:02}.png')
    receipt={'status':'actual_browser_edit_export_reopened','browser':'Codex in-app browser','before':'仕事帰りに出会う、次の一冊。','after':'編集した本文を、HTMLに保存する。','operations':['E enters edit mode','Edit the subtitle as plaintext','ArrowRight within editable text keeps page6','Reload restores text from localStorage','Download edited HTML via the actual save button','Open downloaded HTML at a new URL and observe edited subtitle','Restore the original example text'],
        'original_file':{'path':'index.html','sha256':sha(CASE/'index.html')},'edited_file':{'path':'qa/inline-edited.html','sha256':sha(CASE/'qa/inline-edited.html')},'reopened_image':'render/inline-edit-reopened.jpg','repair_author':'Codex','independent_review':'pending'}
    dump(CASE/'qa/inline-edit.json',receipt)
    qa={'status':'all6_visual_and_inline_edit_checked','build':'passed','repair_author':'Codex','independent_review':False,'independent_recheck':'pending','all_page_visual_review':True,
        'scope':'All6 pages at1280x720; all3 curation tabs; page4 at393x700; E edit, auto-save, actual HTML download and reopen.',
        'visual_proofs':[dict(index=n,image=p.relative_to(CASE).as_posix(),sha256=sha(p)) for n,p in enumerate(images,1)],
        'mobile':{'viewport':[393,700],'page':4,'stage':[393,221.0625],'reflow':False,'horizontal_overflow':0,'image':'render/mobile-stage.png'},
        'inline_edit':'qa/inline-edit.json','source_rebuild':'python source/rebuild.py',
        'not_performed':['Original3-style visual discovery for this already authored example','PPTX conversion','Image-folder selection branch','Independent repaired-candidate review','Formal adoption']}
    if (CASE/'source/zip-replay.json').exists():qa['distribution_replay']='source/zip-replay.json'
    dump(CASE/'QA.json',qa)
    prov=json.loads((CASE/'PROVENANCE.json').read_text(encoding='utf-8'))
    prov['repair_20261015']={'author':'Codex','changes':['Match section numbers to actual pages.','Connect selection tabs to both copy and book highlight.','Implement original default inline editing, localStorage and HTML export.','Separate portable authoring parts and include original style-discovery references.'],'upstream_css_unchanged':True,'text_only_editor':'Case adaptation of the original default affordance; original template gives the control/wiring recipe.','independent_recheck':'pending'}
    dump(CASE/'PROVENANCE.json',prov)
    (CASE/'README.md').write_text('''# Frontend Slidesの日本語作例

原稿を単一HTMLの発表資料へ仕上げるスキル。原典は見た目3案の比較、固定1920×1080 stage、段階表示、本文編集・保存を扱う。PPTXからの変換も別の入口として用意されている。

この見本は架空の図書館企画6ページ。固定stage・段階表示を使い、企画固有の選書タブを追加した。タブで本文と本の強調が切り替わる。配色とSVGはこの作例の制作判断で、原典の既成テンプレートではない。

`index.html` はブラウザーだけで再生する。矢印・Space・PageUp/Down・ホイール・スワイプで移動。Eキーか左上の編集ボタンで本文を直す。変更はこのブラウザーに自動保存され、「編集済みHTMLを保存」で別ファイルへ保存できる。編集は文字単位で、図形や配置の変更はCSS/SVGを使う。編集で長くした文章は全ページを再確認する。

再組立: `python source/rebuild.py`。Python標準ライブラリのみ。`source/slides.html` が原稿、`adaptation.css` が配置と色、`controller.js` が動作。3書体のフルTTF/OFL、原典MIT、原典SKILL・CSS・テンプレート資料を同梱する。新規制作の手順は日本語SKILL.mdを参照。

全6頁を1280×720で、選書3状態とスマートフォン393×700の固定比率も確認した。本文編集→自動保存→実ダウンロード→別URLで再表示を確認し、元の作例本文へ戻した。確認記録はQA.jsonとqa/inline-edit.json。

3案の比較選択、PPTX変換、画像フォルダー評価は今回実行していない。修復後の独立再評価は未了。正式採用と区別する。
''',encoding='utf-8')
    shutil.copy2(FORK/'SKILL.md',CASE/'SKILL.md')
    rel=lambda p:p.relative_to(ROOT).as_posix()
    file=ROOT/'data/sol-motion-repository-examples.json'
    cases=json.loads(file.read_text(encoding='utf-8'));c=cases[0]
    c.update(pages=[rel(CASE/f'render/slide-{n:02}.png') for n in range(1,7)],preview_image_count=6,preview_image_notice='全6頁の実ブラウザー表示。独立再評価は未了。',status='all_pages_visual_checked',execution_status='all_pages_visual_and_inline_edit_checked')
    c['editability_proof']={'before_path':rel(CASE/'render/effect-page-06-after.jpg'),'after_path':rel(CASE/'render/inline-edit-reopened.jpg'),'before_label':'元の本文','after_label':'本文を変えて保存したHTML','artifact_path':rel(CASE/'qa/inline-edited.html'),'artifact_label':'変更したHTMLを取得 ↓','report_path':rel(CASE/'qa/inline-edit.json'),'description':'Eキーで本文を直し、HTMLとして保存。別のファイルを開き直し、変更した本文が残ることを確認した。'}
    dump(file,cases)
    constraints=['出力は単一HTML。PPTXの編集可能化は扱わない。','3案からの選択・PPTX変換・画像フォルダー評価は今回未実行。','選書タブと配色/SVGは本作例の追加設計。原典既成テンプレートではない。','本文の編集・自動保存・HTML保存と再表示を実確認。修復後の独立再評価は未了。']
    steps=['目的・聴衆・素材と発表/配布の密度を決める。','新規作成では3案の実表紙を比較して見た目を選ぶ。PPTX変換では抽出内容を先に確認する。','原典のstage・CSS・controllerと選んだ設計でHTMLを作り、本文編集と保存を付ける。','全頁の本文・図・重なり、大小画面、移動、編集→保存→再表示を確認して直す。']
    patch={'case_id':'sol-motion-showcase','name':'原稿から動き・本文編集つきHTMLを作る','job':'','upstream_principle':'原稿またはPPTXを、見た目の比較から単一HTMLの発表資料へ仕上げる。固定16:9 stage、段階表示、標準の本文編集・保存を備える。','change':'内容と見た目を分けて検討し、ブラウザーで発表・本文編集できる単一HTMLへ組む。','input':'目的・聴衆・枚数・発表/配布の密度・原稿や画像。変換時は元PPTX。','output':'固定16:9の単一HTML、編集用CSS/JS/原稿、書体・帰属・確認記録','how_to_use':steps,'constraints':constraints,
        'demonstration':{'summary':'6頁を固定stageへ組み、段階表示と本文編集を適用。企画固有の選書タブは本文と本の強調を連動。全6頁・3タブを確認し、実際に文字を直してHTML保存・再表示した。','applied_features':['原典viewport-base.css全文と固定1920×1080 stage','段階的な入場表示とキーボード等の移動','原典標準のEキー編集・自動保存・HTML出力'],'not_demonstrated':['新規制作時の3案比較','PPTX変換・画像フォルダー評価','修復後の独立再評価'],
        'pages':[dict(index=2,label='3ページ目',title='予定のない夜にも、入口がある。',skill_rule='固定16:9 stageに情報の順序を置き、段階表示する。',what_to_inspect='一つの見出しの下に3段階を並べる。ブラウザー幅を変えても3列の位置関係は変わらない。',proof_path=rel(images[2]),proof_kind='render-image'),dict(index=3,label='4ページ目',title='今夜の気分は、どの棚に近い？',skill_rule='単一HTMLのJSを、内容に必要な操作へ追加できる。',what_to_inspect='タブを切り替えると説明と本の強調が対応して変わる。この選書タブは作例独自の追加。',proof_path=rel(images[3]),proof_kind='render-image'),dict(index=5,label='6ページ目',title='本文を変え、HTMLで保存する',skill_rule='ロック指定がなければ本文編集と保存を標準で付ける。',what_to_inspect='元のページと保存後の比較を見る。編集した一文が別HTMLを開いても残る。',proof_path=rel(CASE/'render/inline-edit-reopened.jpg'),proof_kind='render-image')],
        'source_proof_paths':[rel(CASE/'source/controller.js'),rel(CASE/'source/viewport-base.css'),rel(CASE/'source/rebuild.py'),rel(CASE/'qa/inline-edit.json'),rel(CASE/'QA.json')]},
        'guide_patch':{'summary_ja':'見た目を比較して選び、本文編集できる単一HTMLの発表資料へ仕上げる。','requirements':['原典SKILLを読める制作エージェント','モダンブラウザー','同梱例の再組立はPython3標準ライブラリ'],'steps':steps,'commands':['python source/rebuild.py'],'limitations':constraints,'production_status':'all6_visual_and_text_edit_save_checked_independent_pending'}}
    patchfile=ROOT/'data/skill-effect-patches/repairs-web67.json'
    patches=json.loads(patchfile.read_text(encoding='utf-8'));patches=[x for x in patches if x['case_id']!=patch['case_id']]+[patch];dump(patchfile,patches)
    package()
    print('Frontend Slides:6 actual pages, inline edit/export/reopen, source parts and two ZIPs synchronized.')

if __name__=='__main__':main()
