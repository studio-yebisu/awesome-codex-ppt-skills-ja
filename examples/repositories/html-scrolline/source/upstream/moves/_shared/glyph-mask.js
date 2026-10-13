/** Canvas glyph masks in the stage display font (kinetic word masks).
 * Draw `text` (or only chars [from, to)) as a white glyph mask the size of `rect`, in the stage's
 * display font. Glyph height = rect.h × scale, width capped at rect.w × 0.92, ink box centred at
 * (0.5, cy). Returns null where canvas text is unavailable (jsdom). `split` gives the x of the
 * boundary between char `split − 1` and `split`, so a word can be cut into doors.
 */
export function glyphMask(ctx, text, rect, { scale = 0.78, cy = 0.5, from = 0, to, split } = {}) {
  const canvas = globalThis.document?.createElement?.('canvas');
  const g = canvas?.getContext?.('2d');
  if (!g || typeof g.measureText !== 'function' || !rect.w || !rect.h) return null;
  const style = globalThis.getComputedStyle?.(ctx.stage.root);
  const family = style?.getPropertyValue('--sl-font-display').trim() || 'sans-serif';
  const weight = ctx.tokens?.maskWeight ?? 900;
  const chars = [...text];
  const probe = 200;
  g.font = `${weight} ${probe}px ${family}`;
  const m = g.measureText(text);
  const inkH = (m.actualBoundingBoxAscent ?? probe * 0.72) + (m.actualBoundingBoxDescent ?? 0);
  const inkW = (m.actualBoundingBoxLeft ?? 0) + (m.actualBoundingBoxRight ?? m.width);
  if (!(inkH > 0) || !(inkW > 0)) return null;
  const size = probe * Math.min((rect.h * scale) / inkH, (rect.w * 0.92) / inkW);
  canvas.width = Math.round(rect.w);
  canvas.height = Math.round(rect.h);
  g.font = `${weight} ${size}px ${family}`;
  const k = size / probe;
  const left = (rect.w - inkW * k) / 2 + (m.actualBoundingBoxLeft ?? 0) * k;
  const base = rect.h * cy - (inkH * k) / 2 + (m.actualBoundingBoxAscent ?? probe * 0.72) * k;
  const prefix = (n) => (n > 0 ? g.measureText(chars.slice(0, n).join('')).width : 0);
  const end = to ?? chars.length;
  g.fillStyle = '#fff';
  g.textBaseline = 'alphabetic';
  g.fillText(chars.slice(from, end).join(''), left + prefix(from), base);
  return {
    url: canvas.toDataURL('image/png'),
    splitX: split === undefined ? undefined : left + prefix(split),
    box: {
      x: left - (m.actualBoundingBoxLeft ?? 0) * k,
      y: base - (m.actualBoundingBoxAscent ?? 0) * k,
      w: inkW * k,
      h: inkH * k,
    },
  };
}
