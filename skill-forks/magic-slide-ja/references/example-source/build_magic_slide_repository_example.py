"""Japanese Magic Slide sample; original merge/server with explicit authenticated QA scope repair."""
from pathlib import Path
import argparse, hashlib, html, json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/'examples/repositories/magic-slide'
REPO='daniel-style/magic-slide'
COMMIT='e29d87cb315eb0afc939820b100d870eabf43f89'
DATA={'title':'朝の支度を10分短くする企画','notice':'架空の5日間実験案。40分・30分・短縮内訳は仮定値。効果は未検証。','baseline':40,'target':30,'days':5,'items':[{'name':'服','minutes':4,'action':'明日着る1組を選ぶ','detail':'天気を見て、上から下までまとめる。'},{'name':'鍵','minutes':3,'action':'置き場所を1か所に','detail':'帰宅したら玄関のトレーへ戻す。'},{'name':'バッグ','minutes':3,'action':'必要な物を詰める','detail':'翌日の予定を見て、中身を確認する。'}], 'titles':['朝に、余白を。','10分を、前夜へ移す。','前夜に、3つだけ。','朝は、確認して出る。','5日間、測って決める。'], 'notes':['朝の支度を急ぐのではなく、前夜へ選択と準備を移す企画です。40分から30分という目標は仮定で、短縮効果の実績はありません。','服を選ぶ4分、鍵を探す3分、バッグを詰める3分を短縮候補と仮定します。合計10分ですが、各値は測定結果ではありません。','前夜の準備は服・鍵・バッグの3つに限定します。カードの内容が次のページへ移動し、夜と朝の役割分担につながります。','夜は選ぶ・置く・詰める、朝は確認する役割に分けます。朝だけでなく、前夜に増えた準備時間も必ず記録し、合計負担が増えていないか確認します。','5日間、起床から出発までの時間と前夜の準備時間、忘れ物、負担感を記録します。記録はまだありません。朝の短縮と一日の負担の両方を見て継続・変更を決めます。']}
PROMPT='原典Magic Slideで「朝の支度を10分短くする企画」を日本語5枚にする。架空の5日間実験案、40分→30分と4+3+3分は仮定、効果は未検証と明示。服・鍵・バッグのカードと時間の数字を、隣接ページへ意味のあるMagic Moveとして受け渡す。原典merge/serveと認証関数のscopeを修正した日本語派生injectorを使い、原典のUIと動きを保持する。写真・外部APIは使わない。講稿を各頁に付け、原典Overviewを先に確認した後、サイト実例用に全頁・motion・移動をagent QAする。人間の正式レビューはpendingのまま残す。'
BRIEF='''# Brief Lite

Audience/setting: 忙しい平日の本人・家族が、玄関で共有する小さな生活実験。
Visual world: 生活雑誌と駅の時刻表も検討したが、生活の具体性を優先し「玄関の持ち物トレー」を選ぶ。
Rejected tropes: 時計アイコンの反復、写真全面グラデーション、根拠のない効率改善の断言。
Cover promise: 写真なしの生成りの紙面。「朝に、余白を。」と10分の大きな文字が主役。左側の静かな文字領域を確保。
Tone mode: primary light; inverse exceptions: none.
Type/color/material: Noto Sans JP。濃い緑は行動、生成りは余白、錆色は仮定の数値。本文は暗い墨色。
Slide families: Cover / Comparison / Metrics Grid / Comparison / Risk Decision Map.
Magic Move motif: 1→2の10分が目標から短縮候補へ。2→3の服・鍵・バッグが候補から準備カードへ。3→4はカードの同じ見出しが前夜の役割へ集約。4→5の5日間・30分が試行条件から評価対象へ。
Review state: ユーザーの自律制作依頼に基づくカタログ試作。agent visual QAとhuman revision/adoptionを区別し、後者はpending。
'''
CSS='''@font-face{font-family:NotoJP;src:url("assets/fonts/noto-sans-jp.woff2") format("woff2");font-weight:100 900;font-display:swap}
:root{--bg:#f7f2e8;--text:#203b34;--subtext:#52685c;--accent:#315c4d;--rust:#a34f31;--pale:#e6eadb;--line:#becbbd}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;font-family:NotoJP,sans-serif;color:var(--text);background:var(--bg)}#deck{width:100%;height:100vh;position:relative;overflow:hidden}
.slide{background:var(--bg)}.slide-content{width:100%;max-width:1680px;aspect-ratio:16/9;margin:0 auto;padding:84px 112px;display:flex;flex-direction:column;justify-content:center;align-items:stretch;position:relative}
.stage{width:100%;min-width:0}h1,h2,h3,p{margin:0}h1{font-size:94px;font-weight:500;line-height:1.3;letter-spacing:-.045em}h2{font-size:52px;line-height:1.35;font-weight:600;letter-spacing:-.035em}h3{font-size:36px;font-weight:600}p{font-size:24px;line-height:1.65}.eyebrow{font-size:17px;letter-spacing:.12em;color:var(--subtext);margin-bottom:28px}.lead{margin-top:24px;color:var(--subtext)}.foot{font-size:15px;color:var(--subtext);margin-top:40px;line-height:1.55}.number{font-weight:600;letter-spacing:-.065em;display:inline-block;font-variant-numeric:tabular-nums}.ten{color:var(--rust)}
.cover .stage{display:grid;grid-template-columns:1.15fr .85fr;align-items:center;gap:50px}.cover .display{font-size:210px;line-height:1.05;white-space:nowrap}.cover .promise{margin-top:22px;font-size:20px}.cover .intro{font-size:26px;margin-top:32px}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:70px;margin-top:45px}.baseline{border-right:2px solid var(--line);padding-right:60px}.metric{font-size:104px;line-height:1.1;margin:18px 0}.metric-label{font-size:21px;color:var(--subtext)}.relay-list{display:flex;flex-direction:column;gap:15px;margin-top:30px}.relay-row{display:flex;align-items:center;gap:22px;font-size:23px}.relay-row .object{font-size:28px;min-width:108px}.object{display:inline-block;line-height:1.25;white-space:nowrap}.saving{font-size:80px;line-height:1.1;margin:20px 0}.small{font-size:20px;color:var(--subtext)}
.items{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px;margin-top:46px}.prep{background:var(--pale);border-radius:26px;padding:38px 32px;min-width:0}.prep .object{font-size:54px}.prep .verb{font-size:25px;line-height:1.5;margin-top:36px}.prep .detail{font-size:20px;color:var(--subtext);margin-top:20px;line-height:1.65}.prep .time{font-size:18px;margin-top:26px;color:var(--rust)}
.night{display:flex;flex-direction:column;gap:18px;margin-top:30px}.night-row{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding:10px 0 22px;gap:20px}.night-row .object{font-size:32px}.night-row p{font-size:23px}.test-days{display:inline-block;font-size:31px;color:var(--accent);font-weight:600}.dayline{margin-top:30px}.decision{display:grid;grid-template-columns:.8fr 1.2fr;gap:70px;margin-top:38px}.decision .test-days{font-size:108px;line-height:1.2}.measure{display:grid;grid-template-columns:1fr 1fr;gap:24px}.measure div{border-top:3px solid var(--accent);padding-top:16px}.measure h3{font-size:26px}.measure p{font-size:20px;color:var(--subtext);margin-top:12px}.finish{margin-top:34px;font-size:22px;font-weight:600}
@keyframes ms-fade{from{opacity:0}to{opacity:1}}@keyframes ms-rise{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}@keyframes ms-scale-in{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:scale(1)}}@keyframes ms-slide-up{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:translateY(0)}}
'''
BRIDGE="""// Catalog navigation only. Native runtime owns rendering, animation and cursor.
(()=>{let pending=null,timer;
 const move=()=>{if(pending===null)return;if(typeof go!=='function'||typeof cur!=='number'){timer=setTimeout(move,100);return}if(cur===pending){pending=null;return}if(typeof animating==='undefined'||!animating)go(cur,pending);timer=setTimeout(move,100)};
 addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin)return;
  const d=e.data;if(!d||d.type!=='yebisu-slide'||!Number.isInteger(d.index))return;
  pending=Math.max(0,Math.min(document.querySelectorAll('#deck>.slide').length-1,d.index));clearTimeout(timer);move();
 });
})();
"""
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def save(p,obj):write(p,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def run(args,out,name):
 env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True,encoding='utf-8',errors='replace',env=env)
 write(out/'source/logs'/name,json.dumps(list(map(str,args)),ensure_ascii=False)+'\n'+p.stdout+'\n'+p.stderr)
 if p.returncode:raise RuntimeError(f'{name}: exit {p.returncode}')
