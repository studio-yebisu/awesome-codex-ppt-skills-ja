/** Timeline arithmetic shared by W3 moves. */
export const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
export const lerp = (a, b, t) => a + (b - a) * t;
/**
 * Segment [a, b] of a d-long move. Spread into tween vars (`tl.to(x, { ...seg(d, a, b) }, 0)`) it gives
 * `delay` + `duration`, so the tween starts at d·a; `.at` (not enumerable, not spread) is the same start for
 * `tl.to(x, { duration: s.duration }, s.at)`. It used to spread `at`, which GSAP ignores, so every segment began at 0.
 */
export const seg = (d, a, b) =>
  Object.defineProperty({ delay: d * a, duration: d * b - d * a }, 'at', { value: d * a, enumerable: false });
export const px = (ctx, n) => n * ctx.viewport.px;
export function slots(n, { start = 0, span, each, compress = 1, minRatio = 0.4 }) {
  if (!n) return [];
  const base = each ?? (n > 1 ? span / (n - 1) : (span ?? 0));
  const ratios = Array.apply(null, { length: Math.max(0, n - 1) }).map((_, i) =>
    Math.max(minRatio, compress ** i),
  );
  const total = ratios.reduce((sum, ratio) => sum + ratio, 0) || 1;
  const scale = each === undefined && span !== undefined ? span / total : base;
  let at = start;
  return Array.apply(null, { length: n }).map((_, i) => {
    const value = { at, duration: base };
    at += (ratios[i] ?? 0) * scale;
    return value;
  });
}
