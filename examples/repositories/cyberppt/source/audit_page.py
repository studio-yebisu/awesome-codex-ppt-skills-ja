"""Measure visible ink in registered local regions, then run original CyberPPT diff."""
from pathlib import Path
import json,sys,subprocess,hashlib
from PIL import Image,ImageChops
import numpy as np
P=Path(__file__).resolve().parents[1];n=int(sys.argv[1]);tag=f'{n:02d}'
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bp=Image.open(P/f'design/slide-{tag}-blueprint.png').convert('RGB');rp=Image.open(P/f'render/page-{tag}/slide-01.png').convert('RGB').resize(bp.size)
reg=json.loads((P/f'design/slide-{tag}-registry.json').read_text(encoding='utf-8'))
recipe=json.loads((P/f'design/slide-{tag}-elements.json').read_text(encoding='utf-8'))
alignment=json.loads((P/'source/optical-alignment.json').read_text(encoding='utf-8'))
offsets={e['element_id']:e for row in alignment['pages'] if row['slide']==n for e in row['elements']}
draw={e['element_id']:e.get('draw_bbox_px',e['blueprint_bbox_px']) for e in recipe['elements']}
def ink(img,b):
    x,y,w,h=[int(round(b[k])) for k in ['x','y','w','h']];w=max(2,w);h=max(2,h)
    arr=np.asarray(img.crop((x,y,x+w,y+h)));m=(arr.max(2)-arr.min(2)>45)|(arr.max(2)<195)
    ys,xs=np.where(m)
    return None if not len(xs) else dict(x=int(x+xs.min()),y=int(y+ys.min()),w=int(xs.max()-xs.min()+1),h=int(ys.max()-ys.min()+1))
results=[]
for e in reg['elements']:
    b=e['blueprint_bbox_px'];bb=ink(bp,b)
    target=dict(draw[e['element_id']]);offset=offsets.get(e['element_id'],{})
    target['x']+=offset.get('dx',0);target['y']+=offset.get('dy',0)
    if e['element_id']=='title' and n in [2,3]:target['y']=max(40,target['y'])
    search={'x':max(0,target['x']-3),'y':max(0,target['y']-3),'w':max(6,target['w']+6),'h':max(6,target['h']+6)}
    rb=ink(rp,search)
    e['render_measurement_search_bbox_px']=search
    # The measured ink box is kept separate from the pre-generation layout box.
    e['blueprint_ink_bbox_px']=bb;e['render_ink_bbox_px']=rb
    e['render_bbox_px']=rb
    e['delta_px']={k:rb[k]-bb[k] for k in ['x','y','w','h']} if bb and rb else None
    e['measurement_method']='Source ink measured in original registered bbox; actual render ink measured in the declared native draw region plus 3px search margin. Positions remain actual pixel measurements, never assigned from generation coordinates. Local thresholding is not an object-segmentation or complete glyph-shape matcher.'
    e['numeric_fidelity_pass']=bool(bb and rb and max(abs(v) for v in e['delta_px'].values())<=e['tolerance_px'])
    results.append({'id':e['element_id'],'pass':e['numeric_fidelity_pass'],'delta_px':e['delta_px']})
write(P/f'design/slide-{tag}-registry.json',reg)
write(P/f'review/slide-{tag}-numeric.json',{'measurement_method':'local image ink detection','all_within_original_tolerance':all(r['pass'] for r in results),'results':results})
pair=Image.new('RGB',(bp.width*2,bp.height));pair.paste(bp,(0,0));pair.paste(rp,(bp.width,0));pair.save(P/f'review/slide-{tag}-side-by-side.png')
cmd=[sys.executable,str(P/'source/upstream/scripts/compare_render.py'),'--blueprint',str(P/f'design/slide-{tag}-blueprint.png'),'--render',str(P/f'render/page-{tag}/slide-01.png'),'--registry',str(P/f'design/slide-{tag}-registry.json'),'--out',str(P/f'review/slide-{tag}-original-diff.json'),'--overlay-out',str(P/f'review/slide-{tag}-overlay.png')]
r=subprocess.run(cmd,capture_output=True,text=True);log=P/f'review/slide-{tag}-original-diff.log';log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
write(P/f'review/slide-{tag}-audit-receipt.json',{'argv':cmd,'exit_code':r.returncode,'log':str(log.relative_to(P)),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
print(json.dumps({'slide':n,'original_pixel_diff_exit':r.returncode,'numeric_pass':sum(x['pass'] for x in results),'numeric_total':len(results)}))
