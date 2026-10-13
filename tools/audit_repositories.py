"""Read the original collection's source entrypoints. Does not execute upstream code."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
import argparse, json, re, subprocess, time

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.build/repository-audit'

def api(path):
    result = subprocess.run(['gh', 'api', path], capture_output=True, text=True,
                            encoding='utf-8', timeout=55)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[:280])
    return json.loads(result.stdout)

def raw(repo, commit, path):
    url = 'https://raw.githubusercontent.com/' + repo + '/' + commit + '/' + path
    with urlopen(Request(url, headers={'User-Agent': 'Yebisu-repository-audit'}), timeout=40) as r:
        value = r.read(600001)
    if len(value) > 600000:
        raise ValueError('Documentation exceeds read limit')
    return value

def one(skill, pins, refresh):
    repo = skill['repo_full_name']
    folder = CACHE / repo.replace('/', '__')
    record = folder / 'record.json'
    if record.exists() and not refresh:
        return json.loads(record.read_text(encoding='utf-8'))
    folder.mkdir(parents=True, exist_ok=True)
    checked = datetime.now(timezone.utc).isoformat()
    base = {'repository': repo, 'checked_at': checked, 'kind': skill['kind'],
            'catalog_license': skill.get('license'), 'generation_status': 'not_generated_here'}
    try:
        info = api('repos/' + repo)
        commit = pins.get(repo) or api('repos/' + repo + '/commits/' + info['default_branch'])['sha']
        tree = api('repos/' + repo + '/git/trees/' + commit + '?recursive=1')
        (folder / 'tree.json').write_text(json.dumps(tree), encoding='utf-8')
        blobs = [x for x in tree['tree'] if x['type'] == 'blob']
        paths = [x['path'] for x in blobs]
        skills = sorted([p for p in paths if p.rsplit('/', 1)[-1].lower() == 'skill.md'],
                        key=lambda p: (p.count('/'), len(p), p))
        readmes = sorted([p for p in paths if p.lower() in ['readme.md', 'readme.rst', 'readme.txt']], key=len)
        licenses = [p for p in paths if re.match(r'^(licen[cs]e|copying|notice)(\.|$)', p.rsplit('/', 1)[-1], re.I)]
        root_licenses = [p for p in licenses if '/' not in p]
        chosen = list(dict.fromkeys(readmes[:1] + skills[:3] + root_licenses[:2]))
        docs = []
        for path in chosen:
            try:
                content = raw(repo, commit, path)
                target = folder / 'documents' / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                docs.append({'path': path, 'url': 'https://github.com/' + repo + '/blob/' + commit + '/' + path,
                             'bytes': len(content)})
            except Exception as error:
                docs.append({'path': path, 'read_error': str(error)[:200]})
        base.update(commit=commit, default_branch=info['default_branch'],
                    github_license=(info.get('license') or {}).get('spdx_id'),
                    archived=info['archived'], source_available=True,
                    tree_truncated=tree.get('truncated', False), file_count=len(blobs),
                    skill_paths=skills, license_paths=licenses,
                    entrypoints=[p for p in paths if re.search(r'(package\.json|requirements.*\.txt|pyproject\.toml|\.mjs|\.py|\.typ|\.tex)$', p)][:100],
                    templates=[p for p in paths if re.search(r'(template|theme|example|layout)', p, re.I)][:100],
                    documentation=docs, inspection_status='entrypoints_downloaded',
                    license_review_status='not_manually_reviewed')
    except Exception as error:
        base.update(source_available=False, inspection_status='source_unavailable',
                    error=str(error)[:280], license_review_status='not_manually_reviewed')
    record.write_text(json.dumps(base, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return base

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'data/skills.json').read_text(encoding='utf-8'))['skills']
    ordered = sorted(catalog, key=lambda x: -x['stars'])
    if args.limit:
        ordered = ordered[:args.limit]
    pins = {p['repository']: p['commit'] for p in json.loads((ROOT / 'data/upstreams.json').read_text(encoding='utf-8'))}
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(one, s, pins, args.refresh) for s in ordered]
        for future in as_completed(futures):
            r = future.result()
            results.append(r)
            if len(results) % 10 == 0 or len(results) == len(ordered):
                print(str(len(results)) + '/' + str(len(ordered)) + ' source entrypoints inspected', flush=True)
    by_repo = {r['repository']: r for r in results}
    out = {'checked_at': datetime.now(timezone.utc).isoformat(), 'catalog_count': len(catalog),
           'inspected_count': len(results),
           'repositories': [by_repo[s['repo_full_name']] for s in catalog if s['repo_full_name'] in by_repo]}
    (ROOT / 'data/repository-audit.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Source available: ' + str(sum(r.get('source_available', False) for r in results)), flush=True)

if __name__ == '__main__':
    main()
