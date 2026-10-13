/** A short declaration lands one word at a time without rebound. */
export default {
  id: 'word-slam',
  family: 'type',
  role: 'enter',
  accepts: ['text'],
  sources: ['kinetic-beats', 'kinetic-type-sweep', 'anticipation'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.6, max: 2.4, doc: '전체 길이(u)' },
    scaleFrom: { type: 'number', default: 1.4, min: 1.1, max: 2, doc: '시작 scale' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    const n = words.length,
      d = p.duration;
    if (n >= 5 && globalThis.process?.env?.NODE_ENV !== 'production')
      console.warn('word-slam is intended for four words or fewer');
    words.forEach((node, i) => {
      const at = n ? (i / n) * d * 0.8 : 0;
      ctx.initial(node, { autoAlpha: 0, scale: p.scaleFrom, y: '-0.08em' });
      tl.to(node, { autoAlpha: 1, duration: Math.min(0.02, d * 0.02), ease: ctx.ease('out') }, at);
      tl.to(node, { scale: 1, y: 0, duration: Math.min(0.16, d * 0.16), ease: ctx.ease('out') }, at);
    });
    const lines = ctx.skipParts.includes('line') ? [] : ctx.beat.part('line');
    lines.forEach((node) => {
      ctx.initial(node, { y: 2 });
      tl.to(node, { y: 0, duration: Math.min(0.12, d * 0.1), ease: ctx.ease('out') }, d * 0.8);
    });
  },
};
