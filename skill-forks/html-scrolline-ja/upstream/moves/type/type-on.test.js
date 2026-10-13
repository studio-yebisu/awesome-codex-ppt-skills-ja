import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './type-on.js';

const scenario = {
  beats: [{ id: 'p', type: 'prompt', data: { text: 'hello' } }],
  rects: {
    'p.field': { x: 10, y: 10, w: 200, h: 40 },
    'p.caret': { x: 10, y: 10, w: 4, h: 30 },
    'p.char#0': { x: 10, y: 10, w: 10, h: 20 },
    'p.char#1': { x: 20, y: 10, w: 10, h: 20 },
    'p.char#2': { x: 30, y: 10, w: 10, h: 20 },
    'p.char#3': { x: 40, y: 10, w: 10, h: 20 },
    'p.char#4': { x: 50, y: 10, w: 10, h: 20 },
  },
  run: { role: 'enter', beat: 'p', params: { speed: 10, chunk: 'char' } },
};
it('satisfies the move contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));
it('uses the specified pure timing and character steps', () => {
  expect(move.timing({ speed: 10, chunk: 'char' }, scenario.beats[0].data).duration).toBe(0.9);
  const h = createHarness(scenario),
    r = h.runMove(move, scenario.run);
  h.seek(r.timing.duration * 0.55);
  expect(
    r.ctx.beat.part('char').filter((node) => Number(r.ctx.gsap.getProperty(node, 'opacity')) === 1).length,
  ).toBeGreaterThan(0);
  h.destroy();
});
it('includes word-mode pauses in timing', () =>
  expect(
    move.timing({ speed: 20, chunk: 'word', chunkMax: 2, pause: 0.3 }, { text: 'a b c' }).duration,
  ).toBeCloseTo(1.25));
