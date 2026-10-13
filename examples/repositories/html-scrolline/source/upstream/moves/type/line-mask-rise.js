/** Headline lines rise through their own clipped windows. Shared by data, launch, and rail. */
import { colorOf } from '../_shared/color.js';
import { line, svgLayer } from '../_shared/stroke.js';

const parts = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name));
export default {
  id: 'line-mask-rise',
  family: 'type',
  role: 'enter',
  accepts: ['text', 'quote'],
  sources: ['mask-reveal', 'word-rise-fade', 'tracking-reveal', 'underline-draw'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.8, min: 0.4, max: 2, doc: '전체 길이(u)' },
    stagger: { type: 'number', default: 0.12, min: 0, max: 0.4, doc: '줄 간 시차(u)' },
    tracking: { type: 'number', default: 0.02, min: 0, max: 0.1, doc: '시작 자간 가산(em)' },
    emDelay: { type: 'number', default: 0.7, min: 0.4, max: 0.95, doc: 'em 강조 시작 비율' },
    rule: { type: 'boolean', default: false, doc: '위 괘선 먼저' },
    emStyle: { type: 'enum', default: 'color', values: ['color', 'underline'], doc: '강조 방식' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const d = p.duration,
      isQuote = ctx.beat.type === 'quote';
    const units = isQuote ? parts(ctx, 'word') : parts(ctx, 'line');
    const animated = isQuote
      ? units
      : units.flatMap((node) => [...node.querySelectorAll('[data-part="word"]')]);
    ctx.initial(units, { clipPath: 'inset(0)' });
    ctx.initial(animated, { yPercent: 105, autoAlpha: 0 });
    // 마지막 단위도 d 안에 끝나도록 시차를 줄인다(어절이 많은 인용).
    const stagger = animated.length > 1 ? Math.min(p.stagger, (d * 0.3) / (animated.length - 1)) : 0;
    animated.forEach((node, i) =>
      tl.to(node, { yPercent: 0, autoAlpha: 1, duration: d * 0.7, ease: ctx.ease('out') }, i * stagger),
    );
    if (p.tracking > 0) {
      ctx.initial(units, { letterSpacing: `${p.tracking}em` });
      tl.to(units, { letterSpacing: '0em', duration: d * 0.55, ease: ctx.ease('out') }, d * 0.15);
    }
    const em = parts(ctx, 'em');
    if (p.emStyle === 'color') {
      ctx.initial(em, { color: colorOf(ctx, 'fg') });
      tl.to(
        em,
        { color: colorOf(ctx, 'accent'), duration: d * (1 - p.emDelay), ease: ctx.ease('out') },
        d * p.emDelay,
      );
    } else {
      em.forEach((node, index) => {
        const rect = ctx.beat.anchor('em', index).rect;
        const underline = document.createElement('i');
        Object.assign(underline.style, {
          position: 'absolute',
          left: `${rect.x}px`,
          top: `${rect.y + rect.h}px`,
          width: `${rect.w}px`,
          height: '0.08em',
          background: colorOf(ctx, 'accent'),
          transformOrigin: 'left center',
        });
        ctx.overlay.append(underline);
        ctx.initial(underline, { scaleX: 0 });
        tl.to(underline, { scaleX: 1, duration: d * (1 - p.emDelay), ease: ctx.ease('out') }, d * p.emDelay);
      });
    }
    if (p.rule) {
      const rect = ctx.beat.anchor('block').rect,
        svg = svgLayer(ctx);
      const rule = line(svg, rect.x, rect.y, rect.x + rect.w, rect.y, {
        stroke: colorOf(ctx, 'rule'),
        'stroke-width': 2,
      });
      ctx.initial(rule, { scaleX: 0, transformOrigin: 'left center' });
      tl.to(rule, { scaleX: 1, duration: d * 0.25, ease: ctx.ease('out') }, 0);
    }
    if (isQuote)
      parts(ctx, 'by').forEach((node) => {
        ctx.initial(node, { autoAlpha: 0 });
        tl.to(node, { autoAlpha: 1, duration: d * 0.3, ease: ctx.ease('out') }, d * 0.7);
      });
  },
};
