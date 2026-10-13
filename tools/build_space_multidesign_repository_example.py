"""Local-only trial. Upstream has no redistribution license; never package its viewer."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / '.build/actual-upstreams/SpaceZephyr__space-multi-design-ppt'
OUT = ROOT / '.build/local-trials/space-multidesign'
PUBLIC = ROOT / 'examples/repositories/space-multidesign'
COMMIT = '44c2f34b1d83022ca1d0dd5e28d772beea1184bd'
TITLE = '予約キャンセルを減らすには'
NOTES = [
    '架空の小規模サロン「こもれび」の運用案です。効果は未検証で、まず一週間の試行と記録を提案します。',
    '予約忘れ、変更方法の分かりにくさ、店舗の対応遅れを仮説として分けます。実際の原因は記録で確かめます。',
    '確認文には日時、変更連絡先、返信が必要かを明記します。個人情報を含まない架空例です。',
    '担当者が確認、変更受付、記録を引き継げるようにします。店舗の営業日と受付時間に合わせて実施時点を調整します。',
    '一週間では効果を断定しません。件数と理由、対応負担を見て、次週に続ける運用を選びます。',
]
CSS = '''*{box-sizing:border-box}html,body{margin:0;width:1280px;height:720px;overflow:hidden}body{background:#faf9f5;color:#181715;font-family:"Noto Sans JP","Yu Gothic",sans-serif}main{padding:72px 96px;height:720px}h1,h2{font-family:"Noto Serif JP","Yu Mincho",serif;font-weight:400;letter-spacing:-1px;margin:20px 0 32px;line-height:1.2}h1{font-size:64px}h2{font-size:48px}h3{font-size:27px;line-height:1.5;margin:18px 0}p{font-size:23px;line-height:1.7;margin:12px 0}.eyebrow{font-size:18px;letter-spacing:2px;color:#6c6a64}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px}.card{background:#f5f0e8;border:1px solid #e6dfd8;border-radius:12px;padding:28px}.card p{font-size:21px}.num{color:#cc785c;font-family:Georgia,serif;font-size:48px}.accent{color:#cc785c}.muted{color:#6c6a64}.message{background:#f5f0e8;border-left:5px solid #cc785c;padding:26px 36px;margin-top:20px}.message p{font-size:25px}.dark{background:#141413;color:#faf9f5}.dark .muted{color:#c7c0b7}'''
PAGES = [
    '<div class="eyebrow">こもれび / 小規模サロンの運用案</div><h1>予約キャンセルを<br>減らすには</h1><p class="accent">忘れにくく、変更しやすく。</p><p class="muted">予約確認・変更受付・記録を整える<br>架空の店舗を使った、未検証の提案</p>',
    '<div class="eyebrow">原因は、まだ仮説</div><h2>連絡の途中で、何が起きるか</h2><div class="grid"><div class="card"><span class="num">01</span><h3>予約を忘れる</h3><p>日時を思い出す<br>きっかけがない。</p></div><div class="card"><span class="num">02</span><h3>変更先が分からない</h3><p>どこに連絡すれば<br>よいか迷う。</p></div><div class="card"><span class="num">03</span><h3>対応が遅れる</h3><p>変更連絡を<br>担当者が見落とす。</p></div></div>',
    '<div class="eyebrow">確認文の例 / 架空の予約</div><h2>日時と変更方法を、一通に</h2><div class="message"><p>こもれび：ご予約の確認です。<br>10月20日（火）14:00からお待ちしています。<br>変更をご希望の場合は、このメッセージに<br>ご返信ください。受付時間は10:00〜18:00です。<br>ご変更がなければ返信は不要です。</p></div><p class="muted">送信時点と受付時間は、店舗の運用に合わせる。</p>',
    '<div class="eyebrow">担当者が変わっても、同じ流れで</div><h2>確認・受付・記録をつなぐ</h2><div class="grid"><div class="card"><span class="num">01</span><h3>前営業日に確認</h3><p>予約一覧を見て、<br>確認文を送る。</p></div><div class="card"><span class="num">02</span><h3>変更を受け付ける</h3><p>受付時間内に確認し、<br>変更内容を返す。</p></div><div class="card"><span class="num">03</span><h3>結果を記録する</h3><p>件数・理由・対応を<br>同じ欄に残す。</p></div></div>',
    '<div class="eyebrow">まずは一週間、試して記録する</div><h1>続けられる形を、<br>記録から選ぶ。</h1><p>予約件数 ／ キャンセル件数 ／ 分かった理由</p><p>連絡にかかった時間 ／ 受付で困ったこと</p><p class="muted">短期間の変化だけで効果を断定しない。<br>翌週は、負担の少ない改善を一つ選ぶ。</p>',
]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def run(args):
    r = subprocess.run([sys.executable, *map(str,args)], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    with (OUT/'execution.log').open('a',encoding='utf-8') as f: f.write(json.dumps([sys.executable,*map(str,args)],ensure_ascii=False)+'\n'+r.stdout+r.stderr+'\n')
    if r.returncode: raise RuntimeError(r.stderr or r.stdout)

def finalize(reviewed):
    refs = [{ 'path':p, 'sha256':sha(UP/p), 'url':f'https://github.com/SpaceZephyr/space-multi-design-ppt/blob/{COMMIT}/{p}'} for p in ['SKILL.md','README.md','scripts/build_deck.py','scripts/export_deck.py','references/slide-html-guide.md','examples/chengzhou-coffee-claude/design-tokens.md']]
    pngs = sorted((OUT/'render').glob('*.png'))
    record = {'repository':'SpaceZephyr/space-multi-design-ppt','commit':COMMIT,'execution_status':'local_trial_generated_not_packaged','production_status':'blocked','blocker':'No LICENSE or redistribution grant found at fixed commit. Original viewer remains exclusively under ignored .build/local-trials; no distributable example or source kit.','license':None,'source_refs':refs,'artifact_type':'html','pages':5,'local_trial_path':'.build/local-trials/space-multidesign','commands':['original scripts/build_deck.py slides --output deck.html','original scripts/export_deck.py slides --pdf deck.pdf --keep-pngs render'],'original_sources_modified':False,'api_calls':0,'qa':{'status':'local_visual_review_complete' if reviewed else 'awaiting_visual_review','render_engine':'Original exporter / Playwright 1.63.0 / Chromium headless shell 1243','png_count':len(pngs),'all_pages_visually_reviewed':reviewed,'notes_count':len(NOTES),'artifacts':{str(p.relative_to(OUT)):sha(p) for p in [OUT/'deck.html',OUT/'deck.pdf',*pngs]},'browser_navigation':json.loads((OUT/'browser-check.json').read_text()) if (OUT/'browser-check.json').exists() else None},'adjustments':['Locally supplied upstream example design tokens; no live brand scraping or claim of current official brand template.','Five original Japanese HTML pages authored under upstream 1280x720 slide contract; upstream builder and exporter executed unchanged.','HTML is primary output; PDF is raster. No editable PPTX claim.']}
    save(PUBLIC/'ATTEMPT.json',record)
    save(ROOT/'data/spacemulti-repository-examples.json',[])
    save(ROOT/'data/spacemulti-repository-guides.json',[{'repository':record['repository'],'execution_type':'original_html_builder_and_exporter_local_trial','execution_status':record['execution_status'],'production_status':'blocked','case_ids':[],'summary_ja':'原典のHTML結合・Chromium書き出しで日本語5ページをローカル生成。固定commitに配布ライセンスがなく、原典runtimeを含むHTMLと再現ZIPは公開しない。','requirements':['Python / Playwright 1.63.0 / Chromium 1243 / Pillow','配布条件の確認と許諾が必要'],'steps':['固定commitの原典をローカル取得','原典の1280×720規約と同梱トークンから日本語HTMLを執筆','原典build_deck.pyとexport_deck.pyを実行','全ページを視認。配布条件未確認のためローカル試作として保管'],'commands':['python tools/build_space_multidesign_repository_example.py'],'source_refs':refs,'evidence':'examples/repositories/space-multidesign/ATTEMPT.json','limitations':['公開・配布できる成功例には数えない。','著作物を含む原典viewer、画像、PDF、HTMLは.buildのローカル試作だけに保管。']}])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--finalize-only',action='store_true');ap.add_argument('--reviewed',action='store_true');a=ap.parse_args()
    if not a.finalize_only:
        (OUT/'slides').mkdir(parents=True,exist_ok=True);(OUT/'render').mkdir(exist_ok=True)
        for i,body in enumerate(PAGES,1):
            (OUT/'slides'/f'{i:02d}-slide.html').write_text(f'<!doctype html><html lang="ja"><meta charset="utf-8"><title>{TITLE}</title><style>{CSS}</style><body class="'+('dark' if i==5 else '')+f'"><main>{body}</main></body></html>',encoding='utf-8')
        save(OUT/'input.json',{'title':TITLE,'fictional':True,'assumptions':'改善効果は未検証。原因は仮説。架空店舗・予約。','notes':NOTES})
        (OUT/'NOTES.md').write_text('\n\n'.join(f'{i}. {n}' for i,n in enumerate(NOTES,1)),encoding='utf-8')
        run([UP/'scripts/build_deck.py',OUT/'slides','--output',OUT/'deck.html','--title',TITLE])
        run([UP/'scripts/export_deck.py',OUT/'slides','--pdf',OUT/'deck.pdf','--keep-pngs',OUT/'render'])
    finalize(a.reviewed)
if __name__=='__main__':main()
