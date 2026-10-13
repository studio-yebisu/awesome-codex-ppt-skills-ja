// @vitest-environment node
import { describe, it, expect, afterAll } from 'vitest';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { checkTests } from './check-tests.mjs';

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-tests-'));
afterAll(() => fs.rmSync(TMP, { recursive: true, force: true }));

describe('check-tests', () => {
  it('@stub 면제, 구현 파일은 테스트 필요, index·_shared 제외', () => {
    const files = {
      'engine/a.js': '/** @stub W2-E1 */',
      'engine/b.js': 'export const b = 1;',
      'engine/c.js': 'export const c = 1;',
      'engine/c.test.js': '',
      'engine/index.js': '',
      'moves/_shared/s.js': '',
      'moves/morph/m.js': 'export default {};',
    };
    for (const [p, code] of Object.entries(files)) {
      fs.mkdirSync(path.dirname(path.join(TMP, p)), { recursive: true });
      fs.writeFileSync(path.join(TMP, p), code);
    }
    const r = checkTests(TMP);
    expect(r.stubs).toEqual(['engine/a.js']);
    expect(r.missing.sort()).toEqual(['engine/b.js', 'moves/morph/m.js']);
  });
});
