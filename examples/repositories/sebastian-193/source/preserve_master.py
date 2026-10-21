import zipfile,pathlib,lxml.etree as E
b=pathlib.Path(__file__).resolve().parent.parent
native=b/'source/native-template-parts.zip'
z=zipfile.ZipFile(b/'generated.pptx');t=zipfile.ZipFile(native);files={n:z.read(n) for n in z.namelist()}
keep=['ppt/slideMasters/slideMaster1.xml','ppt/slideMasters/_rels/slideMaster1.xml.rels','ppt/theme/theme1.xml']
for i in range(1,5):keep += [f'ppt/slideLayouts/slideLayout{i}.xml',f'ppt/slideLayouts/_rels/slideLayout{i}.xml.rels']
keep += [n for n in t.namelist() if n.startswith('ppt/tags/')]
for n in keep:
 if n in t.namelist():files[n]=t.read(n)
ns='http://schemas.openxmlformats.org/package/2006/content-types';r=E.fromstring(files['[Content_Types].xml']);present={e.get('PartName') for e in r}
for n in keep:
 if n.endswith('.xml') and '/_rels/' not in n and '/'+n not in present:
  typ='tags' if '/tags/' in n else 'slideLayout' if 'slideLayouts' in n else 'slideMaster' if 'slideMasters' in n else 'theme'
  E.SubElement(r,'{'+ns+'}Override',PartName='/'+n,ContentType='application/vnd.openxmlformats-officedocument.presentationml.'+typ+'+xml' if typ!='theme' else 'application/vnd.openxmlformats-officedocument.theme+xml')
files['[Content_Types].xml']=E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(b/'deck.pptx','w',zipfile.ZIP_DEFLATED) as out:
 for n,v in files.items():out.writestr(n,v)
z.close();t.close()
(b/'generated.pptx').unlink()

# Original bounded grouping/connector tool; input and output stay distinct.
import subprocess,sys,os
subprocess.run([sys.executable,str(b/'source/upstream/scripts/structure_pptx.py'),str(b/'deck.pptx'),'--plan',str(b/'source/structure-plan.json'),'--output',str(b/'structured.pptx'),'--report',str(b/'source/structure-report.json')],check=True)
import json
r=json.loads((b/'source/structure-report.json').read_text(encoding='utf-8'));r['details']['input']='deck.pptx';r['details']['output']='structured.pptx';(b/'source/structure-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
os.replace(b/'structured.pptx',b/'deck.pptx')
