import { addText, addParagraph } from "./typography.mjs";

export function footer(slide, idx, total, style) {
  slide.addText(`${String(idx).padStart(2, "0")} / ${String(total).padStart(2, "0")}`, {
    x: 11.55,
    y: 7.04,
    w: 1.05,
    h: 0.2,
    fontFace: style.numberFont,
    fontSize: 8.5,
    color: style.muted,
    align: "right",
    margin: 0,
  });
}

export function hairline(slide, ShapeType, x, y, w, style, color = null) {
  slide.addShape(ShapeType.line, { x, y, w, h: 0, line: { color: color || style.line, width: 0.6 } });
}

export function accentBar(slide, ShapeType, x, y, w, h, style, color = null) {
  slide.addShape(ShapeType.rect, { x, y, w, h, fill: { color: color || style.accent }, line: { color: color || style.accent } });
}

export function surface(slide, ShapeType, rect, style, opts = {}) {
  slide.addShape(opts.shape || ShapeType.rect, {
    ...rect,
    rectRadius: opts.radius ?? 0.04,
    fill: { color: opts.fill || style.surface },
    line: { color: opts.line || style.line, width: opts.lineWidth ?? 0.8 },
  });
}

export function insightBlock(slide, ShapeType, rect, label, text, style) {
  accentBar(slide, ShapeType, rect.x, rect.y, 0.05, rect.h, style);
  addText(slide, label, { x: rect.x + 0.18, y: rect.y, w: rect.w - 0.18, h: 0.24 }, style, "label", { bold: true, color: style.accent, fontSize: 10 });
  addParagraph(slide, text, { x: rect.x + 0.18, y: rect.y + 0.36, w: rect.w - 0.18, h: rect.h - 0.36 }, style, { fontSize: 18, bold: true, color: style.fg });
}

export function numberedPoints(slide, ShapeType, items, rect, style, opts = {}) {
  const data = (items || []).filter(Boolean).slice(0, opts.max || 4);
  const gap = opts.gap ?? 0.2;
  const rowH = (rect.h - gap * Math.max(0, data.length - 1)) / Math.max(1, data.length);
  data.forEach((item, i) => {
    const y = rect.y + i * (rowH + gap);
    slide.addShape(ShapeType.ellipse, { x: rect.x, y: y + 0.05, w: 0.38, h: 0.38, fill: { color: i === 0 ? style.accent : style.surface2 }, line: { color: i === 0 ? style.accent : style.line, width: 0.7 } });
    addText(slide, String(i + 1), { x: rect.x, y: y + 0.13, w: 0.38, h: 0.15 }, style, "label", { align: "center", bold: true, color: i === 0 ? "FFFFFF" : style.accent, fontSize: 9 });
    addParagraph(slide, item, { x: rect.x + 0.55, y, w: rect.w - 0.55, h: rowH }, style, { fontSize: opts.fontSize || 16.3 });
  });
}

export function kpi(slide, ShapeType, label, value, rect, style) {
  surface(slide, ShapeType, rect, style, { fill: style.surface, line: style.line, radius: 0.02 });
  addText(slide, value, { x: rect.x + 0.24, y: rect.y + 0.26, w: rect.w - 0.48, h: 0.62 }, style, "kpi", { fontFace: style.numberFont, color: style.accent, fontSize: 36, margin: 0 });
  addParagraph(slide, label, { x: rect.x + 0.26, y: rect.y + 1.02, w: rect.w - 0.52, h: 0.42 }, style, { fontSize: 12.5, color: style.muted });
}

export function visualMotif(slide, ShapeType, rect, style, variant = "stack") {
  const line = { color: style.line, width: 0.7, transparency: 10 };
  slide.addShape(ShapeType.rect, { ...rect, fill: { color: style.surface2, transparency: 8 }, line });
  if (variant === "grid") {
    for (let i = 1; i < 5; i++) slide.addShape(ShapeType.line, { x: rect.x + (rect.w * i) / 5, y: rect.y, w: 0, h: rect.h, line });
    for (let j = 1; j < 4; j++) slide.addShape(ShapeType.line, { x: rect.x, y: rect.y + (rect.h * j) / 4, w: rect.w, h: 0, line });
    accentBar(slide, ShapeType, rect.x + rect.w * 0.16, rect.y + rect.h * 0.68, rect.w * 0.46, 0.08, style);
  } else {
    accentBar(slide, ShapeType, rect.x + rect.w * 0.12, rect.y + rect.h * 0.16, rect.w * 0.42, 0.08, style);
    accentBar(slide, ShapeType, rect.x + rect.w * 0.42, rect.y + rect.h * 0.42, rect.w * 0.36, 0.08, style, style.accent2);
    accentBar(slide, ShapeType, rect.x + rect.w * 0.22, rect.y + rect.h * 0.72, rect.w * 0.55, 0.08, style);
  }
}
