// @vitest-environment node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterAll, expect, it } from 'vitest';
import { deckTemplate, run } from './cli.mjs';

const REPO = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-cli-'));
afterAll(() => fs.rmSync(TMP, { recursive: true, force: true }));

// 문서 대조로 찾은 결함: new가 만든 main.js에 export mode가 없어 MP4 export가 안 됐고,
// plan은 `_` 내부 덱을 거부하고 validateDeck을 건너뛰었다.
it('scaffolds main.js with the export mode and the concept layout import', () => {
  const { main } = deckTemplate('x', 'rail', true);
  expect(main).toContain('mode: import.meta.env.SCROLLINE_MODE');
  expect(main.indexOf("concepts/rail/layout.css")).toBeGreaterThan(main.indexOf('concepts/rail/tokens.css'));
  expect(deckTemplate('x', 'data').main).not.toContain('layout.css');
});

it('plans an internal deck and refuses an invalid one with its validation errors', async () => {
  const root = path.join(TMP, 'repo');
  fs.mkdirSync(path.join(root, 'decks', '_bad'), { recursive: true });
  for (const dir of ['engine', 'moves', 'concepts', 'node_modules']) fs.symlinkSync(path.join(REPO, dir), path.join(root, dir));
  fs.symlinkSync(path.join(REPO, 'decks', '_smoke'), path.join(root, 'decks', '_smoke'));
  fs.writeFileSync(path.join(root, 'decks', '_bad', 'deck.yaml'), 'id: _bad\nlang: ko\nconcept: _smoke\nbeats: []\n');

  const out = [];
  expect(await run(['plan', '_smoke'], { root, out: (x) => out.push(x), err: () => {} })).toBe(0);
  expect(JSON.parse(out[0])).toMatchObject({ deck: '_smoke' });

  const errors = [];
  expect(await run(['plan', '_bad'], { root, out: () => {}, err: (x) => errors.push(x) })).toBe(1);
  expect(errors.join('\n')).toMatch(/deck\.beats/);
}, 90_000);
