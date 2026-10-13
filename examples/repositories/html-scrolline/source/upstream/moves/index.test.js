import { describe, expect, it } from 'vitest';
import registry from './index.js';
import { readFileSync } from 'node:fs';
import path from 'node:path';

// vitest는 레포 루트에서 돈다(happy-dom 환경이라 import.meta.url이 file: 스킴이 아님).
const catalog = readFileSync(path.join(process.cwd(), 'plan/moves.catalog.jsonl'), 'utf8');

const catalogIds = catalog
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line).id);

describe('move registry', () => {
  it('builds and every merged move is in the catalog', () => {
    const ids = registry.ids();
    expect(ids.length).toBeGreaterThan(0);
    for (const id of ids.filter((id) => !id.startsWith('engine:'))) expect(catalogIds).toContain(id);
  });
});
