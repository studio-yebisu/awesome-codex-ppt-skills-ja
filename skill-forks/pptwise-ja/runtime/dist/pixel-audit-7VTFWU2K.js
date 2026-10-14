import {
  CANVAS_H_PX,
  CANVAS_W_PX,
  __collectImageBackedTextRuns,
  blendOver,
  contrastRatio2 as contrastRatio,
  rasterizeSvgInBrowser,
  renderSlideSvg,
  resolveIrTheme
} from "./chunk-DQABTUNM.js";
import {
  getPlatform
} from "./chunk-RHKPZSTM.js";

// src/audit/pixel-audit.ts
var PIXEL_CANVAS_W = CANVAS_W_PX;
var PIXEL_CANVAS_H = CANVAS_H_PX;
var PIXEL_HARD_FINDING_MAX_RATIO = 1.5;
var TEXT_ELEMENT_RE = /<text\b[^>]*\/>|<text\b[^>]*>[\s\S]*?<\/text>/g;
function stripTextNodes(markup) {
  return markup.replace(TEXT_ELEMENT_RE, "");
}
function rgbToHex(r, g, b) {
  const toHex = (v) => Math.round(v).toString(16).padStart(2, "0");
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
}
var SAMPLE_ASCENT_RATIO = 0.75;
var MIN_GUARANTEED_PATCH_PX = 10;
var SAMPLE_STRIDE_PX = MIN_GUARANTEED_PATCH_PX / 2;
var AGGREGATION_HALF_PX = 1;
function samplePositions(lo, hi) {
  if (hi <= lo) return [lo];
  const positions = [];
  for (let v = lo; v < hi; v += SAMPLE_STRIDE_PX) positions.push(v);
  positions.push(hi);
  return positions;
}
function averageWindow(image, cx, cy) {
  const x0 = Math.round(cx);
  const y0 = Math.round(cy);
  let sumR = 0;
  let sumG = 0;
  let sumB = 0;
  let count = 0;
  for (let dy = -AGGREGATION_HALF_PX; dy <= AGGREGATION_HALF_PX; dy++) {
    const y = y0 + dy;
    if (y < 0 || y >= image.height) continue;
    for (let dx = -AGGREGATION_HALF_PX; dx <= AGGREGATION_HALF_PX; dx++) {
      const x = x0 + dx;
      if (x < 0 || x >= image.width) continue;
      const i = (y * image.width + x) * 4;
      const alpha = image.data[i + 3];
      if (alpha < 255) continue;
      sumR += image.data[i];
      sumG += image.data[i + 1];
      sumB += image.data[i + 2];
      count++;
    }
  }
  if (count === 0) return null;
  return { r: sumR / count, g: sumG / count, b: sumB / count };
}
function worstCaseSample(run, image) {
  const top = run.baseline - run.fontSize * SAMPLE_ASCENT_RATIO;
  const bottom = run.baseline + run.descent;
  let worst = null;
  const ys = samplePositions(top, bottom);
  const xs = samplePositions(run.left, run.right);
  for (const y of ys) {
    for (const x of xs) {
      const avg = averageWindow(image, x, y);
      if (!avg) continue;
      const bgHex = rgbToHex(avg.r, avg.g, avg.b);
      const effective = blendOver(run.fill, bgHex, run.alpha);
      const ratio = contrastRatio(effective, bgHex);
      if (!worst || ratio < worst.ratio) worst = { ratio, background: bgHex };
    }
  }
  return worst;
}
function pixelContrastMessage(issue) {
  return `text "${issue.text}" has a pixel-sampled contrast ratio of ${issue.ratio.toFixed(2)}:1 against its image background (sampled ${issue.background}, target ${issue.required}:1) \u2014 this text sits directly on an image with no resolvable solid backing color; reposition it, add an opaque-enough scrim behind it, or recolor the text`;
}
function resolveRasterizer() {
  return getPlatform().rasterizeSvg ?? rasterizeSvgInBrowser;
}
async function pixelFindingsForPage(markup, page, slideId, rasterize) {
  const runs = __collectImageBackedTextRuns(markup);
  if (runs.length === 0) return [];
  const stripped = stripTextNodes(markup);
  const image = await rasterize(stripped, PIXEL_CANVAS_W, PIXEL_CANVAS_H);
  const findings = [];
  for (const run of runs) {
    const sampled = worstCaseSample(run, image);
    if (!sampled) continue;
    if (sampled.ratio < PIXEL_HARD_FINDING_MAX_RATIO) {
      const issue = {
        text: run.text,
        fill: run.fill,
        background: sampled.background,
        ratio: sampled.ratio,
        required: run.required,
        fontSize: run.fontSize
      };
      findings.push({
        page,
        ...slideId !== void 0 ? { slideId } : {},
        code: "low-contrast",
        message: pixelContrastMessage(issue),
        // `source: "pixels"` distinguishes this from an SVG-color-resolved
        // low-contrast finding's own `detail` shape (`ContrastIssue`,
        // `deck-audit.ts`) — same `code`, since both are the same category
        // of defect (text fails contrast against its real background), just
        // measured through a different, more reliable source for that
        // background's color.
        detail: { ...issue, source: "pixels" }
      });
    }
  }
  return findings;
}
var __pixelFindingsForPage = pixelFindingsForPage;
async function runPixelContrastAudit(ir, theme) {
  const boundTheme = resolveIrTheme(ir, theme);
  const rasterize = resolveRasterizer();
  const findings = [];
  for (let i = 0; i < ir.slides.length; i++) {
    const slide = ir.slides[i];
    if (slide.placeholder) continue;
    const page = i + 1;
    const slideId = slide.id;
    const markup = renderSlideSvg(ir, i, { theme: boundTheme });
    findings.push(...await pixelFindingsForPage(markup, page, slideId, rasterize));
  }
  return findings;
}
export {
  __pixelFindingsForPage,
  runPixelContrastAudit,
  stripTextNodes
};
//# sourceMappingURL=pixel-audit-7VTFWU2K.js.map