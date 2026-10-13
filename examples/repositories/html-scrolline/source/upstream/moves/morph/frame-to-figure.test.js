import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './frame-to-figure.js';
const scenario = {
  beats: [
    { id: 'a', type: 'video', data: {} },
    { id: 'b', type: 'number', data: {} },
  ],
  rects: {
    'a.frame': { x: 0, y: 0, w: 800, h: 450 },
    'a.caption': { x: 0, y: 460, w: 200, h: 30 },
    'b.value': { x: 900, y: 300, w: 160, h: 80 },
    'b.label': { x: 900, y: 390, w: 200, h: 30 },
  },
  run: { role: 'link', from: 'a', beat: 'b' },
};
scenario.nodes = (_h, ctx) => [ctx.handoff.from.node, ctx.handoff.to.node];
it('meets the link contract and lands the frame on the figure', () => {
  expect(checkMove(move, scenario, createHarness)).toEqual([]);
});
