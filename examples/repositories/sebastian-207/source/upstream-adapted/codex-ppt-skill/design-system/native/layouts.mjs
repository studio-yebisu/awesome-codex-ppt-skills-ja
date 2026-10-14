import fs from "node:fs";
import { addText, addSlideTitle, addKicker, addParagraph, addBullets } from "./typography.mjs";
import { footer, hairline, accentBar, surface, insightBlock, numberedPoints, kpi, visualMotif } from "./components.mjs";
import { comparisonBar, kpiRow, progressStack, trendLine } from "./charts.mjs";
import { addIntegratedImage } from "./imagery.mjs";

export const layoutArchetypes = [
  "cover-hero", "cover-minimal", "cover-editorial", "agenda-clean", "section-divider", "statement-hero",
  "text-visual-60-40", "visual-text-40-60", "two-column-argument", "three-point-summary", "metric-hero", "kpi-row",
  "comparison", "before-after", "process-linear", "process-cycle", "timeline", "matrix", "chart-hero",
  "chart-with-insight", "case-study", "quote-editorial", "roadmap", "closing-echo",
];

export function normalizeLayout(slide, idx, total) {
  const raw = String(slide.layout_archetype || slide.layout || slide.layout_family || slide.slide_type || "").toLowerCase();
  if (layoutArchetypes.includes(raw)) return raw;
  if (idx === 0 || raw.includes("cover")) return "cover-hero";
  if (idx === total - 1 || raw.includes("closing")) return "closing-echo";
  if (raw.includes("agenda") || raw.includes("toc")) return "agenda-clean";
  if (raw.includes("section") || raw.includes("divider")) return "section-divider";
  if (raw.includes("chart") || raw.includes("data")) return "chart-with-insight";
  if (raw.includes("metric") || raw.includes("kpi")) return "kpi-row";
  if (raw.includes("process") || raw.includes("flow")) return "process-linear";
  if (raw.includes("comparison") || raw.includes("compare")) return "comparison";
  const sequence = ["statement-hero", "text-visual-60-40", "three-point-summary", "chart-with-insight", "process-linear", "two-column-argument", "metric-hero", "case-study", "roadmap"];
  return sequence[(idx - 1 + sequence.length) % sequence.length];
}

function lines(value) {
  if (Array.isArray(value)) return value.map(String).filter(Boolean);
  return String(value || "").replaceAll("；", "\n").replaceAll(";", "\n").split(/\n/).map((s) => s.trim()).filter(Boolean);
}

function firstText(slide) {
  return lines(slide.body || slide.points || slide.key_message || slide.purpose || slide.speaker_notes_seed);
}

function titleText(slide, spec) {
  return slide.title || spec.title || spec.topic || "Presentation";
}

function subText(slide, spec) {
  return slide.subtitle || slide.purpose || slide.key_message || spec.audience || "";
}

function hasImageAsset(asset) {
  return !!(asset?.output_path);
}

function assetBinding(asset = {}, s = {}) {
  const binding = asset.semantic_binding || {};
  return {
    title: binding.slide_title || titleText(s, {}),
    core: binding.core_message || subText(s, {}) || firstText(s)[0] || "",
    role: binding.visual_role || asset.asset_type || s.visual_role || "visual",
    treatment: asset.integration_treatment || "60/40 split",
    slot: asset.image_slot || "",
    brief: binding.visual_brief || asset.reason || "",
  };
}

function visualLabelFor(asset = {}) {
  const type = String(asset.asset_type || assetBinding(asset).role || "").toLowerCase();
  if (type.includes("cover") || type.includes("hero")) return "表紙の挿絵";
  if (type.includes("scenario") || type.includes("scene")) return "街の風景";
  if (type.includes("system") || type.includes("product")) return "体験の設計";
  if (type.includes("process") || type.includes("flow")) return "体験の流れ";
  if (type.includes("chart") || type.includes("data")) return "関係図";
  if (type.includes("case") || type.includes("story")) return "編集の風景";
  return "体験の断片";
}

