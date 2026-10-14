#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const input = process.argv[2];

if (!input) {
  console.error('Usage: node validate_html_deck.mjs <deck-folder>');
  process.exit(2);
}

const root = path.resolve(input);
const required = ['index.html', 'styles.css', 'slides.js'];
const errors = [];
const warnings = [];

for (const filename of required) {
  if (!fs.existsSync(path.join(root, filename))) errors.push(`Missing required file: ${filename}`);
}

const indexPath = path.join(root, 'index.html');
let sectionTags = [];
if (!fs.existsSync(indexPath)) {
  printResult();
  process.exit(1);
}

const html = fs.readFileSync(indexPath, 'utf8');
sectionTags = [...html.matchAll(/<section\b[^>]*class=["'][^"']*\bslide\b[^"']*["'][^>]*>/gi)].map((match) => match[0]);

if (sectionTags.length === 0) errors.push('No slide sections found. Use <section class="slide" ...>.');

const ids = [];
for (const tag of sectionTags) {
  const id = tag.match(/\bdata-slide-id=["']([^"']+)["']/i)?.[1];
  const labelledBy = tag.match(/\baria-labelledby=["']([^"']+)["']/i)?.[1];
  if (!id) errors.push(`Slide is missing data-slide-id: ${tag.slice(0, 120)}`);
  else ids.push(id);
  if (!labelledBy) errors.push(`Slide is missing aria-labelledby: ${id ?? tag.slice(0, 80)}`);
  else if (!new RegExp(`\\bid=["']${escapeRegex(labelledBy)}["']`, 'i').test(html)) {
    errors.push(`aria-labelledby target does not exist: ${labelledBy}`);
  }
}

const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
for (const id of [...new Set(duplicates)]) errors.push(`Duplicate data-slide-id: ${id}`);

const remotePatterns = [
  /(?:src|href)=["']https?:\/\//i,
  /@import\s+(?:url\()?\s*["']?https?:\/\//i,
  /url\(\s*["']?https?:\/\//i,
  /\bfetch\s*\(\s*["']https?:\/\//i,
  /\bXMLHttpRequest\b/i,
];

const textFiles = required
  .map((filename) => path.join(root, filename))
  .filter((filename) => fs.existsSync(filename));

for (const filename of textFiles) {
  const content = fs.readFileSync(filename, 'utf8');
  for (const pattern of remotePatterns) {
    if (pattern.test(content)) errors.push(`Remote or network dependency in ${path.basename(filename)}: ${pattern}`);
  }
}

const localRefs = [...html.matchAll(/(?:src|href)=["']([^"'#?]+)["']/gi)]
  .map((match) => match[1])
  .filter((ref) => !/^(?:data:|mailto:|tel:|javascript:)/i.test(ref));

for (const ref of localRefs) {
  const resolved = path.resolve(root, decodeURIComponent(ref));
  if (!resolved.startsWith(root + path.sep) && resolved !== root) {
    errors.push(`Reference escapes deck folder: ${ref}`);
  } else if (!fs.existsSync(resolved)) {
    errors.push(`Missing local asset: ${ref}`);
  }
}

if (!/prefers-reduced-motion/i.test(readIfPresent(path.join(root, 'styles.css')))) {
  warnings.push('styles.css does not declare prefers-reduced-motion behavior.');
}
if (!/@media\s+print/i.test(readIfPresent(path.join(root, 'styles.css')))) {
  errors.push('styles.css is missing print styles.');
}
if (!/requestFullscreen|webkitRequestFullscreen/i.test(readIfPresent(path.join(root, 'slides.js')))) {
  warnings.push('slides.js does not expose fullscreen support.');
}
if (!/<html\b[^>]*lang=["']zh-Hant(?:-TW)?["']/i.test(html)) {
  warnings.push('Document language is not zh-Hant-TW.');
}

const hasFragments = /class=["'][^"']*\bfragment\b[^"']*["']/i.test(html);
if (hasFragments) {
  const styles = readIfPresent(path.join(root, 'styles.css'));
  const script = readIfPresent(path.join(root, 'slides.js'));
  if (!/data-step/i.test(html)) errors.push('Progressive reveal requires a [data-step] status element.');
  if (!/is-revealed/i.test(styles) || !/is-revealed/i.test(script)) {
    errors.push('Progressive reveal requires .is-revealed support in styles.css and slides.js.');
  }
  if (!/\.fragment[\s\S]*opacity:\s*1\s*!important/i.test(styles)) {
    errors.push('Print styles must force progressive-reveal fragments visible.');
  }
}

printResult();
process.exit(errors.length > 0 ? 1 : 0);

function readIfPresent(filename) {
  return fs.existsSync(filename) ? fs.readFileSync(filename, 'utf8') : '';
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function printResult() {
  console.log(`Deck: ${root}`);
  console.log(`Slides: ${sectionTags?.length ?? 0}`);
  for (const warning of warnings) console.log(`WARN: ${warning}`);
  for (const error of errors) console.error(`ERROR: ${error}`);
  console.log(errors.length === 0 ? 'VALIDATION_OK' : `VALIDATION_FAILED (${errors.length} errors)`);
}
