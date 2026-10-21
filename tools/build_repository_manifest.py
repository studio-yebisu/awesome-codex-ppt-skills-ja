"""Join the original collection to repository-specific production and usage records."""
from pathlib import Path
from urllib.parse import quote
import hashlib, json, re

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
    for name in ['web-repository-examples', 'native-repository-examples', 'japanese-repository-examples','dashi-repository-examples','codex-image-repository-examples','multiagent-repository-examples','knowledgecat-repository-examples','seaslides-repository-examples','pptdesign-repository-examples','magicslide-repository-examples','imageeditable-repository-examples','reactdeck-repository-examples','slidemaker-repository-examples','businesscarousel-repository-examples','cyberppt-repository-examples','handsondeck-repository-examples','slidewriter-repository-examples','htmlscrolline-repository-examples','designsystem-repository-examples','htmlconversion-repository-examples','pradaslides-repository-examples','delivery-repository-examples']:
        if (ROOT / ('data/' + name + '.json')).exists():
            for c in load('data/' + name + '.json'):
                by_id[c['id']] = c
    fragments = sorted((ROOT / 'data').glob('sol-*-repository-examples.json'))
    fragments += [ROOT / 'data' / name for name in ['sci-reconstruction-fragment.json', 'mck-native-fragment.json', 'presentation-repair-fragment.json'] if (ROOT / 'data' / name).exists()]
    for fragment in fragments:
        content = load(fragment.relative_to(ROOT))
        fragment_cases = [content['case']] if isinstance(content, dict) else content
        for c in fragment_cases:
            # Parallel producers write their fragments while exports/packages finish.
            # Keep the live site on completed files until that case is ready.
            required=['qa','artifact_download','source_download','fork_download','cover','preview']
            if not all(c.get(key) and (ROOT/c[key]).is_file() for key in required):
                print('Deferred unfinished production fragment: '+c['id'])
                continue
            by_id[c['id']] = c
    cases = list(by_id.values())
    integration_notes = load('data/case-integration-notes.json') if (ROOT/'data/case-integration-notes.json').exists() else {}
    case_overrides = {}
    case_fields = {'title','style','artifact_download','input_data','status','execution_status','sample_notice','preview_notice','preview_image_notice','method','prompt_text','pages','page_count','titles','notes','font_download','font_families','font_notice_ja','preview_kind','license_notice_ja'}
    for patch_path in sorted((ROOT/'data/skill-effect-patches').glob('*.json')):
        for patch in load(patch_path.relative_to(ROOT)):
            case_overrides.setdefault(patch['case_id'], {}).update({k:v for k,v in patch.items() if k in case_fields})
    for c in cases:
        c.update(integration_notes.get(c['id'], {}))
        c.update(case_overrides.get(c['id'], {}))
        if c['id'] == 'beatdeck-showcase':
            base = Path(c['preview']).parent.parent
            index = base / 'source/verification-index.json'
            if (ROOT / index).exists():
                verified = load(index)
                c['pages'] = [(base / row['image']).as_posix() for row in verified]
                c['verification'] = (base / 'verification.html').as_posix()
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
            'steps': ['原典の環境と個別条件を確認する', '記載したコマンドの外部API使用条件を確認する', '入力を用意し、原典の方式で生成する', '原典のビルドと主要な完成ファイルの初回表示を確認する']}
    for name in ['native-repository-guides', 'japanese-repository-guides', 'web-repository-guides','dashi-repository-guides','codex-image-repository-guides','pptagent-repository-guides','multiagent-repository-guides','knowledgecat-repository-guides','spacemulti-repository-guides','presenter-repository-guides','starry-repository-guides','seaslides-repository-guides','pptdesign-repository-guides','magicslide-repository-guides','imageeditable-repository-guides','reactdeck-repository-guides','claudeoffice-repository-guides','slidemaker-repository-guides','businesscarousel-repository-guides','cyberppt-repository-guides','handsondeck-repository-guides','slidewriter-repository-guides','htmlscrolline-repository-guides','designsystem-repository-guides','htmlconversion-repository-guides','pradaslides-repository-guides','delivery-repository-guides']:
        if (ROOT / ('data/' + name + '.json')).exists():
            authored.update({r['repository']: r for r in load('data/' + name + '.json')})
    for fragment in sorted((ROOT / 'data').glob('sol-*-repository-guides.json')):
        for guide in load(fragment.relative_to(ROOT)):
            repo = guide['repository']
            # Legal and original-file paths stay anchored to the audited upstream.
            merged = dict(authored.get(repo, {}))
            guide = {k: v for k, v in guide.items() if k not in ['license_paths', 'skill_paths']}
            merged.update(guide)
            authored[repo] = merged
    if (ROOT / 'data/mck-native-fragment.json').exists():
        guide = load('data/mck-native-fragment.json')['guide']
        authored[guide['repository']] = guide
    if (ROOT / 'data/skill-effect-repository-guides.json').exists():
        for guide in load('data/skill-effect-repository-guides.json'):
            authored.setdefault(guide['repository'], {}).update(guide)
    for path in sorted((ROOT / 'data/skill-effect-patches').glob('*.json')):
        for patch in load(path.relative_to(ROOT)):
            case = by_id.get(patch['case_id'])
            if case and patch.get('guide_patch'):
                repo = case['repository']
                authored.setdefault(repo, {}).update(patch['guide_patch'])
    verified_descriptions = load('data/verified-skill-descriptions.json') if (ROOT/'data/verified-skill-descriptions.json').exists() else {}
    maintained_effects = {e['repository']:e for e in load('data/skill-effects.json')['skills']} if (ROOT/'data/skill-effects.json').exists() else {}
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
        for field in ('requirements','commands','steps','limitations'):
            if isinstance(profile.get(field), str):profile[field]=[profile[field]]
        if works and not profile['steps']:
            profile['steps']=maintained_effects.get(repo,{}).get('how_to_use',[])
        profile['license_notice_ja']=profile.get('license_notice_ja') or profile.get('license_note') or ('原典の利用条件: '+str(profile.get('license') or '同梱LICENSEを確認')+'。素材・書体・依存物はそれぞれの条件を保持する。')
        if works: profile['production_status'] = 'generated'
        profile['original_description_ja'] = verified_descriptions.get(repo, {}).get('description_ja', s['description_ja'])
        profile['example_ids'] = [c['id'] for c in works]
        if works:
            states = [load(c['qa']).get('status') for c in works]
            profile['execution_status'] = 'generated_light_check' if 'light_check_complete' in states else ('generated_author_qa_complete' if all(s == 'qa_complete' for s in states) else 'generated_author_qa_recorded')
            profile['author_qa_states'] = states
            profile['independent_current_version_review'] = '修正後の独立評価は別の固定版ごとに記録。現行版の最終合格は未確定。'
        if works and not profile['commands']:
            c = works[0]
            provenance = load(c['provenance'])
            profile['execution_type'] = profile.get('execution_type') or provenance.get('execution_type', 'original_skill_workflow')
            profile['method_ja'] = c['method']
            if not profile['requirements']:
                profile['requirements'] = ['原典のスキルを読めるコーディングエージェント', '各作例のPROVENANCE.jsonに記録した制作環境', '作例のREADMEに指定した書体と個別条件']
            if not profile['steps']:
                profile['steps'] = ['日本語派生版と固定原典を読み、入力資料を自分の題材へ置き換える', '原典の方式で制作し、全頁の実表示・内容・書体・関係を確認する', '原典の検査、必要な編集や操作と配布物の再現を確認し、未実施の範囲を記録する']
        profiles.append(profile)
    dump('data/repository-guides.json', profiles)
    dump('data/production-ledger.json', {'catalog_count': len(original),
        'source_inspected_count': len(audit), 'produced_repository_count': sum(bool(p['example_ids']) for p in profiles),
        'case_count': len(cases), 'slide_count': sum(c['page_count'] for c in cases if c.get('page_unit')!='段階'),
        'step_count': sum(c['page_count'] for c in cases if c.get('page_unit')=='段階'),
        'remaining_repository_count': sum(not p['example_ids'] for p in profiles),
        'states': [{'repository': p['repository'], 'state': p['production_status'], 'examples': p['example_ids']} for p in profiles]})
    # Preserve original project identity and historical prototypes while joining
    # current produced examples from the same authoritative case list.
    workflows = load('data/project-workflows.json')
    profile_by_repo = {p['repository']: p for p in profiles}
    for project in workflows['projects']:
        works = [c for c in cases if c['repository'] == project['repository']]
        if works:
            profile = profile_by_repo[project['repository']]
            project.update(examples=works, derived_skills=sorted({c['fork_id'] for c in works if c.get('fork_id')}),
                           generation_status='japanese_cases_generated', license_status='reviewed_for_example',
                           execution_status=profile['execution_status'], upstream_commit=profile['upstream_commit'],
                           license_evidence=profile.get('source_refs', project.get('license_evidence', [])))
    workflows.update(catalog_count=len(original), case_count=len(cases),
                     slide_count=sum(c['page_count'] for c in cases if c.get('page_unit')!='段階'),
                     step_count=sum(c['page_count'] for c in cases if c.get('page_unit')=='段階'))
    dump('data/project-workflows.json', workflows)
    print(str(sum(bool(p['example_ids']) for p in profiles)) + ' repositories with Japanese outputs; ' + str(len(cases)) + ' decks. Curated site is built separately.')

if __name__ == '__main__':
    main()