function contextualVisualPanel(slide, ShapeType, rect, s, style, asset = {}) {
  const binding = assetBinding(asset, s);
  surface(slide, ShapeType, rect, style, { fill: style.surface2, line: style.line, radius: 0.02 });
  addText(slide, visualLabelFor(asset), { x: rect.x + 0.28, y: rect.y + 0.26, w: rect.w - 0.56, h: 0.22 }, style, "label", { color: style.accent, bold: true, fontSize: 10 });
  const message = binding.core || binding.title;
  addParagraph(slide, message, { x: rect.x + 0.3, y: rect.y + 0.72, w: rect.w - 0.6, h: 0.72 }, style, { fontSize: 17.2, bold: true, color: style.fg });
  const items = (s.visual_examples || firstText(s)).slice(0, 3);
  if (!items.length && binding.brief) items.push(binding.brief);
  const baseY = rect.y + 1.78;
  items.forEach((item, i) => {
    const y = baseY + i * 0.82;
    slide.addShape(ShapeType.ellipse, { x: rect.x + 0.34, y: y + 0.05, w: 0.34, h: 0.34, fill: { color: i === 0 ? style.accent : style.bg }, line: { color: style.accent, width: 0.8 } });
    addText(slide, String(i + 1), { x: rect.x + 0.34, y: y + 0.13, w: 0.34, h: 0.13 }, style, "label", { align: "center", color: i === 0 ? "FFFFFF" : style.accent, bold: true, fontSize: 8.5 });
    addParagraph(slide, item, { x: rect.x + 0.86, y, w: rect.w - 1.18, h: 0.46 }, style, { fontSize: 12.8, color: style.muted });
  });

}

function allowsDeckBackground(spec) {
  const scope = spec?.background_image_scope || spec?.background?.scope || spec?.background_scope || "";
  return ["deck", "all_slides", "global"].includes(String(scope).toLowerCase());
}

function addDeckBackground(slide, ShapeType, spec, style) {
  if (!allowsDeckBackground(spec)) return false;
  const bgPath = spec?.background_image_path || spec?.background?.image_path || "";
  if (bgPath && fs.existsSync(bgPath)) {
    slide.addImage({ path: bgPath, x: 0, y: 0, w: 13.333, h: 7.5 });
    slide.addShape(ShapeType.rect, {
      x: 0,
      y: 0,
      w: 13.333,
      h: 7.5,
      fill: { color: style.bg, transparency: 72 },
      line: { color: style.bg, transparency: 100 },
    });
    return true;
  }
  return false;
}

function drawBackground(slide, ShapeType, style, layout, idx, spec = {}) {
  const hasImageBackground = addDeckBackground(slide, ShapeType, spec, style);
  slide.background = { color: style.bg };
  if (layout === "cover-hero" || layout === "closing-echo") {
    if (!hasImageBackground) {
      slide.addShape(ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: style.bg }, line: { color: style.bg } });
    }
    slide.addShape(ShapeType.rect, { x: 9.7, y: 0, w: 3.633, h: 7.5, fill: { color: style.surface2, transparency: hasImageBackground ? 18 : 0 }, line: { color: style.surface2, transparency: hasImageBackground ? 35 : 0 } });
  } else if (idx % 5 === 0) {
    slide.addShape(ShapeType.rect, { x: 0, y: 0, w: 0.16, h: 7.5, fill: { color: style.accent }, line: { color: style.accent } });
  }
}

function cover(slide, ShapeType, s, spec, style, asset, variant = "hero") {
  drawBackground(slide, ShapeType, style, "cover-hero", 0, spec);
  addKicker(slide, spec.kicker || spec.use_case || "PRESENTATION", { x: 0.78, y: 0.86, w: 5.1, h: 0.25 }, style);
  addText(slide, titleText(s, spec), { x: 0.78, y: 1.42, w: 6.5, h: 1.48 }, style, "coverTitle", { fontSize: variant === "minimal" ? 50 : 45, fit: "shrink" });
  addParagraph(slide, subText(s, spec), { x: 0.82, y: 3.18, w: 5.75, h: 0.78 }, style, { fontSize: 18, color: style.muted });
  hairline(slide, ShapeType, 0.82, 4.37, 1.28, style, style.accent);
  if (variant === "minimal") return;
  const rect = { x: 7.32, y: 0.68, w: 4.95, h: 5.98 };
  if (hasImageAsset(asset)) {
    addIntegratedImage(slide, ShapeType, asset?.output_path, rect, style, asset?.integration_treatment || "masked editorial crop");
  } else {
    contextualVisualPanel(slide, ShapeType, rect, s, style, asset);
  }
}

