#!/usr/bin/env python3
"""state/ 정본 갱신기(CONTRACTS C18 스키마 준수). 메인 오케스트레이터 전용.
  state.py run start <name> <run_type> [--wave W2] [--model M] [--target kind:id] [--brief path]
  state.py run end <name> <success|error|cancelled> [--wave W2] [--error msg] [--commit sha]
  state.py feedback <name> <key> <score0..1> [--wave W] [--comment txt] [--by judge-name]
  state.py board <dotted.path> <json-value>      예) board waves.W2.status '"running"'
"""
import json, sys, uuid, hashlib, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; S = ROOT / 'state'
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
def opt(args, k, d=None):
    return args[args.index(k) + 1] if k in args else d
def rid(wave, name): return uuid.uuid5(uuid.NAMESPACE_URL, f'scrolline-v2/{wave}/{name}').hex
def last(run_id):
    p = S / 'runs.jsonl'; row = None
    if p.exists():
        for l in p.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                if r.get('run_id') == run_id and r.get('kind') != 'feedback': row = r
    return row
def append(row):
    with open(S / 'runs.jsonl', 'a') as f: f.write(json.dumps(row, ensure_ascii=False) + '\n')
def wave_root(wave):
    root = rid(wave, '__wave__')
    if not last(root):
        append(dict(kind='run', run_id=root, parent_run_id=None, root_run_id=root, run_type='wave', name=wave, status='running', started_at=now()))
    return root
a = sys.argv[1:]
if a[0] == 'run':
    ev, name = a[1], a[2]; wave = opt(a, '--wave', 'W2'); root = wave_root(wave); r = rid(wave, name)
    if ev == 'start':
        row = dict(kind='run', run_id=r, parent_run_id=root, root_run_id=root, run_type=a[3], name=name, status='running', started_at=now())
        if opt(a, '--model'): row['model'] = opt(a, '--model')
        if opt(a, '--target'): k, i = opt(a, '--target').split(':', 1); row['target'] = dict(kind=k, id=i)
        if opt(a, '--brief'):
            b = opt(a, '--brief'); row['inputs'] = dict(brief=b, brief_sha256=hashlib.sha256((ROOT / b).read_bytes()).hexdigest())
    else:
        row = dict(last(r) or dict(kind='run', run_id=r, parent_run_id=root, root_run_id=root, run_type='build', name=name, started_at=now()))
        row.update(status=a[3], ended_at=now())
        if opt(a, '--error'): row['error'] = opt(a, '--error')
        if opt(a, '--commit'): row['outputs'] = dict(commit=opt(a, '--commit'))
    append(row)
elif a[0] == 'feedback':
    wave = opt(a, '--wave', 'W5')
    row = dict(kind='feedback', feedback_id=uuid.uuid4().hex, run_id=rid(wave, a[1]), key=a[2], score=float(a[3]),
               by_run_id=rid(wave, opt(a, '--by', 'main')), time=now())
    if opt(a, '--comment'): row['comment'] = opt(a, '--comment')
    append(row)
elif a[0] == 'board':
    p = S / 'board.json'; b = json.loads(p.read_text()); keys = a[1].split('.'); cur = b
    for k in keys[:-1]: cur = cur.setdefault(k, {})
    cur[keys[-1]] = json.loads(a[2]); b['updated'] = now()
    p.write_text(json.dumps(b, ensure_ascii=False, indent=2) + '\n')
