"""Rebuild the CyberPPT Japanese example from its frozen ImageGen blueprints."""
from pathlib import Path
import json, shutil, subprocess, sys, hashlib, argparse
ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'examples/repositories/cyberppt'
UP=ROOT/'.build/actual-upstreams/crazyykhllc-bit__CyberPPT'
def write(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--content-only',action='store_true',help='Only replay original content locks; do not rebuild PPTX')
    args=parser.parse_args()
    for d in ['input','design','source/upstream','review','render']: (CASE/d).mkdir(parents=True,exist_ok=True)
    for name in ['SKILL.md','LICENSE']:
        if (UP/name).exists(): shutil.copy2(UP/name,CASE/'source/upstream'/name)
    for d in ['scripts','references']:
        shutil.copytree(UP/d,CASE/'source/upstream'/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    events=[['朝のパン市','11月7日（土）10–12時','こもれび広場','入場無料／購入は別','小雨実施・荒天中止'],['路地の音楽会','11月14日（土）14–16時','ふれあい会館','入場無料','屋内開催'],['夕暮れ古本交換','11月21日（土）16–18時','駅前アーケード','参加無料','屋根下で実施']]
    evidence=[{'id':'E1','claim':'こもれび商店街と掲載イベントは架空','value':None,'unit':None,'period':'2026年11月という設定','source':'本例の制作入力','confidence':'fictional','caveat':'実在の開催情報ではない','implication':'例示と実測を混同しない','visual':'全頁脚注'}, {'id':'E2','claim':'SNS・Web・掲示板に案内が分かれるという課題仮説','value':None,'unit':None,'period':None,'source':'本例の企画仮説','confidence':'hypothesis','caveat':'現地調査未実施','implication':'利用者確認が必要','visual':'現状と集約後の情報経路'}, {'id':'E3','claim':'全イベントを共通項目で比較する','value':events,'unit':'架空イベント','period':'2026年11月','source':'本例の制作入力','confidence':'fictional','caveat':'料金と雨天時の扱いも架空','implication':'一覧の掲載項目を固定','visual':'イベント比較表'}, {'id':'E4','claim':'店から窓口へ情報を渡し、確認して公開する','value':None,'unit':None,'period':None,'source':'本例の運用提案','confidence':'proposal','caveat':'担当者合意は未取得','implication':'公開前に担当と期限を決める','visual':'責任分担の流れ'}, {'id':'E5','claim':'小規模試行で見つけやすさと更新負担を確認する','value':None,'unit':None,'period':'試行2週間という提案','source':'本例の試行提案','confidence':'proposal','caveat':'効果や利用数の実績はない','implication':'検証結果で継続判断','visual':'試行計画と判断基準'}]
    base={'charts':[],'tables':[],'kpis':[],'annotations':[],'caveats':['架空の企画例。開催情報・体制・期間はすべて例示。'],'required_components':['title','main_visual','so_what','footer']}
    specs=[
      ('商店街のイベント案内を、一つにまとめる','こもれび商店街｜企画たたき台',[],['見つける','選ぶ','迷わず行く'],'一つの入口から、必要な案内にたどり着く。',['E1','E2'],'Cover'),
      ('まず「探す場所」をそろえる','SNS・Web・掲示板を行き来する、という課題仮説',[],['現状の仮説：SNS／Web／掲示板','提案：共通のイベント一覧','残すもの：各店の詳しい案内へのリンク'],'既存の発信を生かし、一覧を共通の入口にする。',['E2'],'Complication'),
      ('一覧には、比較に必要な項目をそろえる','日時・場所・費用・雨天時の扱いを同じ順序で掲載',[{'headers':['イベント','日時','場所','費用','雨天時'], 'rows':events}],['追加する管理項目：連絡先／最終更新日','掲載例の年は2026年。実在の開催予定ではない。'],'見た目より先に、掲載項目と更新日をそろえる。',['E1','E3'],'Resolution'),
      ('更新の窓口と、公開前の確認を決める','提案する担当分担｜実際の担当者との合意は未取得',[{'headers':['段階','担当案','確認すること'],'rows':[['情報を渡す','各店・主催者','日時・費用・雨天対応'],['確認して掲載','商店街の編集窓口','不足情報・リンク先・更新日'],['変更を反映','主催者→編集窓口','変更内容・反映時刻・周知先']]}],['掲載済み情報に変更があれば、主催者が窓口へ連絡する。'],'誰が直すかまで決めて、案内を古くしない。',['E4'],'Resolution'),
      ('小さく試し、続けられるかを確かめる','試行期間は2週間という提案｜効果の実測値はまだない',[{'headers':['確認したいこと','確かめ方','判断の材料'],'rows':[['見つけやすさ','来訪者に目的の案内を探してもらう','迷った場所・不足した情報'],['更新のしやすさ','担当者が掲載と変更を実施する','作業時間・手戻り・漏れ'],['紙でも伝わるか','一覧の印刷版を掲示する','文字の読みやすさ・問い合わせ']]}],['試行前：担当者・掲載範囲・確認日を決める','試行後：結果を共有し、継続・修正・中止を判断する'],'便利さと運用負担の両方を見て、次を決める。',['E5'],'Summary')]
    slides=[]
    for i,(title,subtitle,tables,annotations,so,eids,role) in enumerate(specs,1): slides.append(dict(base,slide=i,title=title,subtitle=subtitle,tables=tables,annotations=annotations,so_what=[so],evidence_ids=eids,role=role))
    outline={'fictional':True,'evidence':evidence,'storyline_candidates':[{'id':'A','scr':'案内の分散→比較しづらい→共通一覧と編集窓口','chosen':True,'reason':'案内の内容と運用を同時に説明できる'}, {'id':'B','scr':'イベントの魅力→来訪を促したい→紹介中心','chosen':False,'reason':'来訪効果の裏付けがなく、運用課題が薄れる'},{'id':'C','scr':'編集負担→更新漏れ→内部業務改善','chosen':False,'reason':'来訪者が一覧を使う価値が伝わりにくい'}],'issue_tree':{'見つける':['共通の入口','詳細へのリンク'],'選ぶ':['共通の掲載項目','料金・雨天情報'],'続ける':['編集窓口','試行で検証']},'slides':slides}
    write(CASE/'input/outline.json',outline)
    (CASE/'input/data.json').write_bytes((CASE/'input/outline.json').read_bytes())
    write(CASE/'design/style-choice.json',{'style':6,'background':'F4F0E8','accent':'9A5A2E','text':'161616','choice_actor':'agent under delegated internal-production authorization','human_approval':False,'original_style_samples_reviewed':list(range(1,9))})
    receipts=[]
    for i in range(1,6):
        cmd=[sys.executable,str(CASE/'source/upstream/scripts/build_content_lock.py'),'--outline',str(CASE/'input/outline.json'),'--slide',str(i),'--out',str(CASE/f'design/slide-{i:02d}-content-lock.json')]
        r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');log=CASE/f'review/content-lock-{i:02d}.log';log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8')
        receipts.append({'argv':cmd,'exit_code':r.returncode,'log':str(log.relative_to(CASE)),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
        if r.returncode: raise SystemExit(r.returncode)
    write(CASE/'review/execution-receipts.json',receipts)
    print('Original CyberPPT content locks created for 5 fictional slides.')
    if not args.content_only:
        subprocess.run([sys.executable,str(CASE/'source/reproduce.py')],check=True)
if __name__=='__main__': main()
