"""Two repository-specific native executions. Run with the prepared project Python."""
from pathlib import Path
import argparse,asyncio,contextlib,hashlib,importlib.metadata,io,json,os,shutil,subprocess,sys,xml.etree.ElementTree as ET,zipfile
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/".build/actual-upstreams"
OUT=ROOT/"examples/repositories"
CONFIG={"office-powerpoint-mcp":"GongRzhe/Office-PowerPoint-MCP-Server","mck-design":"likaku/Mck-ppt-design-skill"}
def read(p):return Path(p).read_text(encoding="utf-8-sig")
def write(p,s):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(s,encoding="utf-8")
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+"\n")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
EC=json.loads(read(ROOT/"data/case-inputs.json"))["ec"]
TITLES=["くらし便 EC事業 9月報告","売上増と粗利率低下を同時に見る","売上増200万円の中心は自然検索","粗利額は増え、率は2ポイント低下","返品理由の分類と商品説明を先行","次回は施策の完了と利益要因を確認"]
NOTES=[
"架空のEC事業の月次報告です。2026年9月と前年同月を比較し、商品説明の修正と粗利分析を先行する判断を求めます。",
"売上は1,200万円、前年比20%増。粗利率は38%から36%へ2ポイント低下し、返品率は4%から6%へ2ポイント上昇しました。",
"広告20万円、自然検索90万円、メール50万円、リピート直訪40万円の増加で、合計200万円です。構成比と増加額を混同しません。",
"前年粗利は1,000万円×38%=380万円、当月は1,200万円×36%=432万円。52万円の増加です。値引きと商品構成は原因の仮説で、商品別に確認します。",
"10月9日までにCSが返品理由を分類。16日までに商品担当が説明を改稿し、販売担当が粗利差分を分析します。担当名は架空です。",
"広告増額は分析結果を見てから決めます。次回会議には施策の完了、返品内訳、商品別粗利の差分を持ち寄ります。"]
SOURCE="架空データ：くらし便 2026年9月／前年同月比較"

def prepare(cid):
    folder=OUT/cid
    dump(folder/"input/data.json",EC)
    write(folder/"input/BRIEF.md","# くらし便 EC事業 9月報告\n\n読者：事業責任者・販売・商品・CS担当。6分の月次報告。\n目的：商品説明修正と粗利分析を先行し、広告増額は確認後に判断。\n組織、数値、担当者は架空のサンプル。\n")
    dump(folder/"roster.json",[{"title":t,"note":n} for t,n in zip(TITLES,NOTES)])
    write(folder/"NOTES.md","\n\n".join("## "+str(i)+". "+t+"\n\n"+n for i,(t,n) in enumerate(zip(TITLES,NOTES),1)))
    return folder

def language_and_notes(p,notes):
    """Post-generation Japanese font, language, fixed label and notes adjustments only."""
    from pptx import Presentation
    from pptx.oxml.ns import qn
    prs=Presentation(p)
    for i,slide in enumerate(prs.slides):
        slide.notes_slide.notes_text_frame.text=notes[i]
        for node in slide._element.iter(qn("a:t")):
            if node.text:node.text=node.text.replace("负责人：","担当：")
        for tag in ("a:rPr","a:defRPr","a:endParaRPr"):
            for pr in slide._element.iter(qn(tag)):
                pr.set("lang","ja-JP")
                for script in ("a:latin","a:ea"):
                    font=pr.find(qn(script))
                    if font is None:font=pr.makeelement(qn(script),{});pr.append(font)
                    font.set("typeface","Noto Sans JP")
        # Tables and chart text use the same Japanese family in the saved XML.
    prs.core_properties.language="ja-JP"
    prs.save(p)

