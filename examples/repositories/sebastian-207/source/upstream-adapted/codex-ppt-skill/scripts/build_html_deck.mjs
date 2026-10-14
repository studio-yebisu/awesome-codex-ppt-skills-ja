#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

const specPath = arg("--spec", "spec_lock.json");
const slidesPath = arg("--slides", "slides_plan.json");
const assetPlanPath = arg("--asset-plan", null);
const referenceBoardPath = arg("--reference-board", null);
const output = arg("--output", "html/index.html");

const SKILL_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function readJson(file, fallback = {}) {
  if (!file) return fallback;
  try {
    return JSON.parse((await fs.readFile(file, "utf8")).replace(/^\uFEFF/, ""));
  } catch {
    return fallback;
  }
}

async function readCss(name) {
  return fs.readFile(path.join(SKILL_DIR, "design-system", "html", name), "utf8");
}

function esc(s) {
  return String(s || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

function splitText(value) {
  if (Array.isArray(value)) return value.map(String).filter(Boolean);
  return String(value || "").replaceAll("；", "\n").replaceAll(";", "\n").split(/\n/).map((s) => s.trim()).filter(Boolean);
}

function assetMap(assetPlan) {
  const assets = assetPlan.assets || assetPlan.slides || [];
  return new Map(assets.map((asset) => [asset.slide_id, asset]));
}

function relAssetSrc(assetPath) {
  if (!assetPath) return "";
  const fromDir = path.dirname(path.resolve(output));
  return path.relative(fromDir, path.resolve(assetPath)).replaceAll("\\", "/");
}

async function fileExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

function color(value, fallback) {
  const v = String(value || fallback).trim();
  if (/^#[0-9a-fA-F]{6}$/.test(v)) return v;
  if (/^[0-9a-fA-F]{6}$/.test(v)) return `#${v}`;
  return fallback;
}

function normalizeLayout(s, idx, total) {
  const raw = String(s.layout_archetype || s.layout || s.layout_family || s.slide_type || "").toLowerCase();
  const known = new Set(["cover-hero", "cover-minimal", "cover-editorial", "agenda-clean", "section-divider", "statement-hero", "text-visual-60-40", "visual-text-40-60", "two-column-argument", "three-point-summary", "metric-hero", "kpi-row", "comparison", "before-after", "process-linear", "process-cycle", "timeline", "matrix", "chart-hero", "chart-with-insight", "case-study", "quote-editorial", "roadmap", "closing-echo"]);
  if (known.has(raw)) return raw;
  if (idx === 0) return "cover-hero";
  if (idx === total - 1) return "closing-echo";
  if (raw.includes("chart") || raw.includes("data")) return "chart-with-insight";
  if (raw.includes("process")) return "process-linear";
  return ["statement-hero", "text-visual-60-40", "three-point-summary", "chart-with-insight", "process-linear", "comparison"][idx % 6];
}

function visualLabelFor(asset = {}) {
  const type = String(asset.asset_type || asset.visual_role || "").toLowerCase();
  if (type.includes("cover") || type.includes("hero")) return "主题主视觉";
  if (type.includes("scenario") || type.includes("scene")) return "场景视觉";
  if (type.includes("product") || type.includes("system")) return "能力图解";
  if (type.includes("process") || type.includes("flow")) return "流程图解";
  if (type.includes("chart") || type.includes("data")) return "数据关系";
  if (type.includes("case") || type.includes("story")) return "案例画面";
  return "内容图解";
}

function renderVisual(s, asset, style = "") {
  const binding = asset?.semantic_binding || {};
  const title = binding.slide_title || s.title || "";
  const core = binding.core_message || s.key_message || s.purpose || splitText(s.body || s.points)[0] || "";
  const outputPath = asset?.output_path;
  if (outputPath) {
    return `<figure class="image-frame semantic-image ${esc(asset.integration_treatment || "split")}" style="${style}">
      <img src="${esc(relAssetSrc(outputPath))}" alt="${esc(title || core)}" />
    </figure>`;
  }
  const points = splitText(s.body || s.points || s.key_message).slice(0, 3).map((item, idx) => `<li><b>${idx + 1}</b><span>${esc(item)}</span></li>`).join("");
  return `<div class="semantic-visual" style="${style}">
    <div class="visual-label">${esc(visualLabelFor(asset))}</div>
    <div class="visual-message">${esc(core || title)}</div>
    <ol>${points}</ol>
  </div>`;
}

async function renderSlide(s, i, total, spec, asset) {
  const layout = normalizeLayout(s, i, total);
  const items = splitText(s.body || s.points || s.key_message || s.speaker_notes_seed).slice(0, 5);
  const density = s.density || s.content_budget?.density || (i === 0 || i === total - 1 ? "low" : "medium");
  const title = esc(s.title || spec.title || spec.topic || "");
  const purpose = esc(s.purpose || s.key_message || s.subtitle || "");
  if (layout.startsWith("cover") || layout === "closing-echo") {
    return `<section class="slide cover" data-slide-id="${esc(s.slide_id || `slide_${i + 1}`)}" data-layout="${layout}" data-density="${density}">
      <div class="kicker" style="position:absolute;left:112px;top:126px">${esc(spec.kicker || spec.use_case || "演示文稿")}</div>
      <h1 class="slide-title">${title}</h1>
      <p class="purpose" style="position:absolute;left:116px;top:510px;width:790px">${purpose}</p>
      ${renderVisual(s, asset, "position:absolute;right:126px;top:112px;width:610px;height:800px")}
      <div class="accent-band" style="left:118px;top:660px;width:180px;height:10px"></div>
      <div class="footer">${String(i + 1).padStart(2, "0")} / ${String(total).padStart(2, "0")}</div>
      <aside hidden>${esc(s.speaker_notes_seed || "")}</aside>
    </section>`;
  }
  const pointHtml = items.map((item, idx) => `<div class="point"><b>${idx + 1}</b><span>${esc(item)}</span></div>`).join("");
  const chartHtml = `<div class="shape-chart" style="position:absolute;right:124px;top:255px;width:700px;height:490px;padding:64px">
    <div class="metric">32%</div><div class="metric-label">关键指标提升</div>
    <div style="margin-top:64px"><div class="bar-muted" style="width:78%"></div><div class="bar" style="width:56%;margin-top:22px"></div></div>
    <p class="purpose" style="font-size:28px;margin-top:48px">图表结论直接写在页面上，默认图表样式被替换为形状化表达。</p>
  </div>`;
  return `<section class="slide" data-slide-id="${esc(s.slide_id || `slide_${i + 1}`)}" data-layout="${layout}" data-density="${density}">
    <h1 class="slide-title">${title}</h1>
    <div class="hairline"></div>
    <div class="insight" style="position:absolute;left:112px;top:235px;width:560px">${purpose || esc(items[0] || "")}</div>
    <div class="point-list" style="position:absolute;left:112px;top:415px;width:650px">${pointHtml}</div>
    ${layout.includes("chart") || layout.includes("metric") ? chartHtml : renderVisual(s, asset, "position:absolute;right:124px;top:245px;width:680px;height:515px")}
    <div class="footer">${String(i + 1).padStart(2, "0")} / ${String(total).padStart(2, "0")}</div>
    <aside hidden>${esc(s.speaker_notes_seed || "")}</aside>
  </section>`;
}

async function main() {
  const spec = await readJson(specPath, {});
  const plan = await readJson(slidesPath, { slides: [] });
  const assetPlan = await readJson(assetPlanPath, { assets: [] });
  const refBoard = await readJson(referenceBoardPath, {});
  const palette = spec.palette || {};
  const styleVars = {
    "--deck-bg": color(palette.bg || palette.background || refBoard.design_dna?.palette?.[0], "#F7F8FA"),
    "--deck-fg": color(palette.fg || palette.primary || refBoard.design_dna?.palette?.[1], "#111827"),
    "--deck-muted": color(palette.muted || palette.secondary, "#64748B"),
    "--deck-accent": color(palette.accent || refBoard.design_dna?.palette?.[2], "#2563EB"),
    "--deck-accent-2": color(palette.accent2, "#0F766E"),
    "--deck-surface": color(palette.surface, "#FFFFFF"),
    "--deck-surface-2": color(palette.surface2 || refBoard.design_dna?.palette?.[3], "#EEF2F7"),
    "--deck-line": color(palette.line, "#D6DEE8"),
    "--font-heading": `"${spec.fonts?.heading || "Microsoft YaHei UI"}", "DengXian", sans-serif`,
    "--font-body": `"${spec.fonts?.body || "Microsoft YaHei UI"}", "DengXian", sans-serif`,
  };
  const assets = assetMap(assetPlan);
  const css = `${await readCss("tokens.css")}\n${await readCss("layouts.css")}\n${await readCss("components.css")}\n${await readCss("charts.css")}\n${await readCss("imagery.css")}\n:root{${Object.entries(styleVars).map(([k, v]) => `${k}:${v}`).join(";")}}\n`;
  const slides = plan.slides || [];
  const normalizedAssets = new Map();
  for (const [slideId, asset] of assets.entries()) {
    if (!asset.output_path || await fileExists(asset.output_path)) normalizedAssets.set(slideId, asset);
    else normalizedAssets.set(slideId, { ...asset, output_path: "" });
  }
  const sections = (await Promise.all(slides.map((s, i) => renderSlide(s, i, slides.length, spec, normalizedAssets.get(s.slide_id) || {})))).join("\n");
  const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=1920,height=1080,initial-scale=1" />
  <title>${esc(spec.title || spec.topic || "HTML Deck")}</title>
  <style>${css}</style>
</head>
<body><main class="deck">${sections}</main></body></html>`;
  await fs.mkdir(path.dirname(output), { recursive: true });
  await fs.writeFile(output, html, "utf8");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
