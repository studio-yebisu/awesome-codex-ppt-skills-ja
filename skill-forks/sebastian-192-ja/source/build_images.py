"""Repackage approved images with unchanged original strict validator/packer."""
from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parents[1]
output=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else p/'reproduced.pptx'
scripts=p/'source/upstream/scripts'
subprocess.run([sys.executable,str(scripts/'validate_page_spec.py'),str(p/'page-spec.json'),'--require-images','--strict'],check=True)
subprocess.run([sys.executable,str(scripts/'build_image_ppt.py'),str(p/'page-spec.json'),str(output),'--fit','contain','--max-width','0','--jpeg-quality','0'],check=True)
