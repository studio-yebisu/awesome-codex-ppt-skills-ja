/** Rack-focuses text and data parts into their finished position. */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((node) => !ctx.skipNodes?.includes(node));

function targets(ctx) {
  if (ctx.beat.type === 'text' || ctx.beat.type === 'quote') return usable(ctx, 'word');
  if (ctx.beat.type === 'number') return usable(ctx, 'value');
  if (ctx.beat.type === 'compare') return usable(ctx, 'item');
  return [...usable(ctx, 'title'), ...usable(ctx, 'plot')];
}

export default {
  id: 'focus-pull',
  family: 'reveal',
  role: 'enter',
  accepts: ['text', 'quote', 'number', 'compare', 'chart'],
  sources: ['blur-resolve', 'rack-focus', 'blur-reveal', 'atmospheric-depth'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.1, min: 0.4, max: 2, doc: '전체 길이(u)' },
    stagger: { type: 'number', default: 0.05, min: 0, max: 0.15, doc: '대상 간 시차(u)' },
    blur: { type: 'number', default: 8, min: 0, max: 12, doc: '시작 blur(px), tokens.blurMax로 상한' },
    rise: { type: 'number', default: 10, min: 0, max: 24, doc: '시작 y(px×viewport.px)' },
    scaleFrom: { type: 'number', default: 1, min: 1, max: 1.15, doc: '시작 scale' },
    tracking: { type: 'number', default: 0.06, min: 0, max: 0.12, doc: '블록 시작 자간 가산(em)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const nodes = targets(ctx);
    if (ctx.reduce) {
      ctx.initial(nodes, { autoAlpha: 0 });
      tl.to(nodes, { autoAlpha: 1, duration: d, ease: ctx.ease('out') }, 0);
      return;
    }
    const blur = Math.min(params.blur, ctx.tokens.blurMax ?? 12);
    const span = d * 0.7;
    nodes.forEach((node, index) => {
      const at = Math.min(index * params.stagger, d * 0.45);
      const duration = Math.max(0, span - at);
      ctx.initial(node, {
        autoAlpha: 0,
        y: px(ctx, params.rise),
        scale: params.scaleFrom,
        filter: `blur(${blur}px)`,
      });
      tl.to(node, { autoAlpha: 1, y: 0, scale: 1, filter: 'blur(0px)', duration, ease: ctx.ease('out') }, at);
      tl.set(node, { filter: 'none', transform: 'none' }, at + duration);
    });
    const blocks = usable(ctx, 'block');
    if (params.tracking > 0 && blocks.length) {
      ctx.initial(blocks, { letterSpacing: `${params.tracking}em` });
      tl.to(blocks, { letterSpacing: '0em', duration: d * 0.7, ease: ctx.ease('out') }, d * 0.2);
    }
    const em = usable(ctx, 'em');
    if (em.length) {
      ctx.initial(em, { color: colorOf(ctx, 'fg') });
      tl.to(em, { color: colorOf(ctx, 'accent'), duration: d * 0.3, ease: ctx.ease('out') }, d * 0.7);
    }
  },
};
