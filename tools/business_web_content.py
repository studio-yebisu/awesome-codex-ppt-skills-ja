"""Individually authored content for original Frontend and Guizang architectures."""
import html
e = html.escape

def frontend_cafe(d, calculations):
    profit=calculations["profit_man_yen"]
    return [
      ("運河沿いB案を、調査・交渉へ", '<div class="signal-card reveal"><p class="eyebrow" data-edit>喫茶つむぎ / 2号店出店提案</p><h1 data-edit>地域の居場所を、<br>もう一店舗。</h1></div>',
       "今日決めるのはB案の調査・交渉です。客数・工事額・店長配置を確認してから投資を判断します。"),
      ("新店の顧客と役割", '<h2 class="headline reveal" data-edit>散歩の途中に、<br>長くいられる場所を。</h2><div class="three-up"><div class="principle reveal"><span class="n">01</span><h3 data-edit>平日の近隣客</h3><p data-edit>仕事の合間に、ひと息。<br>落ち着いて滞在できる席。</p></div><div class="principle reveal"><span class="n">02</span><h3 data-edit>週末の来訪者</h3><p data-edit>散歩と買い物の途中に。<br>家族で利用できる場所。</p></div><div class="principle reveal"><span class="n">03</span><h3 data-edit>既存店との役割</h3><p data-edit>24席の既存店は日常使い。<br>新店は滞在しやすさを重視。</p></div></div>',
       "顧客像は仮説です。既存店の聞き取りと現地調査で、新店の利用場面を確かめます。"),
      ("候補地比較", '<h2 class="headline reveal" data-edit>82点。僅差だから、<br>現地で確かめる。</h2><div class="type-split"><div class="type-sample reveal"><strong data-edit>A 駅前 / 81点</strong><p data-edit>38席・賃料28万円<br>通行量と視認性に利点。</p></div><div class="type-sample reveal"><strong data-edit>B 運河沿い / 82点</strong><p data-edit>32席・賃料18万円<br>滞在環境と賃料に利点。</p></div></div><p class="annotation" data-edit>5点満点。重み：滞在30% / 通行25% / 賃料20% / 視認15% / 運営10%</p>',
       "PowerPoint版と同じ評価表です。点数だけで決めず、82人という客数計画の根拠を確かめます。"),
      ("採算と損益分岐", f'<h2 class="headline reveal" data-edit>損益分岐は、一日60人。</h2><div class="type-split"><div class="type-sample reveal"><strong class="mega" data-edit>{profit:.1f}<small>万円 / 月</small></strong><p data-edit>計画売上234.52万円<br>変動費82.08万円・固定費110万円</p></div><div class="type-sample reveal"><p data-edit>82人 × 1,100円 × 26日<br>変動費率35%。計画上の仮定。<br><br>55人 / 日なら、月7.8万円の赤字。<br>初期費用880万円は仮見積。</p></div></div><p class="annotation" data-edit>損益分岐：110万円 ÷ 65% ÷ 1,100円 ÷ 26日 → 59.2人。税・資金繰り等は別途精査。</p>',
       "数値は共通入力から計算しています。利益は保証ではありません。計画より客数が落ちた場合の試算も示します。"),
      ("運営の共通化", '<h2 class="headline reveal" data-edit>仕込みと購買を、<br>二店舗で支え合う。</h2><div class="three-up"><div class="principle reveal"><span class="n">01</span><h3 data-edit>新店</h3><p data-edit>32席の滞在型店舗。<br>店長候補の配置を先行。</p></div><div class="principle reveal"><span class="n">02</span><h3 data-edit>既存店</h3><p data-edit>仕込みの一部を支える。<br>繁忙時間の負荷を確認。</p></div><div class="principle reveal"><span class="n">03</span><h3 data-edit>共通化</h3><p data-edit>材料の購買をまとめる。<br>品質基準と日報を揃える。</p></div></div>',
       "既存店に負担が集中しないか、仕込み量と移送時間を測ります。人件費68万円は計画上の仮定です。"),
      ("契約前の確認", '<h2 class="headline reveal" data-edit>契約前に、3つを確かめる。</h2><div class="three-up"><div class="principle reveal"><span class="n">01</span><h3 data-edit>客数</h3><p data-edit>通行量を2週間調査。<br>試験販売で単価を確認。</p></div><div class="principle reveal"><span class="n">02</span><h3 data-edit>工事額</h3><p data-edit>3社へ同じ条件で見積。<br>予備費と上限を決める。</p></div><div class="principle reveal"><span class="n">03</span><h3 data-edit>店長配置</h3><p data-edit>候補者の意向を確認。<br>採用と育成の日程を確定。</p></div></div>',
       "調査で仮定が崩れた場合は計画を修正します。必要な追加資金も次の決裁で確認します。"),
      ("調査から投資決裁へ", '<h2 class="headline reveal" data-edit>5週目に、判断を置く。</h2><div class="three-up"><div class="principle reveal"><span class="n">1–2</span><h3 data-edit>現地調査</h3><p data-edit>担当：既存店長。<br>客数と利用場面を確認。</p></div><div class="principle reveal"><span class="n">3–4</span><h3 data-edit>見積・条件交渉</h3><p data-edit>新店候補店長が運営設計。<br>工事費と配置を揃える。</p></div><div class="principle reveal"><span class="n">5</span><h3 data-edit>投資決裁</h3><p data-edit>経営者が判断。<br>決裁後に内装・採用へ。</p></div></div>',
       "週数は仮の日程です。調査が不足する場合は投資決裁を延期し、開業日を先に約束しません。"),
      ("今日の決裁事項", '<div class="signal-card reveal"><p class="eyebrow" data-edit>今日の決裁 / 調査と条件交渉</p><h1 data-edit>B案を確かめて、<br>次の判断へ。</h1></div><p class="annotation" data-edit>次回に揃えるもの：客数の根拠、工事見積、店長配置。契約・投資の承認は調査後。</p>',
       "B案の調査と交渉を進めます。契約・投資承認は別の判断です。")
    ]

