import {
  BUILTIN_THEME_FILES,
  BrandSchema,
  CANONICAL_THEME_IDS,
  CAPACITY,
  COMPONENT_TYPES,
  CourseSchema,
  DeckBrandingSchema,
  FooterSchema,
  HexTokenSchema,
  KIND_LANDING,
  KIND_VALUES,
  MetaSchema,
  NarrativeProfileInputSchema,
  OVERFLOW_VOCABULARY_MESSAGE,
  PptwiseError,
  PptxIRSchema,
  RETIRED_THEME_IDS,
  SAFE_FONTS,
  THEME_ID_CONSTRAINT,
  THEME_ID_PATTERN,
  THEME_LABELS,
  THEME_OCCASIONS,
  THEME_REQUIRED_MESSAGE,
  ThemeFileSchema,
  assertContrastFloor,
  assertNotRetiredThemeId,
  compileThemeDefinition,
  contrastRatio,
  faceAcceptedComponentTypes,
  findOverflowVocabulary,
  foldedThemeTarget,
  foldedThemeWarning,
  footerSettingIssues,
  formatIssues,
  getInstalledThemeIds,
  getLayout,
  getThemeDefinition,
  hasExactWidthTable,
  hexToHsl,
  hexToOklch,
  hexToRgb,
  hslToHex,
  hueDelta,
  irJsonSchema,
  landingCandidates,
  mixHex,
  normalizeDeckRootAliases,
  normalizeNarrativeShape,
  offeredContentKinds,
  oklabDistance,
  oklchChroma,
  oklchToHex,
  parseTransform,
  reachableDefs,
  rebaseRelativeColor,
  registerTheme,
  renderSlideSvg,
  requiredContrastRatio,
  resolveBoundThemeResult,
  resolveFontFace,
  resolveIrTheme,
  resolveNarrative,
  retiredThemeHint,
  stripEmphasis,
  themeIssueMessage,
  validateIr,
  visitStringLeaves
} from "./chunk-DQABTUNM.js";
import {
  getPlatform
} from "./chunk-RHKPZSTM.js";

// src/version.ts
var VERSION = "0.44.0";

// src/kind-components.ts
function assertKind(kind) {
  if (KIND_VALUES.includes(kind)) return;
  throw new PptwiseError(`unknown kind "${kind}". Valid kinds: ${KIND_VALUES.join(", ")}`);
}
function faceOffer(theme, kind) {
  const face = theme.menu.content[kind].face;
  const layout = getLayout(face);
  if (layout === void 0) {
    throw new PptwiseError(`theme "${theme.id}" references unknown face "${face}" for kind "${kind}"`);
  }
  return { face, components: faceAcceptedComponentTypes(layout) };
}
function offerFor(theme, kind) {
  if (theme.menu.content[kind] !== void 0) return faceOffer(theme, kind);
  const candidates = landingCandidates(kind, theme.menu);
  if (candidates.length === 0) return void 0;
  const union = /* @__PURE__ */ new Set();
  for (const candidate of candidates) for (const type of faceOffer(theme, candidate).components) union.add(type);
  return { face: faceOffer(theme, candidates[0]).face, components: COMPONENT_TYPES.filter((type) => union.has(type)), drawnAs: candidates };
}
function componentsForKind(kind, options = {}) {
  assertKind(kind);
  const themes = {};
  if (options.theme !== void 0) {
    const theme = typeof options.theme === "string" ? getThemeDefinition(options.theme) : options.theme;
    const offer = offerFor(theme, kind);
    if (offer === void 0) {
      const offered = offeredContentKinds(theme.menu);
      throw new PptwiseError(
        `kind "${kind}" is not offered by theme "${theme.id}", and neither is any kind it can stand in for. Available content kinds: ${offered.join(", ")}`
      );
    }
    themes[theme.id] = offer;
  } else {
    for (const id of getInstalledThemeIds()) {
      const offer = offerFor(getThemeDefinition(id), kind);
      if (offer !== void 0) themes[id] = offer;
    }
    for (const theme of options.extraThemes ?? []) {
      const offer = offerFor(theme, kind);
      if (offer !== void 0) themes[theme.id] = offer;
    }
  }
  const union = /* @__PURE__ */ new Set();
  for (const offer of Object.values(themes)) for (const type of offer.components) union.add(type);
  return { kind, components: COMPONENT_TYPES.filter((type) => union.has(type)), themes };
}
function kindJsonSchema(kind, options = {}) {
  const offer = componentsForKind(kind, { theme: options.theme, extraThemes: options.extraThemes });
  const full = irJsonSchema();
  const head = { $schema: full.$schema, kind: offer.kind, components: offer.components, themes: offer.themes };
  if (offer.components.length === 0) {
    const themes = Object.keys(offer.themes).map((id) => `"${id}"`).join(", ");
    return {
      ...head,
      description: `A "${offer.kind}" page under theme ${themes} takes no component: its face draws the heading alone.`,
      not: {}
    };
  }
  const defs = full.$defs ?? {};
  const oneOf = offer.components.map((type) => ({ $ref: `#/$defs/${type}` }));
  const needed = reachableDefs(defs, oneOf);
  return {
    ...head,
    oneOf,
    ...Object.keys(needed).length > 0 ? { $defs: needed } : {}
  };
}

// src/themes/presets.ts
var THEME_PRESETS = CANONICAL_THEME_IDS.map((id) => ({
  id,
  label: BUILTIN_THEME_FILES[id].label,
  occasions: THEME_OCCASIONS[id].occasions,
  identity: THEME_OCCASIONS[id].identity
}));
function isThemePresetId(id) {
  return CANONICAL_THEME_IDS.includes(id);
}
function getThemePreset(id) {
  const summary = THEME_PRESETS.find((preset) => preset.id === id);
  if (!summary) {
    throw new PptwiseError(
      `unknown theme preset "${id}"${retiredThemeHint(id)}. Installed presets: ${CANONICAL_THEME_IDS.join(", ")}`
    );
  }
  return summary;
}
function withDecor(entry, motif) {
  if (entry.decor !== void 0 || motif === void 0) return structuredClone(entry);
  if (getLayout(entry.face)?.suppressMotif === true) return structuredClone(entry);
  return {
    ...structuredClone(entry),
    decor: motif.params ? { kind: "motif", id: motif.id, params: { ...motif.params } } : { kind: "motif", id: motif.id }
  };
}
function copyMenu(menu, motif) {
  const content = {};
  for (const [kind, entry] of Object.entries(menu.content)) {
    content[kind] = withDecor(entry, motif);
  }
  return {
    cover: withDecor(menu.cover, motif),
    chapter: withDecor(menu.chapter, motif),
    content,
    ending: withDecor(menu.ending, motif)
  };
}
function copyThemePreset(presetId, targetId) {
  getThemePreset(presetId);
  if (!THEME_ID_PATTERN.test(targetId)) {
    throw new PptwiseError(`invalid theme id "${targetId}". ${THEME_ID_CONSTRAINT}`);
  }
  assertNotRetiredThemeId(targetId);
  const preset = BUILTIN_THEME_FILES[presetId];
  const record = THEME_OCCASIONS[preset.id];
  return {
    version: 2,
    id: targetId,
    label: preset.label,
    style: { ...structuredClone(preset.style), id: targetId },
    ...preset.brand ? { brand: structuredClone(preset.brand) } : {},
    occasions: [...record.occasions],
    identity: record.identity,
    ...preset.emphasis ? { emphasis: preset.emphasis } : {},
    // The story travels with the copy for the same reason `emphasis` does:
    // it is what the theme is, not how it was built. A copy that lost it
    // would come out of the box with nothing to say for itself, and the
    // gallery and the docs read the copy, not the preset it came from.
    ...preset.story ? { story: structuredClone(preset.story) } : {},
    menu: copyMenu(preset.menu, preset.motif)
  };
}
function publicStyle(style, id) {
  const colors = { ...style.colors };
  const fonts = {
    heading: [...style.fonts.heading],
    body: [...style.fonts.body]
  };
  if (style.fonts.mono !== void 0) fonts.mono = [...style.fonts.mono];
  if (style.fonts.figure !== void 0) fonts.figure = [...style.fonts.figure];
  const out = {
    id,
    colors,
    fonts,
    defaultBackgrounds: structuredClone(style.defaultBackgrounds)
  };
  if (style.allowCustomBackground !== void 0) out.allowCustomBackground = style.allowCustomBackground;
  if (style.shape !== void 0) {
    const shape = {};
    if (style.shape.radius !== void 0) shape.radius = style.shape.radius;
    if (style.shape.gapScale !== void 0) shape.gapScale = style.shape.gapScale;
    if (style.shape.typeScale !== void 0) shape.typeScale = style.shape.typeScale;
    if (Object.keys(shape).length > 0) out.shape = shape;
  }
  return out;
}
function themeFileFromPreset(presetId, identity) {
  const copy = copyThemePreset(presetId, identity.id);
  const file = {
    version: 2,
    id: identity.id,
    label: identity.label ?? copy.label,
    style: publicStyle(copy.style, identity.id),
    brand: copy.brand,
    occasions: copy.occasions !== void 0 ? [...copy.occasions] : void 0,
    identity: copy.identity,
    emphasis: copy.emphasis,
    story: copy.story,
    menu: copy.menu
  };
  return ThemeFileSchema.parse(file);
}

// src/themes/extract/brand-extract.ts
import JSZip from "jszip";

