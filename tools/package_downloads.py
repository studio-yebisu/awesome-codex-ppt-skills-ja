from pathlib import Path
from hashlib import sha256
import json, zipfile
ROOT=Path(__file__).resolve().parents[1]
def bundle(source,target):
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for file in sorted(source.rglob('*')):
            if file.is_file() and not any(part in ['node_modules','__pycache__','.git'] for part in file.relative_to(source).parts):
                archive.write(file,Path(source.name)/file.relative_to(source))
    return dict(file=str(target.relative_to(ROOT)).replace('\\','/'),bytes=target.stat().st_size,sha256=sha256(target.read_bytes()).hexdigest())
if __name__=='__main__':
    out=ROOT/'downloads';out.mkdir(exist_ok=True)
    manifest=[]
    for folder in sorted((ROOT/'skills').iterdir()):
        if folder.is_dir():manifest.append(bundle(folder,out/(folder.name+'.zip')))
    for folder in sorted((ROOT/'examples').iterdir()):
        if folder.is_dir():manifest.append(bundle(folder,out/(folder.name+'-source.zip')))
    for file in sorted(out.glob('*.pptx')):manifest.append(dict(file=str(file.relative_to(ROOT)).replace('\\','/'),bytes=file.stat().st_size,sha256=sha256(file.read_bytes()).hexdigest()))
    (ROOT/'data/downloads.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'{len(manifest)} verified download files / {sum(m["bytes"] for m in manifest):,} bytes')
