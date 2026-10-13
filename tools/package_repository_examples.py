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
}
FRAGMENTS = ['web','native','japanese','dashi','codex-image']
CODE_SUFFIXES = {'.py','.js','.mjs','.cjs','.jsx','.ts','.tsx','.css','.html','.json','.yaml','.yml','.md','.txt','.toml','.xml','.csv','.svg','.sh','.ps1','.psm1','.ini','.cfg','.in','.sql','.ttf','.woff','.woff2'}
SKIP_PARTS = {'.git','node_modules','__pycache__','.venv','venv','.pytest_cache','.cache','releases','public'}
SPECIAL = {
 'gonta223/japanese-corporate-pptx-skill': ['skills/japanese-corporate-pptx/assets/'],
 'carnot-tech/jinba-consulting-pptx-skill': ['assets/SlideCatalog_16x9.pdf','assets/SuperTemplate_62type.pptx'],
}
NOTES = {
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
 return [p for p in sorted(folder.rglob('*')) if p.is_file() and not (set(p.relative_to(folder).parts)&SKIP_PARTS) and p.suffix!='.pyc' and not p.name.startswith('.env')]

def source_files(folder,repo):
 for p in files(folder):
  name=p.relative_to(folder).as_posix()
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
 own='---\nname: '+fork_id+'\ndescription: '+repo+'の方式で日本語スライドを制作・再現する。原典固有の生成器・テンプレート・実装と個別条件を保ち、実制作例を参考に日本語の資料を作るときに使う。\n---\n\n# '+fork_id+'\n\nStudio Yebisuの日本語派生版。原作者の公式翻訳ではありません。\n\n## 原典を読む\n\n'+paths+'\n\n同梱references/WORKFLOW.mdで、実作例・入力・環境・コマンドと確認範囲を読む。\n\n## 固有の制作方式\n\n'+NOTES[cid]+'\n\n## 日本語で完成させる\n\n- 先に読み手、目的、結論、必要なページ、出力形式を決める。\n- 入力の出典と数値を確認し、万円・件・%・ポイントを区別する。架空条件と評価目標を実績に見せない。\n- 日本語の見出しは意味の区切りで改行し、数字と単位が不自然に分かれないようにする。\n- Webは必要文字を収録したOFL書体を埋め込む。PowerPointは受け手の書体環境と全ページの実描画を確認する。\n- 原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。\n\n## 再現と利用条件\n\n完成例と再現キットはカタログの当該リポに掲載。環境と制約はreferences/WORKFLOW.mdに記載する。上流コードと書体の条件はupstream内の原文を保持し、カタログのCC0を上流へ適用しない。\n'
 # Preserve a human-maintained entrypoint on subsequent packaging runs.
 if not (target/'SKILL.md').exists():write(target/'SKILL.md',own)
 requirements='\n'.join('- '+s for s in profile.get('requirements',[]))
 commands='\n\n'.join('    '+s for s in profile.get('commands',[]) if isinstance(s,str))
 limits='\n'.join('- '+s for s in profile.get('limitations',[]))
 extra='\nDashiのexport engineはこの派生パッケージへ分離収録していません。完全な原典を固定commitで取得して、同じDashi skill内だけで使用します。AGPL対象の対応ソースとtheme05局所差分を保持。専有エンジンは変更しません。\n' if cid=='dashi-ppt' else ''
 workflow='# '+repo+'の日本語制作\n\n原典: https://github.com/'+repo+'/tree/'+case['upstream_commit']+'\n\n'+case['method']+'\n\n'+NOTES[cid]+'\n\n## 作例\n\n- '+case['title']+' / '+str(case['page_count'])+'枚 / '+case['format']+'\n- 完成例: https://studio-yebisu.github.io/awesome-codex-ppt-skills-ja/repository.html?repo='+repo+'\n- 当面のローカル入口: http://127.0.0.1:8847/repository.html?repo='+repo+'\n- 入力、発表者ノート、依頼文、PROVENANCE.json、QA.jsonを完成例に同梱。\n\n## 環境\n\n'+requirements+'\n\n## 元の制作コマンド\n\n'+commands+'\n\n## 確認範囲\n\n'+limits+'\n\n## 権利\n\n原典条件はupstream内のLICENSE/NOTICE等を読む。日本語の独自案内はカタログの条件、上流由来のコードは各原典の条件を引き継ぐ。公開画像や依存書体の条件を一括で保証するものではない。\n'+extra
 workflow=workflow.replace('- 完成例: https://studio-yebisu.github.io/awesome-codex-ppt-skills-ja/repository.html?repo='+repo, '- カタログ内の案内: repository.html?repo='+repo)
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
 requirements=['python-pptx==1.0.2','Pillow==12.3.0','lxml==6.1.3','fonttools==4.63.0','brotli==1.2.0','beautifulsoup4==4.15.0','filelock==4.1.1']
 if cid=='office-powerpoint-mcp':requirements.append('mcp[cli]==1.30.0')
 write(workspace/'requirements-reproduce.txt','\n'.join(requirements)+'\n')
 font=load(ROOT/'data/fonts.json')[0]
 setup=''
 if cid in {'minorun-marp','revealjs-skill'}:setup+='    & npm --prefix .build/repository-runtime ci --ignore-scripts\n    if ($LASTEXITCODE) { throw "npm ci failed" }\n'
 if cid=='dashi-ppt':
  setup+='    & $taskPy tools/acquire_repository.py chuspeeism/dashi-ppt-skill\n    if ($LASTEXITCODE) { throw "Pinned upstream acquisition failed" }\n    & npm --prefix .build/actual-upstreams/chuspeeism__dashi-ppt-skill/skills/dashi-ppt/project ci --ignore-scripts\n    if ($LASTEXITCODE) { throw "Dashi dependencies failed" }\n'
 generation='    & $taskPy tools/'+generator+' '+' '.join(args)+'\n'
 if case['format']=='pptx' and cid!='codex-image-ppt':
  generation='    $taskArgs = @('+','.join('"'+a+'"' for a in args)+')\n    if ($Render) { $taskArgs += "--render" }\n    & $taskPy tools/'+generator+' @taskArgs\n'
 if cid=='codex-image-ppt':
  generation+='    if ($Render) { & pwsh -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/repositories/codex-image-ppt/codex-image-ppt.pptx -OutputDirectory examples/repositories/codex-image-ppt/render }\n'
 fontsetup=''
 if cid!='codex-image-ppt':
  fontsetup='    $taskFont = Join-Path $taskRoot ".build/fonts/NotoSansJP[wght].ttf"\n    if (-not (Test-Path -LiteralPath $taskFont)) {\n        New-Item -ItemType Directory -Path (Split-Path $taskFont) -Force | Out-Null\n        Invoke-WebRequest -Uri "'+font['source_url']+'" -OutFile $taskFont\n    }\n    if ((Get-FileHash -LiteralPath $taskFont -Algorithm SHA256).Hash.ToLower() -ne "'+font['source_sha256']+'") { throw "Pinned font hash mismatch" }\n'
 script='param([switch]$Render)\n$ErrorActionPreference = "Stop"\n$taskRoot = Join-Path $PSScriptRoot "workspace"\nPush-Location -LiteralPath $taskRoot\ntry {\n    & python -m venv .build/ppt-master-venv\n    if ($LASTEXITCODE) { throw "Python environment failed" }\n    $taskPy = Join-Path $taskRoot ".build/ppt-master-venv/Scripts/python.exe"\n    & $taskPy -m pip install -r requirements-reproduce.txt\n    if ($LASTEXITCODE) { throw "Python dependencies failed" }\n'+fontsetup+setup+generation+'    if ($LASTEXITCODE) { throw "Generation failed" }\n    & $taskPy tools/mark_reproduced.py\n    Write-Host "Generated: $taskRoot/examples/repositories/'+cid+'"\n    Write-Host "Open the actual output and review all pages before using it."\n} finally { Pop-Location }\n'
 write(kit/'reproduce/Reproduce.ps1',script)
 mark="from pathlib import Path\nimport json, hashlib\np=Path('examples/repositories/"+cid+"')\nartifact=p/"+repr(Path(case['artifact_download']).name if case['format']=='pptx' else Path(case['preview']).name)+"\n(p/'QA.json').write_text(json.dumps({'status':'generated_awaiting_review','artifact_sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),'visual_review':'Review your reproduced output; the original catalog QA is not transferred to a new run.'},ensure_ascii=False,indent=2),encoding='utf-8')\n"
 write(workspace/'tools/mark_reproduced.py',mark)
 readme='# '+case['title']+'の再現キット\n\n完成資料はこのフォルダー直下。生成経路・使用した原典・当時の確認範囲はPROVENANCE.jsonとQA.jsonに記録しています。\n\n## Windowsで同じ作例を生成\n\n1. ZIPを展開。PowerShellでこのフォルダーへ移動。\n2. Python 3.13、Node.js、必要に応じてGit Bashを用意。\n3. 次を実行（project内venv・固定npm依存・公式固定commitの書体を取得します）。\n\n    .\\reproduce\\Reproduce.ps1\n\n生成先: reproduce/workspace/examples/repositories/'+cid+'/\n\nPowerPoint本体でPNG/PDFを描画する場合は、Noto Sans JPをインストール済みのWindows / PowerPoint / pwshを使用し、-Renderを指定します。HTMLは生成したファイルを開き、原典のページ操作を使います。再生成した出力は確認前として記録し、元のQAを成功扱いで引き継ぎません。\n\n## 自分の題材へ\n\n完成例のinputとPROMPT.txtを参考に、読み手・目的・数値・結論を用意。日本語派生版SKILL.mdから当該原典の手順へ進みます。この再現スクリプトは比較用の固定原稿を作るもので、input/data.jsonだけを変えれば全ページの文章が自動で変わる汎用アプリではありません。\n\n'+NOTES[cid]+'\n\n## 原典と権利\n\nhttps://github.com/'+repo+'/tree/'+case['upstream_commit']+'\n\n原典のコード、個別のライセンス、書体のOFLを保持。原典の広告用画像・動画・不要な既存デッキや実行環境はキットへ収録しません。\n'
 if cid=='codex-image-ppt':readme+='\nこのスクリプトは生成済みの3画像を原典assemble_ppt.pyで組み直すだけです。画像を新たに作るには、promptsとstyleを添えてCodex native image_genへ依頼し、原典のjobs/result記録と画像確認を行ってください。APIや画像生成をこのスクリプトから自動実行しません。\n'
 if cid in {'minorun-marp','revealjs-skill'} and (ROOT/'data/dependency-qa.json').exists():
  copy(ROOT/'data/dependency-qa.json',kit/'source/dependency-qa.json')
  readme+='\n固定npm依存の監査記録はsource/dependency-qa.jsonです。Marp CLI側の依存に未修正の検出項目があります。今回の再現は同梱した原稿のHTML生成を対象とし、サイトのHTTPサーバーではこのCLIを実行していません。\n'
 if cid=='dashi-ppt':readme+='\nDashi専有エンジンを分離再配布しません。スクリプトは完全な原典を固定commitで取得し、そのDashi skill内のHTML生成を実行します。PPTX/PDFエンジンの動作検証は今回の作例に含みません。\n'
 write(kit/'REPRODUCE.md',readme);write(folder/'REPRODUCE.md',readme)
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
   if c['format']=='html':c['artifact_download']=kit
   profiles[c['repository']]['fork']=fork.name
   packaged+=1
  dump(fragment,cases)
 for name in FRAGMENTS:
  p=ROOT/'data'/(name+'-repository-guides.json')
  if p.exists():dump(p,[profiles[v['repository']] for v in load(p)])
 print(str(packaged)+' repository examples packaged with distinct Japanese forks and reproduction workspaces')

if __name__=='__main__':main()