// src/themes/brand/brand-sample.ts
var BRAND_SAMPLE_PHOTO = "brand-sample-photo";
var GREY_PNG = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAADCAIAAAA7ljmRAAAADklEQVR4nGNoQAIMODkAXzYSAY5zHKsAAAAASUVORK5CYII=";
var CONTENT_PAGES = [
  {
    kind: "points",
    heading: "What we decided",
    components: [{ type: "bullets", items: ["Hold hiring at 42", "Cut the analytics rebuild", "Share the support rotation"] }]
  },
  {
    kind: "list",
    heading: "Open workstreams",
    components: [{ type: "bullets", items: ["EU residency addendum", "Partner invite flow", "Invoice localization"] }]
  },
  {
    kind: "comparison",
    heading: "Build vs buy",
    components: [
      {
        type: "comparison",
        columns: ["Build", "Buy"],
        rows: [
          { label: "Time to first report", cells: ["14 weeks", "3 weeks"] },
          { label: "Year-one cost", cells: ["$420k", "$180k"] }
        ]
      }
    ]
  },
  {
    kind: "process",
    heading: "How we ship",
    components: [
      {
        type: "steps",
        items: [
          { title: "Scope", text: "One page, one owner" },
          { title: "Build", text: "Two-week slices" },
          { title: "Prove", text: "A number in production" }
        ]
      }
    ]
  },
  {
    kind: "data",
    heading: "Revenue against target",
    components: [
      {
        type: "chart",
        chart_type: "bar",
        series: [
          { name: "Actual", data: [{ x: "Q1", y: 12 }, { x: "Q2", y: 14 }, { x: "Q3", y: 16 }, { x: "Q4", y: 18 }] },
          { name: "Target", data: [{ x: "Q1", y: 12 }, { x: "Q2", y: 15 }, { x: "Q3", y: 16 }, { x: "Q4", y: 17 }] }
        ]
      }
    ]
  },
  {
    kind: "photo",
    heading: "The new floor",
    components: [{ type: "image", asset_id: BRAND_SAMPLE_PHOTO, caption: "Level three, the week we moved in" }]
  },
  {
    kind: "statement",
    heading: "We will not add a fourth product line this year",
    components: [{ type: "paragraph", text: "Three products is the house." }]
  },
  {
    kind: "quote",
    heading: "From the floor",
    components: [{ type: "blockquote", text: "We almost shipped the wrong thing.", attribution: "Team lead" }]
  },
  {
    kind: "fact",
    heading: "NPS",
    components: [{ type: "kpi_cards", items: [{ value: "61", label: "trailing 90-day NPS", delta: "up" }] }]
  },
  {
    kind: "evidence",
    heading: "What customers said",
    components: [{ type: "blockquote", text: "Setup took an afternoon, not a quarter.", attribution: "Operations director" }]
  },
  {
    kind: "hierarchy",
    heading: "Who owns what",
    components: [
      {
        type: "org_tree",
        root: { name: "Dana Reyes", role: "COO" },
        children: [
          { name: "Sam Okafor", role: "Platform" },
          { name: "Lee Park", role: "Growth" }
        ]
      }
    ]
  }
];
var COVER = { type: "cover", heading: "Third Quarter Review", subheading: "Q3 operating report for the board" };
var CHAPTER = { type: "chapter", heading: "The Quarter" };
var ENDING = { type: "ending", heading: "See you Thursday" };
var BRAND_SAMPLE_HEADINGS = [COVER, CHAPTER, ...CONTENT_PAGES, ENDING].map((page) => page.heading);
function brandSampleIr(themeId, offered) {
  return {
    version: "5",
    filename: "brand-sample",
    theme: { id: themeId },
    meta: { organization: "Northstar", date: "2026-10-01" },
    assets: { images: { [BRAND_SAMPLE_PHOTO]: { src: GREY_PNG, alt: "An office floor" } } },
    slides: [
      COVER,
      CHAPTER,
      ...CONTENT_PAGES.filter((page) => offered.has(page.kind)).map((page) => ({ type: "content", ...page })),
      ENDING
    ]
  };
}

