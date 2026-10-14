"""Select useful, produced skills and provide short, standalone Japanese entries."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SELECTION = [
    ('zarazhangrui/frontend-slides','動きで魅せるWebスライド','motion','sol-motion-showcase','固定ステージとSVGで、大きな日本語タイポを動かす。'),
    ('likaku/Mck-ppt-design-skill','編集誌のようなPowerPoint','editorial','sol-editorial-showcase','公式エンジンを活かし、文字と図形を編集できる誌面へ。'),
    ('HututuWorks/sci-diagram-pptx','編集できる科学の概念図','diagram','sci-diagram-showcase','原典のnative図解ルールで、矢印と注釈まで編集できる教材へ。'),
    ('Hasasasa/html-to-editable-pptx','HTMLから文字と図形のPPTXへ','editorial','html-editable-showcase','原典CLIで日本語HTMLを変換し、編集できるブランド資料へ。'),
    ('ABYR1206/claude-skill-hand-drawn-slides','手描きイラストの章扉','editorial','hand-drawn-showcase','原典SVGと組版レシピで、章のはじまりを親しみのある一枚に。'),
    ('SlideSpeak/slide-design-skill','自分のブランドをWeb資料へ','editorial','slidespeak-showcase','原典エンジンへ独自の書体・色・版式を渡して、緑の誌面を組む。'),
    ('liustack/pptwise','図解から組む編集できる企画書','diagram','pptwise-showcase','原典CLIの図形と構成を使い、拠点の関係を編集できるPPTXへ。'),
    ('Aham-AIAPP/aham-ppt','短い図解で伝えるワークショップ','diagram','aham-showcase','原典の固定版式で、行程や段階を編集できる図解資料へ。'),
    ('mpuig/agent-slides','企画を一枚で伝えるPowerPoint','work','agent-slides-showcase','原典CLIの文字と図形で、行程と関係図を一枚の企画書に。'),
    ('andyluu98/slidefly','図形がつながるモーション資料','motion','slidefly-showcase','原典Morphエンジンで、同じ図形が動いて話をつなぐ。'),
    ('chunyifish/soil-teaching-slides','図解で学べるWeb教材','diagram','soil-teaching-showcase','原典の授業構成と段階表示で、割合を図から理解する教材へ。'),
    ('xukp20/build-beamer-slides','数式と図を組む発表資料','diagram','beamer-showcase','原典Beamerの書式と数式で、説明をPDFへ組み上げる。'),
    ('Noi1r/powerpoint-skill','数式まで編集できるPowerPoint','diagram','native-math-showcase','原典の数式注入器で、平均とばらつきの式・図表を編集できる教材へ。'),
    ('zouchenzhen/thesis-defense-pptx-skill','テンプレートを使う研究発表','work','thesis-defense-showcase','原典テンプレートの複製と置換で、経路図と仮想試算を編集できる研究発表へ。'),
    ('MURMURE11118586/codex-xkppt-skill','大きな文字で組む編集室の企画','editorial','sebastian-207','原典の誌面用生成器で、文字と図形を編集できる企画へ。原典美術QAは未合格。'),
    ('demoolight/academic-image-ppt','画像で描く研究提案','editorial','sebastian-208','原典のページ別画像生成とノート付き包装で、空間の提案を資料へ。'),
    ('helloo1568/slidemuse','模型と断面で描く空間提案','editorial','sebastian-192','原典の4作風比較と頁別画像生成で、白い模型の空間提案を資料へ。'),
    ('Akxan/ppt-agent-skill','三原色と幾何で組む展示企画','editorial','ppt-agent-showcase','原典Bauhausの版式をSVG経由で、文字と形状を編集できるPowerPointへ。'),
    ('henryhyw/slidepoise','AI画像を編集できる図解へ','diagram','slidepoise-showcase','原典の画像計測とscene生成で、予約の流れを編集できる図解へ。'),
    ('wp-a/paper2ppt','根拠から組み立てる研究発表','diagram','sebastian-205','原典の資料分類と主張対応で、研究ノートを図解の発表へ。'),
    ('ficooooo/Paper2ScholarSlides','学術テンプレートで研究提案','work','sebastian-203','原典の版式を使い、空間モデルと比較条件を編集できる提案へ。'),
    ('deathcats4/scholar-ppt-cn','図形で説明する研究計画','diagram','sebastian-193','原典のテンプレート部品と組版方式で、仮説と検証手順を資料へ。'),
    ('LearnAIHubC/LearnDeck','HTMLから花の企画書を作る','editorial','learndeck-showcase','原典のDOM変換器で、書体の役割を保った編集可能PPTXへ。'),
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
    """Ship the maintained skill itself, with a small guide for a loose .md file."""
    source=ROOT/'skill-forks'/case['fork_id']/'SKILL.md'
    text=source.read_text(encoding='utf-8-sig').strip()
    if not text.startswith('---\n'):
        raise ValueError('Maintained skill has no frontmatter: '+str(source))
    # These sentences were our superseded review policy, not upstream build gates.
    text=text.replace('PowerPointは受け手の書体環境と全ページの実描画を確認する。',
                      'PowerPointは受け手の書体環境を案内し、主要な完成ファイルが開くことを確認する。')
    text=text.replace('原典の方式で実ファイルを生成し、全ページの本文、グラフ、図、ノート、移動を確認する。',
                      '原典の方式で実ファイルを生成し、主要な出力の初回表示を確認する。原典の必須ビルド確認は維持し、明白な欠けだけ直す。')
    repo=entry['repository'];commit=case.get('upstream_commit') or profile['upstream_commit']
    notes=profile.get('recipe_notes',[])
    specific=('\n\n## この方式で気をつけること\n\n'+
              '\n'.join('- '+note for note in notes)) if notes else ''
    license_paths=profile.get('license_paths',[])[:3]
    legal='\n'.join('- https://github.com/'+repo+'/blob/'+commit+'/'+p for p in license_paths)
    return text+specific+f'''

## 単体の本文から使う

この本文は `skill-forks/{case['fork_id']}/SKILL.md` を元にした日本語派生です。読み手・目的・自分の原稿を添えてAIへ渡す。

原典: https://github.com/{repo}/tree/{commit}

本文内の `upstream/`・`references/`・制作ソースは、サイトの一式ZIP `{Path(case['fork_download']).name}` を展開した中の参照です。単体Markdownには実装や素材を内包しません。ZIPを渡すか、固定原典から必要ファイルを取得して制作する。書体は公式配布物とOFL原文を利用する。

原作者: {repo.split('/')[0]} / 原典条件: {profile.get('license') or '個別条件'}。公式日本語版ではありません。原文LICENSE・NOTICEと素材・書体の条件を保持し、カタログのCC0を原典へ広げない。

{legal}
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
        skill_source='skill-forks/'+case['fork_id']+'/SKILL.md'
        entry={'repository':repo,'title_ja':title,'description_ja':description,'style':style,'featured_case_id':case_id,'skill_download':'downloads/skills/'+case['fork_id']+'.md','skill_source':skill_source,'skill_source_sha256':hashlib.sha256((ROOT/skill_source).read_bytes()).hexdigest(),'fork_download':case.get('fork_download'),'license':profile.get('license'),'license_notice_ja':profile.get('license_notice_ja','')}
        (ROOT/entry['skill_download']).write_text(skill_text(entry,profile,case),encoding='utf-8')
        entries.append(entry)
    active_case_ids=[e['featured_case_id'] for e in entries]
    by_repo={entry['repository']:entry for entry in entries}
    case_recipes={}
    for case in cases:
        entry=by_repo.get(case['repository'])
        if not entry:continue
        source='skill-forks/'+case['fork_id']+'/SKILL.md'
        download='downloads/skills/'+case['fork_id']+'.md'
        (ROOT/download).write_text(skill_text(entry,profiles[case['repository']],case),encoding='utf-8')
        case_recipes[case['id']]={'skill_download':download,'skill_source':source,'skill_source_sha256':hashlib.sha256((ROOT/source).read_bytes()).hexdigest(),'fork_download':case.get('fork_download'),'source_download':case.get('source_download'),'upstream_commit':case.get('upstream_commit') or profiles[case['repository']]['upstream_commit']}
    dump('data/product-collection.json',{'updated_at':'2026-10-14','title':'Studio Yebisu AIスライドアトリエ','policy':'原典方式で制作した実例から選ぶ日本語の厳選スキル集','archive':'data/skills.json','entries':entries,'active_case_ids':active_case_ids,'case_recipes':case_recipes,'excluded':exclusions})
    with ZipFile(ROOT/'downloads/yebisu-japanese-skill-entries.zip','w',ZIP_DEFLATED) as z:
        for download in sorted({r['skill_download'] for r in case_recipes.values()}):z.write(ROOT/download,Path(download).name)
        z.writestr('README.md','日本語の指示本文集です。各本文の固定原典と個別ライセンスを参照してください。実装・原文LICENSEはサイトの一式ZIPから別途取得できます。\n')
    print(f'{len(entries)} curated skills, {len(case_recipes)} linked cases and {len(set(r["skill_download"] for r in case_recipes.values()))} direct Markdown files built')
