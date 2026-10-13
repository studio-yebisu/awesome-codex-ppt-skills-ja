import { expect, it } from 'vitest';
import { gsap } from 'gsap';
import { build, plan } from './timeline.js';
import { createRegistry } from './registry.js';

// 회귀(data 통합): exit engine:fade-out이 part만 접어 차트의 step·link overlay(waffle canvas·주석)가
// exit 내내 켜 있다가 span 끝에서 한 프레임에 사라졌다.
it('fades the leaving beat move overlays with engine:fade-out and gives moves overlaysOf', () => {
  const seen = [];
  const draw = {
    id: 'draw',
    family: 'data',
    role: 'enter',
    accepts: ['*'],
    sources: ['t'],
    reduce: 'self',
    params: {},
    timing: () => ({ duration: 1, stops: [] }),
    build: (_tl, ctx) => {
      ctx.overlay.textContent = 'note';
      seen.push(ctx.overlaysOf(ctx.beat).length);
    },
  };
  const registry = createRegistry([draw]);
  const concept = { id: 't', timing: {}, defaults: {}, tokens: {}, eases: {} };
  const deck = {
    id: 'ov',
    lang: 'en',
    beats: [
      { id: 'a', type: 'text', text: 'A', enter: { move: 'draw' }, exit: { move: 'engine:fade-out', params: { duration: 1 } } },
      { id: 'b', type: 'text', text: 'B', enter: { move: 'engine:fade-in' } },
    ],
  };
  const map = plan(deck, { registry, concept, beatTypes: {} });
  const root = document.createElement('div');
  const overlays = document.createElement('div');
  root.append(overlays);
  document.body.append(root);
  const stage = {
    root,
    viewport: {},
    placeBeat: (node) => root.append(node),
    overlayFor: (key) => {
      const node = document.createElement('div');
      node.dataset.overlayKey = key;
      overlays.append(node);
      return node;
    },
  };
  const text = {
    primary: 'block',
    render: () => {
      const node = document.createElement('section');
      const part = document.createElement('span');
      part.dataset.part = 'block';
      node.append(part);
      return { root: node, parts: { block: [part] } };
    },
  };
  const built = build(map, { stage, deck, registry, concept, beatTypes: { text }, gsap, measureFn: () => ({ x: 0, y: 0, w: 1, h: 1 }) });
  expect(seen).toEqual([0]);
  const note = [...overlays.children].find((n) => n.dataset.overlayKey.startsWith('a:enter'));
  const exit = map.beats[0].spans.find((s) => s.role === 'exit');
  built.tl.seek(exit.start + 0.01);
  expect(Number(gsap.getProperty(note, 'opacity'))).toBeGreaterThan(0.9);
  built.tl.seek(exit.start + (exit.end - exit.start) / 2);
  const mid = Number(gsap.getProperty(note, 'opacity'));
  expect(mid).toBeGreaterThan(0.1);
  expect(mid).toBeLessThan(0.9);
  built.tl.seek(exit.start + 0.01);
  expect(Number(gsap.getProperty(note, 'opacity'))).toBeGreaterThan(0.9);
  built.tl.kill();
  root.remove();
});
