// @vitest-environment node
import { describe, it, expect, afterAll } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { checkDeps, specifiers } from './check-deps.mjs';

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-deps-'));
afterAll(() => fs.rmSync(TMP, { recursive: true, force: true }));

let n = 0;
/** files: { 'engine/a.js': 'code' } → 임시 레포 루트 */
function tree(files) {
  const root = path.join(TMP, String(n++));
  for (const [p, code] of Object.entries(files)) {
    fs.mkdirSync(path.dirname(path.join(root, p)), { recursive: true });
    fs.writeFileSync(path.join(root, p), code);
  }
  return root;
}
const rules = (files) =>
  checkDeps(tree(files))
    .violations.map((v) => v.rule)
    .sort();

const GOOD = {
  'engine/index.js': "export * from './stage.js';",
  'engine/stage.js': "import gsap from 'gsap';\nexport const s = 1;",
  'engine/scroll.js': "import Lenis from 'lenis';",
  'engine/testing.js': 'export const h = 1;',
  'moves/index.js': "import { s } from '../engine/index.js';\nimport reveal from './reveal/index.js';",
  'moves/reveal/index.js': "import a from './clip.js';\nexport default [a];",
  'moves/reveal/clip.js':
    "import { s } from '../../engine/index.js';\nimport h from '../_shared/split.js';\nexport default {};",
  'moves/reveal/clip.test.js':
    "import { it } from 'vitest';\nimport { createHarness } from '../../engine/testing.js';",
  'moves/_shared/split.js': 'export default 1;',
  'concepts/rail/index.js':
    "import concept from './concept.json' with { type: 'json' };\nexport default concept;",
  'concepts/rail/concept.json': '{}',
  'decks/a/main.js':
    "import { boot } from '../../engine/index.js';\nimport '../../engine/engine.css';\nimport moves from '../../moves/index.js';\nimport c from '../../concepts/rail/index.js';\nimport deck from './deck.yaml';\nimport s from './sequences/x.js';",
  'decks/a/sequences/x.js': "// import gsap from 'gsap' 주석은 무시\nexport default {};",
};

describe('check-deps', () => {
  it('정상 트리는 위반 0', () => {
    const r = checkDeps(tree(GOOD));
    expect(r.violations).toEqual([]);
    expect(r.files).toBe(12);
  });
  // 실제 레포 검사는 `node tools/check.mjs`(C17 ci) 몫: 여기 두면 다른 에이전트의 작업 중 파일과 /mnt/d 부하로 흔들린다.
  it('R0 확장자 없는 상대 import', () => {
    expect(rules({ ...GOOD, 'engine/b.js': "import x from './stage';" })).toEqual(['R0']);
  });
  it('R1 상향 의존·tools import', () => {
    expect(rules({ ...GOOD, 'engine/b.js': "import m from '../moves/index.js';" })).toEqual(['R1']);
    expect(rules({ ...GOOD, 'moves/reveal/b.js': "import t from '../../tools/check-deps.mjs';" })).toEqual([
      'R1',
    ]);
  });
  it('R2 공개 진입점 밖 import', () => {
    expect(rules({ ...GOOD, 'moves/reveal/b.js': "import { s } from '../../engine/stage.js';" })).toEqual([
      'R2',
    ]);
    expect(rules({ ...GOOD, 'moves/reveal/b.js': "import { h } from '../../engine/testing.js';" })).toEqual([
      'R2',
    ]);
    expect(rules({ ...GOOD, 'decks/a/b.js': "import c from '../../concepts/rail/concept.json';" })).toEqual([
      'R2',
    ]);
  });
  it('R3 순환', () => {
    expect(rules({ ...GOOD, 'engine/x.js': "import './y.js';", 'engine/y.js': "import './x.js';" })).toEqual([
      'R3',
    ]);
  });
  it('R4 형제 격리', () => {
    expect(rules({ ...GOOD, 'moves/type/w.js': "import c from '../reveal/clip.js';" })).toEqual(['R4']);
    expect(rules({ ...GOOD, 'decks/b/main.js': "import s from '../a/sequences/x.js';" })).toEqual(['R4']);
  });
  it('R5 외부 패키지 위치', () => {
    expect(rules({ ...GOOD, 'moves/reveal/b.js': "import gsap from 'gsap';" })).toEqual(['R5']);
    expect(rules({ ...GOOD, 'engine/b.js': "import Lenis from 'lenis';" })).toEqual(['R5']);
    expect(rules({ ...GOOD, 'decks/a/b.js': "import YAML from 'yaml';" })).toEqual(['R5']);
    expect(rules({ ...GOOD, 'engine/b.js': "import * as T from 'three';" })).toEqual(['R5']);
    expect(rules({ ...GOOD, 'engine/b.js': "import fs from 'node:fs';" })).toEqual(['R5']);
    expect(rules({ ...GOOD, 'engine/b.js': "import x from 'left-pad';" })).toEqual(['R5']);
  });
  it('지정자 추출: 여러 줄·export from·동적 import, 주석 무시', () => {
    const code =
      "import {\n  a,\n  b\n} from './a.js';\nexport { c } from './c.js';\nconst m = await import('./m.js');\n/* import z from './z.js' */\n// import q from './q.js'\nimport './side.css';";
    expect(specifiers(code)).toEqual(['./a.js', './c.js', './m.js', './side.css']);
  });
});
