/** Dims a chart until one conclusion point and its value are left standing. */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';
const part = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name));
export default {
  id: 'point-focus',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['focus-handoff', 'threshold-pulse'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1, min: 0.4, max: 2, doc: '전체 길이(u)' },
    dim: { type: 'number', default: 0.3, min: 0.1, max: 0.6, doc: '물린 대상 opacity' },
    index: { type: 'integer', default: -1, min: -1, max: 100, doc: '대상 요소 index' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      index = params.index < 0 ? (ctx.beat.data.highlight?.index ?? 0) : params.index,
      named = ctx.beat.data.highlight?.series ?? 0,
      // highlight.series is a series name or an index (C4 chart)
      found = (ctx.beat.data.series ?? []).findIndex((x) => x?.name === named),
      series = typeof named === 'number' ? named : Math.max(0, found);
    const marks = part(ctx, 'mark'),
      target =
        marks.find((n) => Number(n.dataset.index) === index && Number(n.dataset.series) === Number(series)) ??
        marks.filter((n) => n.dataset.index !== 'all')[index];
    const other = marks.filter((n) => n !== target);
    tl.to(other, { autoAlpha: params.dim, duration: d * 0.5, ease: ctx.ease('out') }, 0);
    if (target) {
      tl.to(
        target,
        { scale: 1.8, fill: colorOf(ctx, 'accent'), duration: d * 0.5, ease: ctx.ease('out') },
        d * 0.2,
      );
      const label = part(ctx, 'label')[index];
      if (label) {
        ctx.initial(label, { autoAlpha: 0, y: px(ctx, 8) });
        tl.to(label, { autoAlpha: 1, y: 0, duration: d * 0.5, ease: ctx.ease('out') }, d * 0.5);
      }
    }
  },
};