def frontend_git(d):
    return [
      ("作業前に、状態を見る", '<p class="terminal-kicker reveal">TEAM ONBOARDING / 15 MIN + PRACTICE</p><h1 class="terminal-title reveal" data-edit>小さく変更。<br>差分を見て、レビュー。</h1><pre class="code reveal" data-edit><span class="prompt">$</span> git status<br><span class="prompt">$</span> git diff</pre><p class="terminal-lead reveal" data-edit>作業ブランチで変更し、何を変えたか説明できるようになる。</p>',
       "新入社員向けの教材です。最初に作業ツリーと差分を確認します。Gitが管理する変更と、まだ管理していないファイルを見分けてください。"),
      ("自分のブランチで作業する", '<h2 class="headline reveal" data-edit>作業ブランチを作る</h2><pre class="code reveal" data-edit><span class="prompt">$</span> git switch -c feature/greeting<br><span class="prompt">$</span> git status</pre><div class="three-up"><div class="principle reveal"><h3 data-edit>作る</h3><p data-edit>作業用のブランチ名を付ける。</p></div><div class="principle reveal"><h3 data-edit>直す</h3><p data-edit>目的に必要なファイルだけ変更。</p></div><div class="principle reveal"><h3 data-edit>確認</h3><p data-edit>作業中のブランチと差分を見る。</p></div></div>',
       "演習ではfeature/greetingという新しいブランチを使います。既存の共同作業では、始点のブランチと作業対象を先に確認してください。"),
      ("変更を小さく記録する", '<h2 class="headline reveal" data-edit>commitの前に、差分を読む</h2><pre class="code reveal" data-edit><span class="prompt">$</span> git add README.md<br><span class="prompt">$</span> git diff --staged<br><span class="prompt">$</span> git commit -m "Add greeting"</pre><p class="terminal-lead reveal" data-edit>PRには「目的」「変更点」「確認したこと」。<br>秘密情報や無関係な変更を混ぜない。</p>',
       "addは対象ファイルを指定します。stagedの差分がcommit対象です。PRはGitHubでレビューを依頼する仕組みです。この演習で外部送信は必要ありません。"),
      ("レビューは変更の意図を読む", '<h2 class="headline reveal" data-edit>3つの観点で確認する</h2><div class="three-up"><div class="principle reveal"><span class="n">01</span><h3 data-edit>目的</h3><p data-edit>この変更で何を直すのか。<br>対象は説明と一致しているか。</p></div><div class="principle reveal"><span class="n">02</span><h3 data-edit>差分</h3><p data-edit>意図しないファイルはないか。<br>秘密情報が混ざっていないか。</p></div><div class="principle reveal"><span class="n">03</span><h3 data-edit>確認</h3><p data-edit>手元で何を確かめたか。<br>指摘の理由が具体的か。</p></div></div>',
       "レビューでは変更の意図と実際の差分を対応させます。直し方だけでなく、困る具体的な場面を伝えると相談しやすくなります。"),
      ("競合は、両方の意図を読んで解く", '<h2 class="headline reveal" data-edit>片方を消す前に、相談する</h2><div class="type-split"><pre class="code reveal" data-edit>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD<br>現在の変更<br>=======<br>取り込む変更<br>&gt;&gt;&gt;&gt;&gt;&gt;&gt; branch</pre><div class="type-sample reveal"><p data-edit>1. git statusで対象を確認<br>2. 両方の意図を読む<br>3. 解消して実行を確認<br>4. 対象だけaddし、mergeを完了</p></div></div>',
       "ここではmerge中の競合を説明しています。自分の変更を一律に採用する操作で済ませず、結果を確認します。rebaseなどは手順が異なるので、その作業の正本に従ってください。"),
      ("20分のローカル演習", '<h2 class="headline reveal" data-edit>挨拶を一行、変更してみる</h2><div class="three-up"><div class="principle reveal"><span class="n">01</span><h3 data-edit>準備</h3><p data-edit>input/trainingを作業用にコピー。<br>git initし、初期状態をcommit。</p></div><div class="principle reveal"><span class="n">02</span><h3 data-edit>変更</h3><p data-edit>feature/greetingを作る。<br>README.mdに挨拶を一行追加。</p></div><div class="principle reveal"><span class="n">03</span><h3 data-edit>説明</h3><p data-edit>diff → add → diff --staged。<br>commitし、目的を相手に説明。</p></div></div>',
       "演習用のREADMEを同梱しています。手元の実業務リポジトリを練習のために改変しないよう、別の作業用フォルダーへコピーして実施してください。"),
      ("終了時の確認", '<h2 class="headline reveal" data-edit>何を変えたか、説明できる</h2><pre class="code reveal" data-edit><span class="prompt">$</span> git status<br><span class="prompt">$</span> git log -1 --oneline</pre><p class="terminal-lead reveal" data-edit>ブランチ・対象ファイル・変更の目的を確認。<br>addを外すだけなら git restore --staged README.md<br>作業中の内容を消す操作とは区別する。</p>',
       "git restore --stagedはステージから外す操作で、作業ツリーの編集を取り消す意味ではありません。戻したい対象を取り違えないようにしてください。公式GitとGitHubの文書を入力資料に記載しています。")
    ]

