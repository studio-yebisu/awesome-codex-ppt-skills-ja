import { describe, expect, it } from 'vitest';
import { PLACEHOLDER_PATTERNS } from './constants.js';
import { createRegistry } from './registry.js';
import { validateDeck } from './deck-schema.js';

const move = (id, role) => ({
  id,
  family: 'reveal',
  role,
  accepts: ['*'],
  sources: ['test'],
  reduce: 'self',
  params: {},
  timing: () => ({ duration: 1 }),
  build: () => {},
});
const registry = createRegistry([move('rise', 'enter'), move('leave', 'exit'), move('join', 'link')]);
const type = { fields: {}, primary: 'block', render: () => {} };
const concept = {
  id: 'test',
  beats: { allow: ['text', 'number', 'photo', 'quote', 'chart'] },
  moves: { allow: ['rise', 'leave', 'join'] },
  defaults: { enter: 'rise', exit: 'leave' },
};
const env = {
  registry,
  concept,
  beatTypes: { text: type, number: type, photo: type, quote: type, chart: type },
};
const deck = () => ({
  id: 'valid',
  title: 'Valid',
  lang: 'en',
  concept: 'test',
  sources: [{ id: 's1', title: 'Source', url: 'https://example.test', accessed: '2026-10-08' }],
  beats: [{ id: 'one', type: 'text' }],
});

