"""Dashi single-variant Japanese example, using the upstream renderer and validators."""
from pathlib import Path
import json, shutil, os, difflib
from repository_example_support import ROOT, UP, Production, read, write, dump, rel
import re
def append_assets(doc, production, css='', bridge=''):
    doc = re.sub(r'<html[^>]*>', '<html lang="ja">', doc, count=1)
    font_css = production.fonts(doc + css)
    addition = '<style>' + font_css + '\n' + css + '</style>'
    return doc.replace('</head>', addition + '</head>', 1).replace('</body>', '<script>' + bridge + '</script></body>', 1)

def bridge(api):
    return """
if(parent!==window){
document.addEventListener('keydown', e=>{if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();parent.postMessage({type:'yebisu-close'},location.origin)}},true);
window.addEventListener('message', e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide')return;const n=e.data.index; if(!Number.isInteger(n))return;""" + api + """});
const pager=document.getElementById('deck-page-count');
const report=()=>{const n=parseInt(pager?.textContent,10)-1;if(Number.isInteger(n))parent.postMessage({type:'yebisu-page',index:n},location.origin)};
if(pager)new MutationObserver(report).observe(pager,{childList:true,subtree:true,characterData:true});
report();
}
"""



def dashi():
    repo = 'chuspeeism/dashi-ppt-skill'
    p = Production(repo, 'dashi-ppt', 'ec', 'EC月次報告：売上と粗利を確かめる', 'Dashi / theme05 色譜チャート',
        '原典のgoal-scaffold --layout-variants 1・inspect-layout・props-safe・validate-goal-spec・React/tsx render-goalを実行。theme05の4種類の実テンプレートで6ページを制作。標準3+1経路の検証不整合を記録し、原典が備える1案経路を採用。日本語派生theme05では入力値から図形寸法を計算する局所修正を適用。',
        'json_plan_and_original_react_renderer', ['skills/dashi-ppt/SKILL.md', 'skills/dashi-ppt/project/scripts/goal-scaffold.mjs', 'skills/dashi-ppt/project/scripts/render-goal-deck.jsx', 'skills/dashi-ppt/project/src/deckComposer.jsx', 'LICENSE', 'skills/dashi-ppt/project/packages/html-deck-to-pptx/LICENSE'])
    project = prepare_japanese_runtime(p)
    titles = ['EC月次報告', '売上は前年から20%増えた', '粗利額は増え、粗利率は下がった', '売上の内訳をチャネルで見る', '返品率の上昇を先に確認する', '次月は返品と粗利率を追う']
    notes = ['架空のEC事業の月次報告です。1200万円の売上を使った説明用サンプルです。', '前年1000万円に対して1200万円、増加額200万円、成長率20%です。', '粗利は前年380万円から432万円へ52万円増加しました。粗利率は38%から36%へ2ポイント低下しています。', '240・390・210・360万円の合計は1200万円です。チャネル別の数字は架空です。', '返品率は前年4%から6%へ2ポイント上昇した設定です。要因はまだ調べていません。', '次月は返品の理由と粗利率の変化を追います。施策の実施や成果を示す報告ではありません。']
    p.run(['node', project / 'scripts/goal-scaffold.mjs', '--title', p.title, '--goal', '架空EC事業の売上・粗利・返品を日本語で共有する', '--theme', 'theme05', '--pages', '6', '--layout-variants', '1', '--seed', 'yebisu-ec-single', '--out', p.out / 'goal.json'])
    goal = json.loads(read(p.out / 'goal.json'))
    goal['language'] = 'en'
    goal['slides'] = single_slides()
    dump(p.out / 'goal.json', goal)
    layout_ids = sorted({s['layout'] for s in goal['slides']})
    inspection = p.run(['node', project / 'scripts/inspect-layout.mjs', '--compact', *layout_ids])
    dump(p.out / 'source/inspect-selected.json', json.loads(inspection))
    p.run(['node', project / 'scripts/write-safe-props.mjs', '--goal', p.out / 'goal.json'])
    p.run(['node', project / 'scripts/validate-goal-spec.mjs', p.out / 'goal.json'])
    p.run(['npm.cmd', '--prefix', project, 'run', 'render:goal', '--', p.out / 'goal.json', p.out / 'index.html'])
    p.run(['node', project / 'scripts/validate-swiss-deck.mjs', p.out / 'index.html'], cwd=project)
    p.run(['node', project / 'scripts/validate-goal-copy.mjs', p.out / 'goal.json', p.out / 'index.html'])
    doc = read(p.out / 'index.html')
    css = "body,.slide,.deck{font-family:'Yebisu Noto Sans JP',sans-serif}.pulse-quote__big{white-space:pre-line}"
    write(p.out / 'index.html', append_assets(doc, p, css, bridge("window.go(n,{animate:false,force:true});")))
    p.run(['node', project / 'scripts/validate-swiss-deck.mjs', p.out / 'index.html'], cwd=project)
    p.run(['node', project / 'scripts/validate-goal-copy.mjs', p.out / 'goal.json', p.out / 'index.html'])
    result = p.finish(titles, notes, use_case='月次報告', extra={'license_note': 'AGPL-3.0。内蔵PPTXエンジンは個別の専有条件。本作例はHTML生成経路を使用。'})
    finalize_evidence(p, result)
    return result

