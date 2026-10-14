#!/usr/bin/env node
// Regex-based validation (no HTML parser). Relies on the template structure contract:
// slides are non-nested top-level <section class="slide ...">, the cover slide carries
// data-role="cover", and .section-tabs contains only flat <span class="tab"> children.
import fs from 'node:fs';
import path from 'node:path';

const target = process.argv[2];

if (!target) {
  console.error('Usage: node scripts/validate-deck.mjs path/to/index.html');
  process.exit(2);
}

const file = path.resolve(target);
const baseDir = path.dirname(file);
const errors = [];
const warnings = [];

if (!fs.existsSync(file)) {
  console.error(`Deck not found: ${file}`);
  process.exit(2);
}

const html = fs.readFileSync(file, 'utf8');
const slideSections = [...html.matchAll(/<section\b([^>]*)>([\s\S]*?)<\/section>/gi)]
  .filter((match) => /\bclass=["'][^"']*\bslide\b[^"']*["']/.test(match[1]));
const slideTags = slideSections.map((match) => match[1]);

if (slideTags.length === 0) {
  errors.push('No <section class="slide ..."> blocks found.');
}

// Slides marked data-role="cover" are exempt from framework-navigation checks.
// Decks without any explicit cover marker fall back to treating slide 1 as the cover.
const coverPattern = /\bdata-role=["']cover["']/;
const hasExplicitCover = slideTags.some((tag) => coverPattern.test(tag));

slideSections.forEach(([, tag, body], index) => {
  const n = index + 1;
  const isCover = hasExplicitCover ? coverPattern.test(tag) : index === 0;
  if (!/\bdata-layout=/.test(tag)) {
    errors.push(`Slide ${n} is missing data-layout.`);
  }
  if (!/\bdata-animate=/.test(tag)) {
    warnings.push(`Slide ${n} is missing data-animate.`);
  }
  if (!isCover) {
    if (!/\bclass=["'][^"']*\bsection-tabs\b[^"']*["']/.test(body)) {
      errors.push(`Slide ${n} is missing top-left framework navigation (.section-tabs).`);
    }
    const tabClasses = [...body.matchAll(/class=["']([^"']*\btab\b[^"']*)["']/gi)].map((match) => match[1]);
    const activeTabs = tabClasses.filter((className) => /\bactive\b/.test(className));
    if (tabClasses.length < 2) {
      errors.push(`Slide ${n} should show multiple framework navigation tabs.`);
    }
    if (activeTabs.length !== 1) {
      errors.push(`Slide ${n} should have exactly one active framework tab, found ${activeTabs.length}.`);
    }
  }
});

// One theme color per deck, applied via --accent. 飞泉绿 #497568 is the default;
// other theme colors from references/visual-system.md are allowed (warn for awareness).
const accentMatch = html.match(/--accent\s*:\s*([^;}]+)[;}]/);
if (!accentMatch) {
  errors.push('No --accent theme color variable found.');
} else if (!/#497568|rgb\(\s*73\s*,\s*117\s*,\s*104\s*\)/i.test(accentMatch[1])) {
  warnings.push(`Theme color is ${accentMatch[1].trim()} instead of the default 飞泉绿 #497568. Confirm the user chose this theme color.`);
}

for (const token of ['--zh-title', '--zh-body', '--latin-display']) {
  if (!html.includes(token)) {
    errors.push(`CSS variable ${token} was not found.`);
  }
}

if (/翻页/.test(html)) {
  errors.push('Visible lower-right "翻页" hint should be removed for this style.');
}

if (!/motion\.min\.js/.test(html)) {
  warnings.push('motion.min.js is not referenced. Confirm the deck has an intentional motion fallback.');
}

if (/\bdata-lucide=/.test(html) && !/lucide(?:\.min)?\.js/.test(html)) {
  warnings.push('data-lucide icons are used but no lucide script is referenced. Icons will not render.');
}

if (/<title>[^<]*中国色 PPT 模板[^<]*<\/title>/.test(html)) {
  warnings.push('Template default <title> (中国色 PPT 模板 · 示例) is still present. Replace it for a real deck.');
}

if (/replace-with-your-url/.test(html)) {
  warnings.push('Placeholder deploy link (replace-with-your-url) is still present. Set the real link or remove the element.');
}

const placeholderCopyCount = (html.match(/占位/g) || []).length;
if (placeholderCopyCount > 0) {
  warnings.push(`Placeholder copy ("占位") appears ${placeholderCopyCount} time(s). Replace all template copy for a real deck.`);
}

const localImages = [...html.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["']/gi)]
  .map((match) => match[1])
  .filter((src) => !/^(https?:|data:|blob:)/i.test(src));

const missingImages = [];
for (const src of localImages) {
  const clean = src.split('#')[0].split('?')[0].replace(/^\.\//, '');
  const candidate = path.resolve(baseDir, clean);
  if (!fs.existsSync(candidate)) {
    missingImages.push(src);
  }
}

if (missingImages.length > 0) {
  errors.push(`Missing local image assets: ${[...new Set(missingImages)].join(', ')}`);
}

const placeholderRefs = [...new Set(localImages.filter((src) => /placeholder-[^/\\]*\.svg/i.test(src)))];
if (placeholderRefs.length > 0) {
  warnings.push(`Template placeholder images are still referenced: ${placeholderRefs.join(', ')}. Replace them unless the deck is still a draft.`);
}

const absoluteLocalRefs = [...html.matchAll(/(?:src|href)=["']((?:[A-Za-z]:[\\/]|file:\/\/|\/(?:Users|home|mnt|tmp)\/)[^"']+)["']/g)].map((match) => match[1]);
if (absoluteLocalRefs.length > 0) {
  errors.push(`Absolute local asset paths are not shareable: ${[...new Set(absoluteLocalRefs)].join(', ')}`);
}

if (errors.length > 0) {
  console.error('Deck validation failed:');
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  if (warnings.length > 0) {
    console.error('Warnings:');
    for (const warning of warnings) {
      console.error(`- ${warning}`);
    }
  }
  process.exit(1);
}

for (const warning of warnings) {
  console.warn(`Warning: ${warning}`);
}

console.log(`Deck validation passed: ${slideTags.length} slide(s).`);
