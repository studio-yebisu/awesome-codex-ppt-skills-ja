/** A text mask dives into one stroke before releasing the media full frame. */
import { applyTextMask, clearMask } from '../_shared/mask.js';
import { driveValue } from '../_shared/drive.js';
import { seg } from '../_shared/timeline.js';

export default {
  id: 'text-mask-dive',
  family: 'media',
  role: 'step',
  accepts: ['video', 'photo'],
  sources: ['text-cutout-zoom', 'giant-mask-reveal', 'text-window-fill'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.4, min: 0.8, max: 3, doc: '전체 길이(u)' },
    focusX: { type: 'number', default: 0.36, min: 0, max: 1, doc: 'focusX(안무 설명의 같은 이름)' },
    focusY: { type: 'number', default: 0.5, min: 0, max: 1, doc: 'focusY(안무 설명의 같은 이름)' },
    maxZoom: { type: 'number', default: 40, min: 8, max: 80, doc: 'maxZoom(안무 설명의 같은 이름)' },
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const media = ctx.beat.part('media').filter((n) => !ctx.skipNodes?.includes(n));
    const caption = ctx.beat.part('caption').filter((n) => !ctx.skipParts.includes('caption'));
    const text = ctx.beat.data.mask?.text ?? media[0]?.dataset.maskText ?? 'MASK';
    const rect = ctx.beat.anchor('media').rect;
    const pos = `${params.focusX * 100}% ${params.focusY * 100}%`;
    for (const node of media) {
      applyTextMask(ctx, node, text, { rect });
      ctx.initial(node, { filter: 'brightness(1.3)' });
      if (!ctx.reduce) {
        // 배율은 로그 공간에서 보간해 「빨려 들어가는」 속도가 일정하게 가속한다. 크기·위치를 매 render마다
        // 같이 써야 앞 move(mask-word-in)가 남긴 위치가 덮이지 않고, seek으로 뛰어도 같은 화면이 나온다.
        const ln = Math.log(params.maxZoom);
        const at = `${params.focusX * 100}% ${params.focusY * 100}%`;
        driveValue(
          tl,
          (k) => {
            const pct = Math.exp(ln * k) * 100;
            node.style.maskSize = node.style.webkitMaskSize = `${pct}% ${pct}%`;
            node.style.maskPosition = node.style.webkitMaskPosition = at;
          },
          {
            from: 0,
            to: 1,
            at: params.duration * 0.1,
            duration: params.duration * 0.72,
            ease: 'sine.in',
          },
        );
      }
      clearMask(tl, node, params.duration * 0.88);
      tl.to(node, { filter: 'brightness(1)', ...seg(params.duration, 0.8, 0.88), ease: ctx.ease('out') }, 0);
    }
    ctx.initial(caption, { autoAlpha: 0, yPercent: 40 });
    tl.to(caption, { autoAlpha: 1, yPercent: 0, ...seg(params.duration, 0.85, 1), ease: ctx.ease('out') }, 0);
  },
};
