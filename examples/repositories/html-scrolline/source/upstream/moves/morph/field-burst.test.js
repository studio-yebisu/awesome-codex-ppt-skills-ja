import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './field-burst.js';
const scenario = {
  beats: [
    { id: 'a', type: 'prompt', data: {} },
    { id: 'b', type: 'video', data: {} },
  ],
  rects: {
    'a.field': { x: 400, y: 650, w: 500, h: 50 },
    'a.caret': { x: 850, y: 660, w: 6, h: 28 },
    'a.char#0': { x: 420, y: 660, w: 20, h: 25 },
    'a.char#1': { x: 445, y: 660, w: 20, h: 25 },
    'b.frame': { x: 0, y: 0, w: 1200, h: 700 },
  },
  run: { role: 'link', from: 'a', beat: 'b' },
};
scenario.nodes = (_h, ctx) => [ctx.handoff.from.node, ctx.handoff.to.node];
it('opens the media frame from the field and meets the link contract', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
});
