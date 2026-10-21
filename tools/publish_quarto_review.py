"""Publish the existing Quarto render and the six browser-inspected pages."""
from pathlib import Path
import difflib, hashlib, json, shutil, zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/quarto-talks-showcase'
FORK = ROOT / 'skill-forks/quarto-talks-ja'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    images = [CASE / f'render/effect-page-{n:02}-after.jpg' for n in range(1,7)]
    assert all(p.is_file() for p in images)
    assert 'Output created: index.html' in (CASE/'output/quarto-render.log').read_text(encoding='utf-8')
    normalized=[]
    for n in range(1,7):
        # Lossless format normalization of the browser capture; no pixel edits.
        with Image.open(images[n-1]) as image:
            output=CASE/f'render/slide-{n:02}.png'
            image.save(output)
            if n<=2:image.save(CASE/f'render/major-{n:02}.png')
            normalized.append({'page':n,'source':images[n-1].relative_to(CASE).as_posix(),'source_sha256':hashlib.sha256(images[n-1].read_bytes()).hexdigest(),'png':output.relative_to(CASE).as_posix(),'png_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'pixel_edits':False})
    dump(CASE/'source/canonical-preview-images.json',normalized)
    qa = load(CASE/'QA.json')
    qa.update(status='original_render_and_all6_visual_check_complete')
    qa['checks'].update(all6_visual='All six pages inspected in the browser at 1280x720; original Reveal scales the 1600x900 canvas.',
        native_navigation='ArrowRight through six pages and Home back to page1; correct page counter and notes observed.',
        code_frame_repair='Local SCSS aligns sourceCode background and pre/code widths; no original extension/runtime changes.')
    qa['not_performed']=['independent re-review after repair','PowerPoint export']
    qa['display_proof']['purpose']='All six pages after neutral-title/context-size/layout repair; actual 1280x720 browser screenshots captured after CSS animations settled.'
    qa['display_proof']['pages']=[dict(index=n, image=p.relative_to(CASE).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for n,p in enumerate(images,1)]
    qa['current_calculation']=load(CASE/'output/results.json')
    qa['independent_review']='pending_after_repair'
    if (CASE/'source/zip-replay.json').is_file():
        replay=load(CASE/'source/zip-replay.json')
        qa['checks']['zip_replay']=f"Extracted example ZIP: Python calculation and original Quarto render exit0; NumPy {replay['numpy_version']}, Matplotlib {replay['matplotlib_version']}. Existing dependencies; extracted rebuild not visually reinspected."
    dump(CASE/'QA.json',qa)
    prov=load(CASE/'PROVENANCE.json')
    prov['local_changes']=list(dict.fromkeys([*prov['local_changes'],'Local code frame/background width alignment in source/japanese.scss']))
    prov['repair_author']='Codex'
    prov['repair_scope']='Neutral explanatory titles, larger context, opening columns, plot/limit separation, actual recalculation and all6 settled browser views; original extension/runtime unchanged.'
    prov['current_calculation_environment']={k:qa['current_calculation'][k] for k in ('numpy_version','matplotlib_version')}
    dump(CASE/'PROVENANCE.json',prov)
    text=(FORK/'SKILL.md').read_text(encoding='utf-8')
    begin=text.index('6. この派生では') if '6. この派生では' in text else text.index('6. 原典Step6に従い')
    end=text.index('\n\n## MDだけ', begin)
    text=text[:begin]+'''6. 原典Step6に従い、完成HTMLの全ページを通常の発表画面で確認する。文字・数式・コード・引用・図の欠け、はみ出し、投影時の大きさ、白青の配色と字体役割、説明順を確認し、問題を直して再renderする。

## この6枚の作例で変更した範囲

作例の5分・6枚指定を優先し、原典の16〜24枚既定を短縮した。数値は合成5点から実計算し、コード表示と計算実行を区別した。コード枠の幅を局所SCSSで補正し、原典拡張は変更していない。全6頁とページ移動を実表示で確認した。独立再評価は別途行う。''' +text[end:]
    (FORK/'SKILL.md').write_text(text,encoding='utf-8')
    readme=(CASE/'README.md').read_text(encoding='utf-8')
    begin=readme.index('実計算、Quarto render exit0')
    end=readme.index('\n\n原文条件',begin)
    readme=readme[:begin]+'''実計算、Quarto render exit0、全6頁のブラウザー表示と次頁・先頭への移動を確認した。コードの背景幅はsource/japanese.scssだけで修正した。render/effect-page-01-after.jpg〜06-after.jpgが現在の実画面。独立再評価は未了。Quarto1.9.38のSCSS色変数書き出し警告は残るが、CSSとHTMLの生成はexit0で完了し、全頁の白・青・字体を確認した。元拡張SCSSとReveal runtimeは変更していない。''' +readme[end:]
    (CASE/'README.md').write_text(readme,encoding='utf-8')
    source=load(FORK/'SOURCE.json')
    source['verification_override']='Six-slide example; original all-slide render/inspection requirement retained. Current all6 visual check complete; independent re-review pending.'
    source['local_difference']='LOCAL-DIFF.txt; Japanese workflow; code-frame width in example source/japanese.scss'
    dump(FORK/'SOURCE.json',source)
    shutil.copy2(CASE/'source/local.diff',FORK/'LOCAL-DIFF.txt')
    with (FORK/'LOCAL-DIFF.txt').open('a',encoding='utf-8') as handle:
        handle.write('\n# 2026-10-15: example source/japanese.scss aligns div.sourceCode and pre/code widths. Original extension SCSS unchanged.\n')
    source['files']=[dict(path=p.relative_to(FORK).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json' and '__pycache__' not in p.parts]
    dump(FORK/'SOURCE.json',source)
    for folder,filename in [(CASE,'quarto-talks-example-ja.zip'),(FORK,'quarto-talks-ja.zip')]:
        with zipfile.ZipFile(ROOT/'downloads'/filename,'w',zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(folder.rglob('*')):
                if path.is_file() and not set(path.relative_to(folder).parts)&{'.private','.quarto','__pycache__','.git','.venv'} and path.suffix!='.pyc' and path.name!='_quarto_internal_scss_error.scss':
                    archive.write(path,folder.name+'/'+path.relative_to(folder).as_posix())
    print('Quarto: six visual proofs, current guides, and two ZIPs published locally.')

if __name__=='__main__':
    main()
