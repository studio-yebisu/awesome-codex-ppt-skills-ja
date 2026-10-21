#!/usr/bin/env node
/*
Purpose: Validate a V1 fixed-stage HTML deck.
Input: HTML file path.
Output: JSON report for fixed stage, data attributes, placeholders, and missing local images.
Failure behavior: Report errors; exit 1 when invalid. Does not install dependencies.
*/

import fs from "node:fs";
import path from "node:path";

const file = process.argv[2];
const outputFlagIndex = process.argv.indexOf("--output");
const output = outputFlagIndex >= 0 ? process.argv[outputFlagIndex + 1] : null;

if (!file) {
  console.error("Usage: validate_html_deck.mjs <deck.html> [--output report.json]");
  process.exit(1);
}

const html = fs.readFileSync(file, "utf8");
const errors = [];
const warnings = [];

if (!/1920\s*px/.test(html) || !/1080\s*px/.test(html)) {
  warnings.push("fixed 1920x1080 stage not clearly declared");
}

const slideMatches = [...html.matchAll(/<section\b[^>]*>/gi)];
if (slideMatches.length === 0) errors.push("no <section> slides found");

const ids = new Set();
for (const [idx, match] of slideMatches.entries()) {
  const tag = match[0];
  const id = /data-slide-id=["']([^"']+)["']/i.exec(tag)?.[1];
  const layout = /data-layout=["']([^"']+)["']/i.exec(tag)?.[1];
  const density = /data-density=["']([^"']+)["']/i.exec(tag)?.[1];
  if (!id) errors.push(`slide ${idx + 1} missing data-slide-id`);
  if (!layout) errors.push(`slide ${idx + 1} missing data-layout`);
  if (!density) errors.push(`slide ${idx + 1} missing data-density`);
  if (id && ids.has(id)) errors.push(`duplicate data-slide-id: ${id}`);
  if (id) ids.add(id);
}

if (/(lorem|xxxx|todo|placeholder)/i.test(html)) {
  errors.push("placeholder-like text found");
}

const base = path.dirname(path.resolve(file));
for (const m of html.matchAll(/<img\b[^>]*src=["']([^"']+)["']/gi)) {
  const src = m[1];
  if (/^(https?:|data:)/i.test(src)) continue;
  const local = path.resolve(base, src);
  if (!fs.existsSync(local)) errors.push(`missing local image: ${src}`);
}

const report = { valid: errors.length === 0, errors, warnings, slide_count: slideMatches.length };
const text = JSON.stringify(report, null, 2);
if (output) {
  fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
  fs.writeFileSync(output, `${text}\n`, "utf8");
} else {
  console.log(text);
}
process.exit(report.valid ? 0 : 1);
