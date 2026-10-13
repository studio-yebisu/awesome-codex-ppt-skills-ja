/** Draws a central divider before separating a comparison into its authored positions. */
import { countTo } from '../_shared/count.js';
import { drawOn, line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));

export default {
  id: 'divider-split',
  family: 'assemble',
  role: 'enter',
  accepts: ['compare'],
  sources: ['split-slide', 'push-transition', 'line-draw', 'split-compare', 'count-up'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.6, max: 2.6, doc: '전체 길이(u)' },
    spread: { type: 'number', default: 48, min: 0, max: 160, doc: '항목이 선에서 출발하는 거리(px)' },
    count: { type: 'boolean', default: false, doc: 'value를 0에서 세어 올림' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const items = usable(ctx, 'item');
    const divider = usable(ctx, 'divider');
    const values = usable(ctx, 'value');
    const text = usable(ctx, 'text');
    const verdict = usable(ctx, 'verdict');
    const center = ctx.viewport.w / 2;

    divider.forEach((node, index) => {
      const rect = ctx.beat.anchor('divider', index).rect;
      ctx.initial(node, { scaleY: 0, transformOrigin: 'top' });
      tl.to(node, { scaleY: 1, duration: d * 0.3, ease: ctx.ease('out') }, 0);
      const svg = svgLayer(ctx);
      const stroke = line(svg, rect.x + rect.w / 2, rect.y, rect.x + rect.w / 2, rect.y + rect.h, {
        stroke: ctx.colors?.rule ?? '#444444',
        'stroke-width': 2,
      });
      drawOn(tl, stroke, { at: 0, duration: d * 0.3, ease: ctx.ease('out') });
    });

    items.forEach((node, index) => {
      const rect = ctx.beat.anchor('item', index).rect;
      const direction = rect.x + rect.w / 2 < center ? 1 : -1;
      const at = d * (0.25 + Math.min(0.12, index * 0.06));
      ctx.initial(node, { autoAlpha: 0, x: direction * px(ctx, params.spread) });
      tl.to(node, { autoAlpha: 1, x: 0, duration: d * 0.45, ease: ctx.ease('out') }, at);
    });
    [...values, ...text].forEach((node, index) => {
      ctx.initial(node, { autoAlpha: 0 });
      tl.to(node, { autoAlpha: 1, duration: d * 0.24, ease: ctx.ease('out') }, d * 0.33 + index * 0.02);
    });
    if (params.count) {
      values.forEach((node, index) => {
        const value = ctx.beat.data.items?.[index]?.value;
        if (typeof value !== 'number') return;
        countTo(tl, node, {
          from: 0,
          to: value,
          at: d * 0.3,
          duration: d * 0.5,
          ease: ctx.ease('out'),
          lang: ctx.beat.data.lang ?? 'ko',
        });
      });
    }
    ctx.initial(verdict, { autoAlpha: 0, yPercent: 40 });
    tl.to(verdict, { autoAlpha: 1, yPercent: 0, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.7);
  },
};
