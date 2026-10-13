/** Pure grid placement plus canvas overlay drawing. */
export function gridLayout({
  n,
  cols,
  cell,
  gap = 0,
  origin = { x: 0, y: 0 },
  order = 'row',
  from = origin,
}) {
  const cells = Array.apply(null, { length: n }).map((_, i) => ({
    x: origin.x + (i % cols) * (cell + gap),
    y: origin.y + Math.floor(i / cols) * (cell + gap),
    i,
  }));
  return order === 'near'
    ? cells.sort((a, b) => Math.hypot(a.x - from.x, a.y - from.y) - Math.hypot(b.x - from.x, b.y - from.y))
    : cells;
}
export function canvasLayer(ctx) {
  const canvas = document.createElement('canvas');
  canvas.width = ctx.viewport.w * ctx.viewport.dpr;
  canvas.height = ctx.viewport.h * ctx.viewport.dpr;
  Object.assign(canvas.style, {
    position: 'absolute',
    inset: '0',
    width: `${ctx.viewport.w}px`,
    height: `${ctx.viewport.h}px`,
  });
  ctx.overlay.append(canvas);
  return { canvas, g: canvas.getContext?.('2d') ?? null };
}
export function drawDots(layer, dots, { r, color }) {
  if (!layer.g) return;
  layer.g.fillStyle = color;
  dots.forEach(({ x, y }) => {
    layer.g.beginPath();
    layer.g.arc(x, y, r, 0, Math.PI * 2);
    layer.g.fill();
  });
}
