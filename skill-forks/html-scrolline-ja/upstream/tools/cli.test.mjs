// @vitest-environment node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { createDeck, moveRows, run } from './cli.mjs';

const dirs = [];
afterEach(() => {
  for (const dir of dirs.splice(0)) fs.rmSync(dir, { recursive: true, force: true });
});
function root() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'scrolline-cli-'));
  dirs.push(dir);
  fs.mkdirSync(path.join(dir, 'decks'), { recursive: true });
  return dir;
}

describe('cli', () => {
  it('new creates the C15 entry shape', async () => {
    const dir = root();
    await run(['new', 'my-deck', '--concept', 'smoke'], { root: dir, out: () => {}, err: () => {} });
    const deckDir = path.join(dir, 'decks', 'my-deck');
    expect(fs.existsSync(path.join(deckDir, 'assets'))).toBe(true);
    expect(fs.readFileSync(path.join(deckDir, 'main.js'), 'utf8')).toContain(
      "import concept from '../../concepts/smoke/index.js'",
    );
    expect(fs.readFileSync(path.join(deckDir, 'deck.yaml'), 'utf8')).toContain('id: my-deck');
  });

  it('rejects unsafe ids and prints filtered moves', () => {
    expect(() => createDeck('../bad', 'smoke', root())).toThrow();
    const registry = {
      ids: () => ['engine:fade-in', 'word-rise'],
      get: (id) =>
        id.startsWith('engine')
          ? { id, family: 'engine', role: 'enter' }
          : { id, family: 'type', role: 'enter' },
    };
    expect(moveRows(registry, { family: 'engine' })).toEqual(['engine:fade-in\tengine\tenter']);
  });
});
