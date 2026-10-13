/** Relay words leftward until the line has accelerated out of the viewport. */
export default {
  id: 'sweep-out',
  family: 'type',
  role: 'exit',
  accepts: ['text', 'number'],
  sources: ['word-relay', 'motion-blur', 'overlapping-action'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 0.9, min: 0.4, max: 1.6, doc: '전체 길이(u)' },
    lag: { type: 'number', default: 0.03, min: 0, max: 0.08, doc: '어절 간 출발 시차(u)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const words = ctx.skipParts.includes('word') ? [] : ctx.beat.part('word');
    const nodes = words.length
      ? words
      : ctx.beat.part('digits').length
        ? ctx.beat.part('digits')
        : ctx.beat.part('block');
    nodes
      .filter((node) => !(ctx.skipNodes ?? []).includes(node))
      .forEach((node, index) => {
        const at = index * p.lag,
          duration = Math.max(0, Math.min(p.duration * 0.9, p.duration - at));
        ctx.initial(node, { x: 0, autoAlpha: 1 });
        tl.to(node, { x: -ctx.viewport.w * 1.2, duration, ease: ctx.ease('in') }, at);
        tl.to(node, { autoAlpha: 0, duration: duration * 0.4, ease: ctx.ease('in') }, at + duration * 0.6);
      });
  },
};
