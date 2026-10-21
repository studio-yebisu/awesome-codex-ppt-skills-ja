import pathlib,zipfile,json,hashlib,posixpath,lxml.etree as E
b=pathlib.Path(__file__).resolve().parent.parent;z=zipfile.ZipFile(b/'deck.pptx');t=zipfile.ZipFile(b/'source/native-template-parts.zip');data=json.loads((b/'input/data.json').read_text());ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'};missing=[]
for n in z.namelist():
 if n.endswith('.rels'):
  for e in E.fromstring(z.read(n)):
   if e.get('TargetMode')=='External':continue
   base='' if n=='_rels/.rels' else posixpath.dirname(n).replace('/_rels','');target=posixpath.normpath(posixpath.join(base,e.get('Target')))
   if target not in z.namelist():missing.append(target)
checks={'slide_count':len([n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')])==8,'notes_count':len([n for n in z.namelist() if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml')])==8,'relationship_targets_exist':not missing,'native_master_preserved':z.read('ppt/slideMasters/slideMaster1.xml')==t.read('ppt/slideMasters/slideMaster1.xml'),'native_theme_preserved':z.read('ppt/theme/theme1.xml')==t.read('ppt/theme/theme1.xml'),'rendered_pages':all((b/f'render/slide-{i:02d}.png').exists() for i in range(1,9))}
checks['notes_match_input']=all(s['notes'] in ''.join(E.fromstring(z.read(f'ppt/notesSlides/notesSlide{i+1}.xml')).xpath('//a:t/text()',namespaces=ns)) for i,s in enumerate(data['slides']))
report={'scope':'Additional native template/note checks; original qa_pptx.py and verify_final_qa.py remain separate and required','sha256':hashlib.sha256((b/'deck.pptx').read_bytes()).hexdigest(),'checks':checks,'missing_relationship_targets':missing,'visual_acceptance_not_inferred':True}
(b/'source/template-native-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(checks));assert all(checks.values())
