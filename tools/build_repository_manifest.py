"""Join the original collection to repository-specific production and usage records."""
from pathlib import Path
from urllib.parse import quote
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def dump(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

def main():
    original = load('data/skills.json')['skills']
    audit = {r['repository']: r for r in load('data/repository-audit.json')['repositories']}
    cases = load('data/case-studies.json')
    by_id = {c['id']: c for c in cases}
    for name in ['web-repository-examples', 'native-repository-examples', 'japanese-repository-examples','dashi-repository-examples','codex-image-repository-examples','multiagent-repository-examples','knowledgecat-repository-examples','seaslides-repository-examples','pptdesign-repository-examples','magicslide-repository-examples','imageeditable-repository-examples']:
        if (ROOT / ('data/' + name + '.json')).exists():
            for c in load('data/' + name + '.json'):
                by_id[c['id']] = c
    cases = list(by_id.values())
    for c in cases:
        if 'repository.html?' not in c['guide']:
            c['case_guide'] = c['guide']
        c['guide'] = 'repository.html?repo=' + quote(c['repository'], safe='/')
        c['content_revision'] = hashlib.sha256((ROOT / c['qa']).read_bytes()).hexdigest()[:16]
    dump('data/case-studies.json', cases)
    authored = {}
    readiness = {}
    if (ROOT / 'data/repository-readiness.json').exists():
        readiness = {r['repository']: r for r in load('data/repository-readiness.json')['repositories']}
    for repo, r in readiness.items():
        authored[repo] = {'execution_type': r['generation_method_ja'],
            'requirements': r['dependencies_and_external_services_ja'],
            'commands': [c['command'] for c in r['command_examples']],
            'limitations': r['caveats_ja'],
            'license': r['license']['declared_id'],
            'license_note': r['license']['scope_and_distribution_ja'],
            'source_refs': r['source_refs'],
            'execution_status': r['execution_status'],
            'steps': ['原典の環境と個別条件を確認する', '記載したコマンドの外部API使用条件を確認する', '入力を用意し、原典の方式で生成する', '完成ファイルを開いて全ページを確認する']}
    for name in ['native-repository-guides', 'japanese-repository-guides', 'web-repository-guides','dashi-repository-guides','codex-image-repository-guides','pptagent-repository-guides','multiagent-repository-guides','knowledgecat-repository-guides','spacemulti-repository-guides','presenter-repository-guides','starry-repository-guides','seaslides-repository-guides','pptdesign-repository-guides','magicslide-repository-guides','imageeditable-repository-guides']:
        if (ROOT / ('data/' + name + '.json')).exists():
            authored.update({r['repository']: r for r in load('data/' + name + '.json')})
    profiles = []
    for s in original:
        repo = s['repo_full_name']
        a = audit.get(repo, {})
        works = [c for c in cases if c['repository'] == repo]
        profile = {'repository': repo, 'summary_ja': s['description_ja'], 'kind': s['kind'],
            'upstream_commit': a.get('commit'), 'checked_at': a.get('checked_at'),
            'inspection_status': a.get('inspection_status', 'not_inspected'),
            'license': a.get('github_license') or s.get('license'),
            'license_paths': a.get('license_paths', []), 'skill_paths': a.get('skill_paths', []),
            'source_refs': a.get('documentation', []), 'archived': a.get('archived', False),
            'example_ids': [c['id'] for c in works],
            'production_status': 'generated' if works else ('attempted_not_generated' if repo in readiness and 'attempted' in readiness[repo]['execution_status'] else 'not_started'),
            'license_review_status': 'reviewed_for_example' if works else 'not_manually_reviewed',
            'requirements': [], 'commands': [], 'steps': [],
            'limitations': [] if works else ['この環境での制作は未着手です。原典の入口は取得済みです。'],
            'forks': sorted({c['fork_id'] for c in works if c.get('fork_id')})}
        profile.update(authored.get(repo, {}))
        if works: profile['production_status'] = 'generated'
        profile['original_description_ja'] = s['description_ja']
        profile['example_ids'] = [c['id'] for c in works]
        if works:
            profile['execution_status'] = 'generated_verified_locally' if all(load(c['qa']).get('status') == 'qa_complete' for c in works) else 'generated_with_review_record'
        if works and not profile['commands']:
            c = works[0]
            provenance = load(c['provenance'])
            profile['execution_type'] = provenance.get('execution_type', 'original_skill_workflow')
            profile['method_ja'] = c['method']
            profile['requirements'] = ['原典のスキルを読めるコーディングエージェント', '各作例のPROVENANCE.jsonに記録した制作環境', 'Noto Sans JP（PowerPointでの表示）']
            profile['steps'] = ['日本語派生版を取得し、そのSKILL.mdを読む', '作例の入力資料を、自分の題材へ置き換える', '日本語の依頼文を添付して制作を依頼', '完成した実ファイルを開き、日本語と全ページを確認']
        profiles.append(profile)
    dump('data/repository-guides.json', profiles)
    dump('data/production-ledger.json', {'catalog_count': len(original),
        'source_inspected_count': len(audit), 'produced_repository_count': sum(bool(p['example_ids']) for p in profiles),
        'case_count': len(cases), 'slide_count': sum(c['page_count'] for c in cases),
        'remaining_repository_count': sum(not p['example_ids'] for p in profiles),
        'states': [{'repository': p['repository'], 'state': p['production_status'], 'examples': p['example_ids']} for p in profiles]})
    print(str(sum(bool(p['example_ids']) for p in profiles)) + '/' + str(len(original)) + ' repositories with local Japanese outputs; ' + str(len(cases)) + ' decks')

if __name__ == '__main__':
    main()
