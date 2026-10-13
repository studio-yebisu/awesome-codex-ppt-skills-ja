import { expect, it } from 'vitest';
import { createHarness } from '../../engine/testing.js';
import move from './line-draw.js';

// 회귀: 선 머리 이름표 위치를 onUpdate에서 써서 seek(정지점·발표 키·export) 때 왼쪽 위 0,0에 남았다.
it('moves the head label along the line on a jump', () => {
  const h = createHarness({
    beats: [
      {
        id: 'c',
        type: 'chart',
        data: { categories: ['A', 'B'], series: [{ name: 'One', values: [1, 2] }], parts: { plot: true, mark: true, source: true } },
      },
    ],
  });
  const beat = h.beats.get('c');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  beat.part('mark')[0].replaceWith(path);
  beat.parts.mark[0] = path;
  path.setAttribute('d', 'M 0 0 L 100 50');
  path.dataset.series = '0';
  const r = h.runMove(move, { role: 'enter', beat: 'c', params: { duration: 1.8, headLabels: true, markPop: false } });
  h.seek(r.timing.duration);
  const label = r.ctx.overlay.querySelector('span');
  expect(label.style.left).toBe('100px');
  expect(label.style.top).toBe('50px');
  h.destroy();
});
