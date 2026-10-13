"""Prepare the original att6113 template example; never use the catalog renderer."""
from pathlib import Path
import json, shutil, hashlib
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/ppt-design-system'
UP=ROOT/'.build/actual-upstreams/att6113__ppt-design-system'
def write(name,text):
 p=CASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def main():
 for folder in ['input','source','review','render','licenses']: (CASE/folder).mkdir(parents=True,exist_ok=True)
 for name in ['SKILL.md','README.md','LICENSE','assets/template.html','references/themes.md','references/layouts.md','references/presets.md','ACQUISITION.json']:
  target=CASE/'source/upstream'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UP/name,target)
 shutil.copy2(UP/'LICENSE',CASE/'licenses/LICENSE-upstream.txt')
 pages=[
 {'title':'雨の日も迷わない、図書館イベント案内','tone':'hero dark','kicker':'雨の午後に、本と出会う','body':'<h1 class="h-hero">雨の日も迷わない、<br>図書館イベント案内</h1><p class="lead">出発前・入口・会場。<br>三つの確認で、落ち着いて参加する。</p><div class="meta-row">架空の「みどり図書館」読書会を使った案内例</div>','note':'架空の図書館と読書会を使った参加案内です。実際の開催情報ではありません。'},
 {'title':'まず、今日の予定を確認','tone':'light','kicker':'例の読書会について','body':'<h2 class="h-xl">まず、今日の予定を確認</h2><div class="grid-6">'+''.join(f'<div class="stat-card"><div class="stat-label">{a}</div><div class="stat-nb">{b}</div><div class="stat-note">{c}</div></div>' for a,b,c in [('開始','14:00','受付は13:45から'),('所要時間','60<span class="stat-unit">分</span>','15:00終了予定'),('会場','2<span class="stat-unit">階</span>','交流室'),('参加費','無料','予約者向けの読書会'),('持ち物','1<span class="stat-unit">冊</span>','紹介したい本'),('入口','正面','傘は入口の傘立てへ')])+'</div><p class="lead">この予定は説明用の設定です。参加する催しの案内に置き換えてください。</p>','note':'日時や会場は説明用の架空の設定です。実際のイベントでは主催者の案内を確認してください。'},
 {'title':'出発前に、案内をもう一度','tone':'light','kicker':'家を出る前のひと手間','body':'<h2 class="h-xl">出発前に、案内をもう一度</h2><p class="lead">開催状況と会場変更を、主催者の最新のお知らせで確認。<br>予約済みなら、受付で見せる画面をすぐ開けるように。</p><div class="callout">保存するのは「日時・会場・問い合わせ先」。<br>スクリーンショットにも、更新日を残す。</div><p class="lead">判断に迷ったら、案内に載っている窓口へ。<br>雨の強さだけで開催・中止を決めつけない。</p>','note':'予約確認画面や主催者の案内を用意しておくと、出発時と受付で確認しやすくなります。'},
 {'title':'着いたら、どこへ？','tone':'hero dark','kicker':'入口で、ひと呼吸','body':'<h1 class="h-hero">着いたら、<br>どこへ？</h1><p class="lead">まずは入口の掲示で、イベント名と会場を照合。<br>見つからなければ、受付でイベント名を伝える。</p>','note':'館内の配置を想像で決めず、入口の掲示と受付を起点に会場を確認する案内です。'},
 {'title':'お知らせに合わせて、次の行動を','tone':'dark','kicker':'会場の掲示を読んだら','body':'<h2 class="h-xl">お知らせに合わせて、次の行動を</h2><div class="grid-2-6-6 compare"><div class="before-col"><div class="col-header">予定どおりの案内</div><h3 class="h-sub">受付へ進む</h3><ul class="col-list"><li>イベント名と開始時刻を確かめる</li><li>傘を片づけ、予約画面を用意する</li><li>会場へは館内表示に沿って進む</li></ul></div><div class="after-col"><div class="col-header">変更・中止のお知らせ</div><h3 class="h-sub">変更内容を確かめる</h3><ul class="col-list"><li>会場だけの変更か、開催中止かを読む</li><li>新しい会場と時刻を確認する</li><li>不明点は受付で聞いてから移動する</li></ul></div></div>','note':'同じ重さの二つの行動なので、原典Before/Afterの低い不透明度だけを読みやすく調整しました。'},
 {'title':'確認するのは、この三つ。','tone':'hero light','kicker':'次に参加するときは','body':'<h1 class="h-hero">確認するのは、<br>この三つ。</h1><p class="lead closing">開催状況　／　入口　／　会場</p><p class="lead">最新の案内を保存して、余裕を持って出発。<br>迷ったら、イベント名を添えて受付へ。</p>','note':'最後に、参加前に覚えておく確認事項を三つに絞ります。架空の案内をそのまま実際の開催情報として使わないでください。'}]
 data={'id':'ppt-design-system','title':pages[0]['title'],'theme':'Forest Ink','sample_notice':'図書館名・読書会・時刻・会場は架空の説明例です。実際の開催案内ではありません。','pages':pages}
 write('input/data.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 write('input/BRIEF.md','# 制作条件\n\n雨の日に図書館イベントへ参加する一般の人へ、出発前から受付までを6ページで案内する。架空の図書館・読書会の設定を明記。原典のHTMLテンプレート、Forest Inkの配色、見出し・本文・メタ情報の三層、暗明の交替を使う。\n')
 write('PROMPT.txt','att6113/ppt-design-systemの原典SKILLとassets/template.htmlを使い、「雨の日も迷わない、図書館イベント案内」を日本語6ページにする。Forest Ink配色、原典の見出し階層、カバー・数値カード・本文・問い・比較・終わりのレイアウトを使う。本文は架空の読書会への参加案内として役に立つ内容にし、製品の説明書にしない。原典の矢印キー・ドット・横スクロールを保持する。日本語フォントは端末のフォントを使い、外部フォントを不要にする。\n')
 write('NOTES.md','\n\n'.join(f'## {i+1}. {p["title"]}\n\n{p["note"]}' for i,p in enumerate(pages))+'\n')
 print(CASE)
if __name__=='__main__':main()
