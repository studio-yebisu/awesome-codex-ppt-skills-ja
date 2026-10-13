// @vitest-environment node
import { afterAll, describe, expect, it } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { checkMoves } from './check-moves.mjs';

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-moves-'));
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

describe('check-moves', () => {
  it('C5·C10 위반과 family 불일치를 각각 찾고 테스트 파일은 제외한다', () => {
    const root = tree({
      'moves/type/three-d.js': "export default { family: 'type', build() { return { rotateX: 1 }; } };",
      'moves/type/from.js': "export default { family: 'type', build(tl) { tl.from('.x', {}); } };",
      'moves/type/css-var.js': "export default { family: 'type', build() { return 'var(--sl-accent)'; } };",
      'moves/type/random.js': "export default { family: 'type', build() { return Math.random(); } };",
      'moves/type/gsap.js': "import gsap from 'gsap'; export default { family: 'type' };",
      'moves/type/plugin.js': "import Flip from 'gsap/Flip'; export default { family: 'type' };",
      'moves/type/family.js': "export default { family: 'reveal' };",
      'moves/camera/allowed.js':
        "export default { family: 'camera', build() { return { perspective: 800 }; } };",
      'moves/type/good.js': "export default { family: 'type', build(tl, ctx) { ctx.gsap.to({}, {}); } };",
      'moves/type/ignored.test.js': "export default { family: 'nope', build(tl) { tl.from('.x', {}); } };",
    });

    const result = checkMoves(root);
    expect(result.files).toBe(9);
    expect(result.violations.map((violation) => violation.file)).toEqual([
      'moves/type/css-var.js',
      'moves/type/family.js',
      'moves/type/from.js',
      'moves/type/gsap.js',
      'moves/type/plugin.js',
      'moves/type/random.js',
      'moves/type/three-d.js',
    ]);
    expect(result.violations.map((violation) => violation.rule)).toEqual([
      'C5',
      'C5',
      'C5',
      'C1',
      'C1',
      'C5',
      'C10',
    ]);
  });

  // 실제 레포 검사는 `node tools/check.mjs`(C17 ci) 몫: 여기 두면 다른 에이전트의 작업 중 파일과 /mnt/d 부하로 흔들린다.
});
