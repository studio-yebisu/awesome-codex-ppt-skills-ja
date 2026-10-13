import { describe, expect, it, vi } from 'vitest';
import { SLOT_DEFAULTS } from './constants.js';
import { computeViewport, createStage } from './stage.js';

describe('stage', () => {
  it.each([
    [1920, 1080, false, 1],
    [390, 844, true, 390 / 760],
    [1280, 1024, false, 1280 / 1920],
  ])('computes %ix%i viewport', (w, h, portrait, px) => {
    expect(computeViewport(w, h, 3)).toMatchObject({ w, h, portrait, px, dpr: 2 });
  });
  it('places slot and world beats and clamps camera tilt', () => {
    const host = document.createElement('div');
    const viewport = computeViewport(1920, 1080);
    const stage = createStage(host, { viewport, concept: { id: 'rail' } });
    const slot = document.createElement('section'),
      world = document.createElement('section');
    stage.placeBeat(slot, { slot: 'lower-third' });
    stage.placeBeat(world, { world: { x: 1, y: 0.5, z: 40, s: 2 } });
    expect(slot.classList.contains('sl-slot-lower-third')).toBe(true);
    expect(stage.screen.contains(slot)).toBe(true);
    expect(world.classList.contains('sl-place-world')).toBe(true);
    expect(world.style.left).toBe('1920px');
    expect(stage.world.contains(world)).toBe(true);
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const vars = stage.cameraVars({ x: 1, y: 0.5, s: 2, rx: 20, ry: -20 });
    expect(vars).toMatchObject({
      x: -2880,
      y: -540,
      scale: 2,
      rotationX: 12,
      rotationY: -12,
      transformOrigin: '0 0',
    });
    expect(warn).toHaveBeenCalled();
    warn.mockRestore();
  });

  it('uses slot defaults and key-level concept overrides without transforms', () => {
    const host = document.createElement('div');
    const viewport = computeViewport(1000, 500);
    const stage = createStage(host, {
      viewport,
      concept: { id: 'kinetic', slots: { left: { x: 0.1, y: 0.46 }, center: { w: 0.6 } } },
    });
    const left = document.createElement('section');
    const center = document.createElement('section');
    const full = document.createElement('section');
    stage.placeBeat(left, { slot: 'left' });
    stage.placeBeat(center, { slot: 'center' });
    stage.placeBeat(full, { slot: 'full' });
    expect(left.style.cssText).toContain('left: 10%;');
    expect(left.style.cssText).toContain('top: 46%;');
    expect(left.style.translate).toBe('0% -50%');
    expect(left.style.transform).toBe('');
    expect(center.style.maxWidth).toBe('60%');
    expect(full.style.inset).toBe('0');
  });

  it.each(['center', 'left', 'right', 'top', 'bottom', 'full', 'lower-third'])(
    'places the %s default with inline layout properties',
    (slot) => {
      const stage = createStage(document.createElement('div'), {
        viewport: computeViewport(1000, 500),
        concept: { id: 'rail' },
      });
      const beat = document.createElement('section');
      stage.placeBeat(beat, { slot });
      expect(beat.classList.contains(`sl-slot-${slot}`)).toBe(true);
      expect(beat.style.transform).toBe('');
      if (slot === 'full') {
        expect(beat.style.inset).toBe('0');
        return;
      }
      const { x, y, ax, ay } = SLOT_DEFAULTS[slot];
      expect(beat.style.left).toBe(`${x * 100}%`);
      expect(beat.style.top).toBe(`${y * 100}%`);
      expect(beat.style.translate).toBe(`${-ax * 100}% ${-ay * 100}%`);
    },
  );

  it('places world beats with individual translate and scale properties', () => {
    const host = document.createElement('div');
    const stage = createStage(host, { viewport: computeViewport(1000, 500), concept: { id: 'canvas' } });
    const world = document.createElement('section');
    stage.placeBeat(world, { world: { x: 0.25, y: 0.5, z: 32, s: 1.4 } });
    expect(world.style.left).toBe('250px');
    expect(world.style.top).toBe('250px');
    expect(world.style.translate).toBe('0 0 32px');
    expect(world.style.scale).toBe('1.4');
    expect(world.style.transform).toBe('');
  });
});
