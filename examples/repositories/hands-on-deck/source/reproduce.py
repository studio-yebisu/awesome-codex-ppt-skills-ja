"""Replay the Japanese edit through unmodified hands-on-deck deck.py."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, shutil, os

CASE = Path(__file__).resolve().parents[1]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=CASE/'input/data.json')
    parser.add_argument('--render',action='store_true',help='Render using installed Microsoft PowerPoint on Windows')
    parser.add_argument('--libreoffice-render',action='store_true',help='Also run original LibreOffice/Poppler renderer')
    args=parser.parse_args(); data=json.loads(args.input.resolve().read_text('utf-8'))
    donor=CASE/'input/donor.pptx'
    if digest(donor)!=data['donor_sha256']: raise SystemExit('The donor hash does not match input/data.json')
    review=CASE/'review/replay'; review.mkdir(parents=True,exist_ok=True)
    cli=CASE/'source/upstream/scripts/deck.py'; receipts=[]
    def run(argv,name):
        env=dict(os.environ); lo=Path('C:/Program Files/LibreOffice/program')
        if not shutil.which('soffice') and (lo/'soffice.exe').exists(): env['PATH']=str(lo)+os.pathsep+env.get('PATH','')
        result=subprocess.run([str(x) for x in argv],cwd=CASE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        log=review/(name+'.log');log.write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
        receipts.append({'argv':[str(x) for x in argv],'cwd':str(CASE),'script':name,'exit_code':result.returncode,'log':log.relative_to(CASE).as_posix(),'log_sha256':digest(log)})
        save(review/'execution-receipts.json',receipts)
        if result.returncode: raise SystemExit(result.stdout+'\n'+result.stderr)
    def deck(argv,name): run([sys.executable,cli]+argv,name)
    deck([donor,'inspect','-o',review/'donor-inspect.json'],'inspect-donor')
    inventory=json.loads((review/'donor-inspect.json').read_text('utf-8'))
    ops=[{k:v for k,v in op.items() if k!='repair_native5'} for op in json.loads((CASE/'input/patch.json').read_text('utf-8'))['ops'] if op['op'] in ('set-style','move','resize')]
    ops.insert(0,{'op':'set-props','title':data['title'],'author':'Japanese Example Project','last_modified_by':'Japanese Example Project','subject':'Japanese editing example'})
    for i, slide in enumerate(data['slides']):
        names={v.get('name'):k for k,v in inventory['slides'][str(i)].items() if isinstance(v,dict)}
        fields={k:v for k,v in slide.items() if k not in ('headers','rows')}
        fields.update({'header-'+str(c):v for c,v in enumerate(slide.get('headers',[]))})
        fields.update({f'cell-{r}-{c}':v for r,row in enumerate(slide.get('rows',[])) for c,v in enumerate(row)})
        for name,value in fields.items(): ops.append({'op':'set-text','slide':i,'shape':names[name],'text':value.split('\n')})
        ops.append({'op':'set-notes','slide':i,'notes':data['notes'][i]})
    save(review/'patch.json',{'ops':ops})
    deck([donor,'apply',review/'patch.json','-o',review/'pre-fix.pptx'],'apply')
    deck([review/'pre-fix.pptx','fix','--slides','0,1,2,3,4','-o',CASE/'deck.pptx'],'fix')
    deck([CASE/'deck.pptx','inspect','-o',review/'result-inspect.json'],'inspect-result')
    deck([donor,'diff',CASE/'deck.pptx'],'diff')
    if args.libreoffice_render: deck([CASE/'deck.pptx','render','-o',review/'original-render'],'original-render')
    if args.render:
        shell=shutil.which('pwsh') or shutil.which('powershell')
        if not shell: raise SystemExit('PowerShell and Microsoft PowerPoint are required for --render')
        run([shell,'-NoProfile','-ExecutionPolicy','Bypass','-File',CASE/'source/render_powerpoint.ps1','-PresentationPath',CASE/'deck.pptx','-OutputDirectory',CASE/'render'],'powerpoint-render')
    save(review/'result.json',{'input_sha256':digest(args.input.resolve()),'artifact_sha256':digest(CASE/'deck.pptx'),'operations':len(ops),'render_requested':args.render,'visual_review':'required_for_new_output'})
    save(CASE/'QA.json',{'status':'generated_awaiting_review','page_count':5,'artifact_sha256':digest(CASE/'deck.pptx'),'human_adoption':'pending','production_adoption':False,'visual_review':'Newly rebuilt output requires a new full-page review; catalog QA is not transferred.'})
    print('Rebuilt '+str(CASE/'deck.pptx')+'; review all pages before use.')
if __name__=='__main__': main()
