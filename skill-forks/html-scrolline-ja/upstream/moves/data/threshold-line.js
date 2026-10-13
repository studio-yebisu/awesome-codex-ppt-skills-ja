/** Draws a reference rule through a chart at one category's value and cools every mark below it.
 *  기준 범주(refIndex) 값에 세로(가로 막대) 또는 가로(세로 막대) 기준선을 긋고 이름표를 단다.
 *  기준 아래 막대는 회색으로 식고, focusIndex 막대만 주홍으로 남는다. 상태 층 글자도 교체. */
import { colorOf } from '../_shared/color.js';
import { line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';
import { draw, overlaysOf, plotBox, rangeOf, swapLayers, tag } from './annotation-pin.js';

export default {
  id: 'threshold-line',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['threshold-pulse', 'chart-filter-fade', 'line-draw'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.5, max: 3, doc: '전체 길이(u)' },
    refIndex: { type: 'integer', default: 0, min: 0, max: 40, doc: '기준 범주 index' },
    focusIndex: { type: 'integer', default: -1, min: -1, max: 40, doc: '주홍으로 남길 범주(-1 = highlight)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      R = ctx.reduce ? 0.001 : 1,
      data = ctx.beat.data,
      values = data.series[0].values,
      ref = values[params.refIndex],
      box = plotBox(ctx.beat),
      range = rangeOf(data.series),
      horizontal = data.orient === 'h',
      focus = params.focusIndex >= 0 ? params.focusIndex : (data.highlight?.index ?? -1),
      accent = colorOf(ctx, 'accent');
    const svg = svgLayer(ctx);
    const at = horizontal
      ? box.x + ((ref - range.min) / (range.max - range.min)) * box.w
      : box.y + box.h - ((ref - range.min) / (range.max - range.min)) * box.h;
    const pad = px(ctx, 36);
    const rule = horizontal
      ? line(svg, at, box.y - pad * 0.3, at, box.y + box.h + pad * 0.3, { stroke: colorOf(ctx, 'fg'), 'stroke-width': px(ctx, 3) })
      : line(svg, box.x - pad * 0.3, at, box.x + box.w + pad, at, { stroke: colorOf(ctx, 'fg'), 'stroke-width': px(ctx, 3) });
    ctx.reduce ? tl.set(rule, { strokeDashoffset: 0 }, 0) : draw(tl, ctx, rule, { at: 0, duration: d * 0.3, ease: ctx.ease('inout') });
    const name = data.categories[params.refIndex];
    const unit = data.unit ?? '';
    const label = horizontal
      ? tag(ctx, `${name} ${ref}${unit}`, { x: at, y: box.y + box.h + pad * 0.3 + px(ctx, 8), align: 'center', valign: 'top', size: 28, weight: 700 })
      : tag(ctx, `${name} ${ref}${unit}`, { x: box.x + box.w + pad + px(ctx, 10), y: at, valign: 'middle', size: 28, weight: 700 });
    ctx.initial(label, { autoAlpha: 0 });
    tl.to(label, { autoAlpha: 1, duration: d * 0.15 * R, ease: ctx.ease('out') }, d * 0.22);
    // 기준 아래는 식고, focus만 주홍
    const marks = ctx.beat.part('mark').filter((m) => m.dataset.series === '0' && m.tagName.toLowerCase() !== 'path');
    const tags = overlaysOf(ctx, ctx.beat.id, (k) => k.includes(':link:') || k.includes(':enter:')).filter((n) => n.classList?.contains('sl-data-tag'));
    marks.forEach((m, i) => {
      ctx.initial(m, { fill: globalThis.getComputedStyle?.(m).fill || colorOf(ctx, 'fg') });
      if (tags[i]) ctx.initial(tags[i], { color: tags[i].style.color || colorOf(ctx, 'fg') });
      const below = values[i] < ref;
      const color = i === focus ? accent : below ? colorOf(ctx, 'rule') : i === params.refIndex ? colorOf(ctx, 'fg') : colorOf(ctx, 'fg');
      tl.to(m, { fill: color, duration: d * 0.25 * R, ease: ctx.ease('out') }, d * (0.35 + (0.2 * i) / marks.length));
      const t = tags[i];
      if (t)
        tl.to(t, { color: i === focus ? accent : below ? colorOf(ctx, 'fg-muted') : colorOf(ctx, 'fg'), fontWeight: i === focus ? 800 : 600, fontSize: `${px(ctx, i === focus ? 34 : 26)}px`, duration: d * 0.25 * R }, d * (0.35 + (0.2 * i) / marks.length));
    });
    swapLayers(tl, ctx, d * 0.5, d * 0.3 * R, ['title', 'dek', 'unit', 'note']);
  },
};
