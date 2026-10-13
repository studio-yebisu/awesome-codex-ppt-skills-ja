/** Grows an already-open media window until it covers its map tile (the screen at the stop). */
import { seg } from '../_shared/timeline.js';

/** Scale and offset that make the frame cover its beat tile (layout box, transforms ignored). */
function coverOf(frame, viewport) {
  const w = frame?.offsetWidth || 0,
    h = frame?.offsetHeight || 0;
  if (!w || !h) return { x: 0, y: 0, scale: 1 };
  const cx = frame.offsetLeft + w / 2,
    cy = frame.offsetTop + h / 2;
  return {
    x: viewport.w / 2 - cx,
    y: viewport.h / 2 - cy,
    scale: Math.max(viewport.w / w, viewport.h / h) * 1.01,
  };
}

export default {
  id: 'window-takeover',
  family: 'media',
  role: 'step',
  accepts: ['video', 'photo'],
  sources: ['inline-image-expand', 'scroll-grid-expand'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.5, max: 2.4, doc: '전체 길이(u)' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const [frame] = ctx.beat.part('frame');
    const media = ctx.beat.part('media');
    if (!frame) return;
    const cover = coverOf(frame, ctx.viewport);
    tl.fromTo(
      frame,
      { x: 0, y: 0, scale: 1, transformOrigin: '50% 50%' },
      { ...cover, transformOrigin: '50% 50%', ...seg(params.duration, 0, 0.8), ease: ctx.ease('inout'), immediateRender: false },
      0,
    );
    tl.fromTo(
      media,
      { scale: 1 },
      { scale: 1.04, ...seg(params.duration, 0.2, 1), ease: ctx.ease('out'), immediateRender: false },
      0,
    );
  },
};
