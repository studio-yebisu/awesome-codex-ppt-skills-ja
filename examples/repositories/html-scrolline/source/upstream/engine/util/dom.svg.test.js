import { expect, it } from 'vitest';
import { el } from './dom.js';
import chart from '../beats/chart.js';

const SVG = 'http://www.w3.org/2000/svg';

// 회귀(zoom·data 통합): 차트 svg·rect·text가 HTML 이름공간으로 만들어져 브라우저에서 0×0, 막대가 안 그려졌다.
it('creates svg and its descendants in the SVG namespace, HTML elsewhere', () => {
  const host = el('div', 'host');
  const svg = el('svg', 'sl-chart', host);
  const g = el('g', 'axis', svg);
  const rect = el('rect', 'mark', g);
  const label = el('text', 'label', svg, 'A');
  const fo = el('foreignObject', null, svg);
  const inside = el('span', 'x', fo);
  expect([svg, g, rect, label, fo].map((n) => n.namespaceURI)).toEqual(Array(5).fill(SVG));
  expect(inside.namespaceURI).toBe('http://www.w3.org/1999/xhtml');
  expect(host.namespaceURI).toBe('http://www.w3.org/1999/xhtml');
  expect(rect.getAttribute('class')).toBe('mark');
  rect.classList.add('sl-chart__mark');
  expect(rect.getAttribute('class')).toBe('mark sl-chart__mark');
});

it('renders chart marks as SVG with or without rc.el', () => {
  const data = { kind: 'bar', categories: ['a', 'b'], series: [{ name: 's', values: [1, 2] }] };
  for (const rc of [{}, { el }]) {
    const view = chart.render(data, rc);
    expect(view.parts.plot[0].namespaceURI).toBe(SVG);
    expect(view.parts.mark.every((m) => m.namespaceURI === SVG)).toBe(true);
    expect(view.parts.label.every((m) => m.namespaceURI === SVG)).toBe(true);
  }
});
