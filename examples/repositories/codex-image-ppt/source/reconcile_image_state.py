"""Re-record an already generated final image with the unchanged upstream CLI.

This is state reconciliation, not a new dispatch/generation or approval run.
Extra history/binding fields and relative-path normalization are explicit local
metadata adapters; no slide image, PPTX, render, or upstream code is modified.
"""
from pathlib import Path
import copy,hashlib,json,subprocess,sys
from pptx import Presentation
CASE=Path(__file__).resolve().parents[1]
SCRIPTS=CASE/'source/upstream/skills/codex-ppt/scripts'
sys.path.insert(0,str(SCRIPTS))
from slide_run_state import locked_jobs,locked_run_state,find_slide,update_jobs_run_status,now_iso
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def binding():
    deck=Presentation(CASE/'codex-image-ppt.pptx');rows=[]
    for i,s in enumerate(deck.slides,1):
        images=[x for x in s.shapes if x.shape_type==13]
        assert len(images)==1 and len(s.shapes)==1
        h=hashlib.sha256(images[0].image.blob).hexdigest()
        assert h==sha(CASE/f'origin_image/slide_{i:02}.png')
        rows.append({'slide_id':f'slide_{i:02}','final_image':f'origin_image/slide_{i:02}.png','source_sha256':h,'embedded_image_sha256':h,'match':True})
    return {'artifact':'codex-image-ppt.pptx','artifact_sha256':sha(CASE/'codex-image-ppt.pptx'),'slides':rows,'scope':'Image bytes physically read from delivered PPTX; not inferred from state.'}
