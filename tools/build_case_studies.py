"""Build actual Japanese cases from original pinned upstream templates."""
from pathlib import Path
import argparse,base64,hashlib,html,json,re,shutil,zipfile
from business_web_content import frontend_cafe,frontend_git,magazine_port,swiss_knowledge
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/".build/actual-upstreams"
def read(p): return Path(p).read_text(encoding="utf-8-sig")
def write(p,s):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    Path(p).write_text(s,encoding="utf-8")
def dump(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def sha(b): return hashlib.sha256(b).hexdigest()
def ih(d): return sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
DATA=json.loads(read(ROOT/"data/case-inputs.json"))
UPS={r["repository"]:r for r in json.loads(read(ROOT/"data/upstreams.json"))}
CASES=[
("cafe-pptx","cafe","ppt-master-ja","hugohe3/ppt-master","pptx","編集可能なPPTX","提案・決裁"),
("ec-monthly","ec","ppt-master-ja","hugohe3/ppt-master","pptx","編集可能なPPTX","月次報告"),
("cafe-web","cafe","frontend-slides-ja","zarazhangrui/frontend-slides","html","Bold Signal","提案・説明会"),
("git-onboarding","git","frontend-slides-ja","zarazhangrui/frontend-slides","html","Terminal Green","研修・技術解説"),
("port-town","harbor","guizang-ppt-skill-ja","op7418/guizang-ppt-skill","html","Magazine / Ink Classic","企画提案"),
("knowledge-search","knowledge","guizang-ppt-skill-ja","op7418/guizang-ppt-skill","html","Swiss / IKB","業務改善")]
def replace(pattern,value,s,label):
    result,n=re.subn(pattern,lambda _:value,s,count=1,flags=re.S)
    if n!=1: raise ValueError("Missing upstream anchor: "+label)
    return result
def fonts(style):
    wanted={"Bold Signal":["Archivo Black","Space Grotesk"],"Terminal Green":["JetBrains Mono"],"Magazine / Ink Classic":["Playfair Display","Source Serif 4","IBM Plex Mono"],"Swiss / IKB":["Inter","JetBrains Mono"]}[style]
    entries=[(x["family"],ROOT/x["file"],"truetype","100 900") for x in json.loads(read(ROOT/"data/preset-fonts.json")) if x["family"] in wanted]
    entries += [("Noto Sans JP",ROOT/"assets/fonts/noto-sans-jp.woff2","woff2","100 900"),("Noto Serif JP",ROOT/"assets/fonts/noto-serif-jp.woff2","woff2","100 900"),("BIZ UDPGothic",ROOT/"assets/fonts/biz-udpgothic-regular.woff2","woff2","400"),("BIZ UDPGothic",ROOT/"assets/fonts/biz-udpgothic-bold.woff2","woff2","700")]
    return "\n".join("@font-face{font-family:'%s';src:url(data:%s;base64,%s) format('%s');font-weight:%s;font-display:swap}"%(family,"font/woff2" if fmt=="woff2" else "font/ttf",base64.b64encode(p.read_bytes()).decode(),fmt,weight) for family,p,fmt,weight in entries)
def finish(doc,title,style,kind):
    doc=re.sub(r"<link\b[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com|api\.fontshare\.com)[^>]*>","",doc)
    doc=re.sub(r"<html[^>]*>",'<html lang="ja" data-upstream="'+kind+'">',doc,count=1)
    doc=replace(r"<title>.*?</title>","<title>"+html.escape(title)+"</title>",doc,"title")
    doc=doc.replace("Noto Sans SC","Noto Sans JP").replace("Noto Serif SC","Noto Serif JP")
    css=read(ROOT/"assets/case-slides.css").replace(":root{",":root[data-upstream=frontend]{")
    escape="<script>if(parent!==window)document.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();parent.postMessage({type:'yebisu-close'},location.origin)}},true);</script>"
    return doc.replace("</head>","<style>"+fonts(style)+"\n"+css+"</style></head>",1).replace("</body>",escape+"</body>")
def frontend(cid,title,roster,style,hashvalue):
    upstream=UP/"zarazhangrui__frontend-slides"
    fence=chr(96)*3
    m=re.search(fence+r"html\s*\n(.*?)\n"+fence,read(upstream/"html-template.md"),re.S)
    if not m: raise ValueError("Missing HTML fence")
    doc=m.group(1).replace("/* --- PASTE viewport-base.css CONTENTS HERE --- */",read(upstream/"viewport-base.css"))
    sections=[]
    for i,(_,body,_) in enumerate(roster,1):
        sections.append('<section class="slide frontend" data-slide-id="page-%d"><div class="slide-top"><span class="number">%02d</span><span class="breadcrumbs">%s</span></div>%s<div class="slide-footer"><span>架空の制作サンプル / STUDIO YEBISU</span><span>%02d / %02d</span></div></section>'%(i,i,html.escape(style),body,i,len(roster)))
    doc=replace(r'<main class="deck-stage" id="deckStage">.*?</main>','<main class="deck-stage" id="deckStage">'+"\n".join(sections)+"</main>",doc,"stage")
    keyboard="""document.addEventListener('keydown',e=>{
if(e.target.isContentEditable||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;
if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide+1)}
if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();this.showSlide(this.currentSlide-1)}
if(e.key==='Home'){e.preventDefault();this.showSlide(0)}
if(e.key==='End'){e.preventDefault();this.showSlide(this.slides.length-1)}});"""
    touch="""let x=0,y=0,last=0;
document.addEventListener('touchstart',e=>{x=e.changedTouches[0].clientX;y=e.changedTouches[0].clientY},{passive:true});
document.addEventListener('touchend',e=>{if(e.target.isContentEditable)return;const dx=e.changedTouches[0].clientX-x,dy=e.changedTouches[0].clientY-y;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))this.showSlide(this.currentSlide+(dx<0?1:-1))},{passive:true});
document.addEventListener('wheel',e=>{if(e.target.isContentEditable)return;const now=Date.now();if(Math.abs(e.deltaY)>20&&now-last>550){last=now;this.showSlide(this.currentSlide+(e.deltaY>0?1:-1))}},{passive:true});"""
    doc=doc.replace("// Arrow keys, Space, Page Up/Down",keyboard).replace("// Touch/swipe support for mobile",touch)
    doc=doc.replace("showSlide(index) {","""showSlide(index) {
if(!Number.isFinite(index))return;
const requested=Math.max(0,Math.min(index,this.slides.length-1));
const counter=document.getElementById('page-count');if(counter)counter.textContent=(requested+1)+' / '+this.slides.length;
if(parent!==window)parent.postMessage({type:'yebisu-page',index:requested},location.origin);""")
    doc=doc.replace("new SlidePresentation();","const presentation = new SlidePresentation();")
    if cid=="git-onboarding": doc=doc.replace("<body>",'<body class="terminal">',1)
    controls='<div class="deck-controls"><button id="prev" aria-label="前のページ">←</button><span id="page-count"></span><button id="next" aria-label="次のページ">→</button></div><div class="edit-hotzone"></div><button id="editToggle" class="edit-toggle" aria-label="編集切替">編集 E</button>'
    doc=doc.replace("<script>",controls+"\n<script>",1)
    editor=read(ROOT/"assets/case-editor.js").replace("CASE_STORAGE_KEY","yebisu-"+cid+"-"+hashvalue[:16]).replace("CASE_ID",cid)
    sync="window.addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;presentation.showSlide(e.data.index)});"
    doc=doc.replace("</body>","<script>"+editor+"\n"+sync+"</script></body>")
    return finish(doc,title,style,"frontend")
def guizang(cid,title,roster,style,folder):
    upstream=UP/"op7418__guizang-ppt-skill"
    doc=read(upstream/("assets/template-swiss.html" if cid=="knowledge-search" else "assets/template.html"))
    for old,new in {"开始计时":"計時を開始","重置计时":"計時をリセット","继续计时":"計時を再開","暂停计时":"計時を一時停止"}.items():doc=doc.replace(old,new)
    doc=replace(r'<div id="deck">.*?</div>\s*<div id="nav">','<div id="deck">'+"\n".join(r[1] for r in roster)+'</div>\n<div id="nav">',doc,"deck")
    notes=[]
    for i,(title,_,note) in enumerate(roster,1):
        talk=[s+"。" for s in note.split("。") if s.strip()]
        talk += ["このページの内容を次の判断につなげます。","数値と計画は架空の制作サンプルです。"][:max(0,3-len(talk))]
        notes.append(dict(id="page-"+str(i),title=title,purpose=title,talk=talk,transition="次のページへ進みます。" if i<len(roster) else "判断事項を確認します。"))
    doc=replace(r"const SPEAKER_NOTES\s*=\s*\[.*?\]\s*;","const SPEAKER_NOTES = "+json.dumps(notes,ensure_ascii=False)+";",doc,"notes")
    translations={"演讲者视图":"発表者ビュー","演讲模式":"発表者モード","演示设置":"発表設定","演讲者布局":"発表者の配置","当前页":"現在のページ","下一页":"次のページ","上一页":"前のページ","观众屏":"観客画面","快捷控制":"クイック操作","快捷键":"ショートカット","总览":"一覧","翻页":"ページ送り","静态":"静止","动态":"動作","讲稿":"発表メモ","倒计时":"残り時間","暂停":"一時停止","开始":"開始","继续":"再開","重置":"リセット","全屏":"全画面","返回":"戻る","结束":"終了","自动翻页":"自動ページ送り","全局间隔":"共通の間隔","页面优先":"ページ優先","备注优先":"メモ優先","均衡":"均等","保存":"保存","备注":"メモ","黑屏":"黒画面","白屏":"白画面","冻结":"固定","正常":"通常","需要时手动开启，默认关闭":"必要に応じて手動でオン。初期状態はオフ。"}
    for old,new in sorted(translations.items(),key=lambda row:-len(row[0])):doc=doc.replace(old,new)
    doc=doc.replace("https://unpkg.com/lucide@latest/dist/umd/lucide.min.js","./assets/lucide.min.js")
    assets=folder/"assets";assets.mkdir(exist_ok=True)
    shutil.copy2(upstream/"assets/motion.min.js",assets/"motion.min.js")
    for name in ["lucide.min.js","lucide-LICENSE.txt","motion-LICENSE.txt"]: shutil.copy2(ROOT/"sources/browser-dependencies"/name,assets/name)
    sync="""if(parent!==window)document.documentElement.classList.add('catalog-embedded');
const upstreamGo=go;
go=function(n,opts={}){if(matchMedia('(prefers-reduced-motion: reduce)').matches)opts.force=true;upstreamGo(n,opts);if(parent!==window)parent.postMessage({type:'yebisu-page',index:idx},location.origin)};
window.addEventListener('message',e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide'||!Number.isInteger(e.data.index))return;go(e.data.index,{force:true})});"""
    result=finish(doc.replace("</body>","<script>"+sync+"</script></body>"),DATA["knowledge" if cid=="knowledge-search" else "harbor"]["title"],style,"guizang")
    if cid=="port-town":
        import importlib.util
        path=folder/'source/port_locale_notes.py'
        spec=importlib.util.spec_from_file_location('port_locale_notes',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        result=module.apply_locale_notes(result)
    return result
def evidence(repo,cid):
    upstream=UP/repo.replace("/","__")
    if repo=="hugohe3/ppt-master":
        refs=["skills/ppt-master/"+s for s in ["SKILL.md","scripts/attribution_guard.py","scripts/svg_quality_checker.py","scripts/svg_to_pptx.py","workflows/profiles/quick-generate.md"]]
    elif repo=="zarazhangrui/frontend-slides": refs=["SKILL.md","STYLE_PRESETS.md","html-template.md","viewport-base.css"]
    else:
        refs=["SKILL.md","assets/template-swiss.html" if cid=="knowledge-search" else "assets/template.html"]
        refs += [p.relative_to(upstream).as_posix() for p in (upstream/"references").glob("*swiss*")] if cid=="knowledge-search" else [p.relative_to(upstream).as_posix() for p in (upstream/"references").glob("*layout*")]
    return [dict(path=p,sha256=sha((upstream/p).read_bytes())) for p in refs if (upstream/p).is_file()]
def case_files(cfg,roster,folder):
    cid,key,fork,repo,fmt,style,use=cfg
    data=DATA[key];title=data["title"];native=fmt=="pptx";hashed=ih(data);n=len(roster)
    prompt=("「"+title+"」を"+fork+"で日本語の"+str(n)+"枚にしてください。\ninput/data.jsonを数値・事実・仮定の正本とします。読者："+data["audience"]+"\n構成："+" → ".join(r[0] for r in roster)+"。\n出力："+("編集可能なPPTX、閲覧用PDF、ページ別講稿。" if native else style+"の元テンプレートを使用したHTML一式と講稿。")+"\n単位・比較期間を揃え、仮説と事実、目標と実績を区別。日本語字形と改行を実表示で確認。架空のサンプルと明記し、原典・条件・制作ソースを保持。実施した検証だけを記録してください。\n")
    dump(folder/"input/data.json",data)
    write(folder/"input/BRIEF.md","# "+title+"\n\n"+DATA["notice"]+"\n\n読者："+data["audience"]+"\n\n入力：[data.json](data.json)\n\n入力SHA-256："+hashed+"\n\n## 構成\n\n"+"\n".join(str(i)+". "+r[0] for i,r in enumerate(roster,1))+"\n")
    prompt="$"+fork+" を使ってください。\n\n"+prompt
    write(folder/"PROMPT.txt",prompt)
    write(folder/"NOTES.md","# 発表用講稿\n\n"+"\n\n".join("## "+str(i)+". "+r[0]+"\n\n"+r[2] for i,r in enumerate(roster,1))+"\n")
    license_dir=folder/"licenses/fonts";license_dir.mkdir(parents=True,exist_ok=True)
    for p in (ROOT/"assets/fonts").rglob("*OFL.txt"): shutil.copy2(p,license_dir/p.name)
    shutil.copy2(ROOT/"skill-forks"/fork/"LICENSE",folder/"LICENSE")
    method=("日本語の文字・図形profile。上流guard・checker・native SVG→PPTX変換器を使用。Default全工程ではない。PowerPoint本体でPNG/PDF出力。" if native else "上流SKILL・指定プリセット・固定ステージを適用し、AIが本文を制作。上流の生成CLIを実行したという意味ではない。" if fork=="frontend-slides-ja" else "元HTMLテンプレートに題材別本文を挿入。元ページ制御・演出を維持し、日本語字形・講稿・構図を調整。")
    if not (folder/"QA.json").exists(): dump(folder/"QA.json",dict(status="rendered_pending_visual_review" if native else "generated_pending_browser_review",browser_review="pending",powerpoint_render="render/powerpoint-render.json" if native else None))
    dump(folder/"PROVENANCE.json",dict(case_id=cid,repository=repo,upstream_commit=UPS[repo]["commit"],upstream_files=evidence(repo,cid),fork=fork,method=method,input_sha256=hashed,input="input/data.json",output="deck.pptx" if native else "index.html",generator="tools/make_business_pptx.py" if native else "tools/build_case_studies.py",changes=["日本語入力・講稿","日本語書体と改行","題材別の図表","当地プレビュー同期"],license=UPS[repo].get("github_license"),fonts="licenses/fonts",qa="QA.json",render_report="render/powerpoint-render.json" if native else None))
    reproduction=("リポジトリrootで python tools/make_business_pptx.py。上流依存を導入した .build/ppt-master-venv が必要。\nPowerPoint導入済みWindowsで powershell -NoProfile -File tools/render_powerpoint.ps1 -PresentationPath examples/cases/"+cid+"/deck.pptx -OutputDirectory examples/cases/"+cid+"/render" if native else "リポジトリrootで python tools/build_case_studies.py。元テンプレートを用いた当地の制作処理です。")
    write(folder/"README.md","# "+title+"\n\n"+DATA["notice"]+"\n\n## 閲覧・再制作\n\n"+("deck.pptxをPowerPointで開きます。Noto Sans JPが必要です。閲覧用はrender/deck.pdf。" if native else "フォルダーで python -m http.server 8000 を実行しindex.htmlを開きます。書体はHTML内蔵。Guizangの依存はassetsに同梱。CDN fallbackが残るためオフライン確認結果はQAを参照。")+"\n\ninput/data.jsonとPROMPT.txtを日本語派生スキルへ渡します。NOTES.mdに講稿、PROVENANCE.jsonに原典、QA.jsonに実施状態。\n\n## カタログ全体から再生成\n\n"+reproduction+"\n\nZIPだけにはカタログ生成スクリプト・Python環境を含みません。再生成は同じ出力先を更新するため独自改稿は別の場所へ保存してください。\n\n## 条件\n\nLICENSEとlicenses/fontsを保持。改変ソースは本配布物と https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja のskill-forks/"+fork+"。原作者の公式作例ではありません。\n")
    if cid=="git-onboarding": write(folder/"input/training/README.md","# 練習用プロジェクト\n\nここへ挨拶を一行追加してください。\n")
    p="examples/cases/"+cid+"/"
    record=dict(id=cid,title=title,use_case=use,repository=repo,skill_repository=repo,upstream_commit=UPS[repo]["commit"],fork_id=fork,page_count=n,format=fmt,preview_kind="powerpoint-render" if native else "html",style=style,cover=p+"render/slide-01.png",interior=p+"render/slide-03.png",preview=p+"index.html",artifact_download=p+"deck.pptx" if native else "downloads/"+cid+"-ja.zip",source_download="downloads/"+cid+"-ja.zip",input=p+"input/BRIEF.md",input_data=p+"input/data.json",prompt=p+"PROMPT.txt",prompt_text=prompt,provenance=p+"PROVENANCE.json",qa=p+"QA.json",fork_download="downloads/"+fork+".zip",guide="case.html?id="+cid,titles=[r[0] for r in roster],notes=[r[2] for r in roster],method=method,sample_notice=DATA["notice"],input_sha256=hashed)
    if native: record.update(pages=[p+"render/slide-%02d.png"%i for i in range(1,n+1)],pdf_download=p+"render/deck.pdf")
    if key=="cafe": record["compare_id"]="cafe-web" if native else "cafe-pptx"
    return record
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--package",action="store_true");args=parser.parse_args()
    records=[]
    for cfg in CASES:
        cid,key,fork,repo,fmt,style,_=cfg
        folder=ROOT/"examples/cases"/cid;folder.mkdir(parents=True,exist_ok=True)
        if fmt=="pptx":
            roster=[(r["title"],"",r["note"]) for r in json.loads(read(folder/"roster.json"))]
            if not (folder/"render/powerpoint-render.json").is_file(): raise FileNotFoundError("Render required: "+cid)
        else:
            if cid=="cafe-web": roster=frontend_cafe(DATA[key],json.loads(read(ROOT/"examples/cases/cafe-pptx/calculations.json")))
            elif cid=="git-onboarding": roster=frontend_git(DATA[key])
            elif cid=="port-town": roster=magazine_port(DATA[key])
            else: roster=swiss_knowledge(DATA[key])
            doc=frontend(cid,DATA[key]["title"],roster,style,ih(DATA[key])) if fork=="frontend-slides-ja" else guizang(cid,DATA[key]["title"],roster,style,folder)
            write(folder/"index.html",doc)
        records.append(case_files(cfg,roster,folder))
        if args.package:
            output=ROOT/"downloads"/(cid+"-ja.zip");output.parent.mkdir(exist_ok=True)
            with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED) as archive:
                for p in sorted(folder.rglob("*")):
                    if p.is_file(): archive.write(p,cid+"/"+p.relative_to(folder).as_posix())
        print(cid+": "+str(len(roster))+" slides")
    assert sum(r["page_count"] for r in records)==45
    assert records[0]["input_sha256"]==records[2]["input_sha256"]
    existing_path=ROOT/"data/case-studies.json"
    existing=json.loads(read(existing_path)) if existing_path.exists() else []
    owned={r["id"] for r in records}
    dump(existing_path,records+[c for c in existing if c["id"] not in owned])
    print("Manifest ready: 6 cases / 45 slides")
if __name__=="__main__": main()
