"""Packaging and evidence shared across examples, never a slide renderer."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import base64, html, json, shutil, subprocess
from fontTools.ttLib import TTFont
from fontTools import subset

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / '.build/actual-upstreams'
DATA = json.loads((ROOT / 'data/case-inputs.json').read_text(encoding='utf-8'))

def read(path):
    return Path(path).read_text(encoding='utf-8-sig')

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8', newline='\n')

def dump(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def rel(path):
    return Path(path).relative_to(ROOT).as_posix()

def hfile(path):
    return sha256(Path(path).read_bytes()).hexdigest()

class Production:
    def __init__(self, repo, ident, key, title, style, method, execution_type, references):
        self.repo, self.ident, self.title = repo, ident, title
        self.up = UP / repo.replace('/', '__')
        self.out = ROOT / 'examples/repositories' / ident
        self.out.mkdir(parents=True, exist_ok=True)
        self.input = DATA[key]
        dump(self.out / 'input/data.json', self.input)
        write(self.out / 'input/BRIEF.md', '# ' + title + '\n\n' + json.dumps(self.input, ensure_ascii=False, indent=2) + '\n')
        self.style, self.method, self.execution_type = style, method, execution_type
        self.references = references
        self.commands = []
        self.pin = json.loads(read(self.up / 'ACQUISITION.json'))
        license_path = next((self.up / n for n in ['LICENSE', 'LICENSE.md', 'LICENSE.txt'] if (self.up / n).exists()), None)
        if not license_path:
            raise ValueError('No reviewed root license: ' + repo)
        shutil.copyfile(license_path, self.out / 'LICENSE.upstream')

    def run(self, args, cwd=None):
        args = [str(v) for v in args]
        r = subprocess.run(args, cwd=cwd or ROOT, capture_output=True, text=True, encoding='utf-8', timeout=180)
        log = ROOT / '.build/repository-runs' / self.ident / (str(len(self.commands) + 1) + '.txt')
        write(log, r.stdout + '\n' + r.stderr)
        self.commands.append({'argv': args, 'cwd': str(cwd or ROOT), 'exit_code': r.returncode,
                              'stdout_sha256': sha256(r.stdout.encode()).hexdigest()})
        if r.returncode:
            raise RuntimeError(self.repo + ': ' + r.stderr[-1000:] + r.stdout[-1000:])
        return r.stdout

    def fonts(self, content):
        text = content + ''.join(chr(i) for i in range(32, 127)) + '←→↗×▶Ⅱ…'
        src = ROOT / '.build/fonts/NotoSansJP[wght].ttf'
        font = TTFont(src)
        opt = subset.Options()
        opt.flavor = 'woff2'
        opt.name_IDs = ['*']
        opt.name_languages = ['*']
        sub = subset.Subsetter(options=opt)
        sub.populate(text=text)
        sub.subset(font)
        for name in font['name'].names:
            if name.nameID in [1, 2, 3, 4, 6, 16, 17]:
                value = {2: 'Regular', 17: 'Regular', 6: 'YebisuNotoSansJP'}.get(name.nameID, 'Yebisu Noto Sans JP')
                name.string = value.encode(name.getEncoding(), errors='replace')
        target = self.out / 'fonts/noto-sans-jp.woff2'
        target.parent.mkdir(parents=True, exist_ok=True)
        font.flavor='woff2'
        font.save(target)
        shutil.copyfile(ROOT / 'assets/fonts/notosansjp-OFL.txt', self.out / 'fonts/OFL.txt')
        dump(self.out / 'fonts/SOURCE.json', {'source_url': json.loads(read(ROOT / 'data/fonts.json'))[0]['source_url'],
                'source_sha256': hfile(src), 'subset_sha256': hfile(target),
                'renamed_family': 'Yebisu Noto Sans JP', 'modification': 'この資料の文字を収録してサブセット化・内部名変更'})
        encoded = base64.b64encode(target.read_bytes()).decode()
        return "@font-face{font-family:'Yebisu Noto Sans JP';src:url(data:font/woff2;base64," + encoded + ") format('woff2');font-weight:100 900;font-display:swap}"

    def latin_fonts(self, families):
        records=json.loads(read(ROOT/'data/preset-fonts.json'))
        css=[]
        for family in families:
            r=next(v for v in records if v['family']==family)
            source=ROOT/r['file']
            target=self.out/'fonts'/source.name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
            license_source=source.with_name(source.stem+'-OFL.txt')
            if license_source.exists():shutil.copyfile(license_source,target.with_name(source.stem+'-OFL.txt'))
            dump(target.with_suffix('.SOURCE.json'),r)
            css.append("@font-face{font-family:'"+family+"';src:url(data:font/ttf;base64,"+base64.b64encode(source.read_bytes()).decode()+") format('truetype');font-weight:100 900;font-display:swap}")
        return '\n'.join(css)

    def finish(self, titles, notes, preview='index.html', artifact=None, use_case='技術解説', extra=None):
        if len(titles) != len(notes):
            raise ValueError('Page/notes mismatch')
        source_files = [{'path': p, 'sha256': hfile(self.up / p)} for p in self.references]
        artifact_path = self.out / preview
        provenance = {'repository': self.repo, 'upstream_commit': self.pin['commit'],
                      'acquisition': self.pin, 'method': self.method, 'execution_type': self.execution_type,
                      'references': source_files, 'commands_executed': self.commands,
                      'artifact': rel(artifact_path), 'artifact_sha256': hfile(artifact_path),
                      'input_sha256': hfile(self.out / 'input/data.json'),
                      'authored_by': '八百万図AIツールボックス / Codex',
                      'scope': '実際に原典の固有方法を使った日本語作例。エージェントが書いた本文を使用。',
                      'checked_at': datetime.now(timezone.utc).isoformat()}
        dump(self.out / 'PROVENANCE.json', provenance)
        dump(self.out / 'QA.json', {'status': 'generated_awaiting_browser_review', 'page_count': len(titles),
                     'generation_commands': [r['exit_code'] for r in self.commands],
                     'visual_review': 'pending', 'not_claimed': ['全機能の動作', '人による採用', '外部公開']})
        write(self.out / 'NOTES.md', '\n\n'.join('## ' + str(i + 1) + '. ' + t + '\n\n' + n for i, (t, n) in enumerate(zip(titles, notes))))
        prompt = self.repo + ' の原典スキルを読み、添付の入力資料を使って「' + self.title + '」を日本語で制作してください。' + self.style + 'を使用し、そのリポ固有の生成手順・テンプレート・実装を保ってください。完成ファイルを開き、全ページの日本語・図表・ページ移動を確認してください。'
        write(self.out / 'PROMPT.txt', prompt + '\n')
        write(self.out / 'README.md', '# ' + self.title + '\n\n原典: https://github.com/' + self.repo + '/tree/' + self.pin['commit'] + '\n\n' + self.method + '\n\n' + '\n'.join('    ' + subprocess.list2cmdline(c['argv']) for c in self.commands) + '\n\n入力: input/data.json。出典・実行の記録: PROVENANCE.json。確認範囲: QA.json。原典の条件: LICENSE.upstream。日本語書体: fonts/OFL.txt。\n')
        base = rel(self.out)
        card = {'id': self.ident, 'title': self.title, 'use_case': use_case,
                'repository': self.repo, 'skill_repository': self.repo, 'upstream_commit': self.pin['commit'],
                'fork_id': None, 'page_count': len(titles), 'format': 'html', 'preview_kind': 'html',
                'style': self.style, 'cover': base + '/render/slide-01.png', 'interior': base + '/render/slide-03.png',
                'preview': base + '/' + preview, 'pages': [base + '/render/slide-' + str(i + 1).zfill(2) + '.png' for i in range(len(titles))],
                'artifact_download': artifact or 'downloads/' + self.ident + '-ja.zip',
                'source_download': 'downloads/' + self.ident + '-ja.zip',
                'input': base + '/input/BRIEF.md', 'input_data': base + '/input/data.json',
                'prompt': base + '/PROMPT.txt', 'prompt_text': prompt, 'provenance': base + '/PROVENANCE.json',
                'qa': base + '/QA.json', 'fork_download': None,
                'guide': 'repository.html?repo=' + self.repo,
                'titles': titles, 'notes': notes, 'method': self.method,
                'sample_notice': 'この資料は使い方を示す制作例です。企業・人数・金額・目標などの企画条件は架空です。'}
        if extra:
            card.update(extra)
        return card
