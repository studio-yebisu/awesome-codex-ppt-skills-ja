import { describe, expect, it } from 'vitest';
import { chars, el, words } from './dom.js';

describe('DOM helpers', () => {
  it('creates elements and splits Korean into whitespace-delimited words', () => {
    const parent = document.createElement('div');
    const node = el('p', 'copy', parent, 'hi');
    expect(node.className).toBe('copy');
    expect(words(parent, '안녕 세상  반가워').map((n) => n.textContent)).toEqual(['안녕', '세상', '반가워']);
    expect(parent.textContent).toContain('세상  반가워');
  });
  it('splits characters while line feeds become br elements', () => {
    const parent = document.createElement('div');
    expect(chars(parent, '가 나\nA').map((n) => n.textContent)).toEqual(['가', ' ', '나', 'A']);
    expect(parent.querySelectorAll('br')).toHaveLength(1);
  });
});
