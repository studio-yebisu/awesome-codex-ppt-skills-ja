// @vitest-environment node
import { afterAll, describe, expect, it } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { checkConcepts, checkLayoutCss, colorLiteral, splitSelectors } from './check-concepts.mjs';

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-concepts-'));
afterAll(() => fs.rmSync(TMP, { recursive: true, force: true }));

let n = 0;
function tree(files) {
  const root = path.join(TMP, String(n++));
  for (const [file, code] of Object.entries(files)) {
    const target = path.join(root, file);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, code);
  }
  return root;
}

const tokens = (msgs) => msgs.map((v) => v.token);

describe('check-concepts layout.css (C11 v2.2)', () => {
  it('accepts scoped selectors, token colors, at-rules and concept-local variables', () => {
    const css = `/* .bad { color: red } */
.sl-concept-rail .sl-chronology__track,
.sl-concept-rail[data-x] > .a:is(.b, .c) { color: var(--sl-fg); --rail-month: 64; border: 1px solid transparent; }
@media (max-width: 800px) { .sl-concept-rail .a { font-family: 'Red Hat'; white-space: nowrap; } }
@keyframes rail-blink { from { opacity: 0; } to { opacity: 1; } }`;
    expect(checkLayoutCss('rail', css, 'x.css')).toEqual([]);
  });

  it('flags unscoped selectors, colour literals, --sl-* writes, !important and foreign at-rules', () => {
    const css = `.sl-chronology__track { top: 50%; }
.sl-concept-railway .a { top: 0; }
.sl-concept-rail .a, .b { color: #fff; background: rgb(0 0 0); outline-color: Red; }
.sl-concept-rail .c { --sl-bg: var(--sl-fg); --other: 1; top: 0 !important; }
@media screen { .x { top: 0; } }
@import 'y.css';
@keyframes blink { to { color: white; } }
@layer base { .sl-concept-rail .d { top: 0; } }`;
    const found = checkLayoutCss('rail', css, 'x.css');
    expect(tokens(found)).toEqual(
      expect.arrayContaining([
        '.sl-chronology__track',
        '.sl-concept-railway .a',
        '.b',
        'color: #fff',
        'background: rgb(',
        'outline-color: Red',
        '--sl-bg',
        '--other',
        'top: !important',
        '.x',
        '@import',
        'blink',
        'color: white',
        '@layer',
      ]),
    );
    expect(found.find((v) => v.token === '.b').line).toBe(3);
  });

  it('splits selectors on top-level commas only and ignores quoted or var() words', () => {
    expect(splitSelectors('.a :is(.b, .c), .d')).toEqual(['.a :is(.b, .c)', '.d']);
    expect(colorLiteral("var(--sl-accent) 'Navy Serif'")).toBeNull();
    expect(colorLiteral('url(#red-mask)')).toBeNull();
    expect(colorLiteral('0 0 0 200vmax var(--sl-bg)')).toBeNull();
  });
});

describe('check-concepts deck imports', () => {
  it('requires a deck to import its concept layout after tokens and forbids other concepts', () => {
    const root = tree({
      'concepts/rail/layout.css': '.sl-concept-rail .a { top: 0; }',
      'concepts/data/tokens.css': '',
      'decks/ok/main.js':
        "import '../../concepts/rail/index.js';\nimport '../../concepts/rail/tokens.css';\nimport '../../concepts/rail/layout.css';\nboot({ mode: import.meta.env.SCROLLINE_MODE });",
      'decks/nomode/main.js':
        "import '../../concepts/data/index.js';\nimport '../../concepts/data/tokens.css';\nboot({ deck });",
      'decks/missing/main.js': "import '../../concepts/rail/index.js';\nimport '../../concepts/rail/tokens.css';",
      'decks/order/main.js':
        "import '../../concepts/rail/index.js';\nimport '../../concepts/rail/layout.css';\nimport '../../concepts/rail/tokens.css';",
      'decks/foreign/main.js':
        "import '../../concepts/data/index.js';\nimport '../../concepts/data/tokens.css';\nimport '../../concepts/rail/layout.css';",
    });
    const result = checkConcepts(root);
    expect(result).toMatchObject({ concepts: 2, layouts: 1 });
    expect(result.violations.map((v) => `${v.file} ${v.message}`).sort()).toEqual([
      'decks/foreign/main.js 다른 컨셉 layout.css import 금지',
      'decks/missing/main.js 컨셉 layout.css import 누락',
      'decks/nomode/main.js boot에 mode: import.meta.env.SCROLLINE_MODE 누락(MP4 export 불가)',
      'decks/order/main.js layout.css는 tokens.css 다음에 import',
    ]);
  });

  // 실제 레포 검사는 `node tools/check.mjs`(C17 ci) 몫: 여기 두면 다른 에이전트의 작업 중 파일과 /mnt/d 부하로 흔들린다.
});