// src/themes/brand/brand-face.ts
var BRAND_SLOTS = ["primary", "accent"];
var LARGE_TEXT_PX = 24;
var CHROMA_FLOOR = 0.04;
function isChromatic(hex) {
  return oklchChroma(hex) >= CHROMA_FLOOR;
}
var SHAPE_RE = /<(rect|line|circle|ellipse|path|polygon|polyline)\b([^>]*)>/g;
var TEXT_RE = /<text\b([^>]*)>([\s\S]*?)<\/text>/g;
var TSPAN_RE = /<tspan\b([^>]*)>([^<]*)/g;
var ATTR_RE = /([a-zA-Z][a-zA-Z0-9:-]*)="([^"]*)"/g;
var HEX_RE = /^#[0-9a-fA-F]{6}$/;
var FILL_MIN_SIDE = 16;
var PAGE_AREA = 1280 * 720;
var TEXT_INK_SHARE = 0.35;
var GLYPH_ADVANCE_EM = 0.55;
function attrs(source) {
  const out = /* @__PURE__ */ new Map();
  for (const m of source.matchAll(ATTR_RE)) out.set(m[1], m[2]);
  return out;
}
function num(a, key, fallback = 0) {
  const value = Number(a.get(key));
  return Number.isFinite(value) ? value : fallback;
}
function opacity(a, channel) {
  return num(a, "opacity", 1) * num(a, `${channel}-opacity`, 1);
}
function pointsBox(source) {
  const values = (source.match(/-?\d*\.?\d+(?:e-?\d+)?/g) ?? []).map(Number);
  const xs = values.filter((_, i) => i % 2 === 0);
  const ys = values.filter((_, i) => i % 2 === 1);
  if (xs.length === 0 || ys.length === 0) return { w: 0, h: 0 };
  return { w: Math.max(...xs) - Math.min(...xs), h: Math.max(...ys) - Math.min(...ys) };
}
function shapeGeometry(tag, a) {
  switch (tag) {
    case "rect": {
      const w = num(a, "width");
      const h = num(a, "height");
      return { fill: w * h, stroke: 2 * (w + h), side: Math.min(w, h) };
    }
    case "line":
      return { fill: 0, stroke: Math.hypot(num(a, "x2") - num(a, "x1"), num(a, "y2") - num(a, "y1")), side: 0 };
    case "circle": {
      const r = num(a, "r");
      return { fill: Math.PI * r * r, stroke: 2 * Math.PI * r, side: 2 * r };
    }
    case "ellipse": {
      const rx = num(a, "rx");
      const ry = num(a, "ry");
      return { fill: Math.PI * rx * ry, stroke: Math.PI * (rx + ry), side: 2 * Math.min(rx, ry) };
    }
    default: {
      const box = pointsBox(a.get(tag === "path" ? "d" : "points") ?? "");
      return { fill: box.w * box.h / 2, stroke: box.w + box.h, side: Math.min(box.w, box.h) };
    }
  }
}
function isHeadingRun(text, headings) {
  const run = text.trim().toLowerCase();
  return run.length >= 3 && headings.some((heading) => heading.toLowerCase().includes(run));
}
function countSlotUse(svgs, colors, headings = []) {
  const empty = () => ({ area: 0, bodyText: 0, largeText: 0, headings: 0, headingPx: 0, field: 0, filled: 0 });
  const use = { primary: empty(), accent: empty() };
  const slotsOf = (hex) => hex === void 0 || !HEX_RE.test(hex) ? [] : BRAND_SLOTS.filter((slot) => colors[slot].toUpperCase() === hex.toUpperCase());
  const addText = (a, text, inherited) => {
    const fill = a.get("fill") ?? inherited.get("fill");
    const size = num(a, "font-size", num(inherited, "font-size"));
    const chars = text.replace(/&[a-z#0-9]+;/g, "x").trim().length;
    if (chars === 0) return;
    for (const slot of slotsOf(fill)) {
      use[slot].area += chars * GLYPH_ADVANCE_EM * size * size * TEXT_INK_SHARE * opacity(a, "fill");
      if (size >= LARGE_TEXT_PX) use[slot].largeText++;
      else use[slot].bodyText++;
      if (isHeadingRun(text, headings)) {
        use[slot].headings++;
        use[slot].headingPx = Math.max(use[slot].headingPx, size);
      }
    }
  };
  for (const svg of svgs) {
    for (const m of svg.matchAll(SHAPE_RE)) {
      const a = attrs(m[2]);
      const geometry = shapeGeometry(m[1], a);
      for (const slot of slotsOf(a.get("fill"))) {
        const painted = geometry.fill * opacity(a, "fill");
        use[slot].area += painted;
        if (geometry.side >= FILL_MIN_SIDE) use[slot].filled += painted;
        if (m[1] === "rect") use[slot].field = Math.max(use[slot].field, geometry.fill / PAGE_AREA);
      }
      for (const slot of slotsOf(a.get("stroke"))) {
        use[slot].area += geometry.stroke * num(a, "stroke-width", 1) * opacity(a, "stroke");
      }
    }
    for (const m of svg.matchAll(TEXT_RE)) {
      const a = attrs(m[1]);
      const inner = m[2];
      if (!inner.includes("<tspan")) {
        addText(a, inner.replace(/<[^>]*>/g, ""), /* @__PURE__ */ new Map());
        continue;
      }
      for (const span of inner.matchAll(TSPAN_RE)) addText(attrs(span[1]), span[2], a);
    }
  }
  return use;
}
function slotWeight(use, color, bg) {
  return use.area * oklabDistance(color, bg);
}
function pickBrandFace(colors, use) {
  const chromatic = { primary: isChromatic(colors.primary), accent: isChromatic(colors.accent) };
  const candidates = BRAND_SLOTS.filter((slot2) => chromatic[slot2]);
  const weight = (slot2) => slotWeight(use[slot2], colors[slot2], colors.bg);
  let slot = "accent";
  if (candidates.length > 0) {
    slot = candidates.reduce((best, next) => weight(next) > weight(best) ? next : best);
  }
  return { slot, chromatic, use, headingRuns: 0 };
}
function countHeadingRuns(svgs, headings) {
  let runs = 0;
  for (const svg of svgs) {
    for (const m of svg.matchAll(/<(?:text|tspan)\b[^>]*>([^<]*)/g)) if (isHeadingRun(m[1], headings)) runs++;
  }
  return runs;
}
function renderBrandSample(theme, only) {
  const definition = compileThemeDefinition(theme);
  const raw = brandSampleIr(definition.id, new Set(offeredContentKinds(definition.menu)));
  const v = validateIr(raw, { theme: definition });
  if (!v.ok) {
    throw new PptwiseError(`theme "${definition.id}" cannot draw the brand sample deck:
${formatIssues(v.errors)}`);
  }
  const ir = v.ir;
  const pages = only ?? ir.slides.map((_, index) => index);
  return pages.map((index) => renderSlideSvg(ir, index, { theme: definition }));
}
function withSlot(theme, slot, color) {
  const out = structuredClone(theme);
  const colors = out.style.colors;
  const oneColor = colors.primary.toUpperCase() === colors.accent.toUpperCase();
  colors[slot] = color;
  if (oneColor) colors[slot === "primary" ? "accent" : "primary"] = color;
  return out;
}
function filledRects(svg) {
  const out = [];
  for (const m of svg.matchAll(/<rect\b([^>]*)>/g)) {
    const a = attrs(m[1]);
    out.push({ fill: (a.get("fill") ?? "").toUpperCase(), share: num(a, "width") * num(a, "height") / PAGE_AREA });
  }
  return out;
}
function findDerivedField(theme, slot, own) {
  const color = theme.style.colors[slot].toUpperCase();
  const c = hexToOklch(color);
  const probe = oklchToHex({ L: c.L, C: Math.max(c.C, 0.12), h: c.h + 180 });
  const moved = renderBrandSample(withSlot(theme, slot, probe));
  let best;
  own.forEach((svg, page) => {
    const before = filledRects(svg);
    const after = filledRects(moved[page]);
    if (before.length !== after.length) return;
    before.forEach((rect, ordinal) => {
      if (rect.fill === color || rect.fill === after[ordinal].fill || !HEX_RE.test(rect.fill)) return;
      if (best === void 0 || rect.share > best.share) best = { page, ordinal, share: rect.share };
    });
  });
  return best;
}
function paintedField(theme, slot, color, field) {
  const [svg] = renderBrandSample(withSlot(theme, slot, color), [field.page]);
  const rect = filledRects(svg)[field.ordinal];
  if (rect === void 0 || !HEX_RE.test(rect.fill)) {
    throw new PptwiseError(`theme "${theme.id}" no longer draws the field its ${slot} is worked into on sample page ${field.page + 1}`);
  }
  return rect.fill;
}
function measureBrandFace(theme) {
  const { primary, accent, bg } = theme.style.colors;
  const svgs = renderBrandSample(theme);
  const face = pickBrandFace({ primary, accent, bg }, countSlotUse(svgs, { primary, accent }, BRAND_SAMPLE_HEADINGS));
  for (const slot of BRAND_SLOTS) {
    if (!face.chromatic[slot]) continue;
    const derivedField = findDerivedField(theme, slot, svgs);
    if (derivedField !== void 0) face.use[slot].derivedField = derivedField;
  }
  return { ...face, headingRuns: countHeadingRuns(svgs, BRAND_SAMPLE_HEADINGS) };
}

// src/themes/chart-taboo.ts
var VIVID_SATURATION = 0.35;
function isVividOrange(hex) {
  const { h, s } = hexToHsl(hex);
  return s >= VIVID_SATURATION && h >= 15 && h <= 50;
}
function isVividBlue(hex) {
  const { h, s } = hexToHsl(hex);
  return s >= VIVID_SATURATION && h >= 195 && h <= 260;
}
function isTabooPair(a, b) {
  return isVividOrange(a) && isVividBlue(b) || isVividBlue(a) && isVividOrange(b);
}

// src/themes/brand/color-name.ts
var PINK_FROM = 0.62;
var BROWN_BELOW = 0.6;
var PEACH_FROM = 0.82;
var CREAM_FROM = 0.9;
function colorName(hex) {
  const { L, C, h } = hexToOklch(hex);
  if (C < CHROMA_FLOOR) return "neutral";
  if (h >= 345 || h < 10) return "pink";
  if (h < 45) return L >= PINK_FROM ? "pink" : "red";
  if (h < 75) return L < BROWN_BELOW ? "brown" : L >= PEACH_FROM ? "peach" : "orange";
  if (h < 115) return L < BROWN_BELOW ? "olive" : L >= CREAM_FROM ? "cream" : "yellow";
  if (h < 175) return "green";
  if (h < 215) return "teal";
  if (h < 290) return "blue";
  return "purple";
}
function keepsName(shade, source) {
  return colorName(shade) === colorName(source);
}

// src/themes/brand/brand-regen.ts
var BODY_TEXT_RATIO = 4.5;
var MARK_RATIO = 3;
var GROUND_DISTANCE = 0.15;
var FIELD_SHARE = 0.5;
var FIELD_DRIFT = 0.1;
var FILL_SHARE = 0.5;
var SHADE_STEP = 0.12;
var SERIES_DISTANCE = 0.1;
var VIVID_CHROMA = 0.08;
var NEUTRAL_TINT_CHROMA = 0.035;
var NEIGHBOUR_HUES = [0, 12, -12, 25, -25];
function lightnessSteps(reach) {
  const steps = [0];
  for (let d = 0.04; d <= reach + 1e-9; d += 0.04) steps.push(d, -d);
  return steps;
}
var SERIES_LIGHTNESS_REACH = 0.12;
var SLOT_LIGHTNESS_REACH = 0.32;
var FALLBACK_LIGHTNESS_REACH = 0.3;
var SHADE_LIGHTNESS_BAND = [0.15, 0.92];
var upper = (hex) => hex.toUpperCase();
function otherSlot(slot) {
  return slot === "primary" ? "accent" : "primary";
}
function showsAsColor(hex, bg) {
  return isChromatic(hex) && oklabDistance(hex, bg) >= GROUND_DISTANCE;
}
function liftToContrast(color, bg, need) {
  if (contrastRatio(color, bg) >= need) return upper(color);
  const c = hexToOklch(color);
  const lighter = contrastRatio("#FFFFFF", bg) > contrastRatio("#000000", bg);
  for (let step = 1; step <= 1e3; step++) {
    const L = c.L + (lighter ? step : -step) / 1e3;
    if (L < 0 || L > 1) break;
    const hex = oklchToHex({ L, C: c.C, h: c.h });
    if (contrastRatio(hex, bg) >= need) return hex;
  }
  throw new PptwiseError(
    `cannot fit ${upper(color)} onto the theme's ground (${bg}): no lightness of its hue reaches ${need.toFixed(1)}:1`
  );
}
function shadeOf(target, hue, chromaCap, bg, need, taken, distance, name, reach = SERIES_LIGHTNESS_REACH) {
  const C = Math.min(target.C, chromaCap);
  let renamedOnly = false;
  for (const dh of NEIGHBOUR_HUES) {
    for (const dL of lightnessSteps(reach)) {
      const L = target.L + dL;
      if (L < SHADE_LIGHTNESS_BAND[0] || L > SHADE_LIGHTNESS_BAND[1]) continue;
      const hex = oklchToHex({ L, C, h: hue + dh });
      if (contrastRatio(hex, bg) < need) continue;
      if (taken.some((t) => oklabDistance(t, hex) < distance)) continue;
      if (!keepsName(hex, name)) {
        renamedOnly = true;
        continue;
      }
      return hex;
    }
  }
  if (renamedOnly) return void 0;
  let best;
  for (const dh of NEIGHBOUR_HUES) {
    for (let L = SHADE_LIGHTNESS_BAND[0]; L <= SHADE_LIGHTNESS_BAND[1] + 1e-9; L += 0.02) {
      const hex = oklchToHex({ L, C, h: hue + dh });
      if (contrastRatio(hex, bg) < need || !keepsName(hex, name)) continue;
      if (hexToOklch(hex).C < 0.6 * C || Math.abs(L - target.L) > FALLBACK_LIGHTNESS_REACH) continue;
      const gap = Math.min(...taken.map((t) => oklabDistance(t, hex)));
      if (best === void 0 || gap > best.gap) best = { hex, gap };
    }
  }
  return best !== void 0 && best.gap >= distance ? best.hex : void 0;
}
function themeNeutrals(src) {
  const greys = [...src.chartPalette, ...src.accentPool ?? []].map(upper).filter((hex) => !isChromatic(hex));
  return [.../* @__PURE__ */ new Set([...greys, upper(src.text), upper(src.muted)])];
}
function neutralFor(target, neutrals, bg, need, taken, distance) {
  const L = hexToOklch(target).L;
  const reads = neutrals.filter((hex) => contrastRatio(hex, bg) >= need && !taken.includes(hex));
  const byLightness = (list) => [...list].sort((a, b) => Math.abs(hexToOklch(a).L - L) - Math.abs(hexToOklch(b).L - L));
  const apart = reads.filter((hex) => taken.every((t) => oklabDistance(t, hex) >= distance));
  const pick = byLightness(apart)[0] ?? byLightness(reads)[0] ?? byLightness(neutrals.filter((hex) => contrastRatio(hex, bg) >= need))[0];
  if (pick !== void 0) return pick;
  throw new PptwiseError(`no neutral of the theme reads ${need.toFixed(1)}:1 on its ground (${bg})`);
}
function slotRoles(face, own, bg) {
  const writesHeadings = (s) => face.use[s].headings > 0 && face.use[s].headings * 2 >= face.headingRuns;
  return {
    writesHeadings,
    headingNeed: (s) => requiredContrastRatio(face.use[s].headingPx),
    isGround: (s) => face.use[s].field >= FIELD_SHARE,
    /** Mostly bars and blocks, not rules and strokes: a field of color takes the brand as it is. */
    fills: (s) => face.use[s].area > 0 && face.use[s].filled / face.use[s].area >= FILL_SHARE,
    /** Marks need 3:1, never more than the theme's own color had. */
    markNeed: (s) => Math.min(MARK_RATIO, contrastRatio(own[s], bg)),
    /** A derived color in the slot: body contrast when it sets body words, never more than the theme's own had. */
    shadeNeed: (s) => Math.min(face.use[s].bodyText > 0 ? BODY_TEXT_RATIO : MARK_RATIO, contrastRatio(own[s], bg)),
    isColor: (s) => showsAsColor(own[s], bg)
  };
}
function regenerateFromBrand(source, colors, identity, face = measureBrandFace(source)) {
  const B = upper(HexTokenSchema.parse(colors.brand));
  const B2 = colors.second === void 0 ? void 0 : upper(HexTokenSchema.parse(colors.second));
  const src = source.style.colors;
  const bg = src.bg;
  const F = face.slot;
  const own = { primary: upper(src.primary), accent: upper(src.accent) };
  const oneColor = own.primary === own.accent;
  const roles = slotRoles(face, own, bg);
  const brandHue = hexToOklch(B);
  const neutrals = themeNeutrals(src);
  const refused = (f) => "why" in f;
  const fit = (x, s, checkField = true) => {
    const ratio = contrastRatio(x, bg);
    let fitted;
    if (roles.writesHeadings(s)) {
      const need = roles.headingNeed(s);
      if (ratio < need) return { why: "headings", need, ratio };
      fitted = { written: x, ground: false };
    } else if (roles.isGround(s)) fitted = { written: x, ground: true };
    else if (roles.fills(s)) fitted = { written: x, ground: false, fills: true };
    else {
      const need = roles.markNeed(s);
      fitted = ratio >= need ? { written: x, ground: false } : { written: liftToContrast(x, bg, need), ground: false, lifted: { need, ratio } };
    }
    const field = face.use[s].derivedField;
    if (checkField && field !== void 0 && field.share >= FIELD_SHARE) {
      const painted = paintedField(source, s, fitted.written, field);
      const distance = oklabDistance(painted, x);
      if (distance > FIELD_DRIFT) return { why: "repainted", painted, distance };
    }
    return fitted;
  };
  let brandSlot = F;
  const inFace = fit(B, F);
  let brandFit;
  let passedOver;
  if (!refused(inFace)) brandFit = inFace;
  else {
    const O = otherSlot(F);
    const inOther = !oneColor && roles.isColor(O) ? fit(B, O) : void 0;
    if (inOther !== void 0 && !refused(inOther)) {
      brandSlot = O;
      brandFit = inOther;
      passedOver = { slot: F, ...inFace };
    } else if (inFace.why === "headings") {
      brandFit = { written: liftToContrast(B, bg, inFace.need), ground: false, lifted: { need: inFace.need, ratio: inFace.ratio } };
    } else {
      const kept = fit(B, F, false);
      brandFit = refused(kept) ? { written: liftToContrast(B, bg, MARK_RATIO), ground: false } : kept;
    }
  }
  const slots = { ...own };
  slots[brandSlot] = brandFit.written;
  if (oneColor) slots[otherSlot(brandSlot)] = brandFit.written;
  const S2 = otherSlot(brandSlot);
  const oneColorChart = isSingleColorPalette(src.chartPalette.map(upper));
  let second;
  if (B2 !== void 0) {
    const free = !oneColor && roles.isColor(S2);
    const tried = free ? fit(B2, S2) : void 0;
    const secondFit = tried !== void 0 && !refused(tried) ? tried : void 0;
    if (secondFit !== void 0) slots[S2] = secondFit.written;
    second = {
      color: B2,
      slot: secondFit === void 0 ? null : S2,
      written: secondFit?.written ?? null,
      ground: secondFit?.ground ?? false,
      ...secondFit?.fills ? { fills: true } : {},
      ...secondFit?.lifted ? { lifted: secondFit.lifted } : {},
      ...secondFit === void 0 ? { noSlot: oneColor ? "one-color" : tried !== void 0 && refused(tried) ? tried.why : "neutral" } : {},
      chart: oneColorChart ? null : secondFit !== void 0 && src.chartPalette.map(upper).includes(own[S2]) ? secondFit.written : B2
    };
  } else if (brandSlot === F && !oneColor && roles.isColor(S2)) {
    const need = roles.shadeNeed(S2);
    slots[S2] = shadeOf(hexToOklch(own[S2]), brandHue.h, brandHue.C, bg, need, [slots[F]], SHADE_STEP, B, SLOT_LIGHTNESS_REACH) ?? neutralFor(own[S2], neutrals, bg, need, [slots[F]], SHADE_STEP);
  }
  const repainted = (hex) => {
    const key = upper(hex);
    for (const s of ["primary", "accent"]) if (key === own[s] && slots[s] !== own[s]) return slots[s];
    return void 0;
  };
  const chartRepainted = (hex) => second?.slot && second.chart === null && upper(hex) === own[second.slot] ? void 0 : repainted(hex);
  const ownPalette = new Set(src.chartPalette.map(upper));
  const chartBrand = ownPalette.has(own[brandSlot]) ? slots[brandSlot] : B;
  const shade = (hex, taken) => {
    const need = Math.min(MARK_RATIO, contrastRatio(hex, bg));
    return shadeOf(hexToOklch(hex), brandHue.h, brandHue.C, bg, need, taken, SERIES_DISTANCE, B) ?? neutralFor(hex, neutrals, bg, need, taken, SERIES_DISTANCE);
  };
  const tint = (hex) => {
    const c = hexToOklch(hex);
    return oklchToHex({ ...c, C: Math.min(c.C, NEUTRAL_TINT_CHROMA), h: brandHue.h });
  };
  const chartPalette = deriveSeries(src.chartPalette.map(upper), {
    lead: chartBrand,
    second: second?.chart ?? void 0,
    slotEntries: { [own[brandSlot]]: chartBrand, ...second?.slot && second.chart !== null ? { [own[second.slot]]: second.chart } : {} },
    repainted: chartRepainted,
    shade,
    tint,
    bg,
    neutrals
  });
  const out = { ...src, primary: slots.primary, accent: slots.accent, chartPalette };
  if (src.accentPool !== void 0) {
    out.accentPool = deriveSeries(src.accentPool.map(upper), {
      lead: chartBrand,
      second: second?.chart ?? void 0,
      slotEntries: {},
      repainted: chartRepainted,
      shade,
      tint,
      bg,
      neutrals,
      keepOrder: true
    });
  }
  if (src.emphasisInk !== void 0) {
    const e = upper(src.emphasisInk);
    const base = repainted(e) ?? (e !== own.primary && e !== own.accent && isChromatic(e) ? shadeOf(hexToOklch(e), brandHue.h, brandHue.C, bg, 0, [], 0, B) : void 0);
    const ink = base === void 0 ? e : liftToContrast(base, bg, BODY_TEXT_RATIO);
    out.emphasisInk = ink === e || keepsName(ink, B) ? ink : e;
  }
  const ground = (hex) => repainted(hex) ?? hex;
  const background = (spec) => {
    if (spec.kind === "color") return { ...spec, value: ground(spec.value) };
    if (spec.kind === "gradient") return { ...spec, from: ground(spec.from), to: ground(spec.to) };
    if (spec.overlay !== void 0) return { ...spec, overlay: { ...spec.overlay, color: ground(spec.overlay.color) } };
    return spec;
  };
  const backgrounds = source.style.defaultBackgrounds;
  const file = ThemeFileSchema.parse({
    ...source,
    id: identity.id,
    label: identity.label ?? source.label,
    style: {
      ...source.style,
      id: identity.id,
      colors: out,
      fonts: identity.fonts ?? source.style.fonts,
      defaultBackgrounds: {
        cover: background(backgrounds.cover),
        chapter: background(backgrounds.chapter),
        content: background(backgrounds.content),
        ending: background(backgrounds.ending)
      }
    },
    menu: structuredClone(source.menu)
  });
  assertContrastFloor(file.id, file.style);
  return {
    file,
    placement: {
      bg,
      face: F,
      brand: {
        color: B,
        slot: brandSlot,
        written: brandFit.written,
        ground: brandFit.ground,
        ...brandFit.fills ? { fills: true } : {},
        ...brandFit.lifted ? { lifted: brandFit.lifted } : {},
        ...passedOver ? { passedOver } : {},
        ...isChromatic(B) ? {} : { neutral: true },
        chart: chartBrand
      },
      ...second ? { second } : {}
    }
  };
}
function isSingleColorPalette(palette) {
  return palette.filter((hex) => hexToOklch(hex).C >= VIVID_CHROMA).length <= 1 && palette.some((hex) => !isChromatic(hex));
}
function deriveSeries(palette, opts) {
  const neutral = (hex) => !isChromatic(hex);
  if (opts.keepOrder || isSingleColorPalette(palette)) {
    const fixed = palette.map((hex) => opts.slotEntries[hex] ?? opts.repainted(hex) ?? (neutral(hex) ? hex : null));
    const pending = [opts.lead, ...opts.second ? [opts.second] : []].filter((c) => !fixed.includes(c));
    const out2 = [];
    for (let i = 0; i < palette.length; i++) {
      const value = fixed[i] ?? pending.shift() ?? opts.shade(palette[i], [...out2, ...fixed.slice(i + 1).filter((v) => v !== null)]);
      out2.push(value);
    }
    for (const lead of pending) {
      const at = out2.indexOf(opts.lead);
      out2.splice(at < 0 ? 0 : at + 1, 0, lead);
    }
    return dedupe(keepTaboo(separateNeutrals(out2, palette, opts.bg), [...palette, ...opts.neutrals], opts));
  }
  const leads = [opts.lead, ...opts.second ? [opts.second] : []];
  const out = [...leads];
  const neutrals = palette.filter(neutral);
  const replaced = new Set(palette.filter((hex) => opts.slotEntries[hex] !== void 0));
  for (const lead of leads) {
    if (palette.some((hex) => opts.slotEntries[hex] === lead)) continue;
    const free = palette.find((hex) => !neutral(hex) && !replaced.has(hex));
    if (free !== void 0) replaced.add(free);
  }
  for (const hex of palette) {
    if (neutral(hex) || replaced.has(hex)) continue;
    const repainted = opts.repainted(hex);
    const taken = [...out, ...neutrals];
    out.push(repainted !== void 0 && taken.every((t) => oklabDistance(t, repainted) >= SERIES_DISTANCE) ? repainted : opts.shade(hex, taken));
  }
  return dedupe(keepTaboo(separateNeutrals([...out, ...neutrals], palette, opts.bg), [...palette, ...opts.neutrals], opts));
}
function separateNeutrals(colors, source, bg) {
  const out = [...colors];
  for (let i = 0; i < out.length; i++) {
    const hex = out[i];
    if (!source.includes(hex) || isChromatic(hex)) continue;
    const others = () => out.filter((_, k) => k !== i && !source.includes(out[k]));
    if (others().every((other) => oklabDistance(other, hex) >= SERIES_DISTANCE)) continue;
    const c = hexToOklch(hex);
    const need = Math.min(MARK_RATIO, contrastRatio(hex, bg));
    for (const dL of lightnessSteps(SLOT_LIGHTNESS_REACH).slice(1)) {
      const moved = oklchToHex({ ...c, L: c.L + dL });
      if (contrastRatio(moved, bg) < need) continue;
      if (out.some((other, k) => k !== i && oklabDistance(other, moved) < SERIES_DISTANCE)) continue;
      out[i] = moved;
      break;
    }
  }
  return out;
}
function keepTaboo(colors, source, opts) {
  if (opts.second !== void 0) return colors;
  return colors.map(
    (hex) => source.includes(hex) && colors.some((other) => other !== hex && isTabooPair(hex, other)) ? opts.tint(hex) : hex
  );
}
function dedupe(colors) {
  return [...new Set(colors.map(upper))];
}
function describePlacement(placement, brandSource = "the brand color") {
  const { bg } = placement;
  const describe = (label, p) => {
    const lines = [];
    if (p.slot === null) {
      const why = p.noSlot === "one-color" ? "this theme paints primary and accent as one color" : p.noSlot === "headings" ? "the free slot writes the headings and the color does not read there" : p.noSlot === "repainted" ? "the pages work the free slot into a field that would not look like it" : "the theme's other slot is an ink, not a color";
      lines.push(
        p.chart === null ? `  ${label}: ${p.color} is not used: ${why}, and this theme keeps its charts one color among inks` : `  ${label}: ${p.color} is the chart's second series only: ${why}`
      );
    } else if (p.lifted !== void 0) {
      lines.push(
        `  ${label}: ${p.color} changed to ${p.written} for colors.${p.slot}: same hue, chroma no higher, lightness moved to reach ${p.lifted.need.toFixed(1)}:1 on bg ${bg} (it read ${p.lifted.ratio.toFixed(2)}:1)`
      );
    } else {
      lines.push(`  ${label}: ${p.color} is colors.${p.slot}${label === "brand" && p.passedOver === void 0 ? ", the color this theme shows most" : ""}`);
    }
    if (p.passedOver !== void 0) {
      const o = p.passedOver;
      lines.push(
        o.why === "headings" ? `    colors.${o.slot} keeps the theme's own color: it writes the headings, which need ${o.need.toFixed(1)}:1 on bg ${bg}, and ${p.color} reads ${o.ratio.toFixed(2)}:1` : `    colors.${o.slot} keeps the theme's own color: the pages work it into a larger field, which would come out ${o.painted} for ${p.color} (${o.distance.toFixed(2)} away in OKLab), no longer the brand`
      );
    }
    if (p.ground && p.slot !== null) {
      lines.push(`    colors.${p.slot} fills whole pages here, and the words on it take an ink that reads on ${p.color}`);
    }
    if (p.slot !== null && p.chart === null) {
      lines.push(`    the charts leave it out: this theme keeps them one color among inks`);
    }
    if (p.fills && p.slot !== null) {
      lines.push(`    colors.${p.slot} is mostly bars and blocks here, so it keeps ${p.color} as it is, and the words on it take an ink that reads on it`);
    }
    return lines;
  };
  const neutral = placement.brand.neutral ? [`  ${brandSource} ${placement.brand.color} has no color in it (a grey, a black or a white), so the theme is repainted in grey`] : [];
  return [...neutral, ...describe("brand", placement.brand), ...placement.second ? describe("second", placement.second) : []];
}
function parseBrandOption(value) {
  const parts = value.split(",").map((part) => part.trim());
  const check = (part) => {
    const parsed = part === void 0 ? void 0 : HexTokenSchema.safeParse(part);
    if (!parsed?.success) {
      throw new PptwiseError(`--brand takes a hex color, or two joined by a comma (#156082,#E97132), not "${value}"`);
    }
    return upper(parsed.data);
  };
  if (parts.length > 2) throw new PptwiseError(`--brand takes at most two colors, the brand and its second color, not "${value}"`);
  return parts.length === 2 ? { brand: check(parts[0]), second: check(parts[1]) } : { brand: check(parts[0]) };
}

// src/themes/extract/brand-extract.ts
var ACCENT_SLOTS = ["accent1", "accent2", "accent3", "accent4", "accent5", "accent6"];
var THEME_PART_RE = /theme\d*\.xml$/;
var THEME_VARIANTS_SEGMENT = "themeVariants";
var CLR_SCHEME_RE = /<a:clrScheme name="([^"]*)">([\s\S]*?)<\/a:clrScheme>/;
var CLR_SLOT_RE = /<a:(dk1|lt1|dk2|lt2|accent[1-6]|hlink|folHlink)>\s*<a:(?:srgbClr val="([0-9A-Fa-f]{6})"|sysClr[^>]*lastClr="([0-9A-Fa-f]{6})")/g;
var FONT_SCHEME_RE = /<a:fontScheme name="([^"]*)">[\s\S]*?<a:majorFont>\s*<a:latin typeface="([^"]*)"[\s\S]*?<a:minorFont>\s*<a:latin typeface="([^"]*)"/;
async function findThemePart(zip) {
  const candidates = Object.keys(zip.files).filter((name) => !zip.files[name].dir && THEME_PART_RE.test(name) && !name.includes(THEME_VARIANTS_SEGMENT)).sort((a, b) => a.length - b.length);
  const path = candidates[0];
  if (path === void 0) return void 0;
  const xml = await zip.files[path].async("string");
  return { path, xml };
}
function parseColors(xml) {
  const match = CLR_SCHEME_RE.exec(xml);
  if (!match) return { schemeName: void 0, slots: {} };
  const slots = {};
  for (const m of match[2].matchAll(CLR_SLOT_RE)) {
    const slot = m[1];
    const hex = m[2] ?? m[3];
    if (hex) slots[slot] = `#${hex.toUpperCase()}`;
  }
  return { schemeName: match[1]?.trim() || void 0, slots };
}
function parseFonts(xml) {
  const m = FONT_SCHEME_RE.exec(xml);
  if (!m) return { major: void 0, minor: void 0 };
  return { major: m[2]?.trim() || void 0, minor: m[3]?.trim() || void 0 };
}
var MUTED_STEPS = 20;
var MUTED_TARGET_RATIO = 4.5;
function findMutedCandidate(text, bg, surface) {
  for (let step = MUTED_STEPS; step >= 0; step--) {
    const t = step / MUTED_STEPS;
    const candidate = mixHex(text, bg, t);
    if (contrastRatio(candidate, bg) >= MUTED_TARGET_RATIO && contrastRatio(candidate, surface) >= MUTED_TARGET_RATIO) {
      return candidate.toUpperCase();
    }
  }
  return void 0;
}
function deriveMuted(text, bg, surface) {
  const candidate = findMutedCandidate(text, bg, surface);
  if (candidate !== void 0) return candidate;
  throw new PptwiseError(
    `cannot derive colors.muted with a contrast ratio of ${MUTED_TARGET_RATIO.toFixed(1)}:1 against both colors.bg (${bg}) and colors.surface (${surface}) from colors.text (${text}). Choose compatible background and text anchors`
  );
}
function slugify(input, fallback = "brand") {
  const slug = input.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return slug || fallback;
}
function templateColors(slots, path) {
  const accents = ACCENT_SLOTS.map((slot) => slots[slot]).filter((c) => c !== void 0);
  if (accents.length === 0) {
    throw new PptwiseError(`theme part ${path} has no accent colors \u2014 cannot read a brand color`);
  }
  const brand = slots.accent1 ?? slots.dk2 ?? accents[0];
  const second = slots.accent2;
  return second !== void 0 && second.toUpperCase() !== brand.toUpperCase() && isChromatic(second) ? { brand, second } : { brand };
}
function withTemplateFonts(fonts, template) {
  const notes = [];
  const lead = (role, face, stack) => {
    if (face === void 0) {
      notes.push(`fonts: the template names no ${role} font, so ${role} text keeps the theme's own`);
      return stack;
    }
    const next = [face, ...stack.filter((f) => f.toLowerCase() !== face.toLowerCase())];
    const resolved = resolveFontFace(next, role);
    if (!SAFE_FONTS.has(face.toLowerCase())) {
      notes.push(
        `warning: ${role} font "${face}" is not on the safe font list (the fonts a stock Windows machine has), so the slides set ${role} text in "${resolved}", the next safe face in the stack`
      );
    } else if (!hasExactWidthTable(face)) {
      notes.push(`warning: ${role} font "${face}" has no exact width table: text widths are estimated and long lines may overflow`);
    }
    return next;
  };
  return {
    fonts: { ...fonts, heading: lead("heading", template.major, fonts.heading), body: lead("body", template.minor ?? template.major, fonts.body) },
    notes
  };
}
function donorTheme(from, identity) {
  if (typeof from === "string") return themeFileFromPreset(from, identity);
  const copy = structuredClone(from);
  return ThemeFileSchema.parse({ ...copy, id: identity.id, label: identity.label, style: { ...copy.style, id: identity.id } });
}
async function extractBrandTheme(bytes, opts = {}) {
  const zip = await JSZip.loadAsync(bytes);
  const part = await findThemePart(zip);
  if (!part) {
    throw new PptwiseError(
      "no theme part found in this file \u2014 expected a .thmx/.potx/.pptx OOXML package with a ppt/theme/theme1.xml (or theme/theme/theme1.xml) part"
    );
  }
  const { schemeName, slots } = parseColors(part.xml);
  const colors = templateColors(slots, part.path);
  const label = opts.label ?? schemeName ?? "brand";
  const id = opts.id ?? slugify(opts.label ?? schemeName ?? "brand");
  const donor = donorTheme(opts.from ?? "bulletin", { id, label });
  const template = opts.brandFonts === true ? withTemplateFonts(donor.style.fonts, parseFonts(part.xml)) : void 0;
  const { file, placement } = regenerateFromBrand(donor, colors, { id, label, fonts: template?.fonts });
  return { file, placement, fontNotes: template?.notes ?? [] };
}

