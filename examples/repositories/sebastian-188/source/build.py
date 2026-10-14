from pathlib import Path
import json,html
import fitz
B=Path(__file__).resolve().parents[1]; R='#E2001A'; K='#000000'; W='#FFFFFF'
font='Microsoft YaHei,Noto Sans CJK JP,SimHei,PingFang SC,sans-serif'
def rect(x,y,w,h,c):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
def line(x,y,x2,y2,c=K,w=2):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"/>'
def text(x,y,s,z=36,c=K,b=400):return f'<text x="{x}" y="{y}" style="font-family:{font};font-size:{z}px;font-weight:{b};" fill="{c}">{html.escape(s)}</text>'
def lines(x,y,ss,z=36,c=K,b=400,gap=None):return ''.join(text(x,y+i*(gap or z*1.5),s,z,c,b) for i,s in enumerate(ss))
def base(n,label,bg=W):return rect(0,0,1920,1080,bg)+text(100,90,label,24,W if bg==K else K,700)+text(100,1016,'STUDIO YEBISU / FICTIONAL BRIEF EXAMPLES',20,W if bg==K else K)+text(1710,1016,f'{n:02} / 07',24,W if bg==K else K,700)
slides=[]
s=base(1,'BRIEF BEFORE AI')+rect(0,0,620,1080,R)+text(100,96,'BRIEF BEFORE AI',24,W,700)+text(92,550,'AI',320,W,900)+text(100,1016,'STUDIO YEBISU',20,W)+lines(720,360,['任せる前の','設計図'],144,K,900,180)+line(720,690,1810,690,R,8)+lines(720,790,['目的・読み手・入力・制約・完成条件。','日本語の制作依頼を、具体的に書き分ける。'],36)+text(720,940,'架空の実用例集 / 2026',24)
slides.append(('cover','AIに任せる前の設計図',s))
s=base(2,'01 / THE FIVE QUESTIONS')+text(100,250,'依頼は、五つの問いで組み立てる。',74,K,900)
rows=[('01','目的','読んだ後、何を判断・行動してほしい？'),('02','読み手','誰が読む？ 何を知っている？'),('03','入力','何を材料にする？ どれを正本にする？'),('04','制約','長さ・語調・禁止事項・納品形式は？'),('05','完成条件','何が揃えば、確認できる？')]
for i,(no,lab,body) in enumerate(rows):
 y=360+i*113;s+=line(100,y-38,1810,y-38)+text(100,y+22,no,64,R,900)+text(330,y+16,lab,42,K,700)+text(650,y+10,body,36)
slides.append(('summary','依頼は五つの問いで組み立てる',s))
s=base(3,'02 / PURPOSE + AUDIENCE')+rect(0,170,860,780,K)+lines(100,330,['同じ展示会。','違う、','伝え方。'],106,W,900,140)+text(100,865,'EXAMPLE A / 招待メール',28,W,700)+lines(960,240,['目的を、行動まで書く。'],62,K,900)+text(960,350,'「魅力的に紹介して」から一歩具体的に。',30)+text(960,470,'目的',28,R,700)+lines(960,535,['来場候補日を返信してもらう。','展示の詳説より、返信しやすさを優先。'],36)+text(960,700,'読み手',28,R,700)+lines(960,765,['初めて来る近隣の店舗担当者。','専門用語を避け、所要時間を明記。'],36)+text(960,920,'依頼文：来場候補日を聞く、短い招待メールを。',30,K,700)
slides.append(('contrast','目的を行動まで書く',s))
s=base(4,'03 / INPUT + SOURCE OF TRUTH')+text(100,240,'材料と、空欄を分ける。',92,K,900)+text(100,335,'EXAMPLE B / 新人向けの搬入手順書',28,R,700)
s+=line(100,400,1810,400,K,6)+text(100,480,'渡すもの',36,K,700)+text(1080,480,'渡せないもの',36,R,700)+line(960,435,960,835)
s+=lines(100,580,['現行手順 v3 の本文','入口・受付・保管場所の写真','責任者が確認した注意事項'],42)+lines(1080,580,['未確認の安全基準','担当者の個人連絡先','写真にない経路の推測'],42)+rect(100,860,1710,95,R)+text(140,920,'依頼文：現行手順を正本に。欠けた情報は「要確認」と残す。',36,W,700)
slides.append(('input','材料と空欄を分ける',s))
s=base(5,'04 / CONSTRAINTS',K)+text(100,250,'「いい感じ」を、仕様にする。',88,W,900)+text(100,345,'EXAMPLE C / 架空の展示会告知ポスター',28,W,700)+rect(100,440,490,465,R)+text(140,585,'A3',132,W,900)+lines(140,705,['縦向き','印刷用PDF'],44,W,700)
for y,num,heading,body in [(485,'01','載せる','会期・会場・入場方法・問合せ窓口。'),(635,'02','避ける','実績、来場者数、割引を作らない。'),(785,'03','揃える','赤・黒・白。見出しは最大2行。')]:
 s+=text(700,y,num,64,R,900)+text(875,y-10,heading,36,W,700)+text(875,y+48,body,34,W)+line(700,y+80,1810,y+80,W)
