"""Rebuild a preserved Bento document into a NEW output directory using the upstream CLI."""
from pathlib import Path
import argparse,base64,hashlib,json,subprocess,sys
from fontTools import subset
from fontTools.ttLib import TTFont
CASE=Path(__file__).resolve().parents[1]
def main():
 a=argparse.ArgumentParser();a.add_argument('--input',type=Path,default=CASE/'deck.json');a.add_argument('--identity-source',type=Path,default=CASE/'input/source.bento.html');a.add_argument('--output-dir',type=Path,required=True);v=a.parse_args();out=v.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 if any((out/n).exists() for n in ['deck.bento.html','player.bento.html','deck.json','player.json']):raise SystemExit('Choose a new output directory; no overwrite is performed.')
 d=json.loads(v.input.read_text(encoding='utf8'));font=TTFont(CASE/'source/fonts/NotoSansJP[wght].ttf');o=subset.Options();o.flavor='woff2';o.name_IDs=['*'];o.name_languages=['*'];ss=subset.Subsetter(options=o);ss.populate(text=json.dumps(d,ensure_ascii=False)+''.join(chr(i) for i in range(32,127))+'←→↗×▶Ⅱ…');ss.subset(font)
 for n in font['name'].names:
  if n.nameID in [1,2,3,4,6,16,17]:n.string={2:'Regular',17:'Regular',6:'YebisuNotoSansJP'}.get(n.nameID,'Yebisu Noto Sans JP').encode(n.getEncoding(),errors='replace')
 font.flavor='woff2';font.save(out/'noto-sans-jp.woff2');d.setdefault('assets',{})['jp-font']='data:font/woff2;base64,'+base64.b64encode((out/'noto-sans-jp.woff2').read_bytes()).decode();d['fonts']=[{'family':'Yebisu Noto Sans JP','asset':'jp-font','weight':'100 900'}]
 cli=CASE/'source/upstream/scripts/bento_deck.py';shell=CASE/'source/upstream/assets/bento/Bento_Slides.bento.html';receipts=[]
 for kind,doc in [('deck',d),('player',dict(d,readonly=True))]:
  j=out/(kind+'.json');j.write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf8');args=[sys.executable,str(cli),'build',str(j),'--identity-source',str(v.identity_source.resolve()),'--shell',str(shell),'--output',str(out/(kind+'.bento.html')),'--report',str(out/(kind+'-validation.json'))];r=subprocess.run(args,capture_output=True,text=True,encoding='utf8');(out/(kind+'-build.txt')).write_text(r.stdout+r.stderr,encoding='utf8');receipts.append({'command':args,'exit_code':r.returncode});print(kind,r.returncode);r.check_returncode()
 (out/'rebuild-receipt.json').write_text(json.dumps({'author':'Codex','receipts':receipts,'source_unchanged_sha256':hashlib.sha256(v.identity_source.read_bytes()).hexdigest(),'font_subset_sha256':hashlib.sha256((out/'noto-sans-jp.woff2').read_bytes()).hexdigest(),'scope':'upstream standalone CLI schema + internal shell + identity gates; project validator absent; no overwrite'},ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