async def build_mcp():
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    from pptx import Presentation
    from pptx.util import Inches
    cid="office-powerpoint-mcp";folder=prepare(cid);up=UP/CONFIG[cid].replace("/","__")
    # Only an empty wide page container is made locally; all slide content is authored by MCP tools.
    blank=Presentation();blank.slide_width=Inches(13.333);blank.slide_height=Inches(7.5);blank.save(folder/"input/empty-wide.pptx")
    log=[]
    params=StdioServerParameters(command=sys.executable,args=[str(up/"ppt_mcp_server.py"),"--transport","stdio"],cwd=str(up),env={**os.environ,"PYTHONIOENCODING":"utf-8"})
    with (folder/"server-stderr.log").open("w",encoding="utf-8") as err:
      async with stdio_client(params,errlog=err) as (r,w):
       async with ClientSession(r,w) as session:
        await session.initialize()
        inventory=await session.list_tools();dump(folder/"source/mcp-tools.json",inventory.model_dump(mode="json"))
        async def call(name,**kw):
            result=await session.call_tool(name,arguments=kw)
            obj=result.model_dump(mode="json");log.append(dict(tool=name,arguments=kw,result=obj))
            dump(folder/"source/mcp-calls.json",log)
            if result.isError:raise RuntimeError(str(obj))
            for block in result.content:
                if hasattr(block,"text"):
                    try:value=json.loads(block.text)
                    except json.JSONDecodeError:continue
                    if isinstance(value,dict) and value.get("error"):raise RuntimeError(value["error"])
            return obj
        pid="japanese-ec-report"
        await call("create_presentation_from_template",template_path=str(folder/"input/empty-wide.pptx"),id=pid)
        async def text(i,s,x,y,w,h,size=23,bold=False,color=None):
            return await call("manage_text",slide_index=i,operation="add",left=x,top=y,width=w,height=h,text=s,font_size=size,font_name="Noto Sans JP",bold=bold,color=color or [32,44,57],auto_fit=False,presentation_id=pid)
        for i,title in enumerate(TITLES):
            await call("add_slide",layout_index=6,presentation_id=pid)
            await text(i,title,.65,.4,12,1,31,True)
            await call("add_shape",slide_index=i,shape_type="rectangle",left=.7,top=1.42,width=11.9,height=.035,fill_color=[28,103,150],line_color=[28,103,150],presentation_id=pid)
            await text(i,"架空の組織・数値による制作サンプル",.7,6.98,10,.25,10)
            await text(i,str(i+1)+" / 6",11.7,6.98,.8,.25,10)
        await text(0,"売上は伸長。\n次月は商品説明と粗利分析を先行。",.85,2.2,11.6,2,36,True,[28,103,150])
        await text(0,"2026年9月／比較：2025年9月\n事業責任者・販売・商品・CSの月次会議",.85,4.7,11,1.2,23)
        await call("add_table",slide_index=1,rows=5,cols=4,left=.8,top=2,width=11.7,height=3.25,data=[["指標","当月","前年同月","変化"],["売上","1,200万円","1,000万円","+20%"],["注文","4,000件","3,500件","+500件"],["粗利率","36%","38%","−2ポイント"],["返品率","6%","4%","+2ポイント"]],header_font_size=21,body_font_size=20,header_bg_color=[28,103,150],presentation_id=pid)
        await text(1,"粗利額は432万円。売上だけで次の施策を判断しない。",.85,5.7,11.5,.9,22)
        await text(2,"青：2025年9月　赤：2026年9月",.9,1.63,11.3,.35,17)
        await call("add_chart",slide_index=2,chart_type="column",left=.8,top=2.05,width=11.7,height=4.15,categories=[c["name"] for c in EC["channels"]],series_names=["2025年9月","2026年9月"],series_values=[[c["previous_man_yen"] for c in EC["channels"]],[c["sales_man_yen"] for c in EC["channels"]]],has_legend=False,has_data_labels=False,y_axis_title="万円",presentation_id=pid)
        await text(2,"前年差：広告 +20／自然検索 +90／メール +50／直訪 +40万円",.9,6.45,11.4,.4,17)
        await text(3,"前年 380万円",.9,2,5.4,.8,34,True)
        await text(3,"1,000万円 × 38%",.9,3,5.4,.6,24)
        await text(3,"当月 432万円",7,2,5.4,.8,34,True,[28,103,150])
        await text(3,"1,200万円 × 36%",7,3,5.4,.6,24)
        await text(3,"粗利額は52万円増加。\n値引き・商品構成の影響は、商品別に確認する。",.95,4.6,11.5,1.35,25)
        await call("add_table",slide_index=4,rows=4,cols=3,left=.8,top=2,width=11.7,height=3.6,data=[["期限","担当","確認する作業"],["10/09","CS・森","上位20商品の返品理由を分類"],["10/16","商品・青木","返品上位5商品の説明を改稿"],["10/16","販売・山田","粗利率の差分を商品別に分析"]],header_font_size=20,body_font_size=18,header_bg_color=[28,103,150],presentation_id=pid)
        await text(5,"商品説明の修正と粗利分析を進める。",.9,2,11.5,1,32,True,[28,103,150])
        await text(5,"次回に確認するもの\n\n施策の完了／返品の内訳／商品別の粗利差分\n\n広告増額は、その結果を確認して判断する。",.95,3.35,11.4,2.8,25)
        await call("save_presentation",file_path=str(folder/"deck.pptx"),presentation_id=pid)
        await call("get_presentation_info",presentation_id=pid)
    language_and_notes(folder/"deck.pptx",NOTES)
    print("MCP stdio created six slides:",len(log),"tool calls")

