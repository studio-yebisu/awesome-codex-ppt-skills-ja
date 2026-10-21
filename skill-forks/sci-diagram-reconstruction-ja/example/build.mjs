// Portable SciDiagram PPTX build: 水循環の代表的な経路 (Studio Yebisu reconstruction test input).
// Runtime: Node.js 20+ and pptxgenjs 4.0.1 (explicit SCI_DIAGRAM_RUNTIME=pptxgenjs).
// Body follows assets/pptxgenjs-build-template.mjs from HututuWorks/sci-diagram-pptx
// at cc8f0030edf80eeab6e52849b8c39fe638466776; only data and label styling are adapted.
// Every visible element has exactly one owner: content retained inside an
// INSET must not also appear in NODES or EDGES. This source has no raster
// evidence, so INSETS is empty and every word and arrow is native.
// Run: node build.mjs [--overwrite]

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import PptxGenJS from "pptxgenjs";

const BUILD_DIR = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_PATH = path.join(BUILD_DIR, "editable.pptx");
const OVERWRITE = process.argv.includes("--overwrite");

const SOURCE = {
  file: "source.png",
  width: 1600,
  height: 900,
};

const SLIDE = {
  width: 13.333333,
  height: 7.5,
};

// Source palette and typography read from source.png. At this scale
// 1 source px = 0.6 pt (52/36/32/27 px -> 31.2/21.6/19.2/16.2 pt).
const FONT_FACE = "Yu Gothic";
const PALETTE = {
  heading: "163A4F",
  stroke: "1C5A78",
  fill: "EAF3FA",
  edgeLabel: "3A4F5E",
  footnote: "4A5C68",
};

// Standard editable objects only. Boxes are source-image pixel coordinates.
// role "semantic" = topology node; role "annotation" = standalone text that
// never participates in EDGES.
const NODES = [
  {
    id: "atmospheric-vapor",
    role: "semantic",
    type: "rect",
    text: "大気中の水蒸気",
    box: { x: 100, y: 220, w: 500, h: 140 },
    fill: PALETTE.fill,
    line: PALETTE.stroke,
    lineWidth: 1.8,
    fontFace: FONT_FACE,
    fontSize: 21.6,
    bold: true,
    color: PALETTE.heading,
    margin: 0,
  },
  {
    id: "cloud-droplets",
    role: "semantic",
    type: "rect",
    text: "雲の中の水滴",
    box: { x: 1000, y: 220, w: 500, h: 140 },
    fill: PALETTE.fill,
    line: PALETTE.stroke,
    lineWidth: 1.8,
    fontFace: FONT_FACE,
    fontSize: 21.6,
    bold: true,
    color: PALETTE.heading,
    margin: 0,
  },
  {
    id: "river-water",
    role: "semantic",
    type: "rect",
    text: "川の水",
    box: { x: 1000, y: 560, w: 500, h: 140 },
    fill: PALETTE.fill,
    line: PALETTE.stroke,
    lineWidth: 1.8,
    fontFace: FONT_FACE,
    fontSize: 21.6,
    bold: true,
    color: PALETTE.heading,
    margin: 0,
  },
  {
    id: "sea-lake-water",
    role: "semantic",
    type: "rect",
    text: "海・湖の水",
    box: { x: 100, y: 560, w: 500, h: 140 },
    fill: PALETTE.fill,
    line: PALETTE.stroke,
    lineWidth: 1.8,
    fontFace: FONT_FACE,
    fontSize: 21.6,
    bold: true,
    color: PALETTE.heading,
    margin: 0,
  },
  {
    id: "title",
    role: "annotation",
    type: "textbox",
    text: "水循環の代表的な経路",
    box: { x: 100, y: 54, w: 760, h: 72 },
    fontFace: FONT_FACE,
    fontSize: 31.2,
    bold: true,
    color: PALETTE.heading,
    margin: 0,
    align: "left",
  },
  {
    id: "footnote",
    role: "annotation",
    type: "textbox",
    text: "水の移動の一部のみを示す。量・時間・縮尺は表していない。",
    box: { x: 100, y: 767, w: 900, h: 48 },
    fontFace: FONT_FACE,
    fontSize: 16.2,
    bold: false,
    color: PALETTE.footnote,
    margin: 0,
    align: "left",
  },
];

