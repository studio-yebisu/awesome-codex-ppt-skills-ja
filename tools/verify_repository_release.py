"""Read-only release audit for the live repository-led catalog.

Run: python tools/verify_repository_release.py [--case ID] [--catalog-ref 03a2cb0]
Prints a JSON report; writes no files, launches no browser, generates no evidence.
A pending/unknown QA state is never promoted to pass. PNG/XML checks establish
integrity, not typography or artistic approval; recorded full-page review is
required separately. No fixed number of produced repositories/decks is assumed.
"""
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit, unquote, parse_qs
from html.parser import HTMLParser
from collections import Counter
import argparse, base64, hashlib, json, posixpath, re, struct, subprocess, sys, zipfile, zlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
COMPLETE = {'passed', 'verified', 'qa_complete', 'verified_local', 'complete'}
ISSUES, CHECKS, WARNINGS = [], [], []

def read(p): return Path(p).read_text(encoding='utf-8-sig')
def load(p): return json.loads(read(p))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def need(ok, message):
    if not ok: raise AssertionError(message)
def check(label, fn):
    try:
        fn()
        CHECKS.append(label)
    except Exception as exc:
        ISSUES.append({'check': label, 'detail': str(exc)})
def warn(label, detail): WARNINGS.append({'check': label, 'detail': detail})

def local(base, name, must_exist=True):
    need(isinstance(name, str) and bool(name.strip()), 'Missing path')
    url = urlsplit(name)
    need(not url.scheme and not url.netloc, 'Nonlocal artifact path: ' + name)
    decoded = unquote(url.path)
    parts = PurePosixPath(decoded).parts
    need(not decoded.startswith(('/', '\\')) and '\\' not in decoded and '..' not in parts and ':' not in decoded,
         'Unsafe path: ' + name)
    target = (base / decoded).resolve()
    need(target.is_relative_to(ROOT.resolve()), 'Path escapes catalog: ' + name)
    if must_exist: need(target.is_file(), 'Missing file: ' + str(target.relative_to(ROOT)))
    return target

def record_path(folder, name):
    """Older records use catalog-relative paths; newer ones use case-relative paths."""
    if not isinstance(name, str): raise AssertionError('Invalid evidence path: ' + repr(name))
    root_candidate = local(ROOT, name, False)
    case_candidate = local(folder, name, False)
    if case_candidate.is_file(): return case_candidate
    need(root_candidate.is_file(), 'Missing evidence: ' + name)
    return root_candidate

