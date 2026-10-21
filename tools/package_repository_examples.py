"""Package maintained Japanese forks and genuine per-repository reproduction kits."""
from pathlib import Path
from hashlib import sha256
import json, shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
SPECS = {
 'revealjs-skill': ('revealjs-skill-ja','build_more_repository_examples.py',['reveal']),
 'lewis-html-ppt': ('html-ppt-studio-ja','build_more_repository_examples.py',['lewis']),
 'minorun-marp': ('minorun-marp-ja','build_more_repository_examples.py',['minorun']),
 'neon-slides': ('neon-slides-ja','build_more_repository_examples.py',['neon']),
 'qiaomu-bento': ('qiaomu-bento-ja','build_more_repository_examples.py',['bento']),
 'make-slide': ('make-slide-ja','build_more_repository_examples.py',['kuneosu']),
 'frontend-editable': ('frontend-editable-ja','build_more_repository_examples.py',['editable']),
 'office-powerpoint-mcp': ('office-powerpoint-mcp-ja','build_native_repository_examples.py',['--only','mcp']),
 'mck-design': ('mck-design-ja','build_native_repository_examples.py',['--only','mck']),
 'jinba-consulting': ('jinba-consulting-ja','build_japanese_repository_examples.py',['--only','jinba']),
 'japanese-corporate': ('japanese-corporate-ja','build_japanese_repository_examples.py',['--only','gonta']),
 'dashi-ppt': ('dashi-ppt-ja','build_dashi_repository_example.py',[]),
 'codex-image-ppt': ('codex-image-ppt-ja','build_codex_image_repository_example.py',['assemble']),
 'multiagent-ppt': ('multiagent-ppt-ja','build_multiagent_repository_example.py',[]),
 'knowledge-cat': ('knowledge-cat-ppt-ja','build_knowledge_cat_repository_example.py',[]),
 'seaslides': ('seaslides-ja','build_seaslides_repository_example.py',[]),
 'ppt-design-skill': ('ppt-design-skill-ja','build_ppt_design_repository_example.py',['--input','examples/repositories/ppt-design-skill/input/data.json']),
 'magic-slide': ('magic-slide-ja','build_magic_slide_repository_example.py',['--input','examples/repositories/magic-slide/input/data.json']),
 'image-to-editable': ('image-to-editable-ppt-ja','build_image_editable_repository_example.py',['--replay','--source-dir','.build/recorded-image-editable','--output-dir','examples/repositories/image-to-editable','--upstream-dir','.build/actual-upstreams/ningzimu__image-to-editable-ppt-skill']),
 'react-slide-deck': ('react-slide-deck-ja','build_reactdeck_repository_example.py',['--input','examples/repositories/react-slide-deck/input/data.json']),
 'slide-maker': ('slide-maker-ja','build_slide_maker_repository_example.py',[]),
 'business-carousel': ('business-carousel-ja','build_business_carousel_repository_example.py',['--input','examples/repositories/business-carousel/input/data.json']),
 'cyberppt': ('cyberppt-ja','build_cyberppt_repository_example.py',[]),
 'hands-on-deck': ('hands-on-deck-ja','build_hands_on_deck_repository_example.py',[]),
 'slide-writer': ('slide-writer-ja','build_slide_writer_repository_example.py',['--input','examples/repositories/slide-writer/input/data.json']),
 'html-scrolline': ('html-scrolline-ja','build_htmlscrolline_repository_example.py',[]),
 'ppt-design-system': ('ppt-design-system-ja','build_ppt_design_system_repository_example.py',[]),
 'html-to-ppt-pdf': ('html-to-ppt-pdf-ja','build_html_to_ppt_pdf_repository_example.py',[]),
 'pradaslides': ('pradaslides-ja','build_pradaslides_repository_example.py',[]),
 'presentation-delivery': ('presentation-delivery-ja','build_presentation_delivery_repository_example.py',[]),
}
FRAGMENTS = ['web','native','japanese','dashi','codex-image','multiagent','knowledgecat','seaslides','pptdesign','magicslide','imageeditable','reactdeck','slidemaker','businesscarousel','cyberppt','handsondeck','slidewriter','htmlscrolline','designsystem','htmlconversion','pradaslides','delivery']
CODE_SUFFIXES = {'.py','.js','.mjs','.cjs','.jsx','.ts','.tsx','.css','.html','.json','.yaml','.yml','.md','.txt','.toml','.xml','.csv','.svg','.sh','.ps1','.psm1','.ini','.cfg','.in','.sql','.ttf','.woff','.woff2'}
SKIP_PARTS = {'.git','node_modules','__pycache__','.venv','venv','.pytest_cache','.cache','releases','public'}
SPECIAL = {
 'gonta223/japanese-corporate-pptx-skill': ['skills/japanese-corporate-pptx/assets/'],
 'carnot-tech/jinba-consulting-pptx-skill': ['assets/SlideCatalog_16x9.pdf','assets/SuperTemplate_62type.pptx'],
 'johnson7788/MultiAgentPPT': ['backend/save_ppt/ppt_template_0717.pptx'],
}
NOTES = {
 'pradaslides':'原典のbootstrap、brief・出典・設計・レイアウト等の契約validatorとstrict plan lintを使い、native PPTXを作る。原典はauthoring engineを固定しないため、この作例では専用python-pptxソースを使用する。PowerPoint実描画から無改変の原典build_pptx_preview.pyでrender-parity presenterを作り、原典由来HTTP QAを実行する。ブラウザー表示の本文は画像、編集正本はPPTX。OS游ゴシックは配布せず、MITの原文を保持する。',
 'presentation-delivery':'原典Visual Deck StudioのHTML-first Path A、960×540ptの4条件、無改変の変換・寸法・overflow検査とDOM要素変換を使う。原典deck_index.htmlの概覧・キー操作とPDF結合を保持する。明示HTTP入口、字体待ち、日本語ノート、Windows環境継承だけをadapterで補う。本文文字と図形はnative PPTX。HTML/PPTXの字間・太さ・br行間には差があり、pixel一致・動画・TTS・人の早期承認は主張しない。BIZ UDPGothicのOFL原本を同梱する。',
 'html-to-ppt-pdf':'既存Guizang HTMLを、無改変の原典build.mjsでPNG・画像PPTX・PDFへ変換する。原文HTMLとAGPL対応ソースを保持し、export.htmlだけでdotからの移動をforce:trueへ補正する。原典の短い撮影間隔と700ms待ちの競合によるページ重複を、全ページと一意なPNGで確認する。日本語発表ノートの後処理は本文画像とスライドXMLを保持する。本文編集・motion保持・新規資料構成の生成ではない。MIT変換器、AGPL入力ソース、OFL書体を区別する。',
 'ppt-design-system':'原典template.html、Forest Ink配色、cover・cards・body・question・comparison・closingのレイアウトを使う。固有ナビゲーションJSを保持し、日本語の行間・字体・同じ重要度の比較欄を調整する。HTTPで全ページとキー・dot操作を確認。HTML生成CLIは原典にないため、同梱Pythonは原典テンプレートを埋める再現入口である。PPTX出力と印刷は今回未検証。',
 'hands-on-deck':'原典deck.pyのinspect・atomic JSON patch・apply・fix・diffで既存PPTXを編集する。自作日本語ドナーの図形構造を保って本文・文字サイズ・ノートを更新。元shape ID、入力と差分を残し、全ページを独立レビューする。fix advisoryと実際の見切れを区別し、新しい出力へ元QAを移さない。',
 'slide-writer':'原典template.htmlを複製し、Mode A1の構成・密度・コンポーネントで日本語をまとめ、無改変のbranding・inline-images・smoke-testを実行する。自作しおりテーマとlogo、OFL書体の別名サブセット、意味で区切る改行、原典revealとスクロールを用いる。file://直接起動は安全ポリシーで未確認で、原典の全工程完走とは扱わない。',
 'html-scrolline':'原典deck.yaml・plan・Vite build・Scrolline engineとrail-advance/era-shiftで6停止点を連続的につなぐ。engine/moves/conceptsは原典と一致。内部localeはen、HTMLの表示は日本語。Windows Chrome探索だけを明示adapterで補正する。原典全体CIのWindowsパス3件不合格を保持し、HTTP上のcore・smoke・操作確認と分ける。GSAP独自条件と各MITの原文通知を分けて保持。',
 'cyberppt':'原典の内容lock、ImageGen設計見本、要素の測定・対応登録、PptxGenJS単頁再構築、PowerPoint描画、比較、統合を使う。日本語派生は読みやすさと編集性を確認し、原典の厳密な画像一致ゲート全頁不合格を成功へ読み替えない。画像の字形差と内容の数字の欠落は別に確認する。派生mergeの背景保持と差分を残す。再現は固定した5見本からのreplayで、新規画像生成や異なる原稿への自動再構築ではない。',
 'business-carousel':'原典43-carousel-brief-globalの指示型工程で、読み手とブランド条件、HookからCTAまでの構成、1枚1論点の原稿、図案と背景をブリーフにし、1080×1080のHTML構成確認プレビューを作る。原典に自動生成CLIやPowerPoint出力はない。SNS公開用の制作データ、人の承認、公開とは区別する。実績の証拠がない箇所は、架空の記入例を明示する。',
 'slide-maker':'原典deckkit/native_chartでnative図とグラフを作る。入力のPython実探索、1〜15の全15通り、グラフ全30値、PowerPoint全5枚と独立critic/blind readを照合する。計画比較は制作後に追加した記録。完成例はselfread用途で、人による正式採用・投影可読性・全時系列工程の完走を主張しない。',
 'react-slide-deck':'原典en-context-engineeringのReact App、SlideLayout、useSlideScale、Motion variantsで制作する。training-cycleとBold Signalを保持し、CJK字体、reduced-motion、週別タブ、ページ同期を補う。原典依存のVite8/Tailwind4.2.1衝突はTailwind4.2.2への最小補正で解消し、元lockと差分と固定再現lockを保存。HTTPで表示する。',
 'office-powerpoint-mcp':'原典のstdio MCPへ実際にツール呼び出しを送る。mcp 1.30.0を使う。文字、テーブル、ネイティブチャートを生成し、PowerPoint本体で確認する。サーバーはアーカイブ済み。',
 'mck-design':'原典DeckBuilderとMckEngineを使う。原典の存在しないlayouts参照を前提にせず、同梱engine-apiと実コードを読む。今回のS3/S4検査はPASS、98点。自動採点をデザイン承認とは扱わない。',
 'jinba-consulting':'原典new_deckで固有パーツを展開してから日本語を組み、原典html_to_pptxで変換する。追加パーツ2ページの文字サイズ・行間の0.8補正は作例のconversion-corrections.jsonに記録。原典の検査を削除しない。',
 'japanese-corporate':'原典の15型PowerPointテンプレートから必要な型を選び、図形・文字・表・グラフを編集する。企画の結論、担当、期日、確認方法を日本語で書く。原典の図形を勝手に共通HTMLへ置き換えない。',
 'revealjs-skill':'原典create-presentation.jsで骨格を作る。元スキルのpt単位とsection構造を守り、reveal.jsの実ナビゲーションを使う。',
 'lewis-html-ppt':'原典new-deck.shを実行し、固有のfull-deckテンプレートを展開する。日本語本文とコードが読める文字サイズへ調整し、1920×1080の原典キャンバスとruntimeを保持する。',
 'minorun-marp':'元の日本語3スキル（story・figures・dark design）を読み、問いと段階的な図解を作る。原典minorun-darkテーマでMarp CLIを実行し、check-ai-smellも実行する。',
 'neon-slides':'元template.htmlのナビとCSSを使う。components.mdで追加指定されたCSSも必ず取り込む。日本語フォントを追加し、文字と数字を省略せず読める大きさにする。',
 'qiaomu-bento':'固定Bento shellを変えない。日本語本文・字体・要素IDを文書JSONへ入れ、原典bento_deck.pyで検証・buildする。編集版とreadonly再生版を作り、morphに同一IDを使う。',
 'make-slide':'原典のテーマ別reference.htmlから固有のページを選ぶ。万円・件・率・ポイントを区別し、グラフの高さと角度を実データから計算する。同一カテゴリの色を揃える。',
 'frontend-editable':'原典のSlideDeck、SlideObjectEditor、SlideSidebarを保つ。data-oidを全ページで一意にする。文字の編集・保存・再読込とHTML書き出しを確認する。Undo/Redo全機能の確認済み表示はしない。',
 'dashi-ppt':'原典の1案経路でJSON→React/tsx→HTMLを実行する。theme05の日本語派生ではcopy値を図形寸法計算へ反映する。3+1経路のcopy検証不整合を記録し、検査を弱めて回避しない。PPTXエンジンは専有条件を持ち、別製品へ抽出しない。',
 'codex-image-ppt':'原典spec/style/jobs/stateを経てCodex native image_genで各ページを実生成し、原典assemble_ppt.pyで組む。画像を個別編集可能なPPTXと呼ばない。toolが公開していないモデル名を推測しない。sample採用は制作エージェントの判断と記録し、人の承認と偽らない。',
 'multiagent-ppt':'原典のstart_generate_presentationと同梱templateのAPI不要exportを実行する。実関数はdict入力を要求し、本文処理はsectionのindex1/2に限定。通常のmulti-agent、LLM、画像API経路の成功を示さない。shape IDの設定補正、Noto Sans JP・講稿・固定ラベルの局所化を記録する。',
 'knowledge-cat':'原典native-pptx laneの専用build_native_pptx.mjsと原典plan/text/editability/probeを実行する。Codexのartifact-tool作業環境を指定し、本体は複製しない。日本語action-title警告を消さず、本文の命題を実読する。出力の固定デモラベルとNoto Sans JPを局所化。',
 'seaslides':'原典のHTML lane、TCS、editorial-magazineテーマを使い、source gate→固有compiler --all→visual gateで生成する。Windowsのreceipt相対パスをPOSIX表記へ直す2ファイルの派生差分を保持し、validatorは変更しない。原典Motion・WebGL・ナビゲーションを保持し、日本語OFL書体と講稿を収録する。HTML表示はローカルHTTP経由。PPTXは今回の出力に含めない。',
 'ppt-design-skill':'原典Build Modeのtask初期化、ThemeComposer、strict Presentationと公開text/shapes/bar_chartを使う。日本語の色名aliasと見出しフォントを明示解決し、入力JSON・テーマlock・講稿を残す。売上試算と利益、未収集とゼロを区別する。原典と公開engineは無改変。編集可能な本文と図形をPowerPoint本体で描画して確認する。',
 'magic-slide':'原典のoutline/Brief Lite、モジュールHTML/CSS、merge、inject、serveとMagic Moveを使う。隣接ページで数字・準備品を意味に沿って受け渡す。認証関数のscopeだけを修正した日本語派生injectorを使い、原典と差分を保持する。cursor、dock、Overview、動き、serverの認証と保存先制限を保持する。表示用iframeと、原典serverでの編集・保存を案内し、agent QAと人のrevision/adoptionを区別する。',
 'image-to-editable':'原典editpptのprepare→page worker→build/validate→record→finalizeで画像を再構成する。Codex内蔵image_genで分離したアイコンはbitmapとして保持し、本文・カード・単純な矢印をnative要素にする。新規案内ノートは元画像からの抽出と区別し、本文XMLと画像を保って追加する。再出力kitは保存済みmanifest・分離済み画像の再利用で、新規画像編集ではない。元画像との比較と実PowerPoint描画、編集範囲を確認する。',
}

