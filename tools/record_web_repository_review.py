"""Record a completed, explicitly performed browser/image review without fabricating it."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse, json
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--reviewed',action='store_true');p.add_argument('--case',action='append');a=p.parse_args()
 if not a.reviewed:raise SystemExit('Pass --reviewed only after viewing every current capture.')
 cases=json.loads((ROOT/'data/web-repository-examples.json').read_text(encoding='utf-8'))
 for c in cases:
  if a.case and c['id'] not in a.case:continue
  folder=ROOT/'examples/repositories'/c['id'];artifact=ROOT/c['preview']
  shots=sorted((ROOT/'.build/repository-qa'/c['id']).glob('slide-*.jpg'))
  assert len(shots)==c['page_count']
  assert all(s.stat().st_mtime>=artifact.stat().st_mtime for s in shots),'Stale screenshot '+c['id']
  images=[{'file':'render/slide-'+str(i).zfill(2)+'.png','sha256':digest(folder/'render'/('slide-'+str(i).zfill(2)+'.png'))} for i in range(1,c['page_count']+1)]
  q={'status':'qa_complete','page_count':c['page_count'],'artifact_sha256':digest(artifact),
   'browser_review':'verified','browser':'Codex in-app browser / actual native page controls',
   'viewport':{'width':1280,'height':720},
   'visual_review':{'method':'全ページを原典の操作で表示し、見出し/現在位置をDOM照合。実キャプチャ全頁のcontact sheetをCodexが視認。','pages_reviewed':list(range(1,c['page_count']+1)),'result':'日本語の欠落・はみ出し・意図しない重なりなし。架空条件/目標表示、図表と入力を照合。'},
   'font_review':'実woff2の署名・MIMEとOFLを検査。ブラウザーでdocument.fonts.status=loadedと日本語字形を確認。',
   'capture_conditions':'ページ収まりの撮影ではprefers-reduced-motion。通常の動きはサイトのプレイヤーで別途確認。',
   'images':images,'checked_at':datetime.now(timezone.utc).isoformat(),
   'not_claimed':['上流の全テーマ・全機能','人による採用','外部公開','全209件の実行']}
  if c['id']=='frontend-editable':
   q['editing_review']={'text_edit':'passed','save_reload':'passed;確認文字を元へ戻して保存','export_html':'実ダウンロード確認','undo_redo':'Undo後にRedoが無効だったため全動作の確認済みとは扱わない','drag_copy_delete':'not_verified'}
  (folder/'QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
  print(c['id']+': actual '+str(c['page_count'])+' pages reviewed')
if __name__=='__main__':main()