def prepare_japanese_runtime(p):
    """Patch only the two chart components and one locale label in a derived copy.

    Upstream's copy wrapper replaces React text leaves AFTER chart geometry was
    calculated from defaults; that cannot update axes/height/arc proportions.
    Feed supplied copy into the original components before their calculations.
    """
    from repository_example_support import hfile
    derived = ROOT / '.build/dashi-ja-source'
    shutil.copytree(p.up, derived, dirs_exist_ok=True, ignore=shutil.ignore_patterns('node_modules', '.git'))
    project = derived / 'skills/dashi-ppt/project'
    if not (project / 'node_modules').exists():
        os.symlink(p.up / 'skills/dashi-ppt/project/node_modules', project / 'node_modules', target_is_directory=True)
    module = project / 'dist/theme-runtime/theme05.module.mjs'
    original = read(module)
    text = original
    changes = []
    for start, end, constant, setup in [
        ('function l(n){let i=Object.assign({},l.defaults,n),o=i.accentColor,r=Math.max(2,Math.min(a.points.length,i.pointCount)),c=a.points.slice(0,r);', '}l.controls=', 'a', 'let copy={...a,...n.copy};'),
        ('function o(r){let c=Object.assign({},o.defaults,r),y=c.accentColor,m=Math.max(3,Math.min(t.segments.length,c.segmentCount)),g=t.segments.slice(0,m);', '}o.controls=', 't', 'let copy={...t,...r.copy};'),
    ]:
        assert text.count(start)==1, 'Pinned upstream component signature changed'
        begin=text.index(start); finish=text.index(end,begin)+1
        before=text[begin:finish]
        after=re.sub(r'\b'+constant+r'\.', 'copy.', before)
        brace=after.index('{')+1
        after=after[:brace]+setup+after[brace:]
        if constant=='a':
            source=r'Et("small",{children:[y.s," \u7B14"]})'
            assert after.count(source)==1
            after=after.replace(source, r'i.showSecondary&&Et("small",{children:[y.s," 件"]})')
        changes.append({'component':'PulseTrend' if constant=='a' else 'PulseShare','before':before,'after':after})
        text=text[:begin]+after+text[finish:]
    label=r'" \u9879\u6307\u6807"'
    assert text.count(label)>=1
    text=text.replace(label,'" 項目"')
    write(module,text)
    review_diff = 'Review-only diff of selected component bodies; use the Python builder to apply exact pinned replacements.\n'
    for change in changes:
        review_diff += ''.join(difflib.unified_diff(change['before'].replace(';',';\n').splitlines(True), change['after'].replace(';',';\n').splitlines(True), fromfile='upstream/'+change['component'], tofile='japanese/'+change['component'])) + '\n'
    review_diff += 'Locale suffix: 项指标 -> 項目 (4 occurrences in theme05 module).\n'
    write(p.out/'source/theme05-runtime.diff', review_diff)
    shutil.copyfile(module,p.out/'source/theme05-ja.module.mjs')
    dump(p.out/'source/runtime-changes.json',{'source_path':'skills/dashi-ppt/project/dist/theme-runtime/theme05.module.mjs','source_sha256':__import__('hashlib').sha256(original.encode()).hexdigest(),'modified_sha256':hfile(module),'changes':changes,'label_change':{'from':'项指标','to':'項目'},'validators_modified':False,'export_engine_modified':False})
    # Original bundle builder, linked to the modified AGPL theme module. The
    # proprietary PPTX package is neither modified nor distributed separately.
    runner=p.out/'source/build-ja-runtime.mjs'
    write(runner, "import fs from 'node:fs';\nimport {buildClientRuntime} from " + json.dumps((project/'src/components/themes/runtime-build.mjs').as_uri()) + ";\nimport {buildThemeRegistrySource} from " + json.dumps((project/'src/components/themes/theme-registry-codegen.mjs').as_uri()) + ";\nconst registryPath=" + json.dumps(str(p.out/'source/ja-theme-registry.jsx')) + ";\nfs.writeFileSync(registryPath,buildThemeRegistrySource(['theme05'],{importPrefix:" + json.dumps((project/'dist/theme-runtime').as_posix()+'/') + ",fromModules:true,generated:false}));\nbuildClientRuntime({root:" + json.dumps(str(project)) + ",outFile:" + json.dumps(str(project/'dist/theme-runtime/imported-theme-runtime.theme05.js')) + ",registryPath});\n")
    p.run(['node',runner])
    return project