def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def write(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(v,encoding='utf-8',newline='\n')
def digest(p): return sha256(Path(p).read_bytes()).hexdigest()
def copy(p,q):
 q=Path(q);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def files(folder):
 retained_probes=('source/input-corresponding-source/.build/','source/input-corresponding-source/examples/',
                  'source/input-corresponding-source/upstreams/op7418__guizang-ppt-skill/assets/ppt-skill-showcase.png')
 return [p for p in sorted(folder.rglob('*')) if p.is_file() and not (set(p.relative_to(folder).parts)&SKIP_PARTS) and p.suffix!='.pyc' and not p.name.startswith('.env') and not any(('/'+p.relative_to(folder).as_posix()).find('/'+probe)>=0 for probe in retained_probes)]

def source_files(folder,repo):
 for p in files(folder):
  name=p.relative_to(folder).as_posix()
  if repo in {'prodigeproject/pradaslides','ConnorRX56/presentation-delivery-skills'}:
   fragment='pradaslides' if repo=='prodigeproject/pradaslides' else 'delivery'
   refs=load(ROOT/'data'/f'{fragment}-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='FeeiCN/slide-writer':
   refs=load(ROOT/'data/slidewriter-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='EveryInc/hands-on-deck':
   refs=load(ROOT/'data/handsondeck-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='johnson7788/MultiAgentPPT' and not (name in {'ACQUISITION.json','LICENSE','README.md','frontend/LICENSE'} or name.startswith('backend/save_ppt/')): continue
  if repo=='gnipbao/knowledge-cat-ppt-skill':
   refs=load(ROOT/'data/knowledgecat-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='touying-typ/seaslides':
   refs=load(ROOT/'data/seaslides-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='sunchaokun/PPT-Design-Skill':
   refs=load(ROOT/'data/pptdesign-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='daniel-style/magic-slide':
   refs=load(ROOT/'data/magicslide-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='ningzimu/image-to-editable-ppt-skill':
   refs=load(ROOT/'data/imageeditable-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  if repo=='minhnv0807/ai-business-skills':
   refs=load(ROOT/'data/businesscarousel-repository-guides.json')[0]['source_refs']
   if name not in {r['path'] for r in refs}|{'ACQUISITION.json'}:continue
  # The dedicated proprietary export engine is fetched only inside the original
  # integrated Dashi skill at reproduction time. Never publish a separated copy.
  if repo=='chuspeeism/dashi-ppt-skill' and '/packages/html-deck-to-pptx/' in '/'+name and p.name!='LICENSE': continue
  allowed=(p.suffix.lower() in CODE_SUFFIXES or p.name in {'LICENSE','NOTICE','requirements','Dockerfile'} or p.name.startswith(('LICENSE.','NOTICE.')))
  allowed=allowed or any(name==s or name.startswith(s) for s in SPECIAL.get(repo,[]))
  if allowed: yield p

def zip_folder(source,target,rootname):
 target.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files(source):
   info=zipfile.ZipInfo((Path(rootname)/p.relative_to(source)).as_posix())
   info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)

def make_fork(case,profile):
 cid=case['id'];fork_id,_,_=SPECS[cid];repo=case['repository']
 target=ROOT/'skill-forks'/fork_id;up=ROOT/'.build/actual-upstreams'/repo.replace('/','__')
 target.mkdir(parents=True,exist_ok=True)
 for p in source_files(up,repo):copy(p,target/'upstream'/p.relative_to(up))
 raw_skills=[r['path'] for r in profile.get('source_refs',[]) if isinstance(r,dict) and r.get('path','').endswith('SKILL.md')]
 if not raw_skills:raw_skills=[p.relative_to(up).as_posix() for p in files(up) if p.name=='SKILL.md'][:5]
 paths='\n'.join('- upstream/'+p for p in raw_skills)
 own='---\nname: '+fork_id+'\ndescription: '+repo+'の方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。\n---\n\n# '+fork_id+'\n\n八百万図AIツールボックスの日本語派生版。原作者の公式翻訳ではありません。\n\n## 原典を読む\n\n'+paths+'\n\n同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。\n\n## 固有の制作方式\n\n'+NOTES[cid]+'\n\n## 日本語で完成させる\n\n- 先に読み手、目的、結論、必要なページ、出力形式を決める。\n- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。\n- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。\n- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。\n- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。\n\n## 再現と利用条件\n\n完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。\n'
 # Preserve a human-maintained entrypoint on subsequent packaging runs.
 if not (target/'SKILL.md').exists():write(target/'SKILL.md',own)
 requirements='\n'.join('- '+s for s in profile.get('requirements',[]))
 commands='\n\n'.join('    '+s for s in profile.get('commands',[]) if isinstance(s,str))
 limits='\n'.join('- '+s for s in profile.get('limitations',[]))
 extra='\nDashiのexport engineはこの派生パッケージへ分離収録していません。完全な原典を固定commitで取得して、同じDashi skill内だけで使用します。AGPL対象の対応ソースとtheme05局所差分を保持。専有エンジンは変更しません。\n' if cid=='dashi-ppt' else ''
 workflow='# '+repo+'の日本語制作\n\n原典: https://github.com/'+repo+'/tree/'+case['upstream_commit']+'\n\n'+case['method']+'\n\n'+NOTES[cid]+'\n\n## 作例\n\n- '+case['title']+' / '+str(case['page_count'])+'枚 / '+case['format']+'\n- 完成例: https://studio-yebisu.github.io/yaoyorozu-ai-toolbox-slides/repository.html?repo='+repo+'\n- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo='+repo+'\n- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。\n\n## 環境\n\n'+requirements+'\n\n## 元の制作コマンド\n\n'+commands+'\n\n## 確認範囲\n\n'+limits+'\n\n## 権利\n\n原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。\n'+extra
 workflow=workflow.replace('- 完成例: https://studio-yebisu.github.io/yaoyorozu-ai-toolbox-slides/repository.html?repo='+repo, '- カタログ内の案内: repository.html?repo='+repo)
 write(target/'references/WORKFLOW.md',workflow)
 dump(target/'references/recipe.json',profile)
 gen=SPECS[cid][1]
 copy(ROOT/'tools'/gen,target/'references/example-source'/gen)
 if cid in {'revealjs-skill','lewis-html-ppt','minorun-marp','neon-slides','qiaomu-bento','make-slide','frontend-editable','dashi-ppt'}:
  copy(ROOT/'tools/repository_example_support.py',target/'references/example-source/repository_example_support.py')
 if cid=='dashi-ppt':
  for name in ['theme05-runtime.diff','runtime-changes.json']:
   copy(ROOT/'examples/repositories'/cid/'source'/name,target/'references/example-source'/name)
 dump(target/'SOURCE.json',{'repository':repo,'commit':case['upstream_commit'],'scope':'Japanese entrypoint, repository-specific refinements, original source and actual production recipe','example_ids':[cid],
  'upstream_preserved':True,'proprietary_export_engine_included':False if cid=='dashi-ppt' else None,
  'files':[{'path':p.relative_to(target).as_posix(),'sha256':digest(p)} for p in files(target) if p.name!='SOURCE.json']})
 zip_folder(target,ROOT/'downloads'/(fork_id+'.zip'),fork_id)
 return target

def make_kit(case,fork):
 cid=case['id'];fork_id,generator,args=SPECS[cid];repo=case['repository'];folder=ROOT/'examples/repositories'/cid
 kit=ROOT/'.build/release-kits'/cid;kit.mkdir(parents=True,exist_ok=True)
 for p in files(folder):copy(p,kit/p.relative_to(folder))
 workspace=kit/'reproduce/workspace';workspace.mkdir(parents=True,exist_ok=True)
 for name in ['case-inputs.json','fonts.json','preset-fonts.json','repository-audit.json']:
  copy(ROOT/'data'/name,workspace/'data'/name)
 if cid not in {'ppt-design-system','html-to-ppt-pdf','pradaslides','presentation-delivery'}:
  for p in files(ROOT/'assets/fonts'):copy(p,workspace/'assets/fonts'/p.relative_to(ROOT/'assets/fonts'))
 for name in {generator,'repository_example_support.py','acquire_repository.py','render_powerpoint.ps1','build_more_repository_examples.py'}:
  copy(ROOT/'tools'/name,workspace/'tools'/name)
 audit=ROOT/'.build/repository-audit'/repo.replace('/','__')/'record.json'
 if audit.exists():copy(audit,workspace/'.build/repository-audit'/repo.replace('/','__')/'record.json')
 if cid!='dashi-ppt':
  for p in files(fork/'upstream'):copy(p,workspace/'.build/actual-upstreams'/repo.replace('/','__')/p.relative_to(fork/'upstream'))
 if cid in {'minorun-marp','revealjs-skill'}:
  for name in ['package.json','package-lock.json']:copy(ROOT/'.build/repository-runtime'/name,workspace/'.build/repository-runtime'/name)
 if cid=='codex-image-ppt':
  # The image generation tool is deliberately not invoked by this local script.
  # Reproduction packages the already generated images and honest jobs/state.
  for p in files(folder):copy(p,workspace/'examples/repositories'/cid/p.relative_to(folder))
  up=ROOT/'.build/actual-upstreams'/repo.replace('/','__')
  for p in (up/'skills/codex-ppt/scripts').glob('*.py'):
   copy(p,kit/'source/upstream/skills/codex-ppt/scripts'/p.name)
 if cid=='multiagent-ppt':
  for name in ['source/run_export.py','input/data.json']:
   copy(folder/name,workspace/'examples/repositories'/cid/name)
 if cid=='knowledge-cat':
  for name in ['input/data.json','input/BRIEF.md']:
   copy(folder/name,workspace/'examples/repositories'/cid/name)
 if cid=='ppt-design-skill':copy(folder/'input/data.json',workspace/'examples/repositories'/cid/'input/data.json')
 if cid=='magic-slide':copy(folder/'input/data.json',workspace/'examples/repositories'/cid/'input/data.json')
 if cid=='business-carousel':copy(folder/'input/data.json',workspace/'examples/repositories'/cid/'input/data.json')
 if cid=='react-slide-deck':
  for name in ['data.json','package-lock.json']:copy(folder/'input'/name,workspace/'examples/repositories'/cid/'input'/name)
 if cid=='image-to-editable':
  for p in files(folder):copy(p,workspace/'.build/recorded-image-editable'/p.relative_to(folder))
 if cid=='seaslides':
  for p in files(folder):copy(p,workspace/'examples/repositories'/cid/p.relative_to(folder))
 if cid in {'cyberppt','hands-on-deck','slide-writer','html-scrolline','ppt-design-system','html-to-ppt-pdf','pradaslides','presentation-delivery'}:
  for p in files(folder):copy(p,workspace/'examples/repositories'/cid/p.relative_to(folder))
 requirements=['python-pptx==1.0.2','Pillow==12.3.0','lxml==6.1.3','fonttools==4.63.0','brotli==1.2.0','beautifulsoup4==4.15.0','filelock==4.1.1']
 if cid=='react-slide-deck':requirements=[r.replace('fonttools==4.63.0','fonttools==4.66.1')for r in requirements]
 if cid=='business-carousel':requirements=['fonttools==4.63.0','brotli==1.2.0']
 if cid=='cyberppt':requirements=['Pillow==12.3.0','numpy==2.5.4','pywin32==312; sys_platform == "win32"']
 if cid=='hands-on-deck':requirements=['python-pptx==1.0.2','Pillow==12.3.0','lxml==6.1.3']
 if cid=='slide-writer':requirements=['fonttools==4.66.1','brotli==1.2.0']
 if cid in {'html-scrolline','ppt-design-system','html-to-ppt-pdf'}:requirements=[]
 if cid=='presentation-delivery':requirements=[]
 if cid=='pradaslides':requirements=['python-pptx==1.0.2']
 if cid=='office-powerpoint-mcp':requirements.append('mcp[cli]==1.30.0')
 if cid=='multiagent-ppt':requirements.append('requests==2.34.2')
 if cid=='seaslides':requirements.append('pypdf==6.20.1')
 if cid=='ppt-design-skill':requirements.append('pptx-designer==1.0.0b11')
 if cid=='slide-maker':requirements+=['PyMuPDF==1.28.2','numpy==2.5.4','matplotlib==3.11.2']
 if cid=='image-to-editable':requirements+=['PyMuPDF==1.28.2','openai==3.29.0','numpy==2.5.4','requests==2.34.2','PyYAML==6.0.3']
 write(workspace/'requirements-reproduce.txt','\n'.join(requirements)+'\n')
 font=load(ROOT/'data/fonts.json')[0]
 setup=''
 if cid in {'minorun-marp','revealjs-skill'}:setup+='    & npm --prefix .build/repository-runtime ci --ignore-scripts\n    if ($LASTEXITCODE) { throw "npm ci failed" }\n'
 if cid=='seaslides':
  setup+='    $taskRenderer = ".build/actual-upstreams/touying-typ__seaslides/skills/seaslides-html-slides-skill/scripts/html_to_svg"\n    & npm --prefix $taskRenderer ci --ignore-scripts\n    if ($LASTEXITCODE) { throw "SeaSlides renderer dependencies failed" }\n    & npm --prefix $taskRenderer exec -- playwright install chromium --only-shell\n    if ($LASTEXITCODE) { throw "SeaSlides browser setup failed" }\n'
 if cid=='dashi-ppt':
  setup+='    & $taskPy tools/acquire_repository.py chuspeeism/dashi-ppt-skill\n    if ($LASTEXITCODE) { throw "Pinned upstream acquisition failed" }\n    & npm --prefix .build/actual-upstreams/chuspeeism__dashi-ppt-skill/skills/dashi-ppt/project ci --ignore-scripts\n    if ($LASTEXITCODE) { throw "Dashi dependencies failed" }\n'
 if cid=='image-to-editable':
  setup+='    & $taskPy -m pip install -e .build/actual-upstreams/ningzimu__image-to-editable-ppt-skill/skills/image-to-editable-ppt/cli\n    if ($LASTEXITCODE) { throw "Original editppt CLI installation failed" }\n'
 if cid=='cyberppt':
  setup+='    & npm --prefix examples/repositories/cyberppt/source ci --ignore-scripts\n    if ($LASTEXITCODE) { throw "CyberPPT Node dependencies failed" }\n'
 generation='    & $taskPy tools/'+generator+' '+' '.join(args)+'\n'
 if case['format']=='pptx' and cid!='codex-image-ppt':
  generation='    $taskArgs = @('+','.join('"'+a+'"' for a in args)+')\n    if ($Render) { $taskArgs += "--render" }\n    & $taskPy tools/'+generator+' @taskArgs\n'
 if cid=='slide-maker':
  generation='    & $taskPy tools/'+generator+'\n    if ($LASTEXITCODE) { throw "Slide maker generation failed" }\n    if ($Render) { & pwsh -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/repositories/slide-maker/deck.pptx -OutputDirectory examples/repositories/slide-maker/render }\n'
 if cid=='cyberppt':
  generation='    & $taskPy examples/repositories/cyberppt/source/reproduce.py --input examples/repositories/cyberppt/input/data.json --render\n'
 if cid in {'hands-on-deck','html-scrolline','ppt-design-system'}:
  generation='    $taskArgs = @("--input","examples/repositories/'+cid+'/input/data.json")\n    if ($Render) { $taskArgs += "--render" }\n    & $taskPy examples/repositories/'+cid+'/source/reproduce.py @taskArgs\n'
 if cid=='html-to-ppt-pdf':
  generation='    $taskArgs = @()\n    if ($NodePath) { $taskArgs += @("--node",$NodePath) }\n    if ($Render) { $taskArgs += "--powerpoint" }\n    & $taskPy examples/repositories/html-to-ppt-pdf/source/reproduce.py @taskArgs\n'
 if cid=='presentation-delivery':
  generation='    $taskArgs = @()\n    if ($NodePath) { $taskArgs += @("--node",$NodePath) }\n    if ($Render) { $taskArgs += "--powerpoint" }\n    & $taskPy examples/repositories/presentation-delivery/source/reproduce.py @taskArgs\n'
 if cid=='pradaslides':
  generation='    & $taskPy examples/repositories/pradaslides/source/reproduce.py\n    if ($LASTEXITCODE) { throw "PradaSlides generation failed" }\n    if ($Render) {\n        $taskArgs = @()\n        if ($NodePath) { $taskArgs += @("--node",$NodePath) }\n        & $taskPy examples/repositories/pradaslides/source/qa.py @taskArgs\n    }\n'
 if cid=='knowledge-cat':
  generation='    $taskArgs = @("--node",$NodePath,"--workspace",$ArtifactWorkspace)\n    if ($Render) { $taskArgs += "--render" }\n    & $taskPy tools/'+generator+' @taskArgs\n'
 if cid=='image-to-editable':
  generation='    & $taskPy tools/'+generator+' '+' '.join(args)+'\n    if ($LASTEXITCODE) { throw "Recorded image reconstruction replay failed" }\n    if ($Render) { & pwsh -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/repositories/image-to-editable/deck.pptx -OutputDirectory examples/repositories/image-to-editable/render }\n'
 if cid=='react-slide-deck':
  generation='    & $taskPy tools/'+generator+' '+' '.join(args)+' --node $NodePath\n'
 if cid=='codex-image-ppt':
  generation+='    if ($Render) { & pwsh -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/repositories/codex-image-ppt/codex-image-ppt.pptx -OutputDirectory examples/repositories/codex-image-ppt/render }\n'
 fontsetup=''
 if cid not in {'codex-image-ppt','business-carousel','cyberppt','hands-on-deck','slide-writer','html-scrolline','ppt-design-system','html-to-ppt-pdf','pradaslides','presentation-delivery'}:
  fontsetup='    $taskFont = Join-Path $taskRoot ".build/fonts/NotoSansJP[wght].ttf"\n    if (-not (Test-Path -LiteralPath $taskFont)) {\n        New-Item -ItemType Directory -Path (Split-Path $taskFont) -Force | Out-Null\n        Invoke-WebRequest -Uri "'+font['source_url']+'" -OutFile $taskFont\n    }\n    if ((Get-FileHash -LiteralPath $taskFont -Algorithm SHA256).Hash.ToLower() -ne "'+font['source_sha256']+'") { throw "Pinned font hash mismatch" }\n'
 script='param([switch]$Render)\n$ErrorActionPreference = "Stop"\n$taskRoot = Join-Path $PSScriptRoot "workspace"\nPush-Location -LiteralPath $taskRoot\ntry {\n    & python -m venv .build/ppt-master-venv\n    if ($LASTEXITCODE) { throw "Python environment failed" }\n    $taskPy = Join-Path $taskRoot ".build/ppt-master-venv/Scripts/python.exe"\n    & $taskPy -m pip install -r requirements-reproduce.txt\n    if ($LASTEXITCODE) { throw "Python dependencies failed" }\n'+fontsetup+setup+generation+'    if ($LASTEXITCODE) { throw "Generation failed" }\n    & $taskPy tools/mark_reproduced.py\n    Write-Host "Generated: $taskRoot/examples/repositories/'+cid+'"\n    Write-Host "Open the actual output and review all pages before using it."\n} finally { Pop-Location }\n'
 if cid=='knowledge-cat':
  script=script.replace('param([switch]$Render)','param([switch]$Render, [Parameter(Mandatory=$true)][string]$ArtifactWorkspace, [string]$NodePath="node")')
 if cid=='react-slide-deck':script=script.replace('param([switch]$Render)','param([string]$NodePath="node")')
 if cid in {'html-to-ppt-pdf','pradaslides','presentation-delivery'}:script=script.replace('param([switch]$Render)','param([switch]$Render, [string]$NodePath="")')
 if cid=='business-carousel':script=script.replace('param([switch]$Render)','param()')
 write(kit/'reproduce/Reproduce.ps1',script)
 artifact_name=Path(case['artifact_download'] if case['format']=='pptx' else case['preview']).relative_to(folder.relative_to(ROOT)).as_posix()
 mark="from pathlib import Path\nimport json, hashlib\np=Path('examples/repositories/"+cid+"')\nartifact=p/"+repr(artifact_name)+"\n(p/'QA.json').write_text(json.dumps({'status':'generated_awaiting_review','artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'visual_review':'Review your reproduced output; the original catalog QA is not transferred to a new run.'},ensure_ascii=False,indent=2),encoding='utf-8')\n"
 write(workspace/'tools/mark_reproduced.py',mark)
 readme='# '+case['title']+'の再現キット\n\n完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。\n\n## Windowsで同じ作例を生成\n\n1. ZIPを展開。PowerShellでこのフォルダーへ移動。\n2. Python 3.13、Node.js、必要に応じてGit Bashを用意。\n3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。\n\n    .\\reproduce\\Reproduce.ps1\n\n生成先: reproduce/workspace/examples/repositories/'+cid+'/\n\nPowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。\n\n## 自分の題材へ\n\n完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。\n\n'+NOTES[cid]+'\n\n## 原典と権利\n\nhttps://github.com/'+repo+'/tree/'+case['upstream_commit']+'\n\n原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。\n'
 if cid=='codex-image-ppt':readme+='\nこのスクリプトは生成済みの3画像を原典assemble_ppt.pyで組み直すだけです。画像を新たに作るには、promptsとstyleを添えてCodex native image_genへ依頼し、原典のjobs/result記録と画像確認を行ってください。APIや画像生成をこのスクリプトから自動実行しません。\n'
 if cid in {'minorun-marp','revealjs-skill'} and (ROOT/'data/dependency-qa.json').exists():
  copy(ROOT/'data/dependency-qa.json',kit/'source/dependency-qa.json')
  readme+='\n固定npm依存の監査記録はsource/dependency-qa.jsonです。Marp CLI側の依存に未修正の検出項目があります。今回の再現は同梱した原稿のHTML生成を対象とし、サイトのHTTPサーバーではこのCLIを実行していません。\n'
 if cid=='dashi-ppt':readme+='\nDashi専有エンジンを分離再配布しません。スクリプトは完全な原典を固定commitで取得し、そのDashi skill内のHTML生成を実行します。PPTX/PDFエンジンの動作検証は今回の作例に含みません。\n'
 if cid=='knowledge-cat':
  readme=readme.replace('.\\reproduce\\Reproduce.ps1','.\\reproduce\\Reproduce.ps1 -ArtifactWorkspace "artifact-tool workspaceのパス" -NodePath "node.exeのパス"')
  readme+='\n原典native出力には、Codexに同梱される@oai/artifact-toolを解決できる既存workspaceが必要です。Codexのload_workspace_dependenciesで確認し、node_modules/@oai/artifact-toolを持つNode workspaceを指定してください。本体・node_modulesはZIPに複製していません。任意のpublic npm installで代替する案内ではありません。\n'
 if cid=='seaslides':
  readme+='\n原典package-lockからPlaywright 1.60とChromium headless shell 1223を使用します。Motion11.11.17はMIT表示とともにローカルbundleを同梱。生成HTMLはES moduleを使うため、出力フォルダーを `python -m http.server 8000` 等で配信して開きます。書き換え後も原典source/visual gateを通し、全ページを実表示して確認してください。\n'
  readme+='\n固定renderer依存のnpm audit記録はsource/dependency-qa.jsonです。form-dataのHigh 1件を未解消として記録しています。この実例の再現は同梱原稿のローカル描画で、外部AI APIは呼びません。依存の検出記録と再現成功を区別します。\n'
 if cid=='ppt-design-skill':
  readme=readme.replace('この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。','reproduce/workspace/examples/repositories/ppt-design-skill/input/data.jsonの価格、日数、仮定販売数、見出し、講稿を変えて再実行できます。別の構成や題材には、原典Build Modeのbrief/page-plan/theme-lockを作り、公開部品でページを配置します。')
 if cid=='magic-slide':
  readme+='\n表示・編集・保存には、生成フォルダーで `python source/ja-runtime/scripts/serve.py index.html --no-open` を実行し、表示された /deck/ のURLを開きます。静的サイトのフロートは表示とページ移動の確認用です。原典の人によるrevision/adoptionはpendingとして残し、今回のagent QAを人の承認とは扱いません。\n'
 if cid=='image-to-editable':
  readme+='\nこの再出力は保存済みのpage manifestと分離済みアイコンを原典CLIで組み直します。新しい画像編集やworkerを再実行するものではありません。新規入力は日本語SKILLと原典のbuiltin-imagegen/worker契約から制作します。本文・図形とbitmapの編集範囲を区別し、元画像と比較してください。原典CLIのPyMuPDF等には個別の依存ライセンスがあります。\n'
 if cid=='react-slide-deck':
  readme=readme.replace('PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。','React版はHTTPで表示します。生成先へ移動して `python -m http.server 8000 --bind 127.0.0.1` を実行し、表示されたlocalhostのURLを開いてください。PPTX・PowerPoint描画の-Renderには対応しません。')
  readme+='\nWindowsではフォント用のnative DLLが深いパスで読み込めないことがあります。ZIPを短いパス（例 M:\\slides\\react-deck）へ展開してください。NodeがPATHにない場合は `-NodePath "node.exeの絶対パス"` を指定します。元Vite8を保持し、互換性のあるTailwind4.2.2と記録したlockでnpm ciを実行します。\n'
 if cid=='slide-maker':
  readme=readme.replace('Python 3.13、Node.js、必要に応じてGit Bashを用意。','Python 3.13を用意。PowerPoint描画を行う場合はPowerPointとpwshも必要。')
  readme=readme.replace('次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。','次を実行（キット内の原典と新しいPython仮想環境で生成します）。')
  readme=readme.replace('HTMLは生成したファイルを開き、原典のページ操作を使います。','生成したdeck.pptxをPowerPointで開きます。')
  readme=readme.replace('Noto Sans JPをインストール済みのWindows / PowerPoint / pwsh','游ゴシック（Yu Gothic）が利用できるWindows / PowerPoint / pwsh')
 if cid=='business-carousel':
  readme=readme.replace('Python 3.13、Node.js、必要に応じてGit Bashを用意。','Python 3.13を用意。')
  readme=readme.replace('次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。','次を実行（キット内の原典指示を使った専用ソースとPython仮想環境で生成します）。')
  readme=readme.replace('PowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。','生成先で `python -m http.server 8000 --bind 127.0.0.1` を実行し、localhostのURLで正方形HTMLを開きます。原典の出力は構成確認用プレビューで、PPTX・PowerPoint描画は対象外です。')
  readme+='\n自分の内容にはreproduce/workspace/examples/repositories/business-carousel/input/data.jsonの6枚の見出し・本文・ノートを変更して再実行できます。原稿確認と図案の調整を行い、公開用の仕上げ・人の承認は原典の次の工程として別途実施します。\n'
 if cid=='cyberppt':
  readme='# '+case['title']+'の日本語派生・再現キット\n\nWindows、Microsoft PowerPoint、Python 3.13、Node.js、游ゴシック・游明朝・Times New Romanが必要です。フォント本体は配布しません。\n\n1. ZIPを展開して、このフォルダーでPowerShellを開きます。\n2. ` .\\reproduce\\Reproduce.ps1 ` を実行します。新しいPython仮想環境と固定Node依存を用意し、PowerPointの全ページ描画まで常に実行します。\n3. 出力は `reproduce/workspace/examples/repositories/cyberppt/deck.pptx`。再生成したQAは確認前となるため、全5枚を改めて表示確認します。\n\n保存済み5見本からの再構築で、ImageGenの新規生成は含みません。異なる入力は旧見本と一致しないため停止します。自分の題材へ変える際は、日本語派生SKILLと原典から新しい内容lock・見本・測定・再構築を作成します。\n\n'+NOTES[cid]+'\n\n元のsource/reproduce.pyを直接使う方法、元ゲート未達、派生方針と実行記録はREADME.md、source/JAPANESE-FORK-POLICY.md、PROVENANCE.jsonを確認してください。原典のMIT、SVGアイコンの個別MIT条件を保持します。人による採用と公開は未実施です。\n'
 if cid=='cyberppt':
  readme+='\n生成用lockはPptxGenJS4.0.1を保持し、間接依存image-sizeを修正版2.0.3に固定しています。検出前後のnpm auditはreview/dependency/に保存しています。このキット以外の依存監査へ読み替えません。\n'
 if cid in {'hands-on-deck','slide-writer','html-scrolline'}:
  conditions={'hands-on-deck':'Python3.13。PowerPoint実描画にはWindows、Microsoft PowerPoint、游ゴシック・游明朝等の元書体が必要。Node.js不要。原典の追加renderにはLibreOffice/Popplerが必要ですが、標準再現では使用しません。', 'slide-writer':'Python3.13、fontTools4.66.1、Brotli1.2.0、Git Bash。Node.js不要。初回に公式固定commitのBIZ UDPGothicを取得し、SHAを確認します。', 'html-scrolline':'Python3.13の標準ライブラリ、Node.js22以上、npm。描画にはインストール済みChrome/Edge。原典npm lockから依存を用意し、GSAP独自条件とMIT表示を保持します。'}
  readme='# '+case['title']+'の日本語派生・再現キット\n\n'+conditions[cid]+'\n\n1. ZIPを展開してPowerShellを開く。\n2. `.\\reproduce\\Reproduce.ps1` を実行。新しい環境から原典の固有経路で再生成します。\n3. 出力は `reproduce/workspace/examples/repositories/'+cid+'/`。新出力のQAは確認前です。全ページを改めて確認してください。\n\n'+NOTES[cid]+'\n\n'
  if cid in {'hands-on-deck','html-scrolline'}:readme+='`-Render`を追加すると実描画も行います。Scrollineの描画はlocalhost HTTPで行い、file://起動は行いません。\n\n'
  else:readme+='表示確認は既存localhostで行います。IABではfile://直接起動が安全ポリシーに拒否されるため、その確認や原典の全工程完走は主張しません。\n\n'
  readme+='自分の内容にはinput/data.jsonと日本語SKILLを使い、本文・配置・停止点を原典方式で調整します。再現の詳細、原典固定commit、個別条件と確認範囲はREADME.md、PROVENANCE.json、QA.jsonを参照してください。\n'
 if cid=='ppt-design-system':
  readme='# '+case['title']+'の日本語派生・再現キット\n\n標準生成はPython3の標準ライブラリだけで実行します。Webの書体は端末の游明朝・游ゴシックなどを使用し、フォントファイルは配布しません。\n\n1. ZIPを展開してPowerShellを開く。\n2. `.\\reproduce\\Reproduce.ps1` を実行。\n3. 出力は `reproduce/workspace/examples/repositories/ppt-design-system/deck.html`。新出力のQAは確認前です。\n4. そのフォルダーで `python -m http.server 8000 --bind 127.0.0.1` を実行し、`http://127.0.0.1:8000/deck.html` で全ページを確認します。\n\n`-Render` を追加すると、Node.js22以上とインストール済みChrome/EdgeでHTTP描画・原典操作を検査します。\n\n'+NOTES[cid]+'\n\n自分の内容にはinput/data.jsonの見出し・本文HTMLを更新し、日本語SKILLと原典レイアウトを使って調整します。6ページ・Forest Inkの再現用経路で、他テーマ・PPTX・印刷の対応を確認したものではありません。原典MIT表示を保持し、正式採用と公開は未実施です。\n'
 if cid=='html-to-ppt-pdf':
  readme='# '+case['title']+'の変換・再現キット\n\nPython3、Node.js22以上とnpm、初回依存・公式Chromium取得のネット接続が必要です。\n\n1. ZIPを展開してPowerShellを開く。\n2. `.\\reproduce\\Reproduce.ps1` を実行。既存HTML7ページを再撮影し、画像PPTXとPDFへ変換します。\n3. 出力は `reproduce/workspace/examples/repositories/html-to-ppt-pdf/`。新出力のQAは確認前です。\n4. `-Render` を追加するとWindows / Microsoft PowerPoint / PowerShell7で実描画を確認します。必要なら `-NodePath "Node.jsの実行ファイルの絶対パス"` を指定します。\n\n'+NOTES[cid]+'\n\nこのキットは既存の7ページを変換する再現用経路です。異なる資料には原典SKILLと日本語派生版から入力HTML・ページ数・静止状態を確認し、すべてのページを比較してください。入力HTML自体の再制作はsource/reproduce-input.pyと対応ソースを参照。初期の重複ソース試行はローカルに保存し、配布には使用中の対応ソースだけを含めています。\n'
 if cid in {'pradaslides','presentation-delivery'}:
  conditions=('Windows、Microsoft PowerPoint、PowerShell7、Python3、OS游ゴシックが必要。HTTP QAを行う-RenderにはNode.js22以上とChrome/Edgeも必要。' if cid=='pradaslides' else 'Python3、Node.js22以上とnpm、公式Chromium取得の接続が必要。PowerPoint描画を行う-RenderにはWindows、Microsoft PowerPoint、PowerShell7とインストール済みBIZ UDPGothicも必要。')
  readme='# '+case['title']+'の日本語再現キット\n\n'+conditions+'\n\n1. ZIPを展開しPowerShellを開く。\n2. `.\\reproduce\\Reproduce.ps1 -Render` を実行。必要なら `-NodePath "node.exeの絶対パス"` を添える。\n3. 出力は `reproduce/workspace/examples/repositories/'+cid+'/`。新しい出力は確認前の状態で記録する。全6ページを改めて確認してください。\n4. 出力フォルダーで `python -m http.server 8000 --bind 127.0.0.1` を起動し、localhostのHTML入口を開く。\n\n'+NOTES[cid]+'\n\n制作原稿と構成はinput/data.json、日本語ノートと制作手順はREADME.mdとPROVENANCE.jsonを参照。構成の変更時は原典の計画・寸法・配置検査と全ページの表示確認を行う。原典MITと素材・依存の各条件を保持し、人の正式採用や公開は別とする。\n'
 write(kit/'REPRODUCE.md',readme);write(folder/'REPRODUCE.md',readme)
 if cid in {'cyberppt','hands-on-deck','slide-writer','html-scrolline','ppt-design-system','html-to-ppt-pdf','pradaslides','presentation-delivery'}:
  copy(folder/'REPRODUCE.md',workspace/'examples/repositories'/cid/'REPRODUCE.md')
 zip_folder(kit,ROOT/'downloads'/(cid+'-example-ja.zip'),cid)
 return 'downloads/'+cid+'-example-ja.zip'

def main():
 profiles={}
 for name in FRAGMENTS:
  p=ROOT/'data'/(name+'-repository-guides.json')
  if p.exists():profiles.update({v['repository']:v for v in load(p)})
 packaged=0
 for name in FRAGMENTS:
  fragment=ROOT/'data'/(name+'-repository-examples.json')
  if not fragment.exists():continue
  cases=load(fragment)
  for c in cases:
   if c['id'] not in SPECS:continue
   folder=ROOT/'examples/repositories'/c['id'];generator=SPECS[c['id']][1]
   # New Web routes require their actual authoring source, not a fictitious CLI.
   if name=='web':
    copy(ROOT/'tools'/generator,folder/'source'/generator)
    copy(ROOT/'tools/repository_example_support.py',folder/'source/repository_example_support.py')
   fork=make_fork(c,profiles[c['repository']]);kit=make_kit(c,fork)
   c['fork_id']=fork.name;c['fork_download']='downloads/'+fork.name+'.zip';c['source_download']=kit
   c['reproduce_script']='reproduce/Reproduce.ps1'
   if c['id']=='knowledge-cat':c['reproduce_command']='.\\reproduce\\Reproduce.ps1 -ArtifactWorkspace "artifact-tool workspaceのパス" -NodePath "node.exeのパス"'
   if c['id']=='image-to-editable':c['preview_notice']='文字・カード・矢印は編集可能。アイコンは分離した画像です。日本語の案内ノートを追加しています。'
   if c['format']=='html':c['artifact_download']=kit
   profiles[c['repository']]['fork']=fork.name
   packaged+=1
  dump(fragment,cases)
 for name in FRAGMENTS:
  p=ROOT/'data'/(name+'-repository-guides.json')
  if p.exists():dump(p,[profiles[v['repository']] for v in load(p)])
 print(str(packaged)+' repository examples packaged with distinct Japanese forks and reproduction workspaces')

if __name__=='__main__':main()
