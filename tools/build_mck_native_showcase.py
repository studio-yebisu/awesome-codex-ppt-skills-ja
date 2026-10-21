"""『フォント構成と制作手順』— likaku/Mck-ppt-design-skill の MckEngine 標準版式で作る4ページ。

原典SKILLの五段階に沿って S1 brief → S2 outline → S3 content を先に書き、
S3 は原典 gate_check_s3.py、S4 は原典 gate_check.py を改変せずに subprocess で実行し、
書き出された JSON の passed だけで次へ進む。描画は MckEngine の cover / grouped_bar /
data_table / value_chain をそのまま呼ぶ。上書きや自作 renderer は使わない。

原典constantsの書体名をプロセス内で日本語書体へ指定する。生成後の図形や文字を
置換しない。実データの分類・言語を保持して公開APIへ渡す。原典ファイルは不変。
"""
from collections import Counter
from pathlib import Path
import argparse, hashlib, importlib.util, inspect, json, os, re, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
ZIP_MODE = (ROOT / 'upstream/mck_ppt').exists()
UPSTREAM_CANDIDATES = [
    ROOT / 'upstream',                                            # 配布ZIPの同梱原典
    ROOT / '.build/actual-upstreams/likaku__Mck-ppt-design-skill',  # repoの固定取得物
    ROOT / 'skill-forks/sol-editorial-ja/upstream',               # repoに保存済みの同一commit
]
UPSTREAM_REQUIRED = ['mck_ppt/__init__.py', 'mck_ppt/constants.py', 'mck_ppt/core.py', 'mck_ppt/engine.py',
                     'mck_ppt/qa.py', 'references/scripts/gate_check_s3.py', 'references/scripts/gate_check.py',
                     'references/layout-matrix.yaml']
LAYOUTS = ('cover', 'grouped_bar', 'data_table', 'value_chain')
PROJECT_DIR = 'ppt-project-font-kit'  # 原典SKILLの ppt-project-{slug}/ 規約


def fail(stage, message):
    print(f'[{stage}] 失敗: {message}', file=sys.stderr)
    sys.exit(1)


