const pptxgen = require("pptxgenjs");
const fs = require("fs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Presenter Name";
pres.title = "Presentation Title";

// Theme — short alias T
const T = {
  bg: { title: "1E2761", content: "F8F9FA", section: "1E2761" },
  tx: { pri: "1A1A2E", sec: "4A4A5A", mut: "8C8C8C", wh: "FFFFFF" },
  ac: { pos: "0173B2", neg: "DE8F05", emp: "029E73" },
  chart: ["0173B2", "DE8F05", "029E73", "CC78BC"],
  cardFill: "0173B215", divider: "D0D0D0"
};

// Typography — default baselines (scale up when content is sparse, see QA density check)
const F = {
  cover:    { face: "Georgia", size: 48 },
  section:  { face: "Georgia", size: 36 },
  title:    { face: "Georgia", size: 22 },
  subtitle: { face: "Calibri", size: 18 },
  body:     { face: "Calibri", size: 15 },
  small:    { face: "Calibri", size: 12 },
  caption:  { face: "Calibri", size: 11 },
  stat:     { face: "Georgia", size: 60 },
  cardTitle:{ face: "Georgia", size: 18 },
  tblHead:  { face: "Calibri", size: 13 },
  tblCell:  { face: "Calibri", size: 12 },
};

// Layout constants
const SW = 10, SH = 5.625, M = 0.5;
const CW = SW - 2 * M;       // content width (9")
const CY = 0.9;              // content top Y (below title bar)
const CH = SH - CY - M;      // content height (4.225")

// Slide Masters
pres.defineSlideMaster({
  title: "TITLE_SLIDE",
  background: { color: T.bg.title },
  objects: [
    { rect: { x: 0, y: 4.8, w: SW, h: 0.825, fill: { color: "000000", transparency: 30 } } }
  ]
});
pres.defineSlideMaster({
  title: "SECTION_SLIDE",
  background: { color: T.bg.section }
});
pres.defineSlideMaster({
  title: "CONTENT_SLIDE",
  background: { color: T.bg.content },
  objects: [
    { rect: { x: 0, y: 0, w: SW, h: 0.7, fill: { color: T.bg.title } } }
  ]
});
pres.defineSlideMaster({
  title: "THANK_YOU",
  background: { color: T.bg.title }
});

// Formula manifest — supports OMML (native math) and image (PNG/SVG) entries
const manifest = JSON.parse(fs.readFileSync("formulas/manifest.json", "utf8"));

// OMML placeholder — inject_omml.py replaces these post-generation
function addMathText(slide, id, x, y, w, h, opts = {}) {
  slide.addText(`{{MATH:${id}}}`, {
    x, y, w, h,
    fontFace: opts.fontFace || F.body.face,
    fontSize: opts.fontSize || F.body.size,
    color: opts.color || T.tx.pri,
    align: opts.align || "center",
    valign: opts.valign || "middle",
    margin: 0
  });
}

// Centered formula — auto-routes OMML vs image based on manifest
function addFormula(slide, id, y, targetH = 0.4) {
  const f = manifest[id];
  if (!f || f.error) return;
  if (f.render === "omml") {
    addMathText(slide, id, M, y, CW, targetH);
    return;
  }
  if (f.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(f.file, "utf8")).toString("base64");
    const scale = targetH / (f.height_pt / 72);
    const w = (f.width_pt / 72) * scale;
    slide.addImage({ data: "image/svg+xml;base64," + b64, x: (SW - w) / 2, y, w, h: targetH });
  } else {
    const dpi = f.dpi || 600;
    const scale = targetH / (f.height_px / dpi);
    const w = (f.width_px / dpi) * scale;
    slide.addImage({ path: f.file, x: (SW - w) / 2, y, w, h: targetH });
  }
}

