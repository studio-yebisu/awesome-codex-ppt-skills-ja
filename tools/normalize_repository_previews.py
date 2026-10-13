"""Convert actual browser screenshot encoding and build compact review sheets."""
from pathlib import Path
from PIL import Image, ImageDraw
import json

ROOT=Path(__file__).resolve().parents[1]
for case in json.loads((ROOT/'data/web-repository-examples.json').read_text(encoding='utf-8')):
    ident=case['id']
    folder=ROOT/'examples/repositories'/ident
    source=ROOT/'.build/repository-qa'/ident
    captured=sorted(source.glob('slide-*.jpg'))
    if len(captured)!=case['page_count']:
        print(ident+': browser captures pending ('+str(len(captured))+'/'+str(case['page_count'])+')')
        continue
    images=[]
    for i,p in enumerate(captured,1):
        image=Image.open(p).convert('RGB')
        if image.width*9!=image.height*16:raise ValueError('Non-16:9 browser viewport: '+str(p))
        target=folder/'render'/('slide-'+str(i).zfill(2)+'.png')
        target.parent.mkdir(parents=True,exist_ok=True)
        image.save(target,'PNG')
        images.append(image.copy())
    sheet=Image.new('RGB',(1280,378*((len(images)+1)//2)),'#DBDEDA')
    draw=ImageDraw.Draw(sheet)
    for i,im in enumerate(images):
        x=(i%2)*640;y=(i//2)*378
        draw.text((x+10,y+4),ident+' / '+str(i+1),fill='black')
        sheet.paste(im.resize((640,360)),(x,y+18))
    sheet.save(source/'contact.png')
    print(ident+': '+str(len(images))+' real browser previews converted to PNG')
