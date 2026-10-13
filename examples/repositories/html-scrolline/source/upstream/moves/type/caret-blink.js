/** Place a deterministic, timeline-bound accent caret after a text unit. */
import { colorOf } from '../_shared/color.js';

export default {
  id: 'caret-blink',
  family: 'type',
  role: 'ambient',
  accepts: ['text', 'prompt'],
  sources: ['context-caret', 'typewriter'],
  reduce: 'self',
  params: {
    after: { type: 'integer', default: -1, doc: '커서를 둘 어절 index(−1 = 마지막)' },
    period: { type: 'number', default: 0.5, min: 0.2, max: 1.2, doc: '깜빡임 주기(u)' },
    part: { type: 'part', default: 'word', doc: '기준 part' },
  },
  timing: () => ({ duration: 'fill', stops: [] }),
  build(tl, ctx, p) {
    const nodes = ctx.skipParts.includes(p.part) ? [] : ctx.beat.part(p.part);
    if (!nodes.length) return;
    const index = p.after < 0 ? nodes.length - 1 : Math.min(nodes.length - 1, p.after);
    const rect = ctx.beat.anchor(p.part, index).rect,
      caret = document.createElement('i');
    caret.className = 'sl-caret-blink';
    Object.assign(caret.style, {
      position: 'absolute',
      left: `${rect.x + rect.w}px`,
      top: `${rect.y}px`,
      width: `${Math.max(3, rect.h * 0.04)}px`,
      height: `${rect.h * 0.78}px`,
      marginTop: `${rect.h * 0.13}px`,
      background: colorOf(ctx, 'accent'),
    });
    ctx.overlay.append(caret);
    ctx.initial(caret, { x: rect.h * 0.08, autoAlpha: 1 });
    if (!ctx.reduce)
      for (let at = p.period / 2; at < ctx.duration; at += p.period) {
        tl.set(caret, { autoAlpha: 0 }, at);
        tl.set(caret, { autoAlpha: 1 }, Math.min(ctx.duration, at + p.period / 2));
      }
  },
};
