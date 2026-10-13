/** Recounts the waffle that line-to-waffle laid down for another category of the same chart.
 *  켜진 칸 가운데 새 값을 넘는 칸이 끝에서부터 하나씩 식어 테두리만 남는다(둘의 간격이 보이게).
 *  오른쪽 범주 이름이 바뀌고 큰 값이 새 값까지 센다. 격자가 없으면(link 없이 쓰면) 같은 자리에 새로 깐다. */
import { colorOf } from '../_shared/color.js';
import { driveValue } from '../_shared/drive.js';
import { px } from '../_shared/timeline.js';
import { fmt, overlaysOf, swapLayers } from './annotation-pin.js';
import { cell, waffleGeom, waffleLegend } from './line-to-waffle.js';

const valueAt = (data, index) => data.series?.[0]?.values?.[index] ?? 0;
export default {
  id: 'waffle-recount',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['unit-grid', 'color-encoding-transition'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.6, max: 3, doc: '전체 길이(u)' },
    index: { type: 'integer', default: 1, min: 0, max: 10, doc: '새로 셀 범주 index' },
    from: { type: 'integer', default: 0, min: 0, max: 10, doc: '지금 격자가 보여 주는 범주 index' },
    cells: { type: 'integer', default: 100, min: 20, max: 400, doc: '격자 칸 수' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      R = ctx.reduce ? 0.001 : 1,
      data = ctx.beat.data,
      scale = params.cells / 100;
    const a = Math.round(valueAt(data, params.from) * scale),
      b = Math.round(valueAt(data, params.index) * scale);
    const g = waffleGeom(ctx.beat, { cells: params.cells }),
      accent = colorOf(ctx, 'accent'),
      bg = colorOf(ctx, 'bg');
    const prior = overlaysOf(ctx, ctx.beat.id);
    let cells = prior.filter((n) => n.classList?.contains('sl-data-cell'));
    if (cells.length !== params.cells)
      cells = g.list.map((c) => cell(ctx, g, c, c.i < a ? accent : colorOf(ctx, 'rule')));
    const lo = Math.min(a, b),
      hi = Math.max(a, b),
      cooling = b < a;
    const changing = cells.filter((n) => Number(n.dataset.cell) >= lo && Number(n.dataset.cell) < hi);
    if (cooling) changing.reverse();
    const ring = px(ctx, 3);
    changing.forEach((node, k) => {
      const at = d * (0.1 + (0.5 * k) / Math.max(1, changing.length));
      const vars = cooling
        ? { backgroundColor: bg, boxShadow: `inset 0 0 0 ${ring}px ${accent}` }
        : { backgroundColor: accent, boxShadow: `inset 0 0 0 0px ${accent}` };
      ctx.initial(node, cooling ? { boxShadow: `inset 0 0 0 0px ${accent}` } : {});
      tl.to(node, { ...vars, duration: d * 0.14 * R, ease: ctx.ease('settle') }, at);
    });
    // 오른쪽 범주 이름 교체 + 큰 값 다시 세기
    const oldLabel = prior.filter((n) => n.classList?.contains('sl-data-waffle-label'));
    const oldBig = prior.filter((n) => n.classList?.contains('sl-data-waffle-value'));
    const legend = waffleLegend(ctx, ctx.beat, g, params.index, a);
    ctx.initial(legend.label, { autoAlpha: 0, y: px(ctx, 16) });
    tl.to(oldLabel, { autoAlpha: 0, y: -px(ctx, 16), duration: d * 0.12 * R, ease: ctx.ease('in') }, d * 0.05);
    tl.to(legend.label, { autoAlpha: 1, y: 0, duration: d * 0.16 * R, ease: ctx.ease('settle') }, d * 0.12);
    ctx.initial(legend.big, { autoAlpha: 0 });
    tl.set(oldBig, { autoAlpha: 0 }, d * 0.1);
    tl.set(legend.big, { autoAlpha: 1 }, d * 0.1);
    driveValue(tl, (v) => (legend.digits.textContent = fmt(Math.round(v))), { from: a, to: b, at: d * 0.1, duration: d * 0.55 * R, ease: 'none' });
    swapLayers(tl, ctx, d * 0.55, d * 0.25 * R, ['title', 'dek', 'unit', 'note']);
  },
};
