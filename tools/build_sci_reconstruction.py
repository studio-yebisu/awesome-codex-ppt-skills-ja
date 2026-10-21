"""Prepare the supplied bitmap for the SciDiagram reconstruction example.

The bitmap is an authored test input, not a USGS image or an unassisted baseline.
Reconstruction build.mjs and its inventory are authored by the recorded Opus run.
No canonical catalog files are modified by this builder.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'examples/repositories/sci-diagram-reconstruction'
UPSTREAM = ROOT / '.build/actual-upstreams/HututuWorks__sci-diagram-pptx'
SKILL = UPSTREAM / 'skills/sci-diagram-pptx'
FORK = ROOT / 'skill-forks/sci-diagram-reconstruction-ja'
NODE = Path('C:/Users/owner/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
NODE_MODULES = NODE.parent.parent / 'node_modules'


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', 'utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


SOURCE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<rect width="1600" height="900" fill="#FFFFFF"/>
<defs><marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M 0 0 L 12 6 L 0 12 Z" fill="#145B78"/></marker></defs>
<g font-family="Yu Gothic" fill="#153B50">
<text x="100" y="109" font-size="52" font-weight="700">水循環の代表的な経路</text>
<g stroke="#145B78" stroke-width="4" fill="none" marker-end="url(#arrow)">
<path d="M 350 560 L 350 360"/>
<path d="M 600 290 L 1000 290"/>
<path d="M 1250 360 L 1250 560"/>
<path d="M 1000 630 L 600 630"/>
</g>
<g stroke="#145B78" stroke-width="3">
<rect x="100" y="220" width="500" height="140" fill="#EAF4FA"/>
<rect x="1000" y="220" width="500" height="140" fill="#EAF4FA"/>
<rect x="1000" y="560" width="500" height="140" fill="#EAF4FA"/>
<rect x="100" y="560" width="500" height="140" fill="#EAF4FA"/>
</g>
<g text-anchor="middle" font-size="36" font-weight="700">
<text x="350" y="303">大気中の水蒸気</text>
<text x="1250" y="303">雲の中の水滴</text>
<text x="1250" y="643">川の水</text>
<text x="350" y="643">海・湖の水</text>
</g>
<g text-anchor="middle" font-size="32">
<text x="265" y="471">蒸発</text>
<text x="800" y="260">凝結</text>
<text x="1335" y="471">降水</text>
<text x="800" y="680">水の流れ</text>
</g>
<text x="100" y="801" font-size="27">水の移動の一部のみを示す。量・時間・縮尺は表していない。</text>
</g></svg>
'''


def prepare():
    source = CASE / 'input'
    passed = CASE / 'pass-01'
    source.mkdir(parents=True, exist_ok=True)
    passed.mkdir(parents=True, exist_ok=True)
    svg = source / 'authored-source.svg'
    svg.write_text(SOURCE_SVG, 'utf-8')
    # A source raster is required for the actual image-to-native task. The SVG
    # is retained only as provenance for this deliberately authored test input.
    render = source / 'rasterize-source.cjs'
    render.write_text("const sharp = require(process.argv[2]);\nsharp(process.argv[3]).png().toFile(process.argv[4]);\n", 'utf-8')
    subprocess.run([str(NODE), str(render), str(NODE_MODULES / 'sharp'), str(svg), str(source / 'source.png')], check=True)
    shutil.copy2(source / 'source.png', passed / 'source.png')
    dump(source / 'SOURCE-PROVENANCE.json', {
        'kind': 'original_authored_reconstruction_test_input',
        'author': '八百万図AIツールボックス',
        'description_ja': '科学模式図の復元を試すため、八百万図AIツールボックスが先に作成したPNG入力。既存資料の改善前例や、スキル未使用AI出力ではない。',
        'source_dimensions_px': {'width': 1600, 'height': 900},
        'source_file': 'source.png',
        'source_sha256': sha(source / 'source.png'),
        'source_svg_file': 'authored-source.svg',
        'source_svg_sha256': sha(svg),
        'license': 'CC0-1.0',
        'scientific_scope_ja': '水循環の代表的な経路の一部。定量値、移動時間、地形の縮尺は示さない。',
        'sources': [
            {'title': 'USGS: Condensation and the Water Cycle', 'url': 'https://www.usgs.gov/water-science-school/science/condensation-and-water-cycle', 'supports_ja': '大気中の水蒸気から液体水への凝結と、雲から落下する降水。'},
            {'title': 'USGS: Follow a Drip Through the Water Cycle', 'url': 'https://www.usgs.gov/water-science-school/science/follow-a-drip-through-water-cycle', 'supports_ja': '蒸発、凝結、地表水、海・湖へ戻る経路。'}
        ],
        'science_verification_date': '2026-10-15',
        'usgs_image_reproduced': False,
        'before_after_quality_or_speed_claim': False
    })
    runtime_link = CASE / 'node_modules'
    if not runtime_link.exists():
        subprocess.run(['cmd', '/c', 'mklink', '/J', str(runtime_link), str(NODE_MODULES)], check=True, capture_output=True)
    dump(CASE / 'input/runtime-selection.json', {'runtime': 'pptxgenjs', 'version': '4.0.1', 'explicit_selection': True, 'source_skill_commit': 'cc8f0030edf80eeab6e52849b8c39fe638466776'})
    print(json.dumps({'source': str(source / 'source.png'), 'sha256': sha(source / 'source.png'), 'prepared': True}))


JAPANESE_SKILL = '''---
name: sci-diagram-reconstruction-ja
description: 提供された科学模式図の画像1枚を、元の文言・領域・矢印の関係を保った編集可能なPowerPoint1枚へ復元する。新しい科学図の考案、統計グラフ、画像の貼り付けだけには使わない。
---

# 科学模式図を編集可能なPowerPointに復元する

原典は HututuWorks/sci-diagram-pptx。固定コミットは `cc8f0030edf80eeab6e52849b8c39fe638466776`。Apache-2.0の非公式日本語ガイド。原典SKILLと参照文書を `upstream/` に同梱する。

## 入力と出力

入力は、ラベルと矢印が読める科学模式図の画像1枚。対象パネルを指定した場合は、その範囲を使う。元画像は `source.png` などの原形式で保存する。

出力は図を復元したPPTX1枚と、実際に実行した `build.mjs`。文字、標準図形、関係を示す線は個別に編集できるnativeオブジェクトにする。元画像の全面貼り付け、隠れたトレース画像、参照用スライドは作らない。

## 原図から読み取る内容

原図を元の解像度で開き、次を座標付きで記録する。

- `NODES`: 固定ID、原文のラベル、標準図形、pixel座標の範囲、色と文字。
- `EDGES`: 固定ID、出発点と到着点、片方向・双方向・線のみ、実際の経路、線の意味と注記。
- `INSETS`: native化すると根拠を損なう写真・実験画像などの切り出し範囲と役割。

見た目の近さから関係を推測しない。矢印の向き、原文、式、包含関係、破線の意味を勝手に変えない。各要素はnativeか画像内かの片方だけに所有させ、二重に描かない。読めない文字が意味を変えるときは、推測せず高解像度入力を求める。

## この配布物の実行経路

`SCI_DIAGRAM_RUNTIME=pptxgenjs` を明示的に選択した例。PptxGenJS 4.0.1、Node.js20以上、Python3.10以上、LibreOffice、pdftoppmが必要。依存を備えたホストのruntime rootの下に作業フォルダーを置く。作業・配布フォルダーへnode_modulesをコピーしない。

執筆前に `upstream/scripts/probe_runtime.mjs --runtime pptxgenjs --task-dir <作業フォルダー>` を1回実行する。実際の作業フォルダーから依存を解決できることを確認する。欠けた依存を新しく導入する前に、ホスト環境の条件を確認する。

`upstream/assets/pptxgenjs-build-template.mjs` を元に `build.mjs` を作る。SOURCEのpixel座標からスライド座標への変換は1つだけにする。`connectOneWay`、`connectBothWays`、`connectExactPath`と検証を維持する。4.0.1では到着点の矢印を最終segmentの`endArrowType`に指定する。

文字はtextbox、意味を持つ領域は標準図形、直線関係はnativeの線と矢印にする。画像内の文字を重ねてnative化しない。写真や実験結果は差し替え可能な画像枠として残す。PptxGenJSは既存PPTXを読み込み修復する用途には使えない。

## 確認と渡し方

`pass-01/source.png`、`pass-01/build.mjs`、生成した`pass-01/editable.pptx`を残す。生成後に原典のrendererと`check_pptx.py --require-single-slide --slide 1 --pass-index 1`を実行する。元PNGと描画結果を並べ、文言、矢印、包含、欠落、文字切れを確認する。見た目が同じでも編集可能性は構造で確かめる。

意味や方向の誤り、欠落、読めない文字、flattenされた構造などをまとめて直す。原典の既定は2passまで。利用者が追加修正を明示した場合は、その指示に従う。細かな字間やアンチエイリアス差は元の意味を変えない。

完成時は実行runtime、採用pass、実施した確認、近似や画像部分を短く報告する。「見た目が改善」「何分短縮」「どんな図も復元できる」など、実測していない効果を足さない。

## 作例で試す

同梱作例は八百万図AIツールボックスが先に作った1600×900の模式図PNG。USGS画像の複写ではない。これを実入力として、4個の箱、4本の矢印、元の日本語ラベルをnative PPTXへ復元した。入力作成と復元を分けて記録し、見た目の優劣を比較した例とは扱わない。
'''


GUIDE = '''# 科学図の画像を編集可能なPPTXへ復元する

**sci-diagram-pptx**は、提供された科学模式図の文言と関係を保ち、PowerPointで編集できる図へ復元するスキルです。ラベルだけを直したい、発表用に矢印の位置を調整したい、元の編集ファイルがない場合に使います。

この作例では、八百万図AIツールボックスが先に作ったPNGを入力にしました。Opus 5.5が原典SKILLとその画像を読み、公式portable templateから実行用build.mjsと対応表を作成しました。既存の科学図を改善した事例や、スキルなしのAIと比較した結果ではありません。

入力PNGは画像全体で1個です。出力PPTXは同じラベルと配置を持つ4個の箱、4本の方向付き矢印、タイトル、注記を個別に編集できます。元PNGはPPTX内に埋め込みません。

## 最初の操作

1. `pass-01/source.png`と`render/slide-01.png`を比較し、元の文字と矢印が保持されていることを確認します。
2. `pass-01/editable.pptx`をPowerPointで開きます。
3. 「海・湖の水」だけを選んで文字を編集します。図全体を画像として貼り直す必要はありません。

## 自分の図で使う

日本語スキルと一式ZIPを取得し、読める解像度の科学模式図を入力してください。新しい図を考案する依頼とは分け、元のラベルと関係を保つよう指定します。複雑な写真・実験結果の小図は、必要に応じて差し替え可能な画像として残します。

Node.js20以上とPptxGenJS4.0.1を備えたruntime rootの下へ作業フォルダーを置きます。実行は`node build.mjs`。既存PPTXを意図的に置き換える場合のみ`--overwrite`を付けます。日本語はWindows搭載のYu Gothicを参照し、フォントファイルは再配布しません。別環境の文字表示には対応フォントが必要です。

runtime rootを初めて用意する場合は、`upstream/package.json`と`upstream/package-lock.json`をそのrootへコピーし、そこで`npm ci --ignore-scripts --no-audit --no-fund`を実行します。配下の新しい作業フォルダーへ`source.png`と`build.mjs`だけをコピーし、依存probe後に実行します。依存はホスト側で保持し、成果物へnode_modulesを含めません。

原典のSKILL、再構成契約、portable runtime参照、検査スクリプト、Apache-2.0 LICENSEを同梱しています。原典取得物にNOTICEはありません。PptxGenJSのMIT条件を保持しています。元の科学的説明はUSGSの水循環解説を参照し、図は独自制作です。経路の一部だけを示し、量・時間・縮尺を表していません。

実行環境、確認結果、入力と出力のhashはPROVENANCE.jsonとQA.jsonに記録します。これらの確認は、任意の科学図を自動で正しく復元できることや、時間短縮を証明するものではありません。
'''


def fork_files():
    FORK.mkdir(parents=True, exist_ok=True)
    (FORK / 'SKILL.md').write_text(JAPANESE_SKILL, 'utf-8')
    originals = [
        'SKILL.md', 'references/reconstruction.md', 'references/runtime-pptxgenjs.md',
        'assets/pptxgenjs-build-template.mjs', 'scripts/check_pptx.py',
        'scripts/render_pptx.py', 'scripts/probe_runtime.mjs'
    ]
    for relative in originals:
        target = FORK / 'upstream' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SKILL / relative, target)
    for filename in ['LICENSE', 'package.json', 'package-lock.json']:
        shutil.copy2(UPSTREAM / filename, FORK / 'upstream' / filename)
    dependencies = FORK / 'dependencies/pptxgenjs'
    dependencies.mkdir(parents=True, exist_ok=True)
    shutil.copy2(NODE_MODULES / 'pptxgenjs/LICENSE', dependencies / 'LICENSE')
    (FORK / 'ATTRIBUTION.md').write_text('''# 帰属と変更

原典: HututuWorks/sci-diagram-pptx
https://github.com/HututuWorks/sci-diagram-pptx/tree/cc8f0030edf80eeab6e52849b8c39fe638466776

固定コミット: cc8f0030edf80eeab6e52849b8c39fe638466776
原典ライセンス: Apache-2.0。原文LICENSEをupstream/LICENSEに保持。取得した原典にNOTICEはない。

八百万図AIツールボックスは原典の再構成用途を日本語で案内し、自作入力PNGを実入力にしたnative PPTX復元例を追加した。原典SKILL本文とportable templateの原本をupstream/に未改変で保持する。日本語SKILLと作例実装は非公式派生。PptxGenJS 4.0.1はMIT。Windowsのフォントファイルは同梱しない。
''', 'utf-8')


def package(folder, target):
    files = []
    for base, dirs, names in os.walk(folder, followlinks=False):
        dirs[:] = [name for name in dirs if name not in {'node_modules', '__pycache__', '.private'}]
        for name in names:
            if name.endswith(('.pyc', '.log')) or name in {'runtime-probe.json', 'powerpoint-render.json', 'render-report.json', 'PACKAGES.json', 'index.html'}:
                continue
            files.append(Path(base) / name)
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for item in sorted(files):
            archive.write(item, Path(target.stem) / item.relative_to(folder))
    return {'path': target.relative_to(ROOT).as_posix(), 'sha256': sha(target), 'file_count': len(files)}


def finalize(model, model_record):
    build = CASE / 'pass-01/build.mjs'
    deck = CASE / 'pass-01/editable.pptx'
    inventory = CASE / 'input/reconstruction-inventory.json'
    for item in [build, deck, inventory, CASE / 'render/slide-01.png']:
        if not item.is_file():
            raise RuntimeError(f'Required real artifact missing: {item.name}')
    (CASE / 'GUIDE.md').write_text(GUIDE, 'utf-8')
    prompt = 'この科学模式図の画像1枚を、元の日本語ラベル、4個の箱、4本の矢印の方向、配置を保った編集可能なPowerPoint1枚に復元してください。原典sci-diagram-pptxのReconstructionを使い、ラベル・図形・矢印をnativeオブジェクトにしてください。元画像の全面貼り付けや隠れたトレース画像は使いません。SOURCE、NODES、EDGES、INSETSのpixel対応表、実際に実行するbuild.mjs、元画像、PPTXを残してください。画像は八百万図AIツールボックスが作例用に先に作成した入力です。科学内容の追加やデザイン変更はしません。'
    (CASE / 'PROMPT.txt').write_text(prompt + '\n', 'utf-8')
    source_info = json.loads((CASE / 'input/SOURCE-PROVENANCE.json').read_text('utf-8'))
    if sha(CASE / 'pass-01/source.png') != source_info['source_sha256']:
        raise RuntimeError('The actual reconstruction input no longer matches the authored input.')
    checker = json.loads((CASE / 'qa/check-pass-01.json').read_text('utf-8-sig'))
    native = json.loads((CASE / '.private/editability-test/native-editability.json').read_text('utf-8-sig'))
    if checker['hard_failures'] or not native.get('saved_edit_reopened'):
        raise RuntimeError('Real package/native editing verification failed.')
    dump(CASE / 'QA.json', {
        'status': 'technical_checks_and_agent_visual_inspection_complete',
        'accepted_pass': 'pass-01', 'slide_count': 1,
        'upstream_checker': {'status': checker['status'], 'hard_failures': len(checker['hard_failures']), 'warnings': len(checker['warnings']), 'next_action': checker['decision']['next_action'], 'report': 'qa/check-pass-01.json'},
        'renderers': ['Microsoft PowerPoint 16.0', 'LibreOffice 24.2.5.2 via original isolated renderer'],
        'source_byte_equality': True,
        'native_edit_test': native,
        'agent_visual_inspection': {'reviewer': 'Codex', 'inspected_files': ['input/source.png', 'render/slide-01.png'], 'checks': ['Original Japanese text retained', 'Four relationships and arrow directions retained', 'Source box positions retained', 'No visible clipping or serious overlap'], 'blockers': []},
        'independent_kimi_opus_review': 'pending_parent_integration',
        'human_review': False,
        'measured_time_saving': False, 'aesthetic_improvement_comparison': False
    })
    fork_files()
    shutil.copytree(FORK / 'upstream', CASE / 'upstream', dirs_exist_ok=True)
    shutil.copytree(FORK / 'dependencies', CASE / 'dependencies', dirs_exist_ok=True)
    example = FORK / 'example'
    example.mkdir(parents=True, exist_ok=True)
    for filename in ['source.png', 'build.mjs', 'editable.pptx']:
        shutil.copy2(CASE / 'pass-01' / filename, example / filename)
    shutil.copy2(CASE / 'GUIDE.md', FORK / 'GUIDE.md')
    shutil.copy2(inventory, FORK / 'reconstruction-inventory.json')
    for filename in ['LICENSE']:
        shutil.copy2(UPSTREAM / filename, CASE / filename)
    shutil.copy2(FORK / 'ATTRIBUTION.md', CASE / 'ATTRIBUTION.md')
    dump(CASE / 'PROVENANCE.json', {
        'repository': 'HututuWorks/sci-diagram-pptx', 'upstream_commit': 'cc8f0030edf80eeab6e52849b8c39fe638466776',
        'license': 'Apache-2.0', 'runtime': 'PptxGenJS 4.0.1 (MIT)',
        'route': 'Reconstruction', 'accepted_pass': 'pass-01',
        'source': source_info, 'inventory': 'input/reconstruction-inventory.json',
        'production': {'requested_model': 'claude-opus-5-5', 'reported_model': model, 'scope_ja': '原典SKILLと実入力PNGを読み、復元用build.mjsと要素対応表を執筆。実行と検査はCodexが担当。', 'private_execution_record_id': model_record},
        'template': 'upstream/assets/pptxgenjs-build-template.mjs',
        'applied_rules': ['Provided bitmap input reconstructed as one editable slide', 'Original visible labels and directed topology preserved', 'Native ownership for all meaning-bearing objects; INSETS empty', 'One source-pixel-to-slide transform and original directed connector helpers'],
        'not_claimed': ['aesthetic improvement over input', 'time saving', 'arbitrary figure reconstruction', 'pixel identity across renderers'],
        'source_sha256': sha(CASE / 'pass-01/source.png'), 'build_sha256': sha(build), 'pptx_sha256': sha(deck)
    })
    # Reports are evidence, but host absolute paths do not belong in a public kit.
    def portable_report(value):
        if isinstance(value, dict):
            return {key: portable_report(item) for key, item in value.items()}
        if isinstance(value, list):
            return [portable_report(item) for item in value]
        if isinstance(value, str):
            return value.replace(str(CASE), '.').replace(CASE.as_posix(), '.')
        return value
    for report in [CASE / 'qa/check-pass-01.json', CASE / 'render/powerpoint-render.json', CASE / 'qa/libreoffice-pass-01/render-report.json']:
        if report.is_file():
            dump(report, portable_report(json.loads(report.read_text('utf-8-sig'))))
    # Keep host-specific probe details out of distributable data.
    dump(CASE / 'input/runtime-probe.json', {'ready': True, 'selectedRuntime': 'pptxgenjs', 'node': '24.19.0', 'pptxgenjs': '4.0.1', 'python': '3.12', 'libreoffice': '24.2.5.2', 'pdftoppm': '26.07.0'})
    # The case HTML is deliberately about the skill operation, then its evidence.
    (CASE / 'index.html').write_text('''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>科学図の画像を編集可能なPPTXへ復元する</title><style>
*{box-sizing:border-box}body{margin:0;background:#f8fafb;color:#163444;font-family:system-ui,"Yu Gothic",sans-serif;line-height:1.75}main{max-width:1260px;margin:auto;padding:48px 24px 70px}a{color:#145b78;text-underline-offset:4px}h1{font-size:clamp(28px,4vw,44px);line-height:1.35;margin:14px 0 20px}h2{font-size:23px;margin:0 0 6px}p{max-width:920px}strong{font-weight:750}.name{font-size:16px;margin:28px 0 0}.flow{font-size:20px;font-weight:700;margin:24px 0 8px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:35px}figure{margin:0}figcaption{margin:0 0 12px}figure img{width:100%;display:block;background:white;border:1px solid #b7cbd6}.caption{font-size:15px;color:#3e5a68;max-width:none;margin:10px 0 0}.actions{display:flex;flex-wrap:wrap;gap:16px 26px;margin:28px 0 36px;padding-bottom:28px;border-bottom:1px solid #c6d5dd}.actions a{font-weight:700}.note{font-size:15px;color:#45606d}.details{border-top:1px solid #c6d5dd;margin-top:35px;padding-top:22px}li{margin:6px 0}code{background:#e9f0f3;padding:2px 5px} @media(max-width:780px){main{padding:28px 18px 50px}.compare{grid-template-columns:1fr;gap:32px}}
</style><main><a href="../../../index.html">スキル一覧へ戻る</a><p class="name">sci-diagram-pptx / HututuWorks</p><h1>科学図の画像を、編集可能なPPTXにする</h1><p>元の編集ファイルがなくても、図の文字や矢印をPowerPointで修正したいときに使います。<strong>元の文言と関係を読み取り、文字・図形・線を個別に編集できる1枚へ復元</strong>します。</p><p class="flow">入力は模式図PNG。出力は同じ図のnative PPTX。</p><p>この例は、4個の箱と4本の矢印を持つ自作PNGを入力にしました。Opus 5.5が原典SKILLとPNGを読み、公式portable templateから復元用コードと対応表を作成しています。</p><div class="actions"><a href="pass-01/editable.pptx" download>編集できるPPTXを開く</a><a href="../../../skill-forks/sci-diagram-reconstruction-ja/SKILL.md" download>日本語スキルを読む</a><a href="../../../downloads/sci-diagram-reconstruction-example-ja.zip" download>入力と実行コードのZIP</a><a href="../../../downloads/sci-diagram-reconstruction-ja.zip" download>日本語スキル一式</a></div><div class="compare"><figure><figcaption><h2>入力 PNG</h2>図全体が1枚の画像</figcaption><img src="input/source.png" alt="復元前の入力PNG。水循環の代表的経路を示す四つの箱と四本の矢印。"><p class="caption">この入力は八百万図AIツールボックスが作例用に先に作成しました。USGS画像の複写や、スキルなしAIの出力ではありません。</p></figure><figure><figcaption><h2>出力 PPTXの描画</h2>同じ文言と矢印を個別のオブジェクトに復元</figcaption><img src="render/slide-01.png" alt="編集可能なPPTXをPowerPointで描画した復元結果。元PNGのラベルと矢印の向きを保持。"><p class="caption">PPTXを開くと、「海・湖の水」だけを選んで文字を直せます。元PNGはPPTX内に貼り付けていません。</p></figure></div><div class="details"><h2>この作例で確認する効果</h2><ul><li>画像内の元の日本語を、編集できる文字として保持する。</li><li>4本の矢印の出発点・到着点・方向を保持する。</li><li>図の意味を変えずに、PowerPointで修正できる状態にする。</li></ul><p class="note">見た目の美化や作業時間の短縮を比較した例ではありません。写真や実験結果を含む複雑な図は、内容に応じて画像のまま残す領域があります。</p><p><a href="input/reconstruction-inventory.json">入力要素とnativeオブジェクトの対応表</a> ・ <a href="GUIDE.md">使い方と制約</a> ・ <a href="PROVENANCE.json">原典と制作範囲</a> ・ <a href="QA.json">実施した確認</a> ・ <a href="https://github.com/HututuWorks/sci-diagram-pptx/blob/cc8f0030edf80eeab6e52849b8c39fe638466776/skills/sci-diagram-pptx/SKILL.md">原典SKILL</a></p><p class="note">図は水循環の一部を示す模式図です。量・時間・縮尺は示しません。科学説明の参照: <a href="https://www.usgs.gov/water-science-school/science/condensation-and-water-cycle">USGS 凝結</a>、<a href="https://www.usgs.gov/water-science-school/science/follow-a-drip-through-water-cycle">USGS 水の経路</a>。</p></div></main></html>''', 'utf-8')
    dump(FORK / 'SOURCE.json', {'repository': 'HututuWorks/sci-diagram-pptx', 'commit': 'cc8f0030edf80eeab6e52849b8c39fe638466776', 'license': 'Apache-2.0', 'modified': True, 'case_studies': ['sci-diagram-reconstruction'], 'changes_ja': '原典の再構成用途を日本語で案内。元PNGとnative復元を比較する独自例を追加。', 'upstream_notice_present': False})
    packages = [package(CASE, ROOT / 'downloads/sci-diagram-reconstruction-example-ja.zip'), package(FORK, ROOT / 'downloads/sci-diagram-reconstruction-ja.zip')]
    dump(CASE / 'PACKAGES.json', packages)
    relative = 'examples/repositories/sci-diagram-reconstruction'
    fragment = [{
        'id': 'sci-diagram-reconstruction', 'title': '科学図の画像を編集可能なPPTXへ復元', 'use_case': '科学模式図の復元',
        'repository': 'HututuWorks/sci-diagram-pptx', 'skill_repository': 'HututuWorks/sci-diagram-pptx',
        'upstream_commit': 'cc8f0030edf80eeab6e52849b8c39fe638466776', 'fork_id': 'sci-diagram-reconstruction-ja',
        'page_count': 1, 'format': 'pptx', 'preview_kind': 'powerpoint-render', 'style': '元PNGの文言・配置・矢印を保持',
        'cover': f'{relative}/render/slide-01.png', 'interior': f'{relative}/render/slide-01.png', 'preview': f'{relative}/index.html',
        'artifact_download': f'{relative}/pass-01/editable.pptx', 'pdf_download': f'{relative}/render/deck.pdf',
        'source_download': 'downloads/sci-diagram-reconstruction-example-ja.zip', 'fork_download': 'downloads/sci-diagram-reconstruction-ja.zip',
        'input': f'{relative}/input/source.png', 'input_data': f'{relative}/input/reconstruction-inventory.json', 'prompt': f'{relative}/PROMPT.txt', 'prompt_text': prompt,
        'provenance': f'{relative}/PROVENANCE.json', 'qa': f'{relative}/QA.json',
        'guide': 'repository.html?repo=HututuWorks%2Fsci-diagram-pptx', 'case_guide': f'{relative}/GUIDE.md',
        'titles': ['水循環の代表的な経路'], 'notes': ['自作の入力PNGを実入力として、元の日本語・4箱・4方向関係をnative PPTXへ復元。図は水循環の一部のみ。量・時間・縮尺は示さない。'],
        'method': '原典Reconstructionと公式PptxGenJS portable templateを適用。Opus 5.5が実PNGを読み、native復元コードと対応表を作成。',
        'sample_notice': '復元用に先に作成した自作PNG。スキル未使用AIとの比較ではなく、見た目の美化や時短を測った例ではない。',
        'pages': [f'{relative}/render/slide-01.png'], 'runtime': 'PptxGenJS 4.0.1 (MIT)', 'editability': 'native_pptx_text_shapes_connectors',
        'preview_notice': 'PowerPointで描画。元PNGのラベルと方向を保持し、文字・図形・矢印を個別編集できる。',
        'producer_model': model, 'production_scope': '原典と入力PNGの読解、native復元実装、対応表の執筆',
        'skill_effect': {'input': 'ラベルと矢印が読める科学模式図PNG1枚', 'operation': '原文と方向関係を対応表にし、標準図形・文字・線として復元', 'output': '元の意味と配置を保つ編集可能なPPTX1枚', 'benefit': '元編集ファイルがなくても文字や矢印を個別修正できる', 'limit': '科学図の新規考案や統計グラフの復元を示す例ではない'}
    }]
    dump(ROOT / 'data/sci-reconstruction-fragment.json', fragment)
    print(json.dumps({'fragment': 'data/sci-reconstruction-fragment.json', 'packages': packages}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--finalize', action='store_true')
    parser.add_argument('--model')
    parser.add_argument('--model-record')
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.finalize:
        if not args.model or not args.model_record:
            parser.error('--finalize requires verified --model and --model-record')
        finalize(args.model, args.model_record)
    else:
        parser.error('Use --prepare to author the input raster before reconstruction.')
