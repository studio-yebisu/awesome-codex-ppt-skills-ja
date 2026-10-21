"""Inspect actual compiler/native output and source-specific schedule geometry."""
from pathlib import Path
import collections,hashlib,json,re,zipfile
from lxml import etree as ET
import pymupdf
CASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','s':'http://www.w3.org/2000/svg'}
rows=[];total=collections.Counter()
with zipfile.ZipFile(CASE/'deck.pptx') as z:
    assert z.testzip() is None
    for i in range(1,9):
        r=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        s=ET.parse(CASE/f'source/svg_output/{i:02}.svg')
        a=[''.join(e.itertext()) for e in s.findall('.//s:text',NS)]
        b=[e.text or '' for e in r.findall('.//a:t',NS)]
        assert collections.Counter(a)==collections.Counter(b),(i,a,b)
        row={'page':i,'native_shapes':len(r.findall('.//p:sp',NS)),'native_text_shapes':sum(bool(e.findall('.//a:t',NS)) for e in r.findall('.//p:sp',NS)),'pictures':len(r.findall('.//p:pic',NS)),'native_charts':len(r.findall('.//a:graphicData[@uri="http://schemas.openxmlformats.org/drawingml/2006/chart"]',NS)),'native_tables':len(r.findall('.//a:tbl',NS)),'all_svg_text_preserved':True,'svg_sha256':sha(CASE/f'source/svg_output/{i:02}.svg')}
        for k in ['native_shapes','native_text_shapes','pictures','native_charts','native_tables']:total[k]+=row[k]
        rows.append(row)
dump(CASE/'source/native-elements.json',{'artifact_sha256':sha(CASE/'deck.pptx'),'totals':dict(total),'slides':rows,'scope':'Actual native OOXML; native_shapes includes text shapes. Tables and schedule are editable SVG-derived text/geometry, not Office Table/Chart.'})
pdf=CASE/'render/deck.pdf';doc=pymupdf.open(pdf)
fonts=[{'page':i+1,'fonts':[{'base_font':f[3],'extension':f[1],'type':f[2],'resource':f[4]} for f in pg.get_fonts(full=True)]} for i,pg in enumerate(doc)]
assert all('BIZ-UDPGothic' in f['base_font'] for pg in fonts for f in pg['fonts'])
dump(CASE/'source/pdf-fonts.json',{'source':'render/deck.pdf','source_sha256':sha(pdf),'method':'Actual PowerPoint PDF font resources from PyMuPDF; BIZ checked in every page','pages':fonts})
logs=json.loads((CASE/'build-log.json').read_text('utf-8'))
calc=[x for x in logs if any(str(v).endswith('svg_position_calculator.py') for v in x['command'])]
assert len(calc)==2 and all(x['returncode']==0 for x in calc)
points=[]
for r in calc:
    points.append([float(m.group(1)) for m in re.finditer(r'^\s*\d+\s+[-\d.]+\s+[-\d.]+\s+([-\d.]+)\s+[-\d.]+\s*$',r['stdout'],re.M)])
assert points==[[310,664,1018],[664,1018,1195]],points
svg=ET.parse(CASE/'source/svg_output/07.svg');g=svg.find('.//s:g[@id="decision-schedule-chartArea"]',NS)
bars=[e for e in g.findall('s:rect',NS) if e.get('height')=='44']
actual=[(float(e.get('x')),float(e.get('width'))) for e in bars]
assert actual==[(310,354),(664,354),(1018,177)],actual
dump(CASE/'review/chart-geometry.json',{'source':'input/data.json schedule: 1-2 / 3-4 / week5','scope':'Original verify-charts Gantt recipe, explicit week-boundary axis 0-5. Row placement is qualitative, only time-axis endpoints are verified quantitatively. This technical receipt is part of the disclosed dedicated replay, not a resumable Quick plan.','object_key':'decision-schedule','mode':'decomposable-calc','marker':'chart-plot-area: object=decision-schedule | 310,250,1195,510','original_calculator_calls':2,'scale_pixels_per_week':177,'start_x':points[0],'end_x':points[1],'svg_x_width':actual,'all_endpoint_coordinates_match':True,'early_final_export_receipts':'build-log.json'})
final=json.loads((CASE/'source/validation/svg_quality_report.json').read_text('utf-8'))
assert final['stage']=='final' and final['summary']['errors']==0
for f in final['source_fingerprint']['files']:assert sha(CASE/'source/svg_output'/f['file'])==f['sha256']
dump(CASE/'source/current-check-receipts.json',{'artifact_sha256':sha(CASE/'deck.pptx'),'pipeline':'source/execution-receipts.json','guard_early_final_calculator_export':'build-log.json','original_final_summary':final['summary'],'original_source_fingerprint_matches':True,'native_text_and_shapes':'source/native-elements.json','actual_fonts':'source/pdf-fonts.json','all_original_svg_text_preserved':True,'original_unchanged_files':['source/upstream/scripts/attribution_guard.py','source/upstream/scripts/svg_quality_checker.py','source/upstream/scripts/svg_to_pptx.py'],'disclosed_adapters':['source/export_with_biz.py adds bundled BIZ to in-memory EA font registry only','source/fit_text_frames.py widens undersized editable native text frames from actual PowerPoint bounds, preserving glyph layout'],'overflow':'source/layout-overflow.json','no_score':True})
print('Actual native/text/font/chart and source-fingerprint checks passed',dict(total))
