/** Draws a chart baseline before growing bars from it without rebound. */
import { drawOn } from '../_shared/stroke.js';

const part = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name));
const chartText = (ctx) => ['title', 'dek', 'source'].flatMap((name) => part(ctx, name));

export default {
  id: 'baseline-grow',
  family: 'data',
  role: 'enter',
  accepts: ['chart'],
  sources: ['bar-grow', 'count-up'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.5, max: 2.4, doc: '전체 길이(u)' },
    stagger: { type: 'number', default: 0.04, min: 0, max: 0.2, doc: '항목 간 시차(u)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      horizontal = ctx.beat.data.orient === 'h';
    const baseline = part(ctx, 'baseline')[0] ?? part(ctx, 'axis')[0];
    if (baseline) {
      baseline.setAttribute?.('pathLength', '1');
      baseline.style.strokeDasharray = '1 1';
      ctx.initial(baseline, { strokeDashoffset: 1 });
      tl.to(baseline, { strokeDashoffset: 0, duration: d * 0.25, ease: ctx.ease('out') }, 0);
    }
    const marks = part(ctx, 'mark');
    marks.forEach((node, i) => {
      ctx.initial(
        node,
        horizontal
          ? { scaleX: 0, transformOrigin: 'left center' }
          : { scaleY: 0, transformOrigin: 'center bottom' },
      );
      tl.to(
        node,
        horizontal
          ? { scaleX: 1, duration: d * 0.65, ease: ctx.ease('out') }
          : { scaleY: 1, duration: d * 0.65, ease: ctx.ease('out') },
        d * 0.15 + i * params.stagger,
      );
    });
    const labels = part(ctx, 'label');
    ctx.initial(labels, { autoAlpha: 0 });
    labels.forEach((node, i) =>
      tl.to(
        node,
        { autoAlpha: 1, duration: d * 0.2, ease: ctx.ease('out') },
        d * 0.55 + i * Math.min(params.stagger, 0.04),
      ),
    );
    const text = chartText(ctx);
    ctx.initial(text, { autoAlpha: 0 });
    tl.to(text, { autoAlpha: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.7);
  },
};
