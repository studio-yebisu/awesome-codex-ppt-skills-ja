/** Rolls a numeric value to its final formatted value, then settles its supporting copy. */
import { countTo, formatNumber } from '../_shared/count.js';
import { partFree as part } from '../_shared/skip.js';
import { px } from '../_shared/timeline.js';

export default {
  id: 'count-roll',
  family: 'data',
  role: 'enter',
  accepts: ['number'],
  sources: ['count-up', 'rolling-digits'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.6, max: 3, doc: '전체 길이(u)' },
    ease: { type: 'ease', default: 'out', doc: '카운트 이징 alias(out|inout|none)' },
    unitSlide: {
      type: 'number',
      default: 0,
      min: 0,
      max: 24,
      doc: '단위 x 이동량(px×viewport.px). 0 = 숫자와 함께 등장',
    },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const data = ctx.beat.data;
    const format = data.format ?? {};
    const from = data.from ?? 0;
    const finalText = formatNumber(data.value, { lang: data.lang ?? 'ko', decimals: format.decimals ?? 0 });
    const digits = part(ctx, 'digits');
    const value = part(ctx, 'value');
    if (ctx.reduce) digits.forEach((node) => tl.set(node, { textContent: finalText }, 0));
    else if (value.length) {
      ctx.initial(value, { autoAlpha: 0 });
      ctx.initial(digits, { fontVariantNumeric: 'tabular-nums' });
      tl.to(value, { autoAlpha: 1, duration: d * 0.15, ease: ctx.ease('out') }, 0);
      digits.forEach((node) =>
        countTo(tl, node, {
          from,
          to: data.value,
          at: d * 0.1,
          duration: d * 0.65,
          ease: ctx.ease(params.ease),
          lang: data.lang ?? 'ko',
          decimals: format.decimals ?? 0,
        }),
      );
    }
    const units = part(ctx, 'unit');
    if (params.unitSlide === 0) {
      ctx.initial(units, { autoAlpha: 0 });
      tl.to(units, { autoAlpha: 1, duration: d * 0.15, ease: ctx.ease('out') }, d * 0.1);
    } else {
      ctx.initial(units, { autoAlpha: 0, x: -px(ctx, params.unitSlide) });
      tl.to(units, { autoAlpha: 1, x: 0, duration: d * 0.25, ease: ctx.ease('out') }, d * 0.6);
    }
    const labels = part(ctx, 'label');
    labels.forEach((node, i) => {
      ctx.initial(node, { autoAlpha: 0, y: px(ctx, 10) });
      tl.to(
        node,
        { autoAlpha: 1, y: 0, duration: d * 0.3, ease: ctx.ease('out') },
        d * 0.7 + i * (ctx.tokens.stagger ?? 0.04),
      );
    });
    const source = part(ctx, 'source');
    ctx.initial(source, { autoAlpha: 0 });
    tl.to(source, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.9);
  },
};
