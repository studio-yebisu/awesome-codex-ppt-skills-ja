import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './transcript-condense.js';

const scenario = {
  beats: [
    {
      id: 'notes',
      type: 'prompt',
      data: {
        text: '회의 기록',
        result: { type: 'text', text: '결정 배포하기' },
        parts: { field: true, result: true, word: true },
      },
    },
  ],
  rects: {
    'notes.field': { x: 120, y: 280, w: 500, h: 160 },
    'notes.result': { x: 760, y: 340, w: 400, h: 80 },
  },
  run: { role: 'step', beat: 'notes', params: { duration: 1.2, underline: true } },
};
const harnesses = [];
afterEach(() => harnesses.splice(0).forEach((h) => h.destroy()));

it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));

it('collapses the transcript before revealing the condensed result', () => {
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  harnesses.push(h);
  const run = h.runMove(move, scenario.run);
  const field = h.beats.get('notes').part('field')[0];
  const result = h.beats.get('notes').part('result')[0];
  h.seek(0.55 * run.timing.duration);
  expect(Number(run.ctx.gsap.getProperty(field, 'scaleY'))).toBeLessThanOrEqual(0.05);
  h.seek(run.timing.duration);
  expect(Number(run.ctx.gsap.getProperty(field, 'opacity'))).toBe(0);
  expect(Number(run.ctx.gsap.getProperty(result, 'opacity'))).toBe(1);
  expect(Number(run.ctx.gsap.getProperty(result, 'scaleY'))).toBe(1);
});
