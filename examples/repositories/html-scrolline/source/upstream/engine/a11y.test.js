import { describe, expect, it } from 'vitest';
import { createA11y, prefersReducedMotion } from './a11y.js';
import { EVENTS } from './constants.js';

describe('a11y', () => {
  it('gives motion=reduce precedence over matchMedia', () => {
    expect(prefersReducedMotion({ search: '?motion=reduce', matchMedia: () => ({ matches: false }) })).toBe(
      true,
    );
    expect(prefersReducedMotion({ search: '', matchMedia: () => ({ matches: true }) })).toBe(true);
  });
  it('announces stops and toggles inert for active beats', () => {
    const root = document.createElement('div'),
      first = document.createElement('section'),
      second = document.createElement('section');
    first.textContent = '첫 장면';
    second.textContent = '둘째 장면';
    root.append(first, second);
    const target = new EventTarget();
    const a11y = createA11y({
      stage: { root },
      beats: [
        { id: 'one', root: first },
        { id: 'two', root: second },
      ],
      target,
    });
    target.dispatchEvent(new CustomEvent(EVENTS.stop, { detail: { beat: 'two' } }));
    expect(root.querySelector('.sl-live').textContent).toBe('둘째 장면');
    target.dispatchEvent(new CustomEvent(EVENTS.active, { detail: { beat: 'one', phase: 'leave' } }));
    expect(first.inert).toBe(true);
    expect(first.hasAttribute('inert')).toBe(true);
    target.dispatchEvent(new CustomEvent(EVENTS.active, { detail: { beat: 'one', phase: 'enter' } }));
    expect(first.inert).toBe(false);
    a11y.destroy();
  });
});
