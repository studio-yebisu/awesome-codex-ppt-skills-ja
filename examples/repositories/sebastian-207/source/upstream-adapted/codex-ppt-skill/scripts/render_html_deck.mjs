#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const html = process.argv[2];
const outIndex = process.argv.indexOf("--outdir");
const outdir = outIndex >= 0 ? process.argv[outIndex + 1] : "preview";

if (!html) {
  console.error("Usage: render_html_deck.mjs <deck.html> [--outdir preview]");
  process.exit(1);
}

fs.mkdirSync(outdir, { recursive: true });
const report = { input: html, outdir, screenshots: [], pdf: null, dom_issues: [], warnings: [], errors: [] };

async function loadPlaywright() {
  try {
    return await import("playwright");
  } catch (error) {
    const bundled = "C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js";
    if (fs.existsSync(bundled)) return await import(`file:///${bundled.replaceAll("\\", "/")}`);
    throw error;
  }
}

function fallbackChromium(expected) {
  if (expected && fs.existsSync(expected)) return expected;
  const bundled = "C:/Users/Administrator/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe";
  return fs.existsSync(bundled) ? bundled : undefined;
}

let browser;
try {
  const { chromium } = await loadPlaywright();
  const executablePath = fallbackChromium(chromium.executablePath());
  if (!executablePath) throw new Error(`Chromium executable missing. Expected ${chromium.executablePath()}`);
  browser = await chromium.launch({ executablePath, headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(`file:///${path.resolve(html).replaceAll("\\", "/")}`);
  await page.emulateMedia({ media: "screen" });
  const sections = await page.locator("section[data-slide-id]").count();
  if (sections === 0) report.errors.push("No slide sections found.");
  for (let i = 0; i < sections; i += 1) {
    const locator = page.locator("section[data-slide-id]").nth(i);
    const slideId = await locator.getAttribute("data-slide-id");
    const bbox = await locator.boundingBox();
    if (!bbox) {
      report.errors.push(`Slide ${i + 1} has no bounding box.`);
      continue;
    }
    const output = path.join(outdir, `slide_${String(i + 1).padStart(2, "0")}.png`);
    await locator.screenshot({ path: output });
    report.screenshots.push(output);
    const issues = await locator.evaluate((section) => {
      const result = [];
      const root = section.getBoundingClientRect();
      const visible = [...section.querySelectorAll("*")].filter((el) => {
        const style = getComputedStyle(el);
        return style.display !== "none" && style.visibility !== "hidden" && el.getAttribute("hidden") === null;
      });
      for (const el of visible) {
        const r = el.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) continue;
        if (r.left < root.left - 1 || r.top < root.top - 1 || r.right > root.right + 1 || r.bottom > root.bottom + 1) {
          result.push({ type: "overflow", tag: el.tagName, text: (el.textContent || "").slice(0, 60) });
        }
      }
      const overlapTargets = visible.filter((el) => {
        const tag = el.tagName;
        if (["IMG", "SVG", "CANVAS", "VIDEO"].includes(tag)) return true;
        const text = (el.textContent || "").trim();
        if (!text) return false;
        const visibleChildren = [...el.children].filter((child) => {
          const style = getComputedStyle(child);
          return style.display !== "none" && style.visibility !== "hidden" && child.getAttribute("hidden") === null;
        });
        return visibleChildren.length === 0;
      });
      for (let a = 0; a < overlapTargets.length; a += 1) {
        for (let b = a + 1; b < overlapTargets.length; b += 1) {
          if (overlapTargets[a].contains(overlapTargets[b]) || overlapTargets[b].contains(overlapTargets[a])) continue;
          const ra = overlapTargets[a].getBoundingClientRect();
          const rb = overlapTargets[b].getBoundingClientRect();
          const area = Math.max(0, Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left)) * Math.max(0, Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top));
          const minArea = Math.min(ra.width * ra.height, rb.width * rb.height);
          if (minArea > 1600 && area / minArea > 0.55) {
            result.push({ type: "overlap", a: overlapTargets[a].tagName, b: overlapTargets[b].tagName });
          }
        }
      }
      return result;
    });
    for (const issue of issues) report.dom_issues.push({ slide: slideId || i + 1, ...issue });
  }
  const pdf = path.join(outdir, "final.pdf");
  await page.pdf({ path: pdf, width: "1920px", height: `${1080 * Math.max(1, sections)}px`, printBackground: true });
  report.pdf = pdf;
  if (report.dom_issues.length) report.errors.push("DOM overflow/overlap issues detected.");
} catch (error) {
  report.errors.push(String(error && error.message ? error.message : error));
} finally {
  if (browser) await browser.close();
}

fs.writeFileSync(path.join(outdir, "render_report.json"), `${JSON.stringify(report, null, 2)}\n`, "utf8");
process.exit(report.errors.length ? 1 : 0);
