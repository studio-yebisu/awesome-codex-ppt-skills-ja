"""Prepare an original PradaSlides contract/runtime example, not a shared renderer."""
from pathlib import Path
import json,shutil,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];CASE=ROOT/'examples/repositories/pradaslides';UP=ROOT/'.build/actual-upstreams/prodigeproject__pradaslides'
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 for name in ['input','source','review','render','licenses']:(CASE/name).mkdir(parents=True,exist_ok=True)
 names=['SKILL.md','README.md','LICENSE','ACQUISITION.json']
 names += ['scripts/'+x for x in ['_report.py','bootstrap_project.py','build_pptx_preview.py','capability_scan.py','inspect_pptx.py','lint_deck_plan.py','resolve_capabilities.py','scaffold_presenter.py','self_test.py','validate_asset_manifest.py','validate_brief.py','validate_design_system.py','validate_layout_manifest.py','validate_reference_benchmark.py','validate_source_ledger.py','validate_visual_generation_plan.py','qa_html_presenter.mjs']]
 names += ['references/'+x+'.md' for x in ['intent-playbooks','runtime-and-delivery','capability-orchestration','content-and-narrative','design-and-visuals','art-direction-and-pptx-reconstruction','topology-and-layouts','artifact-contracts','qa','html-presenter-console']]
 names += [p.relative_to(UP).as_posix() for d in ['assets/starter','assets/html-presenter'] for p in (UP/d).glob('*') if p.is_file()]
 for name in names:
  out=CASE/'source/upstream'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(UP/name,out)
 shutil.copy2(UP/'LICENSE',CASE/'licenses/LICENSE-upstream.txt')
 argv=[sys.executable,str(CASE/'source/upstream/scripts/bootstrap_project.py'),'--output',str(CASE/'project'),'--intent','teaching-workshop','--project','町内会の備品貸出','--contracts','full']
 r=subprocess.run(argv,cwd=CASE,capture_output=True,text=True,encoding='utf-8');log=CASE/'review/bootstrap.log';log.write_text(r.stdout+'\n'+r.stderr,encoding='utf-8');save(CASE/'review/bootstrap-receipt.json',{'argv':argv,'cwd':str(CASE),'exit_code':r.returncode,'log':'review/bootstrap.log','log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()});r.check_returncode()
 pages=[
 {'title':'町内会の備品貸出を、迷わない手順に','claim':'借りる前に、返すところまで決める。','role':'cover','phase':'attention','topology':'stage','layout':'hero-decision','tone':'dark','notes':'架空の町内会を想定した手順案です。実際の貸出規則ではありません。申込みから返却までの確認事項を、借りる人と担当者が同じ順序で使うことを目指します。'},
 {'title':'品名・数量・日時を、まとめて伝える','claim':'申込時に必要な情報を一つの記録へそろえる。','role':'content','phase':'orientation','topology':'frame','layout':'artifact-proof-frame','tone':'light','notes':'申込書の例を見せます。折りたたみ椅子10脚、10月20日9時から16時、集会所前での受取りと返却という架空の設定です。実際の担当窓口と貸出条件を確認して記入します。'},
 {'title':'数と状態を、その場で一緒に確認する','claim':'受取り時に数量・状態・返却条件を担当者と照合する。','role':'content','phase':'insight','topology':'spine','layout':'process-spine','tone':'light','notes':'借りる人だけで判断せず、担当者と一緒に数、傷や欠品、返却日時と場所を確かめる手順案です。気づいた点は受取り時の記録に残します。'},
 {'title':'不具合に気づいたら、使う前に窓口へ','claim':'異常に気づいた時点で使用を止め、担当者に扱いを確認する。','role':'content','phase':'resolution','topology':'split','layout':'claim-proof-split','tone':'dark','notes':'受取り時でも使用中でも、異常に気づいたら使い続けず担当者に知らせる案です。破損の原因や弁償をこの資料で決めるものではなく、実際のルールと担当者の指示を確認します。'},
 {'title':'返却は、置くだけで終わらせない','claim':'借りた品と返す品を照合し、担当者の確認を記録する。','role':'content','phase':'decision','topology':'matrix','layout':'decision-matrix','tone':'light','notes':'数量、付属品、状態を記録と照合し、担当者の確認を受けて返却を完了する案です。無人で置いていく可否も各町内会のルールによるため、事前に返却方法を聞きます。'},
 {'title':'借りる前に、返却方法まで聞こう。','claim':'窓口・日時と場所・変更時の連絡先を確認してから申し込む。','role':'closing','phase':'retention','topology':'stage','layout':'decision-lock','tone':'light','notes':'実際の貸出ルールと窓口を確認することが次の行動です。この6ページは相談用の架空の手順案で、既存の運用規則の代わりにはなりません。'}]
 data={'id':'pradaslides','title':pages[0]['title'],'notice':'架空の町内会を想定した手順案','pages':pages,'form_example':{'品名・数量':'折りたたみ椅子 10脚','利用日時':'10月20日 9:00〜16:00','受取・返却':'集会所前で担当者と確認','連絡先':'申込み時に窓口へ伝える'}};save(CASE/'input/data.json',data)
 (CASE/'input/BRIEF.md').write_text('# 備品貸出の説明資料\n\n町内会で備品を借りる人へ、申込みから返却までの確認方法を6ページで伝える。架空の手順案と明記し、導入効果や実在ルールは作らない。編集可能なPPTXと原典のrender-parity HTML presenterを作る。写真や生成画像ではなく、編集できる申込書・手順・照合表を使う。\n',encoding='utf-8')
 (CASE/'PROMPT.txt').write_text('PradaSlidesの原典ワークフローで「町内会の備品貸出を、迷わない手順に」を日本語6ページにする。既定の編集可能PPTXを正本とし、原典build_pptx_preview.pyでPowerPoint実描画からHTML presenterを作る。町内会で備品を借りる人が申込み・受取り・異常時の連絡・返却を確認できる内容にする。すべて架空の手順案。生成画像を使わず、申込書の例と手順図・照合表をnative要素で作る。原典の計画lint、PPTX検査、HTML QAを使い、全ページを実描画・目視する。\n',encoding='utf-8')
 print(CASE)
if __name__=='__main__':main()