def single_slides():
    def slide(n, copy, **props):
        return {'layout': f'theme05_page{n:03}', 'props': {'copy': copy, **props}}
    return [
        slide(1, dict(brand='EC 月次レポート', brandEn='MONTHLY REVIEW', meta=['架空のEC事業','前年同月と比較','説明用サンプル'], kicker='売上・粗利・返品を確認する', titleTop='EC事業の',titleBottom='月次報告',subtitle='売上が伸びた月の、利益と返品を確かめる', subtitleEn='SALES / MARGIN / RETURNS',railHead='当月の主な数値',specs=[{'k':'売上','v':'1,200','vn':'万円'},{'k':'粗利額','v':'432','vn':'万円'},{'k':'粗利率','v':'36','vn':'%'},{'k':'返品率','v':'6','vn':'%'}],footer='実在企業の業績ではありません')),
        slide(9, dict(eyebrow='売上の変化',title='売上は前年から20%増',sub='前年1,000万円から当月1,200万円へ',sheet='月次比較', primaryName='売上（万円）',secondaryName='補助系列なし',points=[{'axis':'前年同月','v':1000,'s':0},{'axis':'当月','v':1200,'s':0}],conclusion='増加額は200万円。成長率は20%です。'), pointCount=2,focusIndex=2,showSecondary=False),
        slide(18, dict(eyebrow='粗利の確認',sheet='金額と率を分ける',quote='粗利額は増え、\n粗利率は下がった',sub='売上拡大と利益率の変化を別々に見る',points=[{'n':'01','t':'粗利額は52万円増','d':'前年380万円から当月432万円へ増加。'},{'n':'02','t':'粗利率は2ポイント低下','d':'前年38%から当月36%へ低下。'},{'n':'03','t':'値引きと原価を確認','d':'低下の原因は未確定。内訳を確認する。'}],source='架空データ：売上×粗利率から計算')),
        slide(10, dict(eyebrow='売上の構成',title='4チャネルで1,200万円',sub='広告390万円が最大。構成比は32.5%。',sheet='チャネル別内訳',unit='%',segments=[{'name':'検索 240万円','v':20},{'name':'広告 390万円','v':32.5},{'name':'メール 210万円','v':17.5},{'name':'直接 360万円','v':30}],conclusion='検索20%・広告32.5%・メール17.5%・直接30%'),segmentCount=4,focusIndex=2),
        slide(9, dict(eyebrow='返品の変化',title='返品率は4%から6%へ',sub='前年から2ポイント上昇。理由は未確認。',sheet='優先して確認',primaryName='返品率（%）',secondaryName='補助系列なし',points=[{'axis':'前年同月','v':4,'s':0},{'axis':'当月','v':6,'s':0}],conclusion='商品別に分け、返品理由を確認します。'),pointCount=2,focusIndex=2,showSecondary=False),
        slide(18, dict(eyebrow='次月の確認事項',sheet='実施前の提案',quote='返品の理由と粗利率を追う',sub='確認した内容を、次月の判断につなげる',points=[{'n':'01','t':'返品を分類する','d':'商品別と理由別に分け、偏りを確認する。'},{'n':'02','t':'粗利率を分析する','d':'値引きと原価の内訳を前年と比較する。'},{'n':'03','t':'対策と数値を報告する','d':'確認結果から施策を選び、変化を追う。'}],source='施策の実施や成果を示す報告ではありません')),
    ]


