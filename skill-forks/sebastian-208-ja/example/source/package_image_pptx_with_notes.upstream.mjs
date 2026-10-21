#!/usr/bin/env node
import fs from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const require = createRequire(import.meta.url);

function loadPptxGenJS() {
  try {
    return require("pptxgenjs");
  } catch (initialError) {
    const searchRoots = (process.env.NODE_PATH ?? "").split(path.delimiter).filter(Boolean);
    for (const root of searchRoots) {
      const candidate = path.join(root, "pptxgenjs");
      if (fs.existsSync(candidate)) {
        return require(candidate);
      }
    }
    throw new Error(`Cannot load pptxgenjs. Run npm install pptxgenjs or set NODE_PATH. ${initialError.message}`);
  }
}

const PptxGenJS = loadPptxGenJS();

function usage() {
  return `Usage:
  node package_image_pptx_with_notes.mjs --images <image_pages_dir> --notes <qa/speaker-notes.md> --out <output.pptx> [--title <deck title>]

Notes format:
  # Speaker Notes
  ## Slide 01
  Presenter narration for slide 01.

  ## Slide 02
  Presenter narration for slide 02.
`;
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith("--")) throw new Error(`Unexpected argument: ${item}`);
    const key = item.slice(2);
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for --${key}`);
    args[key] = value;
    i += 1;
  }
  for (const key of ["images", "notes", "out"]) {
    if (!args[key]) throw new Error(`Missing required --${key}`);
  }
  return args;
}

function naturalImageSort(a, b) {
  const ax = a.match(/(\d+)/g)?.map(Number) ?? [];
  const bx = b.match(/(\d+)/g)?.map(Number) ?? [];
  for (let i = 0; i < Math.max(ax.length, bx.length); i += 1) {
    const av = ax[i] ?? 0;
    const bv = bx[i] ?? 0;
    if (av !== bv) return av - bv;
  }
  return a.localeCompare(b);
}

function listImages(imageDir) {
  const allowed = new Set([".png", ".jpg", ".jpeg", ".webp"]);
  return fs.readdirSync(imageDir)
    .filter((name) => allowed.has(path.extname(name).toLowerCase()))
    .sort(naturalImageSort)
    .map((name) => path.join(imageDir, name));
}

function parseNotes(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const notes = new Map();
  let current = null;
  let buffer = [];

  function flush() {
    if (current == null) return;
    const text = buffer.join("\n").trim();
    if (!text) throw new Error(`Slide ${String(current).padStart(2, "0")} has an empty speaker note`);
    notes.set(current, text);
  }

  for (const line of lines) {
    const match = line.match(/^#{1,3}\s*Slide\s+(\d+)\b/i);
    if (match) {
      flush();
      current = Number(match[1]);
      buffer = [];
    } else if (current != null) {
      buffer.push(line);
    }
  }
  flush();
  return notes;
}

async function main() {
  const args = parseArgs(process.argv);
  const imageDir = path.resolve(args.images);
  const notesPath = path.resolve(args.notes);
  const outPath = path.resolve(args.out);

  if (!fs.existsSync(imageDir)) throw new Error(`Image directory not found: ${imageDir}`);
  if (!fs.existsSync(notesPath)) throw new Error(`Notes file not found: ${notesPath}`);

  const images = listImages(imageDir);
  if (!images.length) throw new Error(`No slide images found in ${imageDir}`);

  const notes = parseNotes(fs.readFileSync(notesPath, "utf8"));
  if (notes.size !== images.length) {
    throw new Error(`Speaker notes count (${notes.size}) does not match image count (${images.length})`);
  }

  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "Academic Image PPT";
  pptx.subject = "Image-only academic PPTX with speaker notes";
  pptx.title = args.title ?? path.basename(outPath, path.extname(outPath));
  pptx.company = "Academic Image PPT";
  pptx.lang = "zh-CN";

  images.forEach((imagePath, index) => {
    const slideNumber = index + 1;
    const note = notes.get(slideNumber);
    if (!note) throw new Error(`Missing note for Slide ${String(slideNumber).padStart(2, "0")}`);
    const slide = pptx.addSlide();
    slide.background = { color: "FFFFFF" };
    slide.addImage({ path: imagePath, x: 0, y: 0, w: 13.333, h: 7.5 });
    slide.addNotes(note);
  });

  await pptx.writeFile({ fileName: outPath });
  console.log(`Created ${outPath}`);
  console.log(`Slides: ${images.length}`);
  console.log(`Speaker notes: ${notes.size}`);
}

main().catch((error) => {
  console.error(error.message);
  console.error(usage());
  process.exit(1);
});
