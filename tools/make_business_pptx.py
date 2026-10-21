"""Editable Japanese business examples through the unmodified PPT Master compiler."""
from pathlib import Path
import html, json, subprocess

ROOT = Path(__file__).resolve().parents[1]
FORK = ROOT / "skill-forks/ppt-master-ja"
PYTHON = ROOT / ".build/ppt-master-venv/Scripts/python.exe"
INPUTS = json.loads((ROOT/"data/case-inputs.json").read_text(encoding="utf-8"))

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
    footer=group("footer","64 659 1150 28",text(64,679,14,"架空の組織・数値による制作サンプル / 八百万図AIツールボックス","#53675E")+text(1115,679,16,f"{n:02d} / {total:02d}","#53675E"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720" lang="ja" font-family="Noto Sans JP" data-pptx-page-role="{role}"><rect id="background" data-pptx-role="background" width="1280" height="720" fill="#F7F5EE"/>{header}{body}{footer}</svg>'

def body(content):
    return group("content","64 190 1150 426",content)

def columns(items, accent="#21654C"):
    out=""
    for i,(head,copy) in enumerate(items):
        x=64+i*390
        out+=rect(x,205,342,3,accent)+text(x,258,30,head,accent,700)+lines(x,319,copy,size=23,gap=45)
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
      ("新店の顧客と、既存店との役割",columns([("平日の近隣客",["仕事の合間に、ひと息。","落ち着いて滞在できる席。"]),("週末の来訪者",["散歩と買い物の途中に。","家族で利用できる場所。"]),("既存店との役割",["24席の既存店は日常使い。","新店は滞在しやすさを重視。"])]),"content","顧客像は仮説です。既存店の来店理由を短い聞き取りで確認し、新店の利用場面が重なるだけにならないか検証します。"),
      ("候補地の比較：B案は82点",body(text(64,223,20,"5点満点 × 重み / 合計100点。仮置き評価のため現地調査で更新。","#53675E")+lines(64,292,["比較項目","滞在しやすさ 30%","通行量 25%","賃料 20%","視認性 15%","運営しやすさ 10%"],size=23,gap=45)+lines(660,292,["A 駅前","4 / 5","5 / 5","3 / 5","4 / 5","4 / 5"],size=24,gap=45)+lines(947,292,["B 運河沿い","5 / 5","3 / 5","5 / 5","3 / 5","4 / 5"],size=24,gap=45,color="#21654C")+text(660,602,27,f"81点 / 賃料28万円",weight=700)+text(947,602,25,"82点 / 賃料18万円","#21654C",700)),"content","僅差の評価です。B案は滞在環境と賃料に利点があり、A案は通行量と視認性が優れます。点数だけで決めず、82人という計画客数が成立するか調査します。"),
      ("損益分岐は、一日60人",body(text(64,273,74,f"{profit:.1f}", "#21654C",700)+text(262,270,27,"万円 / 月の営業利益（仮定）")+lines(64,340,[f"計画売上 {revenue:.2f}万円",f"変動費 {revenue*(1-margin):.2f}万円",f"固定費 {fixed:.0f}万円"],size=26,gap=58)+lines(665,261,["売上 = 82人 × 1,100円 × 26日","変動費率 = 35%","損益分岐 = 110万円 ÷ 65%",f"必要客数 = {customers:.1f}人 / 日"],size=24,gap=62)+text(665,545,25,f"55人 / 日なら {stress:.1f}万円の赤字","#A34327",700)+text(64,608,19,"税・資金繰り・減価償却の別途精査が必要。初期費用880万円は仮見積。","#53675E")),"content",f"損益分岐売上は{breakeven:.2f}万円、必要客数は{customers:.2f}人です。端数を切り上げて一日60人と表示しています。客数55人の試算では月{stress:.2f}万円。利益は保証ではなく入力仮定からの計算です。"),
      ("仕込みと購買を共通化する",columns([("新店",["32席の滞在型店舗。","店長候補の配置を先行。"]),("既存店",["仕込みの一部を支える。","繁忙時間の負荷を確認。"]),("共通化",["材料の購買をまとめる。","品質基準と日報を揃える。"])]),"content","共通化は既存店の負担を増やす可能性があります。仕込み量と移送の時間を測定し、無理のない運営体制を決めます。人件費68万円は計画値です。"),
      ("契約前に、3つのリスクを確認",columns([("客数",["通行量を2週間調査。","試験販売で単価を確認。"]),("工事額",["3社へ同じ条件で見積。","予備費と上限を決める。"]),("店長配置",["候補者の意向を確認。","採用と育成の日程を確定。"])]),"content","調査で仮定が崩れた場合は計画を修正します。契約を進めることが前提ではありません。検証の結果と必要な追加資金を決裁時に示します。"),
      ("5週目に、投資判断を置く",body(rect(105,370,1015,4,"#21654C")+lines(64,240,["1〜2週","現地調査"],size=28,gap=51)+lines(361,240,["3〜4週","見積・条件交渉"],size=28,gap=51)+lines(725,240,["5週","投資決裁"],size=28,gap=51)+lines(64,485,["決裁後：内装・採用・開業準備","担当：既存店長が調査、新店候補店長が運営設計、経営者が決裁"],size=26,gap=66)),"content","現地調査と見積の結果が揃ってから投資を決めます。5週目は仮日程で、調査が不足する場合は決裁を延期します。開業日はここで約束しません。"),
      ("今日の決裁：B案の調査を進める",body(lines(64,271,["承認してほしいこと","B案の現地調査・条件交渉"],size=41,gap=78,weight=700)+lines(68,447,["次回に揃えるもの：客数の根拠、工事見積、店長配置","契約・投資の承認は、調査結果を確認してから"],size=27,gap=71)),"ending","B案の調査と交渉を進めるための判断をお願いします。契約と投資の決裁は別です。客数、工事見積、店長配置を確認して次の会議へ持ち帰ります。")
    ]
    return roster, summary

def ec():
    d=INPUTS["ec"]
    sales=d["sales_man_yen"];prev=d["previous_sales_man_yen"]
    gross=sales*d["gross_margin_ratio"];previous=prev*d["previous_gross_margin_ratio"]
    summary=dict(sales_growth_percent=(sales/prev-1)*100,gross_profit_man_yen=gross,previous_gross_profit_man_yen=previous,average_order_yen=sales*10000/d["orders"],channel_total_man_yen=sum(c["sales_man_yen"] for c in d["channels"]))
    bars=""
    for i,c in enumerate(d["channels"]):
        y=251+i*82
        bars+=text(64,y,25,c["name"])+rect(300,y-27,c["sales_man_yen"]/400*600,33,"#1F5780")+text(938,y,27,f'{c["sales_man_yen"]}万円',weight=700)+text(1070,y,18,f'+{c["sales_man_yen"]-c["previous_man_yen"]}',"#53675E")
    roster=[
      ("売上は前年比20%増、粗利率は低下",body(lines(64,266,["くらし便","EC事業 9月報告"],size=58,gap=88,weight=700)+text(68,496,27,"2026年9月 / 比較：2025年9月")+text(68,556,25,"次月は商品説明と粗利分析を先行","#1F5780",700)),"cover","売上は前年同月比20%増ですが、粗利率と返品率に課題があります。架空データを使った月次報告です。先に商品説明を改善し、利益の差分を分解します。"),
      ("KPI：売上だけで判断しない",columns([("売上 1,200万円",["前年 1,000万円 / +20%","注文 4,000件 / 前年3,500件"]),("粗利率 36%",["前年 38% / −2pt",f"粗利 {gross:.0f}万円 / 前年380万円"]),("返品率 6%",["前年 4% / +2pt","理由を商品別に確認"])]),"content","売上と粗利額は増えています。一方で粗利率は2ポイント下がり、返品率は2ポイント上がりました。百分率の変化とポイント差を混同しないようにしてください。"),
      ("売上増200万円を、チャネルで分解",body(bars+text(64,609,20,"棒：当月売上 / 右端：前年同月との差（万円）。4チャネルの合計は1,200万円。","#53675E")),"content","自然検索が90万円増、メールが50万円増、リピート直訪が40万円増、広告が20万円増です。棒の長さは同じ単位の当月売上に対応しています。"),
      ("粗利は52万円増、率は2pt低下",body(text(64,281,78,"432", "#1F5780",700)+text(282,280,27,"万円 / 当月粗利")+text(68,357,25,"前年：1,000万円 × 38% = 380万円")+text(68,420,25,"当月：1,200万円 × 36% = 432万円")+lines(715,277,["増えた粗利：52万円","売上の増加が率低下を補った","値引き・商品構成を分解する"],size=28,gap=76)+text(64,571,24,"粗利額の増加と、粗利率の改善は別の判断。","#1F5780",700)),"content","当月と前年の粗利額を同じ算式で確認しています。値引きや商品構成はまだ原因の仮説なので、原因として断定しません。次回までに商品別の差分を分析します。"),
      ("課題は、仮説と確認を対にする",columns([("返品の増加",["仮説：説明と実物の差。","確認：返品理由を分類。"]),("粗利率の低下",["仮説：値引きと商品構成。","確認：商品別に利益を分解。"]),("次の判断",["広告増額は保留。","原因の確認後に配分を決める。"])]),"content","仮説を事実として扱わず、確認する作業まで割り当てます。返品の分類と利益分析を先に進め、その結果で販売施策を判断します。"),
      ("10月の施策と、担当・期限",body(lines(64,245,["10/09  CS・森：上位20商品の返品理由を分類","10/16  商品・青木：返品上位5商品の説明を改稿","10/16  販売・山田：粗利率の差分を商品別に分解"],size=28,gap=106)+text(64,592,22,"実行の確認：分類率100%、対象商品の返品率を週次比較、粗利差分の説明。","#53675E")),"content","担当と期限を置きます。施策後の返品率は施策対象商品を同じ期間で比較します。季節性などの影響もあるため、単純な前後比較だけで因果効果を断定しません。"),
      ("次月判断：説明修正と分析を先行",body(lines(64,277,["商品説明を直す","粗利率の差分を説明する"],size=44,gap=81,weight=700)+lines(68,469,["広告増額は、その結果を確認してから判断","次回：施策の完了、返品の内訳、粗利の要因を確認"],size=27,gap=71)),"ending","月次会議で決めたいのは分析と説明修正を先行することです。広告費増額をこの資料だけで決めず、次回の根拠を揃えます。")
    ]
    return roster, summary

def build(case_id, make):
    folder=ROOT/"examples/cases"/case_id
    (folder/"source/svg_output").mkdir(parents=True,exist_ok=True)
    (folder/"source/notes").mkdir(exist_ok=True)
    roster,summary=make()
    for n,(title,content,role,note) in enumerate(roster,1):
        name=f"{n:02d}"
        (folder/f"source/svg_output/{name}.svg").write_text(page(title,content,n,len(roster),"CAFE / PROPOSAL" if case_id=="cafe-pptx" else "EC / MONTHLY REPORT",accent="#21654C" if case_id=="cafe-pptx" else "#1F5780",role=role),encoding="utf-8")
        (folder/f"source/notes/{name}.md").write_text("# "+title+"\n\n"+note+"\n",encoding="utf-8")
    (folder/"calculations.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Keep protected attribution checks, generated authoring validation and converter intact.
    commands=[
      [str(PYTHON),str(FORK/"scripts/attribution_guard.py")],
      [str(PYTHON),str(FORK/"scripts/compact_svg_styles.py"),str(folder/"source/svg_output"),"--inplace"],
      [str(PYTHON),str(FORK/"scripts/svg_quality_checker.py"),str(folder/"source"),"--quick-generate","--canonical-authoring","--stage","final","--json"],
      [str(PYTHON),str(FORK/"scripts/svg_to_pptx.py"),str(folder/"source"),"--quick-generate","--primary-language","ja-JP","--with-notes","-t","fade","-o",str(folder/"deck.pptx")]
    ]
    logs=[]
    for args in commands:
        r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding="utf-8",errors="replace")
        logs.append({"command":[Path(a).relative_to(ROOT).as_posix() if Path(a).is_absolute() and str(ROOT) in a else a for a in args],"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr})
        if r.returncode:
            print(r.stdout[-3500:],r.stderr[-1500:]);raise RuntimeError("PPT Master conversion failed")
    (folder/"build-log.json").write_text(json.dumps(logs,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (folder/"roster.json").write_text(json.dumps([{"title":t,"note":n} for t,_,_,n in roster],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"{case_id}: {len(roster)} editable slides exported")

if __name__=="__main__":
    build("cafe-pptx",cafe)
    build("ec-monthly",ec)
