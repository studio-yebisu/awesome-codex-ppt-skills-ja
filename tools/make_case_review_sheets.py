from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/".build/case-qa";OUT.mkdir(exist_ok=True)
for folder in (ROOT/"examples/cases").iterdir():
    files=sorted((folder/"render").glob("slide-*.png"))
    for i in range(0,len(files),4):
        part=files[i:i+4];sheet=Image.new("RGB",(1600,450*((len(part)+1)//2)),"white")
        for j,f in enumerate(part):sheet.paste(Image.open(f).resize((800,450)),((j%2)*800,(j//2)*450))
        sheet.save(OUT/(folder.name+"-"+str(i//4+1)+".png"))
print("Review sheets from actual application/browser renderings")
