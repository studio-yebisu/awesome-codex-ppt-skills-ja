"""Preserve internal trial, then use SciDiagram's original portable template."""
from pathlib import Path
import shutil, json

ROOT=Path(__file__).resolve().parents[4]
CASE=ROOT/'examples/repositories/sci-diagram-showcase'
FORK=ROOT/'skill-forks/sci-diagram-ja'
HISTORY=ROOT/'.build/sci-diagram-internal-trial-20261014'
HISTORY.mkdir(parents=True,exist_ok=True)
def move_owned(p,label):
    if not p.exists():return
    assert p.resolve().is_relative_to(ROOT.resolve()),p
    dest=HISTORY/label;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():raise RuntimeError('Refusing historical overwrite: '+str(dest))
    shutil.move(str(p),str(dest))
for folder,label in [(CASE,'example'),(FORK,'skill')]:
    for name in ['dependencies/pptx-authoring-runtime','upstream/source-artifact-example.mjs','upstream/references/runtime-artifact-tool.md','source/build.mjs','source/deck.pptx','source/deck.pptx.inspect.ndjson','source/build.log','source/finish_package.py','deck.pptx','render','PROVENANCE.json','QA.json','SOURCE.json','README.md','SKILL.md']:
        move_owned(folder/name,label+'/'+name)
for name in ['sci-diagram-example-ja.zip','sci-diagram-ja.zip']:
    move_owned(ROOT/'downloads'/name,'prior-internal-packages/'+name)
shutil.copy2(ROOT/'tools/build_sci_diagram_showcase.py',HISTORY/'build-internal-trial.py')
data=json.loads((CASE/'source/input.json').read_text(encoding='utf-8'))
# Keep all scientific relationships; standard native rects replace custom
# terrain polygons under the portable phase-one geometry contract.
p=data[-1]
nodes=p['NODES']
land=next(n for n in nodes if n['id']=='land')
land.update(type='rect',bounds=[63,320,1218,640]);land.pop('points',None)
sat=next(n for n in nodes if n['id']=='saturated-zone')
sat.update(type='rect',bounds=[63,450,1218,640]);sat.pop('points',None)
river=next(n for n in nodes if n['id']=='river')
river.update(bounds=[853,450,973,478])
notch={'id':'stream-channel','type':'rect','text':'','bounds':[853,340,973,450],'fill':p['bg']}
nodes.insert(nodes.index(river),notch)
for e in p['EDGES']:
    if e['id']=='groundwater-to-river':e['points']=[[450,543],[780,543],[887,475]]
    if e['id']=='river-callout':e['points']=[[948,425],[948,450]]
(CASE/'source/input.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(CASE/'input/diagram-map.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Internal trial preserved under '+str(HISTORY))
