/** Condenses a prompt transcript into its authored result lines. */
import { transferVars } from '../../engine/index.js';
import { colorOf } from '../_shared/color.js';
import { drawOn, line, svgLayer } from '../_shared/stroke.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name)
    ? []
    : ctx.beat.part(name).filter((node) => !(ctx.skipNodes ?? []).includes(node));

export default {
  id: 'transcript-condense',
  family: 'assemble',
  role: 'step',
  accepts: ['prompt'],
  sources: ['aggregate-split-merge', 'token-split', 'highlight-sweep'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.6, max: 2.5, doc: '전체 길이(u)' },
    underline: { type: 'boolean', default: true, doc: 'underline(안무 설명의 같은 이름)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const fields = usable(ctx, 'field');
    const results = usable(ctx, 'result');
    const words = usable(ctx, 'word');
    const field = fields[0];
    const result = results[0];
    const accent = colorOf(ctx, 'accent');
    if (params.underline && field) {
      const rect = ctx.beat.anchor('field').rect;
      const svg = svgLayer(ctx);
      const underline = line(svg, rect.x, rect.y + rect.h, rect.x + rect.w, rect.y + rect.h, {
        stroke: accent,
        'stroke-width': 2,
      });
      drawOn(tl, underline, { at: 0, duration: d * 0.15, ease: ctx.ease('out') });
      // 밑줄은 응축의 출발 신호일 뿐: 대화가 접히면 같이 사라져 결과 두 줄만 남긴다
      ctx.initial(underline, { autoAlpha: 1 });
      tl.to(underline, { autoAlpha: 0, duration: d * 0.1, ease: ctx.ease('in') }, d * 0.5);
    }
    ctx.initial(fields, { autoAlpha: 1, scaleY: 1, transformOrigin: 'center' });
    tl.to(fields, { autoAlpha: 0.2, scaleY: 0.04, duration: d * 0.4, ease: ctx.ease('in') }, d * 0.15);
    if (field && result) {
      const carrier = field.cloneNode(false);
      carrier.removeAttribute('data-part');
      Object.assign(carrier.style, {
        position: 'absolute',
        left: `${ctx.beat.anchor('field').rect.x}px`,
        top: `${ctx.beat.anchor('field').rect.y}px`,
        width: `${ctx.beat.anchor('field').rect.w}px`,
        height: '2px',
        background: accent,
      });
      ctx.overlay.append(carrier);
      ctx.initial(carrier, {
        autoAlpha: 0,
        x: 0,
        y: 0,
        scaleX: 1,
        scaleY: 1,
        transformOrigin: '0 0',
      });
      tl.to(carrier, { autoAlpha: 1, duration: d * 0.05, ease: ctx.ease('out') }, d * 0.5);
      tl.to(
        carrier,
        {
          ...transferVars(ctx.beat.anchor('field').rect, ctx.beat.anchor('result').rect),
          duration: d * 0.1,
          ease: ctx.ease('inout'),
        },
        d * 0.5,
      );
      tl.to(carrier, { autoAlpha: 0, duration: d * 0.05, ease: ctx.ease('in') }, d * 0.6);
    }
    ctx.initial(results, { autoAlpha: 0, scaleY: 0.04, transformOrigin: 'center' });
    ctx.initial(words, { autoAlpha: 0, scaleY: 0.04, transformOrigin: 'center' });
    tl.set(fields, { autoAlpha: 0 }, d * 0.6);
    tl.to(results, { autoAlpha: 1, scaleY: 1, duration: d * 0.4, ease: ctx.ease('out') }, d * 0.6);
    tl.to(words, { autoAlpha: 1, scaleY: 1, duration: d * 0.4, ease: ctx.ease('out') }, d * 0.6);
  },
};
