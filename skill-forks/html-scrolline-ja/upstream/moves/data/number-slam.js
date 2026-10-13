/** Slams a final numeric value into focus with one optional clipped light sweep. */
import { colorOf } from '../_shared/color.js';
import { px } from '../_shared/timeline.js';

const part = (ctx, name) => (ctx.skipParts.includes(name) ? [] : ctx.beat.part(name));

export default {
  id: 'number-slam',
  family: 'data',
  role: 'enter',
  accepts: ['number'],
  sources: ['scale-pop', 'light-sweep', 'blur-resolve'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1, min: 0.5, max: 2, doc: '전체 길이(u)' },
    slamScale: { type: 'number', default: 1.6, min: 1.1, max: 2.4, doc: 'slamScale(안무 설명의 같은 이름)' },
    slamBlur: { type: 'number', default: 18, min: 0, max: 40, doc: 'slamBlur(안무 설명의 같은 이름)' },
    sweep: { type: 'boolean', default: true, doc: 'sweep(안무 설명의 같은 이름)' },
    sweepWidth: {
      type: 'number',
      default: 0.35,
      min: 0.1,
      max: 0.8,
      doc: 'sweepWidth(안무 설명의 같은 이름)',
    },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const digits = part(ctx, 'digits');
    digits.forEach((node, index) => {
      ctx.initial(node, {
        autoAlpha: 0,
        scale: ctx.reduce ? 1 : params.slamScale,
        filter: 'blur(' + (ctx.reduce ? 0 : params.slamBlur) + 'px)',
        letterSpacing: ctx.reduce ? '0em' : '0.08em',
      });
      tl.to(
        node,
        {
          autoAlpha: 1,
          scale: 1,
          filter: 'blur(0px)',
          letterSpacing: '0em',
          duration: d * 0.35,
          ease: ctx.ease('out'),
        },
        0,
      );
      tl.set(node, { filter: 'none', clearProps: 'transform,letterSpacing' }, d * 0.35);
      if (params.sweep && !ctx.reduce) {
        const rect = ctx.beat.anchor('digits', index).rect;
        const shine = document.createElement('span');
        // overlay는 숫자와 다른 상자라 글꼴을 상속하지 않는다: 계산된 글꼴을 그대로 옮겨야 빛 띠가 획 위에 겹친다
        const cs = globalThis.getComputedStyle?.(node);
        const accent = colorOf(ctx, 'accent');
        shine.className = 'sl-number-slam__sweep';
        shine.textContent = node.textContent;
        Object.assign(shine.style, {
          position: 'absolute',
          left: rect.x + 'px',
          top: rect.y + 'px',
          width: rect.w + 'px',
          height: rect.h + 'px',
          color: 'transparent',
          whiteSpace: 'nowrap',
          backgroundImage: `linear-gradient(90deg, transparent 0%, ${accent} 45%, ${colorOf(ctx, 'fg')} 50%, ${accent} 55%, transparent 100%)`,
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          backgroundSize: `${100 / params.sweepWidth}% 100%`,
          backgroundPosition: '-100% 0',
          pointerEvents: 'none',
          fontFamily: cs?.fontFamily || 'inherit',
          fontSize: cs?.fontSize || 'inherit',
          fontWeight: cs?.fontWeight || 'inherit',
          fontVariantNumeric: cs?.fontVariantNumeric || 'normal',
          letterSpacing: cs?.letterSpacing || 'normal',
          lineHeight: cs?.lineHeight || 'normal',
        });
        ctx.overlay.append(shine);
        ctx.initial(shine, { autoAlpha: 0 });
        tl.to(shine, { autoAlpha: 1, duration: d * 0.02 }, d * 0.35);
        tl.to(shine, { backgroundPosition: '200% 0', duration: d * 0.3, ease: 'none' }, d * 0.35);
        tl.to(shine, { autoAlpha: 0, duration: d * 0.02 }, d * 0.65);
      }
    });
    const units = part(ctx, 'unit');
    ctx.initial(units, { autoAlpha: 0, x: ctx.reduce ? 0 : px(ctx, 24) });
    tl.to(units, { autoAlpha: 1, x: 0, duration: d * 0.35, ease: ctx.ease('out') }, d * 0.45);
    part(ctx, 'label').forEach((node, i) => {
      ctx.initial(node, { autoAlpha: 0, y: ctx.reduce ? 0 : px(ctx, 10) });
      tl.to(node, { autoAlpha: 1, y: 0, duration: d * 0.35, ease: ctx.ease('out') }, d * 0.65 + i * 0.04);
    });
    const source = part(ctx, 'source');
    ctx.initial(source, { autoAlpha: 0 });
    tl.to(source, { autoAlpha: 1, duration: d * 0.1, ease: ctx.ease('out') }, d * 0.9);
  },
};
