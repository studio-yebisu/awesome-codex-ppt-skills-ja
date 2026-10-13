/**
 * Glyphs rise from below their baseline and close by transform, never letter spacing.
 * On a masked video/photo the word itself is the window: a canvas-drawn glyph mask (display font,
 * mask weight, frame-height fit) rises into place while the footage brightens inside the strokes.
 */
import { glyphMask } from '../_shared/glyph-mask.js';
import { applyTextMask } from '../_shared/mask.js';

export default {
  id: 'glyph-rise',
  family: 'type',
  role: 'enter',
  accepts: ['text', 'video', 'photo'],
  sources: ['mask-reveal', 'tracking-reveal', 'char-stagger'],
  reduce: 'fade',
  params: {
    duration: { type: 'number', default: 1.2, min: 0.6, max: 2.4, doc: '전체 길이(u)' },
    stagger: { type: 'number', default: 0.08, min: 0.02, max: 0.2, doc: '항목 간 시차(u)' },
    spread: { type: 'number', default: 0.12, min: 0, max: 0.2, doc: '벌림 거리' },
    maskScale: { type: 'number', default: 0.78, min: 0.4, max: 0.95, doc: '마스크 글자 높이 / 프레임 높이' },
    maskY: { type: 'number', default: 0.5, min: 0.3, max: 0.7, doc: '마스크 글자 세로 중심(프레임 비율)' },
  },
  timing: (p) => ({ duration: p.duration, stops: [] }),
  build(tl, ctx, p) {
    const chars = ctx.skipParts.includes('char') ? [] : ctx.beat.part('char');
    const mid = (chars.length - 1) / 2;
    chars.forEach((node, i) => {
      const at = Math.min(i * p.stagger, p.duration * 0.2);
      ctx.initial(node, {
        yPercent: 100,
        x: `${(i - mid) * p.spread}em`,
        autoAlpha: 0,
        clipPath: 'inset(0)',
      });
      tl.to(node, { yPercent: 0, autoAlpha: 1, duration: p.duration * 0.6, ease: ctx.ease('out') }, at);
      tl.to(
        node,
        { x: 0, duration: p.duration * 0.5, ease: ctx.ease('out') },
        Math.min(p.duration * 0.3 + at, p.duration * 0.5),
      );
    });
    const labels = ['caption', 'label'].flatMap((name) =>
      ctx.skipParts.includes(name) ? [] : ctx.beat.part(name),
    );
    ctx.initial(labels, { autoAlpha: 0, y: 0 });
    tl.to(labels, { autoAlpha: 1, duration: p.duration * 0.3, ease: ctx.ease('out') }, p.duration * 0.7);
    const media = ctx.beat.part('media').filter((node) => !ctx.skipNodes?.includes(node));
    if (chars.length || !media.length) return;
    const rect = ctx.beat.anchor('media').rect;
    const text = ctx.beat.data.mask?.text ?? media[0].dataset.maskText ?? ctx.beat.data.text ?? '';
    const mask = glyphMask(ctx, text, rect, { scale: p.maskScale, cy: p.maskY });
    const rise = Math.round(rect.h * 0.18);
    for (const node of media) {
      if (mask) {
        const value = `url("${mask.url}")`;
        ctx.initial(node, {
          maskImage: value,
          webkitMaskImage: value,
          maskSize: '100% 100%',
          webkitMaskSize: '100% 100%',
          maskRepeat: 'no-repeat',
          webkitMaskRepeat: 'no-repeat',
        });
      } else applyTextMask(ctx, node, text, { rect });
      ctx.initial(node, {
        autoAlpha: 0,
        maskPosition: `0px ${rise}px`,
        webkitMaskPosition: `0px ${rise}px`,
        scale: 1.06,
        filter: 'brightness(0.35)',
      });
      tl.to(
        node,
        {
          autoAlpha: 1,
          maskPosition: '0px 0px',
          webkitMaskPosition: '0px 0px',
          duration: p.duration * 0.6,
          ease: ctx.ease('out'),
        },
        0,
      );
      tl.to(
        node,
        { scale: 1, filter: 'brightness(1)', duration: p.duration * 0.9, ease: ctx.ease('out') },
        0,
      );
    }
  },
};
