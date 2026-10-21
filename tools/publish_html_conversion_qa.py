"""Publish real Stage5 materials and native editing proof for the HTML converter."""
from pathlib import Path
from datetime import datetime, timezone
import difflib
import hashlib
import importlib.util
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/html-editable-showcase'
FORK = ROOT / 'skill-forks/html-editable-ja'


def read(p):
    return json.loads(p.read_text('utf-8-sig'))


def dump(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def portable(d):
    if isinstance(d, dict):
        return {k: portable(v) for k, v in d.items()}
    if isinstance(d, list):
        return [portable(v) for v in d]
    return d.replace(str(CASE), '.').replace(CASE.as_posix(), '.') if isinstance(d, str) else d


SKILL = '''---
name: html-editable-ja
description: 既存HTMLの文字と単純な図形を、編集可能なPowerPointへ変換する。
---

# HTMLから編集できるPowerPointへ

原典 Hasasasa/html-to-editable-pptx / 17c1dbb76e958543dc2741a7d50ca374354f33b7 / MIT。非公式の日本語案内。原文upstream/SKILL.mdとsupported-css.mdを読む。

1. 元HTML、フォント、画像をそろえる。原典のページ検出条件を確認する。特定のdata属性が必須だと思い込まない。
2. Python依存とPlaywright Chromium、PPTX描画用のPowerPointまたはLibreOfficeを用意する。字体の導入可否とaudit.modeを、既に指定された条件に合わせる。不明な条件だけ確認する。
3. convert.pyへ元HTMLと出力先を渡す。原典は元HTMLを保全して.audited.htmlを作る。修正はこのコピーで行う。
4. 原典はpreflight→DOM実測→文字・図形・画像への組立→字体処理を行う。単純な文字・図形は編集性を保ち、複雑な装飾やSVGは画像になる場合がある。全CSSの再現を保証しない。
5. Stage5aの構造警告とStage5bのHTML/PPTX比較画像を確認する。pageなら全頁、triageなら一覧と警告頁、manualなら担当者の結果を記録する。生成成功だけを合格にしない。
6. 欠落やずれの原因を、文字・図形・装飾画像・媒体のどの変換にあるか調べる。.audited.htmlか明示した局所adapterを直し、該当頁または全頁を再変換する。
7. PowerPointで文字を実際に編集できる範囲を確認する。埋込字体を使えない場合は--no-embed-fontsを明示し、利用端末に必要な字体を案内する。
8. 完成PPTX、元HTMLと修正コピー、使用字体・利用条件、比較と未解決事項を渡す。原典cleanupは検査用の中間物を除く機能なので、必要な証拠を保存してから使う。

## 同梱作例の差分

日本語5頁のブランド案。局所フォント登録adapterに加え、CSSの三角形の旗を修正コピーで同じ形のSVGへ替えた。平面デザインにOffice既定の影が付くため、原典assemble直後・原典Stage5検査前に、図形の暗黙effectRefだけを0にするcase専用adapterを通す。原典converterは未改変。SVGの旗は画像部品、文字と単純図形はnative。字体埋込版がPowerPointで開けなかったため--no-embed-fontsを使用。原TTF/OFLは同梱。開けない症状の原因は未確定。埋込みを有効にする場合は、別コピーで開けるか再検証する。
'''


def main():
    index = read(CASE / 'deck_audit/audit_index.json')
    assert index['total_pages'] == 5 and index['audit_mode'] == 'page'
    assert index['self_check_summary']['engine'] == 'PowerPoint'
    assert index['self_check_summary']['structural_warnings_count'] == 0
    edit = read(CASE / 'qa/editability/native-editability.json')
    assert edit['saved_edit_reopened'] and edit['original_untouched']
    assert edit['original_sha256'] == sha(CASE / 'deck.pptx')
    target = CASE / 'qa/comparison'
    target.mkdir(parents=True, exist_ok=True)
    for item in [*list((CASE / 'deck_audit').glob('*compare.png')), CASE / 'deck_audit/audit_contact_01_05.png']:
        shutil.copy2(item, target / item.name)
    dump(target / 'audit-index.json', portable(index))
    receipt = {'checked_at': datetime.now(timezone.utc).isoformat(),
               'command': 'python convert_local_fonts.py index.audited.html --out deck.pptx --keep-screenshots --no-embed-fonts',
               'audit_mode': 'page', 'original_stage5a_structural_warnings': 0,
               'original_stage5b_compare_pages': 5, 'agent_read_all5_compare_images': True,
               'native_edit_saved_and_reopened': True, 'pptx_sha256': sha(CASE / 'deck.pptx'),
               'input_original_sha256': sha(CASE / 'index.html'), 'audited_copy_sha256': sha(CASE / 'index.audited.html'),
               'fixed': ['CSS border triangle flag replaced with equivalent SVG in audited copy',
                         'Implicit Office theme effects removed by a declared adapter before original Stage5 checks'],
               'remaining': ['Browser and PowerPoint line metrics and font weights differ slightly',
                             'SVG flag remains an image object; fonts are not embedded',
                             'Repair not independently regraded yet']}
    dump(CASE / 'qa/quality-loop-receipt.json', receipt)
    qa = read(CASE / 'QA.json')
    qa.update(status='original_stage5_and_all5_compare_review_complete',
              representative_preview='render/slide-01.png is an actual PowerPoint render.',
              preview_export='PowerPoint PNG/PDF for all5 pages; source HTML/PPTX comparisons inspected for all5.',
              quality_loop=receipt, native_edit_test='qa/editability/native-editability.json',
              not_performed=['independent regrade after repair', 'formal adoption'] + ([] if (CASE/'qa/zip-replay.json').exists() else ['ZIP replay']),
              zip_reexecution=(CASE/'qa/zip-replay.json').exists(),
              comparator_label_adapter='qa/comparator-label-adapter.diff')
    dump(CASE / 'QA.json', qa)
    prov = read(CASE / 'PROVENANCE.json')
    prov['command'] = receipt['command']
    prov['method'] = 'Original converter preflight→DOM measure→assemble; local Japanese font adapter and explicit flat-style effects adapter; original Stage5a/5b page audit.'
    prov['modifications'] = ['Japanese font mapping only; original converter files unchanged.',
                             'CSS flag equivalent SVG in audited copy; original HTML retained.',
                             'Implicit shape theme effects cleared before original Stage5; adapter in clear_implicit_effects.py.',
                             'No font embedding; original full TTF/OFL provided.',
                             'Comparison report header labels changed to ASCII in visual_audit_labels.py; slide pixels and original converter unchanged.']
    prov['repair_20261015'] = receipt
    dump(CASE / 'PROVENANCE.json', prov)
    for dest in [FORK / 'SKILL.md', CASE / 'SKILL.md']:
        dest.write_text(SKILL, 'utf-8')
    for filename in ['convert_local_fonts.py', 'clear_implicit_effects.py', 'visual_audit_labels.py']:
        shutil.copy2(CASE / filename, FORK / 'references' / filename)
    diff = ''.join(difflib.unified_diff((CASE / 'index.html').read_text('utf-8').splitlines(True),
                                       (CASE / 'index.audited.html').read_text('utf-8').splitlines(True),
                                       fromfile='index.html preserved input', tofile='index.audited.html working copy'))
    (CASE / 'qa/html-audit-fixes.diff').write_text(diff, 'utf-8')
    for dest in [CASE / 'README.md', FORK / 'README.md']:
        dest.write_text('# HTMLを編集可能なPowerPointへ変換する\n\n原HTMLはindex.html、修正用コピーはindex.audited.html。原典Stage5a/5bを有効に変換し、全5頁のHTML/PPTX比較を確認しました。旗の形の欠落と暗黙の影を局所修正しています。原典converterは未改変です。\n\n`python convert_local_fonts.py index.audited.html --out deck.pptx --keep-screenshots --no-embed-fonts`\n\nPython依存、Playwright Chromium、描画用PowerPointが必要。日本語TTF/OFL同梱、字体埋込みは無効です。SVGの旗は画像部品、文字と単純図形は編集できます。元と同じ字幅・字重は保証しません。\n\nqa/comparison/に原典比較、qa/quality-loop-receipt.jsonに実行範囲、qa/editability/に「ひと旗」を「試作店」に変更・保存・再表示した別PPTXを同梱。独立再評価は未了です。\n', 'utf-8')
    base = CASE.relative_to(ROOT).as_posix()
    path = ROOT / 'data/case-integration-notes.json'
    notes = read(path)
    notes.setdefault('html-editable-showcase', {}).update(method=prov['method'],
        preview_notice='原典変換・構造検査・全5頁のHTML/PPTX比較を実施。文字と単純図形は編集可能、SVGは画像。字体は埋込なし。',
        preview_image_notice='原典Stage5bの比較画像で全5頁のHTML/PPTXを確認。最終PPTXの実描画と文字編集・保存・再表示も確認済み。',
        status='original_stage5_and_all5_compare_review_complete',
        editability_proof={'before_path': base + '/render/slide-01.png',
            'after_path': base + '/qa/editability/native-text-edited.png',
            'artifact_path': base + '/qa/editability/native-text-edited.pptx',
            'report_path': base + '/qa/editability/native-editability.json',
            'before_label': '変換したPPTX：右上「ひと旗」', 'after_label': '文字を変更したPPTX：右上「試作店」',
            'description': 'HTMLから変換した右上の店名だけを変更。別のPPTXへ保存し、PowerPointで開き直して確認しました。'})
    dump(path, notes)
    spec = importlib.util.spec_from_file_location('html_converter_builder', ROOT / 'tools/build_html_editable_showcase.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.package()
    print(json.dumps({'pages_compared': 5, 'structural_warnings': 0, 'native_edit_saved_reopened': True}))


if __name__ == '__main__':
    main()
