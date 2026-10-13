// @vitest-environment node
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { expect, it } from 'vitest';
import { exportPlan } from './export-lib.mjs';
import { usage } from './export.mjs';

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');

// 회귀: export.test.mjs가 node 하위 프로세스로 --help·--dry-run을 돌려(정적 import로 engine·registry 적재)
// 부하 걸린 /mnt/d에서 5–10초 → 전체 vitest에서 타임아웃. 계획은 프로세스 안에서, --help는 가벼운 경로만.
it('answers --help without loading the engine', () => {
  const started = Date.now();
  const output = execFileSync(process.execPath, ['tools/export.mjs', '--help'], { cwd: ROOT, encoding: 'utf8' });
  expect(output.trim()).toBe(usage);
  expect(Date.now() - started).toBeLessThan(3000);
});

it('plans the _smoke export path in-process', async () => {
  const report = await exportPlan(ROOT, { deckId: '_smoke', fps: 15 });
  expect(report.out).toMatch(/out\/export\/_smoke\.mp4$/);
  expect(report.path.duration).toBeGreaterThan(0);
  expect(report.map.stops.length).toBeGreaterThan(0);
}, 60_000);
