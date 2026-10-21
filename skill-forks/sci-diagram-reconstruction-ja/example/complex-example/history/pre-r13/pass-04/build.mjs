// Portable SciDiagram PPTX build — Studio Yebisu task complex-round12, pass-04 (explicit additional refinement request).
// Source: source.png (1600x900 PNG), concept schematic "2区画の可逆交換（概念モデル）".
// The source is a structure-check concept figure, not an experimental result.
// Derived from HututuWorks/sci-diagram-pptx assets/pptxgenjs-build-template.mjs
// (commit cc8f0030edf80eeab6e52849b8c39fe638466776). Only the data and the
// minimal adapters listed below were changed; the pixel->slide transform,
// relative asset resolution, overwrite refusal, direction helpers, and the
// srcRect crop path are kept from the template.
// Runtime: SCI_DIAGRAM_RUNTIME=pptxgenjs; host-probed pptxgenjs 4.0.1 on Node.js 24.18.
// Every visible element has exactly one owner: content retained inside an
// INSET must not also appear in NODES, EDGES, or TEXTS.
// Run (host, from this directory): node build.mjs [--overwrite]
//
// Adapters relative to the template:
// 1. NODES carry `parent`; containment is validated and plates are drawn
//    outer -> inner by nesting depth.
// 2. Container nodes place their label in `labelBox` (top-left heading)
//    instead of the plate centre.
// 3. TEXTS holds standalone native text (title, inset heading, notes). These
//    are not graph nodes and cannot be edge endpoints.
// 4. INSETS accept `borderBox`: the crop excludes the source border band and
//    the native frame is drawn on the source border position.
// 5. Draw order is node plates -> edges (+labels) -> insets -> texts. The
//    template order (edges -> insets -> nodes) would let the filled plates of
//    region-omega, compartment-a, and compartment-b hide the exchange line
//    (x 390-480 and 650-740) and the dashed regulation segment inside Ω
//    (x 1000-1070), so edges must sit above every plate.
// 6. Japanese font and language, zero text margins, no white edge-label patch.
// 8. RoundRect radii follow source SVG rx values; native triangle heads use OOXML lg/lg.
//    Run the shipped Python stdlib source/adjust_native_arrows.py after this build.
//    This additional authored pass follows an explicit continued-refinement request.
// 7. Ownership guard: no native box or edge segment may intersect an inset crop.

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
  width: 13.333,
  height: 7.5,
};

const FONT = "Yu Gothic";
const INK = "1D3B53";
const STROKE = "1F5272";
const MUTED_STROKE = "6E8798";

// Standard editable objects only. Boxes are source-image pixel coordinates.
// `parent` is the source nesting; null means a top-level object on the slide.
const NODES = [
  {
    id: "region-omega",
    cornerRadiusPx: 16,
    role: "container",
    parent: null,
    type: "roundRect",
    text: "反応領域 Ω",
    box: { x: 70, y: 185, w: 1000, h: 530 },
    labelBox: { x: 105, y: 212, w: 240, h: 34 },
    align: "left",
    fontSize: 19,
    fill: "F5F9FC",
    line: STROKE,
    lineWidth: 1.5,
  },
  {
    id: "compartment-a",
    cornerRadiusPx: 12,
    role: "container",
    parent: "region-omega",
    type: "roundRect",
    text: "区画 A",
    box: { x: 130, y: 290, w: 350, h: 330 },
    labelBox: { x: 165, y: 318, w: 200, h: 32 },
    align: "left",
    fontSize: 18,
    fill: "E9F1F8",
    line: MUTED_STROKE,
    lineWidth: 1,
  },
  {
    id: "compartment-b",
    cornerRadiusPx: 12,
    role: "container",
    parent: "region-omega",
    type: "roundRect",
    text: "区画 B",
    box: { x: 650, y: 290, w: 350, h: 330 },
    labelBox: { x: 685, y: 318, w: 200, h: 32 },
    align: "left",
    fontSize: 18,
    fill: "EDF2EC",
    line: MUTED_STROKE,
    lineWidth: 1,
  },
  {
    id: "species-x",
    cornerRadiusPx: 46,
    role: "state",
    parent: "compartment-a",
    type: "roundRect",
    text: "X",
    box: { x: 220, y: 440, w: 170, h: 92 },
    fontSize: 22,
    fill: "FFFFFF",
    line: STROKE,
    lineWidth: 1.75,
  },
  {
    id: "species-xr",
    cornerRadiusPx: 46,
    role: "state",
    parent: "compartment-b",
    type: "roundRect",
    text: "X·R",
    box: { x: 740, y: 440, w: 170, h: 92 },
    fontSize: 22,
    fill: "FFFFFF",
    line: STROKE,
    lineWidth: 1.75,
  },
  {
    id: "condition-u",
    cornerRadiusPx: 12,
    role: "condition",
    parent: null,
    type: "roundRect",
    text: "条件 u",
    box: { x: 1180, y: 160, w: 300, h: 80 },
    fontSize: 18,
    fill: "E9F2FA",
    line: STROKE,
    lineWidth: 1.75,
  },
];

