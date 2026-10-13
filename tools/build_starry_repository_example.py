"""Record fixed-commit StarryKit plugin preflight. Does not claim slide generation."""
from pathlib import Path
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
UP=ROOT/'.build/actual-upstreams/StarryKit__starry-slides'
OUT=ROOT/'examples/repositories/starry-slides'
COMMIT='0e57d121ac2f1b70cd8c1b7b65d603f4e2f21816'
REFS=['LICENSE','README.md','package.json','mcp.json','docs/development.md','skills/starrykit/SKILL.md','skills/starrykit/references/mcp-workflow.md','tests/plugin.test.mjs']
PAGES=[
 {'pageTitle':'週次報告を短く伝える','contentMarkdown':'# 週次報告を短く伝える\n結論 → 変化 → 相談\n架空の小チーム「青葉制作」の報告例','designBrief':'白地に濃紺の大見出しを左上へ。下段に三語を横一列、細い矢印で順序を示す。アクセントは青緑一色。余白を広く取り、カード・写真・装飾アイコンを置かない。日本語文字を編集可能なテキストとして保持。','narration':'聞き手が次の判断をできるよう、結論、前週からの変化、相談の順に伝えます。架空のチームの例で流れを確認します。'},
 {'pageTitle':'最初に、今の状態','contentMarkdown':'# 最初に、今の状態\n今週：遅れあり\n素材の受け取り待ち','designBrief':'同じ白・濃紺・青緑の体系。見出しを左上、遅れありを中央左へ大きく置く。原因を直下に小さく。状態を色だけで表現しない。余計な図表を加えない。','narration':'作業の経緯より先に、今週は遅れがあると伝えます。今回の理由は素材の受け取り待ちです。'},
 {'pageTitle':'前週からの変化だけ','contentMarkdown':'# 前週からの変化だけ\n完了：画面案の確認\n未完了：素材の受け取り','designBrief':'見出しの下に二行の整列リスト。完了と未完了を同じ文字サイズで対比し、細い横罫線だけで区切る。証拠のない達成率や棒グラフを作らない。','narration':'画面案の確認は完了し、素材の受け取りが残っています。すべての作業履歴を読む代わりに、前週との差を示します。'},
 {'pageTitle':'相談は、期限と選択肢で','contentMarkdown':'# 相談は、期限と選択肢で\n木曜までに判断したい\nA：仮素材で進める\nB：素材を待ち、日程を見直す','designBrief':'木曜までに判断したいを見出し直下で強調。AとBを左右のカラムへ置き、同等の重みで比較。角丸カードを使わず、余白と中央の細線で分ける。','narration':'木曜までの判断を依頼します。仮素材で進めるか、素材を待って日程を見直すか、選択肢をそろえて相談します。'},
 {'pageTitle':'次の行動で、報告を閉じる','contentMarkdown':'# 次の行動で、報告を閉じる\n担当・期限・確認方法をそろえる\n短さより、次に動けること','designBrief':'濃紺の背景と白文字で締める。左揃えの見出しを最も大きく、担当・期限・確認方法をその下に配置。最後の一文は青緑で控えめに。情報を追加しない。','narration':'判断のあとに、誰がいつまでに何をするかを記録します。短くすることだけでなく、次の行動が分かる報告を目指します。'},
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'input').mkdir(exist_ok=True);(OUT/'source').mkdir(exist_ok=True)
 node=shutil.which('node');command=[node,'--test','tests/plugin.test.mjs']
 r=subprocess.run(command,cwd=UP,capture_output=True,text=True,encoding='utf-8',errors='replace')
 (OUT/'source/plugin-test.log').write_text(json.dumps(command)+'\n'+r.stdout+r.stderr,encoding='utf-8')
 refs=[{'path':p,'sha256':sha(UP/p),'url':f'https://github.com/StarryKit/starry-slides/blob/{COMMIT}/{p}'}for p in REFS]
 save(OUT/'input/authoring-plan.json',{'title':'週次報告を短く伝える','language':'ja','fictional':True,'status':'prepared_not_submitted','pages':PAGES,'note':'No document/profile IDs invented. This is a content/design plan, not a complete or submitted Hosted MCP request.'})
 (OUT/'PROMPT.md').write_text('架空の小チーム「青葉制作」向けに、週次報告を短く伝える日本語5ページを準備する。各ページは一論点とし、原典Skillに従ってcontentMarkdownとdesignBriefを分離する。外部API禁止のためHosted MCPへの投入・生成・exportは行わない。',encoding='utf-8')
 (OUT/'NOTES.md').write_text('\n\n'.join(f'{i}. {p["pageTitle"]}\n{p["narration"]}'for i,p in enumerate(PAGES,1)),encoding='utf-8')
 shutil.copyfile(UP/'LICENSE',OUT/'LICENSE')
 record={'repository':'StarryKit/starry-slides','commit':COMMIT,'license':'MIT','production_status':'blocked','execution_status':'preflight_complete_generation_not_run','blocker':'Fixed commit is starrykit-plugin v0.4.0, containing client manifests/Skill/docs/demo media only. Authoring/render/export are Hosted MCP services requiring external API and OAuth, excluded by task.','source_refs':refs,'original_sources_modified':False,'local_test':{'command':command,'exit_code':r.returncode,'log':'source/plugin-test.log','scope':'Repository integrity only; not OAuth, service health, generation, render or export.'},'prepared_pages':5,'generated_pages':0,'external_api_calls':0,'native_navigation_api':None,'wrapper_created':False,'qa':{'status':'not_run_generation_not_completed','rendered_pages':0,'visual_reviewed_pages':0},'legacy_branch':'archive/starry-slides-v0.1.38 (not acquired, not substituted for pinned commit)','assets':'No demo or brand image reused. Root MIT confirmed; no additional LICENSE file found.'}
 save(OUT/'ATTEMPT.json',record);save(OUT/'QA.json',record['qa'])
 (OUT/'README.md').write_text('# StarryKit 固定版の実行条件\n\n固定commitはローカルスライドアプリではなく、Hosted MCP用のMITプラグインです。原典Skillを読んで日本語5ページ分の本文・デザイン指示・講稿を準備し、原典nodeテストだけを実行しました。スライド生成は0ページです。\n\n生成にはStarryKitのHosted MCP接続とユーザーOAuth、その環境でのformat取得・document作成・insert_pages・job追跡・ユーザーDraft受諾が必要です。今回の外部API禁止により実行しません。未確認の料金や無料利用条件は推測していません。\n\n旧アプリは別のarchive branchですが、指定commitの代用にはしていません。ローカルCLI、公開ページ移動API、HTML wrapperは存在するものとして扱っていません。日本語の原稿はinput/authoring-plan.jsonに保存。原典HTML exportのlanguage列挙はen-US/zh-CNのみで、日本語本文のexport品質も未検証です。\n',encoding='utf-8')
 save(ROOT/'data/starry-repository-examples.json',[])
 save(ROOT/'data/starry-repository-guides.json',[{'repository':'StarryKit/starry-slides','production_status':'blocked','execution_status':record['execution_status'],'execution_type':'original_plugin_integrity_test_only','case_ids':[],'summary_ja':'固定版はMITのHosted MCP用プラグイン。原典テストと日本語5ページ原稿を準備済みだが、外部API必須のため生成0ページ。','requirements':['StarryKit Hosted MCP接続とユーザーOAuth','外部サービスの利用許可と利用条件確認','ユーザーによるPage Draftの受諾'],'steps':['get_profile_catalogで現行形式を取得','create_document/read_document','ページ別contentMarkdown/designBriefをinsert_pagesへ渡す','jobをterminalまで追跡し全ページpreview、ユーザーDraft受諾後にexport'],'commands':['python tools/build_starry_repository_example.py（ローカル原典テストと原稿の準備のみ）'],'source_refs':refs,'evidence':'examples/repositories/starry-slides/ATTEMPT.json','limitations':['ローカルrenderer/テンプレート/生成CLIは固定commitに含まれない。','原典テストの成功は生成・再生・exportの成功を示さない。','旧archive branchは指定原典の代用にしない。']}])
 print(json.dumps({'exit_code':r.returncode,'generated_pages':0,'status':record['execution_status']}))
if __name__=='__main__':main()