function defaultHeader(slide, ShapeType, s, spec, style, idx, total) {
  addSlideTitle(slide, titleText(s, spec), style);
  hairline(slide, ShapeType, 0.72, 1.2, 11.9, style);
  footer(slide, idx + 1, total, style);
}

function agenda(slide, ShapeType, s, spec, style, idx, total) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  const items = firstText(s).slice(0, 6);
  numberedPoints(slide, ShapeType, items, { x: 1.1, y: 1.65, w: 8.8, h: 4.6 }, style, { max: 6, fontSize: 18 });
}

function section(slide, ShapeType, s, spec, style, idx, total) {
  slide.background = { color: style.fg };
  addKicker(slide, `SECTION ${String(idx).padStart(2, "0")}`, { x: 0.86, y: 0.82, w: 3, h: 0.24 }, { ...style, accent: style.accent2 });
  addText(slide, titleText(s, spec), { x: 0.86, y: 1.58, w: 7.8, h: 1.18 }, { ...style, fg: style.bg }, "sectionTitle", { fontSize: 38 });
  addParagraph(slide, subText(s, spec), { x: 0.9, y: 3.12, w: 6.6, h: 0.62 }, { ...style, fg: style.bg, muted: "D1D5DB" }, { fontSize: 17, color: "D1D5DB" });
  accentBar(slide, ShapeType, 0.9, 4.38, 1.7, 0.08, style);
  footer(slide, idx + 1, total, { ...style, muted: "CBD5E1" });
}

function statement(slide, ShapeType, s, spec, style, idx, total) {
  defaultHeader(slide, ShapeType, { ...s, title: spec.kicker || "企画の視点" }, spec, style, idx, total);
  addText(slide, titleText(s, spec), { x: 1.02, y: 1.62, w: 11.2, h: 1.65 }, style, "statement", { fontSize: 46, color: style.fg });
  insightBlock(slide, ShapeType, { x: 1.05, y: 3.38, w: 8.2, h: 1.15 }, "企画の意図", subText(s, spec) || firstText(s)[0] || "用一句明确判断建立本页焦点。", style);

}

function textVisual(slide, ShapeType, s, spec, style, asset, idx, total, flip = false) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  const textRect = flip ? { x: 7.25, y: 1.58, w: 4.8, h: 4.55 } : { x: 0.92, y: 1.58, w: 5.15, h: 4.55 };
  const imgRect = flip ? { x: 0.92, y: 1.52, w: 5.72, h: 4.82 } : { x: 6.75, y: 1.52, w: 5.62, h: 4.82 };
  addParagraph(slide, subText(s, spec), { ...textRect, h: 0.72 }, style, { fontSize: 18, color: style.fg, bold: true });
  numberedPoints(slide, ShapeType, firstText(s), { x: textRect.x, y: textRect.y + 1.05, w: textRect.w, h: 3.2 }, style, { max: 4, fontSize: 15.8 });
  if (hasImageAsset(asset)) {
    addIntegratedImage(slide, ShapeType, asset?.output_path, imgRect, style, asset?.integration_treatment || "60/40 split");
  } else {
    contextualVisualPanel(slide, ShapeType, imgRect, s, style, asset);
  }
}

function threePoint(slide, ShapeType, s, spec, style, idx, total) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  const items = firstText(s).slice(0, 3);
  insightBlock(slide, ShapeType, { x: 0.9, y: 1.55, w: 3.05, h: 3.85 }, "KEY MESSAGE", subText(s, spec) || items[0] || "", style);
  const rect = { x: 4.45, y: 1.55, w: 7.72, h: 3.85 };
  const gap = 0.22;
  const h = (rect.h - gap * 2) / 3;
  items.forEach((item, i) => {
    const y = rect.y + i * (h + gap);
    surface(slide, ShapeType, { x: rect.x, y, w: rect.w, h }, style, { fill: i === 0 ? style.surface2 : style.surface, line: style.line, radius: 0.02 });
    addText(slide, `0${i + 1}`, { x: rect.x + 0.22, y: y + 0.25, w: 0.5, h: 0.24 }, style, "label", { color: style.accent, bold: true, fontSize: 11 });
    addParagraph(slide, item, { x: rect.x + 0.86, y: y + 0.18, w: rect.w - 1.14, h: h - 0.26 }, style, { fontSize: 16.2 });
  });
}

