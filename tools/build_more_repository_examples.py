"""Apply separate upstream creation paths; helpers only package evidence."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse, base64, html, json, re, shutil, uuid
from repository_example_support import ROOT, UP, Production, read, write, dump, rel

def append_assets(doc, production, css='', bridge=''):
    doc = re.sub(r'<html[^>]*>', '<html lang="ja">', doc, count=1)
    font_css = production.fonts(doc + css)
    motion_css='@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.slide.active .a,.slide.is-active [data-anim]{opacity:1!important;transform:none!important}}'
    addition = '<style>' + font_css + '\n' + css + '\n'+motion_css+'</style>'
    return doc.replace('</head>', addition + '</head>', 1).replace('</body>', '<script>' + bridge + '</script></body>', 1)

def bridge(api):
    return """
if(parent!==window){
document.addEventListener('keydown', e=>{if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();parent.postMessage({type:'yebisu-close'},location.origin)}},true);
window.addEventListener('message', e=>{if(e.source!==parent||e.origin!==location.origin||e.data?.type!=='yebisu-slide')return;const n=e.data.index; if(!Number.isInteger(n))return;""" + api + """});
}
"""

KNOWLEDGE_TITLES = ['社内検索を4週間で試す', '問い合わせの前に、探せる場所をつくる',
                    '見せてよい資料だけを検索する', '4週間で導入判断の材料を集める',
                    '答えの正しさと権限を別々に測る', '小さく試して、継続を決める']
KNOWLEDGE_NOTES = ['50人の架空企業を想定した企画例です。導入効果の実績ではありません。',
                   '対象は30件の社内文書です。まず資料を探す仕事を切り出し、回答を自動承認しない設計にします。',
                   '検索候補の段階でアクセス権限を確認します。利用者の権限外の文書を回答に混ぜないことが最優先です。',
                   '1週目に整理、2週目に検索、3週目に評価、4週目に導入判断を行います。各段階の担当と成果物を決めます。',
                   '質問30件中24件の根拠提示、権限外質問20件の漏えいゼロ、更新の翌営業日反映は評価目標です。達成した数値ではありません。',
                   '50人全員へ一度に広げず、試行の結果を根拠に判断します。品質・権限・運用の条件が揃ってから継続します。']

def reveal():
    repo = 'ryanbbrown/revealjs-skill'
    p = Production(repo, 'revealjs-skill', 'knowledge', KNOWLEDGE_TITLES[0], 'reveal.js / Teal & Coral',
        '原典create-presentation.jsで6ページの骨格とbase-styles.cssを生成。原典のpt単位・2カラム・section構造に日本語本文を組み、reveal.jsの公式ナビゲーションで再生。',
        'scaffold_cli_then_skill_authoring', ['skills/revealjs/SKILL.md', 'skills/revealjs/scripts/create-presentation.js', 'skills/revealjs/references/base-styles.css', 'LICENSE'])
    p.run(['node', p.up / 'skills/revealjs/scripts/create-presentation.js', '--structure', '1,1,1,1,1,1', '--title', p.title, '--output', p.out / 'index.html'])
    doc = read(p.out / 'index.html')
    bodies = [
        '<h1>社内検索を<br>4週間で試す</h1><p>50人の会社から始める、社内文書30件の検索企画</p><p class="subtitle">企画例 / 架空の条件による説明資料</p>',
        '<h2>問い合わせの前に、<br>探せる場所をつくる</h2><div class="columns" style="display:grid;grid-template-columns:1fr 1fr"><div class="col"><h3>今の困りごと</h3><p>保存先がばらばら</p><p>同じ質問が繰り返される</p><p>どの版が新しいか分からない</p></div><div class="col"><h3>試す範囲</h3><p>対象文書は30件</p><p>回答には出典を付ける</p><p>判断は担当者が行う</p></div></div>',
        '<h2>見せてよい資料だけを検索する</h2><div class="flow"><div><strong>利用者</strong><p>所属・権限を確認</p></div><p class="flow-arrow">→</p><div><strong>検索</strong><p>閲覧できる文書だけ</p></div><p class="flow-arrow">→</p><div><strong>回答</strong><p>出典付きで提示</p></div></div><p class="caution">権限外の資料は、検索候補にも入れない</p>',
        '<h2>4週間で判断の材料を集める</h2><table><tr><th>期間</th><th>やること</th><th>残すもの</th></tr><tr><td>1週目</td><td>文書と権限を整理</td><td>対象30件の一覧</td></tr><tr><td>2週目</td><td>検索の試作</td><td>出典付きの回答</td></tr><tr><td>3週目</td><td>質問で評価</td><td>品質・権限の記録</td></tr><tr><td>4週目</td><td>継続を判断</td><td>改善項目と担当</td></tr></table>',
        '<h2>答えの正しさと権限を別々に測る</h2><div class="metrics"><div><strong>24 / 30</strong><p>根拠を示せる質問数</p></div><div><strong>0 / 20</strong><p>権限外への漏えい数</p></div><div><strong>翌営業日</strong><p>更新を反映する期限</p></div></div><p class="caution">すべて試行で測る目標値です</p>',
        '<h2>小さく試して、継続を決める</h2><blockquote>品質・権限・運用の条件を<br>揃えてから、利用を広げる。</blockquote><p>最初の一歩：対象30件と、文書を確認する担当者を決める</p>']
    soup = BeautifulSoup(doc, 'html.parser')
    for section, content, note in zip(soup.select('.slides > section'), bodies, KNOWLEDGE_NOTES):
        section.clear()
        section.append(BeautifulSoup(content + '<aside class="notes">' + html.escape(note) + '</aside>', 'html.parser'))
    doc = str(soup)
    package = ROOT / '.build/repository-runtime/node_modules/reveal.js'
    shutil.copytree(package / 'dist', p.out / 'reveal', dirs_exist_ok=True)
    shutil.copytree(package / 'plugin/notes', p.out / 'reveal/notes', dirs_exist_ok=True)
    shutil.copyfile(package / 'LICENSE', p.out / 'LICENSE.revealjs')
    doc = re.sub(r'<(?:script|link)[^>]*(?:chart\.js|reveal\.js-plugins|font-awesome)[^>]*(?:></script>|>)', '', doc)
    doc = re.sub(r'https://cdn.jsdelivr.net/npm/reveal\.js@[^/]+/dist/', 'reveal/', doc)
    doc = doc.replace('plugins: [ RevealChart ]', 'plugins: []')
    css = "body,.reveal,.reveal p,.reveal li,.reveal td,.reveal th{font-family:'Yebisu Noto Sans JP',sans-serif}.reveal{background:#F4F6F6;color:#1C2833}.reveal h1{font-size:58pt;line-height:1.25}.reveal h2{font-size:34pt;line-height:1.3;color:#277884}.reveal h3{font-size:27pt;margin:0 0 28px}.reveal p,.reveal td,.reveal th{font-size:22pt}.reveal section{padding:64px 80px;box-sizing:border-box}.reveal .subtitle,.reveal .caution{font-size:16pt;color:#5D676E;margin-top:38px}.columns{gap:64px;margin-top:52px}.columns p{margin:22px 0;line-height:1.5}.metrics,.flow{display:flex;align-items:center;justify-content:space-between;gap:30px;margin-top:70px}.metrics strong{font-size:36pt;color:#FE4447}.flow strong{font-size:32pt;color:#277884}.flow>div{padding:32px 22px;border-top:3px solid #277884}.flow .flow-arrow{color:#b63d35;font-size:32pt}.flow p{line-height:1.5}.flow .flow-arrow{margin:0}.reveal table{width:100%;margin-top:46px;border-collapse:collapse}.reveal th{background:#277884;color:#fff;font-weight:600}.reveal td{border-bottom:1px solid #9fb4b7}.reveal td,.reveal th{padding:18px;text-align:left}.reveal blockquote{font-size:35pt;line-height:1.55;border-left:0;padding:50px 0}"
    write(p.out / 'index.html', append_assets(doc, p, css, bridge('Reveal.slide(n);')))
    return p.finish(KNOWLEDGE_TITLES, KNOWLEDGE_NOTES, use_case='業務改善')

def lewis():
    repo = 'lewislulu/html-ppt-skill'
    p = Production(repo, 'lewis-html-ppt', 'git', 'Gitの変更を、チームへ届ける', 'Tech Sharing / original tokens',
        '原典new-deck.shでtech-sharingテンプレートを展開。全8ページの固有レイアウト・style.css・base.css・runtime.jsを保ち、Git入門の本文とコード・発表メモへ差し替え。',
        'template_scaffold_and_instruction_skill', ['SKILL.md', 'scripts/new-deck.sh', 'templates/full-decks/tech-sharing/index.html', 'templates/full-decks/tech-sharing/style.css', 'assets/base.css', 'assets/runtime.js', 'LICENSE'])
    # The upstream scaffold was invoked before this authoring step and its intact result exists.
    # Execute the upstream scaffold in a fresh staging folder on every rebuild.
    stage = ROOT / '.build/repository-scaffolds' / uuid.uuid4().hex
    bash = Path('C:/Program Files/Git/bin/bash.exe')
    shell = str(bash) if bash.exists() else shutil.which('bash')
    if not shell:
        raise RuntimeError('Git Bash is required for the upstream scaffold')
    def bash_path(path):
        value = Path(path).resolve().as_posix()
        return '/' + value[0].lower() + value[2:] if re.match(r'^[A-Za-z]:/', value) else value
    p.run([shell, bash_path(p.up / 'scripts/new-deck.sh'), p.ident, bash_path(stage), '-t', 'tech-sharing'])
    doc = read(stage / p.ident / 'index.html')
    soup = BeautifulSoup(doc, 'html.parser')
    slides = soup.select('.deck > section.slide')
    titles = ['Gitの変更を、チームへ届ける', '小さな変更を、順番に届ける', '保存・記録・共有は別の操作', 'まず今の変更を確かめる', '記録する変更を選ぶ', '変更を説明して、記録する', 'チームへ共有し、レビューする', '自分の変更を確かめてみよう']
    def text(selector, value, page):
        el = slides[page].select_one(selector)
        if el is None: raise ValueError(selector)
        el.clear(); el.append(BeautifulSoup(value, 'html.parser'))
    text('.kicker', 'GIT ONBOARDING / 日本語研修', 0)
    text('h1', 'Gitの変更を、<br><span style="background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent">チームへ届ける</span>', 0)
    text('.lede', '保存したファイルが、レビューされるまで。', 0)
    text('.speaker', '<div class="av"></div><div><b>社内勉強会</b><span>初めてGitを使う人へ / 8ページ</span></div>', 0)
    text('.deck-footer > span', 'STATUS / ADD / COMMIT / PUSH', 0)
    text('h2', titles[1], 1)
    for row, label in zip(slides[1].select('.agenda-row'), ['今の変更を見る', '記録する変更を選ぶ', '変更の理由を残す', '共有してレビューする', '最初の一歩を試す']):
        row.select_one('.t').string = label; row.select_one('.d').string = ''
    text('h2', titles[2], 2)
    for card, head, body in zip(slides[2].select('.card'), ['ファイルの保存', '履歴への記録', 'チームへの共有'], ['エディターで保存した変更は、作業フォルダにあります。', 'commitで、選んだ変更を履歴に残します。', 'pushで、リモートへ変更履歴を送ります。']):
        card.h4.string = head; card.p.string = body; card.select_one('.tag').string = ''
    text('h2', titles[3], 3)
    text('.lede', '<span class="mono">git status</span> は変更の場所を、<span class="mono">git diff</span> は変更の中身を示します。まず対象のファイルを確認します。', 3)
    text('.terminal pre', '$ git status<br>modified: README.md<br><br>$ git diff<br>説明文に、新しい手順を追加', 3)
    for tag, word in zip(slides[3].select('.tag'), ['作業フォルダ', '差分', '対象の確認']): tag.string = word
    text('h2', titles[4], 4)
    text('.lede', '今回届けたいファイルを <span class="mono">git add</span> で選び、<span class="mono">git diff --staged</span> で記録する差分を読みます。', 4)
    text('.stack', '<div class="tag">1. README.mdの変更を読む</div><div class="tag">2. git add README.md</div><div class="tag">3. git diff --staged</div>', 4)
    text('.card', '<h4 class="mono">記録の前に見ること</h4><div class="stack mt-m"><p>依頼された変更か</p><p>不要なファイルが混ざっていないか</p><p>何を変えたか説明できるか</p></div>', 4)
    text('h2', titles[5], 5)
    text('.terminal pre', '$ git diff --staged<br><br>$ git commit -m "説明書にセットアップ手順を追加"<br><br>$ git log -1 --oneline<br>変更の記録と、理由を確認', 5)
    text('h2', titles[6], 6)
    for card, head, body in zip(slides[6].select('.card'), ['ブランチ', 'push', 'レビュー'], ['チームが決めた作業ブランチで変更する。', '送り先とブランチを確認して、履歴を共有する。', '変更の目的・内容・確認方法を説明する。']):
        card.h4.string = head; card.p.string = body
    text('.lede', '参照：git-scm.com/docs / GitHub公式ドキュメント', 6)
    text('h2', titles[7], 7)
    text('.lede', '練習用フォルダで、git status を実行してみよう。', 7)
    text('.row', '<span class="tag">次の一歩：差分を読む</span><span class="tag">不明な状態は、共有前に確認</span>', 7)
    notes = ['初めて使う人向けの練習資料です。チームのリポジトリへ実際にpushする演習は含めません。', '一覧を丸暗記せず、変更がどこにあるかを意識して順に進めます。', '保存はcommitでもpushでもありません。この違いを最初に押さえます。', 'statusで位置、diffで中身を確かめます。', 'addで選んだ変更が、次のcommitの対象になります。', '変更を残す前に差分をもう一度読みます。', 'レビューの目的は、変更をチームが理解して確認できることです。', '自分の練習用フォルダから一歩始めてください。']
    for i, s in enumerate(slides):
        s['data-title'] = titles[i]
        s.append(BeautifulSoup('<aside class="notes">' + html.escape(notes[i]) + '</aside>', 'html.parser'))
    for i,s in enumerate(slides):
        kicker=s.select_one('.kicker')
        if kicker:kicker.string=['GIT ONBOARDING / 日本語研修','変更を届けるまで','保存・記録・共有','今の変更を見る','記録する変更を選ぶ','履歴に残す','チームへ届ける','最初の一歩'][i]
        label=s.select_one('.terminal .bar span:last-child')
        if label:label.string='変更の確認' if i==3 else '履歴への記録'
    soup.html['lang']='ja'
    soup.title.string=p.title
    for el in soup.select('link[href],script[src]'):
        attribute = 'href' if el.name == 'link' else 'src'
        if '/assets/' in el[attribute]:
            el[attribute] = 'assets/' + el[attribute].rsplit('/assets/', 1)[1]
    doc = str(soup)
    shutil.copytree(p.up / 'assets', p.out / 'assets', dirs_exist_ok=True)
    shutil.copyfile(stage / p.ident / 'style.css', p.out / 'style.css')
    # Keep the upstream Latin styling; add a Japanese family from official OFL source.
    write(p.out / 'assets/fonts.css', p.fonts(doc) + p.latin_fonts(['Space Grotesk','JetBrains Mono']) + "\n:root{--font-sans:'Yebisu Noto Sans JP',sans-serif;--font-display:'Yebisu Noto Sans JP',sans-serif}\n@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.slide.is-active [data-anim]{opacity:1!important;transform:none!important}}")
    doc = doc.replace('</head>', "<style>.tpl-tech-sharing{font-family:'Yebisu Noto Sans JP',sans-serif}.tpl-tech-sharing .lede,.tpl-tech-sharing .card p{font-size:30px;line-height:1.6;color:#b5bfc9}.tpl-tech-sharing .card h4{font-size:32px}.tpl-tech-sharing .terminal{font-size:26px}.tpl-tech-sharing .terminal pre{white-space:pre-wrap;overflow-wrap:anywhere}.tpl-tech-sharing .tag{font-size:22px}.tpl-tech-sharing .agenda-row .t{font:600 32px/1.5 'Yebisu Noto Sans JP',sans-serif}.tpl-tech-sharing .kicker{font-size:20px}.tpl-tech-sharing .h1,.tpl-tech-sharing .h2{line-height:1.3}</style></head>", 1)
    runtime = read(p.out / 'assets/runtime.js')
    runtime = runtime.replace('    function go(n, fromRemote){', '    window.yebisuNativeGo=go;\n    function go(n, fromRemote){', 1)
    write(p.out / 'assets/runtime.js', runtime)
    doc = doc.replace('</body>', '<script>' + bridge('if(window.yebisuNativeGo)window.yebisuNativeGo(n);') + '</script></body>')
    write(p.out / 'index.html', doc)
    return p.finish(titles, notes)

def minorun():
    p = Production('minorun365/minorun-marp-skill', 'minorun-marp', 'git', 'Gitの変更、どこに保存された？', 'minorun-dark / Marp',
        '原典のslide-story・slide-figures・slide-design-darkを適用。黒地テーマ本体を保持し、作業・ステージ・記録・共有の図を段階的に開示するMarp原稿を制作。Marp CLIで実HTMLを生成。',
        'instruction_skill_and_marp_cli', ['skills/slide-story/SKILL.md', 'skills/slide-figures/SKILL.md', 'skills/slide-design-dark/SKILL.md', 'theme/minorun-dark.css', 'tools/check-ai-smell.py', 'LICENSE'])
    # This showcase is a five-minute introductory excerpt, not the full 35-minute training.
    if not (p.out / 'input/original-broad-data.json').exists():
        write(p.out / 'input/original-broad-data.json', json.dumps(p.input, ensure_ascii=False, indent=2))
    p.input = {'title': p.title, 'audience': 'Gitを初めて使う人への5分の導入抜粋', 'goal': '保存・選択・記録・共有の違いを4段階の図で説明できる', 'duration_minutes': 5, 'commands': ['git status', 'git add README.md', 'git commit -m "手順を追加"', 'git push'], 'scope': '図による説明例。20分演習・ブランチ・レビュー依頼・競合解消は含めない。pushは送信先確認を説明するだけで実行しない。'}
    write(p.out / 'input/data.json', json.dumps(p.input, ensure_ascii=False, indent=2))
    write(p.out / 'input/BRIEF.md', '# Gitの変更、どこに保存された？\n\n初めてGitを使う人に5分で説明する導入抜粋。保存→ステージ→履歴→リモートの違いを、位置を揃えた4段階の図で示す。status/add/commit/pushは説明例。20分演習、ブランチ、レビュー、競合解消の教材ではない。送信操作は実行しない。元の35分教材の依頼はORIGINAL-BRIEF.mdとoriginal-broad-data.jsonへ保持する。\n')
    titles = ['Gitの変更、どこに保存された？', '保存した変更はどこにある？', 'まず、変更の現在地を見る', '変更は作業フォルダにある', '記録したい変更を選ぶ', '選んだ変更を履歴へ残す', '履歴をチームへ届ける', '迷ったら、まず状態と差分を読む', '今の変更を、git statusで見てみよう']
    notes = ['初めてGitを使う人向けの5分程度の架空勉強会です。', 'エディターで保存しただけではチームへ共有されません。', 'statusの表示を入口に、変更の場所を説明します。', 'まずファイルを編集して、作業フォルダが変わります。', 'addで、次に記録するファイルを選びます。', 'commitで、選んだ変更と理由が履歴に残ります。', 'pushで、指定したリモートへ履歴を送ります。送り先を確認してから行います。', '操作を続ける前に確認します。状態が分からないまま、復元や削除のコマンドを試さないでください。', '練習用フォルダで、いま何が変わったかを見てみましょう。']
    diagrams = []
    labels = ['作業フォルダ', 'ステージ', '履歴', 'リモート']
    for count in range(1, 5):
        elements = []
        for i in range(count):
            x = i * 260
            elements.append('<rect x="' + str(x) + '" y="40" width="210" height="210" rx="5" fill="' + ('#08616B' if i == count - 1 else '#1C2E30') + '"/><text x="' + str(x + 105) + '" y="155" text-anchor="middle" fill="#FFFFFF" font-family="Noto Sans JP" font-size="31">' + labels[i] + '</text>')
            if i:
                elements.append('<path d="M' + str(x - 40) + ',145 h30" stroke="#00C4E4" stroke-width="4" marker-end="url(#next)"/>')
        image = '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="320" viewBox="0 0 1000 320"><defs><marker id="next" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#00C4E4"/></marker></defs>' + ''.join(elements) + '</svg>'
        write(p.out / ('images/location-' + str(count) + '.svg'), image)
        diagrams.append('![w:1100](images/location-' + str(count) + '.svg)')
    bodies = ['# ' + titles[0] + '\n\nはじめてのGit勉強会', '# ' + titles[1], '# ' + titles[2] + '\n\n```console\n$ git status\nmodified: README.md\n```',
              '# ' + titles[3] + '\n\n' + diagrams[0] + '\n\nエディターで保存すると、ファイルが変わる。',
              '# ' + titles[4] + '\n\n' + diagrams[1] + '\n\n`git add README.md`',
              '# ' + titles[5] + '\n\n' + diagrams[2] + '\n\n`git commit -m "手順を追加"`',
              '# ' + titles[6] + '\n\n' + diagrams[3] + '\n\n`git push` の前に、送り先とブランチを確認。',
              '# ' + titles[7] + '\n\n`git status` で変更の位置を見る。\n\n`git diff` で変更の中身を読む。', '# ' + titles[8]]
    for i in [0, 1, 8]: bodies[i] = '<!-- _class: ' + ('top' if i == 0 else 'crosshead') + ' -->\n\n' + bodies[i]
    font = p.fonts('\n'.join(bodies)+''.join(labels))
    for svg in (p.out/'images').glob('location-*.svg'):
        raw=read(svg).replace('font-family="Noto Sans JP"','font-family="Yebisu Noto Sans JP"');cut=raw.index('>')+1;write(svg,raw[:cut]+'<style>'+font+'</style>'+raw[cut:])
    deck = '---\nmarp: true\npaginate: true\ntheme: minorun-dark\n---\n\n<style>' + font + "\nsection{font-family:'Yebisu Noto Sans JP',sans-serif}section.top h1,section.top p{transform:translateY(-64px)}section img{margin-top:24px;margin-bottom:20px}</style>\n\n" + '\n\n---\n\n'.join(body + '\n\n<!-- ' + note + ' -->' for body, note in zip(bodies, notes)) + '\n'
    write(p.out / 'deck.md', deck)
    shutil.copyfile(p.up / 'theme/minorun-dark.css', p.out / 'minorun-dark.css')
    marp = ROOT / '.build/repository-runtime/node_modules/@marp-team/marp-cli/marp-cli.js'
    p.run(['node', marp, '--no-stdin', p.out / 'deck.md', '--html', '--theme', p.out / 'minorun-dark.css', '--allow-local-files', '-o', p.out / 'index.html'])
    p.run(['python', p.up / 'tools/check-ai-smell.py', '--all', p.out / 'deck.md'])
    # Bespoke slides remain the Marp output. Hash navigation is provided by Marp's bespoke runtime.
    doc = read(p.out / 'index.html')
    doc = re.sub(r'<html[^>]*>', '<html lang="ja">', doc, count=1)
    doc = doc.replace('lang="C"', 'lang="ja"')
    doc = doc.replace('</body>', '<script>' + bridge("location.hash=String(n+1);") + '</script></body>')
    write(p.out / 'index.html', doc)
    return p.finish(titles, notes, use_case='登壇・Git入門')

def dashi():
    repo = 'chuspeeism/dashi-ppt-skill'
    p = Production(repo, 'dashi-ppt', 'ec', 'EC月次報告：売上と粗利を確かめる', 'Dashi / theme05 色譜チャート',
        '原典のlayout-query・PageContentPack・goal-scaffold(schema v2、3+1候補)・validate-goal-spec・React/tsx render-goalを実行。6論理ページの選択版を出力。共通HTMLへ描き直していません。',
        'json_plan_and_original_react_renderer', ['skills/dashi-ppt/SKILL.md', 'skills/dashi-ppt/project/scripts/goal-scaffold.mjs', 'skills/dashi-ppt/project/scripts/render-goal-deck.jsx', 'skills/dashi-ppt/project/src/deckComposer.jsx', 'LICENSE', 'skills/dashi-ppt/project/packages/html-deck-to-pptx/LICENSE'])
    project = p.up / 'skills/dashi-ppt/project'
    titles = ['EC月次報告', '売上は前年から20%増えた', '粗利額は増え、粗利率は下がった', '売上の内訳をチャネルで見る', '返品率の上昇を先に確認する', '次月は返品と粗利率を追う']
    notes = ['架空のEC事業の月次報告です。1200万円の売上を使った説明用サンプルです。', '前年1000万円に対して1200万円、増加額200万円、成長率20%です。', '粗利は前年380万円から432万円へ52万円増加しました。粗利率は38%から36%へ2ポイント低下しています。', '240・390・210・360万円の合計は1200万円です。チャネル別の数字は架空です。', '返品率は前年4%から6%へ2ポイント上昇した設定です。要因はまだ調べていません。', '次月は返品の理由と粗利率の変化を追います。施策の実施や成果を示す報告ではありません。']
    plans = [
        ('cover', '架空EC事業の月次報告', [('period', '対象', '説明用の架空データ', 1, '月次', '')]),
        ('metric', '売上1200万円、前年から200万円増', [('sales', '売上', '前年1000万円', 1200, '1,200', '万円'), ('growth', '前年比', '増加額200万円', 20, '+20', '%'), ('orders', '注文数', '前年3500件', 4000, '4,000', '件')]),
        ('comparison', '粗利額は52万円増、率は2ポイント低下', [('current', '当月粗利', '売上1200万円の36%', 432, '432', '万円'), ('previous', '前年粗利', '売上1000万円の38%', 380, '380', '万円'), ('rate', '当月粗利率', '前年38%から低下', 36, '36', '%')]),
        ('structure', '4チャネルの売上合計は1200万円', [('a', '検索', '売上構成20%', 240, '240', '万円'), ('b', '広告', '売上構成32.5%', 390, '390', '万円'), ('c', 'メール', '売上構成17.5%', 210, '210', '万円'), ('d', '直接', '売上構成30%', 360, '360', '万円')]),
        ('risk', '返品率は4%から6%へ上昇', [('returns', '当月返品率', '前年から2ポイント上昇', 6, '6', '%'), ('previous', '前年返品率', '比較対象', 4, '4', '%'), ('action', '確認項目', '商品別と返品理由', 1, '原因確認', '')]),
        ('ending', '返品の理由と粗利率を次月の重点へ', [('returns', '返品', '理由と商品別に確認', 1, '確認', ''), ('margin', '粗利率', '値引きと原価を確認', 1, '分析', ''), ('review', '次月', '対策と数値を報告', 1, '報告', '')])]
    pages = []
    for i, (intent, summary, facts) in enumerate(plans):
        items = [{'id': ident, 'label': label, 'detail': {'full': detail, 'short': detail}, 'value': value, 'displayValue': display, 'unit': unit or '項目', 'required': True, 'priority': 'high'} for ident, label, detail, value, display, unit in facts]
        pages.append({'id': 'page-' + str(i + 1), 'presentation': {'pageIntent': intent, 'coreMessage': summary,
                      'title': {'full': titles[i], 'short': titles[i]}, 'summary': {'full': summary, 'short': summary},
                      'items': items, 'chartData': [{'id': x['id'], 'label': x['label'], 'value': x['value'], 'displayValue': x['displayValue'], 'unit': x['unit']} for x in items if x['unit'] == items[0]['unit'] and x['unit'] != '項目'], 'media': []}})
    dump(p.out / 'page-content-pack.json', {'pages': pages})
    for i, (intent, _, _) in enumerate(plans):
        query = p.run(['node', project / 'scripts/layout-query.mjs', '--theme', 'theme05', '--role', intent, '--limit', '3', '--seed', 'yebisu-ec:slide-' + str(i + 1)])
        dump(p.out / ('source/layout-query-' + str(i + 1) + '.json'), json.loads(query))
    p.run(['node', project / 'scripts/goal-scaffold.mjs', '--title', p.title, '--goal', '架空EC事業の売上・粗利・返品を、日本語で共有する', '--theme', 'theme05', '--pages', '6', '--layout-variants', '3', '--content-plan', p.out / 'page-content-pack.json', '--seed', 'yebisu-ec', '--out', p.out / 'goal.json'])
    goal = json.loads(read(p.out / 'goal.json'))
    goal['language'] = 'en'
    goal['variantOutputMode'] = 'selected-only'
    dump(p.out / 'goal.json', goal)
    p.run(['node', project / 'scripts/validate-goal-spec.mjs', p.out / 'goal.json'])
    p.run(['npm.cmd', '--prefix', project, 'run', 'render:goal', '--', p.out / 'goal.json', p.out / 'index.html'])
    p.run(['node', project / 'scripts/validate-goal-copy.mjs', p.out / 'goal.json', p.out / 'index.html'])
    doc = read(p.out / 'index.html')
    css = "body,.slide,.deck{font-family:'Yebisu Noto Sans JP',sans-serif}"
    write(p.out / 'index.html', append_assets(doc, p, css, bridge("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}));for(let z=0;z<n;z++)document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));")))
    return p.finish(titles, notes, use_case='月次報告', extra={'license_note': 'AGPL-3.0。内蔵PPTXエンジンは個別の専有条件。本作例はHTML生成経路を使用。'})

def neon():
    p = Production('lqshow/neon-slides', 'neon-slides', 'knowledge', KNOWLEDGE_TITLES[0], 'Neon Dark / orange-blue',
        '原典skill/template.htmlを丸ごと複製し、deck内のsectionだけ日本語内容へ差し替え。components.mdのcover/compare/layers/steps/list-gridを使用し、原典CSS変数とgo/jumperのナビゲーションを保持。日本語字体を追加。',
        'locked_html_template_instruction_skill', ['skill/SKILL.md', 'skill/template.html', 'skill/components.md', 'LICENSE'])
    doc = read(p.up / 'skill/template.html')
    bodies = [
        '<div class="cover"><div class="center"><span class="tag">日本語の企画例</span><h1>社内検索を<br><span class="accent-o">4週間</span>で試す</h1><div class="divider"></div><p>50人の会社・社内文書30件から始める</p></div><div class="meta">架空の条件による説明資料</div></div>',
        '<div class="inner"><span class="tag">試す範囲</span><h1>問い合わせの前に、<span class="accent-o">探せる場所</span>を</h1><div class="compare"><div class="cmp old"><h3>今の困りごと</h3><p>文書の保存先が散らばり、同じ質問が繰り返される。</p></div><div class="cmp new"><h3>試行でつくるもの</h3><p>対象30件を整理して、出典付きで答える検索を試す。</p></div></div></div>',
        '<div class="inner"><span class="tag">権限の設計</span><h1>見せてよい資料だけを<span class="accent-b">検索する</span></h1><div class="layers"><div class="layer o"><h3>利用者</h3><p>所属とアクセス権限を確認</p></div><div class="layer b"><h3>検索</h3><p>閲覧できる文書だけを候補へ</p></div><div class="layer o"><h3>回答</h3><p>根拠となる出典を添えて提示</p></div></div></div>',
        '<div class="inner"><span class="tag">4週間の計画</span><h1>導入判断の材料を、<span class="accent-o">順に集める</span></h1><div class="steps"><div class="step o"><div class="label">1週目</div><div class="title">整理</div><div class="desc">文書と権限</div></div><div class="arrow o">→</div><div class="step b"><div class="label">2週目</div><div class="title">試作</div><div class="desc">出典付き検索</div></div><div class="arrow b">→</div><div class="step o"><div class="label">3週目</div><div class="title">評価</div><div class="desc">品質と漏えい</div></div><div class="arrow o">→</div><div class="step b"><div class="label">4週目</div><div class="title">判断</div><div class="desc">継続の条件</div></div></div></div>',
        '<div class="inner"><span class="tag">評価目標</span><h1>正しさと権限を<span class="accent-b">別々に測る</span></h1><div class="list-grid"><div class="item"><div class="num">24/30</div><div class="txt"><h3>根拠を示せる質問</h3><p>評価用30件のうち24件以上を目標</p></div></div><div class="item"><div class="num">0/20</div><div class="txt"><h3>権限外の漏えい</h3><p>権限外質問20件で、漏えいゼロを目標</p></div></div></div><p class="sub">更新は翌営業日までに反映する。数値は実績ではなく試行の目標です。</p></div>',
        '<div class="inner"><span class="tag">最初の一歩</span><h1>小さく試して、<span class="accent-o">継続を決める</span></h1><p class="sub">対象30件と、文書を確認する担当者を決める。<br>品質・権限・運用が揃ってから利用を広げる。</p><div class="compare"><div class="cmp old"><h3>試行中</h3><p>結果と不具合を記録する</p></div><div class="cmp new"><h3>導入判断</h3><p>改善項目と担当を決める</p></div></div></div>']
    sections = '\n'.join('<section class="slide' + (' active' if i == 0 else '') + '" data-slide-id="page-' + str(i + 1) + '">' + body + '</section>' for i, body in enumerate(bodies))
    # The source's initial comment itself contains example deck/title tags. Scope splices to real elements.
    body_start=doc.index('<body>')
    start=doc.index('<div class="deck">',body_start)
    end=doc.index('<div class="nav',start)
    doc=doc[:start]+'<div class="deck">'+sections+'</div>\n'+doc[end:]
    head_start=doc.index('<head>')
    doc=doc[:head_start]+re.sub(r'<title>.*?</title>', '<title>' + p.title + '</title>', doc[head_start:], count=1)
    # The Japanese adaptation preserves upstream styling; only the script integration and font layer are appended.
    component_css = next(block for block in re.findall(r'```css\s*\n(.*?)```', read(p.up / 'skill/components.md'), re.S) if '.list-grid' in block)
    css = p.latin_fonts(['Space Grotesk']) + component_css + "\nbody{font-family:'Yebisu Noto Sans JP','Noto Sans SC',sans-serif}.item .num{font-size:30px;min-width:98px}.item .txt h3{font-size:22px;margin:0 0 12px}.item .txt p{font-size:18px;line-height:1.6}.item{padding:26px}.cmp p,.layer p,.step .desc,.sub{font-size:20px;line-height:1.65}"
    write(p.out / 'index.html', append_assets(doc, p, css, 'go(0);'+bridge('go(n);')))
    return p.finish(KNOWLEDGE_TITLES, KNOWLEDGE_NOTES, use_case='技術企画')

def bento():
    titles = [KNOWLEDGE_TITLES[0], KNOWLEDGE_TITLES[1], '権限を確かめてから、検索する', '出典を付けて、回答する', '答えと権限を、別々に確かめる', KNOWLEDGE_TITLES[5]]
    notes = list(KNOWLEDGE_NOTES)
    notes[3] = '回答には根拠となった文書を添え、利用者が原文を確かめられるようにします。検索結果を自動承認せず、出典と回答の対応を人が確認します。'
    notes[5] += ' 1週目に整理、2週目に試作、3週目に評価、4週目に継続の判断を行います。'
    p = Production('joeseesun/qiaomu-bento-ppt', 'qiaomu-bento', 'knowledge', KNOWLEDGE_TITLES[0], 'bento/slides / morph + native table',
        '原典の固定Bento shell・文書スキーマを使用。bento_deck.pyでJSONを検証し、シェルを変えずに編集版と再生版の.bento.htmlを構築。検索の同一要素が権限確認から回答へ移るmorphを制作。',
        'json_document_and_pinned_bento_shell', ['SKILL.md', 'references/workflow.md', 'references/upstream-contract.md', 'references/upstream/bento-format.md', 'references/upstream/bento-agents.md', 'scripts/bento_deck.py', 'upstream.lock.json', 'NOTICE.md', 'LICENSE'])
    def text(ident, value, x, y, w, h, size=34, weight=500, color='#F2F0EA', fx=None):
        e={'id':ident,'type':'text','x':x,'y':y,'w':w,'h':h,'rotation':0,'opacity':1,'html':value,'fontSize':size,'fontFamily':'Yebisu Noto Sans JP','fontWeight':weight,'color':color,'align':'left','valign':'top','lineHeight':1.35}
        if fx:e['fx']=fx
        return e
    def shape(ident,x,y,w,h,fill,fx=None):
        e={'id':ident,'type':'shape','shape':'rect','x':x,'y':y,'w':w,'h':h,'rotation':0,'opacity':1,'fill':fill,'stroke':'transparent','strokeWidth':0,'radius':0}
        if fx:e['fx']=fx
        return e
    def table(ident, cells, x=96,y=235,w=1088,h=320):
        return {'id':ident,'type':'table','x':x,'y':y,'w':w,'h':h,'rotation':0,'opacity':1,'columns':[{'w':1} for _ in cells[0]],'rows':[{'cells':[{'html':value,'align':'left','bold':i==0} for value in row]} for i,row in enumerate(cells)],'header':True,'style':{'headerBg':'#255A50','headerColor':'#FFFFFF','zebra':True,'borderColor':'#4A5C58','borderWidth':1,'cellPadX':20,'cellPadY':18,'fontSize':27,'color':'#F2F0EA','radius':0}}
    slides=[]
    slides.append({'id':'s1','name':KNOWLEDGE_TITLES[0],'background':'#101B19','transition':'fade','notes':KNOWLEDGE_NOTES[0],'elements':[
        shape('ambient-rule',96,130,1088,8,'#66D1AF',{'loop':{'type':'motion-path','path':'M0 0 L0 12 L0 0','duration':5,'ease':'sine.inOut'}}),
        text('cover-title','社内検索を<br>4週間で試す',96,240,1088,230,78,800),text('cover-sub','50人の会社・社内文書30件から始める',96,500,1088,75,32),text('fiction','架空の条件による企画例',96,640,1088,40,22,400,'#B8CFC7')]})
    slides.append({'id':'s2','name':KNOWLEDGE_TITLES[1],'background':'#101B19','transition':'fade','notes':KNOWLEDGE_NOTES[1],'elements':[
        text('title',KNOWLEDGE_TITLES[1],96,76,1088,130,48,750),
        table('scope-table',[['今の困りごと','試す範囲'],['保存先がばらばら','対象文書30件を整理'],['同じ質問が繰り返される','出典付きの回答を提示'],['どの版が新しいか分からない','更新反映の期限を決める']]),
        text('scope-note','人の判断を助けるところから試す',96,610,1088,55,29,500,'#66D1AF',{'enter':'fade-up','order':1})]})
    for k in [0,1]:
        elements=[text('title', '権限を確かめてから、検索する' if k==0 else '出典を付けて、回答する',96,76,1088,130,49,750)]
        for i,label in enumerate(['利用者','検索','回答']):
            x=96+i*374
            elements.extend([shape('node-'+str(i),x,265,310,190,'#1E3932'),text('node-label-'+str(i),label,x+28,325,254,80,42,700)])
        elements.extend([shape('flow-highlight',96 if k==0 else 844,265,310,8,'#66D1AF'),text('flow-description','閲覧できる文書だけを候補へ' if k==0 else '根拠の文書を添えて回答する',96,530,1088,80,39,600,'#66D1AF')])
        slides.append({'id':'s'+str(k+3),'name':KNOWLEDGE_TITLES[k+2],'background':'#101B19','transition':'morph','notes':KNOWLEDGE_NOTES[k+2],'elements':elements})
    slides.append({'id':'s5','name':KNOWLEDGE_TITLES[4],'background':'#101B19','transition':'fade','notes':KNOWLEDGE_NOTES[4],'elements':[
        text('title','答えと権限を、別々に確かめる',96,76,1088,130,49,750),table('evaluation',[['観点','試行で測る目標'],['根拠の提示','評価質問30件中24件以上'],['権限外の漏えい','権限外質問20件で0件'],['更新の反映','翌営業日までに反映']]),text('target-note','目標値です。実績や達成を示す数値ではありません。',96,610,1088,55,25,450,'#B8CFC7')]})
    slides.append({'id':'s6','name':KNOWLEDGE_TITLES[5],'background':'#101B19','transition':'fade','notes':KNOWLEDGE_NOTES[5],'elements':[
        text('title','小さく試して、<br>継続を決める',96,110,1088,220,74,800),text('next-action','最初の一歩：対象30件と、確認する担当者を決める',96,390,1088,120,37,550,'#66D1AF',{'enter':'fade-up','order':1}),text('pilot-weeks','整理 / 試作 / 評価 / 判断',96,565,1088,60,30,400)]})
    for i, slide in enumerate(slides):
        slide['name'], slide['notes'] = titles[i], notes[i]
    p.fonts(json.dumps(slides,ensure_ascii=False))
    doc={'format':'bento/slides','version':1,'title':p.title,'size':{'width':1280,'height':720},'theme':{'background':'#101B19','color':'#F2F0EA','accent':'#66D1AF','fontFamily':'Yebisu Noto Sans JP'},'slides':slides,'modified':'2026-10-13T00:00:00Z','assets':{'jp-font':'data:font/woff2;base64,'+base64.b64encode((p.out/'fonts/noto-sans-jp.woff2').read_bytes()).decode()},'fonts':[{'family':'Yebisu Noto Sans JP','asset':'jp-font','weight':'100 900'}]}
    old=p.out/'deck.json'
    # Preserve the entire existing document, including unknown fields and stable IDs.
    if old.exists():
        doc=json.loads(read(old))
    else:
        doc['docId']=str(uuid.uuid4());dump(old,doc)
    helper=p.out/'source/rebuild_bento.py'
    if not helper.exists():raise RuntimeError('Bento case requires source/rebuild_bento.py; do not overwrite an identity source.')
    destination=p.out/'rebuilds'/('build-'+uuid.uuid4().hex[:10])
    p.run(['python',helper,'--input',old,'--output-dir',destination])
    for name in ['deck.json','player.json','deck.bento.html','player.bento.html']:
        shutil.copy2(destination/name,p.out/name)
    shutil.copy2(destination/'noto-sans-jp.woff2',p.out/'fonts/noto-sans-jp.woff2')
    write(p.out/'deck-plan.md','# 社内検索を4週間で試す\n\n3役の位置は固定し、3→4頁で同じ文書トークンが権限確認から回答と出典へ移る。固定Bento shellは変更せず、全JSONを保存して別出力へbuildする。\n')
    shutil.copyfile(p.up/'NOTICE.md',p.out/'NOTICE.md')
    shutil.copyfile(p.up/'THIRD_PARTY_LICENSES/bento-MIT.txt',p.out/'LICENSE.bento')
    return p.finish(titles,notes,preview='player.bento.html',use_case='業務改善・動き付き説明',extra={'navigation':'native-keyboard','editable_artifact':rel(p.out/'deck.bento.html')})

def kuneosu():
    p=Production('Kuneosu/make-slide','make-slide','ec','9月ECレポート：売上と返品を確認する','Data Focus / CSS charts',
        '原典Data Focus/reference.htmlの表紙・指標・比較・棒グラフ・ドーナツ・プロセス・結びを複製して本文・数値へ差し替え。原典CSSとGo/notesのナビゲーションを保持。チャートの高さと角度を入力から計算。',
        'theme_reference_html_and_instruction_skill',['SKILL.md','themes/data-focus/reference.html','themes/data-focus/README.md','LICENSE'])
    soup=BeautifulSoup(read(p.up/'themes/data-focus/reference.html'),'html.parser')
    source_slides=soup.select('.deck>.slide')
    chosen=[source_slides[i] for i in [0,6,4,7,8,2,5,11]]
    titles=['9月ECレポート','売上は20%増え、返品率も上がった','粗利額は増え、粗利率は下がった','自然検索と直訪で売上の62.5%を占める','売上の構成を、チャネルで見る','返品率の上昇は、原因を確かめる','返品理由と商品構成を、順に確認する','次月は、返品と粗利率を追う']
    notes=['架空のEC事業を想定した月次報告の作例です。','売上1200万円、注文4000件の設定です。売上の成長と品質指標を一緒に確認します。','前年は1000万円×38%=380万円、当月は1200万円×36%=432万円です。額は52万円増えても、率は2ポイント下がっています。','自然検索390と直訪360の合計は750万円、1200万円の62.5%です。','240/390/210/360万円の合計は1200万円、構成比は20/32.5/17.5/30%です。','返品率は4%から6%へ2ポイント上昇。商品説明と実物の差などは、原因を確かめるための仮説です。','返品理由を分類してから、商品説明と商品構成を確認します。実施済みという報告ではありません。','次月は返品理由と粗利率の変化を確認し、対策の判断材料を揃えます。']
    def put(s,selector,value):
        el=s.select_one(selector)
        if el is None:raise ValueError('Missing Data Focus slot: '+selector)
        el.clear();el.append(BeautifulSoup(value,'html.parser'))
    put(chosen[0],'h1','9月EC<br>レポート')
    put(chosen[0],'.overline','MONTHLY REPORT / 架空の事業例')
    put(chosen[0],'.sub','売上・粗利・返品を、数字から確かめる')
    for i,s in enumerate(chosen[1:]):
        heading=s.select_one('h2')
        if heading:heading.string=titles[i+1]
        tag=s.select_one('.tag')
        if tag:tag.string=['月次指標','前年との比較','チャネル別売上','売上構成','返品の確認','次月の対応','次の一歩'][i]
    for card,label,value,trend,good in zip(chosen[1].select('.stat-card'),['売上 / 万円','注文数 / 件','粗利率','返品率'],['1,200','4,000','36%','6%'],['前年から20%増','前年から500件増','前年から2ポイント低下','前年から2ポイント上昇'],[True,True,False,False]):
        card.select_one('.stat-label').string=label
        card.select_one('.stat-value').string=value
        tr=card.select_one('.stat-trend');tr.string=trend;tr['class']=['stat-trend','up' if good else 'down']
    for col,label,items in zip(chosen[2].select('.cmp-col'),['前年9月','当月9月'],[['売上 1,000万円','粗利率 38%','粗利額 380万円'],['売上 1,200万円','粗利率 36%','粗利額 432万円']]):
        col.select_one('.cmp-label').string=label
        put(col,'ul',''.join('<li>'+v+'</li>' for v in items))
    channels=p.input['channels']
    colors=['#2563EB','#10B981','#F59E0B','#EF4444']
    for bar,channel,color in zip(chosen[3].select('.bar-group'),channels,colors):
        bar.select_one('.bar-value').string=str(channel['sales_man_yen'])+'万円'
        bar.select_one('.bar-label').string=channel['name']
        el=bar.select_one('.bar');el['style']=re.sub(r'height:[^;]+', 'height:'+str(round(channel['sales_man_yen']/500*240))+'px',el['style'])+';background:'+color
    for bar in chosen[3].select('.bar-group')[len(channels):]:bar.decompose()
    for axis,value in zip(chosen[3].select('.chart-grid-val'),['500万円','375','250','125','0']):axis.string=value
    put(chosen[3],'.body','自然検索390万円 + リピート直訪360万円 = <span class="hi">750万円 / 売上の62.5%</span>')
    colors=['#2563EB','#10B981','#F59E0B','#EF4444'];bounds=[0,72,189,252,360]
    chosen[4].select_one('.donut')['style']='background:conic-gradient('+','.join(colors[i]+' '+str(bounds[i])+'deg '+str(bounds[i+1])+'deg' for i in range(4))+')'
    put(chosen[4],'.donut-total','1,200')
    put(chosen[4],'.donut-total-label','売上 / 万円')
    for row,channel,color in zip(chosen[4].select('.legend-item'),channels,colors):
        row.select_one('.legend-label').string=channel['name']
        row.select_one('.legend-value').string=str(channel['sales_man_yen']/12).rstrip('0').rstrip('.')+'%'
        row.select_one('.legend-dot')['style']='background:'+color
    for row in chosen[4].select('.legend-item')[4:]:row.decompose()
    put(chosen[5],'.body','返品率は <span class="hi">4%から6%へ、2ポイント上昇</span>。<br>返品理由を商品ごとに分類する。<br>説明と実物の差は、まだ確認前の仮説。')
    for step,label,sub in zip(chosen[6].select('.step'),['分類','確認','分析','判断'],['返品の理由','商品説明の差','値引きと構成','次月の対策']):
        step.select_one('.step-label').string=label;step.select_one('.step-sub').string=sub
    put(chosen[6],'.body','返品と粗利率の変化を、次月の重点にする。')
    end=chosen[7]
    for el in end.select('.a'):
        if 'tag' in el.get('class',[]):el.string='次の一歩'
        elif el.name in ['h1','h2']:el.string=titles[7]
        elif 'sub' in el.get('class',[]):el.string='返品理由と粗利率を、次月も確認する。'
        else:el.string='架空の事業例 / Data Focus'
    deck=soup.select_one('.deck');deck.clear()
    for i,s in enumerate(chosen):
        s['data-notes']=notes[i];s['class']=['slide']+(['active'] if i==0 else []);s['data-slide-id']='page-'+str(i+1);deck.append(s)
    soup.title.string=p.title;soup.html['lang']='ja'
    # No code slide is used; its optional CDN syntax-highlighting resources are unnecessary.
    for el in soup.select('link[href],script[src]'):
        if 'prism' in (el.get('href','')+el.get('src','')).lower():el.decompose()
    doc=str(soup)
    doc=doc.replace('  function go(to) {','  window.yebisuNativeGo=go;\n  function go(to) {',1)
    css=p.latin_fonts(['JetBrains Mono'])+"\nbody{font-family:'Yebisu Noto Sans JP',sans-serif}.hint,.fullscreen-btn{font-family:'Yebisu Noto Sans JP',sans-serif}"
    write(p.out/'index.html',append_assets(doc,p,css,bridge('if(window.yebisuNativeGo)window.yebisuNativeGo(n);')))
    write(p.out/'script.md','\n\n'.join('## '+str(i+1)+'. '+t+'\n\n'+n for i,(t,n) in enumerate(zip(titles,notes))))
    return p.finish(titles,notes,use_case='月次報告')

def editable():
    p=Production('archlizheng/frontend-slides-editable','frontend-editable','knowledge',KNOWLEDGE_TITLES[0],'Editable reference / object editor',
        '原典editable-deck-reference.htmlのSlideDeck/SlideObjectEditor/SlideSidebarをそのまま使い、slide-edit-layerとdata-oid付きオブジェクトで日本語6ページを制作。ドラッグ・編集・保存機能のある原典runtimeを保持。',
        'instruction_skill_and_original_editable_runtime',['SKILL.md','editor-runtime.md','html-template.md','examples/editable-deck-reference.html','LICENSE'])
    soup=BeautifulSoup(read(p.up/'examples/editable-deck-reference.html'),'html.parser')
    source=soup.select_one('.slides-offset>section.slide')
    headings=['社内検索を4週間で試す','探せる場所を、最初につくる','権限を確かめてから検索する','4週間で導入判断へ進む','正しさと権限を別々に測る','小さく試して、継続を決める']
    bodies=['50人の会社・対象文書30件<br><br>架空の条件による企画例',
            '保存先が散らばり、同じ質問が繰り返される。<br><br>対象30件を整理して、出典付きの検索を試す。',
            '利用者の所属とアクセス権限を確認。<br><br>閲覧できる文書だけを検索候補へ。<br><br>回答には根拠の出典を添える。',
            '1週目：文書と権限を整理<br>2週目：出典付き検索を試作<br>3週目：品質と権限を評価<br>4週目：継続の条件を判断',
            '根拠を示せる質問：30件中24件以上<br>権限外の漏えい：20件で0件<br>更新の反映：翌営業日まで<br><br>これらは試行で測る目標値。',
            '最初の一歩：対象30件と、確認する担当者を決める。<br><br>品質・権限・運用が揃ってから利用を広げる。']
    slides=[]
    for i,(title,body) in enumerate(zip(headings,bodies)):
        s=BeautifulSoup(str(source),'html.parser').section
        s['id']='slide-'+str(i);s['class']=['slide']+(['visible'] if i==0 else [])
        objects=s.select('[data-slide-object]')
        for j,obj in enumerate(objects):obj['data-oid']='s'+str(i)+'-o'+str(j)
        objects[0]['style']='left:8%;top:14%;width:84%;'
        title_el=objects[0].select_one('.slide-object-text');title_el.clear();title_el.append(title);title_el['style']='font-size:64px;font-weight:700;line-height:1.35'
        objects[1]['style']='left:8%;top:38%;width:84%;'
        content=objects[1].select_one('.slide-object-text');content.clear();content.append(BeautifulSoup(body,'html.parser'));content['style']='font-size:36px;line-height:1.65'
        # The original illustrative empty graphic is not part of the business content.
        objects[2].decompose()
        slides.append(s)
    deck=soup.select_one('.slides-offset');deck.clear()
    for s in slides:deck.append(s)
    soup.title.string=p.title;soup.html['lang']='ja';soup.html['data-deck-id']='yebisu-knowledge-editable'
    for el in soup.select('link[href]'):
        if 'fontshare' in el['href']:el.decompose()
    doc=str(soup)
    # Call the original runtime's go method from the parent float player; editing code stays intact.
    doc=doc.replace('  const deck = new SlideDeck();','  const deck = new SlideDeck();\n  window.yebisuNativeDeck=deck;',1)
    css=":root{--font-display:'Yebisu Noto Sans JP',sans-serif;--font-body:'Yebisu Noto Sans JP',sans-serif}.slide-object-text{font-family:'Yebisu Noto Sans JP',sans-serif}"
    write(p.out/'index.html',append_assets(doc,p,css,bridge('if(window.yebisuNativeDeck)window.yebisuNativeDeck.goTo(n);')))
    return p.finish(headings,KNOWLEDGE_NOTES,use_case='企画・編集可能なWeb資料')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pipelines', nargs='*', choices=['reveal', 'lewis', 'minorun', 'dashi', 'neon', 'bento','kuneosu','editable'])
    args = parser.parse_args()
    targets = args.pipelines or ['reveal', 'lewis', 'minorun']
    path = ROOT / 'data/web-repository-examples.json'
    examples = json.loads(read(path)) if path.exists() else []
    for name in targets:
        card = globals()[name]()
        examples = [x for x in examples if x['id'] != card['id']] + [card]
        dump(path, examples)
        print(card['repository'] + ': ' + str(card['page_count']) + ' actual Japanese pages generated', flush=True)
