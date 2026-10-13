from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/skills.json').read_text(encoding='utf-8'))
previews=json.loads((ROOT/'data/previews.json').read_text(encoding='utf-8'))['images']
pins=json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))
actual=ROOT/'data/case-studies.json'
examples=json.loads(actual.read_text(encoding='utf-8')) if actual.exists() else []
profiles={p['repository']:p for p in json.loads((ROOT/'data/repository-guides.json').read_text(encoding='utf-8'))}
records=[]
for project in catalog['skills']:
    repo=project['repo_full_name'];pin=next((s for s in pins if s['repository']==repo),None)
    profile=profiles.get(repo,{})
    records.append(dict(repository=repo,original_project=project,preview=previews.get(repo),
        repository_url='https://github.com/'+repo,
        license=profile.get('license') or (pin['github_license'] if pin else project.get('license')),
        license_checked_at=profile.get('checked_at') or (pin['checked_at'] if pin else None),
        license_evidence=profile.get('source_refs') or (pin['license_evidence'] if pin else []),
        upstream_commit=profile.get('upstream_commit') or (pin['commit'] if pin else None),
        examples=[e for e in examples if e['repository']==repo],
        derived_skills=sorted({e['fork_id'] for e in examples if e['repository']==repo and e.get('fork_id')}),
        generation_status='japanese_cases_generated' if any(e['repository']==repo for e in examples) else 'not_generated_here',
        license_status=profile.get('license_review_status','catalog_only'),
        execution_status=profile.get('execution_status',profile.get('production_status','not_started'))))
(ROOT/'data/project-workflows.json').write_text(json.dumps({'catalog_count':len(catalog['skills']),'case_count':len(examples),'slide_count':sum(e['page_count'] for e in examples),'history':{'withdrawn_examples':'data/actual-examples.json','included_in_current_counts':False},'projects':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"{len(catalog['skills'])} original repositories; {len(examples)} current cases; {sum(e['page_count'] for e in examples)} slides")
