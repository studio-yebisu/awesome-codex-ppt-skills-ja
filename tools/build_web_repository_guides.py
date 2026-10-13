"""Repository-specific Japanese usage, rather than generic prompts attached to cards."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RECIPES={
 'revealjs-skill':{
  'execution_type':'scaffold_cli_then_skill_authoring','summary_ja':'reveal.jsの骨格を公式スクリプトで生成し、日本語の説明・表・発表ノートを組む。横方向の移動とスライドの演出に向く。',
  'requirements':['Node.js 24.18（今回使用）','reveal.js 5.2.1（公式MIT版を同梱）','スキルを読んでHTML/CSSを書けるエージェント'],
  'commands':['node skills/revealjs/scripts/create-presentation.js --structure 1,1,1,1,1,1 --title "社内検索を4週間で試す" --output my-deck.html'],
  'steps':['日本語版スキル一式を取得しSKILL.mdを読む','原典のscaffoldで必要なページ構成を作る','pt単位の文字とレイアウトで、入力原稿・図・表・ノートを組む','同梱したreveal.jsを使ってHTMLを開く。矢印キーで移動し全ページを見る'],
  'limitations':['今回確認したのは横6ページの再生・表・日本語書体・ノート。チャートプラグインは使っていません。'],
  'fork':'revealjs-skill-ja'},
 'lewis-html-ppt':{
  'execution_type':'template_scaffold_and_instruction_skill','summary_ja':'HTML PPT StudioのTech Sharingテンプレートを実際に展開。Git入門の本文とコードを載せ、8ページの原典runtimeで再生。',
  'requirements':['Git for WindowsのBash（scaffold用）','ブラウザ','HTMLを書けるエージェント'],
  'commands':['bash scripts/new-deck.sh my-talk ./output -t tech-sharing'],
  'steps':['日本語版スキル一式を取得。原典のテーマとfull-deck一覧を読む','new-deck.shで用途に合うデッキを展開','固有の部品・style.css・runtime.jsを保って本文とコード・発表メモを差し替える','index.htmlを開き矢印キーで移動。Sは原典の発表者ウィンドウ'],
  'limitations':['今回確認したのはTech Sharingの8ページ。全36テーマの実制作・発表者ウィンドウの全機能は未検証。'],
  'fork':'html-ppt-studio-ja'},
 'minorun-marp':{
  'execution_type':'instruction_skill_and_marp_cli','summary_ja':'みのるんの日本語スキルで、問いと段階的な図解を使う黒地の登壇資料を制作。原稿はMarpのMarkdownとして編集できる。',
  'requirements':['Node.js 24.18','Marp CLI 4.4.0','元スキルを読めるエージェント','PDF書出しにはChrome系ブラウザと原典の検査ツール'],
  'commands':['npx @marp-team/marp-cli@4.4.0 --no-stdin deck.md --html --theme minorun-dark.css --allow-local-files -o index.html','python tools/check-ai-smell.py deck.md'],
  'steps':['原著のslide-story・slide-figures・slide-design-darkを読む','話の骨子を先に作る。今回はGitの保存先を一段ずつ開示','原典のminorun-dark.cssを保持してMarkdownとSVGを制作','Marpで書き出し、図・文字・ページ移動を実表示で確認'],
  'limitations':['原著自体が日本語。今回の派生は再制作用の入力・図と公式OFL由来のNoto Sans JPを添付。Marp原稿からのHTML再生を検証。'],
  'fork':'minorun-marp-ja'},
 'neon-slides':{
  'execution_type':'locked_html_template_instruction_skill','summary_ja':'Neonのテンプレートと部品集で、橙と青の技術説明資料を制作。固有のナビゲーション・ページジャンプを保つ単一HTML。',
  'requirements':['ブラウザ','HTMLを編集できるエージェント'],
  'commands':[],
  'steps':['原典template.htmlとcomponents.mdを読む','テンプレート全体を複製し、deck内のsectionへ日本語本文を組む','cover・compare・layers・stepsの部品を使い、原典の配色とナビゲーションを保持','Noto Sans JPとSpace Groteskを同梱し、完成HTMLを開く'],
  'limitations':['PowerPointの出力経路はありません。今回の作例は単一HTMLの6ページ。日本語書体と初期ページ数の表示を調整。'],
  'fork':'neon-slides-ja'},
 'qiaomu-bento':{
  'execution_type':'json_document_and_pinned_bento_shell','summary_ja':'固定版BentoのJSON文書を生成。編集可能な要素と表を使い、権限確認から出典付き回答へ同じ要素が動いてつながる資料。',
  'requirements':['Python 3.13','スキルに同梱されたBento shell v1.0.10','ブラウザ'],
  'commands':['python scripts/bento_deck.py locate','python scripts/bento_deck.py build deck.json --output deck.bento.html --new-document --report validation.json'],
  'steps':['スキル内のworkflow・固定版format/agentsを読む','入力をJSONのtext/shape/tableと安定したidへ組む','bento_deck.pyで構築・検証する。文書以外のshellを保持','編集版で内容を変更し、readonly再生版でmorphとページ移動を確認'],
  'limitations':['編集版と再生版を別ファイルで同梱。既存文書を再構築するときは--identity-sourceでdocIdを保持する。ネット上の最新版へ差し替えない。'],
  'fork':'qiaomu-bento-ja'},
 'make-slide':{
  'execution_type':'theme_reference_html_and_instruction_skill','summary_ja':'Data Focusの実テンプレートを使い、指標・比較・棒グラフ・ドーナツ・対応手順で日本語の月次資料を制作。',
  'requirements':['ブラウザ','元スキルと選んだtheme/reference.htmlを読めるエージェント'],
  'commands':[],
  'steps':['SKILL.mdとData FocusのREADME/reference.htmlを読む','実テンプレートの各スライド種別を、必要な論点に合わせて選ぶ','本文・ノートと、棒の高さ・円の角度・凡例を入力データへ合わせる','元のgo/notesを使って全ページを確認する'],
  'limitations':['CSSグラフは数値の表示だけでなく、高さ・角度の更新も必要。今回のグラフ値は元入力と一致することを確認。'],
  'fork':'make-slide-ja'},
 'frontend-editable':{
  'execution_type':'instruction_skill_and_original_editable_runtime','summary_ja':'ブラウザ内で文字やオブジェクトを動かせるHTMLを制作。原典のSlideDeck/SlideObjectEditor/SlideSidebarで、内容の修正を続けられる。',
  'requirements':['ブラウザ','editor-runtime.mdと参照HTMLを読めるエージェント'],
  'commands':[],
  'steps':['原典のeditor-runtime.md・html-template.md・参照デッキを読む','slides-offset直下のsectionと、安定したslide id/data-oidで内容を組む','フルの編集runtimeを保持する。Eで編集、Ctrl+Sで保存、Undo/Redoで戻す','ページ一覧と本文を確認し、HTMLとして取得する'],
  'limitations':['今回使用したのは参照HTMLのオブジェクト編集方式。34テンプレートの全移植やPPT/PDF入力は未検証。'],
  'fork':'frontend-editable-ja'}
}

if __name__=='__main__':
    cases=json.loads((ROOT/'data/web-repository-examples.json').read_text(encoding='utf-8'))
    profiles=[]
    for c in cases:
        if c['id'] not in RECIPES:continue
        profile=dict(RECIPES[c['id']])
        profile.update(repository=c['repository'],example_ids=[c['id']],method_ja=c['method'],
                       license='Apache-2.0' if c['id']=='minorun-marp' else 'MIT',
                       license_review_status='reviewed_for_example',source_refs=[])
        proof=json.loads((ROOT/c['provenance']).read_text(encoding='utf-8'))
        profile['source_refs']=[dict(r,url='https://github.com/'+c['repository']+'/blob/'+c['upstream_commit']+'/'+r['path']) for r in proof['references']]
        profiles.append(profile)
    (ROOT/'data/web-repository-guides.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(len(profiles))+' repository-specific Japanese guides')
