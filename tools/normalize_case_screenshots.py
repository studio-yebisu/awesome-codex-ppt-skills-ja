"""Normalize browser capture encoding to the public PNG file extension; no visual edits."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
count=0
for path in (ROOT/"examples/cases").glob("*/render/slide-*.png"):
    with Image.open(path) as im:
        if im.format=="PNG":continue
        copy=im.convert("RGB")
    copy.save(path,format="PNG");count+=1
print(str(count)+" browser captures encoded as PNG")