def derive_runtime(up,out):
 import difflib
 dest=out/'source/ja-runtime/scripts'
 shutil.copytree(up/'scripts',dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 original=(up/'scripts/inject-runtime.py').read_text(encoding='utf-8')
 marker='  var deckBadge=document.getElementById(\'ms-deck-badge\');'
 if original.count(marker)!=1:raise RuntimeError('Pinned injector scope patch marker changed')
 patched=original.replace(marker,'  window.msAuthFetch=msAuthFetch; // Share the existing authenticated closure with QA.\n'+marker)
 write(dest/'inject-runtime.py',patched)
 write(out/'source/ja-runtime/changes.diff',''.join(difflib.unified_diff(original.splitlines(True),patched.splitlines(True),fromfile='upstream/scripts/inject-runtime.py',tofile='ja-runtime/scripts/inject-runtime.py')))
 save(out/'source/ja-runtime/changes.json',{'reason':'QA IIFE calls msAuthFetch but upstream defined it inside the edit/save IIFE. Export the existing authenticated closure before the scheduled QA load.','original_sha256':sha(up/'scripts/inject-runtime.py'),'derived_sha256':sha(dest/'inject-runtime.py'),'server_sha256':sha(dest/'serve.py'),'server_unchanged':sha(dest/'serve.py')==sha(up/'scripts/serve.py'),'changed_behavior':'Authenticated QA note reading can access the existing helper.','unchanged_security':['Token discovery/cache/headers unchanged','Original serve.py authentication and path restrictions unchanged','No plain-fetch replacement or auth bypass','All injected UI/motion retained'],'authorization':'User requested fork/refinement; parent explicitly authorized this local repair.'})
 return dest
def anchor(name,ident,cls='object'):return f'<span class="{cls}" data-magic-id="{ident}" data-magic-line="nowrap">{html.escape(str(name))}</span>'
def section(n,body,data,cls=''):
 return f'<section class="slide {cls}" data-id="morning-{n}" data-transition="fade" data-stagger="cascade" data-bg="light" data-speaker-notes="{html.escape(data["notes"][n-1],quote=True)}"><div class="slide-content"><div class="stage">{body}</div></div></section>'
def create_sources(out,data,fontroot):
 e=html.escape;d=data;items=d['items'];gain=d['baseline']-d['target'];formula=' ＋ '.join(str(x['minutes'])+'分' for x in items)
 notice='<p class="foot">架空の実験案。時間は仮定値・目標値で、短縮効果は未検証。</p>'
 ten=anchor(f'{gain}分','saving','number ten');target=anchor(f'{d["target"]}分','target','number');days=anchor(f'{d["days"]}日間','days','test-days')
 slides=[]
 slides.append(section(1,f'<div><p class="eyebrow">平日の支度を見直す、小さな実験</p><h1>{e(d["titles"][0])}</h1><p class="intro">急ぐより、前夜へ。</p>{notice}</div><div><div class="display">{ten}</div><p class="promise">朝に取り戻したい時間</p></div>',d,'cover'))
 rows=''.join(f'<div class="relay-row">{anchor(x["name"],"object-"+str(i))}<span>{x["minutes"]}分を候補に</span></div>' for i,x in enumerate(items))
 slides.append(section(2,f'<h2>{e(d["titles"][1])}</h2><div class="compare"><div class="baseline"><p class="metric-label">朝の支度：仮の現状</p><div class="metric number">{d["baseline"]}分</div><p class="small">起床から出発までの時間</p><div class="relay-list">{rows}</div></div><div><p class="metric-label">前夜へ移す短縮候補の合計</p><div class="saving">{ten}</div><p>{formula}</p><p class="lead">目標は <strong>{d["target"]}分</strong>。<br>まず「選ぶ・探す・詰める」を見直す。</p></div></div>{notice}',d))
 cards=''.join(f'<article class="prep"><h3>{anchor(x["name"],"object-"+str(i))}</h3><p class="verb">{e(x["action"])}</p><p class="detail">{e(x["detail"])}</p><p class="time">朝の短縮候補：{x["minutes"]}分（仮定）</p></article>' for i,x in enumerate(items))
 slides.append(section(3,f'<h2>{e(d["titles"][2])}</h2><div class="items">{cards}</div><p class="foot">準備品は同じ場所へ。前夜の作業時間も、別に記録する。</p>',d))
 night=''.join(f'<div class="night-row">{anchor(x["name"],"object-"+str(i))}<p>{e(x["action"])}</p></div>' for i,x in enumerate(items))
 slides.append(section(4,f'<h2>{e(d["titles"][3])}</h2><div class="compare"><div class="baseline"><p class="eyebrow">前夜：選択と準備</p><div class="night">{night}</div></div><div><p class="metric-label">朝：確認して、出発</p><div class="metric">{target}</div><p class="small">起床から出発までの目標</p><p class="dayline">まずは {days} 試す。</p><p class="lead">忘れ物がないかを確認。<br>速さより、無理なく続けられるか。</p></div></div><p class="foot">前夜に増えた時間も計測。朝だけ短くても、一日の負担が増えれば調整する。</p>',d))
 slides.append(section(5,f'<h2>{e(d["titles"][4])}</h2><div class="decision"><div>{days}<p class="lead">朝の目標は {target}。</p><p class="small">記録はまだありません。</p></div><div><div class="measure"><div><h3>朝の時間</h3><p>起床 → 出発を計測</p></div><div><h3>前夜の時間</h3><p>追加準備にかかった時間</p></div><div><h3>忘れ物</h3><p>有無と、何を忘れたか</p></div><div><h3>負担感</h3><p>続けやすさを一言で</p></div></div><p class="finish">朝の短縮と一日の負担を比べて、<br>続ける・変えるを決める。</p></div></div><p class="foot">仮定を実績として扱わず、自分の記録で判断する。</p>',d))
 for i,s in enumerate(slides,1):write(out/'sources'/f'slide-{i:02}.html',s)
 write(out/'sources/style.css',CSS);write(out/'sources/i18n.js',BRIDGE);write(out/'sources/head.html','<title>'+e(d['title'])+'</title>')
 for name in ['noto-sans-jp.woff2','notosansjp-OFL.txt']:
  dest=out/'assets/fonts'/name;dest.parent.mkdir(parents=True,exist_ok=True)
  if(fontroot/name).resolve()!=dest.resolve():shutil.copyfile(fontroot/name,dest)
def finalize(out,data,reviewed=False):
 digest=sha(out/'index.html');reviewfile=out/'source/browser-review.json'
 review=json.loads(reviewfile.read_text(encoding='utf-8')) if reviewfile.exists() else None
 if reviewed and(not review or review.get('artifact_sha256')!=digest or review.get('pages_reviewed')!=[1,2,3,4,5]):raise RuntimeError('Current all-page agent review receipt required')
 images=[{'page':i,'file':f'render/slide-{i:02}.png','sha256':sha(out/'render'/f'slide-{i:02}.png')}for i in range(1,6)if(out/'render'/f'slide-{i:02}.png').exists()]
 save(out/'QA.json',{'status':'qa_complete'if reviewed else'awaiting_visual_review','scope':'Agent catalog sample QA; original human revision and adoption gates not completed','human_review':'pending','human_adoption':'pending','page_count':5,'artifact_sha256':digest,'images':images,'visual_review':{'pages_reviewed':[1,2,3,4,5]if reviewed else[],'method':'原典serveのQA Overviewを最初にcaptureし、全5頁の日本語実表示と4隣接境界のFLIP・移動を確認' if reviewed else 'pending','overview_first':bool(reviewed and review.get('overview_first')),'result':'All final pages viewed, original native FLIP and navigation verified'if reviewed else'Pending fresh overview and page review'},'browser_review':review if reviewed else None})
 upstream=out/'source/upstream';refs=[{'path':p.relative_to(upstream).as_posix(),'sha256':sha(p),'url':f'https://github.com/{REPO}/blob/{COMMIT}/'+p.relative_to(upstream).as_posix()}for p in sorted(upstream.rglob('*'))if p.is_file()]
 save(out/'PROVENANCE.json',{'repository':REPO,'upstream_commit':COMMIT,'references':refs,'execution_type':'original_modular_html_with_authenticated_qa_scope_fix','generator':'tools/build_magic_slide_repository_example.py','input_sha256':sha(out/'input/data.json'),'artifact_sha256':digest,'output':'index.html','commands_executed':[{'argv':json.loads((out/'source/logs'/name).read_text(encoding='utf-8-sig').splitlines()[0]),'exit_code':0,'log':'source/logs/'+name,'log_sha256':sha(out/'source/logs'/name)}for name in ['merge.log','inject.log']],'preview_server_receipt':{'state':'running_when_reviewed','log':'source/logs/serve.log','log_sha256':sha(out/'source/logs/serve.log')} if (out/'source/logs/serve.log').exists() else None,'runtime_changes':'source/ja-runtime/changes.diff: expose existing authenticated closure to QA; original source preserved','local_changes':['Japanese modular content/CSS/notes and local OFL font.','Minimal same-origin parent bridge invokes original go(cur,index) only.','One explicit derived injector line exposes the existing authenticated msAuthFetch closure to QA. No security bypass or feature suppression.'],'api_calls':0,'license':'MIT original, Noto Sans JP OFL','human_revision_gate':'pending; autonomous sample and separate agent QA requested by user','navigation':'global go(from,to), cur, native arrows/dock/overview','static_limitations':'Presentation-only. Edit/Save/image replacement require original serve.py; runtime controls retained unchanged.'})
 if Path(__file__).resolve()!=(out/'source/build_magic_slide_repository_example.py').resolve():shutil.copyfile(Path(__file__),out/'source/build_magic_slide_repository_example.py')
 write(out/'README.md','''# Magic Slide：朝の支度を10分短くする企画

原典Magic SlideのHTMLとFLIPを実行した、日本語5枚の架空の実験案です。40分→30分、服4分・鍵3分・バッグ3分は仮定で、実績ではありません。前夜の準備時間も含めて効果を確かめる構成です。

`sources/outline.md` と `brief.md` → 各slide-XX.html/style.css → 原典merge-slides.py → 認証scopeを1行修正した派生inject-runtime.py → 原典と同一のserve.pyで制作。10分、服・鍵・バッグ、30分・5日間を隣接ページに引き継ぎます。講稿はdata-speaker-notesに保持。原典のcursor・stagger・Magic Move・dock・Overview・編集UIを保持しています。

## 表示と編集

静的サイトのiframeはプレゼン用です。矢印、dock、一覧などの表示操作を使います。編集・Save・画像差し替えは原典preview serverが必要です。静的サイトでは保存できません。日本語本文に対し、原典UIのja未登録文字列は原典のEnglish fallbackになります。

このフォルダで `python source/ja-runtime/scripts/serve.py index.html --no-open` を実行し、表示された /deck/ のURLを開いてください。Python標準ライブラリのみ。生成時にはNodeの構文検査を利用しています。画像生成APIや認証情報は不要です。

## 再生成

リポジトリから: `python tools/build_magic_slide_repository_example.py --output-dir morning-regenerated --input examples/repositories/magic-slide/input/data.json`。

このフォルダ単体から: `python source/build_magic_slide_repository_example.py --upstream source/upstream --input input/data.json --font-dir assets/fonts --output-dir ../morning-regenerated`。

既存HTMLを編集した場合は `--source-dir sources` を指定すると、そのモジュールを原典で再merge/injectします。生成先は別フォルダを推奨。再生成は常にawaiting_visual_reviewとなり、今回の合格を引き継ぎません。raw原典はsource/upstreamへ無改変保持。派生runtimeはsource/ja-runtimeへ分離します。

## 原典不具合と局所修正

原典のQAノート読出しが別IIFE内のmsAuthFetchを参照し、ReferenceErrorになりました。source/upstream-failureに実行時の記録を保存。派生injectorは既存の認証付きclosureをwindowへ公開する1行だけを追加します。トークン取得・header付与・server認証・保存パス制限は原典のままです。source/ja-runtime/changes.diffとchanges.jsonが正確な差分です。保存後の再注入にも同じ修正が使われるよう、編集はja-runtime側のserve.pyから起動してください。

## QAと採用状態

原典serve.pyのQA Overview captureを先に視認。その後、依頼されたカタログ実例の検査として全頁とnative motion/navigationを検証しました。記録はQA.jsonとsource/browser-review.json。Agent QAと人によるRevision/正式採用は別です。原典が求める人のレビューはpendingです。

原典MITとNoto Sans JP OFLを同梱。外部写真なし。固定コミット、原典hash、入力/成果物hash、実行ログはPROVENANCE.jsonとsource/に保存しています。
''')
 if out.resolve()==DEFAULT.resolve():
  p='examples/repositories/magic-slide/'
  row={'id':'magic-slide','title':data['title'],'use_case':'生活改善・実験企画','repository':REPO,'skill_repository':REPO,'upstream_commit':COMMIT,'fork_id':None,'page_count':5,'format':'html','preview_kind':'html','style':'Magic Slide / Morning Tray','cover':p+'render/slide-01.png','interior':p+'render/slide-03.png','preview':p+'index.html','preview_options':{'ms_no_presenter':'1'},'preview_notice':'このプレビューでは動きとページ移動を確認できます。本文の編集・保存は、ZIPを展開して専用プレビューを起動してください。','artifact_download':p+'index.html','source_download':p+'source/build_magic_slide_repository_example.py','input':p+'input/BRIEF.md','input_data':p+'input/data.json','prompt':p+'PROMPT.txt','prompt_text':PROMPT,'provenance':p+'PROVENANCE.json','qa':p+'QA.json','guide':p+'README.md','titles':data['titles'],'notes':data['notes'],'pages':[p+f'render/slide-{i:02}.png'for i in range(1,6)],'input_sha256':sha(out/'input/data.json'),'method':'原典merge-slides / auth scopeのみ派生injector / original serve / native Magic Move','sample_notice':data['notice'],'editability':'html_source','navigation':'native-runtime-bridge'}
  save(ROOT/'data/magicslide-repository-examples.json',[row]);save(ROOT/'data/magicslide-repository-guides.json',[{'repository':REPO,'execution_type':'original_modular_html_with_authenticated_qa_scope_fix','execution_status':'generated_and_reviewed'if reviewed else'generated_awaiting_review','case_ids':['magic-slide'],'summary_ja':'原典Magic Moveで時間と準備品を隣接頁へ受け渡す、日本語5枚の生活実験案。','requirements':['Python3 / 原典serve.py','Node（injectorのJS構文検査）','Playwright（表示QA）'],'steps':['outline/briefとsourcesを編集','原典merge-slides.py','認証scopeのみ修正した派生inject-runtime.py','原典serve.py→Overview→依頼範囲のagent QA'],'commands':['python tools/build_magic_slide_repository_example.py --output-dir morning-regenerated'],'source_refs':refs,'limitations':['架空の試行計画で短縮効果は未検証。','静的iframeは表示用。編集・保存には原典serve.pyが必要。','Agent QA完了でも原典human revision/adoption gateはpending。'],'guide':p+'README.md'}])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=DEFAULT);ap.add_argument('--upstream',type=Path);ap.add_argument('--input',type=Path);ap.add_argument('--font-dir',type=Path);ap.add_argument('--source-dir',type=Path);ap.add_argument('--finalize-only',action='store_true');ap.add_argument('--reviewed',action='store_true');a=ap.parse_args();out=a.output_dir.resolve()
 data=json.loads(a.input.read_text(encoding='utf-8'))if a.input else DATA
 if len(data['titles'])!=5 or len(data['notes'])!=5 or len(data['items'])!=3:raise ValueError('This authored sample requires five pages and three preparation items')
 if sum(x['minutes']for x in data['items'])!=data['baseline']-data['target']:raise ValueError('Saving assumptions must sum to baseline minus target')
 up=a.upstream or ROOT/'.build/actual-upstreams/daniel-style__magic-slide'
 if not up.exists():up=Path(__file__).resolve().parent/'upstream'
 if not up.exists():up=DEFAULT/'source/upstream'
 up=up.resolve();fonts=a.font_dir or ROOT/'assets/fonts'
 if not fonts.exists():fonts=Path(__file__).resolve().parent.parent/'assets/fonts'
 if not a.finalize_only:
  out.mkdir(parents=True,exist_ok=True);save(out/'input/data.json',data);write(out/'input/BRIEF.md',BRIEF+'\n'+data['notice']);write(out/'PROMPT.txt',PROMPT)
  dst=out/'source/upstream'
  if dst.resolve()!=up:
   for f in ['LICENSE','SKILL.md','AGENTS.md','README.md']:(dst/f).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(up/f,dst/f)
   for f in ['scripts','references']:shutil.copytree(up/f,dst/f,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
  shutil.copyfile(up/'LICENSE',out/'LICENSE')
  if a.source_dir:
   shutil.copytree(a.source_dir,out/'sources',dirs_exist_ok=True)
   (out/'assets/fonts').mkdir(parents=True,exist_ok=True)
   for n in ['noto-sans-jp.woff2','notosansjp-OFL.txt']:shutil.copyfile(fonts/n,out/'assets/fonts'/n)
  else:create_sources(out,data,fonts)
  write(out/'sources/brief.md',BRIEF)
  write(out/'sources/outline.md','# Outline\n\nThesis: 朝の選択と準備を前夜へ移し、朝の短縮と一日の負担を両方測る。\nAudience: 本人・家族。\nClosing: 実績を記録して継続・変更を決める。\n\n'+'\n'.join(f'{i}. {t}\n   {data["notes"][i-1]}'for i,t in enumerate(data['titles'],1))+'\n\n'+BRIEF)
  write(out/'NOTES.md','\n\n'.join(f'## {i}. {t}\n\n{data["notes"][i-1]}'for i,t in enumerate(data['titles'],1)))
  runtime=derive_runtime(up,out)
  run([sys.executable,up/'scripts/merge-slides.py',out/'sources','--lang','ja'],out,'merge.log');run([sys.executable,runtime/'inject-runtime.py',out/'index.html','--lang','ja'],out,'inject.log')
 finalize(out,data,a.reviewed)
if __name__=='__main__':main()
