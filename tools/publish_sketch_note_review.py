"""Publish the inspected Sketch Notes HTML and annotation repair evidence."""
from pathlib import Path
import difflib, hashlib, json, shutil, subprocess, sys, zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/sketch-note-showcase'
FORK=ROOT/'skill-forks/sketch-note-ja'
SKIP={'.private','.git','.venv','node_modules','__pycache__'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    images=[CASE/f'render/effect-page-{n:02}-after.jpg' for n in range(1,7)]
    assert all(p.is_file() for p in images)
    for n,path in enumerate(images,1):
        with Image.open(path) as image:image.save(CASE/f'render/slide-{n:02}.png')
    diffs=[]
    for name in ['slides.html','adaptation.css']:
        path=CASE/'source'/name
        rel=path.relative_to(ROOT).as_posix()
        previous=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT).decode('utf-8')
        diffs.append(''.join(difflib.unified_diff(previous.splitlines(True),path.read_text(encoding='utf-8').splitlines(True),fromfile='before/'+name,tofile='source/'+name)))
    (CASE/'source/annotation-repair.diff').write_text('\n'.join(diffs),encoding='utf-8')
    qa=json.loads((CASE/'QA.json').read_text(encoding='utf-8'))
    qa.update(status='original_html_all6_visual_checked',browser='Codex in-app browser',
        scope='All six pages at 1280x720; repaired comparison/spacing also inspected at 1600x900.',
        detailed_all_pages_review=True,independent_review=False,visual_review='All6 full pages inspected. Redundant arrows crossing captions removed; counter rings attached to the actual glyph.',
        repair_author='Codex',independent_recheck='pending_after_repair')
    qa['visual_proofs']=[dict(index=i,image=p.relative_to(CASE).as_posix(),sha256=sha(p)) for i,p in enumerate(images)]
    dump(CASE/'QA.json',qa)
    prov=json.loads((CASE/'PROVENANCE.json').read_text(encoding='utf-8'))
    prov['repair_20261015']={'author':'Codex','diff':'source/annotation-repair.diff','changes':['Remove arrows that crossed font-comparison captions.','Attach comparison rings to actual glyph spans, replacing empty-space circles.','Remove a spacing-demo arrow that crossed its label; place text over the highlighter.'],'original_css_and_controller_preserved':True,'independent_recheck':'pending'}
    dump(CASE/'PROVENANCE.json',prov)
    skill=(FORK/'SKILL.md').read_text(encoding='utf-8')
    start=skill.index('計画確認は承認済み') if '計画確認は承認済み' in skill else skill.index('7. 完成HTMLの全ページ')
    end=skill.index('\n\n編集対象は',start)
    skill=skill[:start]+'''7. 完成HTMLの全ページを発表画面で表示する。日本語・改行・比較する字の大きさ・手描き線の指す先を確認し、線と本文の接触や空白を囲む注釈を直す。前後・先頭末尾の移動と、必要なら大小画面も確認する。実施範囲はQAへ記録し、独立評価の合格と分ける。

この6頁の作例では、字体比較の丸を実際の「雨」に固定し、説明文を横切る矢印を除いた。全6頁を1280×720で、修復箇所を1600×900でも確認した。独立再評価は未了。''' +skill[end:]
    (FORK/'SKILL.md').write_text(skill,encoding='utf-8')
    readme=CASE/'README.md'
    text=readme.read_text(encoding='utf-8')
    text=text.replace('確認はHTML組立成功、Chromeで表紙と字体比較の初回表示、ArrowRightで1/6から2/6への移動、page errorなし。代表PNG2枚を表示しました。残り全頁の詳細目視・独立レビュー・構造監査・ZIP再実行は未実施です。',
        'HTML組立と全6頁の本文・図・注釈をブラウザーで確認し、次・前・先頭への移動を実操作しました。独立再評価・構造監査・ZIP再実行の状況はQAへ分けて記録します。')
    if '\n## 2026-10-15 注釈の修復' not in text:
        text+='\n## 2026-10-15 注釈の修復\n\n比較する文字に丸を固定し、本文に触れる矢印を除いた。全6頁をブラウザーで確認し、修復箇所は1600×900でも確認した。最新画像はrender/slide-01.png〜06.png、差分はsource/annotation-repair.diff。独立再評価は未了。\n'
    readme.write_text(text,encoding='utf-8')
    for path in CASE.rglob('*'):
        if path.is_file() and not set(path.relative_to(CASE).parts)&SKIP and path.suffix!='.pyc':
            dest=FORK/'example'/path.relative_to(CASE);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
    source=json.loads((FORK/'SOURCE.json').read_text(encoding='utf-8'))
    source['files']=[dict(path=p.relative_to(FORK).as_posix(),sha256=sha(p)) for p in sorted(FORK.rglob('*')) if p.is_file() and p.name!='SOURCE.json' and not set(p.relative_to(FORK).parts)&SKIP and p.suffix!='.pyc']
    dump(FORK/'SOURCE.json',source)
    for folder,name in [(CASE,'sketch-note-example-ja.zip'),(FORK,'sketch-note-ja.zip')]:
        with zipfile.ZipFile(ROOT/'downloads'/name,'w',zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(folder.rglob('*')):
                if path.is_file() and not set(path.relative_to(folder).parts)&SKIP and path.suffix!='.pyc':archive.write(path,folder.name+'/'+path.relative_to(folder).as_posix())
    print('Sketch Notes: all6 current images, reusable workflow, annotation diff, and two ZIPs synchronized.')

if __name__=='__main__':main()