// The array is the topology. Points are exact source-image pixel coordinates.
// A label is an edge annotation, never a node.
const EDGES = [
  {
    id: "vapor-to-cloud-condensation",
    from: "atmospheric-vapor",
    to: "cloud-droplets",
    direction: "forward",
    points: [
      { x: 600, y: 290 },
      { x: 1000, y: 290 },
    ],
    color: PALETTE.stroke,
    width: 1.8,
    label: "凝結",
    labelBox: { x: 752, y: 224, w: 96, h: 48 },
  },
  {
    id: "cloud-to-river-precipitation",
    from: "cloud-droplets",
    to: "river-water",
    direction: "forward",
    points: [
      { x: 1250, y: 360 },
      { x: 1250, y: 560 },
    ],
    color: PALETTE.stroke,
    width: 1.8,
    label: "降水",
    labelBox: { x: 1287, y: 436, w: 96, h: 48 },
  },
  {
    id: "river-to-sea-flow",
    from: "river-water",
    to: "sea-lake-water",
    direction: "forward",
    points: [
      { x: 1000, y: 630 },
      { x: 600, y: 630 },
    ],
    color: PALETTE.stroke,
    width: 1.8,
    label: "水の流れ",
    labelBox: { x: 720, y: 644, w: 160, h: 48 },
  },
  {
    id: "sea-to-vapor-evaporation",
    from: "sea-lake-water",
    to: "atmospheric-vapor",
    direction: "forward",
    points: [
      { x: 350, y: 560 },
      { x: 350, y: 360 },
    ],
    color: PALETTE.stroke,
    width: 1.8,
    label: "蒸発",
    labelBox: { x: 217, y: 436, w: 96, h: 48 },
  },
];

// Intrinsic raster evidence remains one local, replaceable image object.
// None exists in this source: every word and arrow is owned natively above.
const INSETS = [];

const SHAPE_TYPES = {
  rect: "rect",
  roundRect: "roundRect",
  ellipse: "ellipse",
  diamond: "diamond",
  textbox: "textbox",
};

const NODE_ROLES = new Set(["semantic", "annotation"]);

const EDGE_DIRECTIONS = new Set(["forward", "both", "none"]);

function fail(message) {
  throw new Error(`SciDiagram portable build: ${message}`);
}

function sourcePath(relativePath) {
  if (typeof relativePath !== "string" || !relativePath || path.isAbsolute(relativePath)) {
    fail("source assets must use non-empty paths relative to build.mjs");
  }
  const resolved = path.resolve(BUILD_DIR, relativePath);
  const relative = path.relative(BUILD_DIR, resolved);
  if (relative === ".." || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
    fail(`source asset escapes the build directory: ${relativePath}`);
  }
  if (!fs.existsSync(resolved) || !fs.statSync(resolved).isFile()) {
    fail(`missing source asset: ${relativePath}`);
  }
  return resolved;
}

function toSlidePoint(point) {
  return {
    x: (point.x / SOURCE.width) * SLIDE.width,
    y: (point.y / SOURCE.height) * SLIDE.height,
  };
}

function toSlideBox(box) {
  const origin = toSlidePoint(box);
  return {
    ...origin,
    w: (box.w / SOURCE.width) * SLIDE.width,
    h: (box.h / SOURCE.height) * SLIDE.height,
  };
}

