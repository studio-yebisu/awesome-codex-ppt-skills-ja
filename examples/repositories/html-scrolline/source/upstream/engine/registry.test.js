import { describe, expect, it } from 'vitest';
import { createRegistry } from './registry.js';
const good = {
  id: 'okay',
  family: 'reveal',
  role: 'enter',
  accepts: ['text'],
  sources: ['source'],
  reduce: 'self',
  params: { speed: { type: 'number', default: 1, doc: 'Speed' } },
  timing: () => ({ duration: 1 }),
  build: () => {},
};
describe('createRegistry', () => {
  it('indexes custom and builtin moves', () => {
    const r = createRegistry([good]);
    expect(r.has('engine:fade-in')).toBe(true);
    expect(r.get('okay')).toBe(good);
    expect(r.byFamily('reveal')).toEqual([good]);
  });
  it('rejects the six required invalid definition forms', () => {
    expect(() => createRegistry([{ ...good, id: 'Bad' }])).toThrow();
    expect(() => createRegistry([{ ...good, family: 'bad' }])).toThrow();
    expect(() => createRegistry([{ ...good, role: 'bad' }])).toThrow();
    expect(() =>
      createRegistry([{ ...good, params: { speed: { type: 'number', doc: 'Speed' } } }]),
    ).toThrow();
    expect(() => createRegistry([{ ...good, timing: null }])).toThrow();
    expect(() => createRegistry([{ ...good, sources: [] }])).toThrow();
  });
  it('rejects reserved sequence ids and invalid handoff definitions', () => {
    expect(() => createRegistry([{ ...good, id: 'seq:private' }])).toThrow();
    expect(() => createRegistry([{ ...good, handoff: true }])).toThrow();
    expect(() => createRegistry([{ ...good, handoff: () => {} }])).toThrow();
    expect(() => createRegistry([{ ...good, role: 'link', handoff: () => {} }])).not.toThrow();
  });
});
