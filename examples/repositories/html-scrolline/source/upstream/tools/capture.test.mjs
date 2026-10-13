// @vitest-environment node
import { execFileSync } from 'node:child_process';
import { describe, expect, it } from 'vitest';
import { parseCaptureArgs } from './export-lib.mjs';

describe('capture CLI', () => {
  it('documents stop and named capture options without invoking a renderer', () => {
    const output = execFileSync(process.execPath, ['tools/capture.mjs', '--help'], { encoding: 'utf8' });
    expect(output).toContain('node tools/capture.mjs <deckId>');
    expect(output).toContain('--stops');
    expect(output).toContain('--between');
    expect(output).toContain('--at');
  });

  it('keeps the between-frame option in the documented capture plan', () => {
    const output = execFileSync(process.execPath, ['tools/capture.mjs', '--help'], { encoding: 'utf8' });
    expect(output).toContain('[--between]');
  });

  it('parses stop, between, and named-stop capture requests without rendering', () => {
    expect(parseCaptureArgs(['_smoke', '--stops', '--between', '--at', 'opening,total'])).toEqual({
      deckId: '_smoke',
      stops: true,
      between: true,
      at: ['opening', 'total'],
    });
  });
});
