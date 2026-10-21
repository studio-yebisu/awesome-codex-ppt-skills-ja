from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parent.parent
slides=[
('cover','dark','SOUND WALK / CULTURAL EVENT','音を、<br>地図にする。','街を歩き、聞こえたことを持ち帰る。'),
('statement','light','01 / EXPERIENCE','同じ道でも、<br>聞こえ方は違う。','歩く範囲も、立ち止まる場所も自分で選ぶ。'),
('flow','dark','02 / RECORD','聞いたことを、<br>三つの欄に残す。','録音は不要。気づいたことを、短い言葉で。'),
('data-split','light','03 / EXAMPLE','音の種類と、<br>印象を並べる。','同じ音でも、感じ方はひとつに決まらない。'),
('image-split','dark','04 / EXHIBITION','持ち帰った記録を、<br>壁の地図へ。','音の場所に札を置き、ほかの人の言葉を読む。'),
('bullets','light','05 / CARE','安心して歩ける、<br>余白をつくる。','歩くことも、会場で読むことも選べる。'),
('closing','dark','06 / NEXT','次の角で、<br>ひとつ聞いてみる。','小さな試行から、散歩と展示の流れを確かめる。')]
def map_svg():
 return '''<svg class="map" viewBox="0 0 780 550" role="img" aria-label="橋、路地、広場を結ぶ架空の地図"><g fill="none" stroke="currentColor"><path opacity=".15" stroke-width="1" d="M0 80H780M0 180H780M0 280H780M0 380H780M0 480H780M80 0V550M180 0V550M280 0V550M380 0V550M480 0V550M580 0V550M680 0V550"/><path opacity=".45" stroke-width="18" d="M0 415C180 430 200 100 420 130S650 280 780 210"/><path opacity=".7" stroke-width="2" d="M55 75H275V345H680M115 490V230H515V65M350 505V285H720"/><path stroke-width="3" stroke-dasharray="8 10" d="M160 230H275V345H570"/><circle cx="160" cy="230" r="20" stroke-width="2"/><circle cx="275" cy="345" r="20" stroke-width="2"/><circle cx="570" cy="345" r="20" stroke-width="2"/></g><g fill="currentColor" font-size="40"><text x="115" y="180">橋</text><text x="230" y="405">路地</text><text x="535" y="410">広場</text></g><text x="20" y="530" fill="currentColor" opacity="1" font-size="40">架空マップ・縮尺なし</text></svg>'''
def wave():
 return '<svg class="wave" viewBox="0 0 700 270" aria-label="音の印象を示す抽象記号。実際の波形ではありません" role="img"><g stroke="currentColor" stroke-width="3">'+''.join(f'<path d="M{x} {135-h}V{135+h}"/>' for x,h in [(x,15+int(abs(__import__('math').sin(x*.037))*85)) for x in range(10,700,12)])+'</g></svg>'
contents=[
 f'<div class="cover-object">{map_svg()}</div><div class="cover-note">架空の文化イベント企画<br>企画名 / 音を、地図にする。</div>',
 '<div class="statement-object"><div class="stat"><div class="k">散歩の時間 / 企画上の目安</div><div class="v">30<small>分</small></div><div class="c">気になる場所で足を止める。<br>遠くまで歩かなくてもいい。</div></div><div class="statement-copy">水の音。靴の音。<br>風が通り抜ける音。<br><br>街のいつもの風景を、<br>耳から見直してみる。</div></div>',
 '<div class="flow">'+''.join(f'<div class="node"><div class="n">0{i}</div><div class="t">{t}</div><div class="d">{d}</div></div>' for i,t,d in [(1,'場所をざっくり','「橋の近く」「広場の端」<br>住所や個人の行動は残さない。'),(2,'音の種類を書く','水、足音、風など。<br>聞こえたものを言葉にする。'),(3,'印象を添える','「ゆったり」「こつこつ」<br>自分の感じ方で書く。')])+'</div>',
 '<div class="example-object"><div class="records"><div class="record record-head"><span>場所</span><b>音の種類</b><span>印象</span></div>'+''.join(f'<div class="record"><span>{a}</span><b>{b}</b><span>{c}</span></div>' for a,b,c in [('橋','水音','ゆったり'),('路地','足音','こつこつ'),('広場','風','ひらける')])+'</div></div>',
 f'<div class="exhibit-object"><div>{map_svg()}</div><div class="exhibit-copy"><div class="entry">橋 / 水音<br><strong>「ゆったり」</strong></div><p>札が重なるほど、<br>街の印象が重なる。</p><p>展示への参加は別に選ぶ。<br>外したい札は、いつでも外す。</p></div></div>',
 '<div class="care-object">'+''.join(f'<div class="care-row"><span>0{i}</span><b>{t}</b><p>{d}</p></div>' for i,t,d in [(1,'参加の方法を選ぶ','散歩せず、会場で地図を読む参加も用意。'),(2,'安全な場所で止まる','私有地に入らず、車道で立ち止まらない。'),(3,'個人の情報を残さない','会話の内容や住所を書かない。録音はしない。'),(4,'展示する範囲を選ぶ','記録することと、展示することの同意を分ける。')])+'</div>',
 '<div class="closing-object"><div class="schedule"><div><span>受付</span><b>5</b><span>分 / 参加方法を選ぶ</span></div><div><span>散歩</span><b>30</b><span>分 / 安全な道で記録する</span></div><div><span>共有</span><b>15</b><span>分 / 地図と記録を読む</span></div></div><p>時間は企画上の目安。安全性と記録の負担を試す。</p></div>'
]
tails=['音源未収録。音声再生機能はありません。','30分は企画上の目安。参加実績や調査結果ではありません。','聞き取りづらいときは、見えた動きや場の印象だけでも。','記録・地名・配置はすべて架空。実測データではありません。','地図は架空の展示説明図。個人の現在地は扱いません。','実施時は、会場と歩行ルートの安全確認が必要です。','架空の企画案。日程・会場・募集人数は未定です。']
sections=[]
for i,((slot,theme,ey,title,sub),c,tail) in enumerate(zip(slides,contents,tails),1):
 theme='light' # Proposal brief: choose one paper profile, not mixed theme testing.
 sections.append(f'''<section class="slide slot-{slot}" data-slot="{slot}" data-theme="{theme}" id="slide-{i}"><div class="bg"></div><div class="deck-brand"><span class="wm">SOUND ATLAS</span></div><div class="deck-meta">架空企画 / 2026</div><div class="deck-author">音を、地図にする。</div><div class="deck-page"><b>{i:02}</b> / 07</div><div class="frame"><div class="eyebrow">{ey}</div><h1 class="action-title">{title}</h1><p class="subhead">{sub}</p>{c}<div class="tail">{tail}</div></div></section>''')
html='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>音を、地図にする。</title><link rel="stylesheet" href="assets/styles.css"><link rel="stylesheet" href="assets/adaptation.css"></head><body><main id="deck">'''+''.join(sections)+'''</main><nav aria-label="スライド送り"><button id="prev" aria-label="前の頁">←</button><span id="count">1 / 7</span><button id="next" aria-label="次の頁">→</button></nav><script src="assets/navigation.js"></script></body></html>'''
(R/'index.html').write_text(html)
(R/'input/data.json').write_text(json.dumps({'sample_type':'fictional cultural event proposal','audio_files':[],'real_location_data':False,'slides':[{'slot':s[0],'theme':'light','title':s[3].replace('<br>',''),'subtitle':s[4],'tail':t} for s,t in zip(slides,tails)]},ensure_ascii=False,indent=2))