def magazine_port(d):
    route_copy={"港の案内所":"地図と回遊カード<br>を受け取る","朝市通り":"旬の食材と<br>店主の話","路地の食堂":"地元の<br>昼ごはん","ガラス工房":"制作見学と<br>小物選び","旧灯台":"海を見る休憩と<br>記念写真"}
    def experience(p):return "感想を記入して<br>帰着" if p["time"]=="15:00" else route_copy[p["stop"]]
    def header(n): return f'<div class="chrome"><div>SHIOMI / WEEKEND WALK</div><div>{n:02d} / 07</div></div>'
    def footer(): return '<div class="foot"><div>架空の港町・企画によるサンプル</div><div>八百万図AIツールボックス</div></div>'
    raw=[
      ("週末の汐見港町", "hero dark", "hero", '<div class="kicker" data-anim>地域回遊 / 企画提案</div><h1 class="h-hero" data-anim>港町の、<br>半日をつなぐ。</h1><p class="lead" data-anim>市場・食・工房・灯台。<br>一本の徒歩行程で、町との出会いを増やす。</p>',
       "架空の汐見港町で行う週末回遊の企画です。商店会の合意を得て、2週末の試行へ進むことを提案します。"),
      ("対象者と体験", "light", "quote", '<div class="kicker" data-anim>THE VISITOR</div><h2 class="h-xl" data-anim>日帰りの来訪者へ。</h2><div class="case-mag-split"><p class="case-quote" data-anim>車を置いたら、<br>町を歩く。</p><p class="lead" data-anim>徒歩で半日を楽しめる人が対象。<br><br>店の場所だけでなく、<br>「次にどこへ行くか」を案内する。</p></div>',
       "来訪者全員を対象にするのではなく、徒歩で半日過ごせる人へ絞ります。店を点で紹介するだけでは回り方が分かりにくいため、次の行先まで案内します。"),
      ("4時間の徒歩行程", "dark", "grid-reveal", '<div class="kicker" data-anim>THE WALK / ABOUT 4 KM</div><h2 class="h-xl" data-anim>港から灯台へ、戻る。</h2><div class="case-route">'+''.join(f'<div data-anim><strong>{e(p["time"])}</strong><h3>{e(p["stop"])}</h3><p>{experience(p)}</p></div>' for p in d["itinerary"])+'</div><p class="lead" data-anim>11:00〜15:00 / 約4km / 架空の計画。現地で歩行時間を確認。</p>',
       "市場での買い物、食堂の昼食、工房見学、灯台の休憩を一本の行程にまとめます。時間と距離は仮の計画で、実施前に実測します。"),
      ("集客と、次の店への案内", "light", "grid-reveal", '<div class="kicker" data-anim>BEFORE / DURING / AFTER</div><h2 class="h-xl" data-anim>一度の案内で、終わらせない。</h2><div class="case-mag-three"><div data-anim><h3>来る前</h3><p>商店会の案内に<br>半日行程を載せる。<br>駐車場からの入口を示す。</p></div><div data-anim><h3>歩く途中</h3><p>各店で回遊カードを渡す。<br>次の行先と<br>所要時間を伝える。</p></div><div data-anim><h3>帰るとき</h3><p>感想カードを回収。<br>別の季節の行程も知らせる。</p></div></div>',
       "回遊カードと各店の案内を揃えます。全店舗で同じ地図と時間案内を使い、営業日を前日に確かめます。"),
      ("4日間の試行と運営", "dark", "stats", '<div class="kicker" data-anim>PILOT OPERATION</div><h2 class="h-xl" data-anim>2週末、4日間で試す。</h2><div class="grid-3"><div class="stat-card" data-anim><div class="stat-nb">2<span class="stat-unit"> 人</span></div><div class="stat-note">案内スタッフ / 日</div></div><div class="stat-card" data-anim><div class="stat-nb">28<span class="stat-unit"> 万円</span></div><div class="stat-note">仮予算：案内6・人員16・調整6</div></div><div class="stat-card" data-anim><div class="stat-nb">4<span class="stat-unit"> 日</span></div><div class="stat-note">参加店舗の合意後に日程を確定</div></div></div><p class="lead" data-anim>雨天は短縮。混雑は時間指定で分散。営業時間を前日に確認。</p>',
       "予算は架空の計画値です。案内物6万円、スタッフ16万円、記録と調整6万円の合計28万円。雨天時の短縮と混雑時の分散をあらかじめ決めます。"),
      ("試行の測り方", "light", "stats", '<div class="kicker" data-anim>MEASURE THE PILOT</div><h2 class="h-xl" data-anim>売上効果を、急いで断定しない。</h2><div class="case-mag-three"><div data-anim><h3>60人以上</h3><p>参加者の目標。<br>案内所で匿名カードを渡す。</p></div><div data-anim><h3>40%以上</h3><p>全行程を回る人の目標。<br>各店で印を付ける。</p></div><div data-anim><h3>70%以上</h3><p>カード回収率の目標。<br>帰着時の感想も記録。</p></div></div><p class="lead" data-anim>数字は目標。来街者全体の売上効果は、この試行だけでは判断しない。</p>',
       "表示した数値は実績ではなく目標です。参加者の回遊をカードで記録し、来街者全体の売上効果とは分けて評価します。"),
      ("次の判断", "hero dark", "hero", '<div class="kicker" data-anim>THE NEXT WEEKEND</div><h1 class="h-hero" data-anim>小さく歩いて、<br>次の行程へ。</h1><p class="lead" data-anim>商店会の合意 → 現地で時間確認 → 4日の試行。<br>回収したカードを見て、続け方を決める。</p>',
       "参加店舗の合意、現地の時間確認、試行日程の決定へ進みます。試行の記録を確認して継続や変更を判断します。")
    ]
    return [(title,f'<section class="slide {classes}" data-slide-id="page-{i}" data-animate="{recipe}">{header(i)}<div class="frame case-mag-frame">{content}</div>{footer()}</section>',note) for i,(title,classes,recipe,content,note) in enumerate(raw,1)]

