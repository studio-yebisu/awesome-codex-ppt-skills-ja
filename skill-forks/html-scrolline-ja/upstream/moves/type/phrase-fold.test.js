import { describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './phrase-fold.js';

const scenario = (fold) => ({
  beats: [
    { id: 'a', type: 'text', data: { parts: { word: true } } },
    { id: 'b', type: 'text', data: { parts: { word: true } } },
  ],
  rects: {
    'a.word#0': { x: 100, y: 200, w: 70, h: 40 },
    'a.word#1': { x: 180, y: 200, w: 80, h: 40 },
    'a.word#2': { x: 270, y: 200, w: 90, h: 40 },
    'a.word#3': { x: 370, y: 200, w: 80, h: 40 },
    'b.block': { x: 600, y: 300, w: 300, h: 80 },
    'b.word#0': { x: 600, y: 300, w: 140, h: 80 },
    'b.word#1': { x: 760, y: 300, w: 140, h: 80 },
  },
  run: {
    role: 'link',
    from: 'a',
    beat: 'b',
    params: { fold, keepFrom: 1, keepTo: 2, caret: true, appendIn: true, duration: 1.6 },
  },
});

describe('phrase-fold', () => {
  for (const fold of ['right', 'both'])
    it(`meets the link contract when folding ${fold}`, () =>
      expect(checkMove(move, scenario(fold), createHarness)).toEqual([]));
  it('carries the retained first word to the destination rectangle', () => {
    const h = createHarness(scenario('both')),
      result = h.runMove(move, scenario('both').run);
    h.seek(result.timing.duration);
    const rect = result.ctx.handoff.from.node.getBoundingClientRect();
    expect(rect.left).toBeCloseTo(result.ctx.handoff.to.rect.x);
    expect(rect.top).toBeCloseTo(result.ctx.handoff.to.rect.y);
    h.destroy();
  });
});
