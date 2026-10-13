from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/skills.json').read_text(encoding='utf-8'))
previews=json.loads((ROOT/'data/previews.json').read_text(encoding='utf-8'))['images']
pins=json.loads((ROOT/'data/upstreams.json').read_text(encoding='utf-8'))
actual=ROOT/'data/actual-examples.json'
examples=json.loads(actual.read_text(encoding='utf-8')) if actual.exists() else []
records=[]
for project in catalog['skills']:
    repo=project['repo_full_name'];pin=next((s for s in pins if s['repository']==repo),None)
    records.append(dict(repository=repo,original_project=project,preview=previews.get(repo),
        repository_url='https://github.com/'+repo,
        license=pin['github_license'] if pin else project.get('license'),
        license_checked_at=pin['checked_at'] if pin else None,
        license_evidence=pin['license_evidence'] if pin else [],
        examples=[e for e in examples if e['repository']==repo],
        generation_status='skill_applied' if any(e['repository']==repo for e in examples) else 'not_generated_here'))
(ROOT/'data/project-workflows.json').write_text(json.dumps({'catalog_count':209,'projects':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'209 original repositories; {len(examples)} actual skill-based examples')