def build_mck():
    cid="mck-design";folder=prepare(cid);up=UP/CONFIG[cid].replace("/","__")
    sys.path.insert(0,str(up))
    from mck_ppt.deck_builder import DeckBuilder
    from mck_ppt.constants import NAVY,ACCENT_BLUE
    story=[
     {"type":"cover","data":dict(title="くらし便\nEC事業 9月報告",subtitle="商品説明の修正と粗利分析を先行",author="架空の組織・数値によるサンプル",date="2026年9月／前年同月比較")},
     {"type":"two_stat","data":dict(title=TITLES[1],stats=[("1,200万円","売上：前年1,000万円",True),("36%","粗利率：前年38%",False)],detail_items=["売上は前年比20%増。粗利額は432万円。","返品率は4%から6%へ2ポイント上昇。"],source=SOURCE)},
     {"type":"grouped_bar","data":dict(title=TITLES[2],categories=[c["name"] for c in EC["channels"]],series=[("前年",NAVY),("当月",ACCENT_BLUE)],data=[[c["previous_man_yen"],c["sales_man_yen"]] for c in EC["channels"]],max_val=450,y_ticks=[0,100,200,300,400],summary=("単位：万円","自然検索 +90、メール +50、直訪 +40、広告 +20"),source=SOURCE)},
     {"type":"data_table","data":dict(title=TITLES[3],headers=["指標","前年同月","当月","差分"],rows=[["売上","1,000万円","1,200万円","+200万円"],["粗利率","38%","36%","−2ポイント"],["粗利額","380万円","432万円","+52万円"]],source=SOURCE,bottom_bar=("確認事項","値引き・商品構成は原因の仮説。商品別に確認する。"))},
     {"type":"action_items","data":dict(title=TITLES[4],actions=[("返品理由を分類","10/09","上位20商品を分類\n分類率100%を確認","CS・森"),("商品説明を修正","10/16","返品上位5商品を改稿\n対象商品の返品率を比較","商品・青木"),("粗利差分を分析","10/16","値引き・商品構成を分解\n率低下の要因を説明","販売・山田")],source=SOURCE)},
     {"type":"closing","data":dict(title=TITLES[5],message="次回：施策の完了、返品の内訳、商品別粗利\n広告増額は、確認後に判断する",source_text=SOURCE)}
    ]
    dump(folder/"source/storyline.json",story)
    outline={"brief":{"audience":EC["audience"],"goal":EC["decision"],"duration_minutes":6},"slides":[{"idx":i,"layout":r["type"],"title":r["data"].get("title",""),"key_point":NOTES[i-1]} for i,r in enumerate(story,1)]}
    dump(folder/"source/outline.json",outline)
    content={"slides":[{"idx":i,"layout":r["type"],**r["data"]} for i,r in enumerate(story,1)]}
    dump(folder/"source/content.json",content)
    env={**os.environ,"PYTHONPATH":str(up),"PYTHONIOENCODING":"utf-8"}
    s3=subprocess.run([sys.executable,str(up/"references/scripts/gate_check_s3.py"),str(folder/"source/content.json"),str(folder/"source")],env=env,capture_output=True,text=True,encoding="utf-8")
    write(folder/"source/gate-s3.log",s3.stdout+s3.stderr)
    if s3.returncode:raise RuntimeError("Mck S3 failed: "+s3.stdout)
    log=io.StringIO()
    with contextlib.redirect_stdout(log):DeckBuilder.build(story,str(folder/"deck.pptx"))
    write(folder/"source/build.log",log.getvalue())
    language_and_notes(folder/"deck.pptx",NOTES)
    s4=subprocess.run([sys.executable,str(up/"references/scripts/gate_check.py"),str(folder/"deck.pptx"),str(folder/"source")],env=env,capture_output=True,text=True,encoding="utf-8")
    write(folder/"source/gate-s4.log",s4.stdout+s4.stderr)
    print("Mck generated; S4 process:",s4.returncode)
    write(folder/"source/japanese-adjustments.md","# 日本語調整\n\n元DeckBuilder/MckEngineは無改変。生成後に文字runのlatin/eaをNoto Sans JP、langをja-JPへ設定し講稿を追加。固定語「负责人：」を「担当：」へ翻訳。形状と版式は元engineの出力を維持。\n原典の固定~/.workbuddyパスは当地の取得先をsys.pathへ指定する方法へ置換。references/layouts/は対象commitに存在せず、engine API/brand/guard/layout-matrix/experiencesを参照。\n")

