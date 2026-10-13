"""Execute EveryInc/hands-on-deck atomic editing on a locally authored donor PPTX."""
from pathlib import Path
import json,shutil,subprocess,sys,hashlib,os
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'examples/repositories/hands-on-deck';UP=ROOT/'.build/actual-upstreams/EveryInc__hands-on-deck'
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 for d in ['input','source/upstream','review','render']:(P/d).mkdir(parents=True,exist_ok=True)
 for f in ['LICENSE','README.md','ACQUISITION.json']:shutil.copy2(UP/f,P/'source/upstream'/f)
 skill=UP/'skills/hands-on-deck'
 for f in ['SKILL.md','designing-slides.md']:shutil.copy2(skill/f,P/'source/upstream'/f)
 shutil.copytree(skill/'scripts',P/'source/upstream/scripts',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 shutil.copy2(UP/'LICENSE',P/'LICENSE-UPSTREAM.txt')
 donor=ROOT/'examples/repositories/cyberppt/deck.pptx';shutil.copy2(donor,P/'input/donor.pptx')
 shutil.copy2(ROOT/'examples/repositories/cyberppt/design/icons/LICENSE-tabler.txt',P/'input/LICENSE-tabler.txt')
 shutil.copy2(ROOT/'examples/repositories/cyberppt/source/render_powerpoint.ps1',P/'source/render_powerpoint.ps1')
 slides=[
  {'title':'イベント案内の\n公開前チェック','subtitle':'こもれび商店街｜運用のたたき台','label-0':'見つける','label-1':'確かめる','label-2':'迷わず行く','takeaway':'公開前の確認と、変更時の連絡をそろえる。','footer':'架空の運用例。公開・確認は未実施。'},
  {'title':'入口から詳細まで、つながりを確認する','subtitle':'仮の掲載ページで、リンク切れと情報不足を確認する','section':'案内をたどる経路','current':'入口','proposal':'一覧','keep':'詳細','list-label':'イベント一覧','details-label':'各イベントの\n詳しい案内','caveat':'確認用の架空データ','takeaway':'入口から詳細へ、迷わずたどれるようにする。','footer':'架空の運用例。実際の検証結果ではない。'},
  {'title':'見つけた問題を、次の対応につなげる','subtitle':'以下は不具合の想定例。実際の確認結果ではない。','headers':['チェック項目','見る場所','確認する人','想定する問題','次の対応'],'rows':[['日時・場所','一覧と詳細','主催者','食い違い','確認して修正'],['費用・雨天','詳細ページ','編集窓口','情報が不足','主催者へ確認'],['連絡先','一覧の末尾','編集窓口','窓口が不明','連絡先を追記']],'note-1':'問題がなければ、確認日と確認者を記録する。','note-2':'不明な内容は推測で埋めず、主催者へ確かめる。','takeaway':'見つけるだけで終えず、直す担当まで決める。','footer':'架空の運用例。掲載情報はすべて例示。'},
  {'title':'原稿の確認と、公開後の更新を分担する','subtitle':'担当案を先に共有し、実際の運用前に合意する','headers':['段階','担当案','確認すること'],'rows':[['原稿を点検','編集窓口','内容・リンク・更新日'],['主催者が確認','各店・主催者','日時・料金・雨天対応'],['公開後も更新','主催者→編集窓口','変更内容・反映時刻']],'note-1':'急な変更があれば、主催者が編集窓口へ連絡する。','takeaway':'確認する人と、変更を伝える先を決める。','footer':'架空の運用例。担当者との合意は未取得。'},
  {'title':'最後は、使う人の目線で確かめる','subtitle':'公開前に試す確認案｜利用者テストは未実施','headers':['確認したいこと','確かめ方','記録すること'],'rows':[['入口をたどれるか','SNSや掲示から一覧を開く','行き止まり・リンク切れ'],['必要な情報があるか','日時と場所を探してもらう','見つからない項目'],['紙でも読めるか','印刷した一覧で同じ案内を探す','小さい文字・読めない情報']],'note-1':'実施前：確認するページと担当者を決める','note-2':'実施後：問題・対応・再確認日を記録する','takeaway':'使える案内かを、公開する前に確かめる。','footer':'架空の運用例。テストは提案であり未実施。'}]
 notes=['既存の企画資料を公開前の確認手順へ編集した作例です。実在の運用実績や公開済みという意味ではありません。','SNS、Web、掲示板から一覧へ進み、各イベントの詳細へたどれるかを確認する案です。実際のリンク検証は未実施です。','表の不具合は想定例です。日時や場所の食い違い、費用や雨天対応の不足、連絡窓口の不明瞭さを、確認する人と次の対応へ結びます。','編集窓口が原稿を点検し、主催者が内容を確認してから公開します。公開後の変更連絡も担当を決めるという提案で、合意はまだありません。','公開前に利用者の目線で確認する計画です。結果を測定した表ではありません。問題が出たら対応と再確認日を記録します。']
 dump(P/'input/data.json',{'title':'イベント案内の公開前チェック','fictional':True,'donor':'donor.pptx','donor_sha256':sha(P/'input/donor.pptx'),'donor_origin':'Locally authored CyberPPT Japanese example; not an upstream sample or template.','slides':slides,'notes':notes})
 receipts=[];cli=P/'source/upstream/scripts/deck.py'
 def run(args,name,allowed=(0,)):
  cmd=[sys.executable,str(cli)]+[str(a) for a in args];env=dict(os.environ);lo=Path('C:/Program Files/LibreOffice/program')
  if not shutil.which('soffice') and (lo/'soffice.exe').exists():env['PATH']=str(lo)+os.pathsep+env.get('PATH','')
  r=subprocess.run(cmd,cwd=P,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');log=P/'review'/name;log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');receipts.append({'argv':cmd,'cwd':str(P),'script':'deck.py','exit_code':r.returncode,'log':str(log.relative_to(P)),'log_sha256':sha(log)});dump(P/'review/execution-receipts.json',receipts)
  if r.returncode not in allowed:raise RuntimeError(r.stdout+'\n'+r.stderr)
  return r
 run(['docs'],'original-docs.log')
 run([P/'input/donor.pptx','inspect','-o',P/'review/donor-inspect.json'],'donor-inspect.log')
 inventory=json.loads((P/'review/donor-inspect.json').read_text(encoding='utf-8'));ops=[{'op':'set-props','title':'イベント案内の公開前チェック','author':'Japanese Example Project','last_modified_by':'Japanese Example Project','subject':'架空の商店街の運用案'}];changes=[]
 for i,s in enumerate(slides):
  shapes=inventory['slides'][str(i)];byname={v.get('name'):k for k,v in shapes.items() if isinstance(v,dict)}
  fields={k:v for k,v in s.items() if k not in ['headers','rows']}
  if 'headers' in s:
   fields.update({'header-'+str(c):v for c,v in enumerate(s['headers'])});fields.update({f'cell-{r}-{c}':v for r,row in enumerate(s['rows']) for c,v in enumerate(row)})
  for name,text in fields.items():
   sid=byname[name];old='\n'.join(p.get('text','') for p in shapes[sid].get('paragraphs',[]));ops.append({'op':'set-text','slide':i,'shape':sid,'text':text.split('\n')});changes.append({'slide_0based':i,'shape_id':sid,'shape_name':name,'before':old,'after':text})
  ops.append({'op':'set-notes','slide':i,'notes':notes[i]})
  if i==0:ops.append({'op':'set-style','slide':i,'shape':byname['label-1'],'font_size':24})
  if i==1:ops.append({'op':'set-style','slide':i,'shape':byname['title'],'font_size':32});ops.append({'op':'set-style','slide':i,'shape':byname['takeaway'],'font_size':25})
  if i==2:
   for c in [0,2,3]:ops.append({'op':'set-style','slide':i,'shape':byname['header-'+str(c)],'font_size':19})
  if i==4:
   for r in range(3):ops.append({'op':'set-style','slide':i,'shape':byname[f'cell-{r}-0'],'font_size':18})
 dump(P/'input/patch.json',{'ops':ops});dump(P/'review/changes.json',changes)
 run([P/'input/donor.pptx','apply',P/'input/patch.json','-o',P/'review/pre-fix.pptx'],'apply.log')
 run([P/'review/pre-fix.pptx','fix','--slides','0,1,2,3,4','-o',P/'deck.pptx'],'fix.log')
 run([P/'deck.pptx','inspect','-o',P/'review/result-inspect.json'],'result-inspect.log')
 run([P/'input/donor.pptx','diff',P/'deck.pptx'],'diff.log')
 run([P/'deck.pptx','render','-o',P/'review/original-render'],'original-render.log',allowed=(0,1))
 print(json.dumps({'case':str(P),'patch_operations':len(ops),'text_edits':len(changes),'donor_sha256':sha(P/'input/donor.pptx'),'artifact_sha256':sha(P/'deck.pptx')},ensure_ascii=False))
if __name__=='__main__':main()