def finalize_evidence(p, result):
    from repository_example_support import hfile
    project = p.up / 'skills/dashi-ppt/project'
    for i in range(1, len(p.commands) + 1):
        shutil.copyfile(ROOT / '.build/repository-runs/dashi-ppt' / f'{i}.txt', p.out / 'source' / f'run-{i:02}.txt')
    shutil.copyfile(Path(__file__), p.out / 'source/build_dashi_repository_example.py')
    shutil.copyfile(Path(__file__).with_name('repository_example_support.py'), p.out / 'source/repository_example_support.py')
    shutil.copyfile(project / 'packages/html-deck-to-pptx/LICENSE', p.out / 'LICENSE.export-engine.txt')
    prov = json.loads(read(p.out / 'PROVENANCE.json'))
    prov['upstream_source_modified'] = False
    prov['derived_source_modified'] = True
    prov['derived_source'] = '.build/dashi-ja-source'
    prov['runtime_changes'] = 'source/runtime-changes.json'
    prov['runtime_sha256'] = hfile(p.out/'assets/imported-theme-runtime.js')
    prov['generation_route'] = 'single_variant_goal_props_with_documented_theme05_runtime_fix'
    prov['validation'] = {'props_safe': 'passed; 2 advisory range warnings', 'goal_spec': 'passed', 'swiss': 'passed', 'goal_copy': 'passed', 'validators_modified': False}
    prov['local_changes'] = ['日本語の全copy propsと実データを作成', '表示件数を入力の2点/4構成比へ調整、副系列を非表示', 'PulseTrend/PulseShareがcopy propsからグラフ座標を計算する局所修正', '副系列非表示時の固定単位を抑止、項目ラベルの日本語化、引用見出し改行', 'Noto Sans JPの埋め込みとカタログ連携用navigation bridgeを生成後HTMLへ追加']
    prov['known_blocked_route'] = 'schema-v2 3+1: spec passes, copy validator omits projection.structure and rejects 18 candidate variants; not adopted'
    for name in ['inspect-layout.mjs', 'write-safe-props.mjs', 'validate-goal-spec.mjs', 'validate-goal-copy.mjs', 'validate-swiss-deck.mjs']:
        path = 'skills/dashi-ppt/project/scripts/' + name
        prov['references'].append({'path': path, 'sha256': hfile(p.up / path)})
    dump(p.out / 'PROVENANCE.json', prov)
    guide = {'repository': p.repo, 'execution_type': p.execution_type, 'summary_ja': p.method,
      'requirements': ['Node.js 20以降（実行時24.18.0）とnpm', '原典projectでnpm ci --ignore-scripts', 'このカタログの生成補助はPython / fontTools / Brotliと共通フォント資産を使用'],
      'steps': ['固定commitの原典を取得', 'goal-scaffold --layout-variants 1で6ページを作る', 'inspect-layoutのcopyKeysとfillPlanを読みgoal.jsonのpropsへ日本語を記入', 'props:safe → validate:goal-spec → render:goalを実行', 'validate:swissとvalidate:goal-copyを実行し、ブラウザで6ページを確認'],
      'commands': ['npm --prefix <upstream>/skills/dashi-ppt/project ci --ignore-scripts', 'python tools/build_dashi_repository_example.py'],
      'source_refs': [{**r, 'url': f"https://github.com/{p.repo}/blob/{p.pin['commit']}/{r['path']}"} for r in prov['references']],
      'limitations': ['標準3+1モードは原典の検証不整合があり、本例は原典CLIが提供する1案経路を使用。全3+1機能の検証完了を意味しない。', '派生theme05で入力値がグラフ寸法に反映されるよう修正。原典そのままのruntimeではない。変更差分を同梱。', 'HTMLの本文とページ移動が対象。PPTX/PDF書出しは未検証。', '原典はAGPL-3.0、内蔵PPTXエンジンは別の専有条件。エンジンを抽出・再配布していない。', 'カタログ内の静的previewでは原典の保存/API書出しは利用できない。編集保存/書出しには原典preview serverを使う。'],
      'reproduction': rel(p.out / 'README.md')}
    dump(ROOT / 'data/dashi-repository-guides.json', [guide])
    write(p.out / 'source/SCHEMA-V2-BLOCKER.md', '# 標準3+1経路の未解消問題\n\n固定commitでPageContentPack→goal-scaffold(schemaVersion 2)→validate-goal-spec→render:goalは成功。しかしvalidate-goal-copyはtemplate candidate.propsだけを基準にし、projection.structureの配列・補助欄を具体化せず、18候補を未記入と判定した。明示contentMapを追加するとdeterministic projectionの一致検査で拒否される。検証条件を削除・無視していない。\n\n本作例では原典に実在する--layout-variants 1の経路を採用。全6ページをcopy propsで日本語化し、原典の検証4種を通した。3+1モードを動作済みと扱わない。標準経路のgoalとエラーログはschema-v2-blocked-goal.json / schema-v2-copy-failure.txt。\n')
    readme = read(p.out / 'README.md')
    readme += '\n## 再現と日本語化\n\nこのカタログのルートで `python tools/build_dashi_repository_example.py` を実行します。単独のPythonファイルだけでは再現できません。原典固定commit、data/case-inputs.json、共通フォント資産とrepository_example_support.pyが必要です。原典projectで `npm ci --ignore-scripts` を済ませてください。\n\n日本語の派生runtimeを含めて再生成する場合はこのPython生成器を使います。元runtimeだけでHTMLを生成する場合は同梱goal.jsonを使い、原典projectから `npm run render:goal -- <goal.jsonの絶対パス> <index.htmlの絶対パス>` を実行できますが、原典そのままのグラフではラベルと実際の図形寸法が一致しない問題が再発します。本文はgoal.jsonのslides[].props.copyです。001表紙、009棒グラフ、010構成比、018結論の実テンプレートを使っています。構成比のvは金額でなく百分率（20、32.5、17.5、30）です。棒グラフの1000/1200は原典のサンプル推定範囲を超える警告が2件ありますが、ハード制約ではなく値を縮小していません。\n\n標準3+1経路はsource/SCHEMA-V2-BLOCKER.mdに記録した問題により未採用。採用した1案経路では取得原本とvalidatorは変更していません。派生コピーのtheme05モジュールでは、棒・ドーナツの寸法計算へ入力copy propsを反映し、固定項目ラベルと副系列の単位表示を修正しています。変更前後はsource/runtime-changes.json、読解用差分はsource/theme05-runtime.diff、適用手順はPython生成器に保存しています。全候補切替やPPTX/PDF書出しを動作済みとはしていません。\n\nブラウザの左右キーでページ移動できます。カタログ内の静的previewは閲覧用です。編集保存やPPTX/PDF書出しには原典のpreview:startサーバーとシステムブラウザを使ってください。原典のSKILL.mdに起動手順があります。\n\n原典AGPL条件はLICENSE.upstream。PPTXエンジンはLICENSE.export-engine.txtの専有条件で、今回そのパッケージを抽出・再配布していません。HTMLのテーマ資産は原典生成物です。入力数値は全て架空です。\n'
    write(p.out / 'README.md', readme)


if __name__ == '__main__':
    result = dashi()
    dump(ROOT / 'data/dashi-repository-examples.json', [result])


