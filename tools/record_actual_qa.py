"""Record only the browser checks already performed in this task."""
from pathlib import Path
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parents[1]
examples=json.loads((ROOT/'data/actual-examples.json').read_text(encoding='utf-8'))
for e in examples:
    folder=(ROOT/e['html']).parent
    qa=dict(checked_on='2026-10-13',repository=e['repository'],commit=e['commit'],html_sha256=sha256((folder/'index.html').read_bytes()).hexdigest(),
      browser='Codex in-app browser',visual_pages_reviewed=4,catalog_next_page_checked=True,
      viewports=[[1280,720],[393,852]],scope='rendered source presentation and catalog player',
      unverified=['PowerPoint application display','full Guizang presenter feature set','iframe-body Escape input','all 209 generation workflows'])
    (folder/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    file=folder/'PROVENANCE.json';record=json.loads(file.read_text(encoding='utf-8'));record['qa_status']='browser_preview_reviewed';record['browser_qa']='QA.json'
    file.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows='\n'.join(f'| [{e["repository"]}](https://github.com/{e["repository"]}) | {e["method_label"]} | [制作記録](../{e["proof"]}) | {e["slide_count"]}枚 |' for e in examples)
(ROOT/'docs/制作記録.md').write_text('# 該当スキルを使った日本語の実制作\n\n209件の原典に対応した3件・12枚。共通の独自レンダラーによる旧6デッキは含めない。\n\n| 掲載スキル | 制作方法 | 原典・改変・再生成 | 枚数 |\n|---|---|---|---:|\n'+rows+'\n\n各作例のPROVENANCE.jsonに固定コミットと使用した元ファイルのハッシュ、QA.jsonに実表示の確認範囲を記録。PPT Masterは元変換器によるネイティブPPTXで、ブラウザーは入力SVGをプレビューする。書体警告とPPTXアプリ未検証を保持する。\n\n現在の確認は[QA.md](QA.md)、不採用試作は[withdrawn-prototypes.md](withdrawn-prototypes.md)を参照。\n',encoding='utf-8')
print('Recorded 3 already-reviewed examples and their exact HTML hashes')
