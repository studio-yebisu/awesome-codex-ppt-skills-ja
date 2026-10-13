/** Defocuses a beat on its way out, by word or by whole block. */
import { wordsIn } from '../_shared/words.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((node) => !ctx.skipNodes?.includes(node));

export default {
  id: 'blur-drop',
  family: 'reveal',
  role: 'exit',
  accepts: ['*'],
  sources: ['blur-dissolve', 'word-rise-fade', 'rack-focus'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.8, min: 0.4, max: 1.6, doc: '전체 길이(u)' },
    blur: { type: 'number', default: 4, min: 0, max: 12, doc: '끝 blur(px), tokens.blurMax 상한' },
    drop: { type: 'number', default: 0.25, min: 0, max: 0.5, doc: '어절 하강량(em)' },
    unit: { type: 'enum', default: 'word', values: ['word', 'block'], doc: '퇴장 단위' },
    scaleTo: { type: 'number', default: 1, min: 0.94, max: 1, doc: '블록 끝 scale' },
    emLast: { type: 'number', default: 0, min: 0, max: 0.2, doc: 'em이 늦게 사라지는 지연(u)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    const blur = Math.min(params.blur, ctx.tokens.blurMax ?? 12);
    const words = wordsIn(ctx.beat, 'block').filter((node) => !ctx.skipNodes?.includes(node));
    const useWords = params.unit === 'word' && words.length > 0 && !ctx.skipParts.includes('word');
    if (ctx.reduce) {
      const nodes = useWords ? words : usable(ctx, ctx.beat.primary);
      tl.to(nodes, { autoAlpha: 0, duration: d, ease: ctx.ease('in') }, 0);
      return;
    }
    if (useWords) {
      [...words].reverse().forEach((node, index) => {
        const at = Math.min(index * 0.03, d * 0.4);
        const duration = Math.max(0, d * 0.85 - at);
        tl.to(
          node,
          { y: `${params.drop}em`, filter: `blur(${blur}px)`, autoAlpha: 0, duration, ease: ctx.ease('in') },
          at,
        );
        tl.set(node, { filter: 'none', transform: 'none' }, d);
      });
      return;
    }
    const primary = usable(ctx, ctx.beat.primary);
    const em = usable(ctx, 'em');
    tl.to(
      primary,
      { scale: params.scaleTo, filter: `blur(${blur}px)`, duration: d * 0.6, ease: ctx.ease('in') },
      0,
    );
    tl.to(primary, { autoAlpha: 0, duration: d * 0.8, ease: ctx.ease('in') }, d * 0.2);
    if (em.length)
      tl.to(
        em,
        { autoAlpha: 0, duration: Math.max(0, d * 0.8 - params.emLast), ease: ctx.ease('in') },
        d * 0.2 + params.emLast,
      );
    tl.set(primary, { filter: 'none', transform: 'none' }, d);
  },
};
