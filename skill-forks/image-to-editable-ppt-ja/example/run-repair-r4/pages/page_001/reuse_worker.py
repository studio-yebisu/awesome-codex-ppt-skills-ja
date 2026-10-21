"""Recover this dispatched page from hash-checked assets; use original build commands."""
from pathlib import Path
import hashlib,json,shutil,subprocess,os,sys
C=Path(__file__).resolve().parent;CASE=C.parents[2];OLD=CASE/'run-repair/pages/page_001'
U=CASE/'source/upstream/skills/image-to-editable-ppt';receipts=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text('utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
request=read(C/'page_request.json');prior=read(OLD/'page_request.json')
for key in ['source_size_px','slide','content_box','image_backend']:assert request[key]==prior[key],key
assert sha(C/'source.png')==sha(OLD/'source.png')=='653627b29ffe866f46702b864b88332ea06eff32ab1309e177a114455ccf9618'
old_validation=read(OLD/'validation.json');assert old_validation['passed'] is True
required=['manifest.json','imagegen-jobs.json','page.pptx','preview.png','split_assets_contact.png','validation.json','page_result.json']
previous={p:sha(OLD/p)for p in required}
manifest=read(OLD/'manifest.json');assert len(manifest['text_boxes'])==9 and len(manifest['shapes'])==9 and len(manifest['images'])==3
jobs=read(OLD/'imagegen-jobs.json');evidence=jobs['reuse_evidence'];assert jobs['jobs'][0]['backend']==request['image_backend']['backend_id']=='builtin-imagegen'
assert sha(OLD/'assets/icon-sheet.png')==jobs['jobs'][0]['output_sha256']==evidence['sheet_sha256']
for name,h in evidence['icons'].items():assert sha(OLD/'assets/icons'/name)==h
shutil.copytree(OLD/'assets',C/'assets',dirs_exist_ok=True)
for p in (C/'assets').rglob('*'):
 if p.is_file():assert sha(p)==sha(OLD/p.relative_to(C))
# Preserve original selected-output provenance; only active split-report links become portable.
p=C/'assets/icon-sheet.split-report.json';split=read(p)
split['original_report_sha256']=sha(OLD/'assets/icon-sheet.split-report.json')
split['source']='assets/icon-sheet.asset-sheet-alpha.png'
for row in split['assets']:
 row['path']='assets/icons/'+Path(row['path'].replace('\\','/')).name
 row['source']='assets/icon-sheet.asset-sheet-alpha.png'
write(p,split)
manifest['recovery']={'worker':'/root/repair_core_examples','same_source_sha256':sha(C/'source.png'),'previous_manifest_sha256':previous['manifest.json'],'scope':'Reused successful same-source object decisions/geometry/text/assets. No new OCR, image generation or appearance changes.'}
write(C/'manifest.json',manifest)
jobs['run_id']=request['run_id'];jobs['reuse_evidence_round4']={'previous_run':'run-repair','previous_source_sha256':sha(OLD/'source.png'),'current_source_sha256':sha(C/'source.png'),'previous_imagegen_jobs_sha256':previous['imagegen-jobs.json'],'same_backend_contract':True,'same_inventory_and_canvas':True,'same_font_and_license':{'font_sha256':sha(C/'assets/fonts/BIZUDPGothic-Bold.ttf'),'ofl_sha256':sha(C/'assets/fonts/OFL.txt')},'historical_tool_output_path':'jobs[].source_image is the original selected output, preserved as provenance; active output/alpha/assets/split paths are page-relative.'}
write(C/'imagegen-jobs.json',jobs)
env=dict(os.environ);env['PYTHONPATH']=str(U/'cli')+';'+str(U/'cli/editppt/runtime')
for command in [['page','build',str(C)],['page','contact-sheet',str(C)],['page','validate',str(C),'--report','validation.json']]:
 r=subprocess.run([sys.executable,'-m','editppt.cli']+command,cwd=C,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');name=command[1];log=C/('worker-'+name+'.log');log.write_text(r.stdout+r.stderr,'utf-8');receipts.append({'argv':['python','-m','editppt.cli']+command,'exit_code':r.returncode,'log':log.name,'log_sha256':sha(log)});r.check_returncode()
v=read(C/'validation.json');assert v['passed']is True and v['editable_text_shapes']==9 and v['shape_count']==18 and v['images']==3 and not v['missing_required_text']
write(C/'worker-reuse-receipt.json',{'worker':'/root/repair_core_examples','source_sha256':sha(C/'source.png'),'previous_successful_artifacts':previous,'source_request_backend_inventory_match':True,'reused_assets':{p.relative_to(C).as_posix():sha(p)for p in (C/'assets').rglob('*')if p.is_file()},'commands':receipts,'technical_validation_passed':True,'visual_review':'pending current generated preview/contact inspection','application_render_verified':False})
print(json.dumps({'passed':v['passed'],'texts':v['editable_text_shapes'],'native_shapes_including_text':v['shape_count'],'bitmap_images':v['images'],'preview_equal_previous':sha(C/'preview.png')==sha(OLD/'preview.png')},ensure_ascii=False))
