"""Check the applied original chapter recipe, not artistic quality."""
from pathlib import Path
from zipfile import ZipFile
import json,re,hashlib,xml.etree.ElementTree as E
C=Path(__file__).resolve().parents[1];A='http://schemas.openxmlformats.org/drawingml/2006/main';P='http://schemas.openxmlformats.org/presentationml/2006/main';ns={'a':A,'p':P}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 data=json.loads((C/'input/data.json').read_text(encoding='utf-8'));lib=(C/'upstream/hand-drawn-chapter-slides/scripts/illustrations.md').read_text(encoding='utf-8');assets=[];pages=[]
 for i,item in enumerate(data['slides'][1:],1):
  raw=re.search(r'### '+str(item['topic'])+r'\. .*?```svg\s*(.*?)\s*```',lib,re.S).group(1)
  p=C/f'illustrations/chapter-{i:02}.svg';assert p.read_text(encoding='utf-8').strip()==raw
  assets.append({'path':p.relative_to(C).as_posix(),'original_catalog_number':item['topic'],'unchanged_original_svg':True,'sha256':sha(p)})
 with ZipFile(C/'deck.pptx')as z:
  size=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns);assert abs(int(size.get('cx'))/914400-13.333)<.0001 and int(size.get('cy'))==6858000
  for i,item in enumerate(data['slides']):
   r=E.fromstring(z.read(f'ppt/slides/slide{i+1}.xml'));shapes=r.findall('.//p:sp',ns);pics=r.findall('.//p:pic',ns)
   texts=[''.join(x.itertext())for x in []];textrows=[]
   for sp in shapes:
    txt=''.join(sp.find('p:txBody',ns).itertext());textrows.append(txt)
   assert len(pics)==1 and len(shapes)==(2 if i==0 else 3)
   assert item['title'].replace('\n','') in [''.join(x.splitlines())for x in textrows]
   assert r.find('.//p:bgPr/a:solidFill/a:srgbClr',ns).get('val')==item['background']
   expected=[(1,1.8,9,2.1),(12.3,7,.5,.25)]if i==0 else [(1,5,4,.3),(1,5.3,9,1),(12.3,7,.5,.25)]
   for sp,wanted in zip(shapes,expected):
    tr=sp.find('p:spPr/a:xfrm',ns);off=tr.find('a:off',ns);ext=tr.find('a:ext',ns)
    values=[int(off.get('x')),int(off.get('y')),int(ext.get('cx')),int(ext.get('cy'))]
    assert all(abs(v-round(w*914400))<=1 for v,w in zip(values,wanted))
   tr=pics[0].find('p:spPr/a:xfrm',ns);off=tr.find('a:off',ns);ext=tr.find('a:ext',ns)
   wanted=(10.7,1.1,.9,.75)if i==0 else(5,.4,8,5.5)
   assert all(abs(v-round(w*914400))<=1 for v,w in zip([int(off.get('x')),int(off.get('y')),int(ext.get('cx')),int(ext.get('cy'))],wanted))
   runs=r.findall('.//a:rPr',ns)
   for run in runs:
    face=run.find('a:latin',ns).get('typeface');sz=int(run.get('sz'))
    if face=='Georgia':assert run.find('a:ea',ns).get('typeface')=='Yu Mincho' and sz==(5400 if i==0 else 4000) and run.get('b')!='1'
    else:assert face=='Calibri' and sz==1400
   pages.append({'index':i,'native_text_boxes':len(shapes),'illustration_bitmaps':len(pics),'background':item['background'],'original_text_roles_positions_verified':True,'cover_small_mark_only':i==0 if i==0 else None})
 out={'status':'recipe_checks_passed_visual_review_separate','pptx_sha256':sha(C/'deck.pptx'),'original_sources':[{ 'path':p,'sha256':sha(C/'upstream'/p)}for p in ['hand-drawn-chapter-slides/SKILL.md','hand-drawn-chapter-slides/scripts/illustrations.md','LICENSE']],'original_svg_assets':assets,'cover':'New small sparkle SVG follows original permitted organic-Bezier illustration rules; not an original library block.','Japanese_adaptation':'Latin Georgia retained; East Asian run font Yu Mincho. No fonts embedded or redistributed.','pages':pages}
 (C/'source/recipe-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Original four SVGs and all5 native recipe structures checked.')
if __name__=='__main__':main()
