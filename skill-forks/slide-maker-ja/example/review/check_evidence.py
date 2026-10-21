from pathlib import Path
import json,hashlib,zipfile,importlib.util,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[4]; base=root/'examples/repositories/slide-maker'
spec=importlib.util.spec_from_file_location('subject',root/'tools/build_slide_maker_repository_example.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
d=json.loads((base/'input/data.json').read_text(encoding='utf-8')); rows=[]
for t in range(1,16):
 a=module.linear_search(d['array'],t);b=module.binary_search(d['array'],t);saved=d['traces'][t-1]
 assert saved['target']==t and a==saved['linear'] and b==saved['binary']
 assert a['index']==b['index']==t-1 and a['comparisons']==t
 lo,hi=1,15;ind=[]
 while lo<=hi:
  mid=(lo+hi)//2;ind.append(mid)
  if mid==t:break
  if mid<t:lo=mid+1
  else:hi=mid-1
 assert ind==b['visited']
 rows.append({'target':t,'linear':a['comparisons'],'binary':b['comparisons'],'binary_visited':b['visited']})
ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart','a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
charts=[]
with zipfile.ZipFile(base/'deck.pptx') as z:
 for name in z.namelist():
  if name.startswith('ppt/charts/chart') and name.endswith('.xml'):
   xml=ET.fromstring(z.read(name)); ss=[]
   for ser in xml.findall('.//c:ser',ns):
    cats=[v.text for v in ser.findall('.//c:cat//c:pt/c:v',ns)]; vals=[float(v.text) for v in ser.findall('.//c:val//c:pt/c:v',ns)]
    ss.append({'name':ser.find('.//c:tx//c:v',ns).text,'categories':cats,'values':vals})
   charts.append({'part':name,'series':ss})
assert len(charts)==1
assert charts[0]['series'][0]['values']==[r['linear'] for r in rows]
assert charts[0]['series'][1]['values']==[r['binary'] for r in rows]
assert all(s['categories']==[str(t) for t in range(1,16)] for s in charts[0]['series'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
e={'deck':'../deck.pptx','pptx_sha256':sha(base/'deck.pptx'),'data_sha256':sha(base/'input/data.json'),'build_script_sha256':sha(root/'tools/build_slide_maker_repository_example.py'),'all_15_traces_reexecuted_and_independently_checked':True,'rows':rows,'charts':charts,'target13':rows[12],'maxima':{'linear':max(r['linear'] for r in rows),'binary':max(r['binary'] for r in rows)},'timing_measured':d['timing_measured'],'sorting_cost_measured':d['sorting_cost_measured'],'render_hashes':{f'slide-{i:02}.png':sha(base/f'render/slide-{i:02}.png') for i in range(1,6)}}
(base/'review/evidence.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(e,ensure_ascii=False))
