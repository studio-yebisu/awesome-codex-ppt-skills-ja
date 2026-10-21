"""Widen only undersized native text frames using actual PowerPoint measurements.

This is a disclosed post-export adapter. The pinned SVG checker/converter remain
unchanged. Text, font size, baseline, paint and other geometry are preserved.
"""
from pathlib import Path
import hashlib, json, math, zipfile
from lxml import etree as ET

CASE=Path(__file__).resolve().parents[1]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def walk(container,parent):
    for shape in container:
        tag=ET.QName(shape).localname
        if tag not in {'sp','grpSp','cxnSp','graphicFrame','pic'}:continue
        identity=shape.find('.//p:cNvPr',NS)
        path=parent+'/'+identity.get('name')
        yield path,shape
        if tag=='grpSp':yield from walk(shape,path)
def main():
    deck=CASE/'deck.pptx';report=CASE/'source/layout-overflow.json'
    data=json.loads(report.read_text('utf-8-sig'));before=hashlib.sha256(deck.read_bytes()).hexdigest()
    assert data['artifact_sha256']==before
    if not data['issues']:return
    measurements={(r['page'],r['name']):r for r in data['issues']}
    # PowerPoint may flatten transparent nested groups when opening the SVG
    # output. Generated leaf names are unique on each slide; assert that fact.
    by_leaf={(r['page'],r['name'].rsplit('/',1)[-1]):r for r in data['issues']}
    assert len(by_leaf)==len(measurements)
    changes=[]
    with zipfile.ZipFile(deck) as z:parts={n:z.read(n) for n in z.namelist()}
    for page in range(1,9):
        name=f'ppt/slides/slide{page}.xml';root=ET.fromstring(parts[name])
        for path,shape in walk(root.find('p:cSld/p:spTree',NS),f'page-{page}'):
            r=measurements.get((page,path)) or by_leaf.get((page,path.rsplit('/',1)[-1]))
            if not r:continue
            assert r['bound_height']<=r['available_height']+1,'Vertical reflow requires source repair'
            extent=shape.find('p:spPr/a:xfrm/a:ext',NS)
            assert extent is not None
            old=int(extent.get('cx'));new=math.ceil(old*(r['bound_width']+1)/r['width'])
            assert new>old
            extent.set('cx',str(new))
            changes.append({'page':page,'shape':path,'text':r['text'],'old_width_emu':old,'new_width_emu':new,'measured_glyph_width_pt':r['bound_width'],'text_and_baseline_changed':False})
        parts[name]=ET.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    assert len(changes)==len(measurements)
    temp=deck.with_suffix('.fitting.pptx')
    with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in parts.items():z.writestr(n,b)
    temp.replace(deck)
    output=CASE/'review/text-frame-fit.json';output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({'adapter':'Actual PowerPoint glyph bounds widen native text-frame extents only; original source/converter/checker unchanged','source_pptx_sha256':before,'artifact_sha256':hashlib.sha256(deck.read_bytes()).hexdigest(),'changed_frames':len(changes),'changes':changes,'claim':'Invisible frame repair; actual pre/post render comparison required separately'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Widened {len(changes)} native frames; original glyph layout preserved')
if __name__=='__main__':main()