// Left-aligned formula — auto-routes OMML vs image
function addFormulaAt(slide, id, x, y, maxW, targetH) {
  const f = manifest[id];
  if (!f || f.error) return;
  if (f.render === "omml") {
    addMathText(slide, id, x, y, maxW, targetH, { align: "left" });
    return;
  }
  if (f.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(f.file, "utf8")).toString("base64");
    let scale = targetH / (f.height_pt / 72);
    let w = (f.width_pt / 72) * scale, h = targetH;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ data: "image/svg+xml;base64," + b64, x, y, w, h });
  } else {
    const dpi = f.dpi || 600;
    let scale = targetH / (f.height_px / dpi);
    let w = (f.width_px / dpi) * scale, h = targetH;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ path: f.file, x, y, w, h });
  }
}

// Card with formula body — auto-routes OMML vs image
function addCardFormula(sl, x, y, w, h, color, title, formulaId, fH) {
  chk("cardFormula", y, h);
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill: { color: "FFFFFF" }, shadow: mkSh() });
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h,
    fill: { color } });
  const px = x + 0.25, pw = w - 0.4;
  sl.addText(title, { x: px, y: y + 0.1, w: pw, h: 0.4,
    fontFace: F.cardTitle.face, fontSize: F.cardTitle.size, bold: true,
    color: T.tx.pri, valign: "top", margin: [0, 0, 0, 0], shrinkText: true });
  addFormulaAt(sl, formulaId, px, y + 0.55, pw, fH || (h - 0.7));
}

// Factory: card shadow (NEVER reuse option objects directly)
const mkSh = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 });

// Diagram manifest (optional — only when diagrams/ exists)
const dManifest = (() => {
  try { return JSON.parse(fs.readFileSync("diagrams/manifest.json", "utf8")); }
  catch { return {}; }
})();

// Centered diagram
function addDiagram(slide, id, y, targetH, maxW = CW) {
  const d = dManifest[id];
  if (!d || d.error) return;
  let w, h = targetH;
  if (d.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(d.file, "utf8")).toString("base64");
    const scale = targetH / (d.height_pt / 72);
    w = (d.width_pt / 72) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ data: "image/svg+xml;base64," + b64, x: (SW - w) / 2, y, w, h });
  } else {
    const dpi = d.dpi || 300;
    const scale = targetH / (d.height_px / dpi);
    w = (d.width_px / dpi) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ path: d.file, x: (SW - w) / 2, y, w, h });
  }
}

// Positioned diagram (for two-column layouts)
function addDiagramAt(slide, id, x, y, maxW, targetH) {
  const d = dManifest[id];
  if (!d || d.error) return;
  let w, h = targetH;
  if (d.format === "svg") {
    const b64 = Buffer.from(fs.readFileSync(d.file, "utf8")).toString("base64");
    const scale = targetH / (d.height_pt / 72);
    w = (d.width_pt / 72) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ data: "image/svg+xml;base64," + b64, x, y, w, h });
  } else {
    const dpi = d.dpi || 300;
    const scale = targetH / (d.height_px / dpi);
    w = (d.width_px / dpi) * scale;
    if (w > maxW) { const s = maxW / w; w = maxW; h *= s; }
    slide.addImage({ path: d.file, x, y, w, h });
  }
}

// Extracted figure with caption (source attribution)
// Aspect-ratio-aware: wide images (ratio>1.6) use full-width centered,
// normal/tall images (ratio≤1.6) use left-figure + right-text layout via addFigureWithText.
function addFigure(slide, id, y, targetH, caption) {
  addDiagram(slide, id, y, targetH - 0.3);
  if (caption) {
    slide.addText(caption, {
      x: M, y: y + targetH - 0.25, w: CW, h: 0.25,
      fontFace: F.caption.face, fontSize: F.caption.size,
      color: T.tx.mut, align: "center", italic: true, margin: 0
    });
  }
}

