import { afterEach, describe, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './ladder-callout.js';
const scenario = {
  beats: [{ id: 't', type: 'text', data: { parts: { line: true } } }],
  rects: { 't.line#0': { x: 300, y: 200, w: 400, h: 30 }, 't.line#1': { x: 300, y: 250, w: 400, h: 30 } },
  run: { role: 'enter', beat: 't', params: { rungs: [0, 1], duration: 1.8 } },
  concept: { tokens: { ladderX: 70, ladderTop: 100, ladderStep: 30 } },
};
const hs = [];
afterEach(() => hs.splice(0).forEach((h) => h.destroy()));
describe('ladder-callout', () => {
  it('meets the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
  it('finishes lines in their rendered state', () => {
    const h = createHarness(scenario);
    hs.push(h);
    const r = h.runMove(move, scenario.run);
    h.seek(r.timing.duration);
    h.beats
      .get('t')
      .part('line')
      .forEach((node) => {
        expect(Number(r.ctx.gsap.getProperty(node, 'opacity'))).toBe(1);
        expect(Number(r.ctx.gsap.getProperty(node, 'y'))).toBe(0);
      });
  });
});
