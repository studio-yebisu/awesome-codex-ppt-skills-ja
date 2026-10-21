"""Run the pinned original finalizer against this case's source/runtime adapter.

Original scripts remain byte copies in a private task tree. The sample's local
font and legibility adapters are the same ones used by its public Node build.
This runner neither edits a generated PPTX nor changes QA thresholds.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

CASE = Path(__file__).resolve().parents[1]
ROOT = CASE.parents[2]
UP = ROOT / '.build/actual-upstreams/siril9__presentation-skill'
PRIVATE = CASE / '.private/finalizer-runtime'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--python', default=sys.executable)
    parser.add_argument('--node-dir', type=Path)
    parser.add_argument('--node-modules', type=Path, default=ROOT / '.build/node_modules')
    parser.add_argument('--soffice-dir', type=Path)
    parser.add_argument('--upstream', type=Path, default=UP,
                        help='Checkout/archive of the documented pinned original repository')
    args = parser.parse_args()
    upstream = args.upstream.resolve()
    for name in ['scripts', 'templates', 'schemas', 'references']:
        shutil.copytree(upstream / name, PRIVATE / name, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ['package.json', 'package-lock.json', 'LICENSE']:
        shutil.copy2(upstream / name, PRIVATE / name)
    shutil.copytree(CASE / 'runtime/templates', PRIVATE / 'templates', dirs_exist_ok=True)
    shutil.copy2(CASE / 'runtime/scripts/build_deck_pptxgenjs.js', PRIVATE / 'scripts/build_deck_pptxgenjs.js')
    shutil.copy2(CASE / 'runtime/scripts/render_cache.py', PRIVATE / 'scripts/render_cache.py')
    shutil.copy2(CASE / 'runtime/scripts/render_slides.py', PRIVATE / 'scripts/render_slides.py')
    env = os.environ.copy()
    path_additions = [str(path) for path in [args.node_dir, Path(args.python).parent, args.soffice_dir] if path]
    env['PATH'] = os.pathsep.join([*path_additions, env['PATH']])
    env['PPTX_NODE_MODULES'] = str(args.node_modules)
    env['NODE_PATH'] = env['PPTX_NODE_MODULES']
    command = [args.python, str(PRIVATE / 'scripts/present.py'),
               'finalize', '--outline', str(CASE / 'input/outline.json'),
               '--output', str(CASE / 'deck.pptx'), '--qa-dir', str(CASE / '.private/finalize-qa'),
               '--no-render-cache']
    result = subprocess.run(command, env=env, cwd=PRIVATE, capture_output=True, text=True,
                            encoding='utf-8', errors='replace')
    private_record = CASE / '.private/finalize-execution.json'
    private_record.write_text(json.dumps({'command': command, 'exit_code': result.returncode,
        'original_present_sha256': sha(upstream / 'scripts/present.py'),
        'executed_present_sha256': sha(PRIVATE / 'scripts/present.py'),
        'original_finalizer_sha256': sha(upstream / 'scripts/finalize_quick_deck.py'),
        'executed_finalizer_sha256': sha(PRIVATE / 'scripts/finalize_quick_deck.py'),
        'hash_guard_adapter_sha256': sha(PRIVATE / 'scripts/render_cache.py'),
        'sample_adapter_sha256': sha(CASE / 'runtime/templates/pptxgenjs/slides.js')}, indent=2) + '\n', 'utf-8')
    (CASE / '.private/finalize-stdout.txt').write_text(result.stdout, 'utf-8')
    (CASE / '.private/finalize-stderr.txt').write_text(result.stderr, 'utf-8')
    raw = CASE / '.private/finalize-qa/finalize_receipt.json'
    if raw.is_file():
        receipt = json.loads(raw.read_text('utf-8'))
        # Public evidence retains measured counts, verdicts and artifact hashes.
        # Absolute host paths and command working directories are replaced.
        def safe(value):
            if isinstance(value, dict):
                return {key: safe(item) for key, item in value.items()}
            if isinstance(value, list):
                return [safe(item) for item in value]
            if isinstance(value, str):
                for source, replacement in [(str(PRIVATE), '<pinned-runtime>'),
                    (str(CASE), '<case>'), (str(ROOT), '<slides-root>'),
                    (str(Path(args.python).parent), '<host-python>'),
                    (str(args.node_dir), '<host-node>')]:
                    value = value.replace(source, replacement).replace(source.replace('\\', '/'), replacement).replace(source.replace('\\', '\\\\'), replacement)
                return value
            return value
        public = safe(receipt)
        public['path_sanitization'] = 'Host absolute paths replaced; original receipt retained privately with the recorded SHA256.'
        public['original_receipt_sha256'] = sha(raw)
        public_dir = CASE / 'qa/finalize'
        public_dir.mkdir(parents=True, exist_ok=True)
        (public_dir / 'finalize_receipt.json').write_text(json.dumps(public, ensure_ascii=False, indent=2) + '\n', 'utf-8')
        for filename in ['qa_report.json', 'repair_packet.json', 'design_rules.json', 'layout_lint.json', 'accessibility.json']:
            item = raw.parent / filename
            if item.is_file():
                (public_dir / filename).write_text(json.dumps(safe(json.loads(item.read_text('utf-8'))), ensure_ascii=False, indent=2) + '\n', 'utf-8')
        print(json.dumps({'exit_code': result.returncode, 'receipt': 'qa/finalize/finalize_receipt.json',
                          'passed': receipt.get('passed'), 'failed_stage': receipt.get('failed_stage'),
                          'failure_category': receipt.get('failure_category')}, ensure_ascii=False))
        if not receipt.get('passed'):
            return result.returncode or 1
    else:
        print(json.dumps({'exit_code': result.returncode, 'receipt_written': False,
                          'error_tail': (result.stderr + result.stdout)[-2500:]}, ensure_ascii=False))
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
