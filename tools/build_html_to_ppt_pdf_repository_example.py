"""Prepare the pinned HTML conversion example, preserving input corresponding source."""
from pathlib import Path
import shutil,json,hashlib,os,subprocess,argparse,sys
ROOT=Path(__file__).resolve().parents[1];CASE=ROOT/'examples/repositories/html-to-ppt-pdf'
def cp(source,target):
 target.parent.mkdir(parents=True,exist_ok=True)
 if source.is_dir():shutil.copytree(source,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','__pycache__','.git'))
 else:shutil.copy2(source,target)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--prepare-only',action='store_true');ap.add_argument('--node');ap.add_argument('--browser-cache');ap.add_argument('--powerpoint',action='store_true');args=ap.parse_args()
 for x in ['source','input','licenses','review','original','render']:(CASE/x).mkdir(parents=True,exist_ok=True)
 cp(ROOT/'.build/actual-upstreams/wangzan101__html-to-ppt-pdf',CASE/'source/upstream')
 # Preserve the reviewed image-size override and its lock in the shipped runtime.
 if not (CASE/'source/runtime/package-lock.json').exists():cp(CASE/'source/upstream/scripts',CASE/'source/runtime')
 cp(ROOT/'examples/cases/port-town',CASE/'input/port-town')
 cp(ROOT/'examples/cases/port-town/LICENSE',CASE/'licenses/AGPL-3.0-input.txt')
 cp(CASE/'source/upstream/LICENSE',CASE/'licenses/MIT-converter.txt')
 cp(ROOT/'examples/cases/port-town/licenses/fonts',CASE/'licenses/fonts')
 src=CASE/'source/input-corresponding-source'
 for p in ['tools/build_case_studies.py','tools/business_web_content.py','data/case-inputs.json','data/upstreams.json','data/preset-fonts.json','data/fonts.json','assets/case-slides.css','assets/case-editor.js','sources/browser-dependencies','skill-forks/guizang-ppt-skill-ja']:
  cp(ROOT/p,src/p)
 cp(ROOT/'.build/actual-upstreams/op7418__guizang-ppt-skill',src/'upstreams/op7418__guizang-ppt-skill')
 for p in ['noto-sans-jp.woff2','noto-serif-jp.woff2','biz-udpgothic-regular.woff2','biz-udpgothic-bold.woff2','presets/playfairdisplay.ttf','presets/sourceserif4.ttf','presets/ibmplexmono.ttf']:
  cp(ROOT/'assets/fonts'/p,src/'assets/fonts'/p)
 cp(ROOT/'examples/cases/port-town/licenses/fonts',src/'assets/fonts/licenses')
 if not args.prepare_only:
  command=[sys.executable,str(CASE/'source/reproduce.py')]
  if args.node:command+=['--node',args.node]
  if args.browser_cache:command+=['--browser-cache',args.browser_cache]
  if args.powerpoint:command+=['--powerpoint']
  subprocess.run(command,cwd=CASE,check=True)
 print(CASE)
if __name__=='__main__':main()
