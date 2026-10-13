import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './sweep-out.js';

const scenario = {
  beats: [{ id: 'b', type: 'text', data: { parts: { word: true } } }],
  rects: { 'b.word#0': { x: 100, y: 200, w: 70, h: 40 }, 'b.word#1': { x: 180, y: 200, w: 70, h: 40 } },
  run: { role: 'exit', beat: 'b', params: { duration: 0.9, lag: 0.03 } },
};
it('meets the exit contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('starts the second word exactly one lag after the first', () => {
  const h = createHarness(scenario),
    result = h.runMove(move, scenario.run),
    words = h.beats.get('b').part('word');
  h.seek(0.02);
  expect(Number(result.ctx.gsap.getProperty(words[1], 'x'))).toBe(0);
  h.seek(0.04);
  expect(Number(result.ctx.gsap.getProperty(words[1], 'x'))).toBeLessThan(0);
  h.destroy();
});
