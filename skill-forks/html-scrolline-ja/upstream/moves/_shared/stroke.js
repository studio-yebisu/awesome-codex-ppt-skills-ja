/** SVG stroke primitives using normalized dash lengths. */
const NS = 'http://www.w3.org/2000/svg';
function attrs(node, values) {
  for (const [key, value] of Object.entries(values)) node.setAttribute(key, String(value));
  return node;
}
export function svgLayer(ctx) {
  const svg = document.createElementNS(NS, 'svg');
  attrs(svg, { viewBox: `0 0 ${ctx.viewport.w} ${ctx.viewport.h}`, preserveAspectRatio: 'none' });
  Object.assign(svg.style, { position: 'absolute', inset: '0', overflow: 'visible', pointerEvents: 'none' });
  ctx.overlay.append(svg);
  return svg;
}
export function path(svg, d, extra = {}) {
  const node = document.createElementNS(NS, 'path');
  attrs(node, {
    d,
    pathLength: 1,
    fill: 'none',
    'stroke-dasharray': '1 1',
    'stroke-dashoffset': 1,
    ...extra,
  });
  svg.append(node);
  return node;
}
export const line = (svg, x1, y1, x2, y2, extra) => path(svg, `M ${x1} ${y1} L ${x2} ${y2}`, extra);
export const polyline = (svg, pts, extra) =>
  path(svg, pts.map((p, i) => `${i ? 'L' : 'M'} ${p.x} ${p.y}`).join(' '), extra);
export function drawOn(tl, node, { at, duration, from = 0, to = 1, ease }) {
  tl.fromTo(
    node,
    { strokeDashoffset: 1 - from },
    { strokeDashoffset: 1 - to, duration, ease: ease ?? 'none', immediateRender: false },
    at,
  );
}
export function pointOnPolyline(pts, t) {
  if (!pts.length) return { x: 0, y: 0 };
  if (pts.length === 1) return { ...pts[0] };
  const lengths = pts.slice(1).map((p, i) => Math.hypot(p.x - pts[i].x, p.y - pts[i].y));
  const total = lengths.reduce((a, b) => a + b, 0);
  let wanted = Math.max(0, Math.min(1, t)) * total;
  for (let i = 0; i < lengths.length; i += 1) {
    if (wanted <= lengths[i] || i === lengths.length - 1) {
      const q = lengths[i] ? wanted / lengths[i] : 0;
      return { x: pts[i].x + (pts[i + 1].x - pts[i].x) * q, y: pts[i].y + (pts[i + 1].y - pts[i].y) * q };
    }
    wanted -= lengths[i];
  }
  return { ...pts.at(-1) };
}
