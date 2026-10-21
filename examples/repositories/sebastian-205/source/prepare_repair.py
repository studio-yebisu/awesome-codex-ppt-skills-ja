"""Repair evidence before rebuilding; uses unchanged original preflight."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys

CASE = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

cmd=[sys.executable, str(CASE/'source/upstream-scripts/preflight.py'), str(CASE/'input/BRIEF.md'), '--output', str(CASE), '--json']
result=subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
receipt={'command':['python','source/upstream-scripts/preflight.py','input/BRIEF.md','--output','.','--json'], 'exit_code':result.returncode, 'result':json.loads(result.stdout), 'stderr':result.stderr}
dump(CASE/'source/preflight-repair.json', receipt)
assert result.returncode == 0 and receipt['result']['ok'], receipt
claims=[
 ('情報の問題', '家庭内在庫を一覧にするUIを提案し、「何があるか分からない」問題に対象を絞る。', '提案', '食品在庫を一目で把握できるUI／話者ノートの対象限定', '廃棄原因全体を解決する提案ではなく、食品ロス削減効果は未検証。'),
 ('利用場面', '買い物前・調理前・片づけ時の三場面で、表示が判断に使えるかを確かめる。', '研究の問い', '利用場面三つと「どの場面で見る価値があるか」の問い', '毎回アプリを開く価値があるかは確認していない。'),
 ('入力と精度', '場所別一覧と大まかな残量は、探しやすさと更新負担についての二つの仮説である。', '仮説', '仮説A／仮説B／記録精度との交換条件', '更新が続くという結果ではない。継続と正確さの両方を評価する計画。'),
 ('状態の区別', '提案UIでは、残量・更新時点・包装表示から転記する期限を分け、不明を隠さない。', '設計案', '食品名・残量・更新時点・期限未登録を区別する一覧', '表示例は架空。「未登録」は期限なしを意味せず、安全を保証しない。'),
 ('更新の操作', '選択→残量変更→保存場所確認の操作案に、取り消しと共有時の同意・権限を検討する。', '設計案', '三段階の操作と誤操作を戻す設計／共有の同意・権限', '操作の短さや共有設計の有効性を利用者で評価していない。'),
 ('評価の計画', '三課題を、観察・操作記録・振り返りで評価する計画である。', '評価計画', '食材を見つける／使う候補を選ぶ／残量を更新する課題と評価方法', '観察人数・実測値・評価結果はない。継続評価ではデータ最小化と別の同意が必要。'),
 ('限界', '未入力・更新忘れ・家族の利用により、画面の在庫と実物はずれうる。', '限界', '入力の欠落・更新忘れ・家族利用と実物／包装の確認', 'UIだけで食品ロス削減を証明できず、可食判断を自動化しない。'),
 ('次の試作', 'まず一つの棚を想定した試作で、一覧と更新が判断に使えるかを確かめる。', '次の計画', '棚を決める→試作→課題→修正。通知・レシピは後にする', '試作も利用者による検証も未実施。'),
]
rows=[dict(id=f'claim-{n:02d}', slide=n, topic=topic, claim=claim, claim_type=kind, source=f'input/BRIEF.md §{n}', evidence=detail, support='direct-proposal-in-fictional-notes', source_sufficiency='notes-only', caveat=caveat) for n,(topic,claim,kind,detail,caveat) in enumerate(claims,1)]
dump(CASE/'notes/claim-to-source.json',rows)
builder=CASE/'source/build.py'
old=builder.read_text(encoding='utf-8')
backup=CASE/'.private/build-before-evidence-repair.py'
if not backup.exists():
    backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(builder,backup)
if 'CLAIMS=' not in old:
    old=old.replace("P=Path(__file__).resolve().parents[1]", "P=Path(__file__).resolve().parents[1]\nCLAIMS=json.loads((P/'notes/claim-to-source.json').read_text(encoding='utf-8'))\nassert len(CLAIMS)==8 and [c['slide'] for c in CLAIMS]==list(range(1,9))\nassert all(c['source']==f\"input/BRIEF.md §{c['slide']}\" and c['claim'] and c['caveat'] for c in CLAIMS)")
    old=old.replace("'出典：架空の研究ノート  |  未実施・実測結果なし  |  入力 BRIEF / data.json',10", "f'出典：BRIEF §{n}  |  架空・未実施の研究計画  |  実測結果なし',11")
    old=old.replace('s.notes_slide.notes_text_frame.text=note', "c=CLAIMS[n-1]\n s.notes_slide.notes_text_frame.text=note+'\\n主張: '+c['claim']+'\\n出典: '+c['source']+'\\n資料の限界: '+c['caveat']")
    old=old.replace("prs.save(P/'deck.pptx')", "prs.save(P/'presentation_ja.pptx')\n(P/'deck.pptx').write_bytes((P/'presentation_ja.pptx').read_bytes())")
    old += "\n(P/'source'/'build-evidence.json').write_text(json.dumps({'source_sufficiency':'notes-only','claim_ledger_read_before_authoring':True,'claim_ledger_sha256':__import__('hashlib').sha256((P/'notes/claim-to-source.json').read_bytes()).hexdigest(),'primary_output':'presentation_ja.pptx','compatibility_alias':'deck.pptx','slides':8},ensure_ascii=False,indent=2)+'\\n',encoding='utf-8')\n"
    builder.write_text(old,encoding='utf-8')
subprocess.run([sys.executable,str(builder)],check=True)
dump(CASE/'source/repair-order.json',{'scope':'Repair run, not a claim about the historical first deck.', 'order':['unchanged original preflight','specific claim-to-source ledger','builder reads and validates ledger','native PPTX generation'], 'preflight':'source/preflight-repair.json','ledger_sha256':sha(CASE/'notes/claim-to-source.json'),'pptx_sha256':sha(CASE/'presentation_ja.pptx'),'structural_and_render_qa':'not run by this preparation script'})
print('Original preflight passed; 8 source-specific claims saved before native rebuild.')