describe('validateDeck', () => {
  it('accepts a minimal valid deck', () =>
    expect(validateDeck(deck(), env)).toEqual({ ok: true, errors: [] }));
  it('audits all thirteen placeholder patterns', () => {
    for (const pattern of PLACEHOLDER_PATTERNS) {
      const value = pattern.source.includes('x{3')
        ? 'xxx'
        : pattern.source.includes('TODO')
          ? 'TODO'
          : pattern.source.includes('TBD')
            ? 'TBD'
            : pattern.source.includes('lorem')
              ? 'lorem'
              : pattern.source.includes('ipsum')
                ? 'ipsum'
                : pattern.source.includes('「')
                  ? '「x」'
                  : pattern.source.includes('\\?')
                    ? '???'
                    : pattern.source.includes('\\{\\{')
                      ? '{{'
                      : pattern.source.includes('\\}\\}')
                        ? '}}'
                        : pattern.source.includes('placeholder')
                          ? '<placeholder>'
                          : pattern.source.includes('자리표')
                            ? '자리표'
                            : pattern.source.includes('예시')
                              ? '예시 문구'
                              : '   ';
      const d = deck();
      d.title = value;
      expect(validateDeck(d, env).ok).toBe(false);
    }
  });
  it('requires ledger sources, override, repeat intent, and a non-final link', () => {
    const d = deck();
    d.beats = [
      { id: 'one', type: 'number' },
      { id: 'two', type: 'photo', source: 'missing' },
      { id: 'three', type: 'text', link: { move: 'join' } },
    ];
    const messages = validateDeck(d, env)
      .errors.map((x) => x.message)
      .join(' ');
    expect(messages).toMatch(/source is required/);
    expect(messages).toMatch(/not in deck.sources/);
    expect(messages).toMatch(/last beat cannot have link/);
    const outside = deck();
    outside.beats[0].enter = { move: 'engine:fade-in' };
    expect(validateDeck(outside, env).ok).toBe(true);
    const repeats = deck();
    repeats.beats.push({ id: 'two', type: 'text' });
    expect(validateDeck(repeats, env).errors.some((x) => x.message.includes('repeats'))).toBe(true);
  });

  it('audits v2 common fields, source arrays, chart references, and chronology sources', () => {
    const richEnv = {
      ...env,
      concept: {
        ...concept,
        beats: { allow: [...concept.beats.allow, 'compare', 'chronology', 'sequence'] },
      },
      beatTypes: { ...env.beatTypes, compare: type, chronology: type },
      sequences: { custom: { ...type, fields: { use: { type: 'string', required: true } } } },
    };
    const d = deck();
    d.sources.push({ id: 's2', title: 'Second', short: 'S2' });
    d.beats = [
      { id: 'one', type: 'text', persist: true, tone: 6 },
      { id: 'two', type: 'number', source: [] },
      { id: 'three', type: 'chart', categories: ['A'], states: [{ name: 'base' }], notes: [{ index: 1 }] },
      { id: 'four', type: 'chronology', events: [{ source: 'missing' }] },
      { id: 'five', type: 'sequence', use: 'custom', enter: { move: 'rise' } },
    ];
    const messages = validateDeck(d, richEnv)
      .errors.map((error) => error.message)
      .join(' ');
    expect(messages).toMatch(/place.world/);
    expect(messages).toMatch(/integer from 0 to 5/);
    expect(messages).toMatch(/empty array/);
    expect(messages).toMatch(/must not be base/);
    expect(messages).toMatch(/within categories/);
    expect(messages).toMatch(/source is not in deck.sources/);
    expect(messages).toMatch(/cannot specify enter/);

    const valid = deck();
    valid.beats = [
      {
        id: 'one',
        type: 'text',
        place: { world: { x: 0, y: 0 } },
        persist: true,
        tone: 0,
        enter: { move: 'engine:none' },
        exit: { move: 'engine:none' },
      },
      {
        id: 'two',
        type: 'compare',
        items: [{ label: 'A', value: 1 }],
        source: ['s1'],
        enter: { move: 'engine:none' },
        exit: { move: 'engine:none' },
      },
      { id: 'three', type: 'text', tone: 5, enter: { move: 'engine:none' } },
    ];
    expect(validateDeck(valid, richEnv).ok).toBe(true);
  });

  it('rejects every invalid tone and source-array shape while accepting an in-ledger array', () => {
    for (const tone of [-1, 1.5, 6]) {
      const d = deck();
      d.beats[0].tone = tone;
      expect(validateDeck(d, env).ok).toBe(false);
    }
    for (const source of [[], ['s1', 's1'], ['missing']]) {
      const d = deck();
      d.beats = [{ id: 'one', type: 'number', source }];
      expect(validateDeck(d, env).ok).toBe(false);
    }
    const d = deck();
    d.sources.push({ id: 's2', title: 'Second source', short: 'S2' });
    d.beats = [{ id: 'one', type: 'number', source: ['s1', 's2'] }];
    expect(validateDeck(d, env).ok).toBe(true);
  });

  it('requires each chart state name to belong to a step', () => {
    const d = deck();
    d.beats = [{ id: 'one', type: 'chart', states: [{ name: 'changed' }] }];
    expect(validateDeck(d, env).errors).toContainEqual({
      path: 'deck.beats[0].states[0].name',
      message: 'must match a step name',
    });
  });

  it('accepts a sequence without enter and rejects an authored sequence enter', () => {
    const sequenceEnv = {
      ...env,
      concept: { ...concept, beats: { allow: [...concept.beats.allow, 'sequence'] } },
      sequences: { custom: { ...type, fields: { use: { type: 'string', required: true } } } },
    };
    const d = deck();
    d.beats = [{ id: 'one', type: 'sequence', use: 'custom' }];
    expect(validateDeck(d, sequenceEnv).ok).toBe(true);
    d.beats[0].enter = { move: 'rise' };
    expect(validateDeck(d, sequenceEnv).errors).toContainEqual({
      path: 'deck.beats[0].enter',
      message: 'sequence beat cannot specify enter',
    });
  });

  it('does not count a final beat default exit as a repeated move', () => {
    const d = deck();
    d.beats = [
      { id: 'one', type: 'text', enter: { move: 'engine:none' } },
      { id: 'two', type: 'text', enter: { move: 'engine:none' } },
    ];
    expect(validateDeck(d, env).ok).toBe(true);
  });
});
