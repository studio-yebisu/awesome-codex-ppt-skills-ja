export const SLIDE = { w: 13.333, h: 7.5 };
export const GRID = { marginX: 0.72, marginY: 0.56, gutter: 0.18, columns: 12 };
export const colW = (SLIDE.w - GRID.marginX * 2 - GRID.gutter * (GRID.columns - 1)) / GRID.columns;

export function col(n, span = 1) {
  const x = GRID.marginX + (n - 1) * (colW + GRID.gutter);
  const w = colW * span + GRID.gutter * (span - 1);
  return { x, w };
}

export function box(c, span, y, h) {
  const g = col(c, span);
  return { x: g.x, y, w: g.w, h };
}

export const axes = {
  title: { x: GRID.marginX, y: 0.48, w: 9.8, h: 0.64 },
  bodyTop: 1.34,
  footer: { x: GRID.marginX, y: 7.04, w: SLIDE.w - GRID.marginX * 2, h: 0.22 },
};

export function clampTextHeight(lines, fontSize, lineHeight = 1.28, min = 0.36) {
  return Math.max(min, (lines * fontSize * lineHeight) / 72);
}