class HTMLFacts(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.scripts=[]; self.ids=[]; self.slides=0; self.lang=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if a.get('id'): self.ids.append(a['id'])
        if tag=='script' and a.get('src'): self.scripts.append(a['src'])
        if tag=='section' and ('slide' in a.get('class','').split() or 'data-marpit-svg' in a): self.slides+=1
        for k in ('href','src','poster'):
            if a.get(k): self.links.append((tag,k,a[k]))


def validate_png(p):
    data=p.read_bytes(); need(data[:8]==b'\x89PNG\r\n\x1a\n', 'Not a PNG: '+str(p))
    pos=8; compressed=bytearray(); dimensions=None; ended=False
    while pos+12<=len(data):
        length=struct.unpack('>I',data[pos:pos+4])[0]; kind=data[pos+4:pos+8]
        need(pos+12+length<=len(data), 'Truncated PNG: '+str(p))
        body=data[pos+8:pos+8+length]; crc=struct.unpack('>I',data[pos+8+length:pos+12+length])[0]
        need(zlib.crc32(kind+body)&0xffffffff==crc, 'PNG CRC failure: '+str(p))
        if kind==b'IHDR': dimensions=struct.unpack('>II',body[:8])
        if kind==b'IDAT': compressed.extend(body)
        pos+=12+length
        if kind==b'IEND': ended=True;break
    need(ended and dimensions and all(dimensions), 'Incomplete PNG: '+str(p))
    need(bool(zlib.decompress(compressed)), 'Empty PNG pixels: '+str(p))
    need(dimensions[0]>=640 and abs(dimensions[0]/dimensions[1]-16/9)<0.035, 'Unexpected page dimensions: '+str(dimensions))
    return dimensions


def catalog(ref, rows):
    original=json.loads(subprocess.check_output(['git','show',ref+':data/skills.json'],cwd=ROOT))
    current=load(ROOT/'data/skills.json')
    need(current==original, 'Original catalog differs from '+ref+' (all fields, descriptions, classifications and owner/repository names)')
    need(len(current['skills'])==209, 'Original catalog is no longer 209 repositories')
    names=[r['repo_full_name'] for r in current['skills']]
    need(len(set(names))==len(names), 'Duplicate original repository')
    need(all(r['repository'] in names for r in rows), 'Case references a repository outside original catalog')
    need(len({r['id'] for r in rows})==len(rows), 'Duplicate case IDs')


def registry(rows):
    raw=load(ROOT/'data/skills.json'); originals={r['repo_full_name']:r for r in raw['skills']}
    workflows=load(ROOT/'data/project-workflows.json'); guides=load(ROOT/'data/repository-guides.json')
    ledger=load(ROOT/'data/production-ledger.json'); grouped={k:[] for k in originals}
    for row in rows: grouped[row['repository']].append(row['id'])
    produced={k for k,v in grouped.items() if v}; pages=sum(r['page_count'] for r in rows)
    need(len(workflows['projects'])==len(originals), 'Workflow repository count mismatch')
    need({p['repository'] for p in workflows['projects']}==set(originals), 'Workflow repositories mismatch')
    for p in workflows['projects']:
        repo=p['repository'];need(p['original_project']==originals[repo], 'Original project metadata altered: '+repo)
        need([x['id'] for x in p['examples']]==grouped[repo], 'Workflow examples mismatch: '+repo)
        if not grouped[repo]: need(p['generation_status'] in {'not_generated_here','not_started','blocked'}, 'Unproduced repository claimed generated: '+repo)
    for record in (workflows,ledger):
        for key,expected in [('catalog_count',len(originals)),('case_count',len(rows)),('slide_count',pages)]:
            need(record.get(key)==expected, key+' differs from canonical case registry')
    need(ledger['produced_repository_count']==len(produced), 'Produced repository count mismatch')
    need(ledger['remaining_repository_count']==len(originals)-len(produced), 'Remaining count mismatch')
    states=ledger['states'];need({r['repository'] for r in states}==set(originals) and len(states)==len(originals), 'Ledger coverage mismatch')
    for record in states:
        expected=grouped[record['repository']]
        need(record['examples']==expected, 'Ledger example list mismatch: '+record['repository'])
        need(record['state'] in ({'generated','qa_complete','produced'} if expected else {'not_started','blocked','not_generated_here','attempted_not_generated'}), 'False/unknown ledger state: '+record['repository'])
        if record['state']=='attempted_not_generated':
            guide=next(g for g in guides if g['repository']==record['repository'])
            attempt=load(local(ROOT,guide['evidence']))
            need(attempt['repository']==record['repository'] and attempt['generated_pages']==0 and not attempt['artifact'],'Attempt does not match the unproduced state')
            need(attempt.get('failed_stage') and attempt.get('reason_ja') and attempt.get('commands_executed'),'Attempt has no concrete execution evidence')
    need({g['repository'] for g in guides}==set(originals) and len(guides)==len(originals), 'Guide coverage mismatch')
    for g in guides:
        expected=grouped[g['repository']]
        need(g.get('example_ids',[])==expected, 'Guide examples mismatch: '+g['repository'])
        if expected:
            need(g.get('steps') and g.get('requirements') and g.get('source_refs'), 'Produced repository guide lacks steps, requirements or source refs: '+g['repository'])
        else:
            need(g.get('production_status') in {'not_started','blocked','not_generated_here','attempted_not_generated'}, 'Unproduced guide claims production: '+g['repository'])
    index=read(ROOT/'index.html')
    count_hits=re.findall(r'この環境で制作したリポ\s*(\d+)件',index)
    need(count_hits and all(int(v)==len(produced) for v in count_hits), 'Site produced-repository number mismatch or absent')
    ratio=re.findall(r'<strong>\s*(\d+)\s*/\s*209\s*</strong>',index)
    need(ratio and all(int(v)==len(produced) for v in ratio), 'Site production ratio mismatch')
    for name in ['guide.html','README.md']:
        doc=read(ROOT/name)
        for value in re.findall(r'(\d+)\s*(?:リポジトリ|リポ)で(?:実際に)?制作',doc):
            need(int(value)==len(produced), 'Outdated produced-repository count in '+name)
    need('data/production-ledger.json' in read(ROOT/'guide.html'), 'Guide has no production ledger link')


def page_paths(row):
    if row.get('pages'): return row['pages']
    # Older HTML cases record their full page list in QA.images instead.
    qpath=local(ROOT,row['qa']); data=load(qpath)
    return [record_path(qpath.parent,i['file']).relative_to(ROOT).as_posix() for i in data.get('images',[])]


def case_manifest(row):
    need(row['repository']==row['skill_repository'], 'Repository identity mismatch')
    need(re.fullmatch(r'[0-9a-f]{40}',row.get('upstream_commit','')), 'Missing full upstream commit')
    n=row['page_count'];need(isinstance(n,int) and n>0,'Invalid page count')
    need(row.get('format') in {'html','pptx'},'Unknown output format')
    need(row.get('preview_kind')==('powerpoint-render' if row['format']=='pptx' else 'html'),'Wrong preview type')
    for key in ['cover','interior','preview','artifact_download','source_download','input','input_data','prompt','provenance','qa','guide']:
        local(ROOT,row.get(key))
    if row.get('fork_download'): local(ROOT,row['fork_download'])
    if row.get('fork_id'):
        source=load(local(ROOT,'skill-forks/'+row['fork_id']+'/SOURCE.json'))
        need(source['repository']==row['repository'] and source['commit']==row['upstream_commit'],'Fork identity/commit mismatch')
    if '?' in row['guide']:
        need(parse_qs(urlsplit(row['guide']).query).get('repo')==[row['repository']],'Guide query points to a different repository')
    need(read(local(ROOT,row['prompt'])).strip()==row['prompt_text'].strip(),'Prompt text differs from downloadable prompt')
    need(len(row['titles'])==len(row['notes'])==n and all(str(v).strip() for v in row['notes']),'Missing titles or per-page notes')
    need(len(set(row['notes']))==n,'Repeated generic per-page notes')
    need(len(page_paths(row))==n and len(set(page_paths(row)))==n,'Explicit page paths missing/duplicate')
    need(row['cover'] in page_paths(row) and row['interior'] in page_paths(row),'Preview image not in actual page set')
    if row.get('input_sha256'):
        p=local(ROOT,row['input_data']);need(row['input_sha256'] in {sha(p),canonical(load(p))},'Input hash mismatch')


def image_set(row):
    paths=[local(ROOT,p) for p in page_paths(row)]
    dimensions=[validate_png(p) for p in paths]
    need(len(set(dimensions))==1,'Page dimensions differ inside deck')
    need(len({sha(p) for p in paths})==len(paths),'Duplicate slide images')
    if len({p.parent for p in paths})==1:
        need(set(paths)==set(paths[0].parent.glob('slide-*.png')),'Extra/missing slide PNGs in render directory')


def provenance(row):
    p=local(ROOT,row['provenance']);folder=p.parent;data=load(p)
    need(data['repository']==row['repository'] and data['upstream_commit']==row['upstream_commit'],'Provenance repository/commit mismatch')
    source=ROOT/'.build/actual-upstreams'/row['repository'].replace('/','__')
    refs=data.get('upstream_files') or data.get('source_refs') or data.get('references')
    need(isinstance(refs,list) and len(refs)>=2,'Missing original source-file evidence')
    for ref in refs:
        path=local(source,ref['path']);need(sha(path)==ref.get('sha256'),'Original source hash changed: '+ref['path'])
    acquisition=source/'ACQUISITION.json'
    if acquisition.exists():need(load(acquisition)['commit']==row['upstream_commit'],'Acquisition pin mismatch')
    inp=local(ROOT,row['input_data'])
    need(data.get('input_sha256') in {sha(inp),canonical(load(inp))},'Provenance input hash absent/stale')
    output=local(ROOT,row['artifact_download'] if row['format']=='pptx' else row['preview'])
    if data.get('artifact_sha256'):need(data['artifact_sha256']==sha(output),'Provenance artifact hash stale')
    elif data.get('output'):need(record_path(folder,data['output'])==output,'Provenance output mismatch')
    else:need(False,'No artifact identity in provenance')
    commands=data.get('commands_executed')
    if commands:
        if row.get('editability')=='raster_slides':
            # Preserve failed attempts; each must have an identical successful retry.
            for i,c in enumerate(commands):
                need(c.get('argv'),'Missing generation command')
                need(sha(record_path(folder,c['log']))==c.get('log_sha256'),'Generation log hash stale')
                if c.get('exit_code')!=0:
                    need(any(later.get('argv')==c['argv'] and later.get('exit_code')==0 for later in commands[i+1:]),'Unresolved failed image generation command')
        elif row.get('editability')=='native_text_shapes_and_bitmap_icons':
            # Recovered source-image processing and annotation failures remain
            # visible. Require an actual successful receipt and hashed log.
            by_log={c.get('log'):c for c in commands}
            for c in commands:
                need(c.get('argv'),'Missing generation command')
                need(sha(record_path(folder,c['log']))==c.get('log_sha256'),'Generation log hash stale')
                if c.get('exit_code')!=0:
                    recovered=by_log.get(c.get('resolved_by_log'))
                    need(recovered and recovered.get('exit_code')==0 and recovered.get('argv') and c.get('resolution_reason'),'Unresolved failed reconstruction command')
        else:
            need(all(c.get('exit_code')==0 and c.get('argv') for c in commands),'Missing/failed generation command')
    elif data.get('execution_log'):
        log=record_path(folder,data['execution_log']);need(log.stat().st_size>20,'Empty execution log')
        if log.suffix=='.json':
            entries=load(log)
            if isinstance(entries,list):
                need(entries,'Empty execution list')
                for e in entries:
                    need(e.get('returncode',e.get('exit_code',0))==0,'Failed native execution')
                    if isinstance(e.get('result'),dict):need(not e['result'].get('isError'),'MCP call returned an error')
    elif data.get('generator'):
        local(ROOT,data['generator'])
        if row['format']=='pptx': need(data.get('render_report'),'Missing PowerPoint execution/render evidence')
        else:
            oldqa=load(local(ROOT,row['qa']))
            need(oldqa.get('browser_review') in {'passed','verified'} and oldqa.get('artifact_sha256')==sha(output),'Missing/stale HTML runtime execution evidence')
    else:
        # Instruction/template skills have no CLI entry point. Require their actual
        # executable authoring source and/or native template evidence, not a fake command.
        source_files=list((folder/'source').glob('*.py'))+list((folder/'source').glob('*.js'))
        native_template=data.get('execution_type')=='instruction_skill_native_template'
        instruction='instruction' in data.get('execution_type','') or data.get('execution_type')=='html_parts_cli'
        need(source_files and (native_template or instruction),'No executed command/log or authored source for instruction route')
        if instruction and data.get('execution_type')=='html_parts_cli':need(list((folder/'source').glob('check-*.log')),'Missing converter/checker execution logs')
    licenses=[f for f in folder.rglob('*') if f.is_file() and ('license' in f.name.lower() or 'ofl' in f.name.lower())]
    need(licenses,'No packaged source/font license notices')
    need(any('license' in f.name.lower() and f.stat().st_size>100 for f in licenses),'Empty upstream license')


def qa(row):
    folder=local(ROOT,row['qa']).parent;data=load(local(ROOT,row['qa']))
    need(data.get('status') in COMPLETE,'QA is pending/unknown/failed: '+str(data.get('status')))
    n=row['page_count'];need(data.get('page_count',data.get('structure',{}).get('slides',n))==n,'QA page count mismatch')
    output=local(ROOT,row['artifact_download'] if row['format']=='pptx' else row['preview'])
    digest=data.get('artifact_sha256') or data.get('html_sha256')
    need(digest and digest==sha(output),'QA artifact hash missing/stale')
    visual=data.get('visual_review')
    if isinstance(visual,dict):
        reviewed=visual.get('pages_reviewed',visual.get('pages'))
        need(reviewed==list(range(1,n+1)),'Visual review does not cover every page')
        if row.get('editability')=='raster_slides':
            need(visual.get('status') in COMPLETE and visual.get('reviewer') and visual.get('findings') and visual.get('source_and_powerpoint_reviewed') is True,'Raster review lacks source and PowerPoint visual findings')
            need('日本語' in ''.join(visual['findings']),'Raster review lacks Japanese image-text legibility finding')
        else:
            need(visual.get('result') and visual.get('method'),'Visual review has no findings/method')
    else:
        need(isinstance(visual,str) and ('all_pages' in visual or '全ページ' in visual),'Full-page visual review not recorded')
    if row['format']=='html':
        browser=data.get('browser_review')
        need(browser and browser not in ['pending','failed','not_run'],'Browser runtime review missing/pending')
    for entry in data.get('images',[]):
        if row.get('editability')=='raster_slides':
            for key in ('source','render'):
                need(entry.get(key+'_sha256')==sha(record_path(folder,entry[key])),'Raster QA '+key+' hash stale')
            need(entry.get('visually_reviewed') is True,'Raster page visual review missing')
        else:
            path=record_path(folder,entry['file'])
            need(entry.get('sha256')==sha(path),'QA screenshot hash stale')


def raster_evidence(row, folder):
    """Validate recorded native generation, without claiming OCR or human approval."""
    n=row['page_count'];p=load(local(ROOT,row['provenance']));q=load(local(ROOT,row['qa']))
    need(p.get('editability')==q.get('editability')=='raster_slides','Raster editability labels disagree')
    need(p.get('raster_content_postprocessing') is False,'Raster postprocessing is not excluded')
    images=p.get('image_records',[])
    need(images==q.get('images') and [i.get('page') for i in images]==list(range(1,n+1)),'Raster source/render records missing or mismatched')
    need([record_path(folder,i['render']) for i in images]==[local(ROOT,v) for v in page_paths(row)],'Raster render records differ from manifest pages')
    need(len({i['source_sha256'] for i in images})==n,'Duplicate source images')
    jobs=load(local(folder,'slide_jobs.json'));state=load(local(folder,'slide_run_state.json'))
    need(jobs.get('run_status')==state.get('status')=='slides_recorded','Image jobs not completed')
    need([s.get('to') for s in state.get('history',[])]==['jobs_prepared','slides_dispatched','slides_recorded'],'Incomplete image job state history')
    style=load(local(folder,'style.json'));need(style.get('visual_direction') and style.get('typography'),'Missing image style')
    spec=load(local(folder,'deck_spec.json'));need(spec,'Missing deck specification')
    requests=load(record_path(folder,p['native_requests']))
    need([r.get('slide') for r in requests]==list(range(1,n+1)),'Missing native image requests')
    need(len(jobs.get('slides',[]))==n,'Image job count mismatch')
    commands=p.get('commands_executed',[])
    required={'prepare_slide_prompts.py','record_slide_dispatch.py','record_slide_result.py','slide_job_status.py','assemble_ppt.py'}
    successful={Path(c['argv'][1]).name for c in commands if c.get('exit_code')==0 and len(c.get('argv',[]))>1}
    need(required<=successful,'Missing successful original image workflow/assembler execution')
    upstream=ROOT/'.build/actual-upstreams'/row['repository'].replace('/','__')
    for name in required:
        original=local(upstream,'skills/codex-ppt/scripts/'+name)
        need(any(c.get('exit_code')==0 and len(c.get('argv',[]))>1 and Path(c['argv'][1]).resolve()==original.resolve() for c in commands),'Command did not execute original script: '+name)
    for i,job,request in zip(images,jobs['slides'],requests):
        source=record_path(folder,i['source']);need(validate_png(source)==tuple(i['dimensions']),'Raster source dimensions mismatch')
        need(job.get('number')==i['page'] and job.get('status')=='recorded' and not job.get('blocker'),'Image job incomplete/out of order')
        result=job.get('result',{});dispatch=job.get('dispatch',{})
        need(sha(record_path(folder,dispatch['prompt']))==dispatch.get('prompt_sha256'),'Dispatched prompt hash stale')
        need(record_path(folder,result['final_image'])==source,'Job output differs from original image')
        need(result.get('selected_source_sha256')==result.get('final_image_sha256')==i['source_sha256']==sha(source),'Generated original image bytes differ')
        need(result.get('sample_generation_method_matched') is True and result.get('qa_note'),'Missing image generation/visual QA evidence')
        need(request.get('tool')=='image_gen.imagegen' and request.get('prompt') and result.get('backend_used')=='built-in image_gen.imagegen','Missing native imagegen execution record')
        need(Path(result['selected_source']).name in request.get('result_output_hint',''),'Native image result identity mismatch')
    return images


def powerpoint(row):
    p=local(ROOT,row['artifact_download']);folder=local(ROOT,row['provenance']).parent;n=row['page_count']
    need(p.suffix.lower()=='.pptx','PPTX artifact extension mismatch')
    raster=row.get('editability')=='raster_slides'
    images=raster_evidence(row,folder) if raster else None
    with zipfile.ZipFile(p) as z:
        need(z.testzip() is None,'Corrupt PPTX package')
        slides=sorted([s for s in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',s)],key=lambda s:int(re.search(r'(\d+)\.xml',s).group(1)))
        notes=[s for s in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',s)]
        need(len(slides)==len(notes)==n,'PPTX page/notes count mismatch')
        pres=ET.fromstring(z.read('ppt/presentation.xml'));size=pres.find('p:sldSz',NS);w,h=int(size.get('cx')),int(size.get('cy'))
        need(abs(w/h-16/9)<0.03,'PPTX aspect ratio differs')
        missing_locales=[]
        for page,s in enumerate(slides):
            raw=z.read(s);xml=ET.fromstring(raw);text=''.join(xml.itertext())
            if raster:
                pictures=xml.findall('.//p:pic',NS)
                need(len(pictures)==1,'Raster slide must contain exactly one picture: '+s)
                need(not any(xml.findall('.//p:'+tag,NS) for tag in ('sp','graphicFrame','cxnSp','grpSp','contentPart')) and not xml.findall('.//a:t',NS),'Raster slide contains editable objects or text overlay: '+s)
                blip=pictures[0].find('./p:blipFill/a:blip',NS)
                rid=blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed') if blip is not None else None
                rels=ET.fromstring(z.read('ppt/slides/_rels/'+PurePosixPath(s).name+'.rels'))
                matches=[r for r in rels if r.get('Id')==rid and r.get('Type','').endswith('/image') and r.get('TargetMode')!='External']
                need(len(matches)==1,'Raster image relationship missing')
                media=posixpath.normpath(posixpath.join('ppt/slides',matches[0].get('Target','')))
                need(media.startswith('ppt/media/'),'Raster image outside PPTX media')
                need(hashlib.sha256(z.read(media)).hexdigest()==images[page]['source_sha256'],'PPTX media differs from original generated image')
            else:
                need(re.search(r'[ぁ-んァ-ン一-龯]',text),'Slide lacks Japanese text: '+s)
            need('�' not in text,'Replacement glyph in slide text: '+s)
            if not raster and b'ja-JP' not in raw:
                missing_locales.append(s)
            if not raster:need(xml.findall('.//p:sp',NS) or xml.findall('.//p:graphicFrame',NS),'No editable native objects: '+s)
            # Inspect only top-level shape coordinates; group descendants use a local system.
            for shape in xml.findall('./p:cSld/p:spTree/*',NS):
                for transform in shape.findall('./p:spPr/a:xfrm',NS)+shape.findall('./p:xfrm',NS):
                    off=transform.find('a:off',NS);ext=transform.find('a:ext',NS)
                    if off is None or ext is None:continue
                    x,y,cx,cy=[int(v) for v in (off.get('x'),off.get('y'),ext.get('cx'),ext.get('cy'))]
                    need(cx>=0 and cy>=0,'Negative shape dimensions')
                    tolerance=91440 # 0.1 inch for intentional border/bleed
                    need(x>=-tolerance and y>=-tolerance and x+cx<=w+tolerance and y+cy<=h+tolerance,'Shape beyond slide bounds: '+s)
        if missing_locales: warn(row['id']+':language', str(len(missing_locales))+' slides omit ja-JP run locale; Japanese text integrity checked, rendered glyph review remains mandatory in QA')
        for s in notes:
            xml=ET.fromstring(z.read(s));body=[]
            for sp in xml.findall('.//p:sp',NS):
                placeholder=sp.find('./p:nvSpPr/p:nvPr/p:ph',NS)
                if placeholder is not None and placeholder.get('type')=='body':body+=sp.findall('.//a:t',NS)
            need(any(t.text and len(t.text.strip())>5 for t in body),'Missing substantive speaker note: '+s)
            if raster:need(re.search(r'[ぁ-んァ-ン一-龯]',''.join(t.text or '' for t in body)),'Raster speaker note lacks Japanese: '+s)
    report=load(local(folder,'render/powerpoint-render.json'))
    need(report.get('application')=='Microsoft PowerPoint' and report.get('slide_count')==n,'No matching PowerPoint rendering receipt')
    need(report.get('source_sha256','').lower()==sha(p),'PPTX changed since PowerPoint render')
    need([r.get('page') for r in report.get('slides',[])]==list(range(1,n+1)),'PowerPoint rendered page order/count mismatch')
    if raster:
        for receipt,item in zip(report['slides'],images):
            need(receipt.get('shape_count')==1 and receipt.get('text_shapes')==[],'PowerPoint raster shape receipt mismatch')
            need(local(folder/'render',receipt['image'])==record_path(folder,item['render']),'PowerPoint receipt image differs from reviewed image')
    if row.get('pdf_download'):need(local(ROOT,row['pdf_download']).read_bytes().startswith(b'%PDF-'),'Invalid PDF artifact')


def html(row):
    p=local(ROOT,row['preview']);doc=read(p);facts=HTMLFacts();facts.feed(doc)
    frozen_bento=row['repository']=='joeseesun/qiaomu-bento-ppt'
    if frozen_bento:
        # The upstream contract permits only the JSON payload to change. Its
        # English shell language and native keyboard navigation must survive.
        pattern=re.compile(r'<script type="application/bento\+json" id="bento-doc">\s*([\s\S]*?)\s*</script>')
        original=read(local(ROOT,'.build/actual-upstreams/joeseesun__qiaomu-bento-ppt/assets/bento/Bento_Slides.bento.html'))
        need(len(pattern.findall(doc))==1,'Bento document block missing or duplicated')
        need(pattern.sub('<BENTO_DOCUMENT>',doc)==pattern.sub('<BENTO_DOCUMENT>',original),'Bento fixed shell changed outside document JSON')
        payload=json.loads(pattern.search(doc).group(1))
        editable=read(local(ROOT,row['editable_artifact']))
        need(len(pattern.findall(editable))==1,'Editable Bento document missing')
        need(pattern.sub('<BENTO_DOCUMENT>',editable)==pattern.sub('<BENTO_DOCUMENT>',original),'Editable Bento fixed shell changed')
        edit_payload=json.loads(pattern.search(editable).group(1))
        need(payload.get('readonly') is True,'Bento player is not readonly')
        need(payload.get('docId') and payload['docId']==edit_payload.get('docId'),'Bento player/editor identity mismatch')
        need(len(payload.get('slides',[]))==row['page_count'],'Bento payload page count mismatch')
        need(row.get('navigation')=='native-keyboard','Frozen Bento must use native keyboard navigation')
        fonts=payload.get('fonts',[])
        need(fonts and all(f.get('asset') in payload.get('assets',{}) for f in fonts),'Bento doc.fonts assets missing')
        need(payload.get('theme',{}).get('fontFamily') in {f.get('family') for f in fonts},'Bento theme font is not declared in doc.fonts')
        for report_name in ('bento-validation.json','player-validation.json'):
            report=load(local(p.parent,'source/'+report_name))
            need(report.get('ok') is True and report.get('validation',{}).get('ok') is True,'Original Bento validation failed: '+report_name)
            need(report.get('shell_gate',{}).get('internal',{}).get('ok') is True,'Original Bento shell gate failed: '+report_name)
            need(report.get('identity',{}).get('preserved') is True and report['identity'].get('output_doc_id')==payload['docId'],'Bento validation identity mismatch')
    else:
        need(facts.lang=='ja','HTML lang is not Japanese')
    need(re.search(r'[ぁ-んァ-ン一-龯]',doc),'No Japanese source text')
    need('�' not in doc,'Replacement glyph in HTML')
    for tag,key,name in facts.links:
        u=urlsplit(name)
        if not u.scheme and not u.netloc and u.path:
            if u.path.startswith('/'):
                warn(row['id'],'Root-relative browser endpoint/reference requires native preview server: '+name)
            else:local(p.parent,name)
    runtime=doc+'\n'+'\n'.join(read(local(p.parent,s)) for s in facts.scripts if not urlsplit(s).scheme and not s.startswith('/'))
    signatures={
      'zarazhangrui/frontend-slides':['class SlidePresentation','setupStageScale'],
      'op7418/guizang-ppt-skill':['function go(','__playSlide'],
      'ryanbbrown/revealjs-skill':['Reveal.initialize'],
      'lewislulu/html-ppt-skill':['slide','keydown'],
      'lqshow/neon-slides':['function go(','jumper'],
      'chuspeeism/dashi-ppt-skill':['deck-view-model','imported-theme'],
    }
    markers=signatures.get(row['repository'])
    if markers:need(all(s in runtime for s in markers),'Original runtime identity missing: '+row['repository'])
    elif 'marp' in row['repository'].lower():need('bespoke' in runtime or 'marp' in runtime,'Marp runtime missing')
    else:need(facts.scripts or '<script' in doc,'No interactive HTML runtime')
    if facts.slides:need(facts.slides==row['page_count'],'HTML slide sections/page_count mismatch')
    font_signatures={'woff2':b'wOF2','woff':b'wOFF','ttf':b'\x00\x01\x00\x00','otf':b'OTTO'}
    for font in p.parent.rglob('*'):
        ext=font.suffix.lstrip('.').lower()
        if ext in font_signatures and font.is_file():
            need(font.read_bytes()[:4]==font_signatures[ext], 'Font extension/signature mismatch: '+str(font.relative_to(ROOT)))
    for mime,payload in re.findall(r'data:font/(woff2|woff|ttf|otf);base64,([A-Za-z0-9+/=]+)',doc):
        need(base64.b64decode(payload)[:4]==font_signatures[mime], 'Embedded font MIME/signature mismatch: '+mime)
    if not frozen_bento:
        need('yebisu-slide' in doc,'Catalog page-control bridge missing')
        need('e.source!==parent' in doc and 'e.origin!==location.origin' in doc,'Parent message origin/source checks missing')


def archive(row):
    folder=local(ROOT,row['provenance']).parent
    paths={local(ROOT,row[k]) for k in ['artifact_download','source_download']}
    for p in paths:
        if p.suffix.lower()!='.zip':continue
        with zipfile.ZipFile(p) as z:
            need(z.testzip() is None,'Corrupt archive: '+p.name)
            members=[i for i in z.infolist() if not i.is_dir()];names=[i.filename for i in members]
            need(len(names)==len(set(names)),'Duplicate archive members')
            normalized={}
            for item in members:
                name=item.filename;parts=PurePosixPath(name).parts
                need(not name.startswith(('/','\\')) and '..' not in parts and '\\' not in name and ':' not in name,'Unsafe archive member: '+name)
                need((item.external_attr>>16)&0o170000!=0o120000,'Symlink archive member')
                need('node_modules' not in parts and '__pycache__' not in parts and not name.endswith('.pyc'),'Cache/dependency tree in release ZIP')
                key=name[len(folder.name)+1:] if name.startswith(folder.name+'/') else name
                normalized[key]=item
            for required in ['input/data.json','PROMPT.txt','PROVENANCE.json','QA.json','README.md']:
                need(required in normalized,'Reproduction ZIP missing '+required+' in '+p.name)
            need(any('license' in k.lower() or 'ofl' in k.lower() for k in normalized),'ZIP missing licenses')
            need(any(k.endswith(('.py','.js','.mjs','.json','.md')) and (k.startswith('source/') or k.startswith('input/') or k in {'goal.json','deck.md'}) for k in normalized),'ZIP missing reproduction data/source')
            for key,item in normalized.items():
                current=local(folder,key,False)
                if current.is_file():need(hashlib.sha256(z.read(item)).hexdigest()==sha(current),'Stale ZIP member: '+p.name+' : '+key)
            source_files=[f for f in (folder/'source').glob('*') if f.is_file() and f.suffix in {'.py','.js','.mjs'}]
            for f in source_files:need(f.relative_to(folder).as_posix() in normalized,'ZIP omits reproduction script '+f.name)
            if row.get('editability')=='raster_slides':
                for required in ['slide_jobs.json','slide_run_state.json','style.json','deck_spec.json','speech.md','source/native-imagegen-requests.json','render/powerpoint-render.json']:
                    need(required in normalized,'Raster ZIP missing '+required)
                upstream=ROOT/'.build/actual-upstreams'/row['repository'].replace('/','__')
                for original in (upstream/'skills/codex-ppt/scripts').glob('*.py'):
                    key='source/upstream/'+original.relative_to(upstream).as_posix()
                    need(key in normalized,'Raster ZIP missing original dependency '+key)
                    need(hashlib.sha256(z.read(normalized[key])).hexdigest()==sha(original),'Raster ZIP original script modified: '+key)
                for directory in ('origin_image','prompts','source/logs'):
                    for f in (folder/directory).rglob('*'):
                        if f.is_file():need(f.relative_to(folder).as_posix() in normalized,'Raster ZIP missing evidence '+f.name)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',action='append',default=[]);parser.add_argument('--catalog-ref',default='03a2cb0')
    args=parser.parse_args();rows=load(ROOT/'data/case-studies.json')
    check('original-catalog',lambda:catalog(args.catalog_ref,rows));check('repository-registry-and-site',lambda:registry(rows))
    selected=[r for r in rows if not args.case or r['id'] in args.case]
    if args.case:check('selected-case-ids',lambda:need(set(args.case)<={r['id'] for r in rows},'Unknown requested case'))
    for row in selected:
        for name,fn in [('manifest',case_manifest),('provenance',provenance),('pages',image_set),('qa',qa),('archive',archive),('powerpoint' if row.get('format')=='pptx' else 'html',powerpoint if row.get('format')=='pptx' else html)]:
            check(row['id']+':'+name,lambda fn=fn,row=row:fn(row))
    report={'status':'passed' if not ISSUES else 'incomplete_or_failed','catalog_count':len(load(ROOT/'data/skills.json')['skills']),
      'produced_repository_count':len({r['repository'] for r in rows}),'case_count':len(rows),'slide_count':sum(r['page_count'] for r in rows),
      'checked_case_count':len(selected),'passed_checks':len(CHECKS),'issues':ISSUES,'warnings':WARNINGS,
      'scope':'Read-only integrity, provenance and recorded review audit. Does not synthesize missing evidence, assess artistic quality or approve publication.'}
    print(json.dumps(report,ensure_ascii=False,indent=2));return 1 if ISSUES else 0

if __name__=='__main__':sys.exit(main())
