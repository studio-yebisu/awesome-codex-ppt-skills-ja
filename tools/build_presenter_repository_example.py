"""API-free renderer-only local trial; Presenter has no redistribution license."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/rsrohan99__presenter'
OUT=ROOT/'.build/local-trials/presenter'
COMMIT='6a4534d65bf3e053df16a1f5cb060de6d98b6a2b'
SLIDES=[
 ('週次報告を短く伝える','結論 → 変化 → 相談','架空の小チーム「青葉制作」の報告例です。聞き手が次の判断をできるよう、結論、前週からの変化、相談の順に伝えます。'),
 ('最初に、今の状態','予定どおり / 遅れあり / 判断待ち','今週の状態を短い言葉で伝えます。架空例では「遅れあり」です。経緯の説明より先に、何を知ってほしいかを示します。'),
 ('前週からの変化だけ','完了：画面案の確認\n\n未完了：素材の受け取り','今回の架空例では、画面案の確認は完了し、素材の受け取りが残っています。作業履歴をすべて読む代わりに、前週との差を説明します。'),
 ('相談は、期限と選択肢で','木曜までに、仮素材で進めるか決めたい','素材待ちが続くため、木曜までの判断を依頼します。選択肢は仮素材で進めるか、素材を待って日程を見直すかです。'),
 ('次の行動で、報告を閉じる','担当・期限・確認方法をそろえる','判断が出たら、誰がいつまでに何をするかを記録します。報告を短くすることだけを目的にせず、次の行動が分かることを目指します。'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def finish(reviewed):
 refs=[{'path':p,'sha256':sha(UP/p),'url':f'https://github.com/rsrohan99/presenter/blob/{COMMIT}/{p}'}for p in ['README.md','run.py','workflow.py','utils.py','models.py','agents/slide_maker.py','requirements.txt']]
 browser=json.loads((OUT/'browser-check.json').read_text())if(OUT/'browser-check.json').exists()else None
 record={'repository':'rsrohan99/presenter','commit':COMMIT,'production_status':'blocked','execution_status':'local_trial_generated_not_packaged','license':None,'blocker':'No LICENSE or redistribution grant at fixed commit; renderer trial only, no public example or source kit.','local_trial_path':'.build/local-trials/presenter','pages':5,'execution_scope':'Original utils.get_presentation_config/sanitize_markdown plus workflow.py specified mdslides CLI. Manually supplied Japanese content/narration; original multi-agent/OpenAI workflow, Mermaid, DeckTape, ElevenLabs and video were not executed.','original_source_modified':False,'external_api_calls':0,'source_refs':refs,'dependencies':{'MarkdownSlides':'GitLab da_doomer/markdown-slides fd27dd09cf90f00093a393338e08953c8d65d68e','playwright':'1.63.0','chromium_revision':'1243'},'qa':{'status':'local_visual_review_complete'if reviewed else'awaiting_visual_review','all_pages_visually_reviewed':reviewed,'browser':browser,'artifact_hashes':{str(p.relative_to(OUT)):sha(p)for p in [OUT/'output/index.html',OUT/'presentation.md',*sorted((OUT/'render').glob('*.png'))]}}}
 save(ROOT/'examples/repositories/presenter/ATTEMPT.json',record)
 save(ROOT/'data/presenter-repository-examples.json',[])
 save(ROOT/'data/presenter-repository-guides.json',[{'repository':'rsrohan99/presenter','production_status':'blocked','execution_status':record['execution_status'],'execution_type':'original_utils_and_documented_renderer_only','case_ids':[],'summary_ja':'原典utilsと指定mdslidesで日本語5枚をローカル生成。OpenAIを使うMulti-agent本体は未実行。固定commitにライセンスがなく、公開例・再現ZIPは配布しない。','requirements':['原典をローカル取得','README指定GitLab版MarkdownSlides（同名PyPIパッケージとは異なる）','公開配布には原典の許諾確認が必要'],'steps':['日本語本文と講稿を入力','原典の設定・Markdown整形関数を実行','原典workflow指定mdslidesでHTML生成','全ページとspeaker notesをブラウザ確認'],'commands':['python tools/build_presenter_repository_example.py'],'source_refs':refs,'evidence':'examples/repositories/presenter/ATTEMPT.json','limitations':['OpenAIによる構成・本文生成、Mermaid図、音声、動画、原典DeckTape PDFは未実施。','原典コードおよび生成HTMLは.buildローカル試作に限定。','本リポジトリに固有SKILLやテンプレートは存在しない。']}])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--finalize-only',action='store_true');ap.add_argument('--reviewed',action='store_true');a=ap.parse_args()
 if not a.finalize_only:
  OUT.mkdir(parents=True,exist_ok=True);(OUT/'media').mkdir(exist_ok=True)
  spec=importlib.util.spec_from_file_location('presenter_utils',UP/'utils.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  sections=[f'# {title}\n\n{body}\n\nNote:\n{note}\n'for title,body,note in SLIDES]
  text=mod.get_presentation_config()+mod.sanitize_markdown('\n\n[comment]: # (!!!)\n\n'.join(sections))
  (OUT/'presentation.md').write_text(text,encoding='utf-8')
  save(OUT/'input.json',{'fictional':True,'topic':'週次報告を短く伝える','slides':[{'title':t,'content':c,'narration':n}for t,c,n in SLIDES]})
  (OUT/'PROMPT.md').write_text('架空の小チーム「青葉制作」向けに、週次報告を短く伝える日本語5ページを作る。一枚一論点、説明は講稿へ分ける。外部APIは使わず、原典のMarkdown整形と指定rendererだけを実行する。',encoding='utf-8')
  (OUT/'NOTES.md').write_text('\n\n'.join(f'{i}. {n}'for i,(_,_,n)in enumerate(SLIDES,1)),encoding='utf-8')
  command=[str(Path(sys.executable).parent/'mdslides.exe'),str(OUT/'presentation.md'),'--include',str(OUT/'media'),'--output_dir',str(OUT/'output')]
  env=os.environ.copy();env['PYTHONUTF8']='1'
  r=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');(OUT/'execution.log').write_text(json.dumps(command,ensure_ascii=False)+'\n'+r.stdout+r.stderr,encoding='utf-8')
  if r.returncode:raise RuntimeError(r.stderr)
 finish(a.reviewed)
if __name__=='__main__':main()
