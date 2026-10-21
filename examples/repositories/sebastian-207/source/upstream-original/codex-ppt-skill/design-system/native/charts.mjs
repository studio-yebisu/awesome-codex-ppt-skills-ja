import { addText, addParagraph } from "./typography.mjs";
import { surface, accentBar } from "./components.mjs";

export function comparisonBar(slide, ShapeType, rect, style, data = null) {
  const rows = data || [
    { label: "成本", base: 72, focus: 46 },
    { label: "效率", base: 48, focus: 82 },
    { label: "体验", base: 55, focus: 76 },
  ];
  const max = 100;
  const rowH = rect.h / rows.length;
  rows.forEach((row, i) => {
    const y = rect.y + i * rowH + 0.12;
    addText(slide, row.label, { x: rect.x, y, w: 1.15, h: 0.24 }, style, "chartLabel", { fontSize: 12.5, color: style.fg });
    slide.addShape(ShapeType.rect, { x: rect.x + 1.2, y: y + 0.03, w: rect.w - 1.65, h: 0.12, fill: { color: style.surface2 }, line: { color: style.surface2 } });
    slide.addShape(ShapeType.rect, { x: rect.x + 1.2, y: y + 0.03, w: (rect.w - 1.65) * row.base / max, h: 0.12, fill: { color: style.line }, line: { color: style.line } });
    slide.addShape(ShapeType.rect, { x: rect.x + 1.2, y: y + 0.23, w: (rect.w - 1.65) * row.focus / max, h: 0.16, fill: { color: style.accent }, line: { color: style.accent } });
    addText(slide, `${row.focus}`, { x: rect.x + rect.w - 0.38, y: y + 0.17, w: 0.38, h: 0.2 }, style, "chartLabel", { fontFace: style.numberFont, fontSize: 11, color: style.accent, align: "right" });
  });
}

export function kpiRow(slide, ShapeType, rect, style, metrics = null) {
  const data = metrics || [
    { label: "核心效率提升", value: "32%" },
    { label: "重复工作减少", value: "41%" },
    { label: "交付周期缩短", value: "2.4x" },
  ];
  const gap = 0.18;
  const w = (rect.w - gap * (data.length - 1)) / data.length;
  data.forEach((m, i) => {
    const x = rect.x + i * (w + gap);
    surface(slide, ShapeType, { x, y: rect.y, w, h: rect.h }, style, { fill: i === 0 ? style.surface2 : style.surface, line: style.line, radius: 0.03 });
    addText(slide, m.value, { x: x + 0.22, y: rect.y + 0.25, w: w - 0.44, h: 0.62 }, style, "kpi", { fontFace: style.numberFont, color: i === 0 ? style.accent : style.fg, fontSize: 34 });
    addParagraph(slide, m.label, { x: x + 0.24, y: rect.y + 0.98, w: w - 0.48, h: 0.42 }, style, { fontSize: 12.5, color: style.muted });
  });
}

export function progressStack(slide, ShapeType, rect, style, steps = null) {
  const data = steps || ["输入", "处理", "生成", "复核"];
  const gap = 0.1;
  const w = (rect.w - gap * (data.length - 1)) / data.length;
  data.forEach((s, i) => {
    const x = rect.x + i * (w + gap);
    slide.addShape(ShapeType.rect, { x, y: rect.y + 0.42, w, h: 0.28, fill: { color: i === data.length - 1 ? style.accent : style.surface2 }, line: { color: i === data.length - 1 ? style.accent : style.line, width: 0.7 } });
    addText(slide, s, { x, y: rect.y, w, h: 0.24 }, style, "chartLabel", { fontSize: 11.5, color: i === data.length - 1 ? style.accent : style.muted, bold: i === data.length - 1, align: "center" });
  });
}

export function trendLine(slide, ShapeType, rect, style) {
  surface(slide, ShapeType, rect, style, { fill: style.surface, line: style.line, radius: 0.02 });
  for (let i = 1; i < 4; i++) {
    const y = rect.y + 0.35 + (rect.h - 0.7) * i / 4;
    slide.addShape(ShapeType.line, { x: rect.x + 0.35, y, w: rect.w - 0.7, h: 0, line: { color: style.line, width: 0.5, transparency: 25 } });
  }
  const pts = [
    [rect.x + 0.48, rect.y + rect.h - 0.55],
    [rect.x + rect.w * 0.33, rect.y + rect.h * 0.58],
    [rect.x + rect.w * 0.58, rect.y + rect.h * 0.42],
    [rect.x + rect.w - 0.48, rect.y + 0.62],
  ];
  for (let i = 0; i < pts.length - 1; i++) {
    slide.addShape(ShapeType.line, { x: pts[i][0], y: pts[i][1], w: pts[i + 1][0] - pts[i][0], h: pts[i + 1][1] - pts[i][1], line: { color: style.accent, width: 2 } });
  }
  pts.forEach(([x, y], i) => slide.addShape(ShapeType.ellipse, { x: x - 0.055, y: y - 0.055, w: 0.11, h: 0.11, fill: { color: i === pts.length - 1 ? style.accent : style.surface }, line: { color: style.accent, width: 1 } }));
  accentBar(slide, ShapeType, rect.x + rect.w - 1.35, rect.y + 0.5, 0.9, 0.08, style);
  addText(slide, "趋势向上", { x: rect.x + rect.w - 1.35, y: rect.y + 0.68, w: 1.0, h: 0.22 }, style, "chartLabel", { color: style.accent, bold: true, fontSize: 12 });
}
