import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import concept from '../../concepts/launch/index.js';
import { beatTypes, plan, validateDeck } from '../../engine/index.js';
import moves from '../../moves/index.js';
import deck from './deck.yaml';

const here = path.dirname(fileURLToPath(import.meta.url));
const env = { registry: moves, concept, beatTypes, sequences: {} };

function refs(value, key, result = []) {
  if (Array.isArray(value)) value.forEach((item) => refs(item, key, result));
  else if (value && typeof value === 'object') {
    if (key === 'move' && typeof value.move === 'string') result.push(value.move);
    if (key === 'asset')
      Object.values(value).forEach((item) => {
        if (typeof item === 'string' && item.startsWith('assets/')) result.push(item);
      });
    Object.values(value).forEach((item) => refs(item, key, result));
  }
  return result;
}

describe('launch-orbit-note deck', () => {
  it('validates against the launch concept', () => {
    expect(validateDeck(deck, env)).toEqual({ ok: true, errors: [] });
  });

  it('keeps the planned stop count and duration stable', () => {
    const map = plan(deck, env);
    expect({ stops: map.stops.length, duration: Number(map.duration.toFixed(1)) }).toEqual({
      stops: 18,
      duration: 37.8,
    });
  });

  it('uses only registered moves', () => {
    for (const id of refs(deck, 'move')) expect(moves.has(id)).toBe(true);
  });

  it('contains every referenced local asset', () => {
    for (const asset of refs(deck, 'asset')) expect(fs.existsSync(path.join(here, asset))).toBe(true);
  });
});
