import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const css = readFileSync('engine/engine.css', 'utf8');
const parts = {
  text: ['block', 'line', 'word', 'em'],
  photo: ['frame', 'media', 'caption'],
  video: ['frame', 'media', 'caption', 'credit'],
  number: ['value', 'digits', 'unit', 'label', 'source'],
  chart: ['plot', 'axis', 'mark', 'label', 'legend', 'source', 'title', 'dek', 'note', 'baseline'],
  chronology: [
    'track',
    'event',
    'date',
    'title',
    'note',
    'media',
    'dot',
    'stem',
    'source',
    'label',
    'caption',
    'counter',
    'reel',
    'ground',
    'ghost',
    'now',
    'tick',
  ],
  compare: ['item', 'label', 'value', 'text', 'divider', 'verdict', 'source'],
  quote: ['block', 'mark', 'word', 'by'],
  prompt: ['field', 'char', 'caret', 'label', 'result', 'word'],
  code: ['block', 'line', 'token', 'caret'],
};

describe('engine.css C4/C8/C11 v2', () => {
  it('keeps slot positioning free of transforms', () => {
    for (const slot of ['center', 'left', 'right', 'top', 'bottom', 'full', 'lower-third']) {
      const rule = css.match(new RegExp(`\\.sl-slot-${slot.replace('-', '\\-')}\\s*\\{([^}]*)\\}`));
      expect(rule?.[1]).not.toMatch(/transform\s*:/);
    }
  });

  it('defines every standard beat part selector', () => {
    for (const [type, names] of Object.entries(parts))
      for (const name of names) expect(css).toContain(`.sl-${type}__${name}`);
  });

  it('uses tokens, state layers, and a vertical chronology reel', () => {
    expect(css).toContain('--sl-size-xl');
    expect(css).toContain('--sl-fg');
    expect(css).toContain('--sl-caption-left');
    expect(css).toMatch(/\[data-state\][\s\S]*visibility/);
    expect(css).toMatch(/\.sl-chronology__reel\s*\{[^}]*flex-direction:\s*column/);
    expect(css.replace(/\.sl-blackout\s*\{[^}]*\}/g, '')).not.toMatch(/#|rgb\s*\(/i);
  });
});
