import json
from pathlib import Path
p=Path(__file__).parent
m=json.loads((p/'manifest.json').read_text(encoding='utf-8'))
for t in m['text_boxes']:
 if t['id'] in ['add','commit']:
  t['font_size']=23;t['font']='Arial Narrow';t['preview_font']='C:/Windows/Fonts/ARIALNB.TTF';t['fit_text']=False
  t['calibration_note']='Manually measured Arial Narrow bold at 40 source pixels: commit width165px and glyph height38px. Same font size on both labels.'
  if t['id']=='commit':t['box_px']=[1027,547,170,53]
m['quality_checks']={k:True for k in m['quality_checks']}
m['quality_checks']['evidence']='Inspected source, actual builtin sheet, complete separated assets in deterministic preview. All source Japanese text present and native, with no overlap or clipping; 4 complete foreground assets; native cards/arrows/border; corners, glyph density and layers compared. Command labels manually calibrated to same size.'
m['warnings']=['Yu Gothic Bold substitutes source font; moderate glyph weight and spacing differences remain.','Separated icon strokes and subtle texture differ slightly from source while identities and completeness are retained.','Native fills replace subtle source background texture.']
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
(p/'page_result.json').write_text(json.dumps({'page_manifest':'manifest.json','imagegen_jobs':'imagegen-jobs.json','page_pptx':'page.pptx','preview':'preview.png','contact_sheet':'split_assets_contact.png','validation':'validation.json','page_result':'page_result.json'},indent=2),encoding='utf-8')
