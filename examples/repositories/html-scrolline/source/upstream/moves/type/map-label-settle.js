/** Map-label tracking settles line by line, then sweeps emphasis into accent. */
import { colorOf } from '../_shared/color.js';
export default {
  id: 'map-label-settle',
  family: 'type',
  role: 'enter',
  accepts: ['text'],
  sources: ['tracking-reveal', 'word-rise-fade', 'highlight-sweep'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.3, min: 0.6, max: 2.4, doc: '전체 길이(u)' },
    spread: { type: 'number', default: 0.45, min: 0.1, max: 0.8, doc: '벌림 거리' },
    lineOverlap: { type: 'number', default: 0.5, min: 0, max: 1, doc: 'lineOverlap(안무 설명의 같은 이름)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const lines = ctx.skipParts.includes('line') ? [] : ctx.beat.part('line');
    const each = p.duration * 0.5,
      step = each * (1 - p.lineOverlap);
    lines.forEach((node, i) => {
      const at = Math.min(i * step, p.duration - each);
      ctx.initial(node, { letterSpacing: `${p.spread}em`, x: `${p.spread / 2}em`, autoAlpha: 0 });
      tl.to(node, { letterSpacing: '0em', x: 0, autoAlpha: 1, duration: each, ease: ctx.ease('out') }, at);
    });
    const em = ctx.skipParts.includes('em') ? [] : ctx.beat.part('em');
    em.forEach((node) => {
      ctx.initial(node, { color: colorOf(ctx, 'fg'), clipPath: 'inset(0 100% 0 0)' });
      tl.to(
        node,
        {
          color: colorOf(ctx, 'accent'),
          clipPath: 'inset(0 0% 0 0)',
          duration: p.duration * 0.3,
          ease: ctx.ease('out'),
        },
        p.duration * 0.6,
      );
    });
  },
};
