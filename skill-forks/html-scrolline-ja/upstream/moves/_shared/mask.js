/** Text-mask setup, isolated behind the v2 context API. */
import { textMask } from '../../engine/index.js';
export function applyTextMask(ctx, node, text, { rect, align, font } = {}) {
  const url =
    ctx.textMask?.(text, { rect, align }) ??
    textMask(text, { font: font ?? '900 160px sans-serif', width: rect.w, height: rect.h, align });
  const value = `url("${url}")`;
  ctx.initial(node, {
    maskImage: value,
    webkitMaskImage: value,
    maskSize: '100% 100%',
    maskRepeat: 'no-repeat',
    maskPosition: '50% 50%',
  });
}
export const clearMask = (tl, node, at) => tl.set(node, { maskImage: 'none', webkitMaskImage: 'none' }, at);
