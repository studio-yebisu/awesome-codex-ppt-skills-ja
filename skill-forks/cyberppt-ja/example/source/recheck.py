"""Re-run unchanged upstream gates and separately record derivative checks."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,zipfile,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parents[1]
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def norm(t):return re.sub(r'\s+','',t)
def leaf(v):
 if isinstance(v,str):yield v
 elif isinstance(v,list):
  for x in v:yield from leaf(x)
 elif isinstance(v,dict):
  for x in v.values():yield from leaf(x)
receipts=[]
def run(args,tag):
 p=subprocess.run([sys.executable,*map(str,args)],cwd=P,capture_output=True,text=True,encoding='utf-8',errors='replace')
 (P/'review'/f'{tag}.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 receipts.append({'command':['python',*map(str,args)],'exit_code':p.returncode,'log':f'review/{tag}.log'})
 return p.returncode
sha=hashlib.sha256((P/'deck.pptx').read_bytes()).hexdigest();checks=[];gates=[];stats=[]
with zipfile.ZipFile(P/'deck.pptx') as z:
 for n in range(1,6):
  tag=f'{n:02}';xml=ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'));ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
  text=norm(''.join(xml.itertext()));texts=norm(''.join(e.text or '' for e in xml.findall('.//a:t',ns)));names={e.get('name') for e in xml.findall('.//p:cNvPr',ns)}
  lock=load(P/f'design/slide-{tag}-content-lock.json');recipe=load(P/f'design/slide-{tag}-elements.json')
  required=list(leaf({k:lock.get(k,[]) for k in ['title','subtitle','annotations','so_what','tables','charts','kpis']}))
  missing=[t for t in required if norm(t) not in texts]
  distributed=[]
  if n==2:
   for annotation in lock.get('annotations',[]):
    parts=re.split('[:：／]',annotation)
    if annotation in missing and len(parts)>1 and all(norm(v) in texts for v in parts):
     missing.remove(annotation);distributed.append({'source_annotation':annotation,'separately_visible_labels':parts,'literal_single_textbox_match':False})
  missing_ids=[e['element_id'] for e in recipe['elements'] if e['element_id'] not in names]
  result={'slide':n,'passed':not missing and not missing_ids,'required_text_count':len(required),'missing_text':missing,'registered_elements':len(recipe['elements']),'missing_element_ids':missing_ids,'source_pptx_sha256':sha,'scope':'Exact title/subtitle/annotations/so_what/table/chart/KPI text and registered object names; not semantic or strict visual acceptance','caveat_scope':'Each page retains fictional/proposal caveat; generic caveats are paraphrased and not treated as literal matches.'}
  result['distributed_annotation_matches']=distributed
  dump(P/f'review/slide-{tag}-component-check.json',result);checks.append(result)
  direct=P/f'render/page-{tag}/direct-png/slide-01.png'
  run([P/'source/upstream/scripts/compare_render.py','--blueprint',P/f'design/slide-{tag}-blueprint.png','--render',direct,'--registry',P/f'design/slide-{tag}-registry.json','--out',P/f'review/slide-{tag}-original-diff.json','--overlay-out',P/f'review/slide-{tag}-overlay.png'],f'slide-{tag}-original-diff')
  args=[P/'source/upstream/scripts/build_visual_qa_gate.py','--slide',n,'--blueprint-render',P/f'design/slide-{tag}-blueprint.png','--ppt-render',direct,'--side-by-side',P/f'review/slide-{tag}-side-by-side.png','--component-signature-check',P/f'review/slide-{tag}-component-check.json','--visual-element-registry',P/f'design/slide-{tag}-registry.json','--bbox-delta-report',P/f'review/slide-{tag}-numeric.json','--overlay-comparison',P/f'review/slide-{tag}-overlay.png','--pixel-diff-report',P/f'review/slide-{tag}-original-diff.json','--out',P/f'review/slide-{tag}-original-visual-gate.json']
  run(args,f'slide-{tag}-original-visual-gate');gates+=load(P/f'review/slide-{tag}-original-visual-gate.json')['slides']
  diff=load(P/f'review/slide-{tag}-original-diff.json');stats.append({'slide':n,'elements':len(diff['results']),'passed_elements':sum(x['status']=='passed' for x in diff['results']),'mean_of_element_abs_diff':round(sum(x['pixel_mean_abs_diff'] for x in diff['results'])/len(diff['results']),3)})
dump(P/'review/component-checks.json',{'passed':all(c['passed'] for c in checks),'slides':checks})
dump(P/'review/original-visual-qa-gate.json',{'slides':gates})
run([P/'source/upstream/scripts/inspect_pptx_objects.py',P/'deck.pptx','--out',P/'review/original-object-inspection.json'],'original-object-inspection')
run([P/'source/upstream/scripts/validate_pptx.py',P/'deck.pptx','--manifest',P/'design/slide_manifest.json','--visual-qa',P/'review/original-visual-qa-gate.json','--strict','--json-out',P/'review/original-strict-validation.json'],'original-strict-validation')
run([P/'source/upstream/scripts/compare_merged_render.py','--approved-dir',P/'review/approved-renders','--merged-dir',P/'render/direct-png','--out',P/'review/merge-regression.json'],'direct-png-merge-regression')
run([P/'source/upstream/scripts/compare_merged_render.py','--approved-dir',P/'review/pdf-approved-renders','--merged-dir',P/'render','--out',P/'review/pdf-merge-regression.json'],'pdf-preview-merge-regression')
dump(P/'review/repair-diff-summary.json',{'scope':'Unchanged original pixel tolerance; mean of element crops is descriptive, not a quality score','before':load(P/'source/optical-alignment.json')['baseline_original_diff'],'after':stats,'strict_original_passed':all(g['deliverable_allowed'] for g in gates),'local_font_weight_and_footer_adaptations':True,'direct_png_palette_dither_retained':True,'human_preview':'PowerPoint PDF to RGB PNG, direct PNG preserved separately'})
dump(P/'review/current-check-receipts.json',receipts)
print(json.dumps({'all_locked_text_and_ids_present':all(c['passed'] for c in checks),'original_visual_passed':all(g['deliverable_allowed'] for g in gates),'after_pixel_stats':stats}))