slides.append(('constraints','いい感じを仕様にする',s))
s=base(6,'05 / DEFINITION OF DONE')+text(100,240,'完成は、確認できる言葉で。',88,K,900)+text(100,345,'EXAMPLE A / 招待メールの受け取り条件',28,R,700)+text(100,650,'3',290,R,900)+text(100,810,'CHECKS',48,K,900)
for i,(a,b) in enumerate([('必要な情報','会期・会場・所要時間・返信先がある。'),('文字量','件名30字以内、本文300字以内。'),('根拠と空欄','入力にない事実を追加せず、不明は列挙。')]):
 y=470+i*150;s+=text(650,y,a,42,K,700)+text(650,y+65,b,36)+line(650,y+105,1810,y+105)
s+=text(650,950,'レビュー：送信前に日時・住所・返信先を人が確認する。',30,K,700)
slides.append(('checks','完成は確認できる言葉で',s))
s=base(7,'06 / A COMPLETE REQUEST').replace(text(100,1016,'STUDIO YEBISU / FICTIONAL BRIEF EXAMPLES',20,K),'')+rect(0,0,510,1080,R)+lines(100,295,['五つを、','一つの','依頼へ。'],94,W,900,125)+text(100,880,'COPY & ADAPT',27,W,700)+text(620,150,'招待メールの制作依頼',68,K,900)
req=[('目的','来場候補日を返信してもらう。'),('読み手','初めて来る近隣の店舗担当者。'),('入力','添付の会期・会場・所要時間の一覧だけを使う。'),('制約','件名30字・本文300字以内。専門用語を避ける。'),('完成条件','必要情報を含め、不明点を末尾に別記する。')]
for i,(a,b) in enumerate(req):
 y=280+i*112;s+=text(620,y,a,28,R,700)+text(620,y+50,b,36)+line(620,y+75,1810,y+75)
s+=lines(620,920,['まず一案を作成。送信はせず、レビュー用の文章で渡す。'],32,K,700)+text(100,1016,'架空例 / SVG ORIGINAL',20,W)
slides.append(('ending','五つを一つの依頼へ',s))
structure={'source_file':'input/BRIEF.md','metadata':{'title':'AIに任せる前の設計図','total_pages':7,'fictional':True},'pages':[{'page_number':i,'type':a,'title':b,'density':'low' if i==1 else 'medium'} for i,(a,b,c) in enumerate(slides,1)]}
(B/'.ppt-session/structure.json').write_text(json.dumps(structure,ensure_ascii=False,indent=2))
design={'style_name':'Swiss Style / 日本語派生','style_file':'source/upstream/styles/04-swiss-style.md','canvas':{'width':1920,'height':1080},'colors':[R,K,W],'font_stack':font,'margin':100,'changes':['日本語に合わせたNoto Sans CJK JP fallback','見出しの拡大と行分割','役割別の非カード組版','HTMLページ送りと再生']}
(B/'.ppt-session/design.json').write_text(json.dumps(design,ensure_ascii=False,indent=2))
for i,(kind,title,s) in enumerate(slides,1):
 (B/f'svg/slide-{i:02}-{kind}.svg').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'+s+'</svg>')
import subprocess,tempfile
merged=fitz.open()
with tempfile.TemporaryDirectory() as tmp:
 for i,f in enumerate(sorted((B/'svg').glob('*.svg')),1):
  out=Path(tmp)/f'{i}.pdf'
  subprocess.run(['inkscape',str(f),'--export-type=pdf',f'--export-filename={out}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  d=fitz.open(out);merged.insert_pdf(d)
  d[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(B/f'render/slide-{i:02}.png')
merged.save(B/'deck.pdf')
print('Created seven SVG pages; Inkscape PDF and PDF-render PNG previews')
