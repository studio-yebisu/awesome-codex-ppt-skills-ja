"""Prepare ConnorRX56's original HTML-first / native-PPTX delivery example."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT/'examples/repositories/presentation-delivery'
UP = ROOT/'.build/actual-upstreams/ConnorRX56__presentation-delivery-skills'
REPO = 'ConnorRX56/presentation-delivery-skills'
PIN = '06ddac077030c62f0118b225860cac46fbf658ea'

def dump(p, v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

PAGES = [
 {'title':'引き継ぎは、次の一手まで。','tone':'dark','role':'cover',
  'content':'<h1 class="hero">引き継ぎは、<br>次の一手まで。</h1><p class="lead">ファイルを渡すだけで終わらせない。<br>次の人が動ける案内を添える。</p><div class="handoff"><p>資料</p><p class="arrow">→</p><p>確認</p><p class="arrow">→</p><p>次の行動</p></div>',
  'note':'社内の資料引き継ぎに使える考え方をまとめた説明例です。実在の会社の規程や、測定済みの運用実績を示すものではありません。'},
 {'title':'渡す前に、三つをそろえる','tone':'light','role':'three_items',
  'content':'<h1>渡す前に、三つをそろえる</h1><div class="three"><div><p class="tag">何のため？</p><h2>用途</h2><p>誰が、何を判断するための<br>資料かを一文で書く。</p></div><div><p class="tag">どこにある？</p><h2>場所</h2><p>開くファイルと参照資料の<br>置き場所をまとめる。</p></div><div><p class="tag">何をする？</p><h2>次の行動</h2><p>確認する人と、返してほしい<br>内容・期日を添える。</p></div></div><p class="bottom-line">受け取った人が、最初に読む順番で並べる。</p>',
  'note':'用途・場所・次の行動を別々に書きます。保存先の一覧だけで終わらず、受け取り手が最初にすることまで説明します。'},
 {'title':'ファイル名で、用途と版を伝える','tone':'light','role':'filename',
  'content':'<h1>ファイル名で、用途と版を伝える</h1><p class="lead">同じ資料の「最新版はどれ？」を減らすために。</p><div class="filename"><p>新人案内_v03_確認用.pptx</p></div><div class="three compact"><div><p class="tag">用途</p><h2>新人案内</h2><p>中身がわかる名前</p></div><div><p class="tag">版</p><h2>v03</h2><p>更新順がわかる印</p></div><div><p class="tag">状態</p><h2>確認用</h2><p>公開・配布前とわかる印</p></div></div><p class="bottom-line">これは記入例。チームで使う命名ルールに合わせる。</p>',
  'note':'新人案内_v03_確認用.pptxは架空の記入例です。既存の命名ルールがあるチームでは、そのルールを優先してください。v03や確認用の印が、正式承認を証明するわけではありません。'},
 {'title':'完了と保留を、書き分ける','tone':'dark','role':'status',
  'content':'<h1>完了と保留を、書き分ける</h1><p class="lead">次の人が、途中から迷わず続きを始められるように。</p><div class="status"><div><p class="tag">完了の記入例</p><h2>本文を更新した</h2><p>変更箇所：2〜4ページ<br>残した根拠：更新メモ</p></div><div><p class="tag">保留の記入例</p><h2>担当者の確認待ち</h2><p>確認事項：問い合わせ先<br>次の対応：窓口へ確認する</p></div></div><p class="bottom-line">「作った」「確認した」「承認された」を混ぜない。</p>',
  'note':'完了と保留の欄は架空の記入例です。この作例の実際の確認状態とは別です。作業した事実と、内容確認や正式承認の有無を書き分ける考え方を示しています。'},
 {'title':'受け取る側の画面で、確かめる','tone':'light','role':'checks',
  'content':'<h1>受け取る側の画面で、確かめる</h1><div class="checks"><div><p class="step">1</p><h2>開けるか</h2><p>渡すファイルとリンクを開く。<br>必要なアクセス権も確認する。</p></div><div><p class="step">2</p><h2>読めるか</h2><p>全ページの文字・図・表を見る。<br>字体の置き換わりにも気を配る。</p></div><div><p class="step">3</p><h2>編集できるか</h2><p>編集が必要なら、コピーで試す。<br>元の資料を保って確認する。</p></div></div><p class="bottom-line">自分の端末で成功しただけで、受け取り手にも同じとは決めない。</p>',
  'note':'受け取る側での確認は、資料を実際に配布するときの手順例です。この制作で外部の受け取り手に送信したり、他人のアクセス権を変更したりはしていません。'},
 {'title':'最後に、次の一行を添える','tone':'light','role':'closing',
  'content':'<p class="kicker">引き継ぎメッセージの記入例</p><h1 class="hero closing">最後に、<br>次の一行を添える。</h1><div class="message" data-pptx-merge="true"><p>確認担当の方へ：問い合わせ先の表記をご確認ください。</p><p>期日は合意した日付を記入し、修正点を更新メモへお願いします。</p></div><p class="bottom-line">資料の場所と、次の行動を一緒に渡す。</p>',
  'note':'確認担当者と期日は、その場で合意した内容に置き換えるための記入例です。期日を勝手に決めず、渡す人と受け取る人が次の行動を共有することが目的です。'}
]

def prepare():
    if not (UP/'ACQUISITION.json').exists():
        raise RuntimeError('Acquire the pinned original source before preparation')
    receipt=json.loads((UP/'ACQUISITION.json').read_text(encoding='utf-8'))
    assert receipt['commit']==PIN
    refs=receipt['files']
    for ref in refs:
        p=UP/ref['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==ref['sha256']
        q=CASE/'source/upstream'/ref['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    shutil.copy2(UP/'ACQUISITION.json',CASE/'source/upstream/ACQUISITION.json')
    for name,path in [('LICENSE-upstream.txt','LICENSE'),('LICENSE-visual-deck-studio.txt','skills/visual-deck-studio/LICENSE')]:
        q=CASE/'licenses'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UP/path,q)
    for weight in ['Regular','Bold']:
        src=ROOT/'.build/fonts'/('BIZUDPGothic-'+weight+'.ttf')
        record=next(f for f in json.loads((ROOT/'data/fonts.json').read_text(encoding='utf-8')) if f['family']=='bizudpgothic' and weight.lower() in f['file'])
        assert hashlib.sha256(src.read_bytes()).hexdigest()==record['source_sha256']
        q=CASE/'shared/fonts'/src.name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,q)
    shutil.copy2(ROOT/'assets/fonts/bizudpgothic-OFL.txt',CASE/'licenses/OFL-BIZUDPGothic.txt')
    dump(CASE/'shared/fonts/SOURCE.json',[{**{k:f[k] for k in ['family','license','source_url','license_url','commit','source_sha256','source_bytes']},
         'file':'shared/fonts/'+('BIZUDPGothic-Bold.ttf' if 'bold' in f['file'] else 'BIZUDPGothic-Regular.ttf'),
         'modification':'Unmodified full original TTF; no font renaming or subset.','distributed_sha256':f['source_sha256']} for f in json.loads((ROOT/'data/fonts.json').read_text(encoding='utf-8')) if f['family']=='bizudpgothic'])
    inp=CASE/'input/data.json'
    if not inp.exists():
        dump(inp,{'id':'presentation-delivery','title':PAGES[0]['title'],'sample_notice':'会社・ファイル名・作業状況は説明用の架空の記入例。会社の規程や実績ではありません。',
                  'style_context':{'source':'Existing catalog assets/case-studio.css','paper':'#f7f5ee','ink':'#203e31','font':'BIZ UDPGothic','width_px':1280,'height_px':720},'pages':PAGES})
    text='# 制作条件\n\n社内で資料を引き継ぐ人へ、次の人が動ける案内の作り方を日本語6枚で説明する。架空のファイル名と作業状況の例は記入例と明示する。既存カタログの紙色・深緑を参考に、BIZ UDPGothicの太字と本文を組む。\n\n原典のPath A（HTML先行・960×540pt）、deck_index.htmlの原典概覧、原典html2pptx.jsの検査・要素変換、原典PDF結合を使う。内容は資料の引き継ぎの説明で、カタログやスキル自体の宣伝ではない。\n\n## 制作判断\n\n- 読み手：社内で資料を渡す人。画面共有・PC閲覧を想定。\n- 目的：用途・保存先・次の行動がそろった引き継ぎにする。\n- 題材固有の形：資料→確認→次の行動の連なりと、完了／保留の対照。\n- 原典の質問工程は、ユーザーの実装委任に基づき制作側の仮定を記録して進める。人の早期承認・正式採用とは扱わない。\n- 実在の製品名、ブランド、実績の数値、装飾写真は使わない。既存の明示された設計文脈があるため3案のFallback工程は未実施。\n- 最初に封面と完了／保留の2枚を制作・表示確認し、残りを制作する。\n'
    (CASE/'input/BRIEF.md').write_text(text,encoding='utf-8')
    prompt='ConnorRX56/presentation-delivery-skillsのvisual-deck-studio原典を使い、社内向け「引き継ぎは、次の一手まで。」を日本語6枚で作る。HTML-first Path Aの960×540ptと4条件を守り、原典deck_index.html、html2pptx.js、PDF exporterを使用する。原典の検査を保ち、本文と単純図形をPowerPointで編集可能にする。既存カタログの紙色・深緑とBIZ UDPGothicを参考にする。ファイル名や作業状況の例は架空と明記し、発表ノートを付ける。2枚の表示確認後に全6枚を作り、HTTPのHTML、PDF、PowerPoint本体で表示を確認する。\n'
    (CASE/'PROMPT.txt').write_text(prompt,encoding='utf-8')
    (CASE/'NOTES.md').write_text('\n\n'.join(f'## {i+1}. {p["title"]}\n\n{p["note"]}' for i,p in enumerate(PAGES))+'\n',encoding='utf-8')
    shutil.copy2(ROOT/'tools/render_powerpoint.ps1',CASE/'source/render_powerpoint.ps1')
    return CASE

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');parser.add_argument('--showcase',action='store_true');parser.add_argument('--powerpoint',action='store_true');parser.add_argument('--node')
    args=parser.parse_args();prepare()
    if not args.prepare_only:
        command=[sys.executable,str(CASE/'source/reproduce.py')]
        if args.showcase:command+=['--showcase']
        if args.powerpoint:command+=['--powerpoint']
        if args.node:command+=['--node',args.node]
        raise SystemExit(subprocess.call(command,cwd=CASE))