def main():
    current=binding();expected=load(CASE/'source/imagegen-warning-repair.json')['output_sha256']
    assert current['slides'][2]['embedded_image_sha256']==expected
    jobs=load(CASE/'slide_jobs.json');old=copy.deepcopy(find_slide(jobs,'slide_03'))
    receipt=CASE/'source/state-artifact-reconciliation.json'
    if receipt.exists() and old.get('result',{}).get('final_image_sha256')==expected and jobs.get('artifact_binding')==current:
        print('Current image/state/artifact binding verified; no new generation or record needed.');return
    protected=[CASE/'codex-image-ppt.pptx']+sorted((CASE/'origin_image').glob('slide_*.png'))+sorted((CASE/'render').glob('slide-*.png'))+[CASE/'render/deck.pdf',CASE/'source/imagegen-repair/before-after-page-03.png']
    before_payload={p.relative_to(CASE).as_posix():sha(p)for p in protected}
    before_state={'jobs':sha(CASE/'slide_jobs.json'),'run':sha(CASE/'slide_run_state.json')}
    agent=(old.get('dispatch')or{}).get('agent_id');assert agent=='/root/skill_effect_catalog'
    # The upstream result recorder only accepts dispatched jobs. Reopen the
    # existing dispatch solely for accurate recording of its current output.
    # Keep its actual old timestamp/prompt; do not forge a new generation order.
    with locked_jobs(CASE)as state:
        slide=find_slide(state,'slide_03');slide['status']='dispatched';slide['result']=None;update_jobs_run_status(state)
    cli=SCRIPTS/'record_slide_result.py'
    note='Final warning-legibility image reconciled after generation through original result recorder. Existing dispatch was for the earlier spacing edit; current warning edit had no fresh dispatch. This administrative reopening does not claim dispatch-before-generation or human approval. Image/PPTX/render bytes unchanged.'
    argv=[sys.executable,str(cli),'.','--slide','slide_03','--agent-id',agent,'--backend-used','built-in image_gen.imagegen','--selected-source','origin_image/slide_03.png','--qa-note',note]
    result=subprocess.run(argv,cwd=CASE,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    at=now_iso()
    deviations=[
        {'id':'spacing_generated_before_repair_dispatch','phase':'spacing_edit','generation_at':None,'generation_time_known':False,'generation_before_dispatch':True,'dispatch_at':(old.get('dispatch')or{}).get('dispatched_at'),'generation_source_record':'source/imagegen-repair.json','image_sha256':(old.get('result')or{}).get('final_image_sha256'),'evidence':'Previous result qa_note explicitly recorded candidate-before-refreshed-dispatch.','full_chronological_workflow_claimed':False},
        {'id':'warning_edit_without_new_dispatch','phase':'warning_legibility_edit','generation_at':None,'generation_time_known':False,'generation_tool':'image_gen.imagegen','tool_call_id':load(CASE/'source/imagegen-warning-repair.json')['tool_call_id'],'image_sha256':expected,'new_generation_dispatch_executed':False,'evidence':'source/imagegen-warning-repair.json','full_chronological_workflow_claimed':False}
    ]
    compliance={'scope':'partial_original_workflow','expected_generation_order':['dispatch','image_generation','result_recording'],'observed_repair_order':['spacing_generation','spacing_dispatch_record','spacing_result_record','warning_generation_without_new_dispatch','final_image_artifact_assembly','administrative_final_result_reconciliation'],'deviations':deviations,'human_approval_obtained':False,'multiple_page_workers_used':False,'current_user_delegation':'Autonomous improvement requested; does not retroactively establish missing historical human approvals or worker dispatches.','full_original_workflow_complete':False}
    with locked_jobs(CASE)as state:
        slide=find_slide(state,'slide_03')
        slide.setdefault('repair_history',[]).append({'event':'final_output_reconciled','at':at,'previous_result_image_sha256':(old.get('result')or{}).get('final_image_sha256'),'previous_result_recorded_at':(old.get('result')or{}).get('recorded_at'),'retained_dispatch_at':(old.get('dispatch')or{}).get('dispatched_at'),'recording_method':'unchanged bundled record_slide_result.py','generation_repeated':False,'new_worker_dispatched':False,'historical_deviations':deviations})
        for item in state['slides']:
            value=item.get('result')or{}
            if value:
                value['selected_source']=value['final_image']
                value['selected_source_path_note']='Portable relative alias to byte-identical final image; historical absolute location retained privately, not republished.'
        slide['result']['generation_source_record']='source/imagegen-warning-repair.json'
        slide['result']['recording_role']='administrative_reconciliation_of_existing_generated_output'
        state['artifact_binding']=current;state['workflow_compliance']=compliance
        state['metadata_adapter']='Structured deviation/history/artifact binding and portable selected-source aliases added after unchanged original result recorder.'
    with locked_run_state(CASE)as state:
        state.setdefault('history',[]).append({'event':'final_image_state_artifact_reconciled','at':at,'slide_id':'slide_03','generation_repeated':False,'human_approval_obtained':False,'record':'source/state-artifact-reconciliation.json'})
        state['workflow_compliance']=compliance;state['artifact_binding']=current;state['updated_at']=at
    after_payload={p.relative_to(CASE).as_posix():sha(p)for p in protected};assert before_payload==after_payload
    put(receipt,{'status':'pass','recorded_at':at,'original_script':'source/upstream/skills/codex-ppt/scripts/record_slide_result.py','original_script_sha256':sha(cli),'command':['python','source/upstream/skills/codex-ppt/scripts/record_slide_result.py','.','--slide','slide_03','--agent-id',agent,'--backend-used','built-in image_gen.imagegen','--selected-source','origin_image/slide_03.png','--qa-note','<explicit post-generation reconciliation note>'],'exit_code':result.returncode,'raw_cli_logs_published':False,'state_before_sha256':before_state,'state_after_sha256':{'jobs':sha(CASE/'slide_jobs.json'),'run':sha(CASE/'slide_run_state.json')},'artifact_binding':current,'metadata_adapters':['Existing dispatch reopened only for final result recording; actual old dispatch timestamp/prompt retained.','Bundled recorder writes absolute selected_source; normalized to relative alias without changing selected/output image hashes.','Structured workflow deviation/history/binding fields added through original locked-state helpers.'],'generation_repeated':False,'new_worker_dispatched':False,'human_approval_obtained':False,'protected_payload_before':before_payload,'protected_payload_after':after_payload,'all_protected_payload_bytes_unchanged':True})
    print('Final image state reconciled through original result CLI; image/artifact/render unchanged.')
if __name__=='__main__':main()