function chart(slide, ShapeType, s, spec, style, idx, total, hero = false) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  if (hero) {
    insightBlock(slide, ShapeType, { x: 0.9, y: 1.58, w: 3.25, h: 3.55 }, "INSIGHT", subText(s, spec) || "把图表标题写成结论，而不是数据名称。", style);
    trendLine(slide, ShapeType, { x: 4.55, y: 1.5, w: 7.45, h: 4.25 }, style);
  } else {
    comparisonBar(slide, ShapeType, { x: 0.95, y: 1.66, w: 6.15, h: 3.72 }, style);
    insightBlock(slide, ShapeType, { x: 7.65, y: 1.72, w: 3.9, h: 2.1 }, "READ THIS", subText(s, spec) || firstText(s)[0] || "强调一个结论，其余数据退居背景。", style);
  }
}

function process(slide, ShapeType, s, spec, style, idx, total, cycle = false) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  const items = firstText(s).slice(0, cycle ? 4 : 5);
  progressStack(slide, ShapeType, { x: 1.0, y: 2.0, w: 10.8, h: 1.0 }, style, items);
  numberedPoints(slide, ShapeType, items, { x: 1.05, y: 3.42, w: 10.2, h: 2.15 }, style, { max: 5, fontSize: 14.6 });
}

function comparison(slide, ShapeType, s, spec, style, idx, total, beforeAfter = false) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  const items = firstText(s);
  const left = { x: 0.95, y: 1.62, w: 5.35, h: 4.15 };
  const right = { x: 6.98, y: 1.62, w: 5.35, h: 4.15 };
  surface(slide, ShapeType, left, style, { fill: style.surface, line: style.line, radius: 0.02 });
  surface(slide, ShapeType, right, style, { fill: style.surface2, line: style.accent, radius: 0.02, lineWidth: 1.1 });
  addText(slide, beforeAfter ? "いつもの読書" : "これまで", { x: left.x + 0.28, y: left.y + 0.26, w: left.w - 0.56, h: 0.26 }, style, "label", { bold: true, color: style.muted });
  addText(slide, beforeAfter ? "編集室の読書" : "編集室", { x: right.x + 0.28, y: right.y + 0.26, w: right.w - 0.56, h: 0.26 }, style, "label", { bold: true, color: style.accent });
  addBullets(slide, items.slice(0, 3), { x: left.x + 0.34, y: left.y + 0.9, w: left.w - 0.7, h: 2.8 }, style, { max: 3, fontSize: 15.2 });
  addBullets(slide, items.slice(3, 6).length ? items.slice(3, 6) : items.slice(0, 3), { x: right.x + 0.34, y: right.y + 0.9, w: right.w - 0.7, h: 2.8 }, style, { max: 3, fontSize: 15.2 });
}

function matrix(slide, ShapeType, s, spec, style, idx, total) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  surface(slide, ShapeType, { x: 1.16, y: 1.55, w: 10.3, h: 4.5 }, style, { fill: style.surface, line: style.line, radius: 0.01 });
  hairline(slide, ShapeType, 1.16, 3.8, 10.3, style);
  slide.addShape(ShapeType.line, { x: 6.31, y: 1.55, w: 0, h: 4.5, line: { color: style.line, width: 0.7 } });
  const items = firstText(s);
  [["高影响", 1.55], ["低影响", 3.8]].forEach(([label, y]) => addText(slide, label, { x: 1.34, y: y + 0.18, w: 1.0, h: 0.22 }, style, "label", { color: style.accent, bold: true }));
  items.slice(0, 4).forEach((item, i) => {
    const x = i % 2 === 0 ? 2.05 : 7.2;
    const y = i < 2 ? 2.1 : 4.35;
    addParagraph(slide, item, { x, y, w: 3.2, h: 0.72 }, style, { fontSize: 15 });
  });
}

