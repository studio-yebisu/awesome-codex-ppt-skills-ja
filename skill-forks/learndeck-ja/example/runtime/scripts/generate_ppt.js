#!/usr/bin/env node
/* Generate an HTML slide deck from a structured slide plan, then convert it to PPTX. */

const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const CONVERTER_VALUE_OPTIONS = new Set([
  "--slide-selector",
  "--chrome",
  "--ppt-width",
  "--ppt-height",
  "--font-face",
  "--viewport-width",
  "--viewport-height",
]);
const CONVERTER_BOOL_OPTIONS = new Set(["--keep-raw", "--no-preview"]);
const STYLE_NAMES = new Set(["clean", "academic", "warm", "bold", "dark"]);

function usage(exitCode = 0) {
  console.log(`Usage:
  generate_ppt.js --slides <slides.json> --out-dir <dir> [options]

Required:
  --slides <file>             Structured slide plan JSON
  --out-dir <dir>             Output directory

Options:
  --name <base>               Output basename, defaults to deck title or slides filename
  --html <file>               Generated HTML path, defaults to <out-dir>/<name>.html
  --html-only                 Generate HTML and skip PPTX conversion
  --style <name>              Visual style: clean, academic, warm, bold, dark
  --slide-selector <css>      Forwarded to converter, defaults to .slide
  --chrome <path>             Forwarded to converter
  --ppt-width <inches>        Forwarded to converter
  --ppt-height <inches>       Forwarded to converter
  --font-face <name>          Forwarded to converter
  --viewport-width <px>       Forwarded to converter
  --viewport-height <px>      Forwarded to converter
  --keep-raw                  Forwarded to converter
  --no-preview                Forwarded to converter
  --help                      Show this help

Slide plan shape:
  {
    "title": "Deck title",
    "subtitle": "Optional deck subtitle",
    "style": "clean",
    "slides": [
      { "layout": "cover", "title": "Title", "subtitle": "Subtitle" },
      { "title": "Agenda", "bullets": ["Point A", "Point B"] },
      { "layout": "steps", "title": "Process", "items": [{"title": "Step", "body": "Detail"}] },
      { "layout": "compare", "title": "Options", "columns": [{"title": "A", "bullets": ["..."]}] },
      { "layout": "summary", "title": "Takeaways", "cards": [{"title": "One", "body": "..."}] }
    ]
  }
`);
  process.exit(exitCode);
}

function parseArgs(argv) {
  const opts = { converterArgs: [] };
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`Missing value for ${arg}`);
      return argv[++i];
    };
    if (arg === "--help" || arg === "-h") usage(0);
    else if (arg === "--slides") opts.slides = next();
    else if (arg === "--out-dir") opts.outDir = next();
    else if (arg === "--name") opts.name = next();
    else if (arg === "--html") opts.html = next();
    else if (arg === "--html-only") opts.htmlOnly = true;
    else if (arg === "--style") opts.style = next();
    else if (CONVERTER_VALUE_OPTIONS.has(arg)) opts.converterArgs.push(arg, next());
    else if (CONVERTER_BOOL_OPTIONS.has(arg)) opts.converterArgs.push(arg);
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!opts.slides) throw new Error("--slides is required");
  if (!opts.outDir) throw new Error("--out-dir is required");
  return opts;
}

function resolveStyle(value) {
  const style = text(value || "clean").trim().toLowerCase();
  if (!STYLE_NAMES.has(style)) {
    throw new Error(`Unknown style "${value}". Use one of: ${[...STYLE_NAMES].join(", ")}`);
  }
  return style;
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (err) {
    throw new Error(`Failed to read slide plan JSON: ${file}\n${err.message}`);
  }
}

function asArray(value) {
  if (Array.isArray(value)) return value;
  if (value == null) return [];
  return [value];
}

function text(value, fallback = "") {
  if (value == null) return fallback;
  return String(value);
}

