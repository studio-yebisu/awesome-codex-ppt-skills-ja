"""Author original Japanese vector examples. All business figures are labelled fictional."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def text(x,y,content,size=32,fill=None,weight=400,**kwargs):
    n=dict(type='text',x=x,y=y,text=content,size=size,weight=weight,**kwargs)
    if fill:n['fill']=fill
    return n
def rect(x,y,w,h,fill,**kwargs):return dict(type='rect',x=x,y=y,w=w,h=h,fill=fill,**kwargs)
def circle(x,y,r,fill,**kwargs):return dict(type='circle',x=x,y=y,r=r,fill=fill,**kwargs)
def line(x,y,x2,y2,stroke,width=2):return dict(type='line',x=x,y=y,x2=x2,y2=y2,stroke=stroke,strokeWidth=width,fill='none')
def path(d,stroke,width=3,fill='none'):return dict(type='path',d=d,stroke=stroke,strokeWidth=width,fill=fill)
def page(title,nodes,notes,background=None,duration=7):
    p=dict(title=title,nodes=nodes,notes=notes,duration=duration)
    if background:p['background']=background
    return p
def head(label,title,accent,ink):return [text(72,72,label,18,accent,700,spacing=2),text(72,157,title,48,ink,700),line(72,195,1208,195,accent,1)]
def footer(num,ink,note='八百万図AIツールボックス · オリジナル作例'):
    return [text(72,678,note,16,ink),text(1208,678,f'{num:02d} / 04',16,ink,anchor='end')]
def deck(id,title,category,style,font,bg,ink,accent,skill,description):
    return dict(id=id,title=title,category=category,style=style,font=font,background=bg,ink=ink,accent=accent,skill=skill,description=description,credit='八百万図AIツールボックス',license='CC0-1.0',slides=[])

blue='#243CDA';navy='#162139';cream='#F4F1E8';red='#BC4933';green='#285A4A';dark='#151C32';cyan='#8CD9EE';yellow='#DDF569'
decks=[]

d=deck('team-report','週次レポートのAI導入提案','business','コーポレート','BIZ UDPGothic','#F6F7FC',navy,blue,'yebisu-pptx','社内提案に。結論、比較、導入計画をすっきり整理。')
d['slides']=[
page('まずは、週次レポートから。',[
rect(784,0,496,720,blue),text(72,91,'社内提案 / AIの小さな導入',22,blue,700),text(72,270,'まずは、\n週次レポートから。',66,navy,700,leading=96),text(72,517,'集計と下書きを任せて、\n確認と判断に時間を使う。',28,navy,leading=44),text(836,345,'01',172,'#FFFFFF',700),text(836,458,'試す業務を\nひとつに絞る',32,'#FFFFFF',700,leading=50),text(72,678,'導入計画の説明用サンプル',16,navy)],'架空の社内提案。実績や効果を示す資料ではありません。週次レポートを試行対象に選び、担当者による確認を残す提案です。'),
page('レポート作成の分担',head('WORKFLOW','レポート作成の分担',blue,navy)+[
text(72,277,'現在',26,navy,700),text(72,335,'集計 → 整形 → 下書き → 確認',30,navy),line(72,380,1208,380,'#CBD0E4'),text(72,447,'試行案',26,blue,700),rect(70,473,625,86,blue,rx=8),text(100,526,'AI：集計・整形・下書き',30,'#FFFFFF',700),text(749,526,'人：確認・判断',30,navy,700),text(72,611,'入力に含めてよい情報は、社内のルールで決める。',24,navy)]+footer(2,navy),'社内で許可された情報と環境を使う前提。AIの下書きを人が確認してから使います。'),
page('2週間の試行計画',head('PLAN','2週間の試行計画',blue,navy)+[
line(160,347,1100,347,blue,4),circle(190,347,14,blue),circle(640,347,14,blue),circle(1090,347,14,blue),text(72,290,'1–2日目',28,blue,700),text(516,290,'3–8日目',28,blue,700),text(942,290,'9–10日目',28,blue,700),text(72,432,'入力を整える',32,navy,700),text(72,493,'様式と禁止情報を決める',24,navy),text(516,432,'下書きを比較',32,navy,700),text(516,493,'修正箇所を記録する',24,navy),text(942,432,'運用を判断',32,navy,700),text(942,493,'負担と品質を確かめる',24,navy)]+footer(3,navy),'営業日10日の提案スケジュールです。短縮効果などを測定した結果ではありません。'),
page('採用を決める3つの観点',[
text(72,95,'採用を決める3つの観点',46,navy,700),text(72,250,'品質',74,blue,700),text(72,315,'内容は正しいか',28,navy),text(492,250,'負担',74,blue,700),text(492,315,'修正は減ったか',28,navy),text(908,250,'継続',74,blue,700),text(908,315,'担当者が使えるか',28,navy),line(72,403,1208,403,blue),text(72,521,'小さく試し、運用で判断する。',50,navy,700)]+footer(4,navy),'3つの観点を記録し、実測して採用を判断します。成果を保証するものではありません。')]
decks.append(d)

d=deck('local-coffee','街のコーヒースタンド企画','pitch','エディトリアル','Noto Serif JP',cream,'#332F28',red,'yebisu-editorial-slides','余白と明朝体で、企画の世界観を伝える。')
d['slides']=[
page('朝のコーヒーを、街の習慣に。',[
text(72,92,'CONCEPT / 架空の店舗企画',18,red,700,spacing=2),circle(982,343,216,red),circle(982,343,169,cream),circle(982,343,119,red),text(72,260,'朝のコーヒーを、\n街の習慣に。',64,'#332F28',600,leading=98),text(72,534,'通勤路に、小さな寄り道を。',28,'#332F28'),line(72,605,1208,605,'#332F28',1),text(72,669,'八百万図AIツールボックス · オリジナル作例',16,'#332F28')],'架空のコーヒースタンド企画。特定の実店舗や市場調査を扱っていません。'),
page('朝の5分に合う体験',head('EXPERIENCE','朝の5分に合う体験',red,'#332F28')+[
text(72,297,'見つける',40,red,600),text(72,373,'通りからメニューが見える',25,'#332F28'),text(514,297,'選ぶ',40,red,600),text(514,373,'3つの定番から注文する',25,'#332F28'),text(963,297,'受け取る',40,red,600),text(963,373,'持ち歩きやすいカップで',25,'#332F28'),line(72,432,1208,432,red,2),text(72,553,'迷う時間を減らし、味を覚えてもらう。',40,'#332F28',600)]+footer(2,'#332F28'),'「5分」は企画上の体験目標です。3つの定番メニューも想定で、実測ではありません。'),
page('売上モデルを比較する',head('ILLUSTRATIVE DATA','売上モデルを比較する',red,'#332F28')+[
text(72,295,'月商（万円）',24,'#332F28'),line(220,555,1160,555,'#A49A87',1),rect(260,375,150,180,'#D6C9B6'),rect(550,285,150,270,red),rect(840,225,150,330,'#755F4B'),text(335,355,'12',42,'#332F28',600,anchor='middle'),text(625,266,'18',42,red,600,anchor='middle'),text(915,207,'22',42,'#332F28',600,anchor='middle'),text(335,603,'小さく開始',23,'#332F28',anchor='middle'),text(625,603,'標準案',23,'#332F28',anchor='middle'),text(915,603,'拡張案',23,'#332F28',anchor='middle')]+footer(3,'#332F28','説明用の架空データ。予測・実績ではありません。'),'グラフは単位を持つ説明用データです。12、18、22万円を比較しており、予測や実績ではありません。図形と数値はPPTXで編集できます。'),
page('次に確かめること',[
text(72,104,'次に確かめること',48,'#332F28',600),text(72,266,'01',27,red,700),text(160,266,'朝の通行量',38,'#332F28',600),line(160,305,1208,305,'#C3B7A3'),text(72,386,'02',27,red,700),text(160,386,'提供までの時間',38,'#332F28',600),line(160,425,1208,425,'#C3B7A3'),text(72,506,'03',27,red,700),text(160,506,'また来たい理由',38,'#332F28',600),text(72,606,'数字と現場の観察で、企画を磨く。',27,red,600)]+footer(4,'#332F28'),'検証項目をまとめた企画スライドです。出店や投資の推奨を行う資料ではありません。')]
decks.append(d)

d=deck('ai-classroom','生成AIを3分で説明する','education','図解・教材','BIZ UDPGothic','#ECF4E9','#213E34',green,'yebisu-story-slides','読める日本語と図解で、初めての学びを支える。')
d['slides']=[
page('生成AIのしくみを3分でつかむ',[
text(72,85,'はじめての生成AI',22,green,700),text(72,262,'生成AIのしくみを\n3分でつかむ',64,'#213E34',700,leading=98),circle(970,342,182,'#D5E6CE'),circle(882,320,45,green),circle(1033,280,45,green),circle(1012,439,45,green),line(919,309,990,291,green,5),line(903,354,979,413,green,5),line(1028,326,1018,392,green,5),text(72,556,'文章を作るAIを例に、入力と出力の関係を学ぶ。',26,'#213E34')]+footer(1,'#213E34'),'文章生成AIについての入門教材です。画像生成など、すべての生成モデルに同じ仕組みが当てはまるという説明ではありません。'),
page('入力から、次の言葉の候補へ',head('TEXT GENERATION','入力から、次の言葉の候補へ',green,'#213E34')+[
rect(72,280,320,152,'#FFFFFF',rx=8),text(108,335,'入力',24,green,700),text(108,392,'「今日は」',38,'#213E34',700),line(418,353,544,353,green,5),path('M 523 337 L 544 353 L 523 369',green,5),text(600,294,'次の言葉の候補',30,'#213E34',700),text(600,365,'晴れです / 寒いです / …',32,green,700),text(72,536,'学習したパターンを使って、\n文脈に合う続きを少しずつ作る。',34,'#213E34',700,leading=54)]+footer(2,'#213E34'),'自己回帰型の文章生成の概略です。候補の確率、トークン化、推論方法の詳細は省略しています。具体的な候補は説明用です。'),
page('自然な文章でも、確認は必要',head('CHECK','自然な文章でも、確認は必要',green,'#213E34')+[
text(72,316,'文章が自然',52,green,700),text(628,316,'内容が正しい',52,'#213E34',700),text(517,319,'≠',64,'#C77444',700),text(72,452,'人名、数字、引用、出典は\n元の資料に戻って確認する。',36,'#213E34',700,leading=60),text(72,592,'もっともらしさと正確さを、分けて考える。',26,green,700)]+footer(3,'#213E34'),'生成された文章の自然さだけでは事実の正確さを判断できません。ここでは確認すべき項目の例を示しています。'),
page('伝わる依頼の3つの材料',head('TRY IT','伝わる依頼の3つの材料',green,'#213E34')+[
text(72,299,'相手',44,green,700),text(72,369,'中学生にもわかる言葉で',25,'#213E34'),text(488,299,'目的',44,green,700),text(488,369,'文章生成のしくみを説明',25,'#213E34'),text(931,299,'形',44,green,700),text(931,369,'例をひとつ、200字で',25,'#213E34'),line(72,433,1208,433,green),text(72,540,'書いてもらったあとに、確かめる。',44,'#213E34',700)]+footer(4,'#213E34'),'依頼文の作り方の一例です。スライドの説明を短い文章にして、確認しながら改善する演習に使えます。')]
decks.append(d)

d=deck('evidence-talk','AIの答えをどう確かめるか','research','技術・登壇','Noto Sans JP',dark,'#F4F6FC',cyan,'yebisu-web-slides','暗い背景と明快な構造で、技術の話を伝える。')
d['slides']=[
page('AIの答えをどう確かめるか',[
text(72,89,'TECH TALK / 検証の考え方',19,cyan,700,spacing=2),text(72,268,'AIの答えを\nどう確かめるか',66,'#F4F6FC',700,leading=98),line(796,293,1126,293,cyan,3),line(796,411,1126,411,cyan,3),circle(862,293,24,cyan),circle(1039,411,24,cyan),text(803,227,'主張',28,cyan,700),text(1017,482,'根拠',28,cyan,700),text(72,556,'主張を分けて、根拠までたどる。',30,'#F4F6FC')]+footer(1,'#C4CEE5'),'検証の進め方を示すオリジナル登壇資料。特定の論文や実験結果を要約したものではありません。'),
page('確認できる単位に分ける',head('CLAIM','確認できる単位に分ける',cyan,'#F4F6FC')+[
text(72,286,'「この手法は速くて正確」',46,'#F4F6FC',700),line(72,359,1208,359,'#4D5B7E'),text(72,452,'速度',42,cyan,700),text(72,517,'何を、どの条件で測ったか',26,'#F4F6FC'),text(726,452,'精度',42,cyan,700),text(726,517,'何の問題を、どう評価したか',26,'#F4F6FC')]+footer(2,'#C4CEE5'),'引用符内は架空の例文です。「速い」「正確」の比較対象、条件、評価方法を切り分けます。'),
page('根拠までの道筋',head('TRACE','根拠までの道筋',cyan,'#F4F6FC')+[
line(181,354,1098,354,cyan,3),circle(200,354,40,cyan),circle(640,354,40,cyan),circle(1080,354,40,cyan),text(200,365,'1',31,dark,700,anchor='middle'),text(640,365,'2',31,dark,700,anchor='middle'),text(1080,365,'3',31,dark,700,anchor='middle'),text(72,464,'主張を抜き出す',30,'#F4F6FC',700),text(471,464,'一次資料を読む',30,'#F4F6FC',700),text(928,464,'条件を照合する',30,'#F4F6FC',700),text(72,550,'紹介記事と原典の主張が、同じ範囲かを見る。',28,cyan)]+footer(3,'#C4CEE5'),'一次資料の記述と紹介側の表現の範囲を照合する方法。すべての主張を自分で実験再現できたという意味ではありません。'),
page('結果と推測を分けて伝える',[
text(72,101,'結果と推測を分けて伝える',48,'#F4F6FC',700),text(72,279,'実験で示されたこと',34,cyan,700),text(72,353,'条件・対象・数値を添える',29,'#F4F6FC'),line(72,422,1208,422,'#4D5B7E'),text(72,508,'これから試したいこと',34,cyan,700),text(72,582,'応用の見込みとして伝える',29,'#F4F6FC')]+footer(4,'#C4CEE5'),'実験で示された事実と、将来の応用可能性を分けて表現するためのスライドです。')]
decks.append(d)

d=deck('product-story','プロダクト説明の組み立て方','product','プロダクト','Noto Sans JP','#F6C348','#20201D','#20201D','yebisu-pptx','使う場面から説明して、機能の意味を伝える。')
d['slides']=[
page('伝わるプロダクト説明の順番',[
text(72,85,'PRODUCT STORY',19,'#20201D',700,spacing=3),text(72,266,'伝わるプロダクト\n説明の順番',68,'#20201D',700,leading=100),rect(937,183,205,285,'#20201D',rx=20),rect(957,211,165,219,'#F6C348',rx=2),circle(1040,448,8,'#F6C348'),text(72,559,'使う場面から、機能の意味へ。',30,'#20201D',700)]+footer(1,'#20201D'),'プロダクト説明の構成例です。特定の製品の機能・実績を表すものではありません。'),
page('最初に、使う場面を見せる',head('CONTEXT','最初に、使う場面を見せる','#20201D','#20201D')+[
text(72,319,'誰が',68,'#20201D',700),text(483,319,'いつ',68,'#20201D',700),text(925,319,'何に困る',56,'#20201D',700),text(72,411,'チームの担当者',27,'#20201D'),text(483,411,'会議の前',27,'#20201D'),text(925,411,'資料の最新版が不明',25,'#20201D'),line(72,474,1208,474,'#20201D'),text(72,578,'状況がわかると、機能を理解しやすい。',37,'#20201D',700)]+footer(2,'#20201D'),'架空のチーム用資料管理ツールを説明する場合の例です。具体的な困りごとを先に示しています。'),
page('操作の流れを3場面に絞る',head('DEMO','操作の流れを3場面に絞る','#20201D','#20201D')+[
text(72,297,'01',56,'#20201D',700),text(483,297,'02',56,'#20201D',700),text(925,297,'03',56,'#20201D',700),text(72,403,'資料を選ぶ',34,'#20201D',700),text(483,403,'変更を見る',34,'#20201D',700),text(925,403,'共有する',34,'#20201D',700),line(72,465,1208,465,'#20201D',3),text(72,562,'一度のデモで伝える操作を、絞り込む。',38,'#20201D',700)]+footer(3,'#20201D'),'説明用の操作シナリオです。画面キャプチャや実際に動作するアプリのデモではありません。'),
page('見せた操作を、価値に結びつける',[
text(72,108,'見せた操作を、価値に結びつける',44,'#20201D',700),text(72,281,'変更がわかる',62,'#20201D',700),text(72,368,'確認する相手と内容がはっきりする',31,'#20201D'),line(72,430,1208,430,'#20201D'),text(72,543,'次に試す操作を、ひとつ案内する。',42,'#20201D',700)]+footer(4,'#20201D'),'製品の価値と次の行動を結びつける説明例。効果は製品や利用環境によって検証します。')]
decks.append(d)

d=deck('motion-manifesto','動きで伝えるスライド','motion','タイポグラフィ','Noto Sans JP','#161917','#F6FAEE',yellow,'yebisu-web-slides','図形と文字の出現を揃えて、発表にリズムを。')
d['slides']=[
page('アイデアが、動きだす。',[
text(72,92,'MOTION / VECTOR SLIDES',19,yellow,700,spacing=3),text(72,281,'アイデアが、\n動きだす。',88,'#F6FAEE',700,leading=119),circle(992,325,184,'none',stroke=yellow,strokeWidth=3,delay=160),circle(992,325,132,'none',stroke=yellow,strokeWidth=3,delay=260),circle(992,325,76,yellow,delay=360),text(72,579,'文字と図形で、話の順番をつくる。',30,'#F6FAEE',delay=520)]+footer(1,'#BFCBB8'),'SVGのベクトル要素を、短いフェードと移動で順番に表示する作例です。動画モデルで生成した映像ではありません。'),
page('要素を、順番に見せる',head('SEQUENCE','要素を、順番に見せる',yellow,'#F6FAEE')+[
text(72,352,'① 主張',54,'#F6FAEE',700,delay=100),text(478,352,'② 図解',54,yellow,700,delay=400),text(893,352,'③ 補足',54,'#F6FAEE',700,delay=700),line(72,428,1208,428,yellow,2),text(72,563,'視線の行き先を、ひとつずつ用意する。',39,'#F6FAEE',700,delay=950)]+footer(2,'#BFCBB8'),'3つの要素をずらして表示します。ブラウザの「動きを減らす」が有効な場合、出現アニメーションは省略します。'),
page('強調は、ひとつに絞る',[
text(72,97,'強調は、ひとつに絞る',46,'#F6FAEE',700),text(72,259,'色',36,'#9CA895',700),text(72,352,'大きさ',36,'#9CA895',700),text(72,445,'動き',36,'#9CA895',700),rect(478,190,730,369,yellow,rx=0,delay=200),text(527,421,'伝えたいこと',66,'#161917',700,delay=380),text(72,609,'大事な要素へ、注意が集まる構成にする。',28,'#F6FAEE')]+footer(3,'#BFCBB8'),'カラーとサイズによる強調の説明スライド。多くの要素が同時に動く構成を避けています。'),
page('最後は、言葉を残す',[
text(72,90,'LAST FRAME',19,yellow,700,spacing=3),text(72,327,'最後は、\n言葉を残す。',86,'#F6FAEE',700,leading=112),line(72,528,1208,528,yellow,3),text(72,604,'読み終えるまで、画面を落ち着かせる。',30,yellow,700,delay=600)]+footer(4,'#BFCBB8'),'最終フレームを止めて、文字を読める時間を残す作例です。自動再生は最終ページで停止します。')]
decks.append(d)

for d in decks:
    d['prompt']=f"日本語で『{d['title']}』の4枚のスライドを作ってください。{d['style']}の見た目で、{d['font']}を使い、16:9のSVGと再生HTMLを出力してください。文字と図形を編集できる形にし、1枚につき伝える内容を絞ってください。各ページに発表者ノートを付け、架空の数値・企画はその旨を明示してください。"
    d['production']=dict(author='八百万図AIツールボックス',renderer='八百万図AIツールボックス SVG renderer',pptx='OpenAI Artifact Tool',upstream_execution=False,description='派生スキルの制作方針を反映した独自作例。上流プログラムを実行した結果ではありません。')
(ROOT/'data/decks.json').write_text(json.dumps(decks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(decks)} decks / {sum(len(d["slides"]) for d in decks)} slides authored')