function quote(slide, ShapeType, s, spec, style, idx, total) {
  defaultHeader(slide, ShapeType, { ...s, title: spec.kicker || "企画の宣言" }, spec, style, idx, total);
  addText(slide, `“${titleText(s, spec)}”`, { x: 1.1, y: 1.55, w: 10.8, h: 1.9 }, style, "statement", { fontSize: 52 });
  addParagraph(slide, subText(s, spec) || firstText(s)[0] || "", { x: 1.18, y: 3.25, w: 6.7, h: 0.72 }, style, { fontSize: 18, color: style.muted });

}

function roadmap(slide, ShapeType, s, spec, style, idx, total) {
  defaultHeader(slide, ShapeType, s, spec, style, idx, total);
  const items = firstText(s).slice(0, 5);
  const y = 3.05;
  hairline(slide, ShapeType, 1.2, y, 10.5, style, style.accent);
  items.forEach((item, i) => {
    const x = 1.2 + i * 2.55;
    slide.addShape(ShapeType.ellipse, { x: x - 0.1, y: y - 0.1, w: 0.2, h: 0.2, fill: { color: i === 0 ? style.accent : style.surface }, line: { color: style.accent, width: 1 } });
    addText(slide, `0${i + 1}`, { x: x - 0.24, y: y - 0.58, w: 0.48, h: 0.2 }, style, "label", { align: "center", color: style.accent, bold: true, fontSize: 10 });
    addParagraph(slide, item, { x: x - 0.65, y: y + 0.36, w: 1.5, h: 0.75 }, style, { fontSize: 12.8 });
  });
}

export function drawSlide(slide, ShapeType, s, context) {
  const { spec, style, asset, idx, total } = context;
  const layout = normalizeLayout(s, idx, total);
  drawBackground(slide, ShapeType, style, layout, idx, spec);
  switch (layout) {
    case "cover-hero": return cover(slide, ShapeType, s, spec, style, asset, "hero");
    case "cover-minimal": return cover(slide, ShapeType, s, spec, style, asset, "minimal");
    case "cover-editorial": return cover(slide, ShapeType, s, spec, style, asset, "editorial");
    case "agenda-clean": return agenda(slide, ShapeType, s, spec, style, idx, total);
    case "section-divider": return section(slide, ShapeType, s, spec, style, idx, total);
    case "statement-hero": return statement(slide, ShapeType, s, spec, style, idx, total);
    case "text-visual-60-40": return textVisual(slide, ShapeType, s, spec, style, asset, idx, total, false);
    case "visual-text-40-60": return textVisual(slide, ShapeType, s, spec, style, asset, idx, total, true);
    case "two-column-argument": return comparison(slide, ShapeType, s, spec, style, idx, total, false);
    case "three-point-summary": return threePoint(slide, ShapeType, s, spec, style, idx, total);
    case "metric-hero": return chart(slide, ShapeType, s, spec, style, idx, total, true);
    case "kpi-row": return defaultHeader(slide, ShapeType, s, spec, style, idx, total), kpiRow(slide, ShapeType, { x: 0.94, y: 1.75, w: 11.1, h: 1.62 }, style), insightBlock(slide, ShapeType, { x: 1.02, y: 4.18, w: 8.4, h: 1.05 }, "结论", subText(s, spec) || firstText(s)[0] || "", style);
    case "comparison": return comparison(slide, ShapeType, s, spec, style, idx, total, false);
    case "before-after": return comparison(slide, ShapeType, s, spec, style, idx, total, true);
    case "process-linear": return process(slide, ShapeType, s, spec, style, idx, total, false);
    case "process-cycle": return process(slide, ShapeType, s, spec, style, idx, total, true);
    case "timeline": return roadmap(slide, ShapeType, s, spec, style, idx, total);
    case "matrix": return matrix(slide, ShapeType, s, spec, style, idx, total);
    case "chart-hero": return chart(slide, ShapeType, s, spec, style, idx, total, true);
    case "chart-with-insight": return chart(slide, ShapeType, s, spec, style, idx, total, false);
    case "case-study": return textVisual(slide, ShapeType, s, spec, style, asset, idx, total, false);
    case "quote-editorial": return quote(slide, ShapeType, s, spec, style, idx, total);
    case "roadmap": return roadmap(slide, ShapeType, s, spec, style, idx, total);
    case "closing-echo": return cover(slide, ShapeType, s, spec, style, asset, "minimal");
    default: return threePoint(slide, ShapeType, s, spec, style, idx, total);
  }
}
