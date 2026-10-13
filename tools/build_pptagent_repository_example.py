"""Record a real PPTAgent runtime preflight; never bypass its platform guard.

The attempted Windows build stopped before slide authoring/conversion. This
script preserves that result, not a successful example. It makes no API calls,
does not inspect credentials and does not start Docker or install dependencies.
After arranging a supported Linux/macOS runtime, the original CLI workflow must
still be authored, executed and visually reviewed before a case can be added.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / '.build/actual-upstreams/icip-cas__PPTAgent'
OUT = ROOT / 'examples/repositories/pptagent'
PYTHON = ROOT / '.build/pptagent-py311/Scripts/python.exe'


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', type=Path, default=PYTHON)
    args = parser.parse_args()
    pin = json.loads((UP / 'ACQUISITION.json').read_text(encoding='utf-8'))
    OUT.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([str(args.python), '-c', 'import deeppresenter'],
                            capture_output=True, text=True, encoding='utf-8', timeout=20)
    log = OUT / 'source/import-preflight.txt'
    write(log, result.stdout + result.stderr)
    package_root = args.python.parent.parent / 'Lib/site-packages'
    guard = package_root / 'deeppresenter/__init__.py'
    guard_evidence = {
        'distribution': 'pptagent==1.1.37',
        'path': 'deeppresenter/__init__.py',
        'sha256': sha(guard),
        'platform_guard': 'assert os.name == "posix", "DeepPresenter only supports Linux and macOS"',
    }
    references = []
    for path in ['README.md', 'LICENSE', 'skills/pptagent/SKILL.md',
                 'skills/pptagent/LICENSE', 'skills/pptagent/requirements.txt',
                 'skills/pptagent/package.json', 'skills/pptagent/references/task-contract.md',
                 'skills/pptagent/scripts/pptagent.py',
                 'skills/pptagent/scripts/pptagent_runtime/core.py']:
        references.append({'path': path, 'sha256': sha(UP / path),
                           'url': f"https://github.com/icip-cas/PPTAgent/blob/{pin['commit']}/{path}"})
    status = 'execution_attempted_generation_not_completed'
    reason = ('原典の固定依存pptagent==1.1.37がWindowsをassertで明示拒否。'
              'READMEもLinux（WSL含む）/macOSを要件とする。'
              'libreofficeのWindows shimだけでは、このimport条件を解決できない。')
    if result.returncode == 0:
        status = 'preflight_passed_generation_not_started'
        reason = '依存importは成功。原典CLIの6ページ生成・レビュー工程はまだ未実行。'
    attempted = {
        'status': status, 'repository': 'icip-cas/PPTAgent',
        'upstream_commit': pin['commit'], 'checked_at': datetime.now(timezone.utc).isoformat(),
        'requested_pages': 6, 'generated_pages': 0, 'artifact': None,
        'failed_stage': 'dependency_import' if result.returncode else None,
        'reason_ja': reason, 'api_calls': 0, 'credentials_inspected': False,
        'upstream_modified': False, 'platform_guard_disabled': False,
        'commands_executed': [{'argv': [str(args.python), '-c', 'import deeppresenter'],
                               'exit_code': result.returncode,
                               'log': 'source/import-preflight.txt', 'log_sha256': sha(log)}],
        'dependency_evidence': guard_evidence,
        'earlier_setup_observations': [
            'Project-local Python 3.13 dependency dry-run was stopped; numpy<2 began a source build.',
            'Project-local Python 3.11.15 venv installed pptagent==1.1.37 with --no-deps to inspect/import the fixed dependency.',
            'npm ci --ignore-scripts succeeded in the upstream skill directory; no upstream source was edited.',
            'C:/Program Files/LibreOffice/program/soffice.exe exists; it was not used to create a deck.',
            'Docker Linux engine initially had no named pipe. One hidden Desktop startup was attempted; a later 8-second engine probe timed out.',
            'No WSL distribution settings, OS settings, credentials or external APIs were changed or accessed.',
        ],
        'not_claimed': ['HTML authored', 'PPTX generated', 'original QA passed',
                        'PowerPoint rendering', 'visual approval', 'Linux runtime failure'],
        'next_step_ja': '利用可能なLinux/WSLまたはmacOS環境で原典依存を用意し、multimodalモードの原典CLIを実行する。',
    }
    dump(OUT / 'ATTEMPT.json', attempted)
    dump(OUT / 'PROVENANCE.json', {'repository': 'icip-cas/PPTAgent',
         'upstream_commit': pin['commit'], 'acquisition': pin, 'references': references,
         'execution_status': status, 'generation_status': 'not_generated',
         'method': '原典固定依存の実importまで試行。Windows明示拒否で生成前に停止。',
         'commands_executed': attempted['commands_executed'], 'artifact': None})
    dump(OUT / 'QA.json', {'status': 'not_run_generation_not_completed', 'page_count': 0,
                           'visual_review': 'not_run', 'powerpoint_render': 'not_run',
                           'original_quality_check': 'not_run', 'attempt': 'ATTEMPT.json'})
    inputs = json.loads((ROOT / 'data/case-inputs.json').read_text(encoding='utf-8'))
    dump(OUT / 'input/data.json', inputs['knowledge'])
    write(OUT / 'input/BRIEF.md', '# 制作予定の入力\n\n社内ナレッジ検索の導入提案。'
          '架空の50人企業で4週間・30資料の試作を検討する6ページ。入力はdata.json。'
          'この入力からスライドはまだ生成していません。\n')
    write(OUT / 'PROMPT.txt', 'PPTAgentの原典SKILLとCLIで、添付input/data.jsonから日本語6ページの編集可能PPTXを制作する。'
          'mode: multimodalを使いAPI送信を行わず、原典HTMLレビュー/デッキレビュー/finalizeとPowerPoint全ページ確認を行う。\n')
    shutil.copyfile(UP / 'LICENSE', OUT / 'LICENSE.upstream')
    shutil.copyfile(UP / 'skills/pptagent/LICENSE', OUT / 'LICENSE.skill')
    shutil.copyfile(Path(__file__), OUT / 'source/build_pptagent_repository_example.py')
    write(OUT / 'README.md', '# PPTAgent：Windowsでの実行試行\n\n'
          '**実行試行済み・生成未達です。PPTX、完成HTML、レンダー画像はありません。**\n\n'
          + reason + '\n\n'
          '固定commit: `' + pin['commit'] + '`。`ATTEMPT.json`に実行条件、'
          '`source/import-preflight.txt`に実際のAssertionErrorを保存しています。'
          'Docker Desktopの起動は1回だけ試し、エンジン応答が得られなかったため停止しました。'
          'この結果はLinuxでの動作失敗を意味しません。\n\n'
          '## 対応環境での再開\n\n'
          'Linux（WSL含む）またはmacOS、Python 3.11以降、Node/npm、'
          '`libreoffice`コマンドを用意します。原典のrequirements.txtとpackage-lock.jsonを使い、'
          'Python/Node両方のPlaywright 1.62.0とChromiumを揃えます。'
          '原典`config.example.yaml`のmultimodalモードはホストの実視認を使い、別の画像APIを必要としません。\n\n'
          '原典CLIは `doctor → init → scaffold → review-slides → record-slide-review（各頁）'
          ' → build → review-deck → record-deck-review → finalize` の順です。'
          'record-*のpassは画像を実際に確認してから記録します。'
          '最終`complete=true`とPowerPointレンダーを得るまでは生成済み作例へ登録しません。\n\n'
          '現在の試行のみを再検証するには、カタログrootから'
          '`python tools/build_pptagent_repository_example.py`を実行します。'
          'この補助スクリプトは環境診断と記録だけを行い、依存installやDocker起動はしません。\n\n'
          '原典root/nestedともMIT。再配布時は両LICENSEの著作権・許諾表示を保持します。\n')
    # No successful case is emitted by a preflight or an unsuccessful build.
    dump(ROOT / 'data/pptagent-repository-examples.json', [])
    dump(ROOT / 'data/pptagent-repository-guides.json', [{
        'repository': 'icip-cas/PPTAgent', 'execution_type': 'original_cli_preflight',
        'execution_status': status, 'case_ids': [],
        'summary_ja': reason, 'requirements': ['Linux（WSL含む）またはmacOS',
          'Python>=3.11 / pptagent==1.1.37', 'Python/Node Playwright==1.62.0、Chromium、npm依存',
          'libreofficeコマンド、ホストによる全ページの視認'],
        'steps': ['対応OSで原典runtimeを準備', 'doctor', 'init/scaffoldと日本語HTML執筆',
          'review-slidesと各頁record-slide-review', 'build/review-deck/record-deck-review/finalize',
          'PowerPointで全ページを再描画して確認'],
        'commands': ['python tools/build_pptagent_repository_example.py'],
        'source_refs': references, 'limitations': [reason,
          'Linux環境の生成成功は未検証。Windows失敗を全環境の動作不能と一般化しない。'],
        'evidence': 'examples/repositories/pptagent/ATTEMPT.json',
        'guide': 'examples/repositories/pptagent/README.md',
    }])
    print(json.dumps({'status': status, 'import_exit_code': result.returncode,
                      'generated_pages': 0, 'evidence': str(OUT / 'ATTEMPT.json')}, ensure_ascii=False))
    return 1 if result.returncode else 0


if __name__ == '__main__':
    raise SystemExit(main())