// The array is the topology. Points are exact source-image pixel coordinates.
// A label is an edge annotation, never a node.
const EDGES = [
  {
    id: "exchange-x-xr",
    from: "species-x",
    to: "species-xr",
    direction: "both",
    semantics: "reversible exchange; solid line with arrowheads at both ends",
    points: [
      { x: 390, y: 486 },
      { x: 740, y: 486 },
    ],
    color: STROKE,
    width: 1.75,
    dashType: "solid",
    label: "可逆交換",
    labelBox: { x: 500, y: 414, w: 132, h: 32 },
    labelFontSize: 16,
    labelColor: "3D4B59",
  },
  {
    id: "regulation-u-b",
    from: "condition-u",
    to: "compartment-b",
    direction: "forward",
    semantics: "regulation of compartment B by condition u; dashed orthogonal polyline",
    points: [
      { x: 1180, y: 200 },
      { x: 1100, y: 200 },
      { x: 1100, y: 400 },
      { x: 1000, y: 400 },
    ],
    color: STROKE,
    width: 1.75,
    dashType: "dash",
    label: "調整",
    labelBox: { x: 1112, y: 284, w: 60, h: 30 },
    labelFontSize: 14,
    labelColor: "55636F",
  },
];

// Intrinsic raster content remains one local, replaceable image object.
// The crop starts 2 px inside the source border so the border is native only.
const INSETS = [
  {
    id: "replaceable-image-local-composite",
    source: "source.png",
    sourceBox: { x: 1182, y: 347, w: 296, h: 206 },
    frameBox: { x: 1182, y: 347, w: 296, h: 206 },
    borderBox: { x: 1181, y: 346, w: 298, h: 208 },
    borderColor: MUTED_STROKE,
    borderWidth: 1.25,
    role: "contextual synthetic composite input; not experimental evidence",
    owns: [
      "dark-to-light horizontal gradient field",
      "four light circular blobs",
      "internal text 参考パネル",
    ],
    altText: "局所像（合成入力）：差し替え可能な局所ラスター。内部文字「参考パネル」を含む",
    // PNG source; text reads upright. EXIF/eXIf orientation not byte-inspected by the author.
    sourceOrientation: "normalized",
  },
];

// Standalone native text. Not graph nodes; never edge endpoints.
const TEXTS = [
  {
    id: "title",
    text: "2区画の可逆交換（概念モデル）",
    box: { x: 70, y: 57, w: 780, h: 52 },
    fontSize: 26,
    bold: true,
    color: INK,
  },
  {
    id: "inset-heading",
    text: "局所像（合成入力）",
    describes: "replaceable-image-local-composite",
    box: { x: 1180, y: 297, w: 280, h: 32 },
    fontSize: 15,
    bold: true,
    color: INK,
  },
  {
    id: "note-purpose",
    text: "実験結果ではない構造確認用の入力。矢印と破線の関係をそのまま保持する。",
    box: { x: 70, y: 771, w: 1060, h: 34 },
    fontSize: 16,
    bold: false,
    color: "3D4B59",
  },
  {
    id: "note-legend",
    text: "双方向：可逆交換 ／ 破線：条件 u による区画 B の調整。強さや速度の値は示さない。",
    box: { x: 70, y: 816, w: 1060, h: 30 },
    fontSize: 15,
    bold: false,
    color: "6B7684",
  },
];

