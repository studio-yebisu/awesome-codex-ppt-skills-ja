"""Apply native OOXML triangle sizes to a disposable generated PPTX, using stdlib only."""
from pathlib import Path
import argparse,hashlib,json,re,zipfile

def main():
 p=argparse.ArgumentParser();p.add_argument('pptx',type=Path);p.add_argument('--in-place',action='store_true');p.add_argument('--expected-heads',type=int,required=True);a=p.parse_args()
 if not a.in_place:raise SystemExit('Use --in-place only for a newly generated disposable PPTX.')
 src=a.pptx.resolve();assert src.is_file()
 temporary=src.with_suffix('.arrow-size.tmp.pptx');assert not temporary.exists()
 before=hashlib.sha256(src.read_bytes()).hexdigest();count=0;changed=[]
 with zipfile.ZipFile(src)as old,zipfile.ZipFile(temporary,'w')as new:
  for info in old.infolist():
   data=old.read(info.filename)
   if re.fullmatch(r'ppt/slides/slide\d+\.xml',info.filename):
    def enlarge(m):
     nonlocal count
     count+=1;return b'<a:'+m[1]+b' type="triangle" w="lg" len="lg"/>'
    updated=re.sub(rb'<a:(headEnd|tailEnd) type="triangle"\s*/>',enlarge,data)
    if updated!=data:changed.append(info.filename)
    data=updated
   new.writestr(info,data)
 assert count==a.expected_heads,(count,a.expected_heads)
 with zipfile.ZipFile(temporary)as check:assert check.testzip()is None
 temporary.replace(src)
 print(json.dumps({'status':'native_arrow_sizes_applied','before_sha256':before,'after_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'triangle_heads':count,'changed_parts':changed,'changes':'Only triangle head w/len; text, positions, paths, crop and other ZIP payloads unchanged.'}))
if __name__=='__main__':main()
