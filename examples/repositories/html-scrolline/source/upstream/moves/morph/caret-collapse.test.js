import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './caret-collapse.js';
const scenario = {
  beats: [
    { id: 'a', type: 'video', data: {} },
    { id: 'b', type: 'prompt', data: {} },
  ],
  rects: {
    'a.frame': { x: 0, y: 0, w: 1200, h: 700 },
    'b.field': { x: 600, y: 650, w: 400, h: 50 },
    'b.caret': { x: 780, y: 660, w: 6, h: 28 },
    'b.label': { x: 600, y: 610, w: 160, h: 25 },
  },
  run: { role: 'link', from: 'a', beat: 'b' },
};
scenario.nodes = (_h, ctx) => [ctx.handoff.from.node, ctx.handoff.to.node];
it('meets the caret link contract', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
});
