/** A linear, non-looping final-scene push on media only. */

export default {
  id: 'slow-push',
  family: 'media',
  role: 'ambient',
  accepts: ['photo', 'video'],
  sources: ['push-in', 'ken-burns'],
  reduce: 'fade',
  params: {
    pushScale: { type: 'number', default: 1.05, min: 1, max: 1.15, doc: '끝 media scale' },
    focusX: { type: 'number', default: 0.5, min: 0, max: 1, doc: 'focus X 비율' },
    focusY: { type: 'number', default: 0.45, min: 0, max: 1, doc: 'focus Y 비율' },
  },
  timing() {
    return { duration: 'fill', stops: [] };
  },
  build(tl, ctx, params) {
    const media = ctx.beat
      .part('media')
      .filter((node) => !ctx.skipParts.includes('media') && !ctx.skipNodes?.includes(node));
    ctx.initial(media, { scale: 1, transformOrigin: `${params.focusX * 100}% ${params.focusY * 100}%` });
    tl.to(media, { scale: params.pushScale, duration: ctx.duration, ease: 'none' }, 0);
  },
};
