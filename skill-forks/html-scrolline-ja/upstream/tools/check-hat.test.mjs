// @vitest-environment node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { afterAll, expect, it } from 'vitest';
import { checkHat } from './check-hat.mjs';

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-hat-'));
afterAll(() => fs.rmSync(TMP, { recursive: true, force: true }));
const git = (...args) => execFileSync('git', args, { cwd: TMP, encoding: 'utf8' });
function commit(files, hat) {
  for (const [file, body] of Object.entries(files)) {
    fs.mkdirSync(path.dirname(path.join(TMP, file)), { recursive: true });
    fs.writeFileSync(path.join(TMP, file), body);
  }
  git('add', '-A');
  git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-q', '-m', `c\n\n${hat ? `Hat: ${hat}` : ''}`);
  return git('rev-parse', 'HEAD').trim();
}

it('accepts feature, refactor and docs-only none; rejects missing trailers and code under none', () => {
  git('init', '-q');
  const base = commit({ 'README.md': 'x' }, 'none');
  commit({ 'a.js': '1', 'a.test.js': 't' }, 'feature');
  commit({ 'a.js': '2' }, 'refactor');
  commit({ 'plan/PLAN.md': 'p', 'decks/d/assets/x.webp': 'img' }, 'none');
  const bad = commit({ 'b.css': 'x' }, 'none');
  const missing = commit({ 'c.md': 'x' }, null);
  const found = checkHat(TMP, `${base}..HEAD`);
  expect(found.map((x) => [x.commit, x.message.split(':')[0]])).toEqual([
    [bad, 'none인데 코드 변경'],
    [missing, 'Hat'],
  ]);
});
