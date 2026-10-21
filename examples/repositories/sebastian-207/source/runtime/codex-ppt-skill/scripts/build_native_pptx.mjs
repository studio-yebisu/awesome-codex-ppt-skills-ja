#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";

import { resolveStyle, applyTheme } from "../design-system/native/theme.mjs";
import { drawSlide, normalizeLayout } from "../design-system/native/layouts.mjs";
import { footer } from "../design-system/native/components.mjs";
import { addText } from "../design-system/native/typography.mjs";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");
const PPTX_CONST = new pptxgen();
const ShapeType = PPTX_CONST.ShapeType;

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

const specPath = arg("--spec", "spec_lock.json");
const slidesPath = arg("--slides", "slides_plan.json");
const assetPlanPath = arg("--asset-plan", null);
const notesPath = arg("--notes", null);
const referenceBoardPath = arg("--reference-board", null);
const styleCardPath = arg("--style-card", null);
const fontInventoryPath = arg("--font-inventory", null);
const output = arg("--output", "pptx/final.pptx");
const authoringOut = arg("--authoring", null);
const mode = arg("--mode", "native");

async function readJson(file, fallback = {}) {
  if (!file) return fallback;
  try {
    return JSON.parse((await fs.readFile(file, "utf8")).replace(/^\uFEFF/, ""));
  } catch {
    return fallback;
  }
}

function normalizePlanSlides(plan) {
  return (plan.slides || []).map((slide, idx, arr) => {
    const layout = normalizeLayout(slide, idx, arr.length);
    return {
      density: idx === 0 || idx === arr.length - 1 ? "low" : slide.density || slide.content_budget?.density || "medium",
      visual_role: slide.visual_role || (idx === 0 ? "cover_focus" : layout.includes("chart") ? "data_insight" : "content"),
      focal_point: slide.focal_point || slide.key_message || slide.title || "",
      contrast_with_previous: slide.contrast_with_previous || (idx === 0 ? "opening" : "layout and density shift"),
      repeated_motif: slide.repeated_motif || "accent hairline and stable title axis",
      section_color_state: slide.section_color_state || "default",
      ...slide,
      layout_archetype: layout,
    };
  });
}

function assetMap(assetPlan) {
  const assets = assetPlan.assets || assetPlan.slides || [];
  return new Map(assets.map((a) => [a.slide_id, a]));
}

function noteMap(notes) {
  return new Map((notes.slides || []).map((s) => [s.slide_id, s.notes || s.speaker_notes || ""]));
}

function drawImageFirstSlide(slide, asset, s, spec, style, idx, total) {
  slide.background = { color: style.bg };
  if (asset?.output_path) {
    try {
      slide.addImage({ path: asset.output_path, x: 0, y: 0, w: 13.333, h: 7.5, sizing: { type: "cover", w: 13.333, h: 7.5 } });
    } catch {
      slide.addShape(ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: style.surface2 }, line: { color: style.surface2 } });
    }
  } else {
    slide.addShape(ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: style.surface2 }, line: { color: style.surface2 } });
  }
  slide.addShape(ShapeType.rect, { x: 0, y: 0, w: 5.55, h: 7.5, fill: { color: style.bg, transparency: 8 }, line: { color: style.bg, transparency: 100 } });
  addText(slide, s.title || spec.title || spec.topic || "Image-first slide", { x: 0.72, y: 0.82, w: 4.25, h: 1.05 }, style, idx === 0 ? "coverTitle" : "slideTitle", { fontSize: idx === 0 ? 37 : 28, color: style.fg });
  addText(slide, s.key_message || s.purpose || "", { x: 0.76, y: 2.25, w: 4.1, h: 0.92 }, style, "body", { fontSize: 16.5, color: style.muted });
  footer(slide, idx + 1, total, style);
}

async function main() {
  const spec = await readJson(specPath, {});
  const plan = await readJson(slidesPath, { slides: [] });
  const assetPlan = await readJson(assetPlanPath, { assets: [] });
  const notes = await readJson(notesPath, { slides: [] });
  const referenceBoard = await readJson(referenceBoardPath, {});
  const styleCard = await readJson(styleCardPath, {});
  const fontInventory = await readJson(fontInventoryPath, null);
  const slides = normalizePlanSlides(plan);
  const assets = assetMap(assetPlan);
  const notesBySlide = noteMap(notes);

  const mergedSpec = {
    phase3_design_system: true,
    ...spec,
    reference_board: referenceBoard.primary_reference ? referenceBoard : spec.reference_board,
  };
  const style = await resolveStyle(mergedSpec, styleCard, fontInventory);
  const doc = new pptxgen();
  applyTheme(doc, style);
  doc.subject = mergedSpec.topic || "Generated presentation";
  doc.title = mergedSpec.title || mergedSpec.topic || "Generated presentation";

  slides.forEach((s, idx) => {
    const slide = doc.addSlide();
    const asset = assets.get(s.slide_id) || {};
    if (mode === "image_first" && asset.output_path) {
      drawImageFirstSlide(slide, asset, s, mergedSpec, style, idx, slides.length);
    } else {
      drawSlide(slide, ShapeType, s, { spec: mergedSpec, style, asset, idx, total: slides.length });
    }
    const notesText = notesBySlide.get(s.slide_id) || s.speaker_notes_seed || `本頁の説明：${s.title || ""}`;
    slide.addNotes(notesText);
  });

  await fs.mkdir(path.dirname(output), { recursive: true });
  await doc.writeFile({ fileName: output });
  if (authoringOut) {
    await fs.mkdir(path.dirname(authoringOut), { recursive: true });
    await fs.copyFile(new URL(import.meta.url), authoringOut);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
