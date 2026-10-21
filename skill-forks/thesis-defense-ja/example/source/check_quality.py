"""Run the preserved upstream quality tools; visual acceptance remains separate."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys

CASE=Path(__file__).resolve().parents[1]
def main():
    shell=shutil.which('pwsh') or shutil.which('powershell')
    if not shell:raise SystemExit('This example requires Windows PowerPoint and PowerShell for its COM quality checks.')
    commands=[('original-export',[shell,'-NoProfile','-File','runtime/scripts/export_pptx_png.ps1','-Pptx','deck.pptx','-OutDir','reviews/original-export','-Width','1600','-Height','900']),
        ('overflow',[shell,'-NoProfile','-File','runtime/scripts/inspect_pptx_overflow.ps1','-Pptx','deck.pptx','-Tolerance','40','-OutputJson','reviews/overflow.json']),
        ('contact-sheet',[sys.executable,'runtime/scripts/make_contact_sheet.py','--input','render','--output','reviews/contact-sheet.png']),
        ('stale-text',[sys.executable,'runtime/scripts/scan_pptx_text.py','--pptx','deck.pptx','--bad','中期检查,项目简介,系统框图,算法设计,成果展示,总结分析,TODO,占位','--json','reviews/stale-text-scan.json'])]
    private=CASE/'.private/current-quality-raw';private.mkdir(parents=True,exist_ok=True)
    rows=[]
    for label,cmd in commands:
        r=subprocess.run(cmd,cwd=CASE,capture_output=True,text=True,encoding='utf-8')
        raw=r.stdout+r.stderr;(private/(label+'.txt')).write_text(raw,encoding='utf-8')
        normalized=raw.replace(str(CASE),'.').replace(CASE.as_posix(),'.')
        log=CASE/'reviews'/('current-'+label+'.txt');log.write_text(normalized,encoding='utf-8')
        rows.append({'command':[Path(cmd[0]).name]+cmd[1:],'exit_code':r.returncode,'log':log.relative_to(CASE).as_posix()})
        r.check_returncode()
    overflow=json.loads((CASE/'reviews/overflow.json').read_text(encoding='utf-8-sig'))
    overflow['pptx']='deck.pptx';(CASE/'reviews/overflow.json').write_text(json.dumps(overflow,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert overflow['overflow_count']==0
    stale=json.loads((CASE/'reviews/stale-text-scan.json').read_text(encoding='utf-8-sig'))
    assert not stale['bad_hits']
    stale['pptx']='deck.pptx';(CASE/'reviews/stale-text-scan.json').write_text(json.dumps(stale,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'pptx_sha256':hashlib.sha256((CASE/'deck.pptx').read_bytes()).hexdigest(),'commands':rows,
        'original_overflow_tolerance_unchanged':40,'overflow_count':0,'visual_review':'Not inferred from these scripts; inspect current contact sheet and actual pages.','human_or_independent_approval_claimed':False}
    (CASE/'reviews/current-technical-quality.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Original export/contact/overflow/stale-scan completed; overflow0. Visual acceptance remains separate.')

if __name__=='__main__':main()