const SHAPE_TYPES = {
  rect: "rect",
  roundRect: "roundRect",
  ellipse: "ellipse",
  diamond: "diamond",
};

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

function boxWithin(inner, outer) {
  return inner.x >= outer.x && inner.y >= outer.y
    && inner.x + inner.w <= outer.x + outer.w
    && inner.y + inner.h <= outer.y + outer.h;
}

function boxesIntersect(a, b) {
  return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}

function segmentBox(start, end) {
  return {
    x: Math.min(start.x, end.x),
    y: Math.min(start.y, end.y),
    w: Math.abs(end.x - start.x),
    h: Math.abs(end.y - start.y),
  };
}

function nodeDepth(node, nodesById) {
  let depth = 0;
  let current = node;
  const seen = new Set();
  while (current.parent) {
    if (seen.has(current.id)) fail(`nesting cycle at ${current.id}`);
    seen.add(current.id);
    current = nodesById.get(current.parent);
    depth += 1;
  }
  return depth;
}

function validatePortableMap() {
  if (!(SOURCE.width > 0 && SOURCE.height > 0)) fail("SOURCE dimensions must be positive");
  if (!(SLIDE.width > 0 && SLIDE.height > 0)) fail("SLIDE dimensions must be positive");

  const nodeIds = new Set();
  for (const node of NODES) {
    if (!node.id || nodeIds.has(node.id)) fail(`duplicate or empty node id: ${node.id}`);
    if (!SHAPE_TYPES[node.type]) fail(`unsupported phase-one node type: ${node.type}`);
    nodeIds.add(node.id);
  }

  const nodesById = new Map(NODES.map((node) => [node.id, node]));
  for (const node of NODES) {
    if (node.parent) {
      const parent = nodesById.get(node.parent);
      if (!parent) fail(`node ${node.id} references an unknown parent`);
      if (!boxWithin(node.box, parent.box)) fail(`node ${node.id} is not inside ${node.parent}`);
    }
    if (node.labelBox && !boxWithin(node.labelBox, node.box)) {
      fail(`node ${node.id} labelBox leaves its plate`);
    }
    nodeDepth(node, nodesById);
  }

  const edgeIds = new Set();
  for (const edge of EDGES) {
    if (!edge.id || edgeIds.has(edge.id)) fail(`duplicate or empty edge id: ${edge.id}`);
    if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to)) {
      fail(`edge ${edge.id} references an unknown node`);
    }
    if (!EDGE_DIRECTIONS.has(edge.direction)) fail(`unsupported direction on ${edge.id}`);
    if (!Array.isArray(edge.points) || edge.points.length < 2) {
      fail(`edge ${edge.id} needs an explicit path with at least two points`);
    }
    if (edge.label && !edge.labelBox) fail(`edge ${edge.id} label needs labelBox`);
    edgeIds.add(edge.id);
  }

  const textIds = new Set();
  for (const text of TEXTS) {
    if (!text.id || textIds.has(text.id)) fail(`duplicate or empty text id: ${text.id}`);
    if (!text.box) fail(`text ${text.id} needs a box`);
    textIds.add(text.id);
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
    if (inset.borderBox && !boxWithin(inset.frameBox, inset.borderBox)) {
      fail(`${inset.id} borderBox must surround frameBox`);
    }
    sourcePath(inset.source);
    insetIds.add(inset.id);

    // One owner per visible element: native objects stay outside the crop.
    const nativeBoxes = [
      ...NODES.flatMap((node) => [
        [`node ${node.id}`, node.box],
        ...(node.labelBox ? [[`node label ${node.id}`, node.labelBox]] : []),
      ]),
      ...EDGES.flatMap((edge) => [
        ...edge.points.slice(1).map((end, index) => [
          `edge ${edge.id} segment ${index + 1}`,
          segmentBox(edge.points[index], end),
        ]),
        ...(edge.labelBox ? [[`edge label ${edge.id}`, edge.labelBox]] : []),
      ]),
      ...TEXTS.map((text) => [`text ${text.id}`, text.box]),
    ];
    for (const [owner, box] of nativeBoxes) {
      if (boxesIntersect(box, inset.sourceBox) || boxesIntersect(box, inset.frameBox)) {
        fail(`${owner} overlaps raster-owned ${inset.id}`);
      }
    }
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
  slide.addText(edge.label, {
    ...toSlideBox(edge.labelBox),
    objectName: `Edge-label:${edge.id}`,
    fontFace: FONT,
    fontSize: edge.labelFontSize ?? 14,
    color: edge.labelColor ?? "3E4652",
    margin: 0,
    align: "center",
    valign: "mid",
    // The source labels sit on open background; no white patch is drawn.
    ...(edge.labelFill ? { fill: { color: edge.labelFill } } : {}),
    wrap: false,
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
    ...toSlideBox(inset.borderBox ?? inset.frameBox),
    objectName: `Inset-frame:${inset.id}`,
    fill: { color: "FFFFFF", transparency: 100 },
    line: { color: inset.borderColor ?? "6B7280", width: inset.borderWidth ?? 1 },
  });
}