// src/themes/brand-theme-file.ts
var BrandThemeFileSchema = ThemeFileSchema;
function parseBrandThemeFile(raw, source) {
  const result = ThemeFileSchema.safeParse(raw);
  if (!result.success) {
    const detail = result.error.issues.map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`).join("\n");
    throw new PptwiseError(
      `invalid theme file ${source}: current theme format is version 2 and every file is self-contained.
${detail}`
    );
  }
  return result.data;
}
function registerBrandThemeFile(file) {
  registerTheme(file);
  return file.id;
}

// src/cli/theme-fork.ts
var ORDINARY_BACKGROUND_ANCHORS = ["bg", "surface", "primary", "accent", "text"];
var CHAPTER_BACKGROUND_ANCHORS = ["primary", "bg", "surface", "accent", "text"];
function rgbDistance(a, b) {
  const [ar, ag, ab] = hexToRgb(a);
  const [br, bg, bb] = hexToRgb(b);
  return Math.hypot(ar - br, ag - bg, ab - bb);
}
function resolveBackgroundAnchor(color, slideRole, source) {
  const roles = slideRole === "chapter" ? CHAPTER_BACKGROUND_ANCHORS : ORDINARY_BACKGROUND_ANCHORS;
  let best = roles[0];
  let bestDistance = rgbDistance(color, source[best]);
  for (const role of roles.slice(1)) {
    const distance = rgbDistance(color, source[role]);
    if (distance < bestDistance) {
      best = role;
      bestDistance = distance;
    }
  }
  return best;
}
function deriveBackgroundColor(color, slideRole, source, target) {
  const role = resolveBackgroundAnchor(color, slideRole, source);
  return rebaseRelativeColor(color, source[role], target[role], source.text, target.text);
}
function deriveBackground(spec, slideRole, source, target) {
  if (spec.kind === "color") {
    return { ...spec, value: deriveBackgroundColor(spec.value, slideRole, source, target) };
  }
  if (spec.kind === "gradient") {
    return {
      ...spec,
      from: deriveBackgroundColor(spec.from, slideRole, source, target),
      to: deriveBackgroundColor(spec.to, slideRole, source, target)
    };
  }
  if (spec.overlay !== void 0) {
    return {
      ...spec,
      overlay: {
        ...spec.overlay,
        color: deriveBackgroundColor(spec.overlay.color, slideRole, source, target)
      }
    };
  }
  return spec;
}
function rotatePaletteColor(color, sourceAnchor, targetAnchor) {
  const value = hexToHsl(color);
  const source = hexToHsl(sourceAnchor);
  const target = hexToHsl(targetAnchor);
  if (value.s <= 0.02 || source.s <= 0.02 || target.s <= 0.02) {
    return hslToHex(value);
  }
  return hslToHex({ ...value, h: value.h + hueDelta(source.h, target.h) });
}
function derivePaletteSequence(sequence, sourceAnchor, targetAnchor) {
  return [
    HexTokenSchema.parse(targetAnchor),
    ...sequence.slice(1).map((color) => rotatePaletteColor(color, sourceAnchor, targetAnchor))
  ];
}
var STATUS_CONTRAST_RATIO = 4.5;
var STATUS_LIGHTNESS_STEPS = 1e3;
function calibrateStatusColor(role, color, bg, surface) {
  const source = hexToHsl(color);
  const original = hslToHex(source);
  const clearsFloor = (candidate) => contrastRatio(candidate, bg) >= STATUS_CONTRAST_RATIO && contrastRatio(candidate, surface) >= STATUS_CONTRAST_RATIO;
  if (clearsFloor(original)) return original;
  let best;
  for (let step = 0; step <= STATUS_LIGHTNESS_STEPS; step++) {
    const lightness = step / STATUS_LIGHTNESS_STEPS;
    const candidate = hslToHex({ ...source, l: lightness });
    if (!clearsFloor(candidate)) continue;
    const distance = Math.abs(lightness - source.l);
    if (best === void 0 || distance < best.distance) best = { color: candidate, distance };
  }
  if (best !== void 0) return best.color;
  throw new PptwiseError(
    `cannot calibrate colors.${role} to a ${STATUS_CONTRAST_RATIO.toFixed(1)}:1 contrast ratio against both colors.bg (${bg}) and colors.surface (${surface}) while preserving its hue`
  );
}
function buildForkedTheme(source, anchors, identity) {
  const bg = HexTokenSchema.parse(anchors.bg ?? source.style.colors.bg);
  const primary = HexTokenSchema.parse(anchors.primary);
  const accent = HexTokenSchema.parse(anchors.accent ?? source.style.colors.accent);
  const text = HexTokenSchema.parse(anchors.text ?? source.style.colors.text);
  const surface = HexTokenSchema.parse(anchors.surface ?? source.style.colors.surface);
  const muted = deriveMuted(text, bg, surface);
  const sourceColors = source.style.colors;
  const sourceAnchors = {
    bg: sourceColors.bg,
    surface: sourceColors.surface,
    text: sourceColors.text,
    primary: sourceColors.primary,
    accent: sourceColors.accent
  };
  const targetAnchors = { bg, surface, text, primary, accent };
  const chartPalette = anchors.chartPalette ?? sourceColors.chartPalette;
  const chartAnchor = anchors.chartPalette === void 0 ? sourceColors.primary : chartPalette[0];
  const colors = {
    ...sourceColors,
    bg,
    primary,
    accent,
    text,
    surface,
    muted,
    chartPalette: derivePaletteSequence(chartPalette, chartAnchor, primary)
  };
  if (sourceColors.accentPool !== void 0) {
    colors.accentPool = derivePaletteSequence(sourceColors.accentPool, sourceColors.accent, accent);
  }
  if (sourceColors.panel !== void 0) {
    colors.panel = rebaseRelativeColor(sourceColors.panel, sourceColors.bg, bg, sourceColors.text, text);
  }
  if (sourceColors.border !== void 0) {
    colors.border = rebaseRelativeColor(sourceColors.border, sourceColors.surface, surface, sourceColors.text, text);
  }
  if (sourceColors.cardStroke !== void 0) {
    colors.cardStroke = rebaseRelativeColor(sourceColors.cardStroke, sourceColors.surface, surface, sourceColors.text, text);
  }
  if (sourceColors.emphasisInk !== void 0) {
    colors.emphasisInk = rebaseRelativeColor(sourceColors.emphasisInk, sourceColors.bg, bg, sourceColors.text, text);
  }
  if (sourceColors.danger !== void 0) {
    colors.danger = calibrateStatusColor("danger", sourceColors.danger, bg, surface);
  }
  if (sourceColors.warning !== void 0) {
    colors.warning = calibrateStatusColor("warning", sourceColors.warning, bg, surface);
  }
  if (sourceColors.success !== void 0) {
    colors.success = calibrateStatusColor("success", sourceColors.success, bg, surface);
  }
  const defaultBackgrounds = {
    cover: deriveBackground(source.style.defaultBackgrounds.cover, "cover", sourceAnchors, targetAnchors),
    chapter: deriveBackground(source.style.defaultBackgrounds.chapter, "chapter", sourceAnchors, targetAnchors),
    content: deriveBackground(source.style.defaultBackgrounds.content, "content", sourceAnchors, targetAnchors),
    ending: deriveBackground(source.style.defaultBackgrounds.ending, "ending", sourceAnchors, targetAnchors)
  };
  const file = {
    version: 2,
    id: identity.id,
    label: identity.label ?? source.label,
    style: {
      ...source.style,
      id: identity.id,
      colors,
      fonts: identity.fonts ?? source.style.fonts,
      defaultBackgrounds
    },
    brand: source.brand,
    occasions: source.occasions,
    identity: source.identity,
    // A fork changes the palette, never the handwriting. `emphasisInk` is
    // rebased above like every other color; the stroke that ink is applied
    // with belongs to the source theme and travels unchanged.
    emphasis: source.emphasis,
    // Same reasoning as `emphasis`: a fork repaints, it does not rewrite.
    // The palette changes, what the theme is for does not.
    story: source.story,
    menu: structuredClone(source.menu)
  };
  return ThemeFileSchema.parse(file);
}
function forkTheme(source, anchors, identity) {
  const file = buildForkedTheme(source, anchors, identity);
  assertContrastFloor(file.id, file.style);
  return file;
}

// src/spec/index.ts
import { z } from "zod";
var CommonPageSpecFields = {
  id: z.string(),
  heading: z.string(),
  /** Optional authoring hint pointing fill at a preferred content kind or component type, not a face. */
  focus: z.string().optional(),
  /** Free-text content anchor read by the fill step. */
  summary: z.string().optional(),
  /** A short label over the heading, drawn only by faces with a place for it. See the IR's `kicker`. */
  kicker: z.string().optional()
};
var PageSpecSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("cover"), ...CommonPageSpecFields }).strict(),
  z.object({ type: z.literal("chapter"), ...CommonPageSpecFields }).strict(),
  z.object({
    type: z.literal("content"),
    kind: z.enum(KIND_VALUES),
    ...CommonPageSpecFields
  }).strict(),
  z.object({ type: z.literal("ending"), ...CommonPageSpecFields }).strict()
]);
var DeckSpecSchema = z.object({
  version: z.literal("1").default("1"),
  // Same open-schema/closed-semantic split as PptxIRSchema's `narrative`
  // field — see `NarrativeProfileInputSchema`'s doc comment in `ir/index.ts`
  // for the full rationale (reused verbatim here, not redefined, so the
  // two can't drift apart). Field renamed from `scenario` to `narrative`
  // this task (spec §8.1's `DeckPlan`→`DeckSpec` rename, task 2) — its
  // *value* was already in the new strategy/pacing vocabulary as of task 1
  // (vocabulary-v4 rename) — `resolveNarrative` below is what actually
  // enforces that.
  narrative: z.union([z.string(), NarrativeProfileInputSchema]).optional(),
  theme: z.string({
    error: (iss) => iss.input === void 0 ? THEME_REQUIRED_MESSAGE : void 0
  }).regex(THEME_ID_PATTERN, THEME_ID_CONSTRAINT),
  filename: z.string().optional(),
  meta: MetaSchema.default({}),
  /** Deck logo placement — reused verbatim from the IR's own `brand` field
   *  (`BrandSchema`, `../ir`) so the deck spec and IR can't drift apart on
   *  shape, same pattern as `meta` just above. Unlike `meta`, no
   *  `.default({})`: IR's own `brand` field is a bare `.optional()` with no
   *  default either (`undefined` means "no brand", not "an empty brand
   *  object") — consumed by `Branding` (`src/render/branding.tsx`) for
   *  the deck's logo image and corner position. */
  brand: BrandSchema.optional(),
  /**
   * Where the brand footer and logo appear — reused verbatim from the IR's
   * own `branding` field (`DeckBrandingSchema`, `../ir`) so the spec and IR
   * cannot drift. Optional, no default: omitted stays unset and assemble
   * does not write `"cover-only"` into the IR. The renderer treats that
   * as `"cover-only"`. Omitted by default. Write `"full"` only when every
   * content page needs the brand footer. `"full"` also paints confidentiality
   * and date on cover and ending meta rows. A silent menu entry can suppress
   * branding for its own page.
   */
  branding: DeckBrandingSchema.optional(),
  /**
   * Small marks printed in the page corners, reused verbatim from the
   * IR's own `footer` field (`FooterSchema`, `../ir/footer`) so the spec
   * and IR cannot drift. Optional, no default: omitted, the deck prints
   * none of them, and assemble writes nothing into the IR.
   */
  footer: FooterSchema.optional(),
  /**
   * The stages the talk runs through, reused verbatim from the IR's own
   * `course` field (`CourseSchema`, `../ir`) so the spec and IR cannot
   * drift. Optional, no default. Each page file names its own `stage`.
   */
  course: CourseSchema.optional(),
  pages: z.array(PageSpecSchema)
}).strict();
function specJsonSchema() {
  return z.toJSONSchema(DeckSpecSchema);
}
function formatSpecIssues(errors) {
  return errors.map((e) => e.pageId ? `page "${e.pageId}" \u2014 ${e.path}: ${e.message}` : `${e.path}: ${e.message}`).join("\n");
}
function formatInvalidSpecError(errors) {
  return `invalid spec (${errors.length} issue${errors.length === 1 ? "" : "s"}):
${formatSpecIssues(errors)}`;
}
function resolveSpecThemeId(spec) {
  return foldedThemeTarget(spec.theme) ?? spec.theme;
}
function checkPagesNonEmpty(spec) {
  if (spec.pages.length > 1) return [];
  if (spec.pages.length === 1) {
    return [
      {
        path: "pages",
        message: "spec has 1 page \u2014 a deck opens with a cover and closes with an ending page, so the shortest deck is 2 pages (cover and ending) or 3 (with one content page). If the user asked for one page, ask them which of those they want. Do not add pages on your own"
      }
    ];
  }
  return [{ path: "pages", message: "spec has no pages \u2014 a spec needs at least a cover page and an ending page" }];
}
function checkBoundaryTypes(spec) {
  const { pages } = spec;
  const errors = [];
  const first = pages[0];
  const last = pages[pages.length - 1];
  if (first.type !== "cover") {
    errors.push({
      path: "pages.0.type",
      pageId: first.id,
      message: `first page must be type "cover" (got "${first.type}") \u2014 a spec must open with a cover page`
    });
  }
  if (last.type !== "ending") {
    errors.push({
      path: `pages.${pages.length - 1}.type`,
      pageId: last.id,
      message: `last page must be type "ending" (got "${last.type}") \u2014 a spec must close with an ending page`
    });
  }
  for (let i = 1; i < pages.length - 1; i++) {
    const page = pages[i];
    if (page.type === "cover" || page.type === "ending") {
      errors.push({
        path: `pages.${i}.type`,
        pageId: page.id,
        message: `page "${page.id}" is type "${page.type}", only allowed as the first (cover) or last (ending) page \u2014 use "content" or "chapter" for interior pages`
      });
    }
  }
  return errors;
}
function isUnsafePageId(id) {
  return id.includes("/") || id.includes("\\") || id === "..";
}
function checkPageIds(spec) {
  const errors = [];
  const seen = /* @__PURE__ */ new Map();
  spec.pages.forEach((page, i) => {
    if (page.id.trim() === "") {
      errors.push({ path: `pages.${i}.id`, message: `page ${i + 1} has an empty id \u2014 every page needs a non-empty, unique id` });
      return;
    }
    if (isUnsafePageId(page.id)) {
      errors.push({
        path: `pages.${i}.id`,
        pageId: page.id,
        message: `page id "${page.id}" is not a safe file name \u2014 ids used as page/asset file names must not contain path separators or ".."`
      });
      return;
    }
    const indices = seen.get(page.id);
    if (indices) indices.push(i);
    else seen.set(page.id, [i]);
  });
  for (const [id, indices] of seen) {
    if (indices.length < 2) continue;
    errors.push({
      path: "pages",
      pageId: id,
      message: `duplicate page id "${id}" used by ${indices.length} pages (positions ${indices.map((i) => i + 1).join(", ")}) \u2014 page ids must be unique within a spec`
    });
  }
  return errors;
}
var HEADING_MAX_CHARS = CAPACITY.headingMaxChars;
function specHeadingLength(heading) {
  return stripEmphasis(heading).length;
}
function checkHeadings(spec) {
  const errors = [];
  spec.pages.forEach((page, i) => {
    if (page.heading.trim() === "") {
      errors.push({ path: `pages.${i}.heading`, pageId: page.id, message: `page "${page.id}" is missing a required heading` });
      return;
    }
    const length = specHeadingLength(page.heading);
    if (length > HEADING_MAX_CHARS) {
      errors.push({
        path: `pages.${i}.heading`,
        pageId: page.id,
        message: `page "${page.id}" heading is ${length} characters, exceeds the ${HEADING_MAX_CHARS}-character limit \u2014 tighten it into a short, assertive phrase`
      });
    }
  });
  return errors;
}
function checkOverflowVocabulary(spec) {
  const errors = [];
  const consider = (root, prefix) => {
    visitStringLeaves(root, prefix, (path, text) => {
      if (!text || !findOverflowVocabulary(text)) return;
      const m = /^pages\.(\d+)/.exec(path);
      const page = m ? spec.pages[Number(m[1])] : void 0;
      errors.push({
        path,
        message: OVERFLOW_VOCABULARY_MESSAGE,
        ...page?.id !== void 0 ? { pageId: page.id } : {}
      });
    });
  };
  consider(spec.meta, "meta");
  consider(spec.footer, "footer");
  consider(spec.course, "course");
  consider(spec.pages, "pages");
  return errors;
}
function resolveSpecTheme(spec, theme) {
  const themeId = resolveSpecThemeId(spec);
  const resolved = resolveBoundThemeResult(themeId, theme);
  if (resolved.ok) return resolved;
  if (resolved.reason === "mismatch") {
    return {
      ok: false,
      errors: [
        {
          path: "theme",
          message: `spec binds theme "${themeId}" but the supplied theme definition is "${resolved.suppliedId}"`
        }
      ]
    };
  }
  const renamed = RETIRED_THEME_IDS[themeId];
  const message = themeId === "bloom" ? 'theme id "bloom" was removed \u2014 current format uses an installed theme id (see `pptwise themes`)' : renamed !== void 0 ? `theme id "${themeId}" was renamed to "${renamed}" \u2014 bind the spec to the new id (see \`pptwise themes\`)` : `unknown theme "${themeId}" \u2014 available: ${resolved.installed.join(", ")} (see \`pptwise themes\`)`;
  return { ok: false, errors: [{ path: "theme", message }] };
}
function checkFocusVocabulary(spec) {
  const kinds = KIND_VALUES;
  const errors = [];
  spec.pages.forEach((page, i) => {
    if (page.focus === void 0) return;
    if (page.focus === "tag_row") {
      errors.push({
        path: `pages.${i}.focus`,
        pageId: page.id,
        message: 'component type "tag_row" was removed \u2014 short labels belong in bullets or icon_cards'
      });
      return;
    }
    if (page.focus === "citation") {
      errors.push({
        path: `pages.${i}.focus`,
        pageId: page.id,
        message: 'component type "citation" was removed \u2014 a reference list is document content, not slide content. Name a source on the component that rests on it, in its own "source" field'
      });
      return;
    }
    if (page.focus === "banner-heading") {
      errors.push({
        path: `pages.${i}.focus`,
        pageId: page.id,
        message: '"banner-heading" is a face id, not authoring vocabulary \u2014 focus accepts a content kind or a component type'
      });
      return;
    }
    if (kinds.includes(page.focus) || COMPONENT_TYPES.includes(page.focus)) {
      return;
    }
    errors.push({
      path: `pages.${i}.focus`,
      pageId: page.id,
      message: `unknown focus "${page.focus}" \u2014 expected a content kind (${KIND_VALUES.join(", ")}) or a component type (${COMPONENT_TYPES.join(", ")})`
    });
  });
  return errors;
}
function checkThemeMenuKinds(spec, theme) {
  const menu = theme.menu;
  if (menu === void 0) {
    return {
      errors: [{ path: "theme", message: `theme "${resolveSpecThemeId(spec)}" has no menu` }],
      landings: []
    };
  }
  const themeId = resolveSpecThemeId(spec);
  const offered = offeredContentKinds(menu);
  const errors = [];
  const landings = [];
  spec.pages.forEach((page, index) => {
    if (page.type !== "content") return;
    const candidates = landingCandidates(page.kind, menu);
    if (candidates[0] === page.kind) return;
    const path = `pages.${index}.kind`;
    if (candidates.length === 0) {
      errors.push({
        path,
        pageId: page.id,
        message: `kind "${page.kind}" is not offered by theme "${themeId}", and neither is any kind it can stand in for (${KIND_LANDING[page.kind].join(", ")}). Available content kinds: ${offered.join(", ")}`
      });
      return;
    }
    const [first, ...rest] = candidates;
    const others = rest.length > 0 ? `, or on ${rest.map((kind) => `"${kind}"`).join(" or ")} when its components need that face` : "";
    landings.push({
      path,
      pageId: page.id,
      kind: page.kind,
      lands: candidates,
      message: `theme "${themeId}" offers no "${page.kind}" page: this one is drawn as "${first}"${others}. Nothing to change in the spec`
    });
  });
  return { errors, landings };
}
function checkKindDistribution(spec) {
  const contentPages = spec.pages.map((page, index) => ({ page, index })).filter(
    (entry) => entry.page.type === "content"
  );
  const warnings = [];
  let start = 0;
  while (start < contentPages.length) {
    let end = start + 1;
    while (end < contentPages.length && contentPages[end].page.kind === contentPages[start].page.kind) end++;
    if (end - start >= 3) {
      const run = contentPages.slice(start, end);
      warnings.push({
        path: "pages",
        pageId: run[0].page.id,
        message: `${run.length} consecutive content pages use kind "${run[0].page.kind}" (${run.map((entry) => entry.page.id).join(", ")}). Vary the explanation pattern where the argument allows it`
      });
    }
    start = end;
  }
  return warnings;
}
var SPEC_PAGE_COUNT_RANGE = {
  dense: { min: 8, max: 30 },
  balanced: { min: 6, max: 24 },
  spacious: { min: 4, max: 16 }
};
function checkPageCount(spec, pacing) {
  const { min, max } = SPEC_PAGE_COUNT_RANGE[pacing];
  const n = spec.pages.length;
  if (n >= min && n <= max) return [];
  return [
    {
      path: "pages",
      message: `spec has ${n} pages, outside the ${min}-${max} that "${pacing}" pacing usually spans. If the user asked for ${n} pages, keep ${n}: this is advice, not an error. Otherwise reconsider the page count`
    }
  ];
}
function pageIdFromRawInput(input, index) {
  if (typeof input !== "object" || input === null) return void 0;
  const pages = input.pages;
  if (!Array.isArray(pages)) return void 0;
  const page = pages[index];
  if (typeof page !== "object" || page === null) return void 0;
  const id = page.id;
  return typeof id === "string" ? id : void 0;
}
function specThemeFoldWarning(input) {
  if (typeof input !== "object" || input === null || Array.isArray(input)) return void 0;
  const theme = input.theme;
  if (typeof theme !== "string") return void 0;
  const message = foldedThemeWarning(theme);
  return message === void 0 ? void 0 : { path: "theme", message };
}
function validateSpec(input, opts) {
  const rootAliasPass = normalizeDeckRootAliases(input);
  const narrativeShapePass = normalizeNarrativeShape(rootAliasPass.value);
  const normalizedInput = narrativeShapePass.value;
  const normalized = [...rootAliasPass.normalized, ...narrativeShapePass.normalized];
  const foldWarning = specThemeFoldWarning(normalizedInput);
  const withNormalized = (result) => {
    const noted = normalized.length > 0 ? { ...result, normalized } : result;
    if (foldWarning === void 0) return noted;
    return { ...noted, warnings: [foldWarning, ...noted.warnings ?? []] };
  };
  const r = DeckSpecSchema.safeParse(normalizedInput);
  if (!r.success) {
    const errors = r.error.issues.map((issue) => {
      const path = issue.path.join(".");
      const m = /^pages\.(\d+)/.exec(path);
      return {
        path,
        message: themeIssueMessage(path, issue.message, issue.input, issue.code),
        pageId: m ? pageIdFromRawInput(normalizedInput, Number(m[1])) : void 0
      };
    });
    return withNormalized({ ok: false, errors });
  }
  const spec = r.data;
  const emptyErrors = checkPagesNonEmpty(spec);
  if (emptyErrors.length > 0) return withNormalized({ ok: false, errors: emptyErrors });
  const boundaryErrors = checkBoundaryTypes(spec);
  if (boundaryErrors.length > 0) return withNormalized({ ok: false, errors: boundaryErrors });
  const idErrors = checkPageIds(spec);
  if (idErrors.length > 0) return withNormalized({ ok: false, errors: idErrors });
  const headingErrors = checkHeadings(spec);
  if (headingErrors.length > 0) return withNormalized({ ok: false, errors: headingErrors });
  const overflowVocabularyErrors = checkOverflowVocabulary(spec);
  if (overflowVocabularyErrors.length > 0) return withNormalized({ ok: false, errors: overflowVocabularyErrors });
  const footerErrors = footerSettingIssues({ meta: spec.meta, footer: spec.footer });
  if (footerErrors.length > 0) return withNormalized({ ok: false, errors: footerErrors });
  const boundTheme = resolveSpecTheme(spec, opts?.theme);
  if (!boundTheme.ok) return withNormalized({ ok: false, errors: boundTheme.errors });
  const menu = checkThemeMenuKinds(spec, boundTheme.theme);
  if (menu.errors.length > 0) return withNormalized({ ok: false, errors: menu.errors });
  let resolvedAxes;
  try {
    resolvedAxes = resolveNarrative(spec.narrative);
  } catch (err) {
    if (!(err instanceof PptwiseError)) throw err;
    return withNormalized({ ok: false, errors: [{ path: "narrative", message: err.message }] });
  }
  const focusErrors = checkFocusVocabulary(spec);
  if (focusErrors.length > 0) return withNormalized({ ok: false, errors: focusErrors });
  const warnings = [...checkPageCount(spec, resolvedAxes.pacing), ...checkKindDistribution(spec)];
  return withNormalized({
    ok: true,
    spec,
    errors: [],
    ...warnings.length > 0 ? { warnings } : {},
    ...menu.landings.length > 0 ? { landings: menu.landings } : {}
  });
}

// src/spec/assemble.ts
var PAGE_FILL_FIELDS = ["components", "background", "image_side", "footnote", "fields", "stamp", "tag", "ballot", "years", "stage", "notes"];
var LOCKED_KEYS = ["type", "kind", "heading", "kicker"];
function buildSlide(page, content) {
  const locked = {
    id: page.id,
    type: page.type,
    heading: page.heading,
    ...page.type === "content" ? { kind: page.kind } : {},
    ...page.kicker !== void 0 ? { kicker: page.kicker } : {}
  };
  if (content === void 0) {
    return {
      ...locked,
      placeholder: true,
      ...page.summary !== void 0 ? { subheading: page.summary } : {}
    };
  }
  const filled = {};
  for (const field of PAGE_FILL_FIELDS) {
    if (content[field] !== void 0) filled[field] = content[field];
  }
  return {
    ...locked,
    ...page.type !== "content" && page.summary !== void 0 ? { subheading: page.summary } : {},
    ...filled
  };
}
function assembleDeck(spec, pages, opts) {
  const validated = validateSpec(spec, opts);
  if (!validated.ok) throw new PptwiseError(formatInvalidSpecError(validated.errors));
  const deckSpec = validated.spec;
  for (const page of deckSpec.pages) {
    const raw = pages[page.id];
    if (raw === void 0) continue;
    if (typeof raw !== "object" || raw === null || Array.isArray(raw)) {
      throw new PptwiseError(`page "${page.id}": page content must be an object`);
    }
    for (const key of LOCKED_KEYS) {
      if (Object.hasOwn(raw, key)) {
        throw new PptwiseError(`page "${page.id}": "${key}" is locked by the spec. Remove it from the page file`);
      }
    }
  }
  const specIds = new Set(deckSpec.pages.map((page) => page.id));
  const orphanIds = Object.keys(pages).filter((id) => !specIds.has(id));
  if (orphanIds.length > 0) {
    throw new PptwiseError(
      `orphan page id${orphanIds.length === 1 ? "" : "s"} ${orphanIds.map((id) => `"${id}"`).join(", ")}. Delete the page file or add the page to the spec`
    );
  }
  const rawIr = {
    version: "5",
    ...deckSpec.narrative !== void 0 ? { narrative: deckSpec.narrative } : {},
    theme: { id: deckSpec.theme },
    ...deckSpec.filename !== void 0 ? { filename: deckSpec.filename } : {},
    ...deckSpec.brand !== void 0 ? { brand: deckSpec.brand } : {},
    ...deckSpec.branding !== void 0 ? { branding: deckSpec.branding } : {},
    ...deckSpec.footer !== void 0 ? { footer: deckSpec.footer } : {},
    ...deckSpec.course !== void 0 ? { course: deckSpec.course } : {},
    meta: deckSpec.meta,
    slides: deckSpec.pages.map((page) => buildSlide(page, pages[page.id]))
  };
  const parsed = PptxIRSchema.safeParse(rawIr);
  if (!parsed.success) {
    const detail = parsed.error.issues.map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`).join("\n");
    throw new PptwiseError(`assembled deck did not produce valid IR:
${detail}`);
  }
  return { ir: parsed.data, spec: deckSpec };
}
var UNTITLED_HEADING = "Untitled";
function disassembleDeck(ir) {
  const pages = {};
  const pageSpecs = ir.slides.map((slide, index) => {
    const id = slide.id ?? `p-${index + 1}-${slide.type}`;
    const heading = slide.heading !== void 0 && slide.heading.trim() !== "" ? slide.heading : UNTITLED_HEADING;
    const pageSpec = {
      id,
      type: slide.type,
      heading,
      ...slide.type === "content" ? { kind: slide.kind } : {},
      ...slide.kicker !== void 0 ? { kicker: slide.kicker } : {},
      ...(slide.placeholder === true || slide.type !== "content") && slide.subheading !== void 0 ? { summary: slide.subheading } : {}
    };
    if (slide.placeholder !== true) pages[id] = extractPageContent(slide);
    return pageSpec;
  });
  return {
    spec: {
      version: "1",
      ...ir.narrative !== void 0 ? { narrative: ir.narrative } : {},
      theme: ir.theme.id,
      filename: ir.filename,
      ...ir.brand !== void 0 ? { brand: ir.brand } : {},
      ...ir.branding !== void 0 ? { branding: ir.branding } : {},
      ...ir.footer !== void 0 ? { footer: ir.footer } : {},
      ...ir.course !== void 0 ? { course: ir.course } : {},
      meta: ir.meta,
      pages: pageSpecs
    },
    pages
  };
}
function extractPageContent(slide) {
  const content = {};
  if (slide.components.length > 0) content.components = slide.components;
  if (slide.background !== void 0) content.background = slide.background;
  if (slide.image_side !== void 0) content.image_side = slide.image_side;
  if (slide.footnote !== void 0) content.footnote = slide.footnote;
  if (slide.fields !== void 0) content.fields = slide.fields;
  if (slide.stamp !== void 0) content.stamp = slide.stamp;
  if (slide.tag !== void 0) content.tag = slide.tag;
  if (slide.ballot !== void 0) content.ballot = slide.ballot;
  if (slide.years !== void 0) content.years = slide.years;
  if (slide.stage !== void 0) content.stage = slide.stage;
  if (slide.notes !== void 0) content.notes = slide.notes;
  return content;
}

// src/render/asset-brief.ts
var DUMMY_PNG_DATA_URI = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=";
function extractImageFrames(markup) {
  const Parser = getPlatform().domParser ?? globalThis.DOMParser;
  if (!Parser) {
    throw new Error(
      'DOMParser unavailable \u2014 in Node, call installNodePlatform() from "@liustack/pptwise/node" first (the pptwise CLI does this automatically)'
    );
  }
  const doc = new Parser().parseFromString(markup, "image/svg+xml");
  const byAssetId = /* @__PURE__ */ new Map();
  const visit = (el, ox, oy, os) => {
    const { dx, dy, scale } = parseTransform(el);
    const ax = ox + os * dx;
    const ay = oy + os * dy;
    const as = os * scale;
    if (el.tagName.toLowerCase() === "image") {
      const href = el.getAttribute("href") ?? "";
      const hashAt = href.indexOf("#");
      if (hashAt !== -1) {
        const assetId = href.slice(hashAt + 1);
        const frame = {
          x: ax + as * Number(el.getAttribute("x") ?? 0),
          y: ay + as * Number(el.getAttribute("y") ?? 0),
          w: as * Number(el.getAttribute("width") ?? 0),
          h: as * Number(el.getAttribute("height") ?? 0),
          preserveAspectRatio: el.getAttribute("preserveAspectRatio") ?? "xMidYMid meet"
        };
        const list = byAssetId.get(assetId);
        if (list) list.push(frame);
        else byAssetId.set(assetId, [frame]);
      }
    }
    for (const child of Array.from(el.children)) visit(child, ax, ay, as);
  };
  visit(doc.documentElement, 0, 0, 1);
  return byAssetId;
}
function gcd(a, b) {
  let x = Math.abs(Math.round(a));
  let y = Math.abs(Math.round(b));
  while (y !== 0) [x, y] = [y, x % y];
  return x || 1;
}
function formatAspect(w, h) {
  if (h <= 0 || w <= 0) return `${w}:${h}`;
  const ratio = w / h;
  const TOL = 0.01;
  for (let d = 1; d <= 12; d++) {
    const n = Math.round(ratio * d);
    if (n >= 1 && Math.abs(ratio - n / d) <= TOL) {
      const g = gcd(n, d);
      return `${n / g}:${d / g}`;
    }
  }
  return `${ratio.toFixed(2)}:1`;
}
function toFrame(raw) {
  const w = Math.round(raw.w);
  const h = Math.round(raw.h);
  return { x: Math.round(raw.x), y: Math.round(raw.y), w, h, aspect: formatAspect(w, h) };
}
function buildFit(mode, aspect) {
  if (mode === "cover") {
    return {
      mode,
      note: aspect ? `Cover crop (xMidYMid slice): generate close to ${aspect} to avoid any crop \u2014 otherwise the renderer center-crops to fill the frame, so keep essential subject matter within the center safe zone.` : `Cover crop (xMidYMid slice): the renderer center-crops to fill the frame \u2014 keep essential subject matter centered.`
    };
  }
  return {
    mode,
    note: aspect ? `Contain fit (xMidYMid meet): the renderer letterboxes to show the whole image inside the frame with no crop \u2014 match ${aspect} to avoid empty margins.` : `Contain fit (xMidYMid meet): the renderer letterboxes to show the whole image inside the frame with no crop.`
  };
}
function buildPalette(colors) {
  const candidates = [colors.bg, colors.surface, colors.panel, colors.primary, colors.accent, colors.text, colors.muted, colors.border];
  const hexes = [...new Set(candidates.filter((c) => Boolean(c)))];
  return { hexes, primary: colors.primary, accent: colors.accent };
}
function themeLabel(id) {
  return CANONICAL_THEME_IDS.includes(id) ? THEME_LABELS[id] : id;
}
function humanizeMotif(motif) {
  return motif.replace(/-motif$/, "").replace(/-/g, " ");
}
function buildMood(themeId, themeDef) {
  const label = themeLabel(themeId);
  const tagPhrase = themeDef.tags.length > 0 ? ` (${themeDef.tags.join(", ")})` : "";
  const motifPhrase = themeDef.motif ? ` with a ${humanizeMotif(themeDef.motif)} decorative motif` : "";
  return { tags: themeDef.tags, description: `${label} theme${tagPhrase}${motifPhrase}.` };
}
function buildPrompt(mood, palette, frame, fit) {
  const supporting = palette.hexes.filter((h) => h !== palette.primary && h !== palette.accent);
  const paletteText = `Color palette: primary ${palette.primary}, accent ${palette.accent}${supporting.length > 0 ? `, supporting tones ${supporting.join(", ")}` : ""}.`;
  const compositionText = frame ? `Compose for a ${frame.aspect} frame. ${fit.note}` : `Frame geometry unavailable \u2014 this image slot was not rendered under the deck's currently selected layout; generate at a versatile aspect ratio and verify placement once a layout renders it.`;
  return `${mood.description} ${paletteText} ${compositionText}`;
}
function buildAssetBrief(ir, opts) {
  const themeDef = resolveIrTheme(ir, opts?.theme);
  const palette = buildPalette(themeDef.style.colors);
  const mood = buildMood(ir.theme.id, themeDef);
  const occurrences = [];
  ir.slides.forEach((slide, slideIndex) => {
    for (const component of slide.components) {
      if (component.type === "image") occurrences.push({ slideIndex, component });
    }
  });
  const overrides = {};
  for (const { component } of occurrences) {
    overrides[component.asset_id] = { src: `${DUMMY_PNG_DATA_URI}#${component.asset_id}` };
  }
  const renderIr = { ...ir, assets: { images: { ...ir.assets.images, ...overrides } } };
  const framesBySlide = /* @__PURE__ */ new Map();
  for (const slideIndex of new Set(occurrences.map((o) => o.slideIndex))) {
    framesBySlide.set(slideIndex, extractImageFrames(renderSlideSvg(renderIr, slideIndex, { theme: themeDef })));
  }
  const items = [];
  ir.slides.forEach((slide, slideIndex) => {
    const groups = /* @__PURE__ */ new Map();
    for (const component of slide.components) {
      if (component.type !== "image") continue;
      const list = groups.get(component.asset_id);
      if (list) list.push(component);
      else groups.set(component.asset_id, [component]);
    }
    if (groups.size === 0) return;
    const page = { index: slideIndex, id: slide.id, type: slide.type, heading: slide.heading };
    const frameMap = framesBySlide.get(slideIndex);
    const isMissing = (assetId) => !ir.assets.images[assetId]?.src;
    const altOf = (assetId) => ir.assets.images[assetId]?.alt;
    for (const [assetId, group] of groups) {
      const frames = frameMap?.get(assetId) ?? [];
      if (group.length === 1) {
        const raw = frames[0];
        const frame = raw ? toFrame(raw) : void 0;
        const fit = buildFit(group[0].fit, frame?.aspect);
        items.push({
          page,
          asset_id: assetId,
          alt: altOf(assetId),
          kind: "image",
          missing: isMissing(assetId),
          rendered: frame !== void 0,
          frame,
          suggested_pixels: frame ? { w: frame.w * 2, h: frame.h * 2 } : void 0,
          fit,
          palette,
          mood,
          suggested_prompt: buildPrompt(mood, palette, frame, fit)
        });
        continue;
      }
      const occurrenceCount = group.length;
      const sharedFit = group[0].fit;
      const missing = isMissing(assetId);
      for (const raw of frames) {
        const frame = toFrame(raw);
        const fit = buildFit(sharedFit, frame.aspect);
        items.push({
          page,
          asset_id: assetId,
          alt: altOf(assetId),
          kind: "image",
          missing,
          rendered: true,
          frame,
          suggested_pixels: { w: frame.w * 2, h: frame.h * 2 },
          fit,
          palette,
          mood,
          shared: true,
          occurrenceCount,
          suggested_prompt: buildPrompt(mood, palette, frame, fit)
        });
      }
      for (let i = frames.length; i < occurrenceCount; i++) {
        const fit = buildFit(sharedFit, void 0);
        items.push({
          page,
          asset_id: assetId,
          alt: altOf(assetId),
          kind: "image",
          missing,
          rendered: false,
          fit,
          palette,
          mood,
          shared: true,
          occurrenceCount,
          suggested_prompt: buildPrompt(mood, palette, void 0, fit)
        });
      }
    }
  });
  return { theme: ir.theme.id, items };
}

export {
  VERSION,
  componentsForKind,
  kindJsonSchema,
  THEME_PRESETS,
  isThemePresetId,
  getThemePreset,
  copyThemePreset,
  themeFileFromPreset,
  regenerateFromBrand,
  describePlacement,
  parseBrandOption,
  slugify,
  extractBrandTheme,
  BrandThemeFileSchema,
  parseBrandThemeFile,
  registerBrandThemeFile,
  forkTheme,
  PageSpecSchema,
  DeckSpecSchema,
  specJsonSchema,
  formatSpecIssues,
  formatInvalidSpecError,
  resolveSpecThemeId,
  SPEC_PAGE_COUNT_RANGE,
  validateSpec,
  PAGE_FILL_FIELDS,
  assembleDeck,
  disassembleDeck,
  buildAssetBrief
};
//# sourceMappingURL=chunk-EN3GZEQR.js.map