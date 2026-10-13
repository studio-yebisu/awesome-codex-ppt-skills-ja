"""Acquire a selected catalog repository at the audited commit; never run its installer."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import argparse, io, json, zipfile

ROOT = Path(__file__).resolve().parents[1]

def acquire(repo):
    record = json.loads((ROOT / '.build/repository-audit' / repo.replace('/', '__') / 'record.json').read_text(encoding='utf-8'))
    commit = record['commit']
    dest = ROOT / '.build/actual-upstreams' / repo.replace('/', '__')
    receipt = dest / 'ACQUISITION.json'
    if receipt.exists():
        old = json.loads(receipt.read_text(encoding='utf-8'))
        if old['commit'] != commit:
            raise ValueError('An existing checkout has another pinned commit: ' + repo)
        return repo + ': acquired previously'
    url = 'https://codeload.github.com/' + repo + '/zip/' + commit
    with urlopen(Request(url, headers={'User-Agent': 'Yebisu-local-slides'}), timeout=80) as r:
        content = r.read(200000001)
    if len(content) > 200000000:
        raise ValueError('Archive exceeds 200 MB; inspect source selection first')
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        prefix = archive.namelist()[0].split('/')[0] + '/'
        for member in archive.infolist():
            if member.is_dir():
                continue
            target = (dest / member.filename.removeprefix(prefix)).resolve()
            if not target.is_relative_to(dest.resolve()):
                raise ValueError('Archive path escapes checkout')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    receipt.write_text(json.dumps({'repository': repo, 'commit': commit, 'archive_url': url,
                                 'archive_sha256': sha256(content).hexdigest(), 'bytes': len(content),
                                 'checked_at': datetime.now(timezone.utc).isoformat(),
                                 'root': str(dest)}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return repo + ': ' + str(len(content)) + ' bytes / ' + commit[:12]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('repositories', nargs='+')
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in as_completed([pool.submit(acquire, repo) for repo in args.repositories]):
            print(result.result(), flush=True)
