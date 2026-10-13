import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import concept from '../../concepts/zoom/index.js';
import { beatTypes, plan, validateDeck } from '../../engine/index.js';
import moves from '../../moves/index.js';
import deck from './deck.yaml';

const here = path.dirname(fileURLToPath(import.meta.url));
const env = { registry: moves, concept, beatTypes, sequences: {} };

function moveRefs(value, result = []) {
  if (Array.isArray(value)) value.forEach((item) => moveRefs(item, result));
  else if (value && typeof value === 'object') {
    if (typeof value.move === 'string') result.push(value.move);
    Object.values(value).forEach((item) => moveRefs(item, result));
  }
  return result;
}

function assetRefs(value, result = []) {
  if (Array.isArray(value)) value.forEach((item) => assetRefs(item, result));
  else if (value && typeof value === 'object')
    Object.values(value).forEach((item) => assetRefs(item, result));
  else if (typeof value === 'string' && value.startsWith('assets/')) result.push(value);
  return result;
}

describe('zoom-root-cause deck', () => {
  it('validates against the zoom concept', () => {
    expect(validateDeck(deck, env)).toEqual({ ok: true, errors: [] });
  });

  it('keeps the planned stop count and duration stable', () => {
    const map = plan(deck, env);
    expect({ stops: map.stops.length, duration: Number(map.duration.toFixed(1)) }).toEqual({
      stops: 23,
      duration: 60.5,
    });
  });

  it('uses only registered moves', () => {
    for (const id of moveRefs(deck)) expect(moves.has(id)).toBe(true);
  });

  it('contains every referenced local asset', () => {
    for (const asset of assetRefs(deck)) expect(fs.existsSync(path.join(here, asset))).toBe(true);
  });
});