function escapeHtml(value) {
  return text(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function safeName(value) {
  return text(value, "deck")
    .trim()
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "deck";
}

function normalizeDeck(raw, sourceFile) {
  const deck = Array.isArray(raw) ? { slides: raw } : { ...raw };
  deck.slides = asArray(deck.slides);
  if (!deck.slides.length) throw new Error("Slide plan must contain at least one slide.");
  deck.title = text(deck.title || deck.slides[0].title || path.basename(sourceFile, path.extname(sourceFile)), "Deck");
  deck.subtitle = text(deck.subtitle || deck.slides[0].subtitle || deck.slides[0].body || "");
  return deck;
}

function paragraph(value) {
  const body = text(value);
  if (!body) return "";
  return `<p>${escapeHtml(body)}</p>`;
}

function renderBullets(items) {
  const bullets = asArray(items).filter((item) => text(item).trim());
  if (!bullets.length) return "";
  return `<ul class="bullets">${bullets.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderMetrics(metrics) {
  const list = asArray(metrics).slice(0, 3);
  if (!list.length) return "";
  return `<div class="metrics">${list.map((m, i) => `
    <div class="metric metric-${i + 1}">
      <div class="metric-value">${escapeHtml(m.value || m.number || "")}</div>
      <div class="metric-label">${escapeHtml(m.label || m.title || "")}</div>
      ${paragraph(m.note || m.body)}
    </div>`).join("")}</div>`;
}

function renderItems(slide, label) {
  const items = asArray(slide.items || slide.cards).slice(0, 4);
  if (!items.length) return "";
  return `<div class="${label}">${items.map((item, i) => `
    <article class="item-card">
      <div class="item-index">${String(i + 1).padStart(2, "0")}</div>
      <h3>${escapeHtml(item.title || item.label || `Item ${i + 1}`)}</h3>
      ${paragraph(item.body || item.note || item.description)}
    </article>`).join("")}</div>`;
}

function renderColumns(slide) {
  const columns = asArray(slide.columns).slice(0, 3);
  if (!columns.length) return "";
  return `<div class="columns columns-${columns.length}">${columns.map((col) => `
    <section class="column">
      <h3>${escapeHtml(col.title || col.label || "")}</h3>
      ${paragraph(col.body || col.note)}
      ${renderBullets(col.bullets || col.items)}
    </section>`).join("")}</div>`;
}

function inferLayout(slide, index) {
  if (slide.layout) return slide.layout;
  if (index === 0 && !slide.bullets && !slide.items && !slide.cards && !slide.columns) return "cover";
  if (slide.columns) return "compare";
  if (slide.items) return "steps";
  if (slide.cards) return "summary";
  return "content";
}

function renderSlide(slide, index, total) {
  const layout = inferLayout(slide, index);
  const tone = slide.tone || (layout === "summary" || slide.dark ? "dark" : (index % 2 ? "alt" : "light"));
  const kicker = slide.kicker || `PAGE ${String(index + 1).padStart(2, "0")} / ${String(total).padStart(2, "0")}`;
  const title = slide.title || `Slide ${index + 1}`;
  const subtitle = slide.subtitle || slide.body || "";
  const footer = slide.footer || "";

  if (layout === "cover") {
    return `<section class="slide ${tone} cover">
      <div class="accent accent-a"></div><div class="accent accent-b"></div>
      <div class="kicker">${escapeHtml(kicker)}</div>
      <h1 class="title">${escapeHtml(title)}</h1>
      <p class="subtitle">${escapeHtml(subtitle)}</p>
      <div class="cover-panel">
        <div class="panel-label">${escapeHtml(slide.panelTitle || "Key Signals")}</div>
        ${renderMetrics(slide.metrics || [
          { value: String(total).padStart(2, "0"), label: "slides", note: "Generated from HTML" },
          { value: "HTML", label: "source", note: "Browser-positioned layout" },
          { value: "PPTX", label: "output", note: "Editable objects" },
        ])}
      </div>
      ${footer ? `<div class="footer">${escapeHtml(footer)}</div>` : ""}
    </section>`;
  }

  if (layout === "steps") {
    return `<section class="slide ${tone}">
      <div class="accent accent-a"></div><div class="accent accent-c"></div>
      <div class="kicker">${escapeHtml(kicker)}</div>
      <h2 class="title">${escapeHtml(title)}</h2>
      <p class="subtitle">${escapeHtml(subtitle)}</p>
      ${renderItems(slide, "steps")}
      ${footer ? `<div class="footer">${escapeHtml(footer)}</div>` : ""}
    </section>`;
  }

  if (layout === "compare") {
    return `<section class="slide ${tone}">
      <div class="accent accent-b"></div><div class="accent accent-c"></div>
      <div class="kicker">${escapeHtml(kicker)}</div>
      <h2 class="title">${escapeHtml(title)}</h2>
      <p class="subtitle">${escapeHtml(subtitle)}</p>
      ${renderColumns(slide)}
      ${footer ? `<div class="footer">${escapeHtml(footer)}</div>` : ""}
    </section>`;
  }

  if (layout === "summary") {
    return `<section class="slide dark">
      <div class="accent accent-a"></div><div class="accent accent-b"></div>
      <div class="kicker">${escapeHtml(kicker)}</div>
      <h2 class="title">${escapeHtml(title)}</h2>
      <p class="subtitle">${escapeHtml(subtitle)}</p>
      ${renderItems(slide, "summary-cards")}
      <div class="badge">${escapeHtml(slide.badge || "READY")}</div>
      ${footer ? `<div class="footer">${escapeHtml(footer)}</div>` : ""}
    </section>`;
  }

  return `<section class="slide ${tone}">
    <div class="accent accent-a"></div><div class="accent accent-b"></div>
    <div class="kicker">${escapeHtml(kicker)}</div>
    <h2 class="title">${escapeHtml(title)}</h2>
    <p class="subtitle">${escapeHtml(subtitle)}</p>
    <div class="content-grid">
      <div class="content-panel">
        ${renderBullets(slide.bullets)}
      </div>
      <div class="side-panel">
        ${renderMetrics(slide.metrics)}
        ${renderItems(slide, "mini-cards")}
      </div>
    </div>
    ${footer ? `<div class="footer">${escapeHtml(footer)}</div>` : ""}
  </section>`;
}

function renderHtml(deck, styleName) {
  const total = deck.slides.length;
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(deck.title)}</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #dde3ee;
    color: #172033;
    font-family: "PingFang SC", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  .slide {
    width: 1280px;
    height: 720px;
    position: relative;
    overflow: hidden;
    margin: 0 auto 28px;
    background: #fbfcff;
  }
  .slide.alt { background: #f7fbfa; }
  .slide.dark { background: #111827; color: #f8fafc; }
  .accent { position: absolute; border-radius: 50%; opacity: .7; }
  .accent-a { width: 520px; height: 520px; left: -180px; top: -220px; background: #bfdbfe; }
  .accent-b { width: 470px; height: 470px; right: -160px; bottom: -210px; background: #fecaca; }
  .accent-c { width: 420px; height: 420px; right: 80px; top: -230px; background: #99f6e4; }
  .dark .accent-a { background: rgba(59, 130, 246, .42); }
  .dark .accent-b { background: rgba(20, 184, 166, .34); }
  .dark .accent-c { background: rgba(244, 114, 182, .24); }
  .kicker {
    position: absolute; left: 64px; top: 44px;
    height: 30px; padding: 6px 12px; border-radius: 8px;
    background: #eef2ff; border: 1px solid #dbe4ff;
    color: #4f46e5; font-size: 13px; font-weight: 800;
  }
  .dark .kicker { background: rgba(255,255,255,.12); border-color: rgba(255,255,255,.18); color: #bfdbfe; }
  .title {
    position: absolute; left: 64px; top: 96px; width: 780px;
    font-size: 46px; line-height: 1.15; font-weight: 900;
  }
  .cover .title { top: 118px; width: 760px; font-size: 58px; }
  .subtitle {
    position: absolute; left: 64px; top: 178px; width: 740px;
    color: #64748b; font-size: 19px; line-height: 1.65;
  }
  .cover .subtitle { top: 275px; width: 710px; font-size: 22px; }
  .dark .subtitle { color: #cbd5e1; }
  .cover-panel {
    position: absolute; right: 64px; top: 104px; width: 370px; height: 464px;
    padding: 24px; border-radius: 8px; background: #ffffff;
    border: 1px solid #e7edf5; box-shadow: 0 18px 42px -26px rgba(15,23,42,.46);
  }
  .panel-label { color: #475569; font-size: 14px; font-weight: 800; margin-bottom: 16px; }
  .metrics { display: flex; gap: 16px; }
  .cover-panel .metrics { display: block; }
  .metric {
    width: 240px; min-height: 130px; padding: 18px; border-radius: 8px;
    color: #ffffff; background: #2563eb;
  }
  .cover-panel .metric { width: 100%; margin-bottom: 14px; min-height: 112px; }
  .metric-2 { background: #0f766e; }
  .metric-3 { background: #be4b49; }
  .metric-value { font-size: 38px; line-height: 1; font-weight: 900; }
  .metric-label { margin-top: 8px; font-size: 16px; font-weight: 800; }
  .metric p { margin-top: 8px; color: rgba(255,255,255,.9); font-size: 13px; line-height: 1.45; }
  .content-grid {
    position: absolute; left: 64px; top: 246px; width: 1152px;
    display: grid; grid-template-columns: 1fr 448px; gap: 28px;
  }
  .content-panel, .side-panel, .column, .item-card {
    border-radius: 8px; background: #ffffff; border: 1px solid #e7edf5;
    box-shadow: 0 16px 34px -26px rgba(15,23,42,.42);
  }
  .content-panel { min-height: 332px; padding: 26px 30px; }
  .side-panel { min-height: 332px; padding: 22px; }
  .bullets { list-style: none; }
  .bullets li {
    position: relative; padding-left: 24px; margin-bottom: 18px;
    color: #334155; font-size: 22px; line-height: 1.45; font-weight: 700;
  }
  .bullets li::before {
    content: ""; position: absolute; left: 0; top: 11px;
    width: 9px; height: 9px; border-radius: 50%; background: #2563eb;
  }
  .mini-cards { display: grid; gap: 14px; }
  .mini-cards .item-card { min-height: 92px; padding: 16px; box-shadow: none; }
  .steps, .summary-cards {
    position: absolute; left: 64px; top: 250px; width: 1152px;
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px;
  }
  .summary-cards { grid-template-columns: repeat(3, 1fr); }
  .item-card { min-height: 224px; padding: 22px; }
  .summary-cards .item-card {
    min-height: 235px; background: rgba(255,255,255,.10);
    border-color: rgba(255,255,255,.16); color: #f8fafc; box-shadow: none;
  }
  .item-index {
    width: 44px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center;
    background: #dbeafe; color: #1d4ed8; font-size: 15px; font-weight: 900;
  }
  .summary-cards .item-index { background: rgba(255,255,255,.16); color: #bfdbfe; }
  .item-card h3 { margin-top: 20px; font-size: 24px; line-height: 1.2; }
  .item-card p { margin-top: 12px; color: #64748b; font-size: 15px; line-height: 1.65; }
  .summary-cards .item-card p { color: #cbd5e1; }
  .columns {
    position: absolute; left: 64px; top: 246px; width: 1152px;
    display: grid; gap: 22px;
  }
  .columns-2 { grid-template-columns: repeat(2, 1fr); }
  .columns-3 { grid-template-columns: repeat(3, 1fr); }
  .column { min-height: 340px; padding: 26px; }
  .column h3 { font-size: 28px; margin-bottom: 18px; }
  .column p { color: #64748b; font-size: 17px; line-height: 1.55; margin-bottom: 16px; }
  .column .bullets li { font-size: 18px; margin-bottom: 14px; }
  .badge {
    position: absolute; right: 64px; bottom: 50px; padding: 10px 18px;
    border-radius: 8px; background: #14b8a6; color: #fff; font-size: 15px; font-weight: 900;
  }
  .footer {
    position: absolute; left: 64px; bottom: 30px; color: #64748b;
    font-size: 14px; font-weight: 800;
  }
  .dark .footer { color: #94a3b8; }

  body.theme-academic {
    background: #d8e1ec;
    font-family: Georgia, "Times New Roman", "PingFang SC", serif;
  }
  body.theme-academic .slide:not(.dark) { background: #f8fafc; }
  body.theme-academic .accent-a { background: #c7d2fe; }
  body.theme-academic .accent-b { background: #fde68a; }
  body.theme-academic .accent-c { background: #bae6fd; }
  body.theme-academic .kicker { background: #eff6ff; color: #1e3a8a; border-color: #bfdbfe; }
  body.theme-academic .metric { background: #1e3a8a; }
  body.theme-academic .metric-2 { background: #365314; }
  body.theme-academic .metric-3 { background: #92400e; }
  body.theme-academic .bullets li::before { background: #1e3a8a; }

  body.theme-warm { background: #eadfd3; }
  body.theme-warm .slide:not(.dark) { background: #fff7ed; }
  body.theme-warm .accent-a { background: #fed7aa; }
  body.theme-warm .accent-b { background: #fecaca; }
  body.theme-warm .accent-c { background: #fde68a; }
  body.theme-warm .kicker { background: #ffedd5; color: #9a3412; border-color: #fed7aa; }
  body.theme-warm .metric { background: #c2410c; }
  body.theme-warm .metric-2 { background: #b45309; }
  body.theme-warm .metric-3 { background: #be123c; }
  body.theme-warm .bullets li::before { background: #ea580c; }
  body.theme-warm .badge { background: #ea580c; }

  body.theme-bold { background: #dbeafe; }
  body.theme-bold .slide:not(.dark) { background: #f8fafc; }
  body.theme-bold .accent-a { background: #a5b4fc; }
  body.theme-bold .accent-b { background: #f0abfc; }
  body.theme-bold .accent-c { background: #67e8f9; }
  body.theme-bold .kicker { background: #ede9fe; color: #6d28d9; border-color: #c4b5fd; }
  body.theme-bold .metric { background: #7c3aed; }
  body.theme-bold .metric-2 { background: #0284c7; }
  body.theme-bold .metric-3 { background: #f97316; }
  body.theme-bold .bullets li::before { background: #7c3aed; }
  body.theme-bold .badge { background: #7c3aed; }

  body.theme-dark { background: #020617; }
  body.theme-dark .slide:not(.dark) { background: #0f172a; color: #f8fafc; }
  body.theme-dark .slide:not(.dark) .title { color: #f8fafc; }
  body.theme-dark .slide:not(.dark) .subtitle,
  body.theme-dark .slide:not(.dark) .footer,
  body.theme-dark .slide:not(.dark) .panel-label,
  body.theme-dark .slide:not(.dark) .column p,
  body.theme-dark .slide:not(.dark) .item-card p,
  body.theme-dark .slide:not(.dark) .bullets li { color: #cbd5e1; }
  body.theme-dark .slide:not(.dark) .cover-panel,
  body.theme-dark .slide:not(.dark) .content-panel,
  body.theme-dark .slide:not(.dark) .side-panel,
  body.theme-dark .slide:not(.dark) .column,
  body.theme-dark .slide:not(.dark) .item-card {
    background: #111827;
    border-color: #334155;
    box-shadow: none;
  }
  body.theme-dark .accent-a { background: rgba(59,130,246,.34); }
  body.theme-dark .accent-b { background: rgba(244,63,94,.28); }
  body.theme-dark .accent-c { background: rgba(20,184,166,.30); }
  body.theme-dark .kicker { background: rgba(255,255,255,.12); color: #bfdbfe; border-color: rgba(255,255,255,.18); }
</style>
</head>
<body class="theme-${styleName}">
${deck.slides.map((slide, index) => renderSlide(slide, index, total)).join("\n")}
</body>
</html>
`;
}

function writeHtml(deck, opts, baseName, styleName) {
  const outDir = path.resolve(opts.outDir);
  fs.mkdirSync(outDir, { recursive: true });
  const htmlPath = path.resolve(opts.html || path.join(outDir, `${baseName}.html`));
  fs.mkdirSync(path.dirname(htmlPath), { recursive: true });
  fs.writeFileSync(htmlPath, renderHtml(deck, styleName), "utf8");
  return htmlPath;
}

function convert(htmlPath, opts, baseName) {
  const converter = path.join(__dirname, "html_to_editable_pptx.js");
  const converterArgs = [
    converter,
    "--input", htmlPath,
    "--out-dir", path.resolve(opts.outDir),
    "--name", baseName,
    "--slide-selector", ".slide",
    ...opts.converterArgs,
  ];
  const result = spawnSync(process.execPath, converterArgs, {
    stdio: "inherit",
    env: process.env,
  });
  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    process.exit(result.status == null ? 1 : result.status);
  }
}

function main() {
  const opts = parseArgs(process.argv);
  const raw = readJson(opts.slides);
  const deck = normalizeDeck(raw, opts.slides);
  const styleName = resolveStyle(opts.style || deck.style);
  const baseName = safeName(opts.name || deck.name || deck.title || path.basename(opts.slides, path.extname(opts.slides)));
  const htmlPath = writeHtml(deck, opts, baseName, styleName);
  console.log(`Generated HTML: ${htmlPath}`);
  if (!opts.htmlOnly) convert(htmlPath, opts, baseName);
}

try {
  main();
} catch (err) {
  console.error(err.stack || err.message || String(err));
  process.exit(1);
}
