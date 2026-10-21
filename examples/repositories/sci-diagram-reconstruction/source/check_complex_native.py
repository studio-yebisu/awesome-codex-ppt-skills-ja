"""Check the published concept example's native objects; not an arbitrary SCI validator."""
from pathlib import Path
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

C = Path(__file__).resolve().parents[1]
NS = {'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}

def check(pptx):
    with zipfile.ZipFile(pptx) as archive:
        slides = [n for n in archive.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        if len(slides) != 1:
            raise ValueError('This saved example must contain exactly one slide')
        root = ET.fromstring(archive.read(slides[0]))
    shapes = root.findall('.//p:sp', NS)
    pictures = root.findall('.//p:pic', NS)
    by_name = {s.find('p:nvSpPr/p:cNvPr', NS).get('name'):s for s in shapes}
    texts = [''.join(t.text or '' for t in s.findall('.//a:t',NS)) for s in shapes if s.find('p:txBody',NS) is not None]
    bidir = by_name.get('Edge:exchange-x-xr:segment-1')
    if bidir is None:
        # The one-segment helper names the object without a segment suffix.
        bidir = by_name.get('Edge:exchange-x-xr')
    failures = []
    if len(shapes)!=23 or len(texts)!=12 or len(pictures)!=1:
        failures.append('Expected 23 native shapes (including 12 text shapes) and one cropped picture')
    if 'X' not in texts or 'X·R' not in texts:
        failures.append('Native species labels missing')
    if bidir is None:
        failures.append('Bidirectional native edge missing')
    else:
        line = bidir.find('p:spPr/a:ln',NS)
        if line is None or any(line.find('a:'+end,NS) is None or line.find('a:'+end,NS).get('type')!='triangle' for end in ('headEnd','tailEnd')):
            failures.append('Bidirectional edge must retain both terminal arrowheads')
    dashed=[]
    for i in range(1,4):
        name=f'Edge:regulation-u-b:segment-{i}'
        shape=by_name.get(name)
        line=shape.find('p:spPr/a:ln',NS) if shape is not None else None
        if line is None:
            failures.append(name+' missing')
            continue
        dash=line.find('a:prstDash',NS)
        head=line.find('a:headEnd',NS)
        tail=line.find('a:tailEnd',NS)
        row={'name':name,'dash':None if dash is None else dash.get('val'),
             'head':None if head is None else head.get('type'), 'tail':None if tail is None else tail.get('type')}
        dashed.append(row)
        if row['dash']!='dash' or row['head'] not in (None,'none') or row['tail']!=('triangle' if i==3 else 'none'):
            failures.append(name+' dash/terminal direction differs')
    crop=pictures[0].find('p:blipFill/a:srcRect',NS) if pictures else None
    expected_crop={'l':'73875','r':'7625','t':'38556','b':'38556'}
    if crop is None or crop.attrib!=expected_crop:
        failures.append('Raster inset crop differs')
    if '参考パネル' in texts:
        failures.append('Raster-owned internal label duplicated as native text')
    if root.findall('.//p:cxnSp',NS):
        failures.append('Unexpected attached connector; this example uses separate native lines')
    # Fixed pass04 source geometry, not a generic SCI acceptance threshold.
    expected_radii={'Node:region-omega':'3019','Node:condition-u':'15000',
                    'Node:compartment-a':'3636','Node:compartment-b':'3636',
                    'Node:species-x':'49999','Node:species-xr':'49999'}
    radii={}
    for name,expected in expected_radii.items():
        shape=by_name.get(name)
        geometry=shape.find('p:spPr/a:prstGeom',NS) if shape is not None else None
        adjustment=geometry.find('a:avLst/a:gd',NS) if geometry is not None else None
        value=None if adjustment is None else adjustment.get('fmla')
        radii[name]={'preset':None if geometry is None else geometry.get('prst'),'adjustment':value}
        if geometry is None or geometry.get('prst')!='roundRect' or value!='val '+expected:
            failures.append(name+' saved pass04 radius differs')
    triangles=[]
    for shape in shapes:
        for end in ('headEnd','tailEnd'):
            arrow=shape.find('p:spPr/a:ln/a:'+end,NS)
            if arrow is not None and arrow.get('type')=='triangle':
                triangles.append({'shape':shape.find('p:nvSpPr/p:cNvPr',NS).get('name'),
                                  'end':end,'width':arrow.get('w'),'length':arrow.get('len')})
                if arrow.get('w')!='lg' or arrow.get('len')!='lg':
                    failures.append('Saved pass04 triangle must retain lg/lg size')
    if len(triangles)!=3:failures.append('Expected three saved pass04 terminal triangles')
    return {'status':'pass' if not failures else 'fail','pptx_sha256':hashlib.sha256(pptx.read_bytes()).hexdigest(),
            'native_shapes':len(shapes),'native_text_shapes':len(texts),'pictures':len(pictures),
            'native_text':texts,'triangle_heads':triangles,'rounded_geometry':radii,'dashed_segments':dashed,'picture_srcRect':None if crop is None else crop.attrib,
            'failures':failures,'scope':'Saved example structure only; not visual quality, scientific correctness, grouping or automatic connector routing.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--pptx',type=Path,default=C/'complex-example/pass-04/editable.pptx')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=check(args.pptx)
    value=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(value,encoding='utf-8')
    print(value,end='')
    raise SystemExit(0 if result['status']=='pass' else 1)
