"""Mechanical QA crops only; do not alter the slide or invent content."""
from pathlib import Path
import hashlib,json
from PIL import Image
C=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    rows=[]
    for label,path in [('before','source/imagegen-repair/slide-03-before.png'),('after','render/slide-03.png')]:
        p=C/path;im=Image.open(p).convert('RGB');original_size=list(im.size)
        if im.size!=(1600,900):im=im.resize((1600,900),Image.Resampling.LANCZOS)
        box=(1000,635,1580,755) if label=='before' else (1000,585,1580,755)
        out=C/f'source/imagegen-repair/warning-detail-{label}.png';im.crop(box).save(out)
        rows.append({'label':label,'source':path,'source_sha256':sha(p),'source_size':original_size,'normalized_size':[1600,900],'crop_box':list(box),'out':out.relative_to(C).as_posix(),'out_sha256':sha(out)})
    (C/'source/imagegen-repair/warning-detail.json').write_text(json.dumps({'purpose':'Readable detail for QA comparison; before crop and current actual PowerPoint after crop.','method':'Whole-page mechanical size normalization where needed, then crop each actual warning panel at recorded coordinates. Keep different panel heights; no text/shape repainting.','slide_artifact_changed':False,'rows':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