// Figure + text side-by-side layout (aspect-ratio-aware)
// For images with ratio ≤ 1.6: figure on left, bullets/text on right
// figRatio = original image width / height (read from manifest or measured)
// textItems: array of strings for right-side bullets
function addFigureWithText(slide, id, y, targetH, figRatio, textItems, caption) {
  const d = dManifest[id];
  if (!d || d.error) return;
  const gap = 0.3;
  // Compute figure width from height and ratio, cap at 60% of CW
  let figH = targetH - (caption ? 0.3 : 0);
  let figW = figH * figRatio;
  const maxFigW = CW * 0.6;
  if (figW > maxFigW) { const s = maxFigW / figW; figW = maxFigW; figH *= s; }
  const textX = M + figW + gap;
  const textW = CW - figW - gap;
  // Image (left)
  addDiagramAt(slide, id, M, y, figW, figH);
  // Bullets (right)
  if (textItems && textItems.length > 0) {
    addBullets(slide, textItems, textX, y, textW, figH);
  }
  // Caption (below figure)
  if (caption) {
    slide.addText(caption, {
      x: M, y: y + targetH - 0.25, w: figW, h: 0.25,
      fontFace: F.caption.face, fontSize: F.caption.size,
      color: T.tx.mut, align: "center", italic: true, margin: 0
    });
  }
}

// Speaker notes (optional — add after all slide content)
function addNotes(slide, text) {
  slide.addNotes(text);
}

// Themed chart (auto-applies theme colors and clean styling)
function addChart(sl, type, data, x, y, w, h, opts = {}) {
  chk("chart", y, h);
  sl.addChart(type, data, {
    x, y, w, h,
    chartColors: opts.chartColors || T.chart,
    chartArea: { fill: { color: T.bg.content }, roundedCorners: true },
    catAxisLabelColor: T.tx.sec, valAxisLabelColor: T.tx.sec,
    catAxisLabelFontFace: F.tblCell.face, catAxisLabelFontSize: F.tblCell.size,
    valAxisLabelFontFace: F.tblCell.face, valAxisLabelFontSize: F.tblCell.size,
    valGridLine: { color: T.divider, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: opts.showLegend !== undefined ? opts.showLegend : data.length > 1,
    legendPos: opts.legendPos || "b",
    legendFontFace: F.caption.face, legendFontSize: F.caption.size, legendColor: T.tx.sec,
    ...opts,
  });
}

// --- Slide builders ---

function sTitle(sl, txt) {
  sl.addText(txt, { x: M, y: 0.08, w: CW, h: 0.55,
    fontFace: F.title.face, fontSize: F.title.size, bold: true,
    color: T.tx.wh, margin: [0, 6, 0, 0], shrinkText: true });
}

function sectionSlide(title) {
  const sl = pres.addSlide({ masterName: "SECTION_SLIDE" });
  sl.addText(title, { x: M, y: SH / 2 - 0.5, w: CW, h: 1,
    fontFace: F.section.face, fontSize: F.section.size, bold: true,
    color: T.tx.wh, align: "center", valign: "middle" });
  sl.addShape(pres.shapes.RECTANGLE, { x: SW / 2 - 1.5, y: SH / 2 + 0.4,
    w: 3, h: 0.04, fill: { color: T.ac.pos } });
  return sl;
}

// --- Content helpers ---

function addBullets(sl, items, x, y, w, h, opts = {}) {
  chk("bullets", y, h);
  const arr = items.map((t, i) => ({
    text: t, options: {
      bullet: true, breakLine: i < items.length - 1,
      fontSize: opts.fontSize || F.body.size,
      fontFace: opts.fontFace || F.body.face,
      color: opts.color || T.tx.pri,
    }
  }));
  sl.addText(arr, { x, y, w, h, valign: "top", margin: [4, 6, 4, 4], shrinkText: true });
}

function addCard(sl, x, y, w, h, color, title, body) {
  chk("card", y, h);
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w, h,
    fill: { color: "FFFFFF" }, shadow: mkSh() });
  sl.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h,
    fill: { color } });
  // px: 0.19" clear of accent bar. pw: 0.15" from right edge.
  const px = x + 0.25, pw = w - 0.4;
  sl.addText(title, { x: px, y: y + 0.1, w: pw, h: 0.4,
    fontFace: F.cardTitle.face, fontSize: F.cardTitle.size, bold: true,
    color: T.tx.pri, valign: "top", margin: [0, 0, 0, 0], shrinkText: true });
  sl.addText(body, { x: px, y: y + 0.48, w: pw, h: h - 0.62,
    fontFace: F.body.face, fontSize: F.body.size,
    color: T.tx.sec, valign: "top", margin: [2, 0, 8, 0], shrinkText: true });
}

