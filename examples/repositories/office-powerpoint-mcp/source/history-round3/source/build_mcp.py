"""Create this six-page example through the pinned original PowerPoint MCP stdio server."""
from pathlib import Path
import argparse,asyncio,contextlib,hashlib,importlib.metadata,io,json,os,shutil,subprocess,sys,xml.etree.ElementTree as ET,zipfile
CASE=Path(__file__).resolve().parents[1]
ROOT=CASE
OUT=CASE.parent
UP=CASE/"source"
CONFIG={"office-powerpoint-mcp":"GongRzhe/Office-PowerPoint-MCP-Server"}
def read(p):return Path(p).read_text(encoding="utf-8-sig")
def write(p,s):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(s,encoding="utf-8")
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+"\n")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
EC=json.loads(read(CASE/"input/data.json"))
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
    from pptx.enum.chart import XL_LEGEND_POSITION
    from pptx.enum.dml import MSO_PATTERN
    from pptx.dml.color import RGBColor
    from pptx.util import Pt
    from pptx.enum.text import MSO_ANCHOR
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
                    font.set("typeface","BIZ UDPGothic")
        # Tables and chart text use the same Japanese family in the saved XML.
    # Explicit compatibility adapter: MCP add_chart ignores legend_position and does
    # not expose series pattern fills. Preserve native data while adding a non-color cue.
    chart=next(x.chart for x in prs.slides[2].shapes if x.has_chart)
    chart.has_legend=True;chart.legend.position=XL_LEGEND_POSITION.BOTTOM;chart.legend.include_in_layout=False;chart.legend.font.name='BIZ UDPGothic';chart.legend.font.size=Pt(16)
    chart.series[0].format.fill.patterned();chart.series[0].format.fill.pattern=MSO_PATTERN.DARK_DOWNWARD_DIAGONAL
    chart.series[0].format.fill.fore_color.rgb=RGBColor.from_string('215D85');chart.series[0].format.fill.back_color.rgb=RGBColor.from_string('FFFFFF')
    chart.series[1].format.fill.solid();chart.series[1].format.fill.fore_color.rgb=RGBColor.from_string('128278')
    plot=chart.plots[0];plot.has_data_labels=True;plot.data_labels.font.size=Pt(13);plot.data_labels.font.name='BIZ UDPGothic'
    chart.category_axis.tick_labels.font.name='BIZ UDPGothic';chart.category_axis.tick_labels.font.size=Pt(16)
    chart.value_axis.tick_labels.font.name='BIZ UDPGothic';chart.value_axis.tick_labels.font.size=Pt(14)
    # Original format_table_cell accepts vertical_alignment but drops it when
    # calling its formatter. Apply only that missing native cell property here.
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:cell.vertical_anchor=MSO_ANCHOR.MIDDLE
    delta=next(x.chart for x in prs.slides[3].shapes if x.has_chart)
    delta.has_title=False;delta.has_legend=False;delta.plots[0].gap_width=60;delta.plots[0].has_data_labels=True;delta.plots[0].data_labels.font.name='BIZ UDPGothic';delta.plots[0].data_labels.font.size=Pt(12)
    delta.category_axis.tick_labels.font.name='BIZ UDPGothic';delta.category_axis.tick_labels.font.size=Pt(12)
    delta.value_axis.tick_labels.font.name='BIZ UDPGothic';delta.value_axis.tick_labels.font.size=Pt(11)
    delta.series[0].format.fill.solid();delta.series[0].format.fill.fore_color.rgb=RGBColor.from_string('128278')
    # The original format_runs adds an empty first paragraph. Remove only that
    # empty paragraph before the narrow bottom note can run below the page.
    for index in (4,6,8):
        frame=prs.slides[3].shapes[index].text_frame
        if len(frame.paragraphs)>1 and not frame.paragraphs[0].text:
            empty=frame.paragraphs[0]._p;empty.getparent().remove(empty)
    # Native template coordinates target a10-inch page. Scale x/width to the wide container.
    for shape in prs.slides[3].shapes:shape.left=int(shape.left*13.333/10);shape.width=int(shape.width*13.333/10)
    prs.core_properties.language="ja-JP"
    # python-pptx chart Font.name writes latin only; add explicit Japanese script
    # families to the existing chart text properties to avoid MS Gothic fallback.
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_chart:continue
            for tag in ('a:rPr','a:defRPr','a:endParaRPr'):
                for pr in shape.chart._chartSpace.iter(qn(tag)):
                    pr.set('lang','ja-JP')
                    for script in ('a:latin','a:ea'):
                        node=pr.find(qn(script))
                        if node is None:node=pr.makeelement(qn(script),{});pr.append(node)
                        node.set('typeface','BIZ UDPGothic')
    prs.save(p)

