"""Reproduce the AGPL input from its preserved corresponding source."""
from pathlib import Path
import sys,hashlib
root=Path(__file__).resolve().parent/'input-corresponding-source';sys.path.insert(0,str(root/'tools'))
import build_case_studies as source
source.UP=root/'upstreams'  # Relocate the preserved upstream snapshot without changing its generator.
out=Path(__file__).resolve().parents[1]/'review/input-source-rebuild';out.mkdir(parents=True,exist_ok=True)
data=source.DATA['harbor'];roster=source.magazine_port(data)
html=source.guizang('port-town',data['title'],roster,'Magazine / Ink Classic',out)
(out/'index.html').write_text(html,encoding='utf-8')
expected=Path(__file__).resolve().parents[1]/'input/port-town/index.html'
same=(out/'index.html').read_bytes()==expected.read_bytes();print('Input byte identical:',same)
if not same:raise SystemExit(1)
