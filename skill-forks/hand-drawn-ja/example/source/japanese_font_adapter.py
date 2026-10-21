"""Declare Japanese serif fallback only; leave original Latin Georgia intact."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import sys,json,hashlib,xml.etree.ElementTree as E
A='http://schemas.openxmlformats.org/drawingml/2006/main'
def main():
 p=Path(sys.argv[1]);rows=[]
 with ZipFile(p)as z:parts={n:z.read(n)for n in z.namelist()}
 for name,raw in list(parts.items()):
  if not(name.startswith('ppt/slides/slide')and name.endswith('.xml')):continue
  root=E.fromstring(raw);count=0
  for run in root.iter('{'+A+'}rPr'):
   latin=run.find('{'+A+'}latin');ea=run.find('{'+A+'}ea')
   if latin is not None and latin.get('typeface')=='Georgia':
    if ea is None:ea=E.SubElement(run,'{'+A+'}ea')
    ea.set('typeface','Yu Mincho');count+=1
  parts[name]=E.tostring(root,encoding='utf-8',xml_declaration=True);rows.append({'part':name,'Japanese_fallback_runs':count})
 with ZipFile(p,'w',ZIP_DEFLATED)as z:
  for n,v in parts.items():z.writestr(n,v)
 report={'scope':'Derived Japanese glyph fallback only. Original Latin Georgia and label/page Calibri retained. No font files embedded.','pptx_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parts':rows}
 out=p.parent/'source/japanese-font-adapter.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Japanese serif fallback explicitly declared; Latin Georgia retained.')
if __name__=='__main__':main()