def swiss_knowledge(d):
    def header(n): return f'<div class="chrome-min"><div class="l">INTERNAL KNOWLEDGE / PROPOSAL</div><div class="r">{n:02d} / 08</div></div>'
    def head(k,title): return f'<div class="case-swiss-head" data-anim><div class="t-meta">{k}</div><h2 class="h-xl-zh">{title}</h2></div>'
    def stack(items): return '<div class="stack-row">'+''.join(f'<article class="card-fill sub-card" data-anim><span class="big-num">{i:02d}</span><h4>{e(h)}</h4><p>{e(p)}</p></article>' for i,(h,p) in enumerate(items,1))+'</div>'
    raw=[
      ("社内ナレッジ検索 導入提案","accent","SWISS-COVER-ASCII","hero",'<canvas class="ascii-bg" aria-hidden="true"></canvas><div class="case-swiss-cover"><div class="t-meta">社内業務改善 / 4週間の試作</div><h1>探す時間を、<br>仕事の時間へ。</h1><p class="lead">資料の版・所有者・閲覧範囲を揃え、<br>現行の手順へ辿り着ける検索を作る。</p></div>',
       "架空の50人のソフトウェア会社を想定します。今日の提案は台帳と全文検索の4週間の試作です。回答生成や全社展開はこの時点で決めません。"),
      ("3つの利用場面","","S05","sub-stack",head("USE CASES","現行の手順に、辿り着く。")+stack([("出張精算","現行の規程と手順を探す。"),("初期設定","開発環境の設定手順を探す。"),("顧客対応","最新版のテンプレートを探す。")])+ '<p class="case-swiss-note">対象はまず30資料。所有者と公開範囲が分かる資料から始める。</p>',
       "用途は資料を探すことです。複数フォルダーに分かれた資料で、現行版と所有者が分からず聞き直す課題を解きます。"),
      ("資料・索引・検索の構成","","S17","system-draw",head("SYSTEM","検索する前に、権限を照合。")+'<div class="system-diagram case-system"><div data-anim>資料台帳<br><small>所有者・版・公開範囲</small></div><span>→</span><div data-anim>検索索引<br><small>更新時刻と権限を同期</small></div><span>→</span><div data-anim>検索結果<br><small>根拠リンク・最終更新日</small></div></div><div class="case-swiss-three"><p>利用者の本人情報を確認</p><p>閲覧権限内を検索対象にする</p><p>資料そのものへ戻れるリンク</p></div>',
       "権限外の資料を先に検索してから画面で隠す設計にはしません。閲覧範囲を索引へ反映し、検索前に照合します。生成された回答だけに依存せず根拠へ戻れるようにします。"),
      ("導入方式の比較","","S05","sub-stack",head("OPTIONS","まず、台帳と全文検索。")+stack([(p["name"],p["scope"]+"。"+p["issue"]) for p in d["options"]])+ '<p class="case-swiss-note">回答支援の追加費用は、検索の評価後に見積。製品価格や性能比較ではありません。</p>',
       "現行運用、台帳と全文検索、回答支援追加の三案です。まず小さく資料検索を試し、質問と資料の語句が違う場面を評価します。"),
      ("4週間の段階導入","","S11","timeline-horizontal",head("PILOT PLAN","4週目に、継続を判断。")+'<div class="timeline-h">'+''.join(f'<div class="tl-node" data-anim><span class="big-num">{i:02d}</span><h4>{e(p.split("：")[0])}</h4><p>{e(p.split("：")[1])}</p></div>' for i,p in enumerate(d["phases"],1))+'</div><p class="case-swiss-note">作業順序の計画。見積・担当者の合意後に着手する。</p>',
       "最初の週に対象資料を整理、2週目に台帳と索引、3週目に利用テスト、4週目に継続を判断します。ここは実績ではなく導入の計画です。"),
      ("所有者・権限・更新","","S05","sub-stack",head("OWNERSHIP","資料と検索を、誰が保つか。")+stack([("資料所有者","現行版の指定と更新を担当。"),("情報システム","権限・索引・監査を担当。"),("利用部門","質問と正解を作り、確認する。")])+'<p class="case-swiss-note">公開範囲の変更や削除を索引へ反映。検索に旧版が残る状態を点検する。</p>',
       "導入した後の更新まで担当を決めます。公開範囲の変更と削除が検索索引に反映されることを、権限の試験で確かめます。"),
      ("試作の評価条件","","S05","sub-stack",head("ACCEPTANCE","試す前に、合格条件を決める。")+stack([("24 / 30問","正しい現行資料へ到達する目標。"),("0 / 20ケース","権限外資料の露出はゼロ。"),("翌営業日","資料更新の反映期限。")])+'<p class="case-swiss-note">事前に質問と正解資料を作る。未達なら、対象と設計を修正して再評価。</p>',
       "表示した値は導入の判定基準です。実測した結果として表示していません。正解資料を事前に確定し、権限外資料を含む試験を行います。"),
      ("導入の判断","split","SWISS-CLOSING-ASCII","split-statement",'<div class="half b-accent"><canvas class="ascii-bg" aria-hidden="true"></canvas><h2 class="case-closing-title" data-anim>小さく探して、<br>確かめる。</h2></div><div class="half"><div class="chrome-min"><div>DECISION</div><div>04 WEEKS</div></div><div class="case-takeaways" data-anim><h3>01　30資料から始める</h3><p>台帳と全文検索を試作。</p><h3>02　権限と更新を試す</h3><p>正解資料と制約を事前に用意。</p><h3>03　評価後に、次を決める</h3><p>回答生成と全社展開は別途判断。</p></div></div>',
       "まず4週間の試作を進める判断をお願いします。検索の評価が整ってから、回答生成を追加するか、全社へ広げるかを別途決めます。")
    ]
    out=[]
    for i,(title,classes,layout,recipe,content,note) in enumerate(raw,1):
        chrome="" if classes=="split" else header(i)
        out.append((title,f'<section class="slide {classes}" data-layout="{layout}" data-slide-id="page-{i}" data-animate="{recipe}"><div class="canvas-card">{chrome}{content}<div class="case-sample-label">架空の組織・導入計画によるサンプル</div></div></section>',note))
    return out
