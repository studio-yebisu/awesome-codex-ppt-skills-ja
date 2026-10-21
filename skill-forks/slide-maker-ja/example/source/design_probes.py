"""Post-build direction comparison; uses original deckkit, does not claim pre-approval."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/upstream/skills/slide-maker/scripts'))
import deckkit as d
from pptx.dml.color import RGBColor
d.FONT=d.EAFONT='Yu Gothic'
p=d.blank_deck(13.333,7.5)
def t(s,x,y,w,h,a,z=26,c='132C3B',b=False):return d.text(s,x,y,w,h,[[(a,z,RGBColor.from_string(c),b,False,d.FONT)]])
for k in range(4):
 s=d.add_slide(p)
 if k==0:
  d.title_bar(s,'並べておくと、探し方が変わる',kicker='A / 明るい配列教材')
  for j in range(15):
   d.box(s,.6+j*.81,2.55,.7,.65,fill='A8471C' if j==12 else 'E8EEF0');t(s,.67+j*.81,2.63,.6,.5,str(j+1),20,'FFFFFF' if j==12 else '132C3B')
  t(s,.7,4,5.5,.6,'先頭から',30);t(s,.7,4.9,5.5,1,'13回',48,'A8471C',True)
  t(s,7,4,5.5,.6,'真ん中から',30);t(s,7,4.9,5.5,1,'4回',48,'116B8A',True)
 elif k==1:
  d.box(s,0,0,13.333,7.5,fill='132C3B');t(s,.7,.65,12,1,'B / コード端末を模した表示',30,'FFFFFF',True)
  t(s,.7,2.1,12,1,'target = 13',46,'FFFFFF',True);t(s,.7,3.5,12,1,'linear:  1 → 2 → … → 13',32,'F4B393')
  t(s,.7,4.7,12,1,'binary:  8 → 12 → 14 → 13',32,'8FD0E4');t(s,.7,6.2,12,.6,'比較回数　13回 / 4回',26,'FFFFFF')
 elif k==2:
  t(s,.7,.65,12,.8,'C / 差だけを先に見る',36,b=True)
  d.box(s,.7,2.2,7.8,.75,fill='A8471C');t(s,9,2.2,3,.8,'13回',42,'A8471C',True)
  d.box(s,.7,3.55,2.4,.75,fill='116B8A');t(s,3.6,3.55,3,.8,'4回',42,'116B8A',True)
  t(s,.7,5.45,12,.8,'13を探す：線形探索と二分探索',30);t(s,.7,6.3,12,.5,'配列は昇順の1〜15',22)
 else:
  t(s,.7,.65,12,.8,'D / 判定の木として見る',36,b=True)
  for x,y,num in [(6,2,8),(8,3.3,12),(10,4.6,14),(8,5.9,13)]:
   d.box(s,x,y,1,.65,fill='116B8A');t(s,x+.15,y+.06,.8,.5,str(num),24,'FFFFFF',True)
  t(s,.7,2.5,4.8,2,'中央をたどる\n8 → 12 → 14 → 13',28);t(s,.7,5.3,5,.8,'13を4回で見つける',30)
import visual_languages as vl
k=vl.use('chalkboard',p,fonts='both')
k.cover(k.new_slide(),kicker='E / 原典の黒板スタイル',title='並べておくと、探し方が変わる',subtitle='1〜15から13を探す：13回と4回')
ROOT.joinpath('design').mkdir(exist_ok=True);p.save(ROOT/'design/direction-probes.pptx')
