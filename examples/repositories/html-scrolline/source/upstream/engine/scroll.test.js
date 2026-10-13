import { beforeEach, describe, expect, it, vi } from 'vitest';

const mock = vi.hoisted(() => ({
  handlers: new Map(),
  scrollTo: vi.fn(),
  raf: vi.fn(),
  destroy: vi.fn(),
  create: vi.fn(),
  update: vi.fn(),
  tickerAdd: vi.fn(),
  tickerRemove: vi.fn(),
  lag: vi.fn(),
  register: vi.fn(),
}));

vi.mock('lenis', () => ({
  default: class Lenis {
    constructor(options) {
      this.options = options;
    }
    on(name, fn) {
      mock.handlers.set(name, fn);
    }
    off(name) {
      mock.handlers.delete(name);
    }
    scrollTo = mock.scrollTo;
    raf = mock.raf;
    destroy = mock.destroy;
  },
}));
vi.mock('gsap', () => ({
  gsap: {
    registerPlugin: mock.register,
    ticker: { add: mock.tickerAdd, remove: mock.tickerRemove, lagSmoothing: mock.lag },
  },
}));
vi.mock('gsap/ScrollTrigger', () => ({ ScrollTrigger: { create: mock.create, update: mock.update } }));

import { createScrollDriver } from './scroll.js';

const map = { duration: 10, unit: 0.5, stops: [{ name: 'one', label: 'stop:one', t: 4, beat: 'b1' }] };

describe('createScrollDriver', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    mock.handlers.clear();
    Object.values(mock)
      .filter((item) => typeof item?.mockReset === 'function')
      .forEach((item) => item.mockReset());
    mock.create.mockReturnValue({ start: 100, end: 600, kill: vi.fn() });
  });

  it('uses the C2 track height and converts time/y in both directions', () => {
    const track = document.createElement('div');
    const tl = { time: vi.fn(() => 4), seek: vi.fn() };
    const driver = createScrollDriver({ track, tl, map, viewport: { h: 100 }, reduce: false });
    driver.attach();
    expect(track.style.height).toBe('600px');
    expect(driver.timeToY(4)).toBe(300);
    expect(driver.yToTime(driver.timeToY(7.25))).toBeCloseTo(7.25);
    expect(driver.stops()).toEqual([{ ...map.stops[0], y: 300 }]);
    expect(driver.lenis.options).toEqual({ lerp: 0.1, wheelMultiplier: 0.9, smoothWheel: true });
  });

  it('uses reduced Lenis options, seeks, and emits a stop only after scrolling settles at one', () => {
    const track = document.createElement('div');
    const tl = { time: vi.fn(() => 4), seek: vi.fn() };
    const driver = createScrollDriver({ track, tl, map, viewport: { h: 100 }, reduce: true });
    const received = vi.fn();
    window.addEventListener('scrolline:stop', received);
    driver.attach();
    driver.seek(4, { immediate: true });
    expect(mock.scrollTo).toHaveBeenCalledWith(300, { immediate: true });
    expect(tl.seek).toHaveBeenCalledWith(4);
    mock.handlers.get('scroll')();
    vi.advanceTimersByTime(149);
    expect(received).not.toHaveBeenCalled();
    vi.advanceTimersByTime(1);
    expect(received).toHaveBeenCalledWith(
      expect.objectContaining({ detail: { name: 'one', index: 0, beat: 'b1' } }),
    );
    window.removeEventListener('scrolline:stop', received);
  });

  // 회귀(?stop 브라우저 확인): attach 직후 seek이 ScrollTrigger 범위 계산 전이라 y 0으로 가서 t가 0에 남았다.
  it('measures the ScrollTrigger range on attach so an immediate seek lands at its y', () => {
    const range = { start: 0, end: 0, kill: vi.fn() };
    range.refresh = vi.fn(() => Object.assign(range, { start: 100, end: 600 }));
    mock.create.mockReturnValue(range);
    const track = document.createElement('div');
    const tl = { time: vi.fn(() => 0), seek: vi.fn() };
    const driver = createScrollDriver({ track, tl, map, viewport: { h: 100 }, reduce: false });
    driver.attach();
    expect(range.refresh).toHaveBeenCalledOnce();
    expect(driver.timeToY(4)).toBe(300);
  });
});
