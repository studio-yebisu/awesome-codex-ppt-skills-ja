import { afterEach, expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import { checkMove } from '../_shared/contract-check.js';
import move from './pin-drop.js';

const scenario = {
  beats: [
    {
      id: 'places',
      type: 'compare',
      data: {
        items: [{ label: '서울' }, { label: '부산' }],
        verdict: '두 지점이 준비됐다',
        parts: { item: true, label: true, verdict: true },
      },
    },
  ],
  rects: {
    'places.item#0': { x: 200, y: 120, w: 100, h: 80 },
    'places.item#1': { x: 600, y: 240, w: 100, h: 80 },
  },
  run: { role: 'enter', beat: 'places', params: { duration: 1.5, drop: 28, stagger: 0.18 } },
};
const harnesses = [];
afterEach(() => harnesses.splice(0).forEach((h) => h.destroy()));

it('passes the contract', () => expect(checkMove(move, scenario, createHarness)).toEqual([]));

it('drops each item and lights its label at landing', () => {
  const h = createHarness({ beats: scenario.beats, rects: scenario.rects });
  harnesses.push(h);
  const run = h.runMove(move, scenario.run);
  const [item] = h.beats.get('places').part('item');
  const [label] = h.beats.get('places').part('label');
  h.seek(0);
  expect(Number(run.ctx.gsap.getProperty(item, 'y'))).toBe(-28);
  h.seek(0.5);
  const lit = String(run.ctx.gsap.getProperty(label, 'color'));
  h.seek(run.timing.duration);
  expect(Number(run.ctx.gsap.getProperty(item, 'opacity'))).toBe(1);
  expect(String(run.ctx.gsap.getProperty(label, 'color'))).not.toBe(lit);
});
