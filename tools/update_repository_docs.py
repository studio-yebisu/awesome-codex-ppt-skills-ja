"""Refresh produced-repository tables without touching the original 209-entry catalog."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def main():
 cases=load('data/case-studies.json');ledger=load('data/production-ledger.json')
 n=ledger['produced_repository_count'];books=len(cases);pages=sum(c['page_count'] for c in cases)
 native=[c for c in cases if c['format']=='pptx' and c.get('editability')!='raster_slides']
 raster=[c for c in cases if c.get('editability')=='raster_slides'];web=[c for c in cases if c['format']=='html']
 def total(items):return sum(c['page_count'] for c in items)
 p=ROOT/'README.md';s=p.read_text(encoding='utf-8');intro,original=s.split('以下の原版比較と209件一覧は、',1)
 intro=re.sub(r'\*\*\d+リポジトリで制作した\d+冊・\d+枚を掲載しています。\*\*',f'**{n}リポジトリで制作した{books}冊・{pages}枚を掲載しています。**',intro)
 intro=re.sub(r'残る\d+件',f"残る{ledger['remaining_repository_count']}件",intro)
 intro=re.sub(r'## 実際に制作した\d+リポジトリ',f'## 実際に制作した{n}リポジトリ',intro)
 start=intro.index('| 原典リポジトリ |');end=intro.index('\n\n',start)
 rows=['| 原典リポジトリ | 出力と冊数 | 全ページ再生 | 使い方と派生 |','|---|---|---|---|']
 for repo in dict.fromkeys(c['repository'] for c in cases):
  works=[c for c in cases if c['repository']==repo];c=works[0]
  fmt='画像主体PPTX' if c.get('editability')=='raster_slides' else '編集可能PPTX' if c['format']=='pptx' else '固有HTML'
  play='・'.join(f"[{w['page_count']}枚](http://127.0.0.1:8847/case.html?id={w['id']})" for w in works)
  rows.append(f"| [{repo}](https://github.com/{repo}) | {fmt}／{len(works)}冊 | {play} | [日本語ガイド](repository.html?repo={repo})・[派生SKILL](skill-forks/{c['fork_id']}/SKILL.md) |")
 intro=intro[:start]+'\n'.join(rows)+intro[end:]
 intro=re.sub(r'編集可能なPPTXは\d+冊\d+枚、画像主体のPPTXは\d+冊\d+枚、各リポ固有のHTMLは\d+冊\d+枚',f'編集可能なPPTXは{len(native)}冊{total(native)}枚、画像主体のPPTXは{len(raster)}冊{total(raster)}枚、各リポ固有のHTMLは{len(web)}冊{total(web)}枚',intro)
 intro=re.sub(r'PPTX\d+冊\d+枚はMicrosoft',f'PPTX{len(native)+len(raster)}冊{total(native)+total(raster)}枚はMicrosoft',intro)
 intro=re.sub(r'全\d+ページを実表示',f'全{pages}ページを実表示',intro)
 intro=re.sub(r'\d+冊の対応データ',f'{books}冊の対応データ',intro)
 intro=re.sub(r'成功した\d+リポ',f'成功した{n}リポ',intro)
 p.write_text(intro+'以下の原版比較と209件一覧は、'+original,encoding='utf-8',newline='\n')
 p=ROOT/'docs/QA.md';s=p.read_text(encoding='utf-8')
 s=re.sub(r'\d+リポジトリ、\d+冊、\d+枚。編集可能PPTX \d+冊\d+枚、画像主体PPTX \d+冊\d+枚、固有HTML \d+冊\d+枚。',f'{n}リポジトリ、{books}冊、{pages}枚。編集可能PPTX {len(native)}冊{total(native)}枚、画像主体PPTX {len(raster)}冊{total(raster)}枚、固有HTML {len(web)}冊{total(web)}枚。',s)
 s=re.sub(r'残\d+件',f"残{ledger['remaining_repository_count']}件",s)
 start=s.index('| 事例別QA記録 |');end=s.index('\n\n',start)
 qa_rows=['| 事例別QA記録 | 原典リポジトリ | 枚数 | 出力 |','|---|---|---:|---|']
 for c in cases:
  fmt='画像PPTX' if c.get('editability')=='raster_slides' else '編集可能PPTX' if c['format']=='pptx' else 'HTML'
  qa_rows.append(f"| [{c['id']}](../{c['qa']}) | {c['repository']} | {c['page_count']} | {fmt} |")
 s=s[:start]+'\n'.join(qa_rows)+s[end:]
 s=re.sub(r'全\d+ページの目視確認',f'全{pages}ページの目視確認',s)
 s=re.sub(r'PowerPointで開いた\d+枚',f'PowerPointで開いた{total(native)+total(raster)}枚',s)
 s=re.sub(r'HTML\d+枚は固有ランタイム',f'HTML{total(web)}枚は固有ランタイム',s)
 s=re.sub(r'先行6冊45枚と追加native PPTX4冊25枚、画像PPTX3枚を.*?合わせて\d+枚となる。','先行6冊45枚に、上表の原典別制作を追加している。新規PPTXは実ファイルのPowerPoint描画、HTMLは原典ランタイムの実表示を確認する。',s)
 s=re.sub(r'\d+派生版と\d+配布ファイル',f"{n}派生版と{len(load('data/case-downloads.json'))}配布ファイル",s)
 kit_tests=load('data/reproduction-kit-qa.json')['tests']
 kit_results='、'.join(t['repository'].split('/')[-1]+str(t['pages'])+'枚' for t in kit_tests)
 kit_summary=f"{n}派生版と{len(load('data/case-downloads.json'))}配布ファイルの内容・SHAを検査。[別フォルダー再現](../data/reproduction-kit-qa.json)では、配布ZIPを新しいフォルダーへ展開し新venvから{len(kit_tests)}形式（{kit_results}）の生成に成功。他キットの独立実行や、全リポの再現確認へ読み替えない。再生成した出力は確認前として扱う。"
 s=re.sub(r'\d+派生版と\d+配布ファイルの内容・SHAを検査。\[別フォルダー再現\].*?(?=\n\n)',kit_summary,s)
 s=re.sub(r'\d+リポの成功数',f'{n}リポの成功数',s)
 report=load('data/release-qa.json')
 if report['status']=='passed' and report['case_count']==books:
  final=f"**最終自動検査：{report['passed_checks']}項目通過、問題0件。**"
 else:final='**最終自動検査：今回の統合後の実行待ち。**'
 s=re.sub(r'\*\*最終自動検査：.*?\*\*',final,s)
 p.write_text(s,encoding='utf-8',newline='\n')
 p=ROOT/'docs/出典とライセンス.md';s=p.read_text(encoding='utf-8')
 s=re.sub(r'\d+原典から\d+冊の日本語資料と\d+派生版を制作',f'{n}原典から{books}冊の日本語資料と{n}派生版を制作',s)
 s=re.sub(r'当地で生成した\d+冊',f'当地で生成した{books}冊',s)
 p.write_text(s,encoding='utf-8',newline='\n')
 print(f'Documents refreshed for {n} repositories / {books} decks / {pages} pages; original catalog preserved')
if __name__=='__main__':main()
