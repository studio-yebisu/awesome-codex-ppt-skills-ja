"""Supplement original checker with exact standard-line/arrow topology evidence."""
from pathlib import Path
import hashlib,json,zipfile
from xml.etree import ElementTree as E
C=Path(__file__).resolve().parents[1]
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=C/'pass-01/editable.pptx';inv=json.loads((C/'input/reconstruction-inventory.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(p)as z:
        root=E.fromstring(z.read('ppt/slides/slide1.xml'));presentation=E.fromstring(z.read('ppt/presentation.xml'))
    size=presentation.find('p:sldSz',NS);sx=int(size.get('cx'))/1600;sy=int(size.get('cy'))/900
    shapes={x.find('p:nvSpPr/p:cNvPr',NS).get('name'):x for x in root.findall('.//p:sp',NS)};rows=[]
    for e in inv['directed_edges']:
        name=f"Edge:{e['id']}:segment-1";s=shapes[name];xf=s.find('p:spPr/a:xfrm',NS);off=xf.find('a:off',NS);ex=xf.find('a:ext',NS);x=int(off.get('x'));y=int(off.get('y'));w=int(ex.get('cx'));h=int(ex.get('cy'));fh=xf.get('flipH')in ['1','true'];fv=xf.get('flipV')in ['1','true'];start=[x+(w if fh else 0),y+(h if fv else 0)];end=[x+(0 if fh else w),y+(0 if fv else h)];points=e['points_px'];expected_start=[round(points[0]['x']*sx),round(points[0]['y']*sy)];expected_end=[round(points[-1]['x']*sx),round(points[-1]['y']*sy)];delta=max(abs(a-b)for a,b in zip(start+end,expected_start+expected_end));geom=s.find('p:spPr/a:prstGeom',NS);tail=s.find('p:spPr/a:ln/a:tailEnd',NS);head=s.find('p:spPr/a:ln/a:headEnd',NS)
        row={'edge_id':e['id'],'native_object_name':name,'ooxml_container':'p:sp','preset_geometry':geom.get('prst'),'from_node':e['from'],'to_node':e['to'],'source_start_px':points[0],'source_target_px':points[-1],'actual_start_emu':start,'actual_target_emu':end,'maximum_coordinate_error_emu':delta,'headEnd_at_source':head.get('type')if head is not None else None,'tailEnd_at_target':tail.get('type')if tail is not None else None,'one_zero_extent_expected_for_axis_aligned_line':(w==0)^(h==0),'shape_attachment_links_present':len(s.findall('.//a:stCxn',NS))+len(s.findall('.//a:endCxn',NS)),'editable_native_line':geom.get('prst')=='line'}
        assert row['editable_native_line']and delta<=5 and row['tailEnd_at_target']=='triangle'and row['headEnd_at_source']in [None,'none']and row['one_zero_extent_expected_for_axis_aligned_line'];rows.append(row)
    report={'status':'pass','pptx':'pass-01/editable.pptx','pptx_sha256':sha(p),'source':'pass-01/source.png','source_sha256':sha(C/'pass-01/source.png'),'input_and_pass_source_bytes_equal':sha(C/'input/source.png')==sha(C/'pass-01/source.png'),'native_standard_lines_verified':len(rows),'p_cxnSp_automatic_connectors':len(root.findall('.//p:cxnSp',NS)),'pictures':len(root.findall('.//p:pic',NS)),'checker_interpretation':'Original checker counts p:cxnSp as connectors and excludes four p:sp lines because their axis-aligned bounds have zero width or height. This does not flatten those standard native line shapes. This supplemental check verifies their preset, endpoint geometry, flips and target tailEnd triangle directly.','attachment_limit':'Lines are separately editable but have no shape-attachment links. Moving a box does not automatically reroute the line.','edges':rows};assert len(rows)==4 and report['pictures']==0 and report['input_and_pass_source_bytes_equal'];(C/'qa/native-line-topology.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Four native standard lines / exact source-target endpoints / target arrowheads verified.')
if __name__=='__main__':main()
