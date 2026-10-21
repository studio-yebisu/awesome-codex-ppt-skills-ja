import json,hashlib,datetime
from pathlib import Path
p=Path('examples/repositories/slide-maker');f=p/'review/supplemental-plan-audit.json'
a=json.loads(f.read_text(encoding='utf-8'));g=json.loads((p/'.deck-gates.json').read_text(encoding='utf-8-sig'));plan=json.loads((p/'design/post-build-plan.json').read_text(encoding='utf-8-sig'))
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
assert plan['content']==g['content'] and plan['design_plan']==g['design_plan']
assert 'not an exhaustive' in g['design_plan']['type_scale_note']
assert 'not a full' in g['design_plan']['supplemental_direction_comparison']['scope']
rows=[x for x in g['blind_read']['findings'] if x['code']=='READ_LEGIBILITY']
assert len(rows)==6 and all(not x.get('refuted') and 'not a refutation' in x['resolution'] for x in rows)
assert sha(p/'deck.pptx')==a['candidate_pptx_sha256']
assert all(sha(p/x['file'])==x['sha256'] for x in a['final_slides_visually_inspected_in_prior_pass'])
for name in list(a['input_hashes']):a['input_hashes'][name]=sha(p/name)
a['input_hashes']['design/post-build-plan.json']=sha(p/'design/post-build-plan.json')
a.setdefault('addenda',[]).append({'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Metadata-only verification; no new visual review. Original findings and audit text retained as history.','verified':['type_scale_note now explicitly declares representative values and additional sizes.','Direction comparison now explicitly limits E to a cover probe, not a full rival deck.','All six READ_LEGIBILITY resolutions accept small-type limitations for selfread and contain no refuted assertion.','Current content and design_plan exactly equal the synchronized post-build-plan.json fields.','PPTX and all five completed render hashes remain unchanged.'],'disposition':'Two metadata concerns addressed; direction-comparison limitation remains but is now explicitly disclosed. Prior independent consent and scope limits unchanged.'})
f.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8');print('Metadata verified; hashes and addendum updated.')
