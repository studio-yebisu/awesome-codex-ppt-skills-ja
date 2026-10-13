/** Words converge from a blurred, center-out spread. Kinetic only. */
export default {
  id: 'tracking-close',
  family: 'type',
  role: 'enter',
  accepts: ['text', 'quote'],
  sources: ['tracking-reveal', 'word-rise-fade'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.3, min: 0.6, max: 2.4, doc: '전체 길이(u)' },
    spread: { type: 'number', default: 0.6, min: 0.1, max: 1.2, doc: '벌림 거리' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    const mid = (words.length - 1) / 2;
    words.forEach((node, i) => {
      const at = Math.min(i * 0.1, p.duration * 0.3),
        filter = ctx.reduce ? 'none' : 'blur(4px)';
      ctx.initial(node, { x: `${(i - mid) * p.spread}em`, autoAlpha: 0, filter });
      tl.to(
        node,
        {
          x: 0,
          autoAlpha: 1,
          filter: ctx.reduce ? 'none' : 'blur(0px)',
          duration: p.duration * 0.7,
          ease: ctx.ease('out'),
        },
        at,
      );
      tl.set(node, { filter: 'none' }, at + p.duration * 0.7);
    });
  },
};