function validatePortableMap() {
  if (!(SOURCE.width > 0 && SOURCE.height > 0)) fail("SOURCE dimensions must be positive");
  if (!(SLIDE.width > 0 && SLIDE.height > 0)) fail("SLIDE dimensions must be positive");

  const nodeIds = new Set();
  const semanticIds = new Set();
  for (const node of NODES) {
    if (!node.id || nodeIds.has(node.id)) fail(`duplicate or empty node id: ${node.id}`);
    if (!SHAPE_TYPES[node.type]) fail(`unsupported phase-one node type: ${node.type}`);
    if (!NODE_ROLES.has(node.role)) fail(`unsupported node role on ${node.id}: ${node.role}`);
    if (node.type === "textbox" && node.role !== "annotation") {
      fail(`textbox ${node.id} must be an annotation, not a topology node`);
    }
    nodeIds.add(node.id);
    if (node.role === "semantic") semanticIds.add(node.id);
  }

  const edgeIds = new Set();
  for (const edge of EDGES) {
    if (!edge.id || edgeIds.has(edge.id)) fail(`duplicate or empty edge id: ${edge.id}`);
    if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to)) {
      fail(`edge ${edge.id} references an unknown node`);
    }
    if (!semanticIds.has(edge.from) || !semanticIds.has(edge.to)) {
      fail(`edge ${edge.id} must connect semantic nodes, not annotations`);
    }
    if (!EDGE_DIRECTIONS.has(edge.direction)) fail(`unsupported direction on ${edge.id}`);
    if (!Array.isArray(edge.points) || edge.points.length < 2) {
      fail(`edge ${edge.id} needs an explicit path with at least two points`);
    }
    if (edge.label && !edge.labelBox) fail(`edge ${edge.id} label needs labelBox`);
    edgeIds.add(edge.id);
  }

  const insetIds = new Set();
  for (const inset of INSETS) {
    if (!inset.id || insetIds.has(inset.id)) fail(`duplicate or empty inset id: ${inset.id}`);
    if (inset.sourceOrientation !== "normalized") {
      fail(`${inset.id} requires an orientation-normalized source image`);
    }
    for (const key of ["sourceBox", "frameBox"]) {
      const box = inset[key];
      if (!box || !(box.w > 0 && box.h > 0)) fail(`${inset.id} has an invalid ${key}`);
    }
    sourcePath(inset.source);
    insetIds.add(inset.id);
  }
}

function addDirectedSegment(slide, startPx, endPx, options = {}) {
  const start = toSlidePoint(startPx);
  const end = toSlidePoint(endPx);
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const x = Math.min(start.x, end.x);
  const y = Math.min(start.y, end.y);

  slide.addShape("line", {
    x,
    y,
    w: Math.abs(dx),
    h: Math.abs(dy),
    flipH: dx < 0,
    flipV: dy < 0,
    objectName: options.objectName,
    line: {
      color: options.color ?? "3E4652",
      width: options.width ?? 1.5,
      dashType: options.dashType ?? "solid",
      beginArrowType: options.beginArrow ? "triangle" : "none",
      endArrowType: options.endArrow ? "triangle" : "none",
    },
  });
}

function connectExactPath(slide, edge, direction = edge.direction) {
  const lastSegment = edge.points.length - 2;
  for (let index = 0; index <= lastSegment; index += 1) {
    addDirectedSegment(slide, edge.points[index], edge.points[index + 1], {
      objectName: `Edge:${edge.id}:segment-${index + 1}`,
      beginArrow: direction === "both" && index === 0,
      endArrow: (direction === "forward" || direction === "both")
        && index === lastSegment,
      color: edge.color,
      width: edge.width,
      dashType: edge.dashType,
    });
  }
}

function connectOneWay(slide, edge) {
  connectExactPath(slide, edge, "forward");
}

function connectBothWays(slide, edge) {
  connectExactPath(slide, edge, "both");
}

function addEdgeLabel(slide, edge) {
  if (!edge.label) return;
  // The source keeps a plain white ground behind each relationship label.
  slide.addText(edge.label, {
    ...toSlideBox(edge.labelBox),
    objectName: `Edge-label:${edge.id}`,
    fontFace: FONT_FACE,
    fontSize: 19.2,
    bold: false,
    color: PALETTE.edgeLabel,
    margin: 0,
    align: "center",
    valign: "mid",
    fill: { color: "FFFFFF" },
    line: { color: "FFFFFF", transparency: 100 },
    breakLine: false,
  });
}

