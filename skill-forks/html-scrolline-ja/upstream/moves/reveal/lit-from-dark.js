/** Sweeps a rim-light over launch media before its caption arrives. Signature: launch. */
import { clearMask } from '../_shared/mask.js';
import { frameSeqOf, scrubTo } from '../_shared/media.js';
import { px } from '../_shared/timeline.js';

const usable = (ctx, name) =>
  ctx.skipParts.includes(name) ? [] : ctx.beat.part(name).filter((node) => !ctx.skipNodes?.includes(node));

export default {
  id: 'lit-from-dark',
  family: 'reveal',
  role: 'enter',
  accepts: ['photo', 'video'],
  sources: ['lamp-cone-reveal', 'light-sweep', 'blur-resolve'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.6, min: 0.8, max: 3, doc: '전체 길이(u)' },
    scrubTo: { type: 'number', default: 0, min: 0, max: 1, doc: 'scrubTo(안무 설명의 같은 이름)' },
    rimFromX: { type: 'number', default: -0.2, min: -0.5, max: 0.5, doc: 'rimFromX(안무 설명의 같은 이름)' },
    rimFromY: { type: 'number', default: -0.1, min: -0.5, max: 0.5, doc: 'rimFromY(안무 설명의 같은 이름)' },
    darkFloor: { type: 'number', default: 0.04, min: 0, max: 0.3, doc: 'darkFloor(안무 설명의 같은 이름)' },
    scaleFrom: { type: 'number', default: 1.06, min: 1, max: 1.2, doc: '시작 scale' },
    captionRise: { type: 'number', default: 36, min: 0, max: 120, doc: 'captionRise(안무 설명의 같은 이름)' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration;
    // 빛은 제품(media)에만: frame에 걸면 caption까지 마스크·밝기를 같이 받아 정지점에서 회색으로 남는다
    const media = usable(ctx, 'media');
    const frame = media.length ? media : usable(ctx, 'frame');
    const captions = usable(ctx, 'caption');
    if (ctx.reduce) {
      ctx.initial([...frame, ...captions], { autoAlpha: 0 });
      tl.to(frame, { autoAlpha: 1, duration: d, ease: ctx.ease('out') }, 0);
      tl.to(captions, { autoAlpha: 1, duration: d * 0.35, ease: ctx.ease('out') }, d * 0.65);
      return;
    }
    const fromX = `${params.rimFromX * 100}%`;
    const fromY = `${params.rimFromY * 100}%`;
    const mask = `radial-gradient(circle at ${fromX} ${fromY}, #000 20%, transparent 100%)`;
    ctx.initial(frame, {
      filter: `brightness(${params.darkFloor})`,
      scale: params.scaleFrom,
      y: '2%',
      maskImage: mask,
      webkitMaskImage: mask,
      maskRepeat: 'no-repeat',
      maskPosition: `${fromX} ${fromY}`,
      maskSize: '20% 20%',
    });
    ctx.initial(captions, { autoAlpha: 0, y: px(ctx, params.captionRise), clipPath: 'inset(0)' });
    tl.to(
      frame,
      {
        filter: 'brightness(1)',
        maskPosition: '50% 50%',
        maskSize: '700% 700%',
        duration: d * 0.55,
        ease: ctx.ease('out'),
      },
      d * 0.1,
    );
    tl.to(frame, { scale: 1, y: 0, duration: d * 0.5, ease: ctx.ease('out') }, d * 0.25);
    const seq = frameSeqOf(ctx.beat);
    if (ctx.beat.type === 'video')
      scrubTo(tl, seq, { from: 0, to: params.scrubTo, at: d * 0.1, duration: d * 0.8 });
    captions.forEach((caption, index) => {
      const at = Math.min(d * (0.65 + index * 0.08), d * 0.9);
      tl.to(caption, { autoAlpha: 1, y: 0, duration: Math.max(0, d - at), ease: ctx.ease('out') }, at);
    });
    tl.set(frame, { filter: 'none' }, d);
    clearMask(tl, frame, d);
  },
};