async def build_mcp():
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    from pptx import Presentation
    from pptx.util import Inches
    cid="office-powerpoint-mcp";folder=prepare(cid);up=CASE/"source/upstream"
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
            return await call("manage_text",slide_index=i,operation="add",left=x,top=y,width=w,height=h,text=s,font_size=size,font_name="BIZ UDPGothic",bold=bold,color=color or [32,44,57],auto_fit=False,presentation_id=pid)
        await call("list_slide_templates")
        await call("get_template_info",template_id="before_after_comparison")
        for i,title in enumerate(TITLES):
            await call("add_slide",layout_index=6,presentation_id=pid)
            if i==3:continue # this page is authored by the actual original template API
            await text(i,title,.65,.4,12,1,31,True)
            await call("add_shape",slide_index=i,shape_type="rectangle",left=.7,top=1.42,width=11.9,height=.035,fill_color=[28,103,150],line_color=[28,103,150],presentation_id=pid)
            await text(i,"架空の組織・数値による制作サンプル",.7,6.98,10,.35,13)
            await text(i,str(i+1)+" / 6",11.7,6.98,.8,.35,13)
        await text(0,"売上は伸長。\n次月は商品説明と粗利分析を先行。",.85,2.2,11.6,2,36,True,[28,103,150])
        await text(0,"2026年9月／比較：2025年9月\n事業責任者・販売・商品・CSの月次会議",.85,4.7,11,1.2,23)
        await call("add_table",slide_index=1,rows=5,cols=4,left=.8,top=2,width=11.7,height=3.25,data=[["指標","当月","前年同月","変化"],["売上","1,200万円","1,000万円","+20%"],["注文","4,000件","3,500件","+500件"],["粗利率","36%","38%","−2ポイント"],["返品率","6%","4%","+2ポイント"]],header_font_size=21,body_font_size=20,header_bg_color=[28,103,150],presentation_id=pid)
        await text(1,"粗利額は432万円。売上だけで次の施策を判断しない。",.85,5.7,11.5,.9,22)
        await text(2,"斜線：2025年9月　塗り：2026年9月",.9,1.63,11.3,.35,17)
        await call("add_chart",slide_index=2,chart_type="column",left=.8,top=2.05,width=11.7,height=4.15,categories=[c["name"] for c in EC["channels"]],series_names=["2025年9月","2026年9月"],series_values=[[c["previous_man_yen"] for c in EC["channels"]],[c["sales_man_yen"] for c in EC["channels"]]],has_legend=True,legend_position="bottom",has_data_labels=True,y_axis_title="万円",presentation_id=pid)
        await text(2,"前年差：広告 +20／自然検索 +90／メール +50／直訪 +40万円",.9,6.45,11.4,.4,17)
        await call("apply_slide_template",slide_index=3,template_id="before_after_comparison",color_scheme="modern_blue",content_mapping={"title":TITLES[3],"vs_text":"比較","left_header":"2025年9月（架空）","right_header":"2026年9月（架空）","content_left":"売上 1,000万円\n粗利率 38%\n粗利額 380万円","content_right":"売上 1,200万円\n粗利率 36%\n粗利額 432万円","improvement_text":"額+52万円／率−2ポイント"},presentation_id=pid)
        # The template's English wrapping collapses Japanese newlines. Restore the
        # three native paragraphs through its own formatted-run MCP operation.
        for shape,values in [(4,["売上 1,000万円","粗利率 38%","粗利額 380万円"]),(6,["売上 1,200万円","粗利率 36%","粗利額 432万円"])]:
            await call("manage_text",slide_index=3,operation="format_runs",shape_index=shape,text_runs=[{"text":v,"font_name":"BIZ UDPGothic","font_size":30,"bold":True,"color":[32,44,57]} for v in values],presentation_id=pid)
        await call("manage_text",slide_index=3,operation="format_runs",shape_index=8,text_runs=[{"text":"額+52万円／率−2ポイント","font_name":"BIZ UDPGothic","font_size":21,"italic":False,"bold":True,"color":[28,74,103]}],presentation_id=pid)
        await text(3,"前年差（万円）",.7,4.15,8.6,.3,15,True)
        await call("add_chart",slide_index=3,chart_type="bar",left=.7,top=4.5,width=8.6,height=1.45,categories=["売上差","粗利額差"],series_names=["当月−前年（万円）"],series_values=[[200,52]],has_legend=False,has_data_labels=True,presentation_id=pid)
        await call("add_table",slide_index=4,rows=4,cols=3,left=.8,top=2,width=11.7,height=3.6,data=[["期限","担当","確認する作業"],["10/09","CS・森","上位20商品の返品理由を分類"],["10/16","商品・青木","返品上位5商品の説明を改稿"],["10/16","販売・山田","粗利率の差分を商品別に分析"]],header_font_size=20,body_font_size=18,header_bg_color=[28,103,150],presentation_id=pid)
        await text(5,"商品説明の修正と粗利分析を進める。",.9,2,11.5,1,32,True,[28,103,150])
        await text(5,"次回に確認するもの\n\n施策の完了／返品の内訳／商品別の粗利差分\n\n広告増額は、その結果を確認して判断する。",.95,3.35,11.4,2.8,25)
        # The table format tool aligns each actual cell; no XML/table redraw.
        for slide_index,rows,cols in [(1,5,4),(4,4,3)]:
            for row in range(rows):
                for col in range(cols):await call("format_table_cell",slide_index=slide_index,shape_index=4,row=row,col=col,vertical_alignment="middle",font_name="BIZ UDPGothic",presentation_id=pid)
        for index in range(6):await call("manage_text",slide_index=index,operation="validate",shape_index=0,validation_only=True,font_size=31,presentation_id=pid)
        await call("save_presentation",file_path=str(folder/"deck.pptx"),presentation_id=pid)
        await call("get_presentation_info",presentation_id=pid)
    language_and_notes(folder/"deck.pptx",NOTES)
    print("MCP stdio created six slides:",len(log),"tool calls")


if __name__=="__main__":asyncio.run(build_mcp())
