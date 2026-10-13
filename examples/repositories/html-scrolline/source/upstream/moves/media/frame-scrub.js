/** Makes a scrub-video's image sequence a reversible scroll time axis. */
import { frameSeqOf, scrubTo } from '../_shared/media.js';

export default {
  id: 'frame-scrub',
  family: 'media',
  role: 'step',
  accepts: ['video'],
  sources: ['frame-scrub', 'scroll-frame-scrub', 'scroll-scrub-cinema'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.4, min: 0.8, max: 5, doc: '전체 길이(u)' },
    from: { type: 'number', default: 0, min: 0, max: 1, doc: '시작 진행률' },
    to: { type: 'number', default: 1, min: 0, max: 1, doc: '끝 진행률' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    scrubTo(tl, frameSeqOf(ctx.beat), { from: params.from, to: params.to, at: 0, duration: params.duration });
  },
};