function addInset(slide, inset) {
  const frame = toSlideBox(inset.frameBox);
  const sourceSize = inset.sourceSize ?? { width: SOURCE.width, height: SOURCE.height };
  if (inset.sourceBox.x < 0 || inset.sourceBox.y < 0
    || inset.sourceBox.x + inset.sourceBox.w > sourceSize.width
    || inset.sourceBox.y + inset.sourceBox.h > sourceSize.height) {
    fail(`${inset.id} sourceBox exceeds its source image dimensions`);
  }

  // PptxGenJS 4.0.1 expresses crop offsets against a virtual full-image box,
  // while sizing.w/h become the displayed object size. Convert pixel crop
  // coordinates into that exact contract instead of passing pixels as inches.
  const virtualFullWidth = frame.w * (sourceSize.width / inset.sourceBox.w);
  const virtualFullHeight = frame.h * (sourceSize.height / inset.sourceBox.h);
  slide.addImage({
    path: sourcePath(inset.source),
    x: frame.x,
    y: frame.y,
    w: virtualFullWidth,
    h: virtualFullHeight,
    objectName: inset.id,
    altText: inset.altText ?? `Replaceable ${inset.role ?? "local"} inset`,
    sizing: {
      type: "crop",
      x: virtualFullWidth * (inset.sourceBox.x / sourceSize.width),
      y: virtualFullHeight * (inset.sourceBox.y / sourceSize.height),
      w: frame.w,
      h: frame.h,
    },
  });
  slide.addShape("rect", {
    ...frame,
    objectName: `Inset-frame:${inset.id}`,
    fill: { color: "FFFFFF", transparency: 100 },
    line: { color: "6B7280", width: 1 },
  });
}

function addNode(slide, node) {
  const box = toSlideBox(node.box);
  const isTextbox = node.type === "textbox";
  // A standalone textbox (title, footnote) has no filled plate.
  if (!isTextbox) {
    slide.addShape(SHAPE_TYPES[node.type], {
      ...box,
      objectName: `Node:${node.id}`,
      fill: { color: node.fill ?? "FFFFFF" },
      line: { color: node.line ?? "5B6472", width: node.lineWidth ?? 1.25 },
    });
  }
  slide.addText(node.text, {
    ...box,
    objectName: isTextbox ? `Annotation:${node.id}` : `Node-label:${node.id}`,
    fontFace: node.fontFace ?? "Arial",
    fontSize: node.fontSize ?? 17,
    bold: node.bold ?? true,
    color: node.color ?? "172033",
    margin: node.margin ?? 0.06,
    align: node.align ?? "center",
    valign: node.valign ?? "mid",
    breakLine: false,
  });
}

async function main() {
  if (fs.existsSync(OUTPUT_PATH) && !OVERWRITE) {
    fail("editable.pptx already exists; rerun with --overwrite only when replacement is intended");
  }
  validatePortableMap();

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: "SCI_SOURCE", width: SLIDE.width, height: SLIDE.height });
  pptx.layout = "SCI_SOURCE";
  pptx.author = "Studio Yebisu";
  pptx.subject = "Native editable scientific schematic";
  pptx.title = "水循環の代表的な経路";
  pptx.lang = "ja-JP";
  pptx.theme = {
    headFontFace: FONT_FACE,
    bodyFontFace: FONT_FACE,
    lang: "ja-JP",
  };

  const slide = pptx.addSlide();
  slide.background = { color: "FFFFFF" };

  // Connectors first: EDGES alone define the graph and its directions.
  for (const edge of EDGES) {
    if (edge.direction === "forward") connectOneWay(slide, edge);
    else if (edge.direction === "both") connectBothWays(slide, edge);
    else connectExactPath(slide, edge, "none");
    addEdgeLabel(slide, edge);
  }
  for (const inset of INSETS) addInset(slide, inset);
  for (const node of NODES) addNode(slide, node);

  await pptx.writeFile({ fileName: OUTPUT_PATH, compression: true });
  process.stdout.write(`${JSON.stringify({ output: "editable.pptx", slides: 1, runtime: "pptxgenjs" })}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
