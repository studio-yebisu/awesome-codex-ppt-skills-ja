"""Build comparison proofs from the current two render directories, retaining both source PNGs."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw
CASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=[]
 for page in (2,3,4):
  src=CASE/'review/comparison-sources';src.mkdir(parents=True,exist_ok=True)
  left=src/f'page-{page:02}-html.png';right=src/f'page-{page:02}-powerpoint.png'
  shutil.copy2(CASE/f'html-render/slide-{page:02}.png',left);shutil.copy2(CASE/f'render/slide-{page:02}.png',right)
  a=Image.open(left).convert('RGB');b=Image.open(right).convert('RGB').resize(a.size)
  out=CASE/f'review/html-pptx-page-{page:02}.png';canvas=Image.new('RGB',(a.width*2,a.height+32),'white');canvas.paste(a,(0,32));canvas.paste(b,(a.width,32));d=ImageDraw.Draw(canvas);d.text((12,10),'CURRENT HTML',fill='black');d.text((a.width+12,10),'CURRENT PPTX / PowerPoint PDF',fill='black');canvas.save(out)
  rows.append({'page':page,'left':left.relative_to(CASE).as_posix(),'left_sha256':sha(left),'left_original':f'html-render/slide-{page:02}.png','right':right.relative_to(CASE).as_posix(),'right_sha256':sha(right),'right_original':f'render/slide-{page:02}.png','comparison':out.relative_to(CASE).as_posix(),'comparison_sha256':sha(out),'comparison_size':list(canvas.size),'composition':'Source pixels copied at y=32; right resized to left dimensions only; no text redrawn or substituted'})
 (CASE/'review/html-pptx-comparisons.json').write_text(json.dumps({'scope':'Current HTML source PNG left and current native PPTX PowerPoint-PDF PNG right; both exact source files retained for independent verification; no pixel identity claimed','pptx_sha256':sha(CASE/'deck.pptx'),'html_metrics_sha256':sha(CASE/'html-render/metrics.json'),'pages':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'pages':len(rows),'sources_retained':6,'comparison_hashes':[x['comparison_sha256'] for x in rows]}))
if __name__=='__main__':main()
