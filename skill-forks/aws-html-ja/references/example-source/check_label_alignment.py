from pathlib import Path
import copy,hashlib,importlib.util,json,xml.etree.ElementTree as ET
from pptx import Presentation
BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('aws_rebuild',BASE/'rebuild.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
prs=Presentation(BASE/'input/deck.pptx');expected=build.layout_adapter().audit_document(prs)['mappings'];mapping={r['label']:r for r in expected}
results=[];changed=[]
for idx,slide in enumerate(prs.slides):
 raw,_=build.native_svg(prs,slide,idx,apply_alignment=False)
 actual=(BASE/f'source/slide-{idx+1:02}.svg').read_text('utf-8')
 a,b=ET.fromstring(raw),ET.fromstring(actual)
 if idx not in (1,2):assert ET.tostring(a)==ET.tostring(b)
 else:
  for before,after in zip(list(a),list(b)):
   name=after.get('data-source-shape')
   if name in mapping:
    assert len(before)==len(after)==1
    bt,at=before[0],after[0];assert at.tag=='text' and at.text==bt.text
    assert float(at.get('x'))==mapping[name]['render_x_px'] and at.get('text-anchor')=='middle'
    normalized=copy.deepcopy(at);normalized.set('x',bt.get('x'));normalized.attrib.pop('text-anchor')
    assert ET.tostring(normalized)==ET.tostring(bt)
    changed.append(name)
   else:assert ET.tostring(before)==ET.tostring(after)
 results.append({'page':idx+1,'result':'passed','geometry_colors_arrows_and_content_preserved':True,'svg_sha256':sha(BASE/f'source/slide-{idx+1:02}.svg')})
assert set(changed)==set(mapping) and len(changed)==15
assert sha(BASE/'input/deck.pptx')=='a57652396782363b3d0b186063e9f80e066030cf8a04f5d67140551de241427a'
report={'status':'passed','kind':'bounded_svg_layout_repair_check','changed_pages':[2,3],'changed_label_count':15,'changed_labels':changed,'only_changed_svg_attributes':['text x','text-anchor'],'input_preserved':True,'input_sha256':sha(BASE/'input/deck.pptx'),'original_extractor_sha256':sha(BASE/'upstream/aws-html-slides/scripts/extract-pptx.py'),'source_generator_sha256':sha(BASE/'rebuild.py'),'html_sha256':sha(BASE/'index.html'),'pages':results,'browser_visual_review':'separate evidence; not claimed by this check','independent_review':False}
(BASE/'source/label-alignment-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
print(json.dumps({'status':report['status'],'changed_labels':len(changed),'pages_checked':len(results)},ensure_ascii=False))