function addTable(sl, headers, rows, x, y, w, colW, rowH = 0.35) {
  chk("table", y, rowH * (rows.length + 1));
  const hRow = headers.map(h => ({ text: h, options: {
    fill: { color: T.bg.title }, color: T.tx.wh,
    bold: true, fontFace: F.tblHead.face, fontSize: F.tblHead.size,
    align: "center", valign: "middle"
  }}));
  const dRows = rows.map((row, i) => row.map(cell => {
    const isObj = typeof cell === "object" && cell !== null;
    const txt = isObj ? cell.text : String(cell);
    const base = {
      fill: { color: i % 2 === 0 ? "FFFFFF" : "F0F2F5" },
      fontFace: F.tblCell.face, fontSize: F.tblCell.size,
      color: T.tx.pri, valign: "middle"
    };
    return { text: txt, options: isObj ? { ...base, ...cell.options } : base };
  }));
  sl.addTable([hRow, ...dRows], { x, y, w, colW, border: { pt: 0.5, color: "E0E0E0" } });
}

// Continuation table page — repeats header, adds " (cont'd)" to slide title
function addTableCont(sl, title, headers, rows, x, y, w, colW, rowH = 0.35) {
  sTitle(sl, title + " (cont'd)");
  addTable(sl, headers, rows, x, y, w, colW, rowH);
}

function addNumCard(sl, num, title, body, x, y, w, h, color) {
  addCard(sl, x, y, w, h, color, title, body);
  sl.addShape(pres.shapes.OVAL, { x: x + w - 0.4, y: y - 0.15,
    w: 0.35, h: 0.35, fill: { color } });
  sl.addText(String(num), { x: x + w - 0.4, y: y - 0.15, w: 0.35, h: 0.35,
    fontFace: F.title.face, fontSize: 14, bold: true,
    color: "FFFFFF", align: "center", valign: "middle", margin: 0 });
}

function addFlow(sl, steps, y, h = 0.6) {
  const n = steps.length;
  const gap = 0.25, arrowW = 0.2;
  const totalArrows = (n - 1) * (gap + arrowW);
  const boxW = (CW - totalArrows) / n;
  let cx = M;
  steps.forEach((step, i) => {
    sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y, w: boxW, h,
      fill: { color: T.ac.pos, transparency: 88 },
      line: { color: T.ac.pos, width: 1.5 }, rectRadius: 0.08 });
    sl.addText(step, { x: cx, y, w: boxW, h,
      fontFace: F.small.face, fontSize: F.small.size,
      color: T.tx.pri, align: "center", valign: "middle", margin: 0 });
    if (i < n - 1) {
      const ax = cx + boxW + gap / 2;
      sl.addText("→", { x: ax, y, w: arrowW, h,
        fontFace: F.body.face, fontSize: 18, color: T.tx.mut,
        align: "center", valign: "middle", margin: 0 });
    }
    cx += boxW + gap + arrowW;
  });
}

function cols2() {
  const gap = 0.3, colW = (CW - gap) / 2;
  return {
    left:  { x: M, w: colW },
    right: { x: M + colW + gap, w: colW },
    colW, gap
  };
}

// Boundary check: warn if element bottom exceeds slide content area
function chk(label, y, h) {
  const bot = y + h;
  if (bot > SH - M + 0.05) console.warn(`OVERFLOW: ${label} bottom=${bot.toFixed(2)}" > limit=${(SH-M).toFixed(2)}"`);
}

// Gap check: verify element starts below previous element's bottom with minimum gap
let _lastBot = 0;
function gap(label, y, minGap = 0.08) {
  if (_lastBot > 0 && y < _lastBot + minGap)
    console.warn(`OVERLAP: ${label} y=${y.toFixed(2)}" < prev bottom + gap=${(_lastBot+minGap).toFixed(2)}"`);
}
function trackBot(y, h) { _lastBot = y + h; }
function resetBot() { _lastBot = 0; }

