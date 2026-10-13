import { beforeEach, describe, expect, it, vi } from 'vitest';
import { createPresenter } from './presenter.js';

const stops = [
  { name: 'zero', label: 'stop:zero', t: 0, y: 0, beat: 'a' },
  { name: 'near', label: 'stop:near', t: 0.005, y: 1, beat: 'a' },
  { name: 'two', label: 'stop:two', t: 2, y: 200, beat: 'b' },
  { name: 'five', label: 'stop:five', t: 5, y: 500, beat: 'c' },
];

function driver(time = 0) {
  return { stops: () => stops, time: vi.fn(() => time), timeToY: vi.fn((t) => t * 100), seek: vi.fn() };
}
function key(target, key, init = {}) {
  target.dispatchEvent(new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true, ...init }));
}

describe('createPresenter', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    Object.defineProperty(globalThis, 'innerHeight', { value: 100, configurable: true });
  });

  it('maps all navigation keys and skips stops closer than 0.01u', () => {
    const target = new EventTarget();
    const d = driver();
    const presenter = createPresenter(d, { reduce: true, target });
    ['ArrowRight', 'ArrowDown', 'PageDown', ' '].forEach((name) => key(target, name));
    expect(d.seek).toHaveBeenCalledWith(2, { immediate: true });
    key(target, ' ', { shiftKey: true });
    ['ArrowLeft', 'ArrowUp', 'PageUp'].forEach((name) => key(target, name));
    key(target, 'Home');
    key(target, 'End');
    expect(d.seek).toHaveBeenCalledWith(0, { immediate: true });
    expect(d.seek).toHaveBeenCalledWith(5, { immediate: true });
    presenter.destroy();
  });

  it('ignores modified keys and yields Space to a focused link or input', () => {
    const d = driver();
    const link = document.createElement('a');
    document.body.append(link);
    link.focus();
    const presenter = createPresenter(d, { reduce: true, target: window, doc: document });
    key(window, ' ');
    key(window, 'ArrowRight', { metaKey: true });
    key(window, 'ArrowRight', { ctrlKey: true });
    expect(d.seek).not.toHaveBeenCalled();
    presenter.destroy();
    link.remove();
  });

  it('uses the specified travel formula and reduce is immediate', () => {
    const target = new EventTarget();
    const d = driver();
    const presenter = createPresenter(d, { reduce: false, target });
    presenter.goto('two');
    expect(d.seek).toHaveBeenCalledWith(2, { duration: 1.6 });
    presenter.destroy();
  });

  it('toggles blackout and announces a presenter arrival stop', () => {
    const target = new EventTarget();
    const d = driver();
    const blackouts = [];
    const arrived = [];
    target.addEventListener('scrolline:blackout', (event) => blackouts.push(event.detail));
    target.addEventListener('scrolline:stop', (event) => arrived.push(event.detail));
    const presenter = createPresenter(d, { reduce: true, target });
    presenter.blackout();
    presenter.blackout(false);
    presenter.goto('two');
    expect(blackouts).toEqual([{ on: true }, { on: false }]);
    expect(arrived).toEqual([{ name: 'two', index: 2, beat: 'b' }]);
    presenter.destroy();
  });
});
