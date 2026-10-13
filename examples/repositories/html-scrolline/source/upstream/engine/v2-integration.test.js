import { describe, expect, it } from 'vitest';
import { gsap } from 'gsap';
import { beatTypes } from './beats/index.js';
import { createRegistry } from './registry.js';
import { createStage } from './stage.js';
import { build, plan } from './timeline.js';

const fakeMove = (id, role, build = () => {}) => ({
  id,
  family: 'emphasis',
  role,
  accepts: ['*'],
  sources: ['integration-test'],
  reduce: 'self',
  params: {},
  timing: () => ({ duration: 0.2 }),
  build,
});

describe('v2 engine integration', () => {
  it('uses real beats, handoff anchors, state layers, persist, and sequence construction', () => {
    const handoff = {
      ...fakeMove('test-handoff', 'link'),
      handoff: () => ({ from: { part: 'word', index: 0 }, to: { part: 'word', index: 1 } }),
    };
    const step = fakeMove('test-step', 'step', (tl, ctx) => {
      const states = Object.values(ctx.beat.parts)
        .flat()
        .filter((node) => node.closest('[data-state]'));
      const next = states.filter((node) => node.closest('[data-state]').dataset.state === ctx.step.name);
      const other = states.filter((node) => node.closest('[data-state]').dataset.state !== ctx.step.name);
      ctx.initial(next, { autoAlpha: 0 });
      tl.to(other, { autoAlpha: 0, duration: ctx.duration }, 0);
      tl.to(next, { autoAlpha: 1, duration: ctx.duration }, 0);
    });
    const registry = createRegistry([handoff, step]);
    const sequence = {
      primary: 'ground',
      timing: () => ({ duration: 0.2 }),
      render: () => {
        const root = document.createElement('section');
        const ground = document.createElement('div');
        ground.dataset.part = 'ground';
        root.append(ground);
        return { root, parts: { ground: [ground] } };
      },
      build: () => {},
    };
    const concept = { id: 'test', timing: { hold: 0 }, defaults: {}, tokens: {}, eases: {}, slots: {} };
    const deck = {
      id: 'integration',
      lang: 'en',
      beats: [
        {
          id: 'a',
          type: 'text',
          text: 'Source',
          place: { world: { x: 0, y: 0, s: 1 } },
          persist: true,
          link: { move: 'test-handoff' },
        },
        { id: 'b', type: 'text', text: 'One two', enter: { move: 'engine:fade-in' } },
        {
          id: 'chart',
          type: 'chart',
          kind: 'bar',
          categories: ['A', 'B'],
          series: [{ name: 'Series', values: [1, 2] }],
          title: 'Base',
          states: [{ name: 'next', title: 'Next' }],
          enter: { move: 'engine:none' },
          steps: [{ name: 'next', move: 'test-step' }],
        },
        { id: 'sequence', type: 'sequence', use: 'test-sequence', data: {} },
      ],
    };
    const map = plan(deck, { registry, concept, beatTypes, sequences: { 'test-sequence': sequence } });
    const host = document.createElement('div');
    document.body.append(host);
    const stage = createStage(host, {
      viewport: { w: 1920, h: 1080, px: 1, dpr: 1, portrait: false },
      concept,
    });
    const built = build(map, {
      stage,
      deck,
      registry,
      concept,
      beatTypes,
      sequences: { 'test-sequence': sequence },
      gsap,
      measureFn: () => ({ x: 0, y: 0, w: 100, h: 100 }),
    });
    const linkedNode = built.byId.get('b').part('word')[1];
    built.tl.pause(map.beats[1].start);
    expect(Number(gsap.getProperty(linkedNode, 'opacity'))).toBe(1);
    const chart = built.byId.get('chart');
    const layers = chart.root.querySelectorAll('[data-state]');
    built.tl.pause(map.beats[2].spans.find((span) => span.role === 'step').end);
    expect(
      [...layers]
        .filter((node) => node.dataset.state === 'next')
        .every((node) => Number(gsap.getProperty(node, 'opacity')) === 1),
    ).toBe(true);
    expect(
      [...layers]
        .filter((node) => node.dataset.state === 'base')
        .every((node) => Number(gsap.getProperty(node, 'opacity')) === 0),
    ).toBe(true);
    built.tl.pause(map.beats[0].end + 0.001);
    expect(Number(gsap.getProperty(built.byId.get('a').root, 'opacity'))).toBe(1);
    expect(built.byId.get('sequence').part('ground')).toHaveLength(1);
    built.destroy();
    host.remove();
  });
});
