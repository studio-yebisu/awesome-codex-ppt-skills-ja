/** Inks line series in from left to right, one head per series, up to a chosen category.
 *  렌더러 선 대신 같은 좌표의 선을 overlay에 그린다(upto 이후 구간은 다음 step 몫이라 숨김).
 *  선 머리가 지나는 자리마다 점이 찍히고, 끝점에 「이름 값」 표, 첫 점에 값 표. 강조 계열 = 주홍, 둘째 계열 = accent-2. */
import { colorOf } from '../_shared/color.js';
import { polyline, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';
import { draw, fmt, pointAt, tag } from './annotation-pin.js';

const part = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((n) => !ctx.skipNodes.includes(n)));
const base = (nodes) => nodes.filter((node) => (node.dataset.state ?? 'base') === 'base');
const NS = 'http://www.w3.org/2000/svg';

/** 계열 색 이름: highlight 계열 = accent, 그 밖 첫 계열 = fg(한 계열뿐일 때) 또는 accent-2. */
export function seriesTone(data, si) {
  const hi = data.highlight?.series;
  const hiIndex = typeof hi === 'number' ? hi : data.series.findIndex((s) => s.name === hi);
  if (data.series.length === 1) return 'fg';
  return si === hiIndex ? 'accent' : 'accent-2';
}
export const valueText = (v, unit = '') => `${fmt(v, Number.isInteger(v) ? 0 : 1)}${unit}`;

export default {
  id: 'ink-in',
  family: 'data',
  role: 'enter',
  accepts: ['chart'],
  sources: ['outline-then-fill', 'line-draw', 'line-chart-race'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 2, min: 0.6, max: 3.5, doc: '전체 길이(u)' },
    upto: { type: 'integer', default: -1, min: -1, max: 40, doc: '여기 범주까지 그림(-1 = 끝까지)' },
    names: { type: 'boolean', default: true, doc: '끝점에 계열 이름(여러 계열일 때)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      data = ctx.beat.data,
      n = data.categories.length,
      last = params.upto < 0 ? n - 1 : Math.min(n - 1, params.upto),
      unit = data.unit ?? '';
    // 렌더러 선·점은 overlay 선이 대신한다
    ctx.initial(part(ctx, 'mark'), { autoAlpha: 0 });
    const text = ['title', 'dek', 'unit', 'source'].flatMap((name) => base(part(ctx, name)));
    ctx.initial(text, { autoAlpha: 0, yPercent: 30 });
    tl.to(text, { autoAlpha: 1, yPercent: 0, duration: d * 0.2, ease: ctx.ease('settle') }, 0);
    const support = [...part(ctx, 'axis'), ...part(ctx, 'label').filter((_, i) => i <= last)];
    const later = part(ctx, 'label').filter((_, i) => i > last);
    ctx.initial(support, { autoAlpha: 0 });
    ctx.initial(later, { autoAlpha: 0 });
    tl.to(support, { autoAlpha: 1, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.05);
    const svg = svgLayer(ctx),
      t0 = d * 0.2,
      span = d * 0.6;
    data.series.forEach((series, si) => {
      const pts = series.values.slice(0, last + 1).map((v, i) => pointAt(ctx.beat, i, v));
      const color = colorOf(ctx, seriesTone(data, si));
      const path = polyline(svg, pts, { stroke: color, 'stroke-width': px(ctx, 5), 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
      draw(tl, ctx, path, { at: t0, duration: span, ease: 'none' });
      pts.forEach((p, i) => {
        const c = document.createElementNS(NS, 'circle');
        c.setAttribute('cx', String(p.x));
        c.setAttribute('cy', String(p.y));
        c.setAttribute('r', String(px(ctx, i === last ? 11 : 7)));
        c.setAttribute('fill', color);
        svg.append(c);
        ctx.initial(c, { autoAlpha: 0 });
        tl.to(c, { autoAlpha: 1, duration: d * 0.05, ease: ctx.ease('out') }, t0 + span * (last ? i / last : 1) - d * 0.02);
      });
      // 첫 값·끝 값(여러 계열이면 끝에 이름도)
      const first = pts[0],
        end = pts.at(-1);
      const name = data.series.length > 1 && params.names ? `${series.name} ` : '';
      const tEnd =
        data.series.length > 1
          ? tag(ctx, `${name}${valueText(series.values[last], unit)}`, { x: end.x + px(ctx, 22), y: end.y, valign: 'middle', size: 30, weight: 800, color: seriesTone(data, si) })
          : tag(ctx, valueText(series.values[last], unit), { x: end.x, y: end.y - px(ctx, 24), align: 'center', valign: 'bottom', size: 36, weight: 800, color: 'fg' });
      const tFirst =
        data.series.length > 1
          ? tag(ctx, valueText(series.values[0], unit), { x: first.x - px(ctx, 20), y: first.y, align: 'right', valign: 'middle', size: 24, weight: 600, color: 'fg-muted' })
          : tag(ctx, valueText(series.values[0], unit), { x: first.x, y: first.y - px(ctx, 18), align: 'center', valign: 'bottom', size: 24, weight: 600, color: 'fg-muted' });
      ctx.initial([tEnd, tFirst], { autoAlpha: 0 });
      tl.to(tFirst, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, t0);
      tl.to(tEnd, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, t0 + span);
      tEnd.classList.add('sl-data-end');
    });
  },
};
