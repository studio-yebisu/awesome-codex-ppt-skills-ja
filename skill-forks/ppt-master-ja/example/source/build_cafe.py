"""Editable Japanese business examples through the unmodified PPT Master compiler."""
from pathlib import Path
import html, json, subprocess, sys, os

CASE=Path(__file__).resolve().parents[1]
ROOT=CASE.parents[2]
FORK=Path(os.environ.get('PPT_MASTER_PATH',str(CASE/'source/upstream')))
if not FORK.is_dir():FORK=ROOT/'skill-forks/ppt-master-ja'
PYTHON=Path(sys.executable)
INPUTS={'cafe':json.loads((CASE/'input/data.json').read_text(encoding='utf-8'))}
def text(x, y, size, value, color="#202C29", weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(str(value))}</text>'

def rect(x, y, w, h, color):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'

def group(name, bounds, body):
    return f'<g id="{name}" data-pptx-bounds="{bounds}">{body}</g>'

def lines(x, y, values, size=26, gap=49, color="#202C29", weight=400):
    return "".join(text(x, y+i*gap, size, value, color, weight) for i,value in enumerate(values))

def page(title, body, n, total, label, accent="#21654C", role="content"):
    header=group("heading","64 48 1150 112",text(64,71,16,label,accent,700)+text(64,135,42,title,weight=700))
    footer=group("footer","64 659 1150 28",text(64,679,14,"架空の組織・数値による制作サンプル / STUDIO YEBISU","#53675E")+text(1115,679,16,f"{n:02d} / {total:02d}","#53675E"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" lang="ja" font-family="BIZ UDPGothic" data-pptx-page-role="{role}"><rect id="background" data-pptx-role="background" width="1280" height="720" fill="#F7F5EE"/>{header}{body}{footer}</svg>'

def body(content):
    return group("content","64 190 1150 450",content)

def columns(items, accent="#21654C"):
    out=""
    for i,(head,copy) in enumerate(items):
        x=64+i*390
        out+=rect(x,205,342,3,accent)+text(x,258,30,head,accent,700)+lines(x,319,copy,size=23,gap=45)
    return body(out)

def comparison_table(d):
    out=rect(64,255,1150,48,'#21654C')+text(82,287,23,'比較項目・重み','#FFFFFF',700)+text(655,287,23,'A 駅前','#FFFFFF',700)+text(943,287,23,'B 運河沿い','#FFFFFF',700)
    for i,(label,weight) in enumerate(zip(d['criteria'],d['weights'])):
        y=303+i*48;sa,sb=[v['scores'][i] for v in d['sites']]
        out+=rect(64,y,1150,48,'#E5EEE7' if sb>sa else '#EDF0EC' if sa>sb else '#F7F5EE')
        out+=text(82,y+32,22,f'{label} {weight}%')
        out+=text(655,y+32,24,f'{sa} / 5','#202C29',700 if sa>sb else 400)+text(943,y+32,24,f'{sb} / 5','#21654C',700 if sb>sa else 400)
        out+=rect(64,y+47,1150,1,'#CAD5CC')
    return body(text(64,222,20,'5点満点 × 重み。仮置き評価のため現地調査で更新。','#53675E')+out+text(655,594,25,'81点 / 賃料28万円',weight=700)+text(943,594,25,'82点 / 賃料18万円','#21654C',700))

def audience_relation():
    out=''
    for x,title,copy in [(64,'平日の近隣客','仕事の合間の滞在'),(654,'週末の来訪者','散歩・買い物の途中')]:
        out+=rect(x,217,550,90,'#E5EEE7')+text(x+22,253,27,title,'#21654C',700)+text(x+22,286,21,copy)
        out+=text(x+240,346,33,'↓','#21654C',700)
    out+=rect(64,367,1150,109,'#21654C')+text(88,412,29,'新店：落ち着いて滞在する場所','#FFFFFF',700)+text(88,450,22,'32席の計画。利用場面を調査して確かめる。','#FFFFFF')
    out+=text(64,531,25,'既存店：24席の日常使い',weight=700)+text(64,574,22,'新店との役割が重なるだけにならないか、来店理由を聞く。')
    return body(out)

def operating_relation():
    out=text(64,218,21,'運営体制の提案。仕込みの量・移送時間・繁忙時の負荷は未確認。','#53675E')
    out+=rect(64,254,430,166,'#E5EEE7')+text(88,294,30,'既存店：24席','#21654C',700)
    out+=lines(88,338,['日常使いの営業を維持','仕込みの一部を支える'],size=24,gap=43)
    out+=rect(784,254,430,166,'#E5EEE7')+text(808,294,30,'新店：32席','#21654C',700)
    out+=lines(808,338,['落ち着いて滞在する店舗','店長候補の配置を先行'],size=24,gap=43)
    out+=text(540,302,22,'一部の仕込み','#21654C',700)+rect(516,333,239,3,'#21654C')+text(738,347,34,'→','#21654C',700)
    out+=text(522,390,19,'支援できる量を調べる','#53675E')
    out+=rect(277,420,3,46,'#21654C')+rect(997,420,3,46,'#21654C')
    out+=rect(64,466,1150,109,'#21654C')+text(88,503,27,'両店でそろえるもの','#FFFFFF',700)
    out+=text(88,546,25,'材料の購買　／　品質基準　／　日報','#FFFFFF')
    out+=text(64,613,22,'共通化の前に、既存店の営業を圧迫しないことを確かめる。','#53675E')
    return body(out)

def risk_confirmation_table():
    out=text(64,216,21,'検証前の確認表。仮定が崩れた場合は計画を修正する。','#53675E')
    out+=rect(64,245,1150,52,'#21654C')
    for x,label in [(82,'リスク'),(390,'確認すること'),(842,'次の判断に出す材料')]:out+=text(x,279,24,label,'#FFFFFF',700)
    rows=[('客数が不足',['2週間の通行量調査','試験販売で客単価を確認'],['計画82人・1,100円に','根拠があるか']),('工事額が上振れ',['同じ条件で3社へ見積','予備費と上限を確認'],['見積額と予備費を含む','必要資金']),('店長が不足',['候補者の意向と配置を確認','採用・育成の日程を確定'],['配置の見通しと','育成に必要な期間'])]
    for i,(risk,check,material) in enumerate(rows):
        y=297+i*98
        out+=rect(64,y,1150,98,'#E5EEE7' if i%2==0 else '#F7F5EE')+text(82,y+41,25,risk,'#21654C',700)
        out+=lines(390,y+35,check,size=23,gap=37)+lines(842,y+35,material,size=23,gap=37)+rect(64,y+97,1150,1,'#CAD5CC')
    out+=text(64,628,22,'契約が前提ではない。確認結果と追加資金を、投資決裁へ出す。','#53675E')
    return body(group('risk-confirmation','64 245 1150 346',out))

def decision_schedule():
    # Original input intervals: weeks 1-2, 3-4, then week 5. Boundary scale is 0-5.
    left,right=310,1195
    week=lambda value:left+(right-left)*value/5
    out=text(64,213,21,'仮日程：各週の終わりを目盛りにする。資料が不足すれば決裁は延期。','#53675E')
    chart=f'<g id="decision-schedule"><g id="decision-schedule-chartArea">'
    chart+=rect(left,250,right-left,2,'#53675E')
    chart+='<!-- chart-plot-area: object=decision-schedule | 310,250,1195,510 -->'
    for i in range(6):
        x=week(i);chart+=rect(x,250,1,260,'#CAD5CC')
        chart+=text(x-22 if i else x-8,240,17,f'{i}週末' if i else '開始','#53675E')
    for y,start,end,label,task in [(290,0,2,'現地調査','1〜2週'),(382,2,4,'見積・条件交渉','3〜4週'),(474,4,5,'投資決裁','5週')]:
        out+=text(64,y+14,25,label,weight=700)+text(64,y+44,20,task,'#53675E')
        chart+=rect(week(start),y,week(end)-week(start),44,'#21654C')
        chart+=text(week(start)+16,y+30,23,task,'#FFFFFF',700)
    chart+='</g></g>'
    out+=chart+text(64,566,22,'担当：調査は既存店長、運営設計は新店候補店長、決裁は経営者。')
    out+=rect(64,587,1150,2,'#CAD5CC')+text(64,625,25,'決裁後：内装・採用・開業準備　／　開業日はここでは確定しない。','#21654C',700)
    return body(out)

def requested_decision():
    out=rect(64,230,700,168,'#21654C')+text(89,271,25,'今日、判断してほしいこと','#FFFFFF',700)
    out+=lines(89,322,['B案の現地調査・条件交渉を進める'],size=30,color='#FFFFFF',weight=700)
    out+=text(807,265,23,'調査後に判断すること','#53675E',700)+lines(807,316,['契約の締結','初期投資の承認'],size=28,gap=53)
    out+=text(64,456,27,'次回の決裁にそろえる3つの材料','#21654C',700)
    for i,(a,b) in enumerate([('客数の根拠','調査・試験販売の結果'),('工事見積','同条件の3社見積と予備費'),('店長配置','配置の見通しと育成日程')]):
        x=64+i*390;out+=rect(x,485,342,2,'#21654C')+text(x,530,27,a,weight=700)+text(x,577,22,b)
    return body(out)

def cafe():
    d=INPUTS["cafe"]
    revenue=d["daily_customers"]*d["ticket_yen"]*d["business_days"]/10000
    fixed=sum(d["fixed_cost_man_yen"].values())
    margin=1-d["variable_cost_ratio"]
    profit=revenue*margin-fixed
    breakeven=fixed/margin
    customers=breakeven*10000/d["ticket_yen"]/d["business_days"]
    stress=d["stress_daily_customers"]*d["ticket_yen"]*d["business_days"]/10000*margin-fixed
    scores=[sum(w*s/d["score_scale"] for w,s in zip(d["weights"],p["scores"])) for p in d["sites"]]
    summary=dict(revenue_man_yen=revenue,fixed_cost_man_yen=fixed,variable_cost_man_yen=revenue*(1-margin),profit_man_yen=profit,break_even_man_yen=breakeven,break_even_daily_customers=customers,stress_profit_man_yen=stress,site_scores=scores)
    roster=[
      ("運河沿いB案を、調査・交渉へ",body(lines(64,260,["喫茶つむぎ","2号店出店提案"],size=57,gap=87,weight=700)+text(69,488,27,"投資決裁の前に、客数と工事額を確かめる")+text(69,552,23,"社内決裁用 / 8分の説明 / 計画上の仮定を含む","#53675E")),"cover","今日の判断は契約ではなく、B案の現地調査と条件交渉へ進むことです。最終決裁に必要な客数・工事額・店長配置はまだ仮定です。"),
      ("新店の顧客と、既存店との役割",audience_relation(),"content","顧客像は仮説です。既存店の来店理由を短い聞き取りで確認し、新店の利用場面が重なるだけにならないか検証します。"),
      ("候補地の比較：B案は82点",comparison_table(d),"content","僅差の評価です。B案は滞在環境と賃料に利点があり、A案は通行量と視認性が優れます。点数だけで決めず、82人という計画客数が成立するか調査します。"),
      ("損益分岐は、一日60人",body(text(64,273,74,f"{profit:.1f}", "#21654C",700)+text(262,270,27,"万円 / 月の営業利益（仮定）")+lines(64,340,[f"計画売上 {revenue:.2f}万円",f"変動費 {revenue*(1-margin):.2f}万円",f"固定費 {fixed:.0f}万円"],size=26,gap=58)+lines(665,261,["売上 = 82人 × 1,100円 × 26日","変動費率 = 35%","損益分岐 = 110万円 ÷ 65%",f"必要客数 = {customers:.1f}人 / 日"],size=24,gap=62)+text(665,545,25,f"55人 / 日なら {stress:.1f}万円の赤字","#A34327",700)+text(64,608,19,"税・資金繰り・減価償却の別途精査が必要。初期費用880万円は仮見積。","#53675E")),"content",f"損益分岐売上は{breakeven:.2f}万円、必要客数は{customers:.2f}人です。端数を切り上げて一日60人と表示しています。客数55人の試算では月{stress:.2f}万円。利益は保証ではなく入力仮定からの計算です。"),
      ("仕込みと購買を共通化する",operating_relation(),"content","共通化は既存店の負担を増やす可能性があります。仕込み量と移送の時間を測定し、無理のない運営体制を決めます。人件費68万円は計画値です。"),
      ("契約前に、3つのリスクを確認",risk_confirmation_table(),"content","調査で仮定が崩れた場合は計画を修正します。契約を進めることが前提ではありません。検証の結果と必要な追加資金を決裁時に示します。"),
      ("5週目に、投資判断を置く",decision_schedule(),"content","現地調査と見積の結果が揃ってから投資を決めます。5週目は仮日程で、調査が不足する場合は決裁を延期します。開業日はここで約束しません。"),
      ("今日の決裁：B案の調査を進める",requested_decision(),"ending","B案の調査と交渉を進めるための判断をお願いします。契約と投資の決裁は別です。客数、工事見積、店長配置を確認して次の会議へ持ち帰ります。")
    ]
    return roster, summary

def build(case_id, make):
    folder=CASE
    (folder/"source/svg_output").mkdir(parents=True,exist_ok=True)
    (folder/"source/notes").mkdir(exist_ok=True)
    roster,summary=make()
    logs=[]
    def command(args):
        result=subprocess.run([str(a) for a in args],cwd=folder,capture_output=True,text=True,encoding="utf-8",errors="replace")
        logs.append({"command":[str(a).replace(str(folder),".").replace(str(FORK),"<PPT_MASTER_PATH>") for a in args],"returncode":result.returncode,"stdout":result.stdout,"stderr":result.stderr})
        (folder/"build-log.json").write_text(json.dumps(logs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        if result.returncode:raise RuntimeError(result.stdout+'\n'+result.stderr)
    command([PYTHON,FORK/"scripts/attribution_guard.py"])
    # Only these eight generated outputs are replaced; no input/reference file is removed.
    for index in range(1,len(roster)+1):
        target=folder/f"source/svg_output/{index:02d}.svg"
        if target.is_file():target.unlink()
    for n,(title,content,role,note) in enumerate(roster,1):
        name=f"{n:02d}"
        (folder/f"source/svg_output/{name}.svg").write_text(page(title,content,n,len(roster),"CAFE / PROPOSAL" if case_id=="cafe-pptx" else "EC / MONTHLY REPORT",accent="#21654C" if case_id=="cafe-pptx" else "#1F5780",role=role),encoding="utf-8")
        (folder/f"source/notes/{name}.md").write_text("# "+title+"\n\n"+note+"\n",encoding="utf-8")
        if n==5 and len(roster)>=7:
            command([PYTHON,FORK/"scripts/compact_svg_styles.py",folder/"source/svg_output","--inplace"])
            command([PYTHON,FORK/"scripts/svg_quality_checker.py",folder/"source","--quick-generate","--canonical-authoring","--stage","early","--json"])
    (folder/"calculations.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Original verify-charts Gantt recipe: compare start and end X positions
    # on the explicit week-boundary scale before the one final checker.
    for values in ['0:0,2:0,4:0','2:0,4:0,5:0']:
        command([PYTHON,FORK/'scripts/svg_position_calculator.py','calc','line','--data',values,'--area','310,250,1195,510','--x-range=0,5','--y-range=0,1'])
    # Keep protected attribution checks, generated authoring validation and converter intact.
    commands=[
      [str(PYTHON),str(FORK/"scripts/compact_svg_styles.py"),str(folder/"source/svg_output"),"--inplace"],
      [str(PYTHON),str(FORK/"scripts/svg_quality_checker.py"),str(folder/"source"),"--quick-generate","--canonical-authoring","--stage","final","--json"],
      [str(PYTHON),str(folder/"source/export_with_biz.py"),str(folder/"source"),"--quick-generate","--primary-language","ja-JP","--with-notes","-t","fade","-o",str(folder/"deck.pptx")]
    ]
    for args in commands:
        command(args)
    (folder/"build-log.json").write_text(json.dumps(logs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (folder/"roster.json").write_text(json.dumps([{"title":t,"note":n} for t,_,_,n in roster],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{case_id}: {len(roster)} editable slides exported")

if __name__=="__main__":
    build("cafe-pptx",cafe)
