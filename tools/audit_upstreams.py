"""Acquire pinned upstream skill entrypoints and license evidence; never execute upstream code."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("hugohe3/ppt-master", "skills/ppt-master/SKILL.md", "yebisu-pptx"),
    ("zarazhangrui/frontend-slides", "SKILL.md", "yebisu-web-slides"),
    ("JimLiu/baoyu-skills", "skills/baoyu-slide-deck/SKILL.md", "yebisu-story-slides"),
    ("op7418/guizang-ppt-skill", "SKILL.md", "yebisu-editorial-slides"),
    ("slidevjs/slidev", None, None),
    ("marp-team/marp", None, None),
    ("hakimel/reveal.js", None, None),
    ("gitbrent/PptxGenJS", None, None),
    ("anthropics/skills", "skills/pptx/SKILL.md", None),
]

def api(path):
    result = subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True, encoding="utf-8")
    return json.loads(result.stdout)

def raw(repo, commit, filename):
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{filename}"
    request = urllib.request.Request(url, headers={"User-Agent": "八百万図AIツールボックス-license-audit"})
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()

def audit(source):
    repo, skill_path, fork = source
    metadata = api(f"repos/{repo}")
    commit = api(f"repos/{repo}/commits/{metadata['default_branch']}")["sha"]
    tree = api(f"repos/{repo}/git/trees/{commit}?recursive=1")
    paths = [entry["path"] for entry in tree["tree"] if entry["type"] == "blob"]
    licenses = [p for p in paths if '/' not in p and p.upper().startswith(('LICENSE', 'COPYING'))]
    if not licenses and fork:
        raise ValueError(f"No root license for {repo}; do not redistribute")
    if skill_path and skill_path not in paths:
        candidates = [p for p in paths if p.endswith('SKILL.md')]
        if fork and len(candidates) == 1:
            skill_path = candidates[0]
        elif fork:
            raise ValueError(f"Cannot locate skill for {repo}: {candidates[:10]}")
    dest = ROOT / 'sources' / repo.replace('/', '__')
    dest.mkdir(parents=True, exist_ok=True)
    evidence = []
    for filename in licenses:
        content = raw(repo, commit, filename)
        (dest / Path(filename).name).write_bytes(content)
        evidence.append({'path': str((dest / Path(filename).name).relative_to(ROOT)).replace('\\', '/'),
                         'upstream_path': filename, 'sha256': sha256(content).hexdigest(),
                         'url': f'https://github.com/{repo}/blob/{commit}/{filename}'})
    # Some document skills have a license distinct from the repository license.
    if repo == 'anthropics/skills':
        for filename in [p for p in paths if p.startswith('skills/pptx/') and 'LICENSE' in p.upper()]:
            content = raw(repo, commit, filename)
            # Retain restricted terms as local audit evidence, never distribute skill materials.
            target = ROOT / '.build/license-review' / ('pptx-' + Path(filename).name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            evidence.append({'upstream_path': filename, 'sha256': sha256(content).hexdigest(),
                'url': f'https://github.com/{repo}/blob/{commit}/{filename}'})
    entry = None
    if fork:
        content = raw(repo, commit, skill_path)
        (dest / 'SKILL.upstream.md').write_bytes(content)
        entry = {'path': str((dest / 'SKILL.upstream.md').relative_to(ROOT)).replace('\\', '/'),
                 'upstream_path': skill_path, 'sha256': sha256(content).hexdigest()}
    record = {'repository': repo, 'url': metadata['html_url'], 'commit': commit,
              'stars': metadata['stargazers_count'], 'checked_at': datetime.now(timezone.utc).isoformat(),
              'github_license': (metadata.get('license') or {}).get('spdx_id', 'NOASSERTION'),
              'license_evidence': evidence, 'entrypoint': entry, 'derived_skill': fork,
              'status': 'license_evidence_acquired_pending_review', 'tree_truncated': tree.get('truncated',False)}
    (dest / 'provenance.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"{repo}: {record['github_license']} / {record['stars']:,} stars / {commit[:12]}", flush=True)
    return record

if __name__ == '__main__':
    records = []
    for source in SOURCES:
        cached = ROOT / 'sources' / source[0].replace('/', '__') / 'provenance.json'
        records.append(json.loads(cached.read_text(encoding='utf-8')) if cached.exists() else audit(source))
    (ROOT/'data/upstreams.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
