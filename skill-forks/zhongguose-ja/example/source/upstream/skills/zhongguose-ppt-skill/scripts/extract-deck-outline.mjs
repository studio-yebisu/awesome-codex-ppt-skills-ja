#!/usr/bin/env node
// Regex-based outline extraction (no HTML parser). Relies on the template structure
// contract: slides are non-nested top-level <section> blocks, and .section-tabs
// contains only flat <span class="tab"> children (no nested <div>).
import fs from 'node:fs';
import path from 'node:path';

const target = process.argv[2];

if (!target) {
  console.error('Usage: node scripts/extract-deck-outline.mjs path/to/index.html');
  process.exit(2);
}

const file = path.resolve(target);

if (!fs.existsSync(file)) {
  console.error(`Deck not found: ${file}`);
  process.exit(2);
}

const html = fs.readFileSync(file, 'utf8');
const sections = [...html.matchAll(/<section\b([^>]*)>([\s\S]*?)<\/section>/gi)];

function attr(source, name) {
  const match = source.match(new RegExp(`${name}=["']([^"']+)["']`, 'i'));
  return match ? match[1] : '';
}

function clean(fragment) {
  return fragment
    .replace(/<script\b[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

function firstText(body, tag) {
  const match = body.match(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i'));
  return match ? clean(match[1]) : '';
}

function frameworkNav(body) {
  const navMatch = body.match(/<[^>]*\bclass=["'][^"']*\bsection-tabs\b[^"']*["'][^>]*>([\s\S]*?)<\/div>/i);
  if (!navMatch) return { active: '', labels: [] };
  const labels = [...navMatch[1].matchAll(/<[^>]*\bclass=["']([^"']*\btab\b[^"']*)["'][^>]*>([\s\S]*?)<\/[^>]+>/gi)]
    .map((match) => ({
      active: /\bactive\b/.test(match[1]),
      text: clean(match[2]),
    }))
    .filter((item) => item.text);
  return {
    active: labels.find((item) => item.active)?.text || '',
    labels: labels.map((item) => item.text),
  };
}

sections.forEach(([_, attrs, body], index) => {
  const page = String(index + 1).padStart(2, '0');
  const layout = attr(attrs, 'data-layout') || '-';
  const animate = attr(attrs, 'data-animate') || '-';
  const title = firstText(body, 'h1') || firstText(body, 'h2') || firstText(body, 'h3') || '-';
  const subtitle = firstText(body, 'p');
  const nav = frameworkNav(body);
  const chips = [...body.matchAll(/<(?:span|div)\b[^>]*class=["'][^"']*(?:tag|chip|badge|label|t-cat)[^"']*["'][^>]*>([\s\S]*?)<\/(?:span|div)>/gi)]
    .map((match) => clean(match[1]))
    .filter(Boolean)
    .slice(0, 4);

  const parts = [`${page}`, `layout=${layout}`, `animate=${animate}`, `title=${title}`];
  if (nav.active) {
    parts.push(`activeSection=${nav.active}`);
  }
  if (subtitle) {
    parts.push(`lead=${subtitle.slice(0, 90)}`);
  }
  if (chips.length > 0) {
    parts.push(`labels=${chips.join(' | ')}`);
  }
  console.log(parts.join(' :: '));
});
