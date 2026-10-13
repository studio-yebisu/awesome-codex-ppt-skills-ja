/** Scroll-bound frame-sequence reveal with optional internal stops. */
import { frameSeqOf, scrubTo } from '../_shared/media.js';

export default {
  id: 'video-scrub',
  family: 'media',
  role: 'enter',
  accepts: ['video'],
  sources: ['scroll-frame-scrub', 'frame-scrub', 'scroll-scrub'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 3.2, min: 1, max: 8, doc: '전체 길이(u)' },
    stops: { type: 'array', default: [], doc: '내부 정지점({name, at})' },
  },
  timing(params) {
    return {
      duration: params.duration,
      stops: params.stops.map((stop) => ({ name: stop.name, at: stop.at * params.duration })),
    };
  },
  build(tl, ctx, params) {
    const caption = ctx.beat
      .part('caption')
      .filter((node) => !ctx.skipParts.includes('caption') && !ctx.skipNodes?.includes(node));
    const seq = frameSeqOf(ctx.beat);
    ctx.initial(caption, { autoAlpha: 0 });
    if (caption.length)
      tl.to(caption, { autoAlpha: 1, duration: params.duration * 0.1, ease: ctx.ease('out') }, 0);
    scrubTo(tl, seq, { from: 0, to: 1, at: 0, duration: params.duration });
  },
};