def render(cid):
    p=subprocess.run(["pwsh","-NoProfile","-File",str(ROOT/"tools/render_powerpoint.ps1"),"-PresentationPath",str(OUT/cid/"deck.pptx"),"-OutputDirectory",str(OUT/cid/"render")],capture_output=True,text=True,encoding="utf-8",errors="replace")
    write(OUT/cid/"render/render-command.log",p.stdout+p.stderr)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    print(p.stdout.strip())

def finalize():
    records=[];guides=[]
    for cid,repo in CONFIG.items():
        folder=OUT/cid
        if not (folder/"deck.pptx").exists():continue
        up=UP/repo.replace("/","__");audit=json.loads(read(ROOT/".build/repository-audit"/repo.replace("/","__")/"record.json"))
        source_files=(["README.md","ppt_mcp_server.py","tools/presentation_tools.py","tools/content_tools.py","tools/structural_tools.py","utils/content_utils.py","requirements.txt"] if cid=="office-powerpoint-mcp" else ["SKILL.md","mck_ppt/deck_builder.py","mck_ppt/engine.py","mck_ppt/core.py","mck_ppt/constants.py","references/team/brand-guide.md","references/framework/engine-api.md","references/framework/guard-rails.md","references/layout-matrix.yaml","experiences/layout-pitfalls.md","references/scripts/gate_check_s3.py","references/scripts/gate_check.py"])
        refs=[dict(path=r,sha256=sha(up/r),url="https://github.com/"+repo+"/blob/"+audit["commit"]+"/"+r) for r in source_files]
        for name in ("LICENSE","NOTICE"):
            if (up/name).exists():shutil.copy2(up/name,folder/name)
        packages={p:importlib.metadata.version(p) for p in ["python-pptx","Pillow","lxml"]}
        if cid=="office-powerpoint-mcp":packages["mcp"]=importlib.metadata.version("mcp")
        dump(folder/"environment.json",dict(python=sys.version,platform=sys.platform,packages=packages,font="Noto Sans JP",external_api=False))
        mode="mcp_stdio" if cid=="office-powerpoint-mcp" else "python_engine"
        summary=("公式MCP stdioのcreate_presentation_from_template/add_slide/manage_text/add_table/add_chart/save_presentationを実行。表とネイティブチャートを含む日本語PPTX。" if cid=="office-powerpoint-mcp" else "公式DeckBuilderからMckEngineのcover/two_stat/grouped_bar/data_table/action_items/closingを実行した日本語月次報告。")
        prov=dict(repository=repo,upstream_commit=audit["commit"],execution_type=mode,method=summary,source_refs=refs,upstream_files=refs,input_sha256=sha(folder/"input/data.json"),artifact_sha256=sha(folder/"deck.pptx"),local_changes=["日本語の入力と講稿","生成後のNoto Sans JP・ja-JP指定", "公式manage_textで系列凡例を追加" if mode=="mcp_stdio" else "固定語の负责人を担当へ翻訳"],license=audit["github_license"],archived=audit["archived"],environment="environment.json",execution_log="source/mcp-calls.json" if mode=="mcp_stdio" else "source/build.log",render_report="render/powerpoint-render.json")
        dump(folder/"PROVENANCE.json",prov)
        script=Path(__file__)
        shutil.copy2(script,folder/"source/build_native_repository_examples.py")
        prompt="添付EC月次データを"+repo+"で6枚の日本語資料にしてください。売上増200万円と粗利率低下2ポイントを区別し、チャネル比較、粗利計算、担当と期限、次の判断を含めます。原典固有の制作入口を使用し、Noto Sans JPと講稿を設定。架空の数値と明記してください。"
        write(folder/"PROMPT.txt",prompt)
        flag="mcp" if mode=="mcp_stdio" else "mck"
        target=".build/actual-upstreams/"+repo.replace("/","__")
        commands=["git clone https://github.com/"+repo+" "+target,"git -C "+target+" checkout "+audit["commit"],"python -m venv .venv",r".venv\Scripts\python -m pip install "+('"mcp[cli]==1.30.0" python-pptx Pillow fonttools' if mode=="mcp_stdio" else "python-pptx lxml Pillow"),r".venv\Scripts\python tools/build_native_repository_examples.py --only "+flag+" --render"]
        requirements=["Python 3.13（実測）","PowerShell 7 / pwsh（描画スクリプト）","Noto Sans JP","Microsoft PowerPoint 16.0（PNG/PDF描画用）"]
        limitation="MCP 2.3ではFastMCP importが削除されるため1.30.0で実行。リポはarchived。原典format_chartはlegend_positionを反映しないため、has_legend=Falseと公式manage_textによる系列表示で重なりを回避。" if mode=="mcp_stdio" else "上流references/layouts/は取得commitに存在しない。元engine/API参照で制作。画像生成APIは不使用。生成された固定語『负责人』を『担当』へ翻訳。"
        guide=dict(repository=repo,execution_type=mode,summary_ja=summary,requirements=requirements,steps=["原典を取得しcommitを固定","個別環境へ依存を導入","入力と日本語依頼を用意","原典の入口から制作","PowerPoint本体で日本語の表示を確認"],commands=commands,source_refs=refs,license=audit["github_license"],example_ids=[cid],limitations=[limitation],reproduction="examples/repositories/"+cid+"/README.md")
        guides.append(guide)
        write(folder/"index.html",'''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>日本語実行例</title><style>html,body{margin:0;background:#161b22;color:white;height:100%;font:16px sans-serif}main{height:calc(100% - 48px);display:flex;align-items:center;justify-content:center}img{max-width:100%;max-height:100%;object-fit:contain}nav{text-align:center;height:40px}button{padding:6px 18px;margin:4px}a{color:#b4dfff}</style><main><img id="page" alt="スライド"></main><nav><button id="prev">前へ</button><span id="count"></span><button id="next">次へ</button><a href="deck.pptx">PPTX</a> <a href="render/deck.pdf">PDF</a></nav><script>let current=0;function show(i){current=Math.max(0,Math.min(5,i));document.getElementById('page').src='render/slide-'+String(current+1).padStart(2,'0')+'.png';document.getElementById('count').textContent=(current+1)+' / 6';if(parent!==window)parent.postMessage({type:'yebisu-page',index:current},location.origin)}document.getElementById('prev').onclick=()=>show(current-1);document.getElementById('next').onclick=()=>show(current+1);document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')show(current+1);if(e.key==='ArrowLeft')show(current-1)});window.addEventListener('message',e=>{if(e.source===parent&&e.origin===location.origin&&e.data?.type==='yebisu-slide'&&Number.isInteger(e.data.index))show(e.data.index)});show(0);</script></html>''')
        write(folder/"README.md","# "+repo+" の日本語実行例\n\n"+summary+"\n\n組織・数値は架空。入力はinput/data.json、依頼文はPROMPT.txt、講稿はNOTES.md。deck.pptxは編集可能、render/deck.pdfは閲覧用。\n\n## 環境と導入\n\n"+"\n".join("- "+x for x in requirements)+"\n\n"+limitation+"\n\n## 再現\n\nカタログ全体のrootで、対応原典を .build/actual-upstreams/"+repo.replace("/","__")+" に置き、上記commitへ固定します。次のコマンドのPythonは依存を導入した環境を使います。\n\n    "+commands[-1]+"\n\n一般の利用者は上流README/SKILLを使用してください。MCPは python upstream/ppt_mcp_server.py --transport stdio をクライアントから起動し、source/mcp-calls.jsonの操作・引数を参考に実行。MckはupstreamをPython import pathへ追加しsource/build_native_repository_examples.py内のbuild_mck()と同じstoryをDeckBuilder.buildへ渡します。source/storyline.jsonは保存用で、再読込する場合はseries内のRGB配列をpptx.dml.color.RGBColorへ戻します。当地スクリプトはこの2作例専用で、汎用生成サービスではありません。\n\n## 出典・確認\n\nPROVENANCE.jsonに固定commit、実ファイルhash、適用ファイル、environment.jsonに依存。QA.jsonとrender/powerpoint-render.jsonに検証範囲。LICENSE"+("とNOTICE" if (folder/"NOTICE").exists() else "")+"を保持。原作者の公式日本語版ではありません。\n")
        ns={"p":"http://schemas.openxmlformats.org/presentationml/2006/main","a":"http://schemas.openxmlformats.org/drawingml/2006/main"}
        with zipfile.ZipFile(folder/"deck.pptx") as z:
            slides=[n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            metrics=dict(slides=len(slides),native_shapes=sum(len(ET.fromstring(z.read(n)).findall(".//p:sp",ns)) for n in slides),text_runs=sum(len(ET.fromstring(z.read(n)).findall(".//a:t",ns)) for n in slides),charts=len([n for n in z.namelist() if n.startswith("ppt/charts/chart") and n.endswith(".xml")]),notes=len([n for n in z.namelist() if n.startswith("ppt/notesSlides/notesSlide") and n.endswith(".xml")]))
        existing=json.loads(read(folder/"QA.json")) if (folder/"QA.json").exists() else {}
        existing.update(structure=metrics,artifact_sha256=sha(folder/"deck.pptx"),powerpoint_render="render/powerpoint-render.json")
        existing.setdefault("status","pending_visual_review")
        dump(folder/"QA.json",existing)
        p="examples/repositories/"+cid+"/"
        records.append(dict(id=cid,title="くらし便 EC事業 9月報告",use_case="月次報告",repository=repo,skill_repository=repo,upstream_commit=audit["commit"],fork_id=None,page_count=6,format="pptx",preview_kind="powerpoint-render",style="MCP native chart/table" if mode=="mcp_stdio" else "Mck consulting layouts",cover=p+"render/slide-01.png",interior=p+"render/slide-03.png",preview=p+"index.html",artifact_download=p+"deck.pptx",source_download=p+"source/build_native_repository_examples.py",input=p+"input/BRIEF.md",input_data=p+"input/data.json",prompt=p+"PROMPT.txt",prompt_text=prompt,provenance=p+"PROVENANCE.json",qa=p+"QA.json",guide=p+"README.md",titles=TITLES,notes=NOTES,method=summary,sample_notice="組織・数値は架空の制作サンプルです。",pages=[p+"render/slide-%02d.png"%i for i in range(1,7)],pdf_download=p+"render/deck.pdf"))
    dump(ROOT/"data/native-repository-examples.json",records);dump(ROOT/"data/native-repository-guides.json",guides)

def main():
    p=argparse.ArgumentParser();p.add_argument("--only",choices=["mcp","mck","both"],default="both");p.add_argument("--render",action="store_true");p.add_argument("--finalize-only",action="store_true");args=p.parse_args()
    if not args.finalize_only:
        if args.only in ("mcp","both"):
            asyncio.run(build_mcp())
            if args.render:render("office-powerpoint-mcp")
        if args.only in ("mck","both"):
            build_mck()
            if args.render:render("mck-design")
    finalize()
if __name__=="__main__":main()

