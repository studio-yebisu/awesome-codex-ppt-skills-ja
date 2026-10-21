"""Native legibility repair, retaining original generated images and reconstruction."""
from pathlib import Path
import json,os,shutil,subprocess,sys
p=Path(__file__).resolve().parents[1]
private=p/'.private/text-layout-repair';private.mkdir(parents=True,exist_ok=True)
for sid in ['reduce-steps','targets-and-order']:
 q=p/'slides'/sid/'work/semantic-map.json';backup=private/(sid+'.json')
 if not backup.exists():shutil.copy2(q,backup)
 d=json.loads(q.read_text(encoding='utf-8'))
 if sid=='targets-and-order':
  d['entities']=[e for e in d['entities'] if not e['id'].startswith('metric-unit-')]
  for i,value in enumerate(['4操作','90%','60秒']):
   e=next(e for e in d['entities'] if e['id']==f'metric-{i}');e['text']=value;e['bbox_hint']=[[85,285,423,190],[604,285,386,190],[1116,285,410,190]][i];e['style_hint'].update(font_family='BIZ UDPGothic',target_font_size_px=152,alignment='center')
  hp=q.with_name('reconstruction-handoff.json');hb=private/'targets-handoff.json'
  if not hb.exists():shutil.copy2(hp,hb)
  handoff=json.loads(hp.read_text(encoding='utf-8'))
  for i,unit in enumerate(['操作','%','秒']):
   combined=next(e for e in d['entities'] if e['id']==f'metric-{i}')
   assert unit in combined['text']
   obligation=next(o for o in handoff['content_obligations'] if o['id']==f'preserve-metric-unit-{i}')
   obligation['entity_ids']=[f'metric-{i}']
   obligation['description']=f'Preserve {unit} in the combined native text {combined["text"]}; number and unit share one allocation after legibility repair.'
  hp.write_text(json.dumps(handoff,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 else:
  for i in range(8):
   x=269.71+i*156;y=371.09;w=180;h=107.12;notch=24
   e=next(e for e in d['entities'] if e['id']==f'old-step-{i}');e['bbox_hint']=[x,y,w,h]
   pts=[[x,y],[x+w-notch,y],[x+w,y+h/2],[x+w-notch,y+h],[x,y+h]]+([[x+notch,y+h/2]] if i else [])
   e['path_commands_px']=[{'op':'M' if k==0 else 'L','point':xy} for k,xy in enumerate(pts)]+[{'op':'Z'}]
   t=next(e for e in d['entities'] if e['id']==f'old-label-{i}');t['bbox_hint']=[x+(15 if i==0 else 27),398.83,126,54.52];t['style_hint'].update(alignment='center',target_font_size_px=30)
 q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cli=p/'runtime/slidepoise/scripts/slidepoise_runtime.py';receipts=[]
for sid in ['reduce-steps','targets-and-order']:
 work=p/'slides'/sid/'work';cmd=[sys.executable,str(cli),'reconstruct-slide','--image',str(work/'accepted-slide.png'),'--semantic-map',str(work/'semantic-map.json'),'--upstream-handoff',str(work/'reconstruction-handoff.json'),'--config',str(p/'work/reconstruction-config.json'),'--slide-id',sid,'--output-dir',str(work/'reconstruction')]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');receipts.append({'slide':sid,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,r.stderr
r=subprocess.run([sys.executable,str(cli),'render-deck','--manifest',str(p/'work/deck-scenes.json'),'--output',str(p/'deck.pptx')],env=dict(os.environ,PYTHON=sys.executable),capture_output=True,text=True,encoding='utf-8');receipts.append({'stage':'original-render-deck','exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,r.stderr
(p/'source/text-layout-repair.json').write_text(json.dumps({'author':'Codex','changes':['Metric and unit combined into one native text allocation per metric','Uniform old-stage chevrons with inner label padding','Original generated targets retained; explicit native legibility adaptation, no pixel-identity claim.'],'calls':receipts},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Original reconstruction and renderer succeeded after native text/chevron repairs.')
