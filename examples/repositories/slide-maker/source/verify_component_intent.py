"""Check the original gate's acceptance of explicit numeric-array intent.

The geometry detector still reports exit 2. This verifies only its documented
per-slide waiver path, not the independent critic or the full delivery gate.
"""
from pathlib import Path
import hashlib, json, sys

CASE = Path(__file__).resolve().parents[1]
SCRIPTS = CASE/'source/upstream/skills/slide-maker/scripts'
sys.path.insert(0, str(SCRIPTS))
import codex_delivery_gate as gate

def main():
    load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
    evidence=load(CASE/'.codex-deck-evidence.json')
    components=load(CASE/'source/current-components.json')
    errors=[]
    calls,_=gate.parse_script(CASE/'source/build_slide_maker_repository_example.py',errors)
    rows={r['slide']:r for r in evidence['design']['slides']}
    gate.check_components(evidence,components,rows,calls,errors)
    result={'scope':'Original check_components only; full delivery and critic gates remain separate.',
        'pptx_sha256':hashlib.sha256((CASE/'deck.pptx').read_bytes()).hexdigest(),
        'original_checker':'source/upstream/skills/slide-maker/scripts/codex_delivery_gate.py',
        'detector_still_actionable':len(components['actionable']),
        'explicit_accepted_intents':[{'slide':c['slide'],'pattern':c['pattern'],
            'accepted_by_original_waiver_function':gate.waived(evidence,'component',slide=c['slide'],pattern=c['pattern'])}
            for c in components['clusters'] if c.get('suggest')],
        'component_intent_errors':errors,'component_intent_passed':not errors,
        'full_delivery_pass_claimed':False}
    (CASE/'source/component-intent-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
