"""Japanese teaching example using the pinned, unmodified slides_maker deckkit."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, re
ROOT=Path(__file__).resolve().parents[1]
COMMIT='3767cc346d63ef1646082c87f15fbf0be582b152'
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def linear_search(values,target):
    visited=[]
    for index,value in enumerate(values):
        visited.append(value)
        if value==target:return {'index':index,'visited':visited,'comparisons':len(visited)}
    return {'index':-1,'visited':visited,'comparisons':len(visited)}
def binary_search(values,target):
    lo,hi=0,len(values)-1;visited=[];steps=[]
    while lo<=hi:
        mid=(lo+hi)//2;value=values[mid];visited.append(value)
        steps.append({'low':values[lo],'high':values[hi],'mid':value})
        if value==target:return {'index':mid,'visited':visited,'comparisons':len(visited),'steps':steps}
        if value<target:lo=mid+1
        else:hi=mid-1
    return {'index':-1,'visited':visited,'comparisons':len(visited),'steps':steps}
TITLES=['昇順なら、中央から範囲を絞れる','線形探索は、先頭から13回比較する','二分探索は、大小で残す側を決める','二分探索は、15通りとも4回以内','比較回数から、秒数は決められない']
NOTES=[
'初めて探索を学ぶ人への短い教材です。同じ昇順の配列から、実際にPythonで13を探しました。ここで数える1回は、調べる要素を1つ選んで目的値と比べることです。CPU命令数や秒数ではありません。',
'線形探索では先頭から順に値を確認します。目的値が13なら1から13まで調べます。この方法は、データが未整列でも使えます。今回は両方式で同じ配列を使って条件をそろえました。',
'二分探索は昇順という前提を利用します。8より大きいので9〜15、12より大きいので13〜15、14より小さいので13だけを残し、次に13を調べて終了します。中央は添字の小さい側へ切り捨てています。',
'1から15の全てを目的値にして実行しました。線形探索は先頭の1なら1回、末尾の15なら15回。二分探索は8なら1回で、最多でも4回でした。存在する値だけを探す15通りの比較であり、未発見時や大規模データの計測は含めていません。',
'二分探索の前に整列が必要です。今回の実行では初めから昇順の配列を与えたため、並べ替えの手間は計測していません。途中で並びを変えれば前提が崩れます。配列の中央を直接参照できる条件での教材であり、検索回数の減少をそのまま何倍速いと読み替えないでください。']
def build(out,up):
    scripts=up/'skills/slide-maker/scripts';sys.path.insert(0,str(scripts))
    import deckkit as dk
    from pptx.dml.color import RGBColor
    from pptx.util import Pt
    from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
    dk.FONT=dk.EAFONT='Yu Gothic';dk.MONO='Consolas'
    ink=RGBColor.from_string('132C3B');blue=RGBColor.from_string('116B8A');orange=RGBColor.from_string('A8471C');muted=RGBColor.from_string('4E626C');purple=RGBColor.from_string('7044A0');white=RGBColor(255,255,255)
    dk.DEEP=ink
    values=list(range(1,16));traces=[{'target':t,'linear':linear_search(values,t),'binary':binary_search(values,t)} for t in values]
    data={'title':TITLES[0],'titles':TITLES,'notes':NOTES,'array':values,'unit':'訪問した要素数（目的値と照合した回数）','timing_measured':False,'sorting_cost_measured':False,'traces':traces}
    assert traces[12]['linear']['comparisons']==13 and traces[12]['binary']['visited']==[8,12,14,13]
    assert max(t['binary']['comparisons'] for t in traces)==4
    dump(out/'input/data.json',data)
    prs=dk.blank_deck(13.333,7.5)
    def txt(s,x,y,w,h,t,size=24,c=ink,bold=False,center=False):
        size=13 if size<=13 else 16 if size<=18 else 24 if size<=30 else 32 if size<=32 else 34
        # Japanese uses tight CJK/Latin boundaries consistently; arrows retain their own spacing.
        t=re.sub(r'(?<=[\u3040-\u30ff\u3400-\u9fff]) +(?=[A-Za-z0-9])|(?<=[A-Za-z0-9]) +(?=[\u3040-\u30ff\u3400-\u9fff])','',t)
        return dk.text(s,x,y,w,h,[[(t,size,c,bold,False,dk.FONT)]],align=PP_ALIGN.CENTER if center else PP_ALIGN.LEFT,anchor=MSO_ANCHOR.MIDDLE,space_after=0)
    def start(i):
        s=dk.add_slide(prs);dk.a11y_title(s,TITLES[i],ea=dk.EAFONT);dk.title_bar(s,TITLES[i],accent=muted,title_c=ink)
        # Keep the original title component, removing only its optional decorative rule.
        rule=s.shapes[-1];rule._element.getparent().remove(rule._element)
        dk.footer(s,page=i+1)
        # Local type-token adapter; original deckkit remains unchanged.
        for shape in s.shapes:
            if shape.has_text_frame and shape.text==TITLES[i]:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:run.font.size=Pt(34)
            elif shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size and run.font.size.pt<13:run.font.size=Pt(13)
        txt(s,.55,7.0,11.4,.35,'条件：昇順の配列1〜15／比較回数＝訪問した要素数',13,muted)
        s.notes_slide.notes_text_frame.text=NOTES[i]
        return s
    def row(s,y,active,hit=None):
        for j,v in enumerate(values):
            fill='116B8A' if v in active else 'E8EEF0'
            if v==hit:fill='A8471C'
            sh=dk.box(s,.55+j*.805,y,.71,.65,fill=fill)
            sh._element.nvSpPr.cNvPr.set('descr',f'値 {v}'+('：確認する値' if v in active else '：対象外'))
            txt(s,.55+j*.805,y,.71,.65,str(v),20,white if v in active or v==hit else muted,True,True)
    s=start(0)
    txt(s,.55,1.65,11.7,.55,'15個の数字から「13」を見つける。',30,bold=True)
    txt(s,.55,2.16,11.9,.45,'目標：次に調べる値を、自分で選べる。',24)
    row(s,2.85,[],13)
    txt(s,.55,3.57,12.1,.32,'1回＝値を一つ選び、目的値と比べること。秒数は数えない。',16,muted)
    txt(s,.7,4.05,5.3,.5,'線形探索：先頭から',25,blue,True)
    txt(s,7,4.05,5.4,.5,'二分探索：中央から',25,purple,True)
    txt(s,.7,4.8,5.3,.8,'13回',34,blue,True)
    txt(s,7,4.8,5.3,.8,'4回',34,purple,True)
    txt(s,.7,6.1,11.9,.4,'昇順の15個なら、二分探索は最悪でも4回。',22)
    s=start(1);row(s,2.35,list(range(1,14)),13)
    txt(s,.55,1.65,11.8,.45,'線形探索：見つかるまで、左から順に照合',26,blue,True)
    txt(s,.55,3.1,11.8,.4,'青：照合済み　茶：発見　灰：調べていない',16,muted)
    txt(s,.55,3.8,8.4,.65,'1 → 2 → 3 → … → 12 → 13',34,ink,True)
    txt(s,.55,5.1,8.7,.8,'先頭から13個と比べて、13を見つけた。',25)
    txt(s,10.1,3.8,2.4,.65,'13回',34,blue,True,True);txt(s,10.1,4.55,2.4,.5,'比較した回数',23,ink,True,True)
    s=start(2)
    for k,step in enumerate(traces[12]['binary']['steps']):
        y=1.65+k*1.08
        txt(s,.55,y,.7,.5,str(k+1),24,purple,True)
        txt(s,1.2,y,2.35,.5,f"範囲 {step['low']}〜{step['high']}",21)
        decision=['13 > 8 → 右半分','13 > 12 → 右半分','13 < 14 → 左半分','13 = 13 → 発見'][k]
        txt(s,.55,y+.53,3.05,.46,decision,24,purple if k<3 else orange,True)
        for j,v in enumerate(values):
            x=3.65+j*.58;active=step['low']<=v<=step['high'];mid=v==step['mid'];fill=('A8471C' if v==13 else '7044A0') if mid else ('E6DDF0' if active else 'FFFFFF')
            sh=dk.box(s,x,y,.51,.52,fill=fill,line='A8471C' if v==13 else ('DCE2E5' if not active else None),line_w=1.5 if v==13 else .5);sh._element.nvSpPr.cNvPr.set('descr',f'第{k+1}回 値{v}'+(' 中央で照合' if mid else ''))
            if active:txt(s,x,y,.51,.52,str(v),24,white if mid else ink,True,True)
    txt(s,.55,6.0,12.1,.45,'昇順なら、中央より小さい値は左、大きい値は右。',24,bold=True)
    txt(s,.55,6.48,12.1,.38,'紫：中央　茶枠：目的値13　茶塗り：発見　空枠：除外した位置',16,muted)
    s=start(3)
    txt(s,.55,1.53,11.9,.5,'目的値を1〜15に変えて、全15通りを実行',25,bold=True)
    chart=dk.native_chart(s,.55,2.14,8.8,3.65,[str(v) for v in values],[('線形探索',[t['linear']['comparisons'] for t in traces]),('二分探索',[t['binary']['comparisons'] for t in traces])],kind='line_markers',palette=[blue,purple],font=dk.FONT,smooth=False,value_fmt='0')
    chart.font.size=Pt(16);chart.legend.font.size=Pt(16)
    chart.category_axis.tick_labels.font.size=Pt(16);chart.value_axis.tick_labels.font.size=Pt(16)
    chart.value_axis.minimum_scale=0;chart.value_axis.maximum_scale=16;chart.value_axis.major_unit=4
    for axis,label in [(chart.value_axis,'比較回数（回）'),(chart.category_axis,'探す値')]:
        axis.has_title=True;axis.axis_title.text_frame.text=label
        for paragraph in axis.axis_title.text_frame.paragraphs:
            for run in paragraph.runs:run.font.name=dk.FONT;run.font.size=Pt(16)
    chart.legend.include_in_layout=True
    txt(s,10.15,2.6,2.6,.5,'二分探索の最大',24,purple,True);txt(s,10.15,3.2,2.6,.65,'4回',32,purple,True);txt(s,10.15,4.1,2.6,1.15,'線形探索は\n最大15回',24,blue)
    txt(s,.55,6.15,12.1,.55,'目的値1〜3は線形の方が少ない。比べるのは最大回数。',24,bold=True)
    s.notes_slide.notes_text_frame.text+='\n実行結果：input/data.json。配列内に存在する値だけの比較。目的値1では線形1回に対し二分4回であり、個々の値で常に二分が少ないとは限らない。'
    s=start(4)
    txt(s,.55,1.65,12.1,.65,'昇順の配列1〜15で、比較回数だけを数えた。',24)
    txt(s,.55,2.85,5.65,.55,'二分探索の比較回数',24,purple,True)
    dk.box(s,.55,3.55,5.65,1.0,fill='7044A0')
    txt(s,.55,3.55,5.65,1.0,'最大4回',32,white,True,True)
    txt(s,.55,4.8,5.65,.75,'全15通りを実行して確認',24)
    txt(s,7.0,2.85,5.65,.55,'実際にかかる秒数',24,ink,True)
    dk.box(s,7.0,3.55,5.65,1.0,fill='FFFFFF',line='4E626C',line_w=1.5)
    txt(s,7.0,3.55,5.65,1.0,'未計測',32,ink,True,True)
    txt(s,7.0,4.8,5.65,.75,'並べ替えの手間も含めて測る',24)
    txt(s,.55,6.0,12.1,.65,'回数の比から「何倍速い」とは言えない。',24,ink,True)
    dk.lint_layout(prs,strict=True)
    out.mkdir(parents=True,exist_ok=True);dk.declare_delivery(out,'selfread',builds='static');prs.core_properties.language='ja-JP';prs.save(out/'deck.pptx')
    gatefile=out/'.deck-gates.json'
    if gatefile.exists():
        gates=json.loads(gatefile.read_text(encoding='utf-8'));gates.setdefault('design_plan',{})['type_scale']={'display': 34, 'title': 32, 'body': 24, 'diagram': 24, 'footnote': 13};gates['design_plan']['type_scale_roles']='Display34=visible slide heading; title32=secondary callouts; body24=main text; diagram24=active array/range labels; footnote13=conditions and native chart axes/legend.';dump(gatefile,gates)
    dump(out/'roster.json',[{'title':t,'note':n} for t,n in zip(TITLES,NOTES)])
    (out/'NOTES.md').write_text('\n\n'.join(f'## {i+1}. {t}\n\n{n}' for i,(t,n) in enumerate(zip(TITLES,NOTES))),encoding='utf-8')
    print(json.dumps({'slides':len(prs.slides),'target13':traces[12],'output':str(out/'deck.pptx')},ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=ROOT);ap.add_argument('--upstream-dir',type=Path,default=ROOT/'source/upstream');a=ap.parse_args();build(a.output_dir.resolve(),a.upstream_dir.resolve())
