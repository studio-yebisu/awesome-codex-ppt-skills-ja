"""Label actual SVG and PowerPoint renders without claiming pixel identity."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
CASE=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(CASE/'fonts/BIZUDPGothic-Bold.ttf'),26)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for n in range(1,9):
    left=CASE/f'review/svg-render/slide-{n:02}.png';right=CASE/f'render/slide-{n:02}.png'
    out=CASE/f'review/slide-{n:02}-svg-native.png'
    sheet=Image.new('RGB',(1600,500),'#E5E5E5');d=ImageDraw.Draw(sheet)
    d.text((20,12),'変換前：入力SVG（Chromium）',font=font,fill='#202C29')
    d.text((820,12),'変換後：native PPTX（PowerPoint）',font=font,fill='#202C29')
    sheet.paste(Image.open(left).convert('RGB').resize((800,450)),(0,50))
    sheet.paste(Image.open(right).convert('RGB').resize((800,450)),(800,50))
    sheet.save(out)
    rows.append({'page':n,'left':left.relative_to(CASE).as_posix(),'left_sha256':sha(left),'right':right.relative_to(CASE).as_posix(),'right_sha256':sha(right),'comparison':out.relative_to(CASE).as_posix(),'comparison_sha256':sha(out),'claim':'Actual pre/post conversion; different rendering engines, no pixel identity claim'})
(CASE/'review/svg-native-sources.json').write_text(json.dumps({'artifact_sha256':sha(CASE/'deck.pptx'),'comparisons':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Eight source SVG/native comparisons saved')