function addNode(slide, node) {
  const box = toSlideBox(node.box);
  slide.addShape(SHAPE_TYPES[node.type], {
    ...box,
    objectName: `Node:${node.id}`,
    rectRadius: node.cornerRadiusPx * Math.min(SLIDE.width / SOURCE.width, SLIDE.height / SOURCE.height),
    fill: { color: node.fill ?? "FFFFFF" },
    line: { color: node.line ?? "5B6472", width: node.lineWidth ?? 1.25 },
  });
  slide.addText(node.text, {
    ...(node.labelBox ? toSlideBox(node.labelBox) : box),
    objectName: `Node-label:${node.id}`,
    fontFace: node.fontFace ?? FONT,
    fontSize: node.fontSize ?? 17,
    bold: node.bold ?? true,
    color: node.color ?? INK,
    margin: 0,
    align: node.align ?? "center",
    valign: node.valign ?? "mid",
    wrap: false,
    breakLine: false,
  });
}

function addStandaloneText(slide, text) {
  slide.addText(text.text, {
    ...toSlideBox(text.box),
    objectName: `Text:${text.id}`,
    fontFace: FONT,
    fontSize: text.fontSize,
    bold: text.bold ?? false,
    color: text.color ?? INK,
    margin: 0,
    align: "left",
    valign: "mid",
    wrap: false,
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
  pptx.subject = "編集可能な科学模式図の再構成（構造確認用の概念図。実験結果ではない）";
  pptx.title = "2区画の可逆交換（概念モデル）";
  pptx.lang = "ja-JP";
  pptx.theme = {
    headFontFace: FONT,
    bodyFontFace: FONT,
    lang: "ja-JP",
  };

  const slide = pptx.addSlide();
  slide.background = { color: "FFFFFF" };

  // Plates first, outer -> inner, so a parent never covers its children.
  const nodesById = new Map(NODES.map((node) => [node.id, node]));
  const platesInOrder = NODES
    .map((node, index) => ({ node, index, depth: nodeDepth(node, nodesById) }))
    .sort((a, b) => a.depth - b.depth || a.index - b.index)
    .map((entry) => entry.node);
  for (const node of platesInOrder) addNode(slide, node);

  // Connectors above every plate: EDGES alone define the graph and its directions.
  for (const edge of EDGES) {
    if (edge.direction === "forward") connectOneWay(slide, edge);
    else if (edge.direction === "both") connectBothWays(slide, edge);
    else connectExactPath(slide, edge, "none");
    addEdgeLabel(slide, edge);
  }
  for (const inset of INSETS) addInset(slide, inset);
  for (const text of TEXTS) addStandaloneText(slide, text);

  await pptx.writeFile({ fileName: OUTPUT_PATH, compression: true });
  process.stdout.write(`${JSON.stringify({ output: "editable.pptx", slides: 1, runtime: "pptxgenjs" })}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
