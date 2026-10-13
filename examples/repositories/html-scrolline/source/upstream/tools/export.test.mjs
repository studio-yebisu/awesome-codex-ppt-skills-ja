// @vitest-environment node
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { exportPaths, parseExportArgs } from './export-lib.mjs';

describe('export CLI', () => {
  it('documents its supported invocation without invoking a build', () => {
    const output = execFileSync(process.execPath, ['tools/export.mjs', '--help'], { encoding: 'utf8' });
    expect(output).toContain('node tools/export.mjs <deckId>');
    expect(output).toContain('--dry-run');
  });

  // --dry-run 계획은 export.plan.test.mjs가 프로세스 안에서 본다(하위 node 프로세스는 /mnt/d 부하에서 10초+).

  it('parses an internal deck ID and resolves its isolated output paths', () => {
    expect(parseExportArgs(['_smoke', '--fps', '15', '--dry-run'])).toMatchObject({ deckId: '_smoke', fps: 15, dryRun: true });
    expect(exportPaths('/workspace', '_smoke')).toEqual({
      deckFile: '/workspace/decks/_smoke/deck.yaml',
      buildDir: '/workspace/out/export/_smoke',
      out: '/workspace/out/export/_smoke.mp4',
    });
  });
});
