/** Opens a line or rounded media window. Shared by canvas and launch. */
import { partFree } from '../_shared/skip.js';
import { seg } from '../_shared/timeline.js';

const clipLine = (width) => `inset(50% ${50 - width * 50}% 50% ${50 - width * 50}%)`;
const clipBox = (inset, radius) => `inset(${inset}% ${inset}% ${inset}% ${inset}% round ${radius}px)`;
export default {
  id: 'window-open',
  family: 'media',
  role: 'enter',
  accepts: ['video', 'photo'],
  sources: [
    'iris-mask',
    'clip-reveal',
    'mask-reveal',
    'screen-emergence',
    'inline-image-expand',
    'window-expand',
  ],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.6, max: 3, doc: '전체 길이(u)' },
    shape: { type: 'enum', default: 'line', values: ['line', 'box'], doc: '창 시작 모양' },
    lineWidth: { type: 'number', default: 0.4, min: 0.1, max: 1, doc: 'line 시작 선 폭 비율' },
    startInset: { type: 'number', default: 30, min: 10, max: 45, doc: 'box 시작 inset(%)' },
    radius: { type: 'number', default: 28, min: 0, max: 80, doc: 'box 시작 모서리(px)' },
    mediaScale: { type: 'number', default: 1.12, min: 1, max: 1.3, doc: 'media 시작 scale' },
    scrim: { type: 'boolean', default: false, doc: 'caption 뒤 scrim' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const frame = partFree(ctx, 'frame');
    const media = partFree(ctx, 'media');
    const caption = partFree(ctx, 'caption');
    const start =
      params.shape === 'line' ? clipLine(params.lineWidth) : clipBox(params.startInset, params.radius);
    ctx.initial(frame, { clipPath: start, autoAlpha: params.shape === 'box' ? 0 : 1 });
    ctx.initial(media, { scale: params.mediaScale });
    ctx.initial(caption, { autoAlpha: 0, y: 12 });
    if (params.shape === 'line') {
      tl.to(
        frame,
        { clipPath: 'inset(50% 0% 50% 0%)', ...seg(params.duration, 0, 0.3), ease: ctx.ease('out') },
        0,
      );
      tl.to(
        frame,
        { clipPath: 'inset(0% 0% 0% 0%)', ...seg(params.duration, 0.3, 0.75), ease: ctx.ease('inout') },
        0,
      );
    } else {
      tl.to(frame, { autoAlpha: 1, ...seg(params.duration, 0, 0.2), ease: ctx.ease('out') }, 0);
      tl.to(
        frame,
        {
          clipPath: 'inset(0% 0% 0% 0% round 0px)',
          ...seg(params.duration, 0.15, 0.8),
          ease: ctx.ease('inout'),
        },
        0,
      );
    }
    tl.to(media, { scale: 1, ...seg(params.duration, 0.15, 0.8), ease: ctx.ease('inout') }, 0);
    tl.to(caption, { autoAlpha: 1, y: 0, ...seg(params.duration, 0.75, 1), ease: ctx.ease('out') }, 0);
    if (params.scrim && caption.length) {
      const s = document.createElement('div');
      s.className = 'sl-media-scrim';
      ctx.overlay.append(s);
      ctx.initial(s, { autoAlpha: 0 });
      tl.to(s, { autoAlpha: 1, ...seg(params.duration, 0.75, 1) }, 0);
    }
  },
};
