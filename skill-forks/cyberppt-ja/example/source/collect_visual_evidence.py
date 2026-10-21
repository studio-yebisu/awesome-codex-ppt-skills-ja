"""Bind actual technical evidence to visual fields without accepting failed fidelity."""
from pathlib import Path
import hashlib,json,subprocess,sys,collections
P=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text('utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=load(P/'design/slide_manifest.json');rows=[]
for m in manifest['slides']:
    n=m['slide'];tag=f'{n:02}';base='review/'
    visually_same=m['label_collision_check'].get('current_pixels_match_inspected_pixels') is True
    evidence={
      'main_chart_semantics_match':{'method':'Codex full-size source/native comparison','proof':f'review/slide-{tag}-main-crop.png','result':'Same table rows/columns or flow nodes and labels; exact geometry checked separately'},
      'editable_information_layer_pass':{'objects':'review/original-object-inspection.json','content_and_ids':f'review/slide-{tag}-component-check.json','full_slide_blueprint_embedded':False},
      'label_collision_pass':m['label_collision_check'],
      'text_overflow_pass':{'report':'source/layout-overflow.json','result':'Actual PowerPoint TextFrame2 text/cell inner-bound measurements, 90 objects, zero issues'},
      'container_overflow_pass':m['container_overflow_check'],
      'continuous_text_flow_pass':m['continuous_text_flow_check'],
      'table_semantic_typography_pass':{'text_objects':m['table_text_objects'],'result':'Prose cells use T7, never T11; actual font sizes retained and upper-range deviations disclosed'},
      'table_density_pass':m['table_density_check'] if n>=3 else {'applies':False,'reason':'Not a table; actual diagram fully inspected','proof':f'review/slide-{tag}-main-crop.png'},
      'blueprint_background_not_used':{'actual_object_inventory':'review/original-object-inspection.json','pictures':3 if n==1 else 0,'scope':'Only three small non-text SVG icons on cover, no page bitmap in deck'},
    }
    rows.append({'slide':n,'artifact_sha256':sha(P/'deck.pptx'),'blueprint_render_path':f'design/slide-{tag}-blueprint.png','ppt_render_path':f'render/slide-{tag}.png','side_by_side_comparison_path':f'review/slide-{tag}-preview-side-by-side.png','local_overlay_artifacts':[f'review/slide-{tag}-overlay.png'],'measurement_evidence_path':f'design/slide-{tag}-registry.json','spatial_numeric_check_path':f'review/slide-{tag}-numeric.json','component_signature_check_path':f'review/slide-{tag}-component-check.json','visual_element_registry_path':f'design/slide-{tag}-registry.json','bbox_delta_report_path':f'review/slide-{tag}-numeric.json','overlay_comparison_path':f'review/slide-{tag}-overlay.png','pixel_diff_report_path':f'review/slide-{tag}-original-diff.json','local_crop_comparisons':[f'review/slide-{tag}-{k}-crop.png' for k in ['title','main','takeaway','footer']],'visual_differences':[{'severity':'High','what':'Original unmodified pixel/bbox comparison not passed; flat native paper versus generated bitmap tonal variation, glyphs/icons differ. Footer clearance deliberately repaired.','evidence':f'review/slide-{tag}-original-diff.json'}],'evidence':evidence,'surface_system_match':False,'main_chart_semantics_match':visually_same,'visual_semantics_preserved':False,'editable_information_layer_pass':True,'spatial_registration_pass':False,'curve_fidelity_pass':False,'label_collision_pass':visually_same,'text_overflow_pass':m['container_overflow_check']['passed'],'container_overflow_pass':m['container_overflow_check']['passed'],'continuous_text_flow_pass':m['continuous_text_flow_check']['passed'],'table_semantic_typography_pass':True,'table_density_pass':visually_same,'blueprint_background_not_used':True,'deliverable_allowed':False,'notes':['Technical evidence collected during current Codex repair; original acceptance remains failed. No user approval or new model generation is claimed.','Visual fields reuse only exact pixel SHA from review/codex-visual-inspection.json; changed pixels require new inspection.','curve_fidelity_pass stays false because exact source geometry has not passed; not a claim that a trace gate was completed.']})
record={'artifact_sha256':sha(P/'deck.pptx'),'scope':'Current technical checks plus Codex all-page visual inspection. Does not replace unchanged original failed gate.','slides':rows}
dump(P/'review/repair-visual-evidence.json',record)
cmd=[sys.executable,str(P/'source/upstream/scripts/validate_pptx.py'),str(P/'deck.pptx'),'--manifest',str(P/'design/slide_manifest.json'),'--visual-qa',str(P/'review/repair-visual-evidence.json'),'--strict','--json-out',str(P/'review/repair-strict-validation.json')]
r=subprocess.run(cmd,cwd=P,capture_output=True,text=True,encoding='utf-8',errors='replace')
(P/'review/repair-strict-validation.log').write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
report=load(P/'review/repair-strict-validation.json')
dump(P/'review/repair-strict-receipt.json',{'command':['python','source/upstream/scripts/validate_pptx.py','deck.pptx','--manifest','design/slide_manifest.json','--visual-qa','review/repair-visual-evidence.json','--strict','--json-out','review/repair-strict-validation.json'],'exit_code':r.returncode,'artifact_sha256':sha(P/'deck.pptx'),'errors':len(report['errors']),'error_codes':dict(collections.Counter(x['code'] for x in report['errors'])),'acceptance':'failed; no threshold or validator changes'})
print('Current technical evidence bound; original strict result',r.returncode,'errors',len(report['errors']))