def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p, s): p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8')
def dump(p, v): write(p, json.dumps(v, ensure_ascii=False, indent=2) + '\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return Path(p).resolve().relative_to(ROOT).as_posix()
def first_existing(paths): return next((p for p in paths if p.exists()), None)


def find_upstream():
    for up in UPSTREAM_CANDIDATES:
        if all((up / f).exists() for f in UPSTREAM_REQUIRED):
            return up
    fail('setup', '原典 likaku/Mck-ppt-design-skill が見つかりません: ' + ', '.join(rel(p) for p in UPSTREAM_CANDIDATES))


def upstream_identity(up):
    for meta in (up / 'ACQUISITION.json', up.parent / 'SOURCE.json', up / 'SOURCE.json'):
        if meta.exists():
            d = load(meta)
            if d.get('repository') and d.get('commit'):
                return {'repository': d['repository'], 'commit': d['commit']}  # root等の絶対パスは持ち出さない
    return {'repository': 'likaku/Mck-ppt-design-skill', 'commit': None}


def load_engine(up, fonts):
    """原典constantsを読み、実在する名前だけ差し替えてから原典パッケージを読み込む。"""
    if 'mck_ppt' in sys.modules:
        fail('setup', 'mck_ppt が既に読み込まれています。新しいプロセスで実行してください')
    spec = importlib.util.spec_from_file_location('mck_ppt.constants', up / 'mck_ppt/constants.py')
    const = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(const)
    for name, value in fonts.items():
        if not isinstance(getattr(const, name, None), str):
            fail('setup', f'原典constantsに書体名 {name} がありません')
        setattr(const, name, value)
    sys.modules['mck_ppt.constants'] = const
    sys.path.insert(0, str(up))
    import mck_ppt, mck_ppt.core as core, mck_ppt.engine as engine
    if Path(mck_ppt.__file__).resolve().parent != (up / 'mck_ppt').resolve():
        fail('setup', '固定原典以外の mck_ppt が読み込まれました')
    defaults = inspect.signature(core.add_text).parameters
    if (engine.FONT_HEADER, defaults['font_name'].default, defaults['ea_font'].default) != \
            (fonts['FONT_HEADER'], fonts['FONT_BODY'], fonts['FONT_EA']):
        fail('setup', '書体名の局所指定が原典エンジンに反映されていません')
    return engine.MckEngine, const


def read_layout_matrix(path):
    """layout-matrix.yaml の Layout Capacity Matrix 表を読む。"""
    out = {}
    row = re.compile(r'^\|\s*`(\w+)`\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|')
    for line in path.read_text(encoding='utf-8').splitlines():
        m = row.match(line)
        if not m:
            continue
        name, _, items, title, body = m.groups()
        n = re.search(r'(\d+)', items)
        out[name] = {'max_items': int(n.group(1)) if n else None,
                     'title': int(title) if title.isdigit() else None,
                     'body': {k.strip(): int(v) for k, v in re.findall(r'([^,:]+?):\s*(\d+)', body)}}
    return out


# ─── S1 ──────────────────────────────────────────────────────────────

def font_stats(data, plan):
    langs, cats = list(plan['languages']), list(plan['categories'])
    fams = data['families']
    if not fams:
        fail('S1', 'フォントデータの families が空です')
    ids = [f['id'] for f in fams]
    if len(ids) != len(set(ids)):
        fail('S1', 'フォントデータの id が重複しています')
    names = [f['family'] for f in fams]
    if len(names) != len(set(names)):
        fail('S1', 'フォントデータの family 名が重複しています')
    unknown = sorted({f['language'] for f in fams} - set(langs)) + sorted({f['category'] for f in fams} - set(cats))
    if unknown:
        fail('S1', f'plan.json に表示名がない language/category: {unknown}')
    by_lang = Counter(f['language'] for f in fams)
    by_cat = Counter(f['category'] for f in fams)
    cross = Counter((f['category'], f['language']) for f in fams)
    order = sorted((c for c in cats if by_cat[c]), key=lambda c: (-by_cat[c], cats.index(c)))
    first = {}
    for f in fams:
        first.setdefault((f['category'], f['language']), f['family'])
    exclusive = [(c, l) for c in order for l in langs if cross[(c, l)] == by_cat[c]]
    family_lang = {f['family']: f['language'] for f in fams}
    presets = data.get('presets', [])
    for preset in presets:
        for role in ('heading', 'body', 'latin', 'code'):
            family = preset.get(role)
            if (role != 'code' or family) and family not in family_lang:
                fail('S1', f'プリセットの {role} が収録字体を参照していません: {family}')
    split = bool(presets) and all(family_lang.get(p.get('heading')) == 'ja' and family_lang.get(p.get('body')) == 'ja'
                                  and family_lang.get(p.get('latin')) == 'latin' for p in presets)
    return {'total': len(fams), 'files': sum(len(f['files']) for f in fams),
            'updated_on': data.get('updated_on', ''), 'langs': langs, 'order': order,
            'by_lang': by_lang, 'by_cat': by_cat, 'cross': cross, 'first': first, 'exclusive': exclusive,
            'presets': len(presets), 'presets_split': split}


def summary_json(st):
    return {'family_count': st['total'], 'font_file_record_count': st['files'], 'updated_on': st['updated_on'],
            'by_language': {l: st['by_lang'][l] for l in st['langs']},
            'by_category': {c: st['by_cat'][c] for c in st['order']},
            'by_category_language': {c: {l: st['cross'][(c, l)] for l in st['langs']} for c in st['order']},
            'preset_count': st['presets'], 'presets_all_ja_with_latin': st['presets_split']}


def write_brief(path, plan, st):
    L, K = plan['languages'], plan['categories']
    top = st['order'][0]
    messages = [
        f"収録は{st['total']}字体（" + '・'.join(f"{L[l]}{st['by_lang'][l]}" for l in st['langs']) + '）',
        f"分類別の最多は{K[top]}の{st['by_cat'][top]}字体",
        '、'.join(f'{K[c]}は{L[l]}のみ' for c, l in st['exclusive']) or '各分類に複数の言語がある',
        '制作は要件→構成→原稿→描画・検査→交付・経験記録の順。所要時間は計測していない',
    ]
    b = plan['brief']
    if not (b.get('audience') and b.get('goal') and messages):
        fail('S1', 'audience / goal / key_messages のいずれかが空です')
    fonts = ' / '.join(f'{k}={v}' for k, v in plan['fonts'].items())
    write(path, f"# {plan['title']} — brief\n\n"
                f"- 受け手（audience）: {b['audience']}\n"
                f"- 目的（goal）: {b['goal']}\n"
                f"- 時間: {b['duration_minutes']}分 / 4ページ\n"
                f"- 主要メッセージ（key_messages）:\n" + ''.join(f'  {i}. {m}\n' for i, m in enumerate(messages, 1)) +
                f"- データ: {b['data_source']}（{st['updated_on']}更新）\n"
                f"- 扱わないもの: {b['exclusions']}\n"
                f"- 書体: 原典constantsの {fonts} をこの生成プロセス内でだけ指定\n")
    return messages


# ─── S2 / S3 ─────────────────────────────────────────────────────────

def build_content(plan, st):
    L, K = plan['languages'], plan['categories']
    fmt = {'total':st['total'],'file_count':st['files'],'preset_count':st['presets'],'updated_on':st['updated_on']}
    fmt.update({f'{l}_count':st['by_lang'][l] for l in st['langs']})
    chart,t,p = plan['grouped_bar'],plan['table'],plan['process']
    widths=t['col_widths_in']
    if len(widths)!=len(st['langs'])+3: fail('S3','table.col_widths_in の列数が表と一致しません')
    headers=[t['headers']['category'],*(L[l] for l in st['langs']),t['headers']['total'],t['headers']['sample']]
    rows=[[K[c],*(str(st['cross'][(c,l)]) for l in st['langs']),str(st['by_cat'][c]),
           '\n'.join(f"{L[l]}：{st['first'].get((c,l),'該当なし')}" for l in st['langs'])] for c in st['order']]
    rows.append([t['total_label'],*(str(st['by_lang'][l]) for l in st['langs']),str(st['total']),'—'])
    table_title=(t['title_prefix']+'、'.join(f'{K[c]}は{L[l]}のみ' for c,l in st['exclusive']) if st['exclusive'] else t['title_fallback'])
    table_bar=[t['bottom_bar_label'],t['presets_split'].format(n=st['presets'])] if st['presets_split'] else None
    values=[[st['cross'][(c,l)] for l in st['langs']] for c in st['order']]
    maximum=max(max(row) for row in values)
    stages=[(title,desc.replace('｜','\n'),p['color']) for title,(_,_,desc) in zip(p['stage_titles'],p['steps'])]
    if len(stages)!=len(p['steps']):fail('S3','process stage_titles and steps differ')
    return [
        {'idx':1,'layout':'cover','title':plan['cover'].get('title',plan['title']).format(**fmt),'key_point':'',
         'subtitle':plan['cover']['subtitle'].format(**fmt),'author':plan['cover']['author'].format(**fmt),'date':plan['cover']['date'].format(**fmt)},
        {'idx':2,'layout':'grouped_bar','title':chart['title'],
         'key_point':'元の分類と言語を保ち、実カタログの字体数を整数で比べる',
         'categories':[K[c] for c in st['order']],'series':[(L[l],chart['colors'][i]) for i,l in enumerate(st['langs'])],
         'data':values,'max_val':maximum,'y_ticks':list(range(maximum+1)),
         'summary':[chart['summary_label'], '・'.join(f"{L[l]}{st['by_lang'][l]}字体" for l in st['langs'])+f"＝計{st['total']}字体。元{len(st['order'])}分類をそのまま比較。"],
         'source':chart['source']},
        {'idx':3,'layout':'data_table','title':table_title,'key_point':'分類ごとに日本語と欧文の字体数を分け、代表書体を添える',
         'headers':headers,'rows':rows,'col_widths':widths,'bottom_bar':table_bar,'source':t['source'].format(**fmt)},
        {'idx':4,'layout':'value_chain','title':p['title'],
         'key_point':'実際の五段階と保存ファイルを横方向へ対応し、S5の固定fixtureを明示する',
         'stages':stages,'bottom_bar':p['bottom_bar'],'source':p['source']},
    ]


def count_checks(st, slides):
    """Source-count invariants; no download/glyph/font-quality claim."""
    chart,table=slides[1],slides[2]
    expected=[[st['cross'][(c,l)] for l in st['langs']] for c in st['order']]
    checks={'language_counts_sum_to_families':sum(st['by_lang'].values())==st['total'],
        'category_counts_sum_to_families':sum(st['by_cat'].values())==st['total'],
        'cross_counts_sum_to_families':sum(st['cross'].values())==st['total'],
        'chart_exact_source_cross_counts':chart['data']==expected,
        'chart_counts_sum_to_families':sum(sum(row) for row in chart['data'])==st['total'],
        'table_category_totals_match_source':[int(row[-2]) for row in table['rows'][:-1]]==[st['by_cat'][c] for c in st['order']],
        'table_language_totals_match_source':[int(x) for x in table['rows'][-1][1:-2]]==[st['by_lang'][l] for l in st['langs']],
        'table_family_total_matches_source':int(table['rows'][-1][-2])==st['total'],
        'five_actual_steps_retained':len(slides[3]['stages'])==5}
    return {'passed':all(checks.values()),'checks':checks,**summary_json(st),'chart_data':chart['data'],
        'computed_chart_summary':chart['summary'],
        'scope':'Counts of catalog metadata records. Not download, glyph-coverage, font-quality or arbitrary-document conversion proof.'}


def check_outline(outline, matrix):
    """原典SKILLのS2門禁（AI自評項目）をコードで確認する。動詞の有無は判定しない。"""
    slides, minutes = outline['slides'], outline['brief']['duration_minutes']
    issues = []
    if not any(s['layout'] == 'cover' for s in slides):
        issues.append('cover がありません')
    if len(slides) > minutes * 1.2:
        issues.append(f'{len(slides)}ページは {minutes}分×1.2 を超えます')
    issues += [f"{s['idx']}: {s['layout']} は layout-matrix.yaml にありません" for s in slides if s['layout'] not in matrix]
    issues += [f"{s['idx']}: Action Title が10字以下" for s in slides if s['layout'] != 'cover' and len(s['title']) <= 10]
    if sum(s['layout'] == 'two_column_text' for s in slides) > 1:
        issues.append('two_column_text が2枚以上あります')
    return issues


def budget_issues(slide, matrix):
    """Original matrix capacity checks before unchanged upstream S3."""
    m,lay,out=matrix[slide['layout']],slide['layout'],[]
    def over(field,text,limit):
        n=len(str(text).replace('\n',''))
        if limit is not None and n>limit:out.append(f"slide {slide['idx']} {lay} {field}: {n}>{limit}字")
    over('title',slide['title'],m['title']);b=m['body']
    if lay=='cover':
        over('subtitle',slide['subtitle'],b.get('subtitle'));over('author',slide['author'],b.get('author'))
    elif lay=='data_table':
        for h in slide['headers']:over('header',h,b.get('header'))
        for row in slide['rows']:
            for cell in row:over('cell',cell,b.get('cell'))
        if len(slide['rows'])>m['max_items']:out.append('data_table capacity exceeded')
    elif lay=='grouped_bar':
        if len(slide['categories'])>6 or len(slide['series'])>3:out.append('grouped_bar capacity exceeded')
        for label in slide['categories']:over('category',label,8)
        for label,_ in slide['series']:over('series',label,15)
        if len(slide['data'])!=len(slide['categories']) or any(len(row)!=len(slide['series']) for row in slide['data']):out.append('grouped_bar data dimensions differ')
    elif lay=='value_chain':
        if len(slide['stages'])>m['max_items']:out.append('value_chain capacity exceeded')
        for title,desc,_ in slide['stages']:
            over('stage title',title,15);over('desc',desc,60)
    return out


def method_kwargs(slide, const):
    """Convert documented high-level inputs, without touching engine output."""
    from pptx.util import Inches
    kw={k:v for k,v in slide.items() if k not in ('idx','layout','key_point')}
    for field in ('series','stages'):
        if field in kw:
            colors=[item[-1] for item in kw[field]]
            if any(not hasattr(const,color) for color in colors):fail('S3','原典constantsに指定色がありません')
            kw[field]=[(*item[:-1],getattr(const,item[-1])) for item in kw[field]]
    if 'col_widths' in kw:kw['col_widths']=[Inches(w) for w in kw['col_widths']]
    if kw.get('bottom_bar'):kw['bottom_bar']=tuple(kw['bottom_bar'])
    return kw




# ─── 原典 gate ───────────────────────────────────────────────────────

def run_upstream_script(up, script, args, cwd):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    env['PYTHONPATH'] = os.pathsep.join(filter(None, [str(up), os.environ.get('PYTHONPATH')]))
    proc = subprocess.run([sys.executable, str(up / 'references/scripts' / script), *args], cwd=cwd, env=env,
                          capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(proc.stdout, end='')
    if proc.stderr:
        print(proc.stderr, end='', file=sys.stderr)
    return proc.returncode


def upstream_s3_checkers(up, slides):
    """原典 gate_check_s3.py の LAYOUT_CHECKERS を読み、各ページに掛かる検査名を記録する。"""
    spec = importlib.util.spec_from_file_location('_upstream_gate_s3', up / 'references/scripts/gate_check_s3.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {str(s['idx']): [f.__name__ for f in mod.LAYOUT_CHECKERS.get(s['layout'], [mod.check_source])]
            for s in slides}


def assert_public(paths):
    private = set()
    for base in (ROOT, Path.home()):
        s = str(base)
        private |= {s, s.replace('\\', '/'), json.dumps(s)[1:-1]}
    for p in paths:
        text = p.read_text(encoding='utf-8-sig')
        if any(x in text for x in private):
            fail('S5', f'{rel(p)} に端末固有の絶対パスが含まれています')


def self_refinement(out, project, gate, deck):
    """Replay a fixed repair fixture after the current actual S4; no new judgment."""
    if gate.get('passed') is not True:
        fail('S5', 'S4 passed=true の記録なしには交付記録を作れません')
    experience = out / 'experiences/chart-limits.md'
    write(experience, '# 日本語作例の固定経験記録\n\n'
          'この文書は、作例を修復した際の判断を保存した固定fixtureです。JP-001〜003は過去のdonut/timeline/vertical_steps版の経験で、現版の検査値ではありません。現版はJP-004のgrouped_bar/value_chainです。生成器は同じ記録を再生し、今回のゲート合否・成果物hashだけを実行時に取得します。実行時の新規診断や新しい経験の発見を行いません。\n\n'
          '## Experience JP-001: donut凡例とsummaryの安全な間隔\n'
          '**Date**: 2026-10-16\n'
          '**Problem**: 5分類の凡例最下段とsummaryが接触寸前だった。\n'
          '**Root Cause**: 原典の凡例は1.85+0.78×行、文字箱高0.34インチ。5行目の下端5.31に対しsummaryの上端は5.32で、隙間は0.01インチ。\n'
          '**Fix**: 原典の位置は変えず、元categoryの見出し調4と等幅3を明示して合算し、円を4書体群へ分ける。次頁の表では元の5分類を残し、元値と合計は変更しない。\n'
          '**Rule**: この生成器ではsummary付きdonutを4区分以下に制限。適切な集計が作れなければsummaryを別頁へ分ける。原典gateと免除一覧は変更しない。\n\n'
          '## Experience JP-002: 保持する原典差分と実視覚確認を分ける\n'
          '**Date**: 2026-10-16\n'
          '**Problem**: timeline最終見出しの本文領域右はみ出しを「空文字箱」と誤説明した。\n'
          '**Root Cause**: 原典の免除を実文字の安全領域内配置と混同した。\n'
          '**Fix**: 最終見出しの実文字を確認し、原典whitelistによる免除と本文領域外0.47インチを別に記録する。\n'
          '**Rule**: gateの免除categoryだけで可読性を判定せず、実文字/箱/スライド境界を記録する。原典側の修正なしに「本文領域内」と言わない。\n\n'
          '## Experience JP-003: 工程の保存ファイルは縦順で読む\n'
          '**Date**: 2026-10-16\n'
          '**Problem**: 横タイムラインの下部に大きな余白があり、長い識別子の下線も読み取りづらかった。\n'
          '**Fix**: 原典vertical_stepsの5行へ入力を渡し、保存ファイルと確認行為を同じ行に置いた。S5は固定記録の再生だと頁上でも明示する。元のtimelineエンジンや免除一覧は修正していない。\n'
          '**Rule**: 日付のない工程説明では、時間軸を装うより各段階の入出力を読める原典版式を選ぶ。空白を埋めるために数値や効果を作らない。\n\n'
          '## Experience JP-004: 元の分類を比較し、番号と見出しをそろえる\n'
          '**Date**: 2026-10-16\n'
          '**Problem**: donutの細い輪と余白、vertical_stepsの番号中心と見出し中心の差が残った。\n'
          '**Fix**: 未改変のgrouped_barへ元5分類×2言語の実集計を渡し、整数軸で比較する。value_chainへ実5工程と保存ファイルを渡し、番号と見出しの中心をそろえる。表紙と表の内容・図形は保持する。\n'
          '**Rule**: 原典の別メソッドと公開入力で改善する。peer_font_inconsistency2件は既定免除として記録し、新しい免除を追加しない。value_chain中央下の余白は残り、免除を視覚品質合格の代用にしない。\n')
    state = {'S4_gate_passed': True, 'gate_result': f'{PROJECT_DIR}/gate_result.json',
             'artifact': 'deck.pptx', 'artifact_sha256': sha(deck),
             'delivery_state': 'files_prepared; user adoption and independent review separate',
             'refinement_decision': 'PATTERN',
             'refinement_decision_origin': 'Fixed Codex repair judgment replayed by this dedicated example generator',
             'runtime_new_diagnosis': False, 'record_mode': 'fixed_repair_fixture_replay',
             'experience': 'experiences/chart-limits.md',
             'experience_sha256': sha(experience), 'upstream_experiences_modified': False,
             'preventive_rule': 'Preserve source category/language counts; original API inputs only; retain and explain original gate exclusions separately from visual observations',
             'original_gate_or_whitelist_changed': False}
    dump(project / 'delivery-and-refinement.json', state)
    return state


# ─── main ────────────────────────────────────────────────────────────

def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')  # 原典 save() の絵文字出力対策
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--render', action='store_true', help='Microsoft PowerPointで4ページのPNG/PDFを書き出す')
    ap.add_argument('--font-data', type=Path, help='oss-font-kit.json の場所')
    ap.add_argument('--out', type=Path, help='出力先（既定: repoでは作例フォルダー、配布ZIPでは rebuild/）')
    args = ap.parse_args()

    case_dir = ROOT if ZIP_MODE else ROOT / 'examples/repositories/mck-native-showcase'
    out = (args.out or (ROOT / 'rebuild' if ZIP_MODE else case_dir)).resolve()
    if not out.is_relative_to(ROOT.resolve()):
        fail('setup', '--out は repository / ZIP の中を指定してください')
    plan_path = case_dir / 'input/plan.json'
    data_path = args.font_data or first_existing([ROOT / 'data/oss-font-kit.json', ROOT / 'input/oss-font-kit.json'])
    if not plan_path.exists():
        fail('setup', f'{rel(plan_path)} がありません')
    if not data_path or not Path(data_path).exists():
        fail('setup', 'oss-font-kit.json が見つかりません（--font-data で指定）')
    data_path = Path(data_path).resolve()
    data_label = rel(data_path) if data_path.is_relative_to(ROOT.resolve()) else data_path.name
    plan, data = load(plan_path), load(data_path)
    up = find_upstream()
    MckEngine, const = load_engine(up, plan['fonts'])
    matrix = read_layout_matrix(up / 'references/layout-matrix.yaml')

    project = out / PROJECT_DIR
    deck = out / 'deck.pptx'
    record_path = out / 'build-record.json'
    for stale in (record_path, deck, project / 'gate_s3.json', project / 'gate_result.json'):
        stale.unlink(missing_ok=True)  # 前回の合格結果を残さない

    # S1 brief
    st = font_stats(data, plan)
    messages = write_brief(project / 'brief.md', plan, st)
    print(f"[S1] {st['total']}字体 / " + ', '.join(f"{l}={st['by_lang'][l]}" for l in st['langs']))

    # S2 outline
    slides = build_content(plan, st)
    checked_counts = count_checks(st, slides)
    dump(out / 'font-count-checks.json', checked_counts)
    if not checked_counts['passed']:
        fail('S2', '実フォントカタログの集計と図・表の値が一致しません')
    outline = {'brief': {'audience': plan['brief']['audience'], 'goal': plan['brief']['goal'],
                         'duration_minutes': plan['brief']['duration_minutes'], 'key_messages': messages},
               'slides': [{k: s[k] for k in ('idx', 'layout', 'title', 'key_point')} for s in slides]}
    dump(project / 'outline.json', outline)
    if issues := check_outline(outline, matrix):
        fail('S2', ' / '.join(issues))
    print('[S2] outline: ' + ' → '.join(s['layout'] for s in slides))

    # S3 content + 事前確認 + 原典 gate_check_s3.py
    for s in slides:
        if s['layout'] not in LAYOUTS:
            fail('S3', f"{s['layout']} は今回使う原典メソッドに含めていません")
        try:
            inspect.signature(getattr(MckEngine, s['layout'])).bind(None, **method_kwargs(s, const))
        except TypeError as e:
            fail('S3', f"slide {s['idx']} {s['layout']} の引数が原典メソッドと一致しません: {e}")
    if issues := [i for s in slides for i in budget_issues(s, matrix)]:
        fail('S3', 'layout-matrix.yaml の文字数・項目数を超えています: ' + ' / '.join(issues))
    dump(project / 'content.json', {'title': plan['title'], 'units': {'col_widths': 'inch'},
                                    'colors': 'mck_ppt.constants の名前', 'slides': slides})
    code = run_upstream_script(up, 'gate_check_s3.py', ['content.json', '.'], project)
    if not (project / 'gate_s3.json').exists():
        fail('S3', f'原典 gate_check_s3.py が gate_s3.json を書かずに終了しました（exit {code}）')
    gate_s3 = load(project / 'gate_s3.json')
    if gate_s3.get('passed') is not True:
        fail('S3', 'gate_s3.json passed=false: ' + ' / '.join(
            f"slide {i.get('slide_idx')} [{i.get('check')}] {i.get('message')}" for i in gate_s3.get('fail_items', [])))

    # S4 原典メソッドで描画 + 原典 gate_check.py
    content = load(project / 'content.json')  # 門禁を通ったファイルそのものから描く
    eng = MckEngine(total_slides=len(content['slides']))
    label_changes = []
    for s in content['slides']:
        generated_slide = getattr(eng, s['layout'])(**method_kwargs(s, const))
    eng.save(str(deck))
    from pptx import Presentation
    if len(Presentation(str(deck)).slides) != len(content['slides']):
        fail('S4', 'PPTXのページ数が content.json と一致しません')
    shadow = Path(os.path.expanduser('~/.workbuddy/skills/mck-ppt-design/mck_ppt'))
    if shadow.exists():
        fail('S4', '原典gate_check.pyが優先読込する ~/.workbuddy/skills/mck-ppt-design があり、固定原典のQAを保証できません')
    code = run_upstream_script(up, 'gate_check.py', ['../deck.pptx', '.'], project)
    if not (project / 'gate_result.json').exists():
        fail('S4', f'原典 gate_check.py が gate_result.json を書かずに終了しました（exit {code}）')
    gate_s4 = load(project / 'gate_result.json')
    if gate_s4.get('passed') is not True:
        detail = ' / '.join(f"slide {e.get('slide')} [{e.get('category')}] {e.get('message')}"
                            for e in gate_s4.get('user_code_error_detail', []))
        fail('S4', 'gate_result.json passed=false: ' + (detail or gate_s4.get('error', '詳細なし')))

    # PowerPoint 描画（任意）
    render = {'run': False}
    public = [project / f for f in ('outline.json', 'content.json', 'gate_s3.json', 'gate_result.json')]
    if args.render:
        ps1 = first_existing([case_dir / 'source/render_powerpoint.ps1', ROOT / 'source/render_powerpoint.ps1', ROOT / 'tools/render_powerpoint.ps1'])
        shell = shutil.which('pwsh') or shutil.which('powershell')
        if not ps1 or not shell:
            fail('render', 'render_powerpoint.ps1 または PowerShell が見つかりません')
        rdir = out / 'render'
        for f in [*rdir.glob('slide-*.png'), rdir / 'deck.pdf', rdir / 'powerpoint-render.json']:
            f.unlink(missing_ok=True)
        code = subprocess.run([shell, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(ps1),
                               '-PresentationPath', str(deck), '-OutputDirectory', str(rdir)]).returncode
        if code != 0:
            fail('render', f'{rel(ps1)} が exit {code} で終了しました')
        report_path = rdir / 'powerpoint-render.json'
        report = load(report_path)
        report['source'] = '../deck.pptx'  # 描画scriptが書く絶対パスを公開用に相対化
        dump(report_path, report)
        pngs = sorted(p.name for p in rdir.glob('slide-*.png'))
        if report.get('slide_count') != len(content['slides']) or len(pngs) != len(content['slides']) \
                or not (rdir / 'deck.pdf').exists():
            fail('render', f"PowerPoint出力が不足しています（slides={report.get('slide_count')}, png={len(pngs)}）")
        render = {'run': True, 'application': report.get('application'), 'version': report.get('version'),
                  'pages': [f'render/{n}' for n in pngs], 'pdf': 'render/deck.pdf',
                  'reported_fonts': sorted({t.get('font') for s in report.get('slides', [])
                                            for t in s.get('text_shapes', []) if t.get('font')}),
                  'source_path_relativized': True}
        public.append(report_path)

    # S5: 今回のゲート/成果物hashへ、修復時に判断した固定経験記録を紐付ける。
    s5 = self_refinement(out, project, gate_s4, deck)
    # 相対パスのみ。モデル実行ログは含めない。
    record = {
        'id': plan['id'], 'title': plan['title'],
        'upstream': {**upstream_identity(up), 'location': rel(up),
                     'sha256': {f: sha(up / f) for f in UPSTREAM_REQUIRED if f != 'mck_ppt/__init__.py'}},
        'engine_methods': [s['layout'] for s in content['slides']] + ['save'],
        'engine_overrides': [], 'custom_renderer': False,
        'current_revision_author': 'Codex',
        'S5_scope': 'Replay of fixed repair experience; actual gate and artifact hash are current execution, new self-refinement judgment is not automated',
        'font_overrides': {'module': 'mck_ppt.constants', 'scope': 'この生成プロセス内のみ', 'values': plan['fonts']},
        'label_format_adapter': {'reason': '未使用。原典grouped_barの整数値を保持し、生成後の図形・文字を変更しない。', 'changes': label_changes},
        'data': {'file': data_label, 'sha256': sha(data_path), **summary_json(st)},
        'stages': {
            'S1': {'file': f'{PROJECT_DIR}/brief.md', 'check': 'audience / goal / key_messages 非空（コード確認）'},
            'S2': {'file': f'{PROJECT_DIR}/outline.json', 'check': 'SKILL S2門禁の項目をコード確認（動詞判定は除く）'},
            'S3': {'file': f'{PROJECT_DIR}/content.json', 'precheck': 'layout-matrix.yaml char_budget / Max Items',
                   'gate': '原典 references/scripts/gate_check_s3.py（未改変・subprocess）',
                   'result': f'{PROJECT_DIR}/gate_s3.json', 'passed': gate_s3['passed'],
                   'checkers': upstream_s3_checkers(up, content['slides'])},
            'S4': {'file': 'deck.pptx', 'gate': '原典 references/scripts/gate_check.py（未改変・subprocess・PYTHONPATH=固定原典）',
                   'result': f'{PROJECT_DIR}/gate_result.json', 'passed': gate_s4['passed'],
                   'overall_score': gate_s4.get('overall_score'), 'checklist': gate_s4.get('checklist')},
            'S5': s5,
        },
        'pptx_sha256': sha(deck), 'render': render,
        'deviations': ['原典SKILLのエンジン固定パス(~/.workbuddy)ではなく固定commitの原典を読み込む',
                       '原典brand-guideのKaiTi指定を日本語書体へ局所変更（色・位置・字号は原典のまま）',
                       'TaskCreate による進捗管理は行わず、各段階のファイルとJSONで記録する'],
        'not_done_by_generator': [*([] if args.render else ['PowerPointによるPNG/PDF描画（--render 未指定）']),
                     '全ページの目視確認', '独立レビュー', 'フォーク梱包とプロベナンス'],
    }
    dump(record_path, record)
    assert_public([project / 'brief.md', record_path, *public])
    print(f"[S4] gate passed / score {gate_s4.get('overall_score')} → {rel(deck)}")


if __name__ == '__main__':
    main()
