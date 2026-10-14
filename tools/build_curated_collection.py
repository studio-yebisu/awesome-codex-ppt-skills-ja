"""Select useful, produced skills and provide short, standalone Japanese entries."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).resolve().parents[1]
SELECTION = [
    ('zarazhangrui/frontend-slides','動きで魅せるWebスライド','motion','sol-motion-showcase','固定ステージとSVGで、大きな日本語タイポを動かす。'),
    ('likaku/Mck-ppt-design-skill','編集誌のようなPowerPoint','editorial','sol-editorial-showcase','公式エンジンを活かし、文字と図形を編集できる誌面へ。'),
    ('HututuWorks/sci-diagram-pptx','編集できる科学の概念図','diagram','sci-diagram-showcase','原典のnative図解ルールで、矢印と注釈まで編集できる教材へ。'),
    ('Hasasasa/html-to-editable-pptx','HTMLから文字と図形のPPTXへ','editorial','html-editable-showcase','原典CLIで日本語HTMLを変換し、編集できるブランド資料へ。'),
    ('ABYR1206/claude-skill-hand-drawn-slides','手描きイラストの章扉','editorial','hand-drawn-showcase','原典SVGと組版レシピで、章のはじまりを親しみのある一枚に。'),
    ('op7418/guizang-ppt-skill','雑誌とSwissのレイアウト','editorial','port-town','原典テンプレートで、企画を余白とグリッドに落とし込む。'),
    ('crazyykhllc-bit/CyberPPT','情報を整理するPPTX','work','cyberppt','原典の内容設計を活かし、文字と図形を編集できる資料へ。'),
    ('gongnyang/awesome-html-scrolline-deck','スクロールで語る企画','motion','html-scrolline','横断する図形と流れで、体験を一つのストーリーに。'),
    ('code-on-sunday/slide-deck-generator','Reactで育てるスライド','motion','react-slide-deck','コードでレイアウトと動きを扱えるWeb制作。'),
    ('hugohe3/ppt-master','編集できる日本語PPTX','work','cafe-pptx','公式ツールの文字・図形・ノートで、提案を仕上げる。'),
    ('gonta223/japanese-corporate-pptx-skill','日本語の業務資料','work','japanese-corporate','日本語の単位と情報量を整えた業務スライド。'),
    ('ConnorRX56/presentation-delivery-skills','HTMLから編集できるPPTX','work','presentation-delivery','原典の変換器で、Web原稿を編集可能なPowerPointへ。'),
    ('prodigeproject/pradaslides','構成から仕上げるPowerPoint','work','pradaslides','ページ設計と原典ワークフローで、伝わる順序を作る。'),
    ('GongRzhe/Office-PowerPoint-MCP-Server','MCPでPowerPointを作る','work','office-powerpoint-mcp','実際のMCP操作でスライドと図表を組み立てる。'),
    ('joeseesun/qiaomu-bento-ppt','Bentoで整理する提案','diagram','qiaomu-bento','原典のshellとグリッドで情報の優先順位を見せる。'),
    ('touying-typ/seaslides','構成から組むWebスライド','diagram','seaslides','原典のTCSとHTMLコンパイラーで、話の順番を資料へ。'),
    ('minorun365/minorun-marp-skill','Markdownで育てる資料','work','minorun-marp','原稿を短く書き、Marpの原典テーマで発表資料へ。'),
    ('sunchaokun/PPT-Design-Skill','企画をビジュアルにする','editorial','ppt-design-skill','元スキルの制作方式を、日本語の企画提案へ。'),
    ('att6113/ppt-design-system','デザインを揃えるPPTX','work','ppt-design-system','原典のデザインシステムで、資料の基準を揃える。'),
    ('EveryInc/hands-on-deck','JSONで編集するPowerPoint','work','hands-on-deck','原典CLIの編集指示で、文字・図形・図表を組み立てる。'),
    ('ningzimu/image-to-editable-ppt-skill','画像から編集できる図へ','diagram','image-to-editable','再構成した文字や図形を、あとから編集できる形に。'),
    ('ningzimu/codex-ppt-skill','画像で伝えるスライド','editorial','codex-image-ppt','原典の画像制作方式を活かした日本語の図解。'),
    ('addsumtech/slides_maker','図表を組めるPPTX','diagram','slide-maker','原典deckkitの図表と文字で、編集可能な資料を作る。'),
    ('minhnv0807/ai-business-skills','正方形のカルーセル','editorial','business-carousel','短いページをつないで伝える日本語カルーセル。'),
    ('daniel-style/magic-slide','すばやく作るWebスライド','motion','magic-slide','原典テンプレートを使い、企画を再生できる資料へ。'),
    ('ryanbbrown/revealjs-skill','ブラウザーで発表する','motion','revealjs-skill','Reveal.jsの原典構成で、ブラウザー発表を始める。')
]

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def dump(path,value): (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def skill_text(entry,profile,case):
    repo=entry['repository']; commit=profile['upstream_commit']
    refs=profile.get('source_refs') or profile.get('skill_paths') or []
    paths=[r if isinstance(r,str) else r.get('path','') for r in refs]
    paths=list(dict.fromkeys(p for p in paths if p))[:8]
    links='\n'.join('- https://github.com/'+repo+'/blob/'+commit+'/'+p for p in paths if not p.startswith('examples/'))
    legal_links='\n'.join('- https://github.com/'+repo+'/blob/'+commit+'/'+p for p in profile.get('license_paths',[]) if not p.startswith('examples/'))
    requirements='\n'.join('- '+str(r) for r in profile.get('requirements',[])[:6])
    method=profile.get('method_ja') or case['method']
    recipe_notes='\n'.join('- '+v for v in profile.get('recipe_notes',[]))
    return f'''---
name: {case['fork_id']}-entry
description: {entry['title_ja']}を日本語で制作するときに使う。{repo}の原典方式を使い、作例の作風を自分の題材へ展開する。
---

# {entry['title_ja']}

Studio Yebisuの日本語制作指示。原作者の公式翻訳ではありません。

## 元の方式で作る

原典: https://github.com/{repo}/tree/{commit}

{links}

{method}

このMarkdownは指示本文です。実装・テンプレートを内包しません。上の固定原典から必要ファイルを読むか、サイトの「一式ZIP」から日本語派生と原典を取得してから制作する。別の汎用rendererへ置き換えて、この原典の作例と呼ばない。

## 必要なもの

{requirements or '- 原典の方式を実行できるコーディングエージェントと依存環境。'}

{recipe_notes}

## 日本語で魅力ある資料へ

1. 読者、目的、最後に伝えたいこと、形式を決める。入力の数字・単位・出典を維持する。架空の企画はそう表示する。
2. 原典のテンプレート・controller・生成器に沿って構成する。日本語見出しは意味の区切りで改行し、本文を詰め込まない。
3. 見出し・本文・英数字の書体を分ける。誌面はShippori Mincho × Zen Kaku Gothic New × Manrope、動く資料はZen Kaku Gothic New × Space Groteskがこのサイトの推奨。公式OFL配布物を使い、条件を保持する。
4. 大胆な表紙、余白、大きな図形・数字、ページごとの構図の変化を作る。角丸カードをただ繰り返さない。Webの動きは主張を順に見せるために使う。
5. 原典方式で実ファイルを生成する。主要な出力が開くことと明白な欠けだけ確認し、必要な箇所を直す。

## この作例を自分の題材へ

作例: {case['title']}

{case['prompt_text']}

上の施設名・企画・数値を、自分の入力に置き換える。生成方法の変更は短く記す。完成資料と必要な入力・制作ソースを渡す。

## 帰属と配布条件

原作者: {repo.split('/')[0]} / 原典条件: {profile.get('license') or '個別条件'}

{legal_links}

{profile.get('license_note','原文LICENSE・NOTICEと素材・依存物の条件を保持する。')}

サイトのカタログ条件を、原典コードや書体の再許諾に用いない。詳細な実装と原文条件は一式ZIPまたは固定原典を参照する。
'''

if __name__=='__main__':
    cases=load('data/case-studies.json'); by_case={c['id']:c for c in cases}
    profiles={p['repository']:p for p in load('data/repository-guides.json')}
    exclusions=load('data/product-exclusions.json')['excluded'] if (ROOT/'data/product-exclusions.json').exists() else []
    excluded_repos={e['repository'] for e in exclusions}
    entries=[]
    out=ROOT/'downloads/skills';out.mkdir(parents=True,exist_ok=True)
    for repo,title,style,case_id,description in SELECTION:
        if repo in excluded_repos:continue
        if case_id not in by_case:continue
        case=by_case[case_id];profile=profiles[repo]
        entry={'repository':repo,'title_ja':title,'description_ja':description,'style':style,'featured_case_id':case_id,'skill_download':'downloads/skills/'+case['fork_id']+'.md','fork_download':case.get('fork_download'),'license':profile.get('license')}
        (ROOT/entry['skill_download']).write_text(skill_text(entry,profile,case),encoding='utf-8')
        entries.append(entry)
    active_case_ids=[e['featured_case_id'] for e in entries]
    dump('data/product-collection.json',{'updated_at':'2026-10-14','title':'Studio Yebisu AIスライドアトリエ','policy':'原典方式で制作した実例から選ぶ日本語の厳選スキル集','archive':'data/skills.json','entries':entries,'active_case_ids':active_case_ids,'excluded':exclusions})
    with ZipFile(ROOT/'downloads/yebisu-japanese-skill-entries.zip','w',ZIP_DEFLATED) as z:
        for e in entries:z.write(ROOT/e['skill_download'],Path(e['skill_download']).name)
        z.writestr('README.md','日本語の指示本文集です。各本文の固定原典と個別ライセンスを参照してください。実装・原文LICENSEはサイトの一式ZIPから別途取得できます。\n')
    print(f'{len(entries)} curated skills and direct Markdown downloads built')
