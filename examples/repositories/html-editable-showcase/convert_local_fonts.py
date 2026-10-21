"""Local full-TTF registry; all rendering/conversion stays in original convert.py."""
from pathlib import Path
import os,runpy,sys
HERE=Path(__file__).resolve().parent
UP=HERE/'upstream'
CACHE=HERE/'cache/fonts';CACHE.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(UP/'scripts'))
import font_paths
font_paths.CACHE_DIR=CACHE
import embed_fonts,font_resolver
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import shutil
entries=[]
for family,style,cjk,regular,bold,aliases in [
 ('Zen Kaku Gothic New','sans',True,'ZenKakuGothicNew-Regular.ttf','ZenKakuGothicNew-Black.ttf',['Noto Sans SC']),
 ('Shippori Mincho','serif',True,'ShipporiMincho-Bold.ttf','ShipporiMincho-Bold.ttf',['Noto Serif SC']),
 ('Manrope','sans',False,'Manrope[wght].ttf','Manrope[wght].ttf',[])]:
 slots={}
 for slot,filename,weight in [('regular',regular,400),('bold',bold,700)]:
  destination=CACHE/(family.replace(' ','')+'-'+slot+'.ttf')
  source=HERE/'fonts'/filename
  if '[' in filename:
   font=TTFont(source);instance=instantiateVariableFont(font,{'wght':weight},inplace=False);instance.save(destination)
  else:shutil.copy2(source,destination)
  slots[slot]=destination.name
 entries.append({'typeface':family,'charset':'128' if cjk else '0','pitchFamily':'18' if style=='serif' else '34','cjk':cjk,'style':style,'slots':slots,'aliases':aliases})
font_resolver.register_in_font_plan(entries)
font_resolver.resolve_fonts=lambda needed,bundled:{'resolved':entries,'unavailable':[],'cached':[e['typeface'] for e in entries]}
import assemble as assemble_runtime
from clear_implicit_effects import clear_implicit_effects
from native_flag import replace_simple_flag
original_assemble=assemble_runtime.assemble
def assemble_flat_input(measurement,out_path):
 original_assemble(measurement,out_path)
 replace_simple_flag(out_path)
 clear_implicit_effects(out_path)
assemble_runtime.assemble=assemble_flat_input
import visual_audit,visual_audit_labels
visual_audit.build_compare_image=visual_audit_labels.build_compare_image
import no_quit_render
no_quit_render.install()
runpy.run_path(str(UP/'convert.py'),run_name='__main__')
