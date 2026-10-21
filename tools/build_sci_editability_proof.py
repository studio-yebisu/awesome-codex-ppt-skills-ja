"""Publish an actual saved PowerPoint text edit without changing the reconstruction.

Run the PowerPoint renderer and qa/native_editability.ps1 first. This step only
publishes their existing outputs; it never substitutes a simulated edit image.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/sci-diagram-reconstruction'
FORK = ROOT / 'skill-forks/sci-diagram-reconstruction-ja'


def read(path):
    return json.loads(path.read_text('utf-8-sig'))


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    proof = CASE / 'qa/editability'
    report = read(proof / 'native-editability.json')
    assert report['saved_edit_reopened'] is True
    assert report['picture_count'] == 0
    assert report['original_label'] == '海・湖の水' and report['edited_label'] == '湖の水'
    for name in ['native-label-edited.pptx', 'native-label-edited.pdf', 'native-label-edited.png']:
        assert (proof / name).is_file(), name
    checker_path = CASE / 'qa/check-pass-01.json'
    checker = read(checker_path)
    assert checker['status'] == 'PASS' and not checker['hard_failures']

    def portable(value):
        if isinstance(value, dict):
            return {k: portable(v) for k, v in value.items()}
        if isinstance(value, list):
            return [portable(v) for v in value]
        return value.replace(str(CASE), '.').replace(CASE.as_posix(), '.') if isinstance(value, str) else value

    dump(checker_path, portable(checker))
    render_report = CASE / 'render/powerpoint-render.json'
    data = portable(read(render_report))
    data['preview_pipeline'] = 'PowerPoint PDF export → Poppler pdftoppm PNG, 1600px width'
    data['reason'] = 'Direct PowerPoint PNG export added faint marks under Japanese labels; the PDF and LibreOffice render do not.'
    dump(render_report, data)
    report.update(render_pipeline=data['preview_pipeline'], pptx_sha256=digest(proof / 'native-label-edited.pptx'),
                  image_sha256=digest(proof / 'native-label-edited.png'), original_pptx_sha256=digest(CASE / 'pass-01/editable.pptx'))
    dump(proof / 'native-editability.json', report)
    qa = read(CASE / 'QA.json')
    qa['native_edit_test'] = report
    qa['native_edit_test_report'] = 'qa/editability/native-editability.json'
    qa['render_preview_pipeline'] = data['preview_pipeline']
    qa['agent_visual_inspection']['inspected_files'] += ['qa/editability/native-label-edited.png']
    qa['agent_visual_inspection']['inspected_files'] = list(dict.fromkeys(qa['agent_visual_inspection']['inspected_files']))
    qa['repair_20261015'] = {'scope': 'Preview render and published native text edit proof',
                           'original_reconstruction_changed': False, 'independent_review': 'pending'}
    dump(CASE / 'QA.json', qa)
    provenance = read(CASE / 'PROVENANCE.json')
    assert digest(CASE / 'pass-01/build.mjs') == provenance['build_sha256']
    assert digest(CASE / 'pass-01/editable.pptx') == provenance['pptx_sha256']
    provenance['editability_proof'] = 'qa/editability/native-editability.json'
    provenance['preview_pipeline'] = data['preview_pipeline']
    dump(CASE / 'PROVENANCE.json', provenance)

    base = CASE.relative_to(ROOT).as_posix()
    record = {'before_path': f'{base}/render/slide-01.png',
              'after_path': f'{base}/qa/editability/native-label-edited.png',
              'before_label': '復元したPPTX：「海・湖の水」', 'after_label': '文字を変更したPPTX：「湖の水」',
              'artifact_path': f'{base}/qa/editability/native-label-edited.pptx',
              'report_path': f'{base}/qa/editability/native-editability.json',
              'description': '図全体を画像として貼り直さず、「海・湖の水」の文字だけを「湖の水」へ変更。別のPPTXとして保存し、PowerPointで開き直して確認しました。'}
    fragment_path = ROOT / 'data/sci-reconstruction-fragment.json'
    fragment = read(fragment_path)
    fragment[0]['editability_proof'] = record
    fragment[0]['preview_notice'] = 'PowerPoint出力PDFをPNG化。元のラベルと方向を保持し、文字・図形・矢印を個別編集できます。別コピーで実際の文字編集・保存・再表示を確認済み。'
    dump(fragment_path, fragment)
    marker = '<div class="details"><h2>この作例で確認する効果</h2>'
    block = '<section class="saved-edit"><h2>文字だけを変更して保存する</h2><p>' + record['description'] + '</p><img style="width:100%;max-width:920px;border:1px solid #b7cbd6" src="qa/editability/native-label-edited.png" alt="海・湖の水の文字を湖の水へ変更した実際のPPTX描画"><p><a href="qa/editability/native-label-edited.pptx" download>変更したPPTX</a> · <a href="qa/editability/native-editability.json">保存・再表示の確認記録</a></p></section>'
    html_path = CASE / 'index.html'
    html = html_path.read_text('utf-8')
    if '<section class="saved-edit">' not in html:
        html = html.replace(marker, block + marker)
    html = html.replace('PowerPointで描画。', 'PowerPoint出力PDFをPNG化。')
    html_path.write_text(html, 'utf-8')
    guide_path = CASE / 'GUIDE.md'
    guide = guide_path.read_text('utf-8')
    if '## 実際に保存した文字編集' not in guide:
        guide += '\n## 実際に保存した文字編集\n\n`qa/editability/native-label-edited.pptx`は「海・湖の水」だけを「湖の水」へ変え、別ファイルで保存・再表示したPPTXです。元の復元PPTXは変更していません。両方のプレビューはPowerPoint出力PDFをPopplerでPNG化しています。直接PNG出力時の日本語文字下の薄い描画ノイズを避けるためです。\n\nこの経路はReconstruction専用です。既存PPTXのRepairはartifact runtimeが必要で、この作例では実行していません。\n'
    guide_path.write_text(guide, 'utf-8')
    shutil.copy2(guide_path, FORK / 'GUIDE.md')
    shutil.copytree(proof, FORK / 'editability-proof', dirs_exist_ok=True)
    spec = importlib.util.spec_from_file_location('sci', ROOT / 'tools/build_sci_reconstruction.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    packages = [module.package(CASE, ROOT / 'downloads/sci-diagram-reconstruction-example-ja.zip'),
                module.package(FORK, ROOT / 'downloads/sci-diagram-reconstruction-ja.zip')]
    dump(CASE / 'PACKAGES.json', packages)
    print(json.dumps({'native_edit_saved_reopened': True, 'original_reconstruction_unchanged': True, 'packages': packages}))


if __name__ == '__main__':
    main()
