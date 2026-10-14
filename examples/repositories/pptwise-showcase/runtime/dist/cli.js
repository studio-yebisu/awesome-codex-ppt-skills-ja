#!/usr/bin/env node
import {
  PAGE_FILL_FIELDS,
  VERSION,
  assembleDeck,
  buildAssetBrief,
  describePlacement,
  disassembleDeck,
  extractBrandTheme,
  forkTheme,
  formatInvalidSpecError,
  kindJsonSchema,
  parseBrandOption,
  parseBrandThemeFile,
  regenerateFromBrand,
  resolveSpecThemeId,
  slugify,
  specJsonSchema,
  themeFileFromPreset,
  validateSpec
} from "./chunk-EN3GZEQR.js";
import {
  installNodePlatform,
  isMissingModuleError,
  proxyFetch
} from "./chunk-CE2HUEOP.js";
import {
  AUDIENCE_VALUES,
  BOUNDARY_UNRENDERED_FIELDS,
  BUILTIN_THEME_IDS,
  CANONICAL_THEME_IDS,
  CANVAS_H_PX,
  CANVAS_W_PX,
  CAPACITY,
  COMPONENT_TYPES,
  FORMAT_BY_MIME,
  FULL_BODY_TYPES,
  IDENTITY_STRENGTHS,
  LAYOUT_REGISTRY,
  MIME_BY_SNIFFED_FORMAT,
  NARRATIVE_PRESETS,
  OCCASION_VOCAB,
  PACING_BUDGETS,
  PPTX_ICON_NAMES,
  PptwiseError,
  RECIPES,
  RETIRED_THEME_IDS,
  STEP_ASIDE_ATTR,
  STRATEGY_DEFINITIONS,
  STRATEGY_VALUES,
  THEME_DEFINITIONS,
  THEME_ID_CONSTRAINT,
  THEME_ID_PATTERN,
  THEME_OCCASIONS,
  ThemeFileSchema,
  architecture_exports,
  assertComponentType,
  assertNotRetiredThemeId,
  auditDeck,
  blockquote_exports,
  bmc_exports,
  bullets_exports,
  callout_exports,
  chart_exports,
  chevron_process_exports,
  code_exports,
  comparison_exports,
  compileThemeDefinition,
  componentFace,
  componentJsonSchema,
  concept_equation_exports,
  contentPageDensity,
  cycle_exports,
  data_table_exports,
  decision_tree_exports,
  describeShape,
  device_mockup_exports,
  drawSlide,
  dropPhrase,
  faceAcceptedComponentTypes,
  fishbone_exports,
  five_forces_exports,
  flowchart_exports,
  foldedThemeTarget,
  formatIssues,
  formatWarnings,
  from_to_exports,
  gantt_exports,
  generatePptx,
  getLayout,
  getThemeDefinition,
  harvey_balls_exports,
  heatmap_exports,
  hub_spoke_exports,
  iceberg_exports,
  icon_cards_exports,
  image_compare_exports,
  image_exports,
  image_grid_exports,
  insight_panel_exports,
  irJsonSchema,
  issue_tree_exports,
  journey_map_exports,
  kpi_cards_exports,
  landingCandidates,
  listThemes,
  logo_wall_exports,
  matrix_exports,
  numbered_cards_exports,
  offeredContentKinds,
  org_tree_exports,
  paragraph_exports,
  parseDropKind,
  people_cards_exports,
  pest_exports,
  pictogram_exports,
  pillar_model_exports,
  positioning_map_exports,
  product_cards_exports,
  progress_donuts_exports,
  pros_cons_exports,
  pyramid_exports,
  quote_wall_exports,
  reachableDefs,
  renderSlideSvg,
  resolveEffectiveFace,
  resolveFontFace,
  resolveIrTheme,
  resolveNarrative,
  retiredThemeIdMessage,
  rings_exports,
  roadmap_exports,
  row_cards_exports,
  sankey_exports,
  scorecard_exports,
  segmented_wheel_exports,
  shapeGaps,
  shapesIn,
  sketch_exports,
  sniffImageFormat,
  staircase_exports,
  steps_exports,
  swimlane_exports,
  swot_exports,
  timeline_exports,
  validateIr,
  value_chain_exports,
  venn_exports,
  verdict_banner_exports,
  waterfall_exports,
  word_cloud_exports,
  writesHeading
} from "./chunk-DQABTUNM.js";
import {
  getPlatform
} from "./chunk-RHKPZSTM.js";

// src/cli.ts
import { Command } from "commander";

// src/cli/commands.ts
import { mkdir as mkdir6, readFile as readFile7, rm as rm3, writeFile as writeFile7 } from "fs/promises";
import { basename as basename5, dirname as dirname6, isAbsolute as isAbsolute4, join as join11, relative as relative3, resolve as resolve7 } from "path";

// src/ir/components/stories.ts
var COMPONENT_STORY_MODULES = {
  architecture: architecture_exports,
  blockquote: blockquote_exports,
  bmc: bmc_exports,
  bullets: bullets_exports,
  callout: callout_exports,
  chart: chart_exports,
  chevron_process: chevron_process_exports,
  code: code_exports,
  comparison: comparison_exports,
  concept_equation: concept_equation_exports,
  cycle: cycle_exports,
  data_table: data_table_exports,
  decision_tree: decision_tree_exports,
  device_mockup: device_mockup_exports,
  fishbone: fishbone_exports,
  five_forces: five_forces_exports,
  flowchart: flowchart_exports,
  from_to: from_to_exports,
  gantt: gantt_exports,
  heatmap: heatmap_exports,
  hub_spoke: hub_spoke_exports,
  icon_cards: icon_cards_exports,
  image_compare: image_compare_exports,
  image_grid: image_grid_exports,
  image: image_exports,
  insight_panel: insight_panel_exports,
  journey_map: journey_map_exports,
  kpi_cards: kpi_cards_exports,
  matrix: matrix_exports,
  numbered_cards: numbered_cards_exports,
  paragraph: paragraph_exports,
  people_cards: people_cards_exports,
  pest: pest_exports,
  positioning_map: positioning_map_exports,
  progress_donuts: progress_donuts_exports,
  logo_wall: logo_wall_exports,
  product_cards: product_cards_exports,
  quote_wall: quote_wall_exports,
  pros_cons: pros_cons_exports,
  sketch: sketch_exports,
  rings: rings_exports,
  roadmap: roadmap_exports,
  row_cards: row_cards_exports,
  sankey: sankey_exports,
  staircase: staircase_exports,
  segmented_wheel: segmented_wheel_exports,
  steps: steps_exports,
  swimlane: swimlane_exports,
  swot: swot_exports,
  timeline: timeline_exports,
  venn: venn_exports,
  verdict_banner: verdict_banner_exports,
  waterfall: waterfall_exports,
  org_tree: org_tree_exports,
  issue_tree: issue_tree_exports,
  pyramid: pyramid_exports,
  iceberg: iceberg_exports,
  pillar_model: pillar_model_exports,
  value_chain: value_chain_exports,
  harvey_balls: harvey_balls_exports,
  scorecard: scorecard_exports,
  pictogram: pictogram_exports,
  word_cloud: word_cloud_exports
};
var COMPONENT_STORY_TYPES = Object.keys(COMPONENT_STORY_MODULES);
function componentStory(type) {
  return COMPONENT_STORY_MODULES[type]?.story;
}

// src/layouts/signature.ts
function faceCompositions(layout, params) {
  const declared = layout?.compositions;
  return typeof declared === "function" ? declared(params) : declared;
}
function signatureOffers(offered) {
  if (offered === void 0) return [];
  return offered.offer.map((id) => ({ id, recipe: RECIPES[id], shapes: shapesIn(RECIPES[id], offered.setting) })).filter((offer) => offer.shapes.length > 0);
}
function splitByKind(offers, kinds) {
  const forPage = offers.filter((offer) => offer.recipe.kinds.some((kind) => kinds.includes(kind)));
  return { forPage, others: offers.filter((offer) => !forPage.includes(offer)) };
}
function pageOffers(ir, slide, theme2) {
  if (slide.type !== "content") return void 0;
  const effective = resolveEffectiveFace(ir, slide, theme2);
  if (effective.route === "unresolved" || effective.layoutId === null) return void 0;
  const offered = faceCompositions(effective.layout, effective.entry?.params);
  const offers = signatureOffers(offered);
  if (offered === void 0 || offers.length === 0) return void 0;
  const kinds = effective.servedKind !== void 0 && effective.servedKind !== slide.kind ? [slide.kind, effective.servedKind] : [slide.kind];
  return { face: effective.layoutId, ...splitByKind(offers, kinds), subheadingDeclines: offered.subheading === "declines" };
}
function pageGaps(slide, shape, subheadingDeclines) {
  const gaps = shapeGaps(shape, slide);
  return subheadingDeclines && slide.subheading?.trim() ? ["drop the subheading", ...gaps] : gaps;
}
function nearestRecipe(slide, offers) {
  let best;
  for (const offer of [...offers.forPage, ...offers.others]) {
    for (const shape of offer.shapes) {
      const changes = pageGaps(slide, shape, offers.subheadingDeclines);
      if (best === void 0 || changes.length < best.changes.length) best = { id: offer.id, look: offer.recipe.look, write: describeShape(shape), changes };
    }
  }
  return best;
}
function drawnByIn(svg) {
  const match = /data-gauge-module="([a-z-]+)"/.exec(svg);
  return match !== null && match[1] in RECIPES ? match[1] : null;
}
var PHOTOGRAPH = "photograph";
function boundaryHasPhoto(slide) {
  return slide.background?.kind === "asset" || slide.components.some((component) => component.type === "image");
}
function photoEntry(slide) {
  return {
    id: PHOTOGRAPH,
    look: `The ${slide.type} drawn over a photograph, the face's own lettering kept`,
    write: ['background {"kind": "asset", "asset_id": "<a picture>"}'],
    written: boundaryHasPhoto(slide)
  };
}
function photoFace(ir, slide, theme2) {
  const effective = resolveEffectiveFace(ir, slide, theme2);
  return effective.layout?.drawsPhoto === true && effective.layoutId !== null ? effective.layoutId : void 0;
}
function pageSignature(ir, slide, theme2) {
  if (slide.type !== "content") {
    const face = photoFace(ir, slide, theme2);
    return face === void 0 ? void 0 : { face, forPage: [photoEntry(slide)], others: [], subheadingDeclines: false };
  }
  const offers = pageOffers(ir, slide, theme2);
  if (offers === void 0) return void 0;
  return {
    face: offers.face,
    forPage: offers.forPage.map((offer) => ({
      id: offer.id,
      look: offer.recipe.look,
      write: offer.shapes.map(describeShape),
      written: offer.shapes.some((shape) => pageGaps(slide, shape, offers.subheadingDeclines).length === 0)
    })),
    others: offers.others.map((offer) => ({ id: offer.id, kinds: [...offer.recipe.kinds] })),
    subheadingDeclines: offers.subheadingDeclines
  };
}
function pageSignatureUse(ir, slide, theme2, svg) {
  if (slide.type !== "content") {
    if (photoFace(ir, slide, theme2) === void 0) return void 0;
    if (boundaryHasPhoto(slide)) return { drawnBy: PHOTOGRAPH };
    const entry = photoEntry(slide);
    return { drawnBy: null, nearest: { id: PHOTOGRAPH, look: entry.look, write: entry.write[0], changes: ["add a background photograph"] } };
  }
  const offers = pageOffers(ir, slide, theme2);
  if (offers === void 0) return void 0;
  const drawnBy = drawnByIn(svg);
  if (drawnBy !== null) return { drawnBy };
  const nearest = nearestRecipe(slide, offers);
  return nearest === void 0 ? { drawnBy: null } : { drawnBy: null, nearest };
}

// src/inspect/page-contract.ts
var CANVAS_BOUND = {
  "bullets items": 16,
  "comparison rows": 15,
  "architecture layers": 11
};
function reachable(limit) {
  if (limit.of?.length !== 1) return true;
  const bound = CANVAS_BOUND[`${limit.of[0]} ${limit.measure}`];
  return bound === void 0 || limit.max <= bound;
}
function pageIndex(ir, pageId) {
  const index = ir.slides.findIndex((slide) => slide.id === pageId);
  if (index !== -1) return index;
  const ids = ir.slides.map((slide) => slide.id).filter((id) => id !== void 0);
  throw new PptwiseError(`no page "${pageId}" in this deck. Pages: ${ids.join(", ")}`);
}
function inspectedPage(ir, index, pageSpec) {
  const slide = ir.slides[index];
  return {
    id: slide.id ?? `page-${index + 1}`,
    number: index + 1,
    of: ir.slides.length,
    type: slide.type,
    ...slide.type === "content" ? { kind: slide.kind } : {},
    heading: slide.heading ?? pageSpec?.heading ?? "",
    ...pageSpec?.summary !== void 0 ? { summary: pageSpec.summary } : {},
    ...pageSpec?.focus !== void 0 ? { focus: pageSpec.focus } : {},
    filled: slide.placeholder !== true
  };
}
function isBoundary(slide) {
  return slide.type !== "content";
}
function slideSchema(full, type) {
  const slides = full.properties.slides;
  const variant = slides.items.oneOf.find((option) => option.properties.type.const === type);
  if (variant === void 0) throw new Error(`IR schema has no slide variant for "${type}"`);
  return variant;
}
var FACE_PLACED_FIELDS = ["fields", "stamp", "tag", "ballot", "years", "stage"];
function pageFields(full, slide, face) {
  const variant = slideSchema(full, slide.type);
  const placed = face?.pageFields ?? [];
  const fields = {};
  for (const field of PAGE_FILL_FIELDS) {
    if (FACE_PLACED_FIELDS.includes(field) && !placed.includes(field)) continue;
    if (isBoundary(slide) && BOUNDARY_UNRENDERED_FIELDS.includes(field) && !placed.includes(field)) continue;
    fields[field] = field === "components" ? {
      type: "array",
      description: "Components from components.legal. Expand one with --component <type> for its fields."
    } : variant.properties[field];
  }
  const defs = reachableDefs(full.$defs ?? {}, Object.values(fields));
  return Object.keys(defs).length > 0 ? { ...fields, $defs: defs } : fields;
}
function landingLegal(slide, theme2) {
  const accepted = /* @__PURE__ */ new Set();
  const offered = theme2.menu.content[slide.kind] !== void 0;
  for (const kind of offered ? [slide.kind] : landingCandidates(slide.kind, theme2.menu)) {
    const layout = getLayout(theme2.menu.content[kind].face);
    if (layout !== void 0) for (const type of faceAcceptedComponentTypes(layout)) accepted.add(type);
  }
  return COMPONENT_TYPES.filter((type) => accepted.has(type));
}
function pageComponents(ir, slide, theme2, pageSpec) {
  const face = componentFace(ir, slide, theme2);
  const legal = slide.type === "content" ? landingLegal(slide, theme2) : face === void 0 ? [] : [...faceAcceptedComponentTypes(face)];
  const required = slide.type === "content" && face !== void 0 ? face.slots.flatMap(
    (slot) => slot.required === true && slot.accepts !== "any" ? [{ slot: slot.name, accepts: [...slot.accepts] }] : []
  ) : [];
  const onPage = [...new Set(slide.components.map((component) => component.type))];
  const recommended = [];
  const notes = [];
  const focus = pageSpec?.focus;
  if (focus !== void 0 && COMPONENT_TYPES.includes(focus)) {
    if (legal.includes(focus)) recommended.push({ type: focus, because: "spec focus" });
    else notes.push(`The spec's focus "${focus}" is not a component this page draws.`);
  }
  for (const type of onPage) {
    if (legal.includes(type) && !recommended.some((r) => r.type === type)) recommended.push({ type, because: "on the page" });
  }
  if (legal.length === 0) {
    notes.push(
      face === void 0 && resolveEffectiveFace(ir, slide, theme2).route === "image-cover" ? `This ${slide.type} is drawn over its background picture and takes no component.` : "This page's face draws the heading alone and takes no component."
    );
  }
  return {
    legal,
    fullBody: legal.filter((type) => FULL_BODY_TYPES.has(type)),
    required,
    onPage,
    recommended,
    notes
  };
}
function pageLimits(full, ir, slide, theme2, pacing, legal) {
  if (legal.length === 0) return [];
  const limits = [];
  const budget = PACING_BUDGETS[pacing];
  if (slide.type === "content") {
    const density = contentPageDensity(ir, slide, theme2, pacing);
    const sources = [`${pacing} pacing allows ${density.pacingBudget}`];
    if (density.layoutCapacity !== void 0) sources.push(`the face's body holds ${density.layoutCapacity}`);
    if (density.takeoverImage) sources.push("the page's picture is not counted");
    const face = componentFace(ir, slide, theme2);
    const drawn = face === void 0 ? [] : faceAcceptedComponentTypes(face);
    const of = drawn.length > 0 && drawn.length < legal.length ? { of: [...drawn] } : {};
    limits.push({ level: "warning", measure: "components", per: "page", ...of, max: density.limit, source: sources.join(", ") });
    const itemSlot = density.itemSlot;
    if (itemSlot !== void 0) {
      limits.push({
        level: "warning",
        measure: "items",
        per: "page",
        of: [...itemSlot.accepts],
        max: itemSlot.capacity,
        source: `the face's ${itemSlot.name} slot, items counted across every component it takes`
      });
    }
  } else {
    const face = componentFace(ir, slide, theme2);
    for (const slot of face?.slots ?? []) {
      if (slot.accepts === "any") continue;
      if (slot.capacity !== void 0) {
        limits.push({
          level: "error",
          measure: "components",
          per: "page",
          of: [...slot.accepts],
          max: slot.capacity,
          source: `the face's ${slot.name} slot`
        });
      }
      const listed = slot.accepts.filter((type) => holdsItems(full, type));
      if (slot.itemCapacity !== void 0 && listed.length > 0) {
        const headed = slot.headingRow === true && writesHeading(slide);
        limits.push({
          level: "error",
          measure: "items",
          per: "component",
          of: listed,
          max: headed ? slot.itemCapacity - 1 : slot.itemCapacity,
          ...slot.itemMinimum !== void 0 ? { min: slot.itemMinimum } : {},
          source: `the face's ${slot.name} slot, blank items not counted${headed ? ", its first row set with the heading" : ""}`
        });
      }
    }
  }
  const width = "where a CJK character is 1 width unit and a Latin letter less";
  if (legal.includes("bullets")) {
    limits.push(
      { level: "warning", measure: "items", per: "component", of: ["bullets"], max: budget.bullets.maxItems, source: `${pacing} pacing` },
      { level: "warning", measure: "item width", per: "item", of: ["bullets"], max: budget.bullets.maxUnitsPerItem, source: `${pacing} pacing, ${width}` },
      { level: "error", measure: "items", per: "component", of: ["bullets"], max: CAPACITY.bullets.countOverflowItems, source: "engine ceiling" },
      { level: "error", measure: "item width", per: "item", of: ["bullets"], max: CAPACITY.bullets.itemOverflowUnits, source: `render-safety limit, ${width}` }
    );
  }
  if (legal.includes("comparison")) {
    limits.push(
      { level: "warning", measure: "rows", per: "component", of: ["comparison"], max: CAPACITY.comparison.warnRows, source: "rows the narrowest face holds" },
      { level: "error", measure: "rows", per: "component", of: ["comparison"], max: CAPACITY.comparison.errorRows, source: "engine ceiling" }
    );
  }
  if (legal.includes("architecture")) {
    limits.push(
      { level: "warning", measure: "layers", per: "component", of: ["architecture"], max: CAPACITY.architecture.warnLayers, source: "layers the narrowest face holds" },
      { level: "error", measure: "layers", per: "component", of: ["architecture"], max: CAPACITY.architecture.errorLayers, source: "the most layers a page holds under its heading" }
    );
  }
  if (legal.includes("chart")) {
    limits.push({
      level: "warning",
      measure: "series",
      per: "component",
      of: ["chart"],
      max: CAPACITY.chart.lineSeriesAdvisoryMax,
      source: "line and area charts, past which the lines stop reading apart"
    });
  }
  const kept = limits.filter(reachable);
  return kept.filter((limit) => !kept.some((other) => other !== limit && outranks(other, limit)));
}
function holdsItems(full, type) {
  const def = (full.$defs ?? {})[type];
  return def?.properties?.items?.type === "array" || def?.properties?.milestones?.type === "array";
}
function outranks(other, limit) {
  if (other.level !== "error" || other.measure !== limit.measure || other.per !== limit.per) return false;
  if (other.max > limit.max) return false;
  if (other.max === limit.max && other.level === limit.level) return false;
  const covers = other.of === void 0 || limit.of !== void 0 && limit.of.every((type) => other.of.includes(type));
  return covers;
}
function pageIssues(issues, index) {
  const prefix = `slides.${index}`;
  const out = [];
  for (const issue of issues) {
    if (issue.page === void 0) {
      out.push({ scope: "deck", path: issue.path, message: issue.message });
      continue;
    }
    if (issue.page !== index + 1) continue;
    const path2 = issue.path === prefix ? "" : issue.path.startsWith(`${prefix}.`) ? issue.path.slice(prefix.length + 1) : issue.path;
    out.push({ scope: "page", path: path2, message: issue.message });
  }
  return out;
}
function pageContract(ir, pageId, opts) {
  const index = pageIndex(ir, pageId);
  const slide = ir.slides[index];
  const { theme: theme2, pageSpec } = opts;
  const validation = opts.validation ?? validateIr(ir, { theme: theme2 });
  const pacing = resolveNarrative(ir.narrative).pacing;
  const components = pageComponents(ir, slide, theme2, pageSpec);
  const schema = irJsonSchema();
  const effective = resolveEffectiveFace(ir, slide, theme2);
  const drawnAs = slide.type === "content" && effective.servedKind !== void 0 && effective.servedKind !== slide.kind ? effective.servedKind : void 0;
  const signature = pageSignature(ir, slide, theme2);
  return {
    page: inspectedPage(ir, index, pageSpec),
    theme: theme2.id,
    face: effective.layoutId,
    ...drawnAs !== void 0 ? { drawnAs } : {},
    fields: pageFields(schema, slide, componentFace(ir, slide, theme2)),
    components,
    ...signature !== void 0 ? { signature } : {},
    limits: pageLimits(schema, ir, slide, theme2, pacing, components.legal),
    errors: pageIssues(validation.errors, index),
    warnings: pageIssues(validation.warnings ?? [], index)
  };
}
function pageComponentContract(ir, pageId, type, opts) {
  assertComponentType(type);
  const contract = pageContract(ir, pageId, opts);
  const { legal } = contract.components;
  if (!legal.includes(type)) {
    const where2 = `page "${contract.page.id}"`;
    throw new PptwiseError(
      legal.length === 0 ? `${where2} takes no component. ${contract.components.notes.join(" ")}` : `${where2} does not draw ${type}. It draws: ${legal.join(", ")}`
    );
  }
  const story = componentStory(type);
  return {
    page: contract.page,
    component: type,
    fullBody: contract.components.fullBody.includes(type),
    limits: contract.limits.filter((limit) => limit.of?.includes(type)),
    ...story !== void 0 ? { story: { name: story.name, story: story.story, positioning: story.positioning, notFor: story.notFor } } : {},
    schema: componentJsonSchema(type)
  };
}

// src/inspect/page-fit.ts
var FALLBACK_SELECTOR = [
  `[${STEP_ASIDE_ATTR}="fallback"]`,
  '[data-takeover-mode="fallback"]',
  '[data-annotate-mode="fallback"]'
].join(", ");
function pageFit(ir, pageId, opts) {
  const index = pageIndex(ir, pageId);
  const { root, dropped, drops } = drawSlide(ir, ir.slides[index], index, opts.theme);
  return {
    fits: dropped === 0,
    dropped: drops.map((drop) => ({ ...drop, what: dropPhrase(drop.kind, drop.count) })),
    truncated: Array.from(root.querySelectorAll('[data-truncated="1"]')).map((el) => (el.textContent ?? "").trim()),
    steppedAside: root.querySelector(FALLBACK_SELECTOR) !== null
  };
}

// src/themes/select.ts
var FALLBACK_THEME_ID = "brief";
function vocabOccasions(input) {
  if (!input || input.length === 0) return [];
  const seen = /* @__PURE__ */ new Set();
  const out = [];
  for (const word of input) {
    if (!Object.hasOwn(OCCASION_VOCAB, word) || seen.has(word)) continue;
    seen.add(word);
    out.push(word);
  }
  return out;
}
function resolvedIdentity(value) {
  if (value === void 0) return void 0;
  return IDENTITY_STRENGTHS.includes(value) ? value : void 0;
}
function narrativeRecommendations(strategy) {
  if (!strategy) return [];
  if (Object.hasOwn(NARRATIVE_PRESETS, strategy)) {
    return [...NARRATIVE_PRESETS[strategy].themeRecommendations];
  }
  if (!STRATEGY_VALUES.includes(strategy)) return [];
  const recs = [];
  const seen = /* @__PURE__ */ new Set();
  for (const preset of Object.values(NARRATIVE_PRESETS)) {
    if (preset.axes.strategy !== strategy) continue;
    for (const id of preset.themeRecommendations) {
      if (seen.has(id)) continue;
      seen.add(id);
      recs.push(id);
    }
  }
  return recs;
}
function hitCount(themeId, occasions) {
  const owned = THEME_OCCASIONS[themeId].occasions;
  let n = 0;
  for (const word of occasions) {
    if (owned.includes(word)) n++;
  }
  return n;
}
function identityMatch(themeId, identity) {
  if (identity === void 0) return 0;
  return THEME_OCCASIONS[themeId].identity === identity ? 1 : 0;
}
function recRank(themeId, recs) {
  const index = recs.indexOf(themeId);
  return index === -1 ? recs.length : index;
}
function catalogIndex(themeId) {
  return BUILTIN_THEME_IDS.indexOf(themeId);
}
function compareCandidates(a, b, occasions, identity, recs) {
  const byHits = hitCount(b, occasions) - hitCount(a, occasions);
  if (byHits !== 0) return byHits;
  const byIdentity = identityMatch(b, identity) - identityMatch(a, identity);
  if (byIdentity !== 0) return byIdentity;
  const byRec = recRank(a, recs) - recRank(b, recs);
  if (byRec !== 0) return byRec;
  return catalogIndex(a) - catalogIndex(b);
}
function suggestThemes(signals) {
  const occasions = vocabOccasions(signals.occasions);
  const identity = resolvedIdentity(signals.identity);
  const recs = narrativeRecommendations(signals.strategy);
  if (occasions.length > 0) {
    const hits = BUILTIN_THEME_IDS.filter((id) => hitCount(id, occasions) > 0);
    if (hits.length > 0) {
      return [...hits].sort((a, b) => compareCandidates(a, b, occasions, identity, recs));
    }
  }
  if (recs.length > 0) {
    if (identity === void 0) return recs;
    return [...recs].sort((a, b) => {
      const aId = identityMatch(a, identity);
      const bId = identityMatch(b, identity);
      if (bId !== aId) return bId - aId;
      return recRank(a, recs) - recRank(b, recs);
    });
  }
  if (identity !== void 0) {
    return BUILTIN_THEME_IDS.filter((id) => THEME_OCCASIONS[id].identity === identity).slice();
  }
  return [FALLBACK_THEME_ID];
}
var THEME_SHORTLIST_MIN = 4;
var THEME_SHORTLIST_MAX = 6;
var SHORTLIST_SPREAD = ["brief", "swiss", "journal", "terminal", "ember", "rally"];
function themeShortlist(signals) {
  const picked = suggestThemes(signals).slice(0, THEME_SHORTLIST_MAX);
  for (const id of SHORTLIST_SPREAD) {
    if (picked.length >= THEME_SHORTLIST_MIN) break;
    if (!picked.includes(id)) picked.push(id);
  }
  return picked;
}

// src/cli/config.ts
import { readFile as readFile2 } from "fs/promises";
import { dirname, join as join2, resolve } from "path";
import { z as z2 } from "zod";

// src/cli/home.ts
import { homedir as osHomedir } from "os";
import { join } from "path";

// src/cli/product-env.ts
var PRODUCT_ENV_PREFIX = "PPTWISE_";
var LEGACY_ENV_PREFIXES = ["PPTPRESS_", "PPTFAST_"];
var warnedLegacyKeys = /* @__PURE__ */ new Set();
function productEnvName(suffix) {
  return `${PRODUCT_ENV_PREFIX}${suffix}`;
}
function legacyEnvNames(suffix) {
  return LEGACY_ENV_PREFIXES.map((prefix) => `${prefix}${suffix}`);
}
function nonempty(value) {
  return value === void 0 || value === "" ? void 0 : value;
}
function warnLegacy(legacyKey, currentKey) {
  if (warnedLegacyKeys.has(legacyKey)) return;
  warnedLegacyKeys.add(legacyKey);
  process.stderr.write(`${legacyKey} is deprecated. Use ${currentKey} instead.
`);
}
function resolveProductEnv(suffix, env = process.env) {
  const currentKey = productEnvName(suffix);
  const current = nonempty(env[currentKey]);
  if (current !== void 0) return current;
  for (const legacyKey of legacyEnvNames(suffix)) {
    const legacy = nonempty(env[legacyKey]);
    if (legacy !== void 0) {
      warnLegacy(legacyKey, currentKey);
      return legacy;
    }
  }
  return void 0;
}

// src/cli/home.ts
var HOME_DIRNAME = ".pptwise";
function pptwiseHome(opts = {}) {
  const env = opts.env ?? process.env;
  const fromEnv = resolveProductEnv("HOME", env);
  if (fromEnv !== void 0) return fromEnv;
  return join((opts.homedir ?? osHomedir)(), HOME_DIRNAME);
}
function userConfigPath(opts) {
  return join(pptwiseHome(opts), "config.json");
}

// src/cli/image-config.ts
import { chmodSync, lstatSync } from "fs";
import { mkdir, readFile, writeFile } from "fs/promises";
import { z } from "zod";
var ImageProviderConfigSchema = z.object({
  apiKey: z.string().optional()
}).strict();
var OpenverseConfigSchema = z.object({
  clientId: z.string().optional(),
  clientSecret: z.string().optional()
}).strict();
var GENERATOR_IDS = ["grok", "codex", "antigravity"];
var DEFAULT_GENERATOR_ORDER = ["grok", "codex", "antigravity"];
var DEFAULT_GENERATOR_TIMEOUT_MS = 18e4;
var GeneratorFlagsSchema = z.object({ enabled: z.boolean().optional() }).strict();
var GeneratorsConfigSchema = z.object({
  grok: GeneratorFlagsSchema.optional(),
  codex: GeneratorFlagsSchema.optional(),
  antigravity: GeneratorFlagsSchema.optional(),
  order: z.array(z.enum(GENERATOR_IDS)).optional(),
  timeoutMs: z.number().int().positive().optional()
}).strict();
var ImagesConfigSchema = z.object({
  pexels: ImageProviderConfigSchema.optional(),
  pixabay: ImageProviderConfigSchema.optional(),
  openverse: OpenverseConfigSchema.optional(),
  generators: GeneratorsConfigSchema.optional()
}).strict();
var API_KEY_PROVIDERS = ["pexels", "pixabay"];
var ENV_SUFFIX_BY_PROVIDER = {
  pexels: "PEXELS_API_KEY",
  pixabay: "PIXABAY_API_KEY"
};
var FORBIDDEN_SEGMENTS = /* @__PURE__ */ new Set(["__proto__", "constructor", "prototype"]);
var CLI_KEYS = {
  "pexels.apiKey": {
    cliKey: "pexels.apiKey",
    path: ["images", "pexels", "apiKey"],
    omitValue: true,
    secret: true,
    kind: "string"
  },
  "pixabay.apiKey": {
    cliKey: "pixabay.apiKey",
    path: ["images", "pixabay", "apiKey"],
    omitValue: true,
    secret: true,
    kind: "string"
  },
  "openverse.clientId": {
    cliKey: "openverse.clientId",
    path: ["images", "openverse", "clientId"],
    omitValue: false,
    secret: true,
    kind: "string"
  },
  "openverse.clientSecret": {
    cliKey: "openverse.clientSecret",
    path: ["images", "openverse", "clientSecret"],
    omitValue: true,
    secret: true,
    kind: "string"
  },
  "images.generators.grok.enabled": {
    cliKey: "images.generators.grok.enabled",
    path: ["images", "generators", "grok", "enabled"],
    omitValue: false,
    secret: false,
    kind: "boolean"
  },
  "images.generators.codex.enabled": {
    cliKey: "images.generators.codex.enabled",
    path: ["images", "generators", "codex", "enabled"],
    omitValue: false,
    secret: false,
    kind: "boolean"
  },
  "images.generators.antigravity.enabled": {
    cliKey: "images.generators.antigravity.enabled",
    path: ["images", "generators", "antigravity", "enabled"],
    omitValue: false,
    secret: false,
    kind: "boolean"
  },
  "images.generators.order": {
    cliKey: "images.generators.order",
    path: ["images", "generators", "order"],
    omitValue: false,
    secret: false,
    kind: "order"
  },
  "images.generators.timeoutMs": {
    cliKey: "images.generators.timeoutMs",
    path: ["images", "generators", "timeoutMs"],
    omitValue: false,
    secret: false,
    kind: "timeoutMs"
  }
};
function maskKey(value) {
  if (value.length <= 8) return "****";
  return `${value.slice(0, 6)}...${value.slice(-2)}`;
}
function assertSafeConfigKeyPath(key) {
  for (const segment of key.split(".")) {
    if (FORBIDDEN_SEGMENTS.has(segment)) {
      throw new PptwiseError(`refusing to set "${key}": "${segment}" is not a valid config key`);
    }
  }
}
function parseCliConfigKey(key) {
  assertSafeConfigKeyPath(key);
  const hit = CLI_KEYS[key];
  if (!hit) {
    throw new PptwiseError(
      `unknown config key "${key}" \u2014 expected pexels.apiKey, pixabay.apiKey, openverse.clientId, openverse.clientSecret, or images.generators.*`
    );
  }
  return hit;
}
function providerNamedInFile(file, provider) {
  return file?.images?.[provider] !== void 0;
}
function nonempty2(value) {
  return typeof value === "string" && value !== "" ? value : void 0;
}
function resolveOne(file, env, provider) {
  const namedInFile = providerNamedInFile(file, provider);
  if (namedInFile) {
    const apiKey2 = nonempty2(file?.images?.[provider]?.apiKey);
    return { apiKey: apiKey2, source: apiKey2 ? "file" : null, namedInFile: true };
  }
  const apiKey = nonempty2(resolveProductEnv(ENV_SUFFIX_BY_PROVIDER[provider], env));
  return { apiKey, source: apiKey ? "env" : null, namedInFile: false };
}
function resolveOpenverse(file, env) {
  const namedInFile = providerNamedInFile(file, "openverse");
  if (namedInFile) {
    const clientId2 = nonempty2(file?.images?.openverse?.clientId);
    const clientSecret2 = nonempty2(file?.images?.openverse?.clientSecret);
    const ready2 = Boolean(clientId2 && clientSecret2);
    return { clientId: clientId2, clientSecret: clientSecret2, source: ready2 ? "file" : null, namedInFile: true, ready: ready2 };
  }
  const clientId = nonempty2(resolveProductEnv("OPENVERSE_CLIENT_ID", env));
  const clientSecret = nonempty2(resolveProductEnv("OPENVERSE_CLIENT_SECRET", env));
  const ready = Boolean(clientId && clientSecret);
  return { clientId, clientSecret, source: ready ? "env" : null, namedInFile: false, ready };
}
function resolveImageKeys(opts = {}) {
  const file = opts.file ?? null;
  const env = opts.env ?? process.env;
  return {
    pexels: resolveOne(file, env, "pexels"),
    pixabay: resolveOne(file, env, "pixabay"),
    openverse: resolveOpenverse(file, env)
  };
}
function resolveGenerators(opts = {}) {
  const g = opts.file?.images?.generators;
  const order = g?.order && g.order.length > 0 ? g.order : DEFAULT_GENERATOR_ORDER;
  return {
    enabled: {
      grok: g?.grok?.enabled === true,
      codex: g?.codex?.enabled === true,
      antigravity: g?.antigravity?.enabled === true
    },
    order,
    timeoutMs: typeof g?.timeoutMs === "number" && g.timeoutMs > 0 ? g.timeoutMs : DEFAULT_GENERATOR_TIMEOUT_MS
  };
}
function parseCliConfigValue(parsed, raw) {
  if (parsed.kind === "boolean") {
    const v2 = raw.trim().toLowerCase();
    if (v2 !== "true" && v2 !== "false") {
      throw new PptwiseError(`${parsed.cliKey} must be true or false`);
    }
    return v2 === "true";
  }
  if (parsed.kind === "order") {
    const names = raw.split(",").map((s) => s.trim()).filter((s) => s !== "");
    const unknown = names.find((n) => !GENERATOR_IDS.includes(n));
    if (unknown) {
      throw new PptwiseError(`unknown generator "${unknown}" \u2014 expected grok, codex, or antigravity`);
    }
    if (names.length === 0) {
      throw new PptwiseError("images.generators.order must not be empty");
    }
    return names;
  }
  if (parsed.kind === "timeoutMs") {
    if (!/^[0-9]+$/.test(raw.trim()) || Number(raw) <= 0) {
      throw new PptwiseError(`${parsed.cliKey} must be a positive integer`);
    }
    return Number(raw);
  }
  return raw;
}
function knownSecretsFrom(keys) {
  const secrets = [];
  for (const provider of API_KEY_PROVIDERS) {
    const apiKey = keys[provider].apiKey;
    if (apiKey && apiKey.length >= 6) secrets.push(apiKey);
  }
  const { clientId, clientSecret } = keys.openverse;
  if (clientSecret && clientSecret.length >= 6) secrets.push(clientSecret);
  if (clientId && clientId.length >= 6) secrets.push(clientId);
  return secrets;
}
function assertNotSymlink(path2) {
  let st;
  try {
    st = lstatSync(path2);
  } catch (e) {
    if (e.code === "ENOENT") return;
    throw e;
  }
  if (st.isSymbolicLink()) {
    throw new PptwiseError(`refusing to write ${path2}: it is a symlink`);
  }
}
function asPlainObject(value) {
  if (typeof value === "object" && value !== null && !Array.isArray(value)) {
    return { ...value };
  }
  return {};
}
async function readRawUserConfig() {
  const path2 = userConfigPath();
  let text;
  try {
    text = await readFile(path2, "utf8");
  } catch (e) {
    if (e.code === "ENOENT") return {};
    throw e;
  }
  let raw;
  try {
    raw = JSON.parse(text);
  } catch (e) {
    throw new PptwiseError(`${path2} is not valid JSON: ${e.message}`);
  }
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) {
    throw new PptwiseError(`${path2} must be a JSON object`);
  }
  return raw;
}
async function persistUserConfigValue(path2, value) {
  for (const segment of path2) {
    if (FORBIDDEN_SEGMENTS.has(segment) || segment === "") {
      throw new PptwiseError(`refusing to set "${path2.join(".")}": "${segment}" is not a valid config key`);
    }
  }
  if (path2.length === 0) {
    throw new PptwiseError("refusing to set an empty config path");
  }
  const filePath = userConfigPath();
  assertNotSymlink(filePath);
  const raw = await readRawUserConfig();
  let cursor = raw;
  for (let i = 0; i < path2.length - 1; i++) {
    const segment = path2[i];
    const next = asPlainObject(cursor[segment]);
    cursor[segment] = next;
    cursor = next;
  }
  const leaf = path2[path2.length - 1];
  if (value === "") {
    delete cursor[leaf];
  } else {
    cursor[leaf] = value;
  }
  await mkdir(pptwiseHome(), { recursive: true });
  const text = JSON.stringify(raw, null, 2) + "\n";
  await writeFile(filePath, text, { encoding: "utf8", mode: 384 });
  try {
    chmodSync(filePath, 384);
  } catch {
  }
  return filePath;
}
function pexelsApplyUrl() {
  return "https://www.pexels.com/api/";
}
function pixabayApplyUrl() {
  return "https://pixabay.com/api/docs/";
}
function missingKeysError(kind) {
  if (kind === "pixabay") {
    return new PptwiseError(
      `Pixabay is not configured. Apply at ${pixabayApplyUrl()}, then run \`pptwise config set pixabay.apiKey\`.`
    );
  }
  return new PptwiseError(
    `Pexels is not configured. Apply at ${pexelsApplyUrl()}, then run \`pptwise config set pexels.apiKey\`.`
  );
}

// src/cli/config.ts
var ConfigSchema = z2.object({}).strict();
var UserConfigSchema = z2.object({
  images: ImagesConfigSchema.optional()
}).strict();
var CONFIG_FILENAME = "pptwise.config.json";
var LEGACY_CONFIG_FILENAMES = ["pptpress.config.json", "pptfast.config.json"];
async function readConfigFile(path2, schema) {
  let text;
  try {
    text = await readFile2(path2, "utf8");
  } catch {
    return null;
  }
  let raw;
  try {
    raw = JSON.parse(text);
  } catch (e) {
    throw new PptwiseError(`${path2} is not valid JSON: ${e.message}`);
  }
  const r = schema.safeParse(raw);
  if (!r.success) {
    const detail = r.error.issues.map((i) => `${i.path.join(".") || "(root)"}: ${i.message}`).join("\n");
    throw new PptwiseError(`invalid ${path2}:
${detail}`);
  }
  return { path: path2, config: r.data };
}
async function findConfig(startDir) {
  let dir = resolve(startDir);
  for (; ; ) {
    const hit = await readConfigFile(join2(dir, CONFIG_FILENAME), ConfigSchema);
    if (hit) return hit;
    for (const name of LEGACY_CONFIG_FILENAMES) {
      const legacy = await readConfigFile(join2(dir, name), ConfigSchema);
      if (legacy) return legacy;
    }
    const parent = dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}
async function findUserConfig() {
  return readConfigFile(userConfigPath(), UserConfigSchema);
}

// src/cli/deck-dir.ts
import { copyFile, mkdir as mkdir2, readdir, stat, writeFile as writeFile2 } from "fs/promises";
import { basename as basename2, extname as extname2, isAbsolute as isAbsolute2, join as join3, relative, resolve as resolve3 } from "path";

// src/cli/load-ir.ts
import { readFile as readFile3 } from "fs/promises";
import { basename, extname, isAbsolute, resolve as resolve2 } from "path";
import { fileURLToPath } from "url";
var MIME_BY_EXT = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif"
};
var EXT_BY_MIME = {
  "image/png": ".png",
  "image/jpeg": ".jpg",
  "image/gif": ".gif",
  "image/webp": ".webp"
};
function unwrapFileSrc(src, platform = process.platform) {
  if (platform === "win32") {
    const url = new URL(src);
    let pathname = decodeURIComponent(url.pathname.replace(/\//g, "\\"));
    if (url.hostname) return `\\\\${url.hostname}${pathname}`;
    if (pathname.startsWith("\\") && pathname.length >= 3 && pathname[2] === ":") {
      return pathname.slice(1);
    }
    return pathname;
  }
  return fileURLToPath(src);
}
async function loadIrFile(irPath, kind = "IR") {
  let text;
  try {
    text = await readFile3(irPath, "utf8");
  } catch {
    throw new PptwiseError(`cannot read ${kind} file: ${irPath}`);
  }
  try {
    return JSON.parse(text);
  } catch (e) {
    throw new PptwiseError(`${kind} file ${irPath} is not valid JSON: ${e.message}`);
  }
}
async function readFromWorkspace(src, workspaceAssetsDir) {
  const candidates = [resolve2(workspaceAssetsDir, src), resolve2(workspaceAssetsDir, basename(src))];
  const seen = /* @__PURE__ */ new Set();
  for (const candidate of candidates) {
    if (seen.has(candidate)) continue;
    seen.add(candidate);
    try {
      return await readFile3(candidate);
    } catch {
      continue;
    }
  }
  return null;
}
async function resolveLocalAssets(ir, baseDir, workspaceAssetsDir) {
  for (const [name, asset] of Object.entries(ir.assets.images)) {
    const src = asset.src;
    if (src.startsWith("data:") || /^https?:\/\//.test(src)) continue;
    const abs = src.startsWith("file:") ? unwrapFileSrc(src) : isAbsolute(src) ? src : resolve2(baseDir, src);
    let bytes;
    try {
      bytes = await readFile3(abs);
    } catch {
      const fallback = workspaceAssetsDir && !isAbsolute(src) ? await readFromWorkspace(src, workspaceAssetsDir) : null;
      if (!fallback) {
        throw new PptwiseError(`asset "${name}": cannot read image file ${abs} (from src "${src}")`);
      }
      bytes = fallback;
    }
    if (bytes.length === 0) {
      throw new PptwiseError(`asset "${name}": image file ${abs} is zero bytes \u2014 re-export or re-select the file`);
    }
    const ext = extname(abs).toLowerCase();
    const mime = MIME_BY_EXT[ext];
    if (mime) {
      const sniffed = sniffImageFormat(bytes);
      if (sniffed === null) {
        throw new PptwiseError(
          `asset "${name}": image file ${abs} has a corrupt or unrecognized header (extension claims ${mime}) \u2014 re-export or re-select the file`
        );
      }
      const expected = FORMAT_BY_MIME[mime];
      if (expected && sniffed !== expected) {
        throw new PptwiseError(
          `asset "${name}": image file ${abs} is named "${ext}" but its bytes are actually ${MIME_BY_SNIFFED_FORMAT[sniffed]} \u2014 rename the file to match its real format, or re-export/re-save it as a genuine ${mime}`
        );
      }
      asset.src = `data:${mime};base64,${bytes.toString("base64")}`;
      continue;
    }
    const recode = getPlatform().recodeImageToPng;
    if (!recode) {
      throw new PptwiseError(
        `asset "${name}": unsupported image format "${extname(abs)}" \u2014 install sharp or convert to png/jpeg/gif`
      );
    }
    asset.src = await recode(`data:application/octet-stream;base64,${bytes.toString("base64")}`);
  }
}

// src/cli/deck-dir.ts
var SPEC_FILENAME = "deck.spec.json";
var PAGES_DIRNAME = "pages";
var ASSETS_DIRNAME = "assets";
var THEME_FILENAME = "theme.json";
function assertSafeFileSegment(id, context) {
  const safeBase = resolve3("/pptwise-safe-base");
  const rel = relative(safeBase, resolve3(safeBase, id));
  const safe = !isAbsolute2(id) && !id.includes("/") && !id.includes("\\") && id !== ".." && !rel.startsWith("..") && !isAbsolute2(rel);
  if (!safe) {
    throw new PptwiseError(
      `${context} "${id}" is not a safe file name \u2014 ids used as page/asset file names must not contain path separators or ".."`
    );
  }
}
async function isDeckDirectory(path2) {
  try {
    return (await stat(path2)).isDirectory();
  } catch (e) {
    if (e.code === "ENOENT") return false;
    throw new PptwiseError(`cannot check ${path2}: ${e.message}`);
  }
}
async function pathExists(path2) {
  try {
    await stat(path2);
    return true;
  } catch (e) {
    if (e.code === "ENOENT") return false;
    throw new PptwiseError(`cannot check path ${path2}: ${e.message}`);
  }
}
async function resolveDeckTarget(arg, cwd = process.cwd()) {
  if (arg.trim() === "") throw new PptwiseError("deck target must not be empty");
  return resolve3(cwd, arg);
}
function expectedLayoutHint() {
  const rows = [
    [SPEC_FILENAME, "the locked spec (see `pptwise spec validate`)"],
    [`${PAGES_DIRNAME}/<page-id>.json`, "one file per filled page (missing pages become placeholders)"],
    [`${ASSETS_DIRNAME}/`, "optional local images"]
  ];
  const width = Math.max(...rows.map(([name]) => name.length)) + 2;
  return rows.map(([name, desc]) => `  ${name.padEnd(width)}${desc}`).join("\n");
}
async function readSpecFile(dir) {
  const specPath = join3(dir, SPEC_FILENAME);
  if (!await pathExists(specPath)) {
    throw new PptwiseError(
      `no ${SPEC_FILENAME} in ${dir} \u2014 expected a deck project directory:
${expectedLayoutHint()}`
    );
  }
  return loadIrFile(specPath, "spec");
}
async function readPages(dir) {
  const pagesDir = join3(dir, PAGES_DIRNAME);
  let entries;
  try {
    entries = (await readdir(pagesDir, { withFileTypes: true })).filter((entry) => entry.isFile() && extname2(entry.name) === ".json").map((entry) => entry.name);
  } catch (e) {
    if (e.code === "ENOENT") return {};
    throw new PptwiseError(`cannot read ${PAGES_DIRNAME}/ directory ${pagesDir}: ${e.message}`);
  }
  const pages = {};
  await Promise.all(
    entries.map(async (entry) => {
      const id = basename2(entry, ".json");
      pages[id] = await loadIrFile(join3(pagesDir, entry), `page "${id}"`);
    })
  );
  return pages;
}
async function scanAssets(dir) {
  const assetsDir = join3(dir, ASSETS_DIRNAME);
  let entries;
  try {
    entries = (await readdir(assetsDir, { withFileTypes: true })).filter((entry) => entry.isFile() && !entry.name.startsWith(".")).map((entry) => entry.name);
  } catch (e) {
    if (e.code === "ENOENT") return {};
    throw new PptwiseError(`cannot read ${ASSETS_DIRNAME}/ directory ${assetsDir}: ${e.message}`);
  }
  const images2 = {};
  const sourceFile2 = /* @__PURE__ */ new Map();
  for (const entry of entries) {
    if (extname2(entry).toLowerCase() === ".json") continue;
    const id = basename2(entry, extname2(entry));
    const previous = sourceFile2.get(id);
    if (previous !== void 0) {
      throw new PptwiseError(
        `${ASSETS_DIRNAME}/${previous} and ${ASSETS_DIRNAME}/${entry} both register image id "${id}" \u2014 rename one of the files`
      );
    }
    sourceFile2.set(id, entry);
    images2[id] = { src: `${ASSETS_DIRNAME}/${entry}` };
  }
  return images2;
}
function specThemeFromRaw(spec2) {
  if (typeof spec2 !== "object" || spec2 === null) return void 0;
  const theme2 = spec2.theme;
  return typeof theme2 === "string" ? theme2 : void 0;
}
async function readOnePage(dir, id) {
  assertSafeFileSegment(id, "page id");
  const path2 = join3(dir, PAGES_DIRNAME, `${id}.json`);
  if (!await pathExists(path2)) return {};
  return { [id]: await loadIrFile(path2, `page "${id}"`) };
}
async function readDeckDir(dir, opts) {
  const deckDir = resolve3(dir);
  const specPath = join3(deckDir, SPEC_FILENAME);
  const spec2 = opts?.spec !== void 0 ? opts.spec.parsed : await readSpecFile(deckDir);
  const specTheme = specThemeFromRaw(spec2);
  const pages = opts?.page !== void 0 ? await readOnePage(deckDir, opts.page) : await readPages(deckDir);
  const assembled = assembleDeck(spec2, pages, opts);
  const images2 = await scanAssets(deckDir);
  const merged = { ...assembled.ir, assets: { images: { ...assembled.ir.assets.images, ...images2 } } };
  return {
    ir: merged,
    spec: assembled.spec,
    deckDir,
    specPath,
    ...specTheme !== void 0 ? { specTheme } : {}
  };
}
async function writeDeckAssets(images2, outDir, sourceBaseDir) {
  const entries = Object.entries(images2);
  const assetsDir = join3(outDir, ASSETS_DIRNAME);
  if (entries.length === 0) return { count: 0, assetsDir };
  await mkdir2(assetsDir, { recursive: true });
  await Promise.all(entries.map(([id, asset]) => writeOneAsset(id, asset.src, assetsDir, sourceBaseDir)));
  return { count: entries.length, assetsDir };
}
var DATA_URI_RE = /^data:([^;,]+);base64,(.*)$/s;
async function writeOneAsset(id, src, assetsDir, sourceBaseDir) {
  assertSafeFileSegment(id, "asset id");
  if (src.startsWith("data:")) {
    const match = DATA_URI_RE.exec(src);
    if (!match) {
      throw new PptwiseError(`asset "${id}": only base64-encoded data URIs can be disassembled (malformed data URI)`);
    }
    const mime = match[1];
    const payload = match[2];
    const ext = EXT_BY_MIME[mime];
    if (!ext) {
      throw new PptwiseError(
        `asset "${id}": cannot disassemble a data URI with mime "${mime}" \u2014 expected one of ${Object.keys(EXT_BY_MIME).join(", ")}`
      );
    }
    await writeFile2(join3(assetsDir, `${id}${ext}`), Buffer.from(payload, "base64"));
    return;
  }
  if (/^https?:\/\//.test(src)) {
    throw new PptwiseError(
      `asset "${id}": URL assets cannot be disassembled into a deck directory \u2014 inline it as a data URI or download it first`
    );
  }
  const abs = isAbsolute2(src) ? src : resolve3(sourceBaseDir, src);
  try {
    await copyFile(abs, join3(assetsDir, `${id}${extname2(abs)}`));
  } catch {
    throw new PptwiseError(`asset "${id}": cannot read source image ${abs} (from src "${src}") \u2014 cannot disassemble`);
  }
}

// src/cli/inspect-format.ts
function pageHeader(page, theme2, file) {
  const kind = page.kind !== void 0 ? `, kind "${page.kind}"` : "";
  const bound = theme2 !== void 0 ? `, theme "${theme2}"` : "";
  const lines = [`page ${page.id} (${page.number} of ${page.of}): ${page.type}${kind}${bound}`, `heading: ${page.heading}`];
  if (page.summary !== void 0) lines.push(`summary: ${page.summary}`);
  if (page.focus !== void 0) lines.push(`focus: ${page.focus}`);
  lines.push(`file: ${file} (${page.filled ? "filled" : "not written yet"})`);
  return lines;
}
function formatLimit(limit) {
  const of = limit.of?.join(" or ");
  let what;
  if (limit.per === "page") {
    what = `at most ${limit.max} ${limit.measure}${of !== void 0 ? ` (${of})` : ""} on the page`;
  } else if (limit.per === "component") {
    what = `${limit.min !== void 0 ? `at least ${limit.min} and ` : ""}at most ${limit.max} ${limit.measure} in each ${of ?? "component"}`;
  } else {
    what = `at most ${limit.max} width units in each ${of ?? "component"} item`;
  }
  return `${what} (${limit.source})`;
}
function formatIssue(issue) {
  const where2 = issue.path === "" ? issue.scope : `${issue.scope} ${issue.path}`;
  return `${where2}: ${issue.message}`;
}
function issueBlock(label, issues) {
  if (issues.length === 0) return [`${label}: none`];
  return [`${label}:`, ...issues.map((issue) => `  ${formatIssue(issue)}`)];
}
var PAGE_KEY_GLOSS = {
  fields: "a form's header lines, such as To and From",
  stamp: "a stamp pressed on the page",
  tag: "a small tag beside the heading",
  ballot: "the boxes ticked beside each item",
  years: "a strip of years with this page's lit",
  stage: "the course stage this page lights",
  footnote: "the source line",
  notes: "speaker notes, never drawn"
};
function formatSignature(signature) {
  const lines = [`signature layouts (the theme's own drawings on face ${signature.face}, the ones its samples are made of):`];
  for (const entry of signature.forPage) {
    const mark2 = signature.drawnBy === entry.id ? ", draws this page now" : entry.written ? ", the page is written to it" : "";
    lines.push(`  ${entry.id}${mark2}: ${entry.look}`);
    for (const write of entry.write) lines.push(`    write: ${write}`);
  }
  if (signature.others.length > 0) {
    lines.push(`  also on this face, made for other kinds: ${signature.others.map((other) => `${other.id} (${other.kinds.join(", ")}${signature.drawnBy === other.id ? ", draws this page now" : ""})`).join(", ")}`);
  }
  if (signature.subheadingDeclines) lines.push("  a page with a subheading gets none of them");
  if (signature.drawnBy === null) lines.push("  drawn now: none of them, the face's plain layout. Write to one where the content holds it, never add content to fit");
  return lines;
}
function formatPageContract(contract, file) {
  const { components } = contract;
  const lines = [...pageHeader(contract.page, contract.theme, file), ""];
  if (contract.drawnAs !== void 0) {
    lines.push(`drawn as: "${contract.drawnAs}", the nearest kind theme "${contract.theme}" draws this page as`, "");
  }
  const keys = Object.keys(contract.fields).filter((key) => key !== "$defs");
  lines.push(`page file keys (the top-level keys of ${file}): ${keys.map((key) => PAGE_KEY_GLOSS[key] !== void 0 ? `${key} (${PAGE_KEY_GLOSS[key]})` : key).join(", ")}`);
  lines.push(`components (${components.legal.length}): ${components.legal.length > 0 ? components.legal.join(", ") : "none"}`);
  if (components.fullBody.length > 0) {
    lines.push(`  full-body, each must be the page's only component: ${components.fullBody.join(", ")}`);
  }
  for (const slot of components.required) {
    lines.push(`  required: one of ${slot.accepts.join(", ")} for the ${slot.slot} slot`);
  }
  if (components.recommended.length > 0) {
    lines.push(`  recommended: ${components.recommended.map((r) => `${r.type} (${r.because})`).join(", ")}`);
  }
  for (const note of components.notes) lines.push(`  note: ${note}`);
  if (components.legal.length > 0) lines.push("  expand one with --component <type>");
  lines.push("");
  if (contract.signature !== void 0) lines.push(...formatSignature(contract.signature), "");
  const errors = contract.limits.filter((limit) => limit.level === "error");
  const warnings = contract.limits.filter((limit) => limit.level === "warning");
  if (errors.length > 0) {
    lines.push("limits (validate refuses the page past these):", ...errors.map((limit) => `  ${formatLimit(limit)}`));
  }
  if (warnings.length > 0) {
    lines.push("advice (validate warns past these):", ...warnings.map((limit) => `  ${formatLimit(limit)}`));
  }
  if (contract.limits.length > 0) lines.push("");
  lines.push(...issueBlock("errors", contract.errors), ...issueBlock("warnings", contract.warnings));
  lines.push("fit: not checked here. Run --fit to draw this page and see what it would lose");
  return lines.join("\n");
}
function formatPageComponentContract(expanded) {
  const { page } = expanded;
  const kind = page.kind !== void 0 ? `, kind "${page.kind}"` : "";
  const lines = [`component ${expanded.component} on page ${page.id} (${page.number} of ${page.of}): ${page.type}${kind}`];
  if (expanded.story !== void 0) {
    lines.push(
      `name: ${expanded.story.name}`,
      `what it is: ${expanded.story.story}`,
      `choose it: ${expanded.story.positioning}`,
      `not for: ${expanded.story.notFor}`
    );
  }
  lines.push(`full-body: ${expanded.fullBody ? "yes, it must be the page's only component" : "no"}`);
  if (expanded.limits.length > 0) {
    lines.push(
      "limits on this page:",
      ...expanded.limits.map(
        (limit) => `  ${formatLimit(limit)}, validate ${limit.level === "error" ? "refuses" : "warns"} past it`
      )
    );
  }
  lines.push("schema:", JSON.stringify(expanded.schema, null, 2));
  return lines.join("\n");
}
function formatPageFitReport(report, theme2) {
  const lines = pageHeader(report.page, theme2, report.page.file);
  const { fit } = report;
  if (!fit.checked) {
    lines.push(`fit: not checked, ${fit.reason}`);
  } else if (fit.fits) {
    lines.push("fit: fits, nothing dropped");
  } else {
    lines.push(
      `fit: does not fit, ${fit.dropped.map((drop) => drop.what).join(", ")} dropped. render refuses a deck that drops content: shorten the page or split it in two`
    );
  }
  if (fit.checked) {
    for (const text of fit.truncated) lines.push(`  text cut to fit: "${text}" (render allows it, audit reports it)`);
    if (fit.steppedAside) lines.push("  stepped aside: the theme's face declined this page, and a plainer layout drew all of it");
  }
  lines.push(...issueBlock("errors", report.errors), ...issueBlock("warnings", report.warnings));
  return lines.join("\n");
}

// src/cli/theme-write.ts
import { link, mkdir as mkdir3, rename, rm, writeFile as writeFile3 } from "fs/promises";
import { basename as basename3, dirname as dirname2, join as join4 } from "path";
import { randomBytes } from "crypto";
async function writeThemeFile(path2, file, force = false, hooks) {
  const dir = dirname2(path2);
  await mkdir3(dir, { recursive: true });
  const tmp = join4(dir, `.${basename3(path2)}.${randomBytes(8).toString("hex")}.tmp`);
  try {
    await writeFile3(tmp, JSON.stringify(file, null, 2) + "\n");
    await hooks?.beforePublish?.(tmp, path2);
    if (force) {
      await rename(tmp, path2);
      return;
    }
    try {
      await link(tmp, path2);
    } catch (error) {
      if (error.code === "EEXIST") {
        throw new PptwiseError(`theme file already exists: ${path2}. Pass --force to overwrite.`);
      }
      throw error;
    }
    await rm(tmp, { force: true });
  } catch (error) {
    await rm(tmp, { force: true });
    throw error;
  }
}

// src/cli/build-report.ts
function topField(field) {
  return field.split(/[.[]/)[0] ?? field;
}
function sourceFile(pageId, field) {
  if (pageId === void 0) return void 0;
  if (field !== void 0 && PAGE_FILL_FIELDS.includes(topField(field))) {
    return `${PAGES_DIRNAME}/${pageId}.json`;
  }
  return SPEC_FILENAME;
}
function validateIssue(issue, isDir) {
  const slidePath = /^slides\.(\d+)(?:\.(.+))?$/.exec(issue.path);
  const field = slidePath ? slidePath[2] : issue.path || void 0;
  const file = isDir && slidePath ? sourceFile(issue.slideId, field) : void 0;
  return {
    stage: "validate",
    ...issue.page !== void 0 ? { page: issue.page } : {},
    ...issue.slideId !== void 0 ? { pageId: issue.slideId } : {},
    ...file !== void 0 ? { file } : {},
    ...field !== void 0 ? { field } : {},
    message: issue.message
  };
}
function auditIssue(finding, isDir) {
  return {
    stage: "audit",
    page: finding.page,
    ...finding.slideId !== void 0 ? { pageId: finding.slideId } : {},
    ...finding.slideId !== void 0 && isDir ? { file: `${PAGES_DIRNAME}/${finding.slideId}.json` } : {},
    code: finding.code,
    message: finding.message,
    ...finding.detail !== void 0 ? { detail: finding.detail } : {}
  };
}
function placeholderIssues(ir, isDir) {
  const issues = [];
  ir.slides.forEach((slide, i) => {
    if (!slide.placeholder) return;
    const file = slide.id !== void 0 && isDir ? `${PAGES_DIRNAME}/${slide.id}.json` : void 0;
    issues.push({
      stage: "validate",
      page: i + 1,
      ...slide.id !== void 0 ? { pageId: slide.id } : {},
      ...file !== void 0 ? { file } : {},
      message: file !== void 0 ? `this page is not written yet. Write ${file}` : "this page is not written yet"
    });
  });
  return issues;
}
function assembleIssues(message, pageIds2 = []) {
  const lines = message.split("\n").map((line) => line.trim()).filter((line) => line !== "");
  const specFailed = lines.length > 0 && /^invalid spec \(\d+ issues?\):$/.test(lines[0]);
  const irFailed = lines.length > 0 && /^assembled deck did not produce valid IR:$/.test(lines[0]);
  const body = specFailed || irFailed ? lines.slice(1) : lines;
  return body.map((line) => {
    const slide = irFailed ? /^slides\.(\d+)\.([^:\s]+): (.*)$/.exec(line) : null;
    if (slide) {
      const index = Number(slide[1]);
      const pageId = pageIds2[index];
      const field = slide[2];
      const file2 = sourceFile(pageId, field);
      return {
        stage: "assemble",
        page: index + 1,
        ...pageId !== void 0 ? { pageId } : {},
        ...file2 !== void 0 ? { file: file2 } : {},
        field,
        message: slide[3]
      };
    }
    const page = /^page "([^"]+)"/.exec(line);
    const specField = /— pages\.(\d+)\.([^:\s]+):/.exec(line);
    const file = specFailed || specField ? SPEC_FILENAME : page ? `${PAGES_DIRNAME}/${page[1]}.json` : void 0;
    return {
      stage: "assemble",
      ...specField ? { page: Number(specField[1]) + 1 } : {},
      ...page ? { pageId: page[1] } : {},
      ...file !== void 0 ? { file } : {},
      ...specField ? { field: specField[2] } : {},
      message: line
    };
  });
}
function signatureSummary(signature) {
  const all = signature.offered === signature.pages ? "" : ` (${signature.pages} pages in all)`;
  return `signature layouts: ${signature.drawn} of the ${signature.offered} page${signature.offered === 1 ? "" : "s"} that can take one${all}`;
}
function signatureHint(entry) {
  const page = entry.pageId !== void 0 ? `page ${entry.page} (${entry.pageId})` : `page ${entry.page}`;
  const near = entry.nearest;
  if (near === void 0) return `${page}: drawn plain`;
  const changes = near.changes.length > 0 ? `to change: ${near.changes.join(", ")}` : "it has the recipe and the drawing still declined it: the words run long, or say something the drawing does not set";
  return `${page}: drawn plain, nearest ${near.id} (${near.look}). write: ${near.write}. ${changes}`;
}
function where(issue) {
  const parts = [];
  if (issue.page !== void 0) parts.push(issue.pageId !== void 0 ? `page ${issue.page} (${issue.pageId})` : `page ${issue.page}`);
  else if (issue.pageId !== void 0) parts.push(`page "${issue.pageId}"`);
  if (issue.file !== void 0) parts.push(issue.field !== void 0 ? `${issue.file} ${issue.field}` : issue.file);
  else if (issue.field !== void 0) parts.push(issue.field);
  return parts.length > 0 ? `${parts.join(" \u2014 ")}: ` : "";
}
function issueLine(issue) {
  const code = issue.code !== void 0 ? `[${issue.code}] ` : "";
  return `${where(issue)}${code}${issue.message} (${issue.stage})`;
}
function formatBuildReport(report) {
  const lines = [];
  if (report.status === "ok") {
    const theme2 = report.theme !== void 0 ? `, theme "${report.theme}"` : "";
    lines.push(`OK: ${report.pageCount} page${report.pageCount === 1 ? "" : "s"}${theme2}, audit clean`);
  } else {
    const n = report.errors.length;
    lines.push(`needs revision: ${n} problem${n === 1 ? "" : "s"}, no .pptx written`);
    for (const issue of report.errors) lines.push(`  ${issueLine(issue)}`);
  }
  if (report.writtenFor !== void 0) {
    lines.push(
      `note: this deck's pages were written for theme "${report.writtenFor}". Theme "${report.theme}" leaves off or cuts what the warnings below name. The sources keep all of it: building under "${report.writtenFor}" draws it whole, and rewriting those pages to fit "${report.theme}" makes them this theme's.`
    );
  }
  for (const issue of report.warnings) lines.push(`warning: ${issueLine(issue)}`);
  for (const landed of report.drawnAs ?? []) {
    const page = landed.pageId !== void 0 ? `page ${landed.page} (${landed.pageId})` : `page ${landed.page}`;
    lines.push(`note: ${page}: theme "${report.theme}" draws this "${landed.kind}" page as "${landed.drawnAs}", the nearest kind whose face takes it`);
  }
  if (report.signature !== void 0 && report.signature.offered > 0) {
    lines.push(signatureSummary(report.signature));
    const plain = report.signature.perPage.filter((entry) => entry.drawnBy === null);
    for (const entry of plain) lines.push(`  hint: ${signatureHint(entry)}`);
    if (plain.length > 0) lines.push("  hints only: rewrite a page where its content holds the recipe, and leave it plain where it does not. Never add content to fit");
  }
  if (report.alternatives !== void 0 && report.alternatives.themes.length > 0) {
    const named = report.alternatives.themes.map((theme2, i) => `${i + 1} ${theme2.theme}`).join(", ");
    lines.push(`alternatives: the deck's own pages in ${named} (${report.alternatives.dir}). To switch, change "theme" in ${SPEC_FILENAME} and build again.`);
  }
  if (report.preview !== null) lines.push(`preview: ${report.preview.html}`);
  if (report.pptx !== null) lines.push(`pptx: ${report.pptx}`);
  lines.push(...report.notes);
  return lines.join("\n");
}

// src/cli/written-for.ts
import { readFile as readFile4, writeFile as writeFile4 } from "fs/promises";
import { join as join5 } from "path";
var WRITTEN_FOR_FILENAME = "written-for.json";
async function readWrittenFor(workspaceDir) {
  let raw;
  try {
    raw = await readFile4(join5(workspaceDir, WRITTEN_FOR_FILENAME), "utf8");
  } catch (e) {
    if (e.code === "ENOENT") return void 0;
    throw e;
  }
  try {
    const value = JSON.parse(raw);
    return typeof value.theme === "string" && value.theme !== "" ? value.theme : void 0;
  } catch {
    return void 0;
  }
}
async function writeWrittenFor(workspaceDir, theme2) {
  await writeFile4(join5(workspaceDir, WRITTEN_FOR_FILENAME), `${JSON.stringify({ theme: theme2 }, null, 2)}
`);
}

// src/cli/build-alternatives.ts
import { mkdir as mkdir4, rm as rm2, writeFile as writeFile5 } from "fs/promises";
import { join as join6 } from "path";
var ALTERNATIVES_DIRNAME = "alternatives";
var ALTERNATIVES_MAX = 3;
var CONTENT_PAGES_MAX = 2;
var CONTENT_PAGES_TRIED = 6;
function strategyOf(ir) {
  const narrative = ir.narrative;
  if (typeof narrative === "string") return narrative;
  return typeof narrative?.strategy === "string" ? narrative.strategy : void 0;
}
function alternativeCandidates(ir, bound) {
  const shortlist = themeShortlist({ occasions: bound.occasions, strategy: strategyOf(ir) });
  const ordered = [...shortlist, ...BUILTIN_THEME_IDS.filter((id) => !shortlist.includes(id))];
  return ordered.filter((id) => id !== bound.id && id !== ir.theme.id);
}
function drawAlone(ir, slide, theme2) {
  const raw = { ...ir, theme: { ...ir.theme, id: theme2.id }, slides: [slide] };
  const v2 = validateIr(raw, { theme: theme2 });
  if (!v2.ok) return void 0;
  return renderSlideSvg(v2.ir, 0, { theme: theme2 });
}
function kindOf(slide) {
  return slide.type === "content" ? slide.kind : void 0;
}
function drawIn(ir, theme2) {
  const drawn = [];
  const coverIndex = ir.slides.findIndex((slide) => slide.type === "cover");
  if (coverIndex !== -1) {
    const svg = drawAlone(ir, ir.slides[coverIndex], theme2);
    if (svg !== void 0) drawn.push({ index: coverIndex, slide: ir.slides[coverIndex], svg });
  }
  const content = ir.slides.map((slide, index) => ({ slide, index })).filter(({ slide }) => slide.type === "content" && slide.placeholder !== true).slice(0, CONTENT_PAGES_TRIED);
  const drawable = [];
  for (const { slide, index } of content) {
    const svg = drawAlone(ir, slide, theme2);
    if (svg !== void 0) drawable.push({ index, slide, svg });
  }
  const first = drawable[0];
  const second = drawable.find((d) => d !== first && kindOf(d.slide) !== kindOf(first.slide)) ?? drawable[1];
  const taken = [first, second].filter((d) => d !== void 0).slice(0, CONTENT_PAGES_MAX);
  taken.sort((a, b) => a.index - b.index);
  if (taken.length === 0) return void 0;
  return [...drawn, ...taken];
}
async function writeBuildAlternatives(ir, bound, workspaceDir) {
  const started = performance.now();
  const dir = join6(workspaceDir, ALTERNATIVES_DIRNAME);
  const themes = [];
  for (const id of alternativeCandidates(ir, bound)) {
    if (themes.length >= ALTERNATIVES_MAX) break;
    const theme2 = getThemeDefinition(id);
    const drawn = drawIn(ir, theme2);
    if (drawn === void 0) continue;
    const pageFiles = drawn.map((d) => ({ name: `${id}-${String(d.index + 1).padStart(2, "0")}.svg`, svg: d.svg }));
    themes.push({
      theme: id,
      name: theme2.label ?? id,
      pages: drawn.map((d, i) => ({
        page: d.index + 1,
        ...d.slide.id !== void 0 ? { id: d.slide.id } : {},
        type: d.slide.type ?? "content",
        file: join6(dir, pageFiles[i].name)
      })),
      pageFiles
    });
  }
  await rm2(dir, { recursive: true, force: true });
  await mkdir4(dir, { recursive: true });
  for (const theme2 of themes) for (const page of theme2.pageFiles) await writeFile5(join6(dir, page.name), page.svg);
  const ms = Math.round(performance.now() - started);
  const manifest = {
    bound: ir.theme.id,
    slide: { width: CANVAS_W_PX, height: CANVAS_H_PX },
    themes: themes.map((theme2) => ({
      id: theme2.theme,
      label: theme2.name,
      pages: theme2.pages.map((page, i) => ({ page: page.page, ...page.id !== void 0 ? { id: page.id } : {}, type: page.type, file: theme2.pageFiles[i].name }))
    }))
  };
  await writeFile5(join6(dir, "manifest.json"), `${JSON.stringify(manifest, null, 2)}
`);
  return { dir, themes: themes.map(({ pageFiles: _files, ...theme2 }) => theme2), ms };
}

// src/lib/slide-edge.ts
var TAG = /<(\/?)(g|rect)\b([^>]*?)(\/?)>/g;
var ATTR_CACHE = /* @__PURE__ */ new Map();
function attr(attrs, name) {
  let re = ATTR_CACHE.get(name);
  if (!re) {
    re = new RegExp(`\\b${name}="([^"]*)"`);
    ATTR_CACHE.set(name, re);
  }
  const m = re.exec(attrs);
  return m ? m[1] : void 0;
}
function num(attrs, name, fallback) {
  const raw = attr(attrs, name);
  if (raw === void 0) return fallback;
  const n = Number(raw);
  return Number.isFinite(n) ? n : fallback;
}
function isOpaque(attrs) {
  for (const name of ["opacity", "fill-opacity"]) {
    const raw = attr(attrs, name);
    if (raw !== void 0 && Number(raw) < 1) return false;
  }
  return true;
}
var HEX = /^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/;
function slideEdgeFill(svg) {
  const rows = new Array(CANVAS_H_PX);
  let moved = 0;
  const open = [];
  let painted = false;
  TAG.lastIndex = 0;
  for (let m = TAG.exec(svg); m; m = TAG.exec(svg)) {
    const [, closing, tag, attrs, selfClosing] = m;
    if (tag === "g") {
      if (closing) {
        if (open.pop()) moved--;
        continue;
      }
      const movesChildren = /\btransform="/.test(attrs);
      if (selfClosing) continue;
      open.push(movesChildren);
      if (movesChildren) moved++;
      continue;
    }
    if (closing || moved > 0) continue;
    const fill = attr(attrs, "fill");
    if (!fill || !HEX.test(fill) || !isOpaque(attrs)) continue;
    const x = num(attrs, "x", 0);
    const width = num(attrs, "width", 0);
    if (x > 0 || x + width < CANVAS_W_PX) continue;
    const y = num(attrs, "y", 0);
    const height = num(attrs, "height", 0);
    const top = Math.max(0, Math.round(y));
    const bottom = Math.min(CANVAS_H_PX, Math.round(y + height));
    for (let r = top; r < bottom; r++) rows[r] = fill;
    if (bottom > top) painted = true;
  }
  if (!painted) return null;
  let last;
  for (let r = 0; r < CANVAS_H_PX; r++) {
    if (rows[r]) last = rows[r];
    else rows[r] = last;
  }
  for (let r = CANVAS_H_PX - 1; r >= 0; r--) {
    if (rows[r]) last = rows[r];
    else rows[r] = last;
  }
  const stops = [];
  for (let r = 0; r < CANVAS_H_PX; r++) {
    const fill = rows[r];
    const run = stops[stops.length - 1];
    if (run && run.fill === fill) run.bottom = r + 1;
    else stops.push({ fill, top: r, bottom: r + 1 });
  }
  if (stops.length === 1) return stops[0].fill;
  const pct = (row) => `${(row / CANVAS_H_PX * 100).toFixed(3).replace(/\.?0+$/, "")}%`;
  const body = stops.map((s) => `${s.fill} ${pct(s.top)} ${pct(s.bottom)}`).join(",");
  return `linear-gradient(180deg,${body})`;
}

// src/lib/svg-ids.ts
function namespaceSvgIds(svg, prefix) {
  if (!prefix) return svg;
  return svg.replace(/\bid="([^"]*)"/g, (_m, id) => `id="${prefix}${id}"`).replace(/url\(#([^)"']*)\)/g, (_m, id) => `url(#${prefix}${id})`).replace(/\b(xlink:href|href)="#([^"]*)"/g, (_m, attr2, id) => `${attr2}="#${prefix}${id}"`);
}
function svgIdPrefix(index) {
  return `s${index}-`;
}

// src/cli/preview-html.ts
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function embedJson(value) {
  return JSON.stringify(value).replace(/</g, "\\u003c");
}
function findingBadge(count, className) {
  if (count === 0) return "";
  return `<div class="${className}" aria-hidden="true">${count}</div>`;
}
function slideNode(slide, findingCount) {
  const idAttr = slide.id !== void 0 ? ` data-id="${escapeHtml(slide.id)}"` : "";
  const badge = slide.placeholder ? `<div class="pf-badge" aria-hidden="true">unfilled</div>` : "";
  const fBadge = findingBadge(findingCount, "pf-finding-badge");
  const svg = namespaceSvgIds(slide.svg, svgIdPrefix(slide.index));
  const edgeAttr = edgeAttribute(slide, "data-edge");
  return `<div class="pf-slide" id="pf-slide-${slide.index}" data-index="${slide.index}"${idAttr}${edgeAttr}>${badge}${fBadge}${svg}</div>`;
}
function edgeAttribute(slide, name) {
  const edge = slideEdgeFill(slide.svg);
  if (!edge) return "";
  return ` ${name}="${escapeHtml(name === "style" ? `background:${edge}` : edge)}"`;
}
function thumbDescription(slide) {
  const parts = [`slide ${slide.index + 1}`, slide.type];
  if (slide.id !== void 0) parts.push(slide.id);
  if (slide.placeholder) parts.push("unfilled");
  return escapeHtml(parts.join(" \xB7 "));
}
function positionLabel(slide) {
  const idPart = slide.id !== void 0 ? ` \xB7 ${slide.id}` : "";
  return escapeHtml(`${slide.index + 1}${idPart}`);
}
function counterText(slide, total) {
  const idPart = slide.id !== void 0 ? ` \xB7 ${slide.id}` : "";
  return escapeHtml(`${slide.index + 1} / ${total}${idPart}`);
}
function thumbButton(slide, isActive, slotContent, findingCount) {
  const description = thumbDescription(slide);
  const badge = slide.placeholder ? `<span class="pf-thumb-badge" aria-hidden="true">unfilled</span>` : "";
  const fBadge = findingBadge(findingCount, "pf-thumb-finding-badge");
  return `<button type="button" class="pf-thumb${isActive ? " pf-thumb-active" : ""}" id="pf-thumb-${slide.index}" data-index="${slide.index}" title="${description}" aria-label="${description}"><span class="pf-thumb-slot" id="pf-slot-${slide.index}"${edgeAttribute(slide, "style")}>${slotContent}</span><span class="pf-thumb-label">${positionLabel(slide)}</span>${badge}${fBadge}</button>`;
}
function findingPanelEntry(f) {
  const idPart = f.slideId !== void 0 ? ` \xB7 ${escapeHtml(f.slideId)}` : "";
  return `<button type="button" class="pf-finding" data-page-index="${f.page - 1}"><span class="pf-finding-loc">page ${f.page}${idPart}</span><span class="pf-finding-code">[${escapeHtml(f.code)}]</span> <span class="pf-finding-msg">${escapeHtml(f.message)}</span></button>`;
}
var CSS = `
:root{
  --bg:#f4f4f2;--panel:#fff;--line:#d9d9d4;--ink:#1b1b19;--ink-dim:#6d6d66;
  --stage:#e8e8e4;--warn:#9a6b16;--bad:#a8342d;--radius:10px;
  color-scheme:light
}
body[data-surround="dark"]{
  --bg:#17181a;--panel:#1f2124;--line:#34373c;--ink:#e9eaec;--ink-dim:#9195a0;--stage:#101113;
  color-scheme:dark
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{display:flex;flex-direction:column;background:var(--bg);color:var(--ink);
  font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB",sans-serif;
  -webkit-font-smoothing:antialiased}

header{display:flex;align-items:center;gap:14px;padding:11px 18px;background:var(--panel);
  border-bottom:1px solid var(--line);flex:0 0 auto}
#pf-title{font-weight:650;letter-spacing:-.01em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#pf-counter{font-variant-numeric:tabular-nums;color:var(--ink-dim);white-space:nowrap;font-size:13px}
.pf-spacer{flex:1 1 auto}
#pf-audit-note{color:var(--warn);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:46ch}
#pf-audit-checks{color:var(--ink-dim);font-size:12px;white-space:nowrap}

.pf-seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;flex:0 0 auto}
.pf-seg button{appearance:none;border:0;border-right:1px solid var(--line);background:transparent;color:var(--ink);
  font:inherit;font-size:13px;padding:4px 10px;cursor:pointer}
.pf-seg button:last-child{border-right:0}
.pf-seg button[aria-pressed="true"]{background:var(--ink);color:var(--panel)}
.pf-seg button:hover:not([aria-pressed="true"]){background:var(--stage)}

/* container-type:size so the stage below can ask this box how tall it is
   instead of guessing. Legal here because the box's own size never depends on
   its contents: it is a flex item stretched to the body's width and given the
   leftover height by flex:1 1 auto. */
#pf-stage-wrap{container-type:size;flex:1 1 auto;min-height:0;display:flex;align-items:center;
  justify-content:center;gap:16px;padding:18px}
/* The stage has to fit both ways: as wide as its height allows, never wider
   than the room left beside the findings panel. Sizing it off its height and
   capping the width is the only arrangement that holds in both directions.
   Measured, not reasoned about: height-driven rules (height:100%) overflow
   when width is the tighter axis, and width-driven ones
   (width:100%;max-height:100%) stop being 16:9 when height is.
   100cqh is the wrap's real content height. It used to be 100vh - 210px, a
   guess at what the header and filmstrip take. Guess high and the slide comes
   out smaller than the window allows; guess low and the box comes out wider
   than 16:9, which aspect-ratio cannot correct once both width and max-height
   are set -- the slide then letterboxes inside its own stage and paints a grey
   bar down each side. The first declaration is that old guess, left in as the
   fallback a browser without container query units will land on. */
#pf-stage{position:relative;background:var(--stage);box-shadow:0 10px 40px rgba(0,0,0,.18);
  aspect-ratio:16/9;max-height:100%;
  width:min(100%,calc((100vh - 210px) * 16 / 9));
  width:min(100%,calc(100cqh * 16 / 9))}
#pf-stage,.pf-thumb-slot{position:relative}
.pf-slide{position:absolute;inset:0}
.pf-slide svg{display:block;width:100%;height:100%}

#pf-side{flex:0 0 250px;align-self:stretch;overflow-y:auto;background:var(--panel);
  border:1px solid var(--line);border-radius:var(--radius);padding:12px 13px;font-size:13px}
#pf-side h2{margin:0 0 8px;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-dim)}
.pf-finding{display:block;width:100%;text-align:left;background:transparent;border:1px solid var(--line);
  border-radius:8px;padding:7px 9px;margin-bottom:7px;cursor:pointer;font:inherit;color:var(--ink)}
.pf-finding:hover{background:var(--stage)}
.pf-finding-loc{display:block;font-size:11px;color:var(--ink-dim)}
.pf-finding-code{display:inline-block;font-size:11px;font-weight:700;color:var(--bad)}
.pf-finding-msg{display:block;font-size:12px;color:var(--ink-dim);margin-top:2px}

/* The strip is cut off by its own right edge when it scrolls, which reads as
   a clipping bug rather than as "there is more this way" -- the last thumbnail
   is simply sliced, and inside an embedder's rounded frame it is sliced on a
   curve. The two widths are driven from script (see fadeStrip) and are 0 until
   there is really something hidden on that side, so a strip that fits is
   untouched: at 0 the gradient is opaque from edge to edge. */
#pf-filmstrip{display:flex;gap:10px;padding:11px 18px;overflow-x:auto;background:var(--panel);
  border-top:1px solid var(--line);flex:0 0 auto;--pf-fade-l:0px;--pf-fade-r:0px;
  -webkit-mask-image:linear-gradient(to right,transparent 0,#000 var(--pf-fade-l),
    #000 calc(100% - var(--pf-fade-r)),transparent 100%);
  mask-image:linear-gradient(to right,transparent 0,#000 var(--pf-fade-l),
    #000 calc(100% - var(--pf-fade-r)),transparent 100%)}
.pf-thumb{flex:0 0 auto;width:154px;padding:0;margin:0;border:1px solid var(--line);background:var(--panel);
  cursor:pointer;border-radius:8px;overflow:hidden;position:relative;font:inherit;text-align:left}
.pf-thumb:hover{border-color:var(--ink-dim)}
.pf-thumb-active,.pf-thumb-active:hover{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink)}
.pf-thumb-slot{display:block;width:100%;aspect-ratio:16/9;background:var(--stage)}
/* The active slide's SVG lives in the stage, not here \u2014 one node per slide,
   moved between the two homes. Without this the vacated slot reads as a
   broken empty box, so it states what it is instead. */
.pf-thumb-active .pf-thumb-slot::after{content:"on stage";position:absolute;inset:0;display:flex;
  align-items:center;justify-content:center;font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink-dim)}
.pf-thumb-label{display:block;font-size:11px;line-height:1.5;padding:4px 7px;color:var(--ink-dim);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pf-badge,.pf-thumb-badge{position:absolute;top:5px;right:5px;background:var(--warn);color:#fff;font-size:10px;
  font-weight:700;letter-spacing:.03em;padding:2px 6px;border-radius:999px;text-transform:uppercase;z-index:2;pointer-events:none}
.pf-finding-badge,.pf-thumb-finding-badge{position:absolute;top:5px;left:5px;background:var(--bad);color:#fff;
  font-size:10px;font-weight:700;padding:2px 6px;border-radius:999px;z-index:2;pointer-events:none}
`.trim();
var JS = `
(function () {
  var stage = document.getElementById('pf-stage')
  var counter = document.getElementById('pf-counter')
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('.pf-thumb'))
  var total = thumbs.length
  if (total === 0) return
  var current = parseInt(thumbs[0].getAttribute('data-index'), 10)

  function slideEl(i) { return document.getElementById('pf-slide-' + i) }
  function slotEl(i) { return document.getElementById('pf-slot-' + i) }
  function thumbEl(i) { return document.getElementById('pf-thumb-' + i) }
  function thumbPos(i) {
    for (var t = 0; t < thumbs.length; t++) {
      if (parseInt(thumbs[t].getAttribute('data-index'), 10) === i) return t
    }
    return -1
  }

  function updateCounter(i) {
    var el = slideEl(i)
    if (!el) return
    var text = (thumbPos(i) + 1) + ' / ' + total
    var id = el.getAttribute('data-id')
    if (id) text += ' \xB7 ' + id
    counter.textContent = text
  }

  function activate(i) {
    if (i === current) return
    var nextSlide = slideEl(i)
    var nextThumb = thumbEl(i)
    if (!nextSlide || !nextThumb) return
    var prevSlide = slideEl(current)
    var prevSlot = slotEl(current)
    if (prevSlide && prevSlot) prevSlot.appendChild(prevSlide)
    var prevThumb = thumbEl(current)
    if (prevThumb) prevThumb.classList.remove('pf-thumb-active')
    stage.appendChild(nextSlide)
    stage.style.background = nextSlide.getAttribute('data-edge') || ''
    nextThumb.classList.add('pf-thumb-active')
    nextThumb.scrollIntoView({ block: 'nearest', inline: 'nearest' })
    current = i
    updateCounter(i)
  }

  thumbs.forEach(function (t) {
    t.addEventListener('click', function () {
      activate(parseInt(t.getAttribute('data-index'), 10))
    })
  })

  document.addEventListener('keydown', function (e) {
    var pos = thumbPos(current)
    if (e.key === 'ArrowRight' && pos < total - 1) {
      activate(parseInt(thumbs[pos + 1].getAttribute('data-index'), 10))
    } else if (e.key === 'ArrowLeft' && pos > 0) {
      activate(parseInt(thumbs[pos - 1].getAttribute('data-index'), 10))
    }
  })

  // Click a finding, jump to its page \u2014 the same activate() a thumbnail uses.
  Array.prototype.slice.call(document.querySelectorAll('.pf-finding')).forEach(function (b) {
    b.addEventListener('click', function () {
      activate(parseInt(b.getAttribute('data-page-index'), 10))
    })
  })

  // Fade whichever end of the strip has more thumbnails behind it. Driven
  // from here rather than left to CSS because no CSS rule can ask whether a
  // box currently overflows. See the #pf-filmstrip rule for why it matters.
  var strip = document.getElementById('pf-filmstrip')
  function fadeStrip() {
    if (!strip || thumbs.length === 0) return
    // Measured off the thumbnails, not off scrollWidth. The strip's own
    // 18px of padding counts as scrollable width, so scrollWidth says there
    // is more to the right while a reader is already looking at the last
    // thumbnail \u2014 and activate()'s scrollIntoView stops exactly there,
    // leaving the padding unscrolled. The fade would then claim there is
    // more to see and dim the selected thumbnail's own ring to do it. Asking
    // whether a thumbnail is actually cut off is what the fade means anyway.
    var box = strip.getBoundingClientRect()
    var hiddenLeft = box.left - thumbs[0].getBoundingClientRect().left
    var hiddenRight = thumbs[thumbs.length - 1].getBoundingClientRect().right - box.right
    // A pixel of slack: sub-pixel layout leaves a fraction of overflow on
    // strips that visibly fit, and fading those is the bug in reverse.
    strip.style.setProperty('--pf-fade-l', (hiddenLeft > 1 ? 28 : 0) + 'px')
    strip.style.setProperty('--pf-fade-r', (hiddenRight > 1 ? 28 : 0) + 'px')
  }
  if (strip) {
    fadeStrip()
    strip.addEventListener('scroll', fadeStrip, { passive: true })
    // The strip also stops and starts overflowing as the window changes width,
    // and scrollIntoView moves it without a resize.
    window.addEventListener('resize', fadeStrip)
    if (window.ResizeObserver) new ResizeObserver(fadeStrip).observe(strip)
  }

  // Open on a given page: #page=3 is the third thumbnail, not slide index 3.
  // A reader who clicks page 3 in a harness that embeds this file expects to
  // land on page 3, and the embedder has no other way to say so \u2014 it holds a
  // URL, not a handle on this script. Reading the position rather than the
  // index keeps that promise honest for a deck whose slides are not numbered
  // 0..n-1. Silently ignored when it names a page this deck does not have.
  function fromHash() {
    var m = /(?:^|[#&])page=(\\d+)/.exec(location.hash || '')
    if (!m) return
    var pos = parseInt(m[1], 10) - 1
    // >= 0, not > 0. Page 1 is a no-op on first load, but not afterwards: a
    // reader who pages forward and then hits Back gets #page=1 in the URL,
    // and skipping it leaves the address bar and the deck disagreeing.
    // activate() already returns early when it is handed the current page.
    if (pos >= 0 && pos < total) activate(parseInt(thumbs[pos].getAttribute('data-index'), 10))
  }
  fromHash()
  window.addEventListener('hashchange', fromHash)

  // Light/dark surround. A deck is judged on color and weight, and the
  // surround it sits on changes both \u2014 a dark theme reads muddy on a light
  // page and vice versa, so the reviewer picks rather than the page deciding.
  var seg = document.getElementById('pf-surround')
  if (seg) {
    seg.addEventListener('click', function (e) {
      var btn = e.target.closest('button')
      if (!btn) return
      document.body.setAttribute('data-surround', btn.getAttribute('data-surround'))
      Array.prototype.slice.call(seg.children).forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn))
      })
    })
  }
})()
`.trim();
function buildPreviewHtml(input) {
  const { title, slides, findings = [], auditNote, checks } = input;
  const total = slides.length;
  const escapedTitle = escapeHtml(title);
  const findingsByPage = /* @__PURE__ */ new Map();
  for (const f of findings) {
    const list = findingsByPage.get(f.page);
    if (list) list.push(f);
    else findingsByPage.set(f.page, [f]);
  }
  const countFor = (slide) => findingsByPage.get(slide.index + 1)?.length ?? 0;
  const stageSlide = total > 0 ? slideNode(slides[0], countFor(slides[0])) : "";
  const stageEdge = total > 0 ? edgeAttribute(slides[0], "style") : "";
  const thumbs = slides.map((s, i) => thumbButton(s, i === 0, i === 0 ? "" : slideNode(s, countFor(s)), countFor(s))).join("");
  const initialCounter = total > 0 ? counterText(slides[0], total) : "0 / 0";
  const auditPanel = findings.length > 0 ? `<section id="pf-audit-panel"><h2>Audit findings (${findings.length})</h2><div id="pf-audit-list">${findings.map(findingPanelEntry).join("")}</div></section>` : "";
  const findingsDataScript = findings.length > 0 ? `<script type="application/json" id="pf-audit-findings">${embedJson(findings)}</script>` : "";
  const auditNoteHtml = auditNote !== void 0 ? `<span id="pf-audit-note">${escapeHtml(auditNote)}</span>` : "";
  const checksLine = checks !== void 0 ? `<span id="pf-audit-checks">audit: svg ${checks.svg} \xB7 pixels ${checks.pixels}</span>` : "";
  const sideHtml = auditPanel ? `<aside id="pf-side">${auditPanel}</aside>` : "";
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapedTitle} \u2014 pptwise preview</title>
<style>${CSS}</style>
</head>
<body data-surround="light">
<header>
<span id="pf-title">${escapedTitle}</span>
<span id="pf-counter">${initialCounter}</span>
<span class="pf-spacer"></span>
${auditNoteHtml}
${checksLine}
<div class="pf-seg" id="pf-surround" role="group" aria-label="surround">
<button type="button" data-surround="light" aria-pressed="true">Light</button>
<button type="button" data-surround="dark" aria-pressed="false">Dark</button>
</div>
</header>
<div id="pf-stage-wrap"><div id="pf-stage"${stageEdge}>${stageSlide}</div>${sideHtml}</div>
<nav id="pf-filmstrip" aria-label="slides">${thumbs}</nav>
${findingsDataScript}
<script>${JS}</script>
</body>
</html>
`;
}
var CONTACT_SHEET_CSS = `
:root { color-scheme: light; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font: 14px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  color: #111;
  background: #f4f4f1;
  padding: 24px;
}
h1 { font-size: 18px; font-weight: 600; margin: 0 0 16px; }
table.cs { width: 100%; border-collapse: collapse; table-layout: fixed; }
table.cs th, table.cs td { vertical-align: top; padding: 8px; }
table.cs td.cs-missing { color: #8a8a85; vertical-align: middle; text-align: center; }
table.cs thead th { text-align: left; font-size: 13px; font-weight: 600; }
table.cs tbody th { text-align: left; font-weight: 500; color: #555; width: 88px; }
.cs-cell svg { display: block; width: 100%; height: auto; background: #fff; }
`.trim();
function buildContactSheetHtml(input) {
  const { title, themes } = input;
  const rowLabels = [];
  for (const col of themes) {
    for (const slide of col.slides) {
      const label = slide.label ?? slide.type;
      if (!rowLabels.includes(label)) rowLabels.push(label);
    }
  }
  const head = themes.map((t) => `<th scope="col">${escapeHtml(t.id)}</th>`).join("");
  const body = rowLabels.map((label) => {
    const cells = themes.map((t, colIdx) => {
      const slide = t.slides.find((s) => (s.label ?? s.type) === label);
      if (!slide) return `<td class="cs-missing">not in ${escapeHtml(t.id)}'s menu</td>`;
      const svg = namespaceSvgIds(slide.svg, `t${colIdx}-${label}-`);
      return `<td class="cs-cell">${svg}</td>`;
    }).join("");
    return `<tr><th scope="row">${escapeHtml(label)}</th>${cells}</tr>`;
  }).join("");
  const escapedTitle = escapeHtml(title);
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapedTitle} \u2014 theme comparison</title>
<style>${CONTACT_SHEET_CSS}</style>
</head>
<body>
<h1>${escapedTitle}</h1>
<table class="cs">
<thead><tr><th></th>${head}</tr></thead>
<tbody>${body}</tbody>
</table>
</body>
</html>
`;
}
var THEME_WALL_CSS = `
:root { color-scheme: light; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font: 14px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  color: #111;
  background: #f4f4f1;
  padding: 24px;
}
h1 { font-size: 18px; font-weight: 600; margin: 0 0 16px; }
table.tw { width: 100%; max-width: 1200px; border-collapse: collapse; table-layout: fixed; }
table.tw th, table.tw td { vertical-align: top; padding: 8px; }
table.tw thead th { text-align: left; font-size: 13px; font-weight: 600; color: #555; }
table.tw tr > th:first-child { text-align: left; width: 120px; }
table.tw tbody th span { display: block; font-weight: 600; }
table.tw tbody th code { font-size: 12px; color: #777; }
td.tw-missing { color: #8a8a85; font-size: 12px; }
.tw-cell svg { display: block; width: 100%; height: auto; background: #fff; }
`.trim();
function buildThemeWallHtml(input) {
  const head = input.columns.map((column) => `<th scope="col">${escapeHtml(column)}</th>`).join("");
  const body = input.rows.map((row, rowIdx) => {
    const cells = row.cells.map((cell) => {
      if ("reason" in cell) return `<td class="tw-missing">${escapeHtml(cell.reason)}</td>`;
      return `<td class="tw-cell">${namespaceSvgIds(cell.svg, `w${rowIdx}-${cell.type}-`)}</td>`;
    }).join("");
    return `<tr><th scope="row"><span>${escapeHtml(row.label)}</span><code>${escapeHtml(row.id)}</code></th>${cells}</tr>`;
  }).join("");
  const escapedTitle = escapeHtml(input.title);
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapedTitle} \u2014 themes</title>
<style>${THEME_WALL_CSS}</style>
</head>
<body>
<h1>${escapedTitle}</h1>
<table class="tw">
<thead><tr><th></th>${head}</tr></thead>
<tbody>${body}</tbody>
</table>
</body>
</html>
`;
}

// src/cli/theme-wall.ts
var THEME_WALL_LANGS = ["zh", "en"];
var THEME_WALL_MANIFEST_VERSION = 1;
var THEME_WALL_MANIFEST_FILE = "manifest.json";
var THEME_WALL_SHEET_FILE = "contact-sheet.html";
var DEFAULT_CONTENT_PAGE = {
  zh: {
    type: "content",
    kind: "points",
    heading: "\u8FD9\u4E00\u5B63\u6211\u4EEC\u5B9A\u4E0B\u7684\u4E09\u4EF6\u4E8B",
    components: [{ type: "bullets", items: ["\u62DB\u8058\u540D\u989D\u51BB\u7ED3\u5728 42 \u4EBA", "\u6682\u505C\u5206\u6790\u5E73\u53F0\u91CD\u5EFA", "\u5BA2\u670D\u8F6E\u503C\u7531\u5404\u7EC4\u5206\u62C5"] }]
  },
  en: {
    type: "content",
    kind: "points",
    heading: "What we decided",
    components: [{ type: "bullets", items: ["Hold hiring at 42", "Cut the analytics rebuild", "Share the support rotation"] }]
  }
};
var CJK = /[぀-ヿ㐀-鿿豈-﫿가-힯]/;
function themeWallLang(title, lang) {
  if (lang === void 0) return CJK.test(title) ? "zh" : "en";
  const base = lang.trim().toLowerCase().split(/[-_]/)[0];
  const found = THEME_WALL_LANGS.find((candidate) => candidate === base);
  if (found === void 0) {
    throw new PptwiseError(`unknown --lang "${lang}". Use one of: ${THEME_WALL_LANGS.join(", ")}`);
  }
  return found;
}
function themeWallContentPage(raw, source) {
  if (raw === null || typeof raw !== "object" || Array.isArray(raw)) {
    throw new PptwiseError(`${source} must hold one content page as a JSON object`);
  }
  const page = { ...raw };
  if (page.type === void 0) page.type = "content";
  if (page.type !== "content") {
    throw new PptwiseError(`${source} holds a ${String(page.type)} page. --page takes one content page, with its kind`);
  }
  return page;
}
function pageReason(errors) {
  return formatIssues(errors.map((issue) => ({ path: issue.path.replace(/^slides\.0\.?/, "") || "page", message: issue.message })));
}
function drawPage(slide, theme2) {
  const raw = { version: "5", filename: "theme-try", theme: { id: theme2.id }, slides: [slide] };
  const v2 = validateIr(raw, { theme: theme2.definition });
  if (!v2.ok) return { reason: pageReason(v2.errors) };
  return { svg: renderSlideSvg(v2.ir, 0, { theme: theme2.definition }) };
}
function buildThemeWall(input) {
  const cover = {
    type: "cover",
    heading: input.title,
    ...input.subtitle !== void 0 ? { subheading: input.subtitle } : {}
  };
  const content = input.contentPage ?? DEFAULT_CONTENT_PAGE[input.lang];
  const kind = typeof content.kind === "string" ? content.kind : void 0;
  const files = [];
  const rows = [];
  const themes = input.themes.map((theme2) => {
    const pages = [];
    const skipped = [];
    const row = { id: theme2.id, label: theme2.label, cells: [] };
    for (const [type, slide] of [["cover", cover], ["content", content]]) {
      const drawn = drawPage(slide, theme2);
      const pageKind = type === "content" && kind !== void 0 ? { kind } : {};
      if ("reason" in drawn) {
        skipped.push({ type, ...pageKind, reason: drawn.reason });
        row.cells.push({ type, reason: drawn.reason });
        continue;
      }
      const name = `${theme2.id}-${type}.svg`;
      files.push({ name, svg: drawn.svg });
      pages.push({ type, ...pageKind, file: name });
      row.cells.push({ type, svg: drawn.svg });
    }
    rows.push(row);
    return {
      id: theme2.id,
      label: theme2.label,
      source: theme2.source,
      pages,
      ...skipped.length > 0 ? { skipped } : {}
    };
  });
  return {
    manifest: {
      manifestVersion: THEME_WALL_MANIFEST_VERSION,
      generator: "pptwise theme try",
      pptwiseVersion: VERSION,
      title: input.title,
      ...input.subtitle !== void 0 ? { subtitle: input.subtitle } : {},
      lang: input.lang,
      slide: { width: CANVAS_W_PX, height: CANVAS_H_PX },
      contactSheet: THEME_WALL_SHEET_FILE,
      themes
    },
    files,
    rows
  };
}
function themeWallSkipNotes(themes) {
  const groups = /* @__PURE__ */ new Map();
  for (const theme2 of themes) {
    for (const skip of theme2.skipped ?? []) {
      const what = skip.kind !== void 0 ? `${skip.type} (${skip.kind})` : skip.type;
      const reason = skip.reason.replace(/\n/g, " ");
      const key = `${what}\0${reason}`;
      const group = groups.get(key) ?? { what, type: skip.type, reason, ids: [] };
      group.ids.push(theme2.id);
      groups.set(key, group);
    }
  }
  return [...groups.values()].map((group) => {
    if (group.ids.length === themes.length && themes.length > 1) {
      const fix = group.type === "content" ? " Fix the page, or leave it out to draw the default sample page" : "";
      return `note: every theme left out its ${group.what} page: ${group.reason}.${fix}`;
    }
    return `note: ${group.ids.join(", ")} left out ${group.ids.length === 1 ? "its" : "their"} ${group.what} page: ${group.reason}`;
  });
}
function formatThemeWall(manifest, dir) {
  const lines = [
    `wrote ${manifest.themes.length} theme${manifest.themes.length === 1 ? "" : "s"} (cover and one content page each) to ${dir}`,
    `  themes: ${manifest.themes.map((theme2) => theme2.id).join(", ")}`,
    `  manifest: ${THEME_WALL_MANIFEST_FILE}`,
    `  contact sheet: ${manifest.contactSheet}`,
    ...themeWallSkipNotes(manifest.themes)
  ];
  return lines.join("\n");
}

// src/cli/preview-manifest.ts
var PREVIEW_MANIFEST_VERSION = 1;
function pageSlug(slide) {
  const raw = slide.id?.trim();
  if (raw) {
    const safe = raw.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    if (safe) return safe;
  }
  return `page-${String(slide.index + 1).padStart(3, "0")}`;
}
function pageIds(slides) {
  const taken = /* @__PURE__ */ new Set();
  const claim = (candidate) => {
    if (!taken.has(candidate)) {
      taken.add(candidate);
      return candidate;
    }
    for (let n = 2; ; n++) {
      const suffixed = `${candidate}-${n}`;
      if (!taken.has(suffixed)) {
        taken.add(suffixed);
        return suffixed;
      }
    }
  };
  return slides.map((slide) => {
    const slug = pageSlug(slide);
    if (!taken.has(slug)) return claim(slug);
    return claim(`page-${String(slide.index + 1).padStart(3, "0")}`);
  });
}
function buildPreviewManifest(input) {
  const byPage = /* @__PURE__ */ new Map();
  for (const f of input.findings ?? []) {
    const list = byPage.get(f.page) ?? [];
    list.push({ code: f.code, message: f.message });
    byPage.set(f.page, list);
  }
  const ids = pageIds(input.slides);
  const pages = input.slides.map((slide, i) => {
    const findings = byPage.get(slide.index + 1) ?? [];
    return {
      id: ids[i],
      page: slide.index + 1,
      type: slide.type,
      file: slide.file,
      ...slide.id !== void 0 ? { slideId: slide.id } : {},
      ...slide.placeholder ? { placeholder: true } : {},
      ...findings.length > 0 ? { findings } : {}
    };
  });
  return {
    manifestVersion: PREVIEW_MANIFEST_VERSION,
    generator: "pptwise preview",
    pptwiseVersion: input.pptwiseVersion,
    title: input.title,
    slide: { width: input.width, height: input.height },
    ...input.checks !== void 0 ? { checks: input.checks } : {},
    ...input.auditNote !== void 0 ? { auditNote: input.auditNote } : {},
    pages
  };
}

// src/cli/workspace.ts
import { appendFile, mkdir as mkdir5, readFile as readFile5, readdir as readdir2, stat as stat2, unlink, writeFile as writeFile6 } from "fs/promises";
import { createHash } from "crypto";
import { basename as basename4, dirname as dirname3, extname as extname3, isAbsolute as isAbsolute3, join as join7, relative as relative2, resolve as resolve4, sep } from "path";

// src/cli/child.ts
import {
  execFile,
  spawn
} from "child_process";

// src/cli/win-exec.ts
import * as fs from "fs";
import * as path from "path";

// src/cli/path-lookup.ts
import { constants } from "fs";
import { access as fsAccess } from "fs/promises";
import { delimiter as defaultDelimiter, join as defaultJoin } from "path";
var DEFAULT_PATHEXT = ".COM;.EXE;.BAT;.CMD";
function envValue(env, name) {
  const upper = name.toUpperCase();
  for (const [key, value] of Object.entries(env)) {
    if (key.toUpperCase() === upper) return value;
  }
  return void 0;
}
async function findOnPath(bin, env, deps = {}) {
  const platform = deps.platform ?? process.platform;
  const join19 = deps.join ?? defaultJoin;
  const delimiter = deps.delimiter ?? defaultDelimiter;
  const tryAccess = deps.access ?? ((target, mode) => fsAccess(target, mode));
  const dirs = (envValue(env, "PATH") ?? "").split(delimiter).filter(Boolean);
  const suffixes = platform === "win32" ? [...(envValue(env, "PATHEXT") ?? DEFAULT_PATHEXT).split(";").map((ext) => ext.trim()).filter(Boolean), ""] : [""];
  for (const dir of dirs) {
    for (const suffix of suffixes) {
      const full = join19(dir, `${bin}${suffix}`);
      try {
        await tryAccess(full, constants.X_OK);
        return full;
      } catch {
      }
    }
  }
  return null;
}

// src/cli/win-exec.ts
function existenceOf(target) {
  try {
    return fs.statSync(target).isDirectory() ? "directory" : "present";
  } catch (error) {
    return error.code === "ENOENT" ? "absent" : "unknown";
  }
}
var REAL_DEPS = {
  platform: process.platform,
  readFileSync: (p) => fs.readFileSync(p, "utf8"),
  resolveOnPath: (bin, env) => findOnPath(bin, env),
  existence: existenceOf
};
var UnrecognizedBatchShimError = class extends Error {
  constructor(command) {
    super(
      `Cannot spawn "${command}" as a Windows batch file without a shell. Node refuses to run .cmd/.bat files without a shell (EINVAL after CVE-2024-27980), and wrapping the call in cmd.exe would truncate multi-line arguments at the first newline. Use a recognised npm/pnpm shim, or spawn the real executable.`
    );
    this.name = "UnrecognizedBatchShimError";
  }
};
var PATHEXT_EDIT = /^@?SET PATHEXT=%PATHEXT:;\.([A-Z]+);=;%$/;
var FLAG = /^--?[A-Za-z0-9][-A-Za-z0-9._]*(?:=[-A-Za-z0-9._/\\:]+)?$/;
function withWindowsEnvAssignment(env, name, value) {
  const upper = name.toUpperCase();
  const next = {};
  let replaced = false;
  for (const [key, val] of Object.entries(env)) {
    if (key.toUpperCase() === upper) {
      next[key] = value;
      replaced = true;
    } else {
      next[key] = val;
    }
  }
  if (!replaced) next[name] = value;
  return next;
}
function withoutWindowsEnvVariable(env, name) {
  const upper = name.toUpperCase();
  const next = {};
  for (const [key, val] of Object.entries(env)) {
    if (key.toUpperCase() !== upper) next[key] = val;
  }
  return next;
}
function withPathextEdit(env, removed) {
  const current = envValue(env, "PATHEXT") ?? "";
  const edited = current.replace(new RegExp(`;\\.${removed};`, "gi"), ";");
  if (edited === "") return withoutWindowsEnvVariable(env, "PATHEXT");
  return withWindowsEnvAssignment(env, "PATHEXT", edited);
}
function isFullyQualifiedLocalPath(target) {
  return /^[A-Za-z]:[\\/]/.test(target);
}
function templatePath(text, shimDir) {
  const rooted = /^%(?:dp0%|~dp0)\\?(.*)$/i.exec(text);
  if (!rooted) {
    return isFullyQualifiedLocalPath(text) && !text.includes("%") ? text : null;
  }
  const rest = rooted[1] ?? "";
  if (rest.includes("%") || rest === "") return null;
  return path.win32.normalize(path.win32.join(shimDir, rest));
}
function interpreterTail(middle, shimDir) {
  const tokens = middle.trim().split(/\s+/).filter((token) => token !== "");
  if (tokens.length === 0) return null;
  const quoted = /^"([^"]*)"$/.exec(tokens[tokens.length - 1] ?? "");
  if (!quoted) return null;
  const entry = templatePath(quoted[1], shimDir);
  if (entry === null) return null;
  const flags = tokens.slice(0, -1);
  return flags.every((flag) => FLAG.test(flag)) ? [...flags, entry] : null;
}
async function nodeRecipe(shimDir, tail, effective, env, deps) {
  const local = path.win32.join(shimDir, "node.exe");
  const found = deps.existence(local);
  if (found === "unknown") return null;
  if (found === "present" || found === "directory") {
    return {
      command: local,
      args: tail,
      ...effective.present === env ? {} : { env: effective.present }
    };
  }
  const resolved = await deps.resolveOnPath("node", effective.absent);
  return resolved === null ? null : {
    command: resolved,
    args: tail,
    ...effective.absent === env ? {} : { env: effective.absent }
  };
}
var NPM_PROLOGUE = [
  "@ECHO off",
  "GOTO start",
  ":find_dp0",
  "SET dp0=%~dp0",
  "EXIT /b",
  ":start",
  "SETLOCAL",
  "CALL :find_dp0"
];
var NPM_PREFIX = "endLocal & goto #_undefined_# 2>NUL || title %COMSPEC% & ";
var NPM_EXEC_LEGACY = /^"%_prog%"(.*)\s%\*$/;
var NPM_EXEC_CURRENT = /^set PATHEXT=%PATHEXT:;\.([A-Z]+);=;% & "%_prog%"(.*)\s%\*$/;
var NPM_NATIVE_EXEC = /^"([^"]*)"\s+%\*$/;
var PNPM_NODE_PATH_IF = /^@IF NOT DEFINED NODE_PATH \($/;
var PNPM_NODE_PATH_SET = /^@SET "NODE_PATH=([^"%]+)"$/;
var PNPM_NODE_PATH_PREPEND = /^@SET "NODE_PATH=([^"%]+);%NODE_PATH%"$/;
var PNPM_IF = /^@IF EXIST "([^"]*)" \($/;
var PNPM_ARM = /^"([^"]*)"(.*)\s%\*$/;
var PNPM_BARE_ARM = /^node(.*)\s%\*$/;
var PNPM_ONELINE = /^@"([^"]*)"(.*)\s%\*$/;
function normalizeLines(content) {
  const lines = content.split(/\r?\n/).map((line) => line.trim());
  while (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  return lines;
}
async function matchNpm(lines, shimDir, env, deps) {
  if (lines.length < NPM_PROLOGUE.length) return null;
  if (!NPM_PROLOGUE.every((expected, index) => lines[index] === expected)) return null;
  const body = lines.slice(NPM_PROLOGUE.length).filter((line) => line !== "");
  if (body.length === 1) {
    const native = NPM_NATIVE_EXEC.exec(body[0] ?? "");
    if (!native) return null;
    const target = templatePath(native[1], shimDir);
    if (target === null || !/\.exe$/i.test(target)) return null;
    const normalizedDir = path.win32.normalize(shimDir);
    const dp0 = normalizedDir.endsWith("\\") ? normalizedDir : `${normalizedDir}\\`;
    return { command: target, args: [], env: withWindowsEnvAssignment(env, "dp0", dp0) };
  }
  if (body[0] !== 'IF EXIST "%dp0%\\node.exe" (') return null;
  if (body[1] !== 'SET "_prog=%dp0%\\node.exe"') return null;
  if (body[2] !== ") ELSE (") return null;
  if (body[3] !== 'SET "_prog=node"') return null;
  if (body.length === 7) {
    if (!PATHEXT_EDIT.test(body[4] ?? "")) return null;
    if (body[5] !== ")") return null;
    if (!(body[6] ?? "").startsWith(NPM_PREFIX)) return null;
    const exec = NPM_EXEC_LEGACY.exec((body[6] ?? "").slice(NPM_PREFIX.length));
    if (!exec) return null;
    const tail = interpreterTail(exec[1] ?? "", shimDir);
    return tail === null ? null : nodeRecipe(shimDir, tail, { present: env, absent: env }, env, deps);
  }
  if (body.length === 6) {
    if (body[4] !== ")") return null;
    if (!(body[5] ?? "").startsWith(NPM_PREFIX)) return null;
    const exec = NPM_EXEC_CURRENT.exec((body[5] ?? "").slice(NPM_PREFIX.length));
    if (!exec) return null;
    const tail = interpreterTail(exec[2] ?? "", shimDir);
    if (tail === null) return null;
    const edited = withPathextEdit(env, exec[1] ?? "JS");
    return nodeRecipe(shimDir, tail, { present: edited, absent: edited }, env, deps);
  }
  return null;
}
async function matchPnpm(lines, shimDir, env, deps) {
  if (lines[0] !== "@SETLOCAL") return null;
  let body = lines.slice(1).filter((line) => line !== "");
  let baseEnv = env;
  if (body.length > 0 && PNPM_NODE_PATH_IF.test(body[0] ?? "")) {
    if (body.length < 5) return null;
    const set = PNPM_NODE_PATH_SET.exec(body[1] ?? "");
    const prepend = PNPM_NODE_PATH_PREPEND.exec(body[3] ?? "");
    if (!set || body[2] !== ") ELSE (" || !prepend || body[4] !== ")") return null;
    if (set[1] !== prepend[1]) return null;
    const currentValue = envValue(env, "NODE_PATH");
    const defined = currentValue !== void 0 && currentValue !== "";
    baseEnv = withWindowsEnvAssignment(env, "NODE_PATH", defined ? `${set[1]};${currentValue}` : set[1]);
    body = body.slice(5);
  }
  if (body.length === 1) {
    const one = PNPM_ONELINE.exec(body[0] ?? "");
    if (!one) return null;
    const program2 = templatePath(one[1], shimDir);
    if (program2 === null) return null;
    const onelineEnv = baseEnv === env ? {} : { env: baseEnv };
    if ((one[2] ?? "").trim() === "") {
      return /\.exe$/i.test(program2) ? { command: program2, args: [], ...onelineEnv } : null;
    }
    const tail2 = interpreterTail(one[2] ?? "", shimDir);
    return tail2 === null || /\.(cmd|bat)$/i.test(program2) ? null : { command: program2, args: tail2, ...onelineEnv };
  }
  if (body.length !== 6) return null;
  const opened = PNPM_IF.exec(body[0] ?? "");
  if (!opened) return null;
  const local = path.win32.join(shimDir, "node.exe");
  const candidate = templatePath(opened[1], shimDir);
  if (candidate === null || candidate.toLowerCase() !== local.toLowerCase()) return null;
  const present = PNPM_ARM.exec(body[1] ?? "");
  if (!present) return null;
  const presentProgram = templatePath(present[1], shimDir);
  if (presentProgram === null || presentProgram.toLowerCase() !== local.toLowerCase()) return null;
  if (body[2] !== ") ELSE (") return null;
  const edit = PATHEXT_EDIT.exec(body[3] ?? "");
  if (!edit) return null;
  const absent = PNPM_BARE_ARM.exec(body[4] ?? "");
  if (!absent) return null;
  if (body[5] !== ")") return null;
  const tail = interpreterTail(present[2] ?? "", shimDir);
  const otherTail = interpreterTail(absent[1] ?? "", shimDir);
  if (tail === null || otherTail === null || tail.join(" ") !== otherTail.join(" ")) return null;
  const removed = edit[1] ?? "JS";
  return nodeRecipe(
    shimDir,
    tail,
    { present: baseEnv, absent: withPathextEdit(baseEnv, removed) },
    env,
    deps
  );
}
async function recognizeShim(cmdPath, content, env, deps = REAL_DEPS) {
  if (!isFullyQualifiedLocalPath(cmdPath)) return null;
  const shimDir = path.win32.dirname(cmdPath);
  const lines = normalizeLines(content);
  if (lines.length === 0) return null;
  return await matchNpm(lines, shimDir, env, deps) ?? await matchPnpm(lines, shimDir, env, deps);
}
async function resolveSpawnPlan(command, args, env = process.env, _cwd, deps = REAL_DEPS) {
  if (deps.platform !== "win32") return { command, args: [...args] };
  let resolved = command;
  if (!command.includes("/") && !command.includes("\\")) {
    resolved = await deps.resolveOnPath(command, env) ?? command;
  }
  if (!/\.(cmd|bat)$/i.test(path.win32.basename(resolved))) {
    return { command: resolved, args: [...args] };
  }
  if (!isFullyQualifiedLocalPath(resolved)) {
    throw new UnrecognizedBatchShimError(command);
  }
  let content;
  try {
    content = deps.readFileSync(resolved);
  } catch {
    throw new UnrecognizedBatchShimError(command);
  }
  const recipe = await recognizeShim(resolved, content, env, deps);
  if (recipe === null) throw new UnrecognizedBatchShimError(command);
  return {
    command: recipe.command,
    args: [...recipe.args, ...args],
    ...recipe.env ? { env: recipe.env } : {}
  };
}

// src/cli/child.ts
var DRAIN_GRACE_MS = 500;
function spawnHidden(command, args = [], options = {}) {
  return spawn(command, args, { ...options, windowsHide: true });
}
var ChildTimeoutError = class extends Error {
  timedOut = true;
  constructor(timeoutMs) {
    super(`child process timed out after ${timeoutMs}ms`);
    this.name = "ChildTimeoutError";
  }
};
async function runChild(command, args = [], options = {}) {
  const { timeoutMs, signal, ...spawnOptions } = options;
  const cwd = typeof spawnOptions.cwd === "string" ? spawnOptions.cwd : void 0;
  const plan = await resolveSpawnPlan(command, args, spawnOptions.env ?? process.env, cwd);
  return new Promise((resolve11, reject) => {
    const child = spawnHidden(plan.command, plan.args, {
      ...spawnOptions,
      env: plan.env ?? spawnOptions.env,
      stdio: ["ignore", "pipe", "pipe"]
    });
    let stdout = "";
    let stderr = "";
    let settled = false;
    let drainTimer;
    let timeoutTimer;
    let exitCode = null;
    let exited = false;
    let timedOut = false;
    const settle = (code) => {
      if (settled) return;
      settled = true;
      if (timeoutTimer) clearTimeout(timeoutTimer);
      if (drainTimer) clearTimeout(drainTimer);
      child.stdout?.destroy();
      child.stderr?.destroy();
      child.unref();
      signal?.removeEventListener("abort", onAbort);
      if (timedOut) {
        reject(new ChildTimeoutError(timeoutMs ?? 0));
        return;
      }
      resolve11({ code: code ?? 0, stdout, stderr });
    };
    const restartDrain = () => {
      if (!exited || settled) return;
      if (drainTimer) clearTimeout(drainTimer);
      drainTimer = setTimeout(() => settle(exitCode), DRAIN_GRACE_MS);
    };
    child.stdout?.on("data", (chunk) => {
      stdout += typeof chunk === "string" ? chunk : chunk.toString("utf8");
      restartDrain();
    });
    child.stderr?.on("data", (chunk) => {
      stderr += typeof chunk === "string" ? chunk : chunk.toString("utf8");
      restartDrain();
    });
    child.on("error", (error) => {
      if (settled) return;
      settled = true;
      if (timeoutTimer) clearTimeout(timeoutTimer);
      if (drainTimer) clearTimeout(drainTimer);
      signal?.removeEventListener("abort", onAbort);
      reject(error);
    });
    child.on("exit", (code) => {
      exitCode = code;
      exited = true;
      restartDrain();
    });
    child.on("close", (code) => settle(code));
    if (timeoutMs !== void 0) {
      timeoutTimer = setTimeout(() => {
        timedOut = true;
        child.kill("SIGTERM");
        settle(null);
      }, timeoutMs);
    }
    const onAbort = () => child.kill();
    if (signal) {
      if (signal.aborted) onAbort();
      else signal.addEventListener("abort", onAbort, { once: true });
    }
  });
}

// src/cli/workspace.ts
var WORKSPACE_DIRNAME = ".pptwise";
var WORKSPACE_IGNORE_ENTRY = `${WORKSPACE_DIRNAME}/`;
var RENDERED_SVG_PATTERN = /^\d{3}-[a-z-]+\.svg$/;
var RESERVED_SLUGS = /* @__PURE__ */ new Set(["previews", "theme-try"]);
function deckSlug(target, isDir, anchor) {
  const withoutExt = (p) => isDir ? p : p.slice(0, p.length - extname3(p).length);
  const name = withoutExt(basename4(target));
  let key = name;
  let hashed;
  if (anchor !== void 0 && isAbsolute3(target)) {
    const rel = relative2(resolve4(anchor), withoutExt(resolve4(target)));
    if (rel === "") key = name;
    else if (rel.startsWith("..") || isAbsolute3(rel)) hashed = withoutExt(resolve4(target));
    else key = rel;
  }
  const words = key.split(/[\\/]+/u).join("-");
  if (hashed === void 0 && /[^A-Za-z0-9 ._-]/u.test(words.replace(/-/gu, ""))) hashed = key;
  const base = slugify(hashed === void 0 ? words : name, "deck");
  const hashedSlug = hashed === void 0 ? base : `${base}-${createHash("sha1").update(hashed.split(sep).join("/")).digest("hex").slice(0, 6)}`;
  const slug = anchor !== void 0 && isAbsolute3(target) && RESERVED_SLUGS.has(hashedSlug) ? `${hashedSlug}-deck` : hashedSlug;
  assertSafeFileSegment(slug, "deck slug");
  return slug;
}
function resolveWorkspaceRoot(opts) {
  const anchor = opts.projectConfigPath ? dirname3(resolve4(opts.projectConfigPath)) : resolve4(opts.cwd);
  return { anchor, root: join7(anchor, WORKSPACE_DIRNAME) };
}
function resolveWorkspaceLocation(opts) {
  const { anchor, root } = resolveWorkspaceRoot(opts);
  const slug = deckSlug(opts.target, opts.isDir, anchor);
  return { anchor, root, dir: join7(root, slug), slug, name: deckSlug(opts.target, opts.isDir) };
}
var UNSAFE_NAME_CHARS = '<>:"/\\|?*';
function finalPptxName(filename, fallback) {
  const raw = typeof filename === "string" ? filename.trim().replace(/\.pptx$/iu, "") : "";
  const safe = Array.from(raw, (ch) => ch.charCodeAt(0) < 32 || UNSAFE_NAME_CHARS.includes(ch) ? "-" : ch).join("").replace(/-{2,}/gu, "-").replace(/^[.\s-]+|[.\s]+$/gu, "");
  const name = safe === "" ? fallback : safe;
  assertSafeFileSegment(name, "deck filename");
  return `${name}.pptx`;
}
async function removeFinalPptx(dir) {
  let entries;
  try {
    entries = await readdir2(dir);
  } catch {
    return;
  }
  await Promise.all(entries.filter((name) => /\.pptx$/iu.test(name)).map((name) => unlink(join7(dir, name))));
}
var runGitDefault = async (args, cwd) => {
  try {
    const { code, stdout } = await runChild("git", args, { cwd });
    return { code, stdout };
  } catch (error) {
    const code = error.code;
    if (typeof code !== "number") return null;
    throw error;
  }
};
async function gitIgnoreStatus(dir, entry, runGit = runGitDefault) {
  const check = await runGit(["check-ignore", "-q", "--", entry], dir);
  if (check === null) return "not-a-repo";
  if (check.code === 0) return "ignored";
  if (check.code === 1) return "not-ignored";
  return "not-a-repo";
}
async function inspectWorkspace(opts) {
  const { anchor, root } = resolveWorkspaceRoot(opts);
  if (await isSelfIgnored(root)) return { anchor, root, ignore: "ignored" };
  const ignore = await gitIgnoreStatus(anchor, WORKSPACE_IGNORE_ENTRY, opts.runGit);
  return { anchor, root, ignore };
}
async function ensureGitIgnored(dir, entry, runGit = runGitDefault) {
  const status = await gitIgnoreStatus(dir, entry, runGit);
  if (status === "ignored") return { kind: "already-ignored" };
  if (status === "not-a-repo") return { kind: "no-repo" };
  const common = await runGit(["rev-parse", "--git-common-dir"], dir);
  if (common === null || common.code !== 0 || common.stdout.trim() === "") return { kind: "no-repo" };
  const excludePath = join7(resolve4(dir, common.stdout.trim()), "info", "exclude");
  try {
    await mkdir5(dirname3(excludePath), { recursive: true });
    let existing = "";
    try {
      existing = await readFile5(excludePath, "utf8");
    } catch {
      existing = "";
    }
    const lead = existing === "" || existing.endsWith("\n") ? "" : "\n";
    await appendFile(excludePath, `${lead}${entry}
`);
    return { kind: "appended", path: excludePath };
  } catch (e) {
    return { kind: "failed", path: excludePath, reason: e.message };
  }
}
async function exists(path2) {
  try {
    await stat2(path2);
    return true;
  } catch {
    return false;
  }
}
var SELF_IGNORE_FILENAME = ".gitignore";
var SELF_IGNORE_RULES = "*\n";
async function writeSelfIgnore(root) {
  try {
    await writeFile6(join7(root, SELF_IGNORE_FILENAME), SELF_IGNORE_RULES, { flag: "wx" });
  } catch (e) {
    if (e.code !== "EEXIST") throw e;
  }
}
async function isSelfIgnored(root) {
  try {
    const text = await readFile5(join7(root, SELF_IGNORE_FILENAME), "utf8");
    return text.split(/\r?\n/u).some((line) => line.trim() === "*");
  } catch {
    return false;
  }
}
async function prepareWorkspaceDir(location, opts = {}) {
  const rootExisted = await exists(location.root);
  try {
    await mkdir5(location.dir, { recursive: true });
  } catch (e) {
    throw new PptwiseError(
      `cannot create the output directory ${location.dir}: ${e.message}
  pass -o <path> to write somewhere writable, or run from a writable project`
    );
  }
  if (rootExisted || opts.gitIgnore === false) return [];
  const ignoreEntry = WORKSPACE_IGNORE_ENTRY;
  const outcome = await ensureGitIgnored(location.anchor, ignoreEntry, opts.runGit);
  const selfIgnore = join7(location.root, SELF_IGNORE_FILENAME);
  let selfIgnored = true;
  const notes = [];
  try {
    await writeSelfIgnore(location.root);
  } catch (e) {
    selfIgnored = false;
    notes.push(`note: could not write ${selfIgnore} (${e.message})`);
  }
  if (outcome.kind === "appended") {
    notes.push(`note: added ${ignoreEntry} to ${outcome.path} \u2014 a local ignore, your shared .gitignore is untouched`);
  } else if (outcome.kind === "failed") {
    notes.push(
      selfIgnored ? `note: could not write ${outcome.path} (${outcome.reason}). ${selfIgnore} still keeps ${ignoreEntry} out of git` : `note: could not write ${outcome.path} (${outcome.reason}) \u2014 add ${ignoreEntry} to your ignore rules yourself`
    );
  }
  return notes;
}
async function pruneRenderedSvgs(dir) {
  let entries;
  try {
    entries = await readdir2(dir);
  } catch {
    return 0;
  }
  const stale = entries.filter((name) => RENDERED_SVG_PATTERN.test(name));
  await Promise.all(stale.map((name) => unlink(join7(dir, name))));
  return stale.length;
}
var WORKSPACE_IMAGE_EXTS = /* @__PURE__ */ new Set([".png", ".jpg", ".jpeg", ".gif", ".webp"]);
async function scanWorkspaceAssets(assetsDir) {
  let names;
  try {
    names = (await readdir2(assetsDir, { withFileTypes: true })).filter((entry) => entry.isFile() && !entry.name.startsWith(".")).map((entry) => entry.name);
  } catch (e) {
    if (e.code === "ENOENT") return {};
    throw new PptwiseError(`cannot read workspace assets directory ${assetsDir}: ${e.message}`);
  }
  const images2 = {};
  const sourceFile2 = /* @__PURE__ */ new Map();
  for (const name of names) {
    const ext = extname3(name).toLowerCase();
    if (ext === ".json" || !WORKSPACE_IMAGE_EXTS.has(ext)) continue;
    const id = basename4(name, extname3(name));
    const previous = sourceFile2.get(id);
    if (previous !== void 0) {
      throw new PptwiseError(
        `workspace ${ASSETS_DIRNAME}/${previous} and ${ASSETS_DIRNAME}/${name} both register image id "${id}" \u2014 rename one of the files`
      );
    }
    sourceFile2.set(id, name);
    images2[id] = { src: join7(assetsDir, name) };
  }
  return images2;
}

// src/cli/theme-resolve.ts
import { dirname as dirname4, join as join9, resolve as resolve5 } from "path";

// src/cli/packs/store.ts
import { readdir as readdir3, readFile as readFile6 } from "fs/promises";
import { join as join8 } from "path";

// src/cli/packs/manifest.ts
import { z as z3 } from "zod";
var PACK_MANIFEST_FILENAME = "pack.json";
var PACK_ID_PATTERN = /^[a-z0-9][a-z0-9-]*$/;
var PACK_VERSION_PATTERN = /^[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*$/;
var PackManifestSchema = z3.object({
  pack: z3.literal(1),
  id: z3.string().regex(PACK_ID_PATTERN),
  version: z3.string().regex(PACK_VERSION_PATTERN),
  title: z3.string().min(1),
  engine: z3.string().min(1),
  themes: z3.array(z3.string().min(1))
});
function parsePackManifest(raw, source) {
  const result = PackManifestSchema.safeParse(raw);
  if (!result.success) {
    const detail = result.error.issues.map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`).join(". ");
    throw new PptwiseError(`invalid ${source}: ${detail}`);
  }
  return result.data;
}
function unsafePackPathReason(name) {
  if (name.length === 0) return "is empty";
  if (name.includes("\0")) return "contains a NUL byte";
  if (name.includes("\\")) return "contains a backslash";
  if (name.startsWith("/") || /^[A-Za-z]:/.test(name)) return "is absolute, and only relative paths are allowed";
  if (name.split("/").includes("..")) return "climbs out of the pack with ..";
  return void 0;
}

// src/cli/packs/store.ts
var PACKS_DIRNAME = "packs";
function packsRoot() {
  return join8(pptwiseHome(), PACKS_DIRNAME);
}
function damagedPackError(dir, detail) {
  return new PptwiseError(
    `installed pack ${dir} cannot be read: ${detail}. Run \`pptwise packs sync\` to reinstall it, or remove the directory.`
  );
}
async function readJson(path2, dir) {
  let text;
  try {
    text = await readFile6(path2, "utf8");
  } catch (e) {
    const code = e.code;
    throw damagedPackError(dir, code === "ENOENT" ? `${path2} is missing` : `${path2}: ${e.message}`);
  }
  try {
    return JSON.parse(text);
  } catch {
    throw damagedPackError(dir, `${path2} is not valid JSON`);
  }
}
async function readInstalledPack(dir, id) {
  const manifestPath = join8(dir, PACK_MANIFEST_FILENAME);
  const raw = await readJson(manifestPath, dir);
  let manifest;
  try {
    manifest = parsePackManifest(raw, manifestPath);
  } catch (e) {
    throw damagedPackError(dir, e.message);
  }
  if (manifest.id !== id) throw damagedPackError(dir, `its pack.json names pack "${manifest.id}", not "${id}"`);
  const themes = [];
  for (const rel of manifest.themes) {
    const unsafe = unsafePackPathReason(rel);
    if (unsafe !== void 0) throw damagedPackError(dir, `theme path "${rel}" ${unsafe}`);
    const path2 = join8(dir, ...rel.split("/"));
    const raw2 = await readJson(path2, dir);
    const themeId = typeof raw2 === "object" && raw2 !== null ? raw2.id : void 0;
    if (typeof themeId !== "string") throw damagedPackError(dir, `${path2} has no theme id`);
    themes.push({ id: themeId, path: path2 });
  }
  return { id, version: manifest.version, title: manifest.title, engine: manifest.engine, dir, themes };
}
async function installedPackIds(root = packsRoot()) {
  let entries;
  try {
    entries = await readdir3(root, { withFileTypes: true });
  } catch (e) {
    if (e.code === "ENOENT") return [];
    throw e;
  }
  return entries.filter((entry) => entry.isDirectory() && !entry.name.startsWith(".")).map((entry) => entry.name).sort();
}
async function listInstalledPacks(root = packsRoot(), opts = {}) {
  const out = [];
  for (const id of await installedPackIds(root)) {
    if (id === opts.except) continue;
    out.push(await readInstalledPack(join8(root, id), id));
  }
  return out;
}

// src/cli/theme-resolve.ts
var WORKSPACE_THEMES_DIRNAME = "themes";
function sortKeysDeep(value) {
  if (Array.isArray(value)) return value.map(sortKeysDeep);
  if (value !== null && typeof value === "object") {
    const sorted = {};
    for (const key of Object.keys(value).sort()) {
      sorted[key] = sortKeysDeep(value[key]);
    }
    return sorted;
  }
  return value;
}
function menusEqual(a, b) {
  return JSON.stringify(sortKeysDeep(a)) === JSON.stringify(sortKeysDeep(b));
}
function assertThemeId(id) {
  if (!THEME_ID_PATTERN.test(id)) {
    throw new PptwiseError(`invalid theme id "${id}". ${THEME_ID_CONSTRAINT}`);
  }
  assertNotRetiredThemeId(id);
}
function lookupThemeName(name) {
  return foldedThemeTarget(name) ?? name;
}
async function readThemeFile(path2) {
  const raw = await loadIrFile(path2, "theme");
  return parseBrandThemeFile(raw, path2);
}
function isCanonicalThemeId(name) {
  return CANONICAL_THEME_IDS.includes(name);
}
async function tryParseThemeFile(path2) {
  const raw = await loadIrFile(path2, "theme");
  const parsed = ThemeFileSchema.safeParse(raw);
  return parsed.success ? parsed.data : void 0;
}
async function acceptThemeFile(path2, file) {
  const definition = compileThemeDefinition(file);
  return { kind: "file", id: file.id, path: path2, file, definition };
}
async function acceptIfNameMatches(path2, name, file) {
  if (file.id !== name) return void 0;
  return acceptThemeFile(path2, file);
}
function deckThemeCandidates(deckDir, name) {
  return [
    { path: join9(deckDir, THEME_FILENAME), loose: false, deck: true, anchor: deckDir },
    { path: join9(deckDir, `${name}.theme.json`), loose: false, deck: true, anchor: deckDir },
    { path: join9(deckDir, `${name}.json`), loose: true, deck: true, anchor: deckDir }
  ];
}
function workspaceThemeCandidates(startDir, name) {
  const out = [];
  let dir = resolve5(startDir);
  for (; ; ) {
    const themesDir = join9(dir, WORKSPACE_THEMES_DIRNAME);
    out.push(
      { path: join9(themesDir, `${name}.theme.json`), loose: false, deck: false, anchor: dir },
      { path: join9(themesDir, `${name}.json`), loose: true, deck: false, anchor: dir },
      { path: join9(themesDir, name, THEME_FILENAME), loose: false, deck: false, anchor: dir }
    );
    const parent = dirname4(dir);
    if (parent === dir) return out;
    dir = parent;
  }
}
function themeCandidates(name, opts) {
  const deck = opts.deckDir !== void 0 ? deckThemeCandidates(opts.deckDir, name) : [];
  return [...deck, ...workspaceThemeCandidates(opts.startDir, name)];
}
async function resolveThemeFileFrom(candidates, name) {
  for (const candidate of candidates) {
    if (!await pathExists(candidate.path)) continue;
    const file = candidate.loose ? await tryParseThemeFile(candidate.path) : await readThemeFile(candidate.path);
    if (file === void 0) continue;
    const hit = await acceptIfNameMatches(candidate.path, name, file);
    if (hit !== void 0) return hit;
  }
  return void 0;
}
async function resolvePackTheme(name) {
  const packs2 = await listInstalledPacks();
  const hits = packs2.flatMap((pack) => pack.themes.filter((theme2) => theme2.id === name).map((theme2) => ({ pack, theme: theme2 })));
  if (hits.length > 1) {
    const where2 = hits.map(({ pack }) => pack.dir).join(" and ");
    throw new PptwiseError(`theme "${name}" is shipped by more than one installed pack (${where2}). Remove one of them.`);
  }
  const found = hits[0];
  if (found === void 0) return { hit: void 0, searched: packs2.map((pack) => pack.dir) };
  let file;
  try {
    file = await readThemeFile(found.theme.path);
  } catch (e) {
    throw damagedPackError(found.pack.dir, e instanceof Error ? e.message : String(e));
  }
  if (file.id !== name) {
    throw new PptwiseError(`installed pack theme ${found.theme.path} no longer has id "${name}". Run \`pptwise packs sync\` to reinstall its pack.`);
  }
  const accepted = await acceptThemeFile(found.theme.path, file);
  return { hit: { ...accepted, pack: { id: found.pack.id, version: found.pack.version } }, searched: [] };
}
async function resolveThemeByName(requested, opts) {
  const name = lookupThemeName(requested);
  assertThemeId(name);
  const fileHit = await resolveThemeFileFrom(themeCandidates(name, opts), name);
  if (fileHit !== void 0) return fileHit;
  if (isCanonicalThemeId(name)) return { kind: "builtin", id: name, definition: THEME_DEFINITIONS[name] };
  const packs2 = await resolvePackTheme(name);
  if (packs2.hit !== void 0) return packs2.hit;
  const places = [
    opts.deckDir !== void 0 ? `deck directory ${opts.deckDir}` : void 0,
    `workspace ${WORKSPACE_THEMES_DIRNAME}/ walking up from ${resolve5(opts.startDir)}`,
    packs2.searched.length > 0 ? `installed packs (${packs2.searched.join(", ")})` : `installed packs in ${packsRoot()} (none installed)`,
    "built-in presets"
  ].filter((place) => place !== void 0);
  throw new PptwiseError(`unknown theme "${name}". Searched ${places.join(", ")}.`);
}
function assertThemeRebind(bound, resolved) {
  if (bound === void 0) return;
  if (menusEqual(bound.menu, resolved.definition.menu)) return;
  throw new PptwiseError(
    `cannot rebind theme "${bound.id}" to "${resolved.id}": menus differ, and this deck froze "${bound.id}" in its own theme.json. To switch, delete that theme.json, or replace it with "${resolved.id}"'s theme file. The spec and page files stay as they are. A same-menu color fork needs neither.`
  );
}
async function resolveThemeSelection(name, opts) {
  if (name === void 0 || name.length === 0) return void 0;
  return resolveThemeByName(name, opts);
}
function themeNameFromUnknown(raw) {
  if (typeof raw !== "object" || raw === null) return void 0;
  const theme2 = raw.theme;
  return typeof theme2 === "string" ? theme2 : void 0;
}

// src/cli/theme-inputs.ts
import { createHash as createHash2 } from "crypto";
import { dirname as dirname5, join as join10, resolve as resolve6 } from "path";
async function collectThemeInputs(target) {
  const deckDir = target.isDir ? target.resolvedTarget : dirname5(target.resolvedTarget);
  let source;
  try {
    source = await readSource(target);
  } catch (e) {
    return withKey({ source: void 0, bound: { error: e }, resolved: void 0, localTheme: void 0 });
  }
  const name = source.kind === "spec" ? themeNameFromUnknown(source.parsed) : irThemeIdOf(source.parsed);
  return resolveThemeInputs({ name }, { startDir: target.startDir, deckDir }, source);
}
function unreadThemeInputs(error) {
  return withKey({ source: void 0, bound: { error }, resolved: void 0, localTheme: void 0 });
}
async function resolveThemeInputs(bound, opts, source) {
  if ("error" in bound || bound.name === void 0) {
    return withKey({ source, bound, resolved: void 0, localTheme: void 0 });
  }
  let resolved;
  try {
    resolved = await resolveThemeByName(bound.name, opts);
  } catch (e) {
    return withKey({ source, bound, resolved: { error: e }, localTheme: void 0 });
  }
  return withKey({ source, bound, resolved, localTheme: await readLocalTheme(opts.deckDir, resolved) });
}
function sourceFromInputs(inputs) {
  if ("error" in inputs.bound) throw inputs.bound.error;
  if (inputs.source === void 0) throw new Error("theme inputs were collected without their source");
  return inputs.source;
}
function themeFromInputs(inputs) {
  if ("error" in inputs.bound) throw inputs.bound.error;
  if (inputs.resolved === void 0) return void 0;
  if ("error" in inputs.resolved) throw inputs.resolved.error;
  return inputs.resolved;
}
function boundThemeName(inputs) {
  return "name" in inputs.bound ? inputs.bound.name : void 0;
}
function guardThemeRebind(local, resolved) {
  if (local !== void 0 && "error" in local) throw local.error;
  assertThemeRebind(local?.file, resolved);
}
async function readSource(target) {
  if (target.isDir) {
    return { kind: "spec", path: join10(target.resolvedTarget, SPEC_FILENAME), parsed: await readSpecFile(target.resolvedTarget) };
  }
  return { kind: "ir", path: target.resolvedTarget, parsed: await loadIrFile(target.resolvedTarget) };
}
function irThemeIdOf(raw) {
  if (typeof raw !== "object" || raw === null) return void 0;
  const theme2 = raw.theme;
  if (typeof theme2 !== "object" || theme2 === null) return void 0;
  const id = theme2.id;
  return typeof id === "string" ? id : void 0;
}
async function readLocalTheme(deckDir, resolved) {
  const path2 = resolve6(join10(deckDir, THEME_FILENAME));
  if (resolved.kind === "file" && resolve6(resolved.path) === path2) return void 0;
  try {
    if (!await pathExists(path2)) return void 0;
    return { path: path2, file: await readThemeFile(path2) };
  } catch (e) {
    return { path: path2, error: e };
  }
}
function withKey(inputs) {
  return { ...inputs, key: themeInputsKey(inputs) };
}
function messageOf(e) {
  return e instanceof Error ? e.message : String(e);
}
function contentDigest(parsed) {
  return createHash2("sha256").update(JSON.stringify(sortKeysDeep(parsed)) ?? "").digest("hex");
}
function themeInputsKey(inputs) {
  const { source, bound, resolved, localTheme } = inputs;
  if ("error" in bound) return `source:error:${messageOf(bound.error)}`;
  const parts = [];
  if (source !== void 0) parts.push(`source:${source.kind}:${contentDigest(source.parsed)}`);
  if (bound.name === void 0) {
    parts.push("bound:none");
    return parts.join("|");
  }
  parts.push(`bound:${bound.name}`);
  if (resolved === void 0) return parts.join("|");
  if ("error" in resolved) {
    parts.push(`theme:error:${messageOf(resolved.error)}`);
    return parts.join("|");
  }
  parts.push(resolved.kind === "builtin" ? `theme:builtin:${resolved.id}` : `theme:file:${contentDigest(resolved.file)}`);
  if (localTheme === void 0) parts.push("local:none");
  else if ("error" in localTheme) parts.push(`local:error:${messageOf(localTheme.error)}`);
  else parts.push(`local:file:${contentDigest(localTheme.file)}`);
  return parts.join("|");
}

// src/cli/fixtures/theme-try-sample.ts
var THEME_TRY_SAMPLE_IR = {
  version: "5",
  filename: "northstar-review",
  theme: { id: "brief" },
  slides: [
    {
      type: "cover",
      heading: "Northstar Review",
      subheading: "Q3 operating report for the board"
    },
    {
      type: "chapter",
      heading: "The Quarter"
    },
    {
      type: "content",
      kind: "points",
      heading: "What we decided",
      components: [
        {
          type: "bullets",
          items: [
            "Hold hiring at 42",
            "Cut the analytics rebuild",
            "Share the support rotation"
          ]
        }
      ]
    },
    {
      type: "content",
      kind: "list",
      heading: "Open workstreams",
      components: [
        {
          type: "bullets",
          items: [
            "EU residency addendum",
            "Partner invite flow",
            "Invoice localization"
          ]
        }
      ]
    },
    {
      type: "content",
      kind: "comparison",
      heading: "Build vs buy",
      components: [
        {
          type: "comparison",
          columns: ["Build", "Buy"],
          rows: [
            { label: "Time to first report", cells: ["14 weeks", "3 weeks"] },
            { label: "Year-one cost", cells: ["$420k", "$180k"] },
            { label: "Lock-in", cells: ["None", "Vendor roadmap"] }
          ]
        }
      ]
    },
    {
      type: "content",
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
      type: "content",
      kind: "data",
      heading: "Pipeline by stage",
      components: [
        {
          type: "chart",
          chart_type: "bar",
          series: [
            {
              name: "Qualified",
              data: [
                { x: "Discover", y: 42 },
                { x: "Propose", y: 19 },
                { x: "Close", y: 11 }
              ]
            }
          ]
        }
      ]
    },
    {
      type: "content",
      kind: "statement",
      heading: "We will not add a fourth product line this year",
      components: [
        {
          type: "blockquote",
          text: "Three products is the house."
        }
      ]
    },
    {
      type: "content",
      kind: "fact",
      heading: "NPS",
      components: [
        {
          type: "kpi_cards",
          items: [{ value: "61", label: "trailing 90-day NPS", delta: "up" }]
        }
      ]
    },
    {
      type: "ending",
      heading: "See you Thursday"
    }
  ]
};

// src/cli/commands.ts
async function readConfigs(cwd) {
  const [project, user] = await Promise.allSettled([findConfig(cwd), findUserConfig()]);
  const failures = [project, user].filter((r) => r.status === "rejected");
  if (failures.length === 1) throw failures[0].reason;
  if (failures.length === 2) {
    const message = (e) => e instanceof Error ? e.message : String(e);
    throw new PptwiseError(failures.map((f) => message(f.reason)).join("\n"), { cause: failures[0].reason });
  }
  return [project.value, user.value];
}
async function applyDeckConfig(raw, themeInputs) {
  if (typeof raw !== "object" || raw === null) return void 0;
  const deck = raw;
  const irTheme = typeof deck.theme === "object" && deck.theme !== null ? deck.theme : {};
  const resolved = themeFromInputs(themeInputs);
  if (resolved === void 0) return void 0;
  guardThemeRebind(themeInputs.localTheme, resolved);
  deck.theme = {
    ...irTheme,
    id: boundThemeName(themeInputs) ?? resolved.id
  };
  return resolved;
}
function mergeWorkspaceImages(raw, extras) {
  if (typeof raw !== "object" || raw === null) return raw;
  const deck = raw;
  const existing = deck.assets?.images ?? {};
  return { ...deck, assets: { images: { ...extras, ...existing } } };
}
async function loadWorkspaceStock(cwd, projectHit, resolvedTarget, isDir) {
  const location = resolveWorkspaceLocation({
    cwd,
    projectConfigPath: projectHit?.path,
    target: resolvedTarget,
    isDir
  });
  const workspaceAssetsDir = join11(location.dir, ASSETS_DIRNAME);
  const images2 = await scanWorkspaceAssets(workspaceAssetsDir);
  return { workspaceAssetsDir, images: images2 };
}
async function locateDeckTarget(arg, cwd) {
  const target = await resolveDeckTarget(arg, cwd);
  if (await isDeckDirectory(target)) return { resolvedTarget: resolve7(target), isDir: true };
  return { resolvedTarget: resolve7(target), isDir: false };
}
async function locateDeck(arg, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  await readConfigs(cwd);
  return locateDeckTarget(arg, cwd);
}
async function collectDeckThemeInputs(arg, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  let location;
  try {
    location = await locateDeck(arg, { cwd });
  } catch (e) {
    return unreadThemeInputs(e);
  }
  return collectThemeInputs({ startDir: cwd, ...location });
}
async function readDeckTarget(location, themeInputs, cwd, projectHit, page) {
  const { resolvedTarget, isDir } = location;
  const source = sourceFromInputs(themeInputs);
  if (isDir) {
    const theme2 = themeFromInputs(themeInputs)?.definition;
    const { ir, spec: spec2, deckDir } = await readDeckDir(resolvedTarget, { theme: theme2, spec: source, ...page !== void 0 ? { page } : {} });
    const stock2 = await loadWorkspaceStock(cwd, projectHit, deckDir, true);
    return {
      raw: mergeWorkspaceImages(ir, stock2.images),
      baseDir: deckDir,
      isDir: true,
      resolvedTarget: deckDir,
      workspaceAssetsDir: stock2.workspaceAssetsDir,
      missingAssetPath: assetPathIn(join11(deckDir, ASSETS_DIRNAME), cwd),
      themeInputs,
      spec: spec2
    };
  }
  const stock = await loadWorkspaceStock(cwd, projectHit, resolvedTarget, false);
  return {
    raw: mergeWorkspaceImages(source.parsed, stock.images),
    baseDir: dirname6(resolvedTarget),
    isDir: false,
    resolvedTarget,
    workspaceAssetsDir: stock.workspaceAssetsDir,
    missingAssetPath: assetPathIn(stock.workspaceAssetsDir, cwd),
    themeInputs
  };
}
function deckFilename(loaded) {
  if (loaded.isDir) return loaded.spec?.filename;
  const raw = loaded.raw;
  return typeof raw === "object" && raw !== null ? raw.filename : void 0;
}
function assetPathIn(dir, cwd) {
  return (assetId) => {
    const path2 = join11(dir, assetId);
    const rel = relative3(resolve7(cwd), path2);
    return rel !== "" && !rel.startsWith("..") && !isAbsolute4(rel) ? rel : path2;
  };
}
async function loadDeckTarget(arg, cwd, projectHit) {
  const location = await locateDeckTarget(arg, cwd);
  const themeInputs = await collectThemeInputs({ startDir: cwd, ...location });
  return readDeckTarget(location, themeInputs, cwd, projectHit);
}
async function loadValidatedDeckIr(target, cwd) {
  const [projectHit] = await readConfigs(cwd);
  const { raw, baseDir, workspaceAssetsDir, themeInputs, missingAssetPath } = await loadDeckTarget(target, cwd, projectHit);
  const theme2 = (await applyDeckConfig(raw, themeInputs))?.definition;
  const v2 = validateIr(raw, { theme: theme2, missingAssetPath });
  if (!v2.ok) {
    throw new PptwiseError(
      `invalid IR (${v2.errors.length} issue${v2.errors.length === 1 ? "" : "s"}):
${formatIssues(v2.errors)}`
    );
  }
  await resolveLocalAssets(v2.ir, baseDir, workspaceAssetsDir);
  return { ir: v2.ir, theme: theme2 };
}
async function runRender(irPath, opts) {
  const cwd = opts.cwd ?? process.cwd();
  const [projectHit] = await readConfigs(cwd);
  const loaded = await loadDeckTarget(irPath, cwd, projectHit);
  const { raw, baseDir, isDir, resolvedTarget, workspaceAssetsDir, themeInputs, missingAssetPath } = loaded;
  const theme2 = (await applyDeckConfig(raw, themeInputs))?.definition;
  const v2 = validateIr(raw, { theme: theme2, missingAssetPath, allowDroppedContent: opts.allowDroppedContent });
  if (!v2.ok) throw new PptwiseError(`invalid IR:
${formatIssues(v2.errors)}`);
  await resolveLocalAssets(v2.ir, baseDir, workspaceAssetsDir);
  const bytes = await generatePptx(v2.ir, {
    draft: opts.draft,
    allowDroppedContent: opts.allowDroppedContent,
    theme: theme2
  });
  const extraNotes = [];
  let output;
  if (opts.output !== void 0) {
    output = resolve7(cwd, opts.output);
    await mkdir6(dirname6(output), { recursive: true });
  } else {
    const location = resolveWorkspaceLocation({
      cwd,
      projectConfigPath: projectHit?.path,
      target: resolvedTarget,
      isDir
    });
    extraNotes.push(...await prepareWorkspaceDir(location, { gitIgnore: opts.gitIgnore, runGit: opts.runGit }));
    output = join11(location.dir, finalPptxName(deckFilename(loaded), location.name));
  }
  await writeFile7(output, bytes);
  const ok = `wrote ${output} (${v2.ir.slides.length} slides, ${bytes.length} bytes)`;
  const notes = [...extraNotes, warningsNote(v2.warnings), normalizedNote(v2.normalized)].filter(
    (n) => n !== void 0
  );
  return notes.length > 0 ? `${ok}
${notes.join("\n")}` : ok;
}
function normalizedNote(normalized) {
  if (!normalized || normalized.length === 0) return void 0;
  const n = normalized.length;
  return `note: ${n} field alias${n === 1 ? "" : "es"} normalized
${normalized.map((line) => `  ${line}`).join("\n")}`;
}
function warningsNote(warnings) {
  if (!warnings || warnings.length === 0) return void 0;
  return formatWarnings(warnings);
}
function placeholderNote(ir) {
  const placeholders = ir.slides.map((slide, i) => ({ slide, page: i + 1 })).filter(({ slide }) => slide.placeholder);
  if (placeholders.length === 0) return void 0;
  const refs = placeholders.map(({ slide, page }) => slide.id ? `${slide.id} (page ${page})` : `page ${page}`).join(", ");
  return `note: ${placeholders.length} unfilled placeholder page${placeholders.length === 1 ? "" : "s"}: ${refs}`;
}
async function runValidate(irPath, cwd = process.cwd()) {
  const [projectHit] = await readConfigs(cwd);
  const { raw, baseDir, isDir, workspaceAssetsDir, themeInputs, missingAssetPath } = await loadDeckTarget(irPath, cwd, projectHit);
  const theme2 = (await applyDeckConfig(raw, themeInputs))?.definition;
  const v2 = validateIr(raw, { theme: theme2, missingAssetPath });
  if (!v2.ok)
    throw new PptwiseError(
      `invalid IR (${v2.errors.length} issue${v2.errors.length === 1 ? "" : "s"}):
${formatIssues(v2.errors)}`
    );
  await resolveLocalAssets(v2.ir, baseDir, workspaceAssetsDir);
  const ok = `OK \u2014 ${v2.ir.slides.length} slides, theme "${v2.ir.theme.id}"`;
  const notes = [];
  const warnNote = warningsNote(v2.warnings);
  if (warnNote) notes.push(warnNote);
  const aliasNote = normalizedNote(v2.normalized);
  if (aliasNote) notes.push(aliasNote);
  if (isDir) {
    const note = placeholderNote(v2.ir);
    if (note) notes.push(note);
  }
  return notes.length > 0 ? `${ok}
${notes.join("\n")}` : ok;
}
function formatAuditFinding(f) {
  const idSuffix = f.slideId !== void 0 ? ` (${f.slideId})` : "";
  return `page ${f.page}${idSuffix}: [${f.code}] ${f.message}`;
}
function formatAuditReport(report, ir) {
  const lines = report.findings.map(formatAuditFinding);
  lines.push(
    `audited ${report.pagesAudited} page${report.pagesAudited === 1 ? "" : "s"}, ${report.pagesSkipped} skipped, ${report.findings.length} finding${report.findings.length === 1 ? "" : "s"}`
  );
  if (report.checks.pixels === "completed") {
    lines.push("pixel-contrast check: completed");
  }
  const note = placeholderNote(ir);
  if (note) lines.push(note);
  return lines.join("\n");
}
async function runAudit(target, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  const [projectHit] = await readConfigs(cwd);
  const { raw, baseDir, workspaceAssetsDir, themeInputs, missingAssetPath } = await loadDeckTarget(target, cwd, projectHit);
  const theme2 = (await applyDeckConfig(raw, themeInputs))?.definition;
  const v2 = validateIr(raw, { theme: theme2, missingAssetPath });
  if (!v2.ok) {
    throw new PptwiseError(
      `invalid IR (${v2.errors.length} issue${v2.errors.length === 1 ? "" : "s"}):
${formatIssues(v2.errors)}`
    );
  }
  await resolveLocalAssets(v2.ir, baseDir, workspaceAssetsDir);
  const report = opts.pixels ? await auditDeck(v2.ir, { pixels: true, theme: theme2 }) : auditDeck(v2.ir, { theme: theme2 });
  const hasFindings = report.findings.length > 0;
  const output = opts.json ? JSON.stringify(report, null, 2) : formatAuditReport(report, v2.ir);
  return { output, hasFindings };
}
async function runInspect(target, opts) {
  if (opts.page === void 0 || opts.page.length === 0) {
    throw new PptwiseError("pass --page <id>: the id of one page in deck.spec.json");
  }
  if (opts.component !== void 0 && opts.fit) throw new PptwiseError("pass --component or --fit, not both");
  const cwd = opts.cwd ?? process.cwd();
  const [projectHit] = await readConfigs(cwd);
  const location = await locateDeckTarget(target, cwd);
  if (!location.isDir) {
    throw new PptwiseError(`pptwise inspect reads a deck project directory (deck.spec.json plus pages/), and ${target} is not one`);
  }
  assertSafeFileSegment(opts.page, "page id");
  const themeInputs = await collectThemeInputs({ startDir: cwd, ...location });
  const loaded = await readDeckTarget(location, themeInputs, cwd, projectHit, opts.page);
  const theme2 = (await applyDeckConfig(loaded.raw, themeInputs))?.definition;
  if (theme2 === void 0) throw new PptwiseError(`${SPEC_FILENAME} binds no theme`);
  const ir = loaded.raw;
  const validation = validateIr(ir, { theme: theme2, missingAssetPath: loaded.missingAssetPath });
  const pageSpec = loaded.spec?.pages.find((page) => page.id === opts.page);
  const contractOpts = { theme: theme2, validation, ...pageSpec !== void 0 ? { pageSpec } : {} };
  if (opts.component !== void 0) {
    const expanded = pageComponentContract(ir, opts.page, opts.component, contractOpts);
    return { output: opts.json ? JSON.stringify(expanded) : formatPageComponentContract(expanded), failed: false };
  }
  const contract = pageContract(ir, opts.page, contractOpts);
  const file = `${PAGES_DIRNAME}/${opts.page}.json`;
  if (opts.fit) {
    let fit;
    if (!contract.page.filled) {
      fit = { checked: false, reason: "the page is not written yet" };
    } else if (!validation.ok) {
      fit = { checked: false, reason: "fix the page's validate errors first" };
    } else {
      await resolveLocalAssets(validation.ir, loaded.baseDir, loaded.workspaceAssetsDir);
      fit = { checked: true, ...pageFit(validation.ir, opts.page, { theme: theme2 }) };
    }
    const report = {
      page: { ...contract.page, file },
      errors: contract.errors,
      warnings: contract.warnings,
      fit
    };
    return {
      output: opts.json ? JSON.stringify(report) : formatPageFitReport(report, contract.theme),
      failed: contract.errors.length > 0 || fit.checked && !fit.fits
    };
  }
  if (contract.signature !== void 0 && contract.page.filled && validation.ok) {
    await resolveLocalAssets(validation.ir, loaded.baseDir, loaded.workspaceAssetsDir);
    const index = pageIndex(validation.ir, opts.page);
    const svg = renderSlideSvg(validation.ir, index, { theme: theme2 });
    contract.signature = { ...contract.signature, drawnBy: pageSignatureUse(validation.ir, validation.ir.slides[index], theme2, svg).drawnBy };
  }
  const output = opts.json ? JSON.stringify({ ...contract, page: { ...contract.page, file } }) : formatPageContract(contract, file);
  return { output, failed: contract.errors.length > 0 };
}
function formatAssetBriefItem(item) {
  const idSuffix = item.page.id !== void 0 ? `, ${item.page.id}` : "";
  const sharedSuffix = item.shared ? ` (shared by ${item.occurrenceCount} image slots, frame not attributable to one)` : "";
  const header = `page ${item.page.index + 1} (${item.page.type}${idSuffix}) \u2014 ${item.asset_id}${item.missing ? " (missing)" : ""}${item.rendered ? "" : " (not rendered under the selected layout)"}${sharedSuffix}`;
  const lines = [header];
  if (item.frame && item.suggested_pixels) {
    lines.push(
      `  frame: ${item.frame.w}x${item.frame.h} @ (${item.frame.x},${item.frame.y}), aspect ${item.frame.aspect}, ${item.fit.mode}`
    );
    lines.push(`  suggested pixels: ${item.suggested_pixels.w}x${item.suggested_pixels.h}`);
  }
  lines.push(`  fit: ${item.fit.note}`);
  lines.push(`  palette: primary ${item.palette.primary}, accent ${item.palette.accent} (${item.palette.hexes.join(", ")})`);
  lines.push(`  mood: ${item.mood.description}`);
  lines.push(`  prompt: ${item.suggested_prompt}`);
  return lines.join("\n");
}
function formatAssetBriefReport(brief) {
  if (brief.items.length === 0) return `no image components found for theme "${brief.theme}"`;
  const missingCount = brief.items.filter((i) => i.missing).length;
  const notRenderedCount = brief.items.filter((i) => !i.rendered).length;
  const lines = brief.items.map(formatAssetBriefItem);
  lines.push(
    `${brief.items.length} image slot${brief.items.length === 1 ? "" : "s"}, ${missingCount} to generate, ${notRenderedCount} not rendered under their selected layout`
  );
  return lines.join("\n\n");
}
async function runAssetBrief(target, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  const [projectHit] = await readConfigs(cwd);
  const { raw, baseDir, workspaceAssetsDir, themeInputs, missingAssetPath } = await loadDeckTarget(target, cwd, projectHit);
  const theme2 = (await applyDeckConfig(raw, themeInputs))?.definition;
  const v2 = validateIr(raw, { theme: theme2, missingAssetPath });
  if (!v2.ok) {
    throw new PptwiseError(
      `invalid IR (${v2.errors.length} issue${v2.errors.length === 1 ? "" : "s"}):
${formatIssues(v2.errors)}`
    );
  }
  await resolveLocalAssets(v2.ir, baseDir, workspaceAssetsDir);
  const brief = buildAssetBrief(v2.ir, { theme: theme2 });
  return opts.json ? JSON.stringify(brief, null, 2) : formatAssetBriefReport(brief);
}
async function runSpecValidate(specPath) {
  const raw = await loadIrFile(specPath, "spec");
  const specDir = dirname6(resolve7(specPath));
  const resolved = await resolveThemeSelection(themeNameFromUnknown(raw), { startDir: specDir, deckDir: specDir });
  const v2 = validateSpec(raw, { theme: resolved?.definition });
  if (!v2.ok) {
    throw new PptwiseError(formatInvalidSpecError(v2.errors));
  }
  const spec2 = v2.spec;
  const axes = resolveNarrative(spec2.narrative);
  const ok = `OK \u2014 ${spec2.pages.length} pages, narrative ${axes.strategy}/${axes.pacing}/${axes.audience}, theme "${resolveSpecThemeId(spec2)}"`;
  const lines = [ok];
  for (const w of v2.warnings ?? []) {
    lines.push(`warning: ${w.path ? `${w.path}: ` : ""}${w.message}`);
  }
  for (const landing of v2.landings ?? []) lines.push(`note: ${landing.path}: ${landing.message}`);
  const aliasNote = normalizedNote(v2.normalized);
  if (aliasNote) lines.push(aliasNote);
  return lines.join("\n");
}
async function runSpecValidateJson(specPath) {
  const raw = await loadIrFile(specPath, "spec");
  const specDir = dirname6(resolve7(specPath));
  const resolved = await resolveThemeSelection(themeNameFromUnknown(raw), { startDir: specDir, deckDir: specDir });
  const v2 = validateSpec(raw, { theme: resolved?.definition });
  const issue = (i) => ({ path: i.path, message: i.message, ...i.pageId ? { pageId: i.pageId } : {} });
  if (!v2.ok) {
    return { ok: false, output: JSON.stringify({ ok: false, errors: v2.errors.map(issue), warnings: (v2.warnings ?? []).map(issue) }, null, 2) };
  }
  const spec2 = v2.spec;
  const axes = resolveNarrative(spec2.narrative);
  const pages = spec2.pages.map((page, index) => ({
    page: index + 1,
    id: page.id,
    type: page.type,
    ...page.type === "content" ? { kind: page.kind } : {},
    heading: page.heading,
    ...page.summary !== void 0 ? { summary: page.summary } : {}
  }));
  const cover = spec2.pages.find((page) => page.type === "cover");
  const report = {
    ok: true,
    theme: resolveSpecThemeId(spec2),
    narrative: { strategy: axes.strategy, pacing: axes.pacing, audience: axes.audience },
    ...cover ? { title: cover.heading } : {},
    pageCount: pages.length,
    pages,
    warnings: (v2.warnings ?? []).map(issue),
    ...v2.landings && v2.landings.length > 0 ? { landings: v2.landings } : {},
    ...v2.normalized && v2.normalized.length > 0 ? { normalized: v2.normalized } : {}
  };
  return { ok: true, output: JSON.stringify(report, null, 2) };
}
async function schemaDeckDir(cwd, deck, themeName) {
  if (deck !== void 0) {
    const dir = resolve7(cwd, deck);
    if (!await isDeckDirectory(dir)) throw new PptwiseError(`--deck ${deck}: ${dir} is not a directory`);
    return dir;
  }
  if (await pathExists(join11(cwd, SPEC_FILENAME))) return cwd;
  for (const candidate of deckThemeCandidates(cwd, themeName)) {
    if (await pathExists(candidate.path)) return cwd;
  }
  return void 0;
}
async function runSchema(opts = {}) {
  const modes = [opts.spec ? "--spec" : void 0, opts.component !== void 0 ? "--component" : void 0, opts.kind !== void 0 ? "--kind" : void 0].filter((flag) => flag !== void 0);
  if (modes.length > 1) throw new PptwiseError(`pass one of --spec, --component, --kind (got ${modes.join(" and ")})`);
  if (opts.theme !== void 0 && opts.kind === void 0) throw new PptwiseError("--theme requires --kind");
  if (opts.deck !== void 0 && opts.theme === void 0) throw new PptwiseError("--deck requires --theme");
  let schema;
  if (opts.spec) {
    schema = specJsonSchema();
  } else if (opts.component !== void 0) {
    schema = componentJsonSchema(opts.component);
  } else if (opts.kind !== void 0) {
    const cwd = opts.cwd ?? process.cwd();
    let deckDir;
    if (opts.theme !== void 0 && opts.theme.length > 0) {
      const name = lookupThemeName(opts.theme);
      assertThemeId(name);
      deckDir = await schemaDeckDir(cwd, opts.deck, name);
    }
    const resolved = await resolveThemeSelection(opts.theme, { startDir: cwd, deckDir });
    schema = kindJsonSchema(opts.kind, {
      theme: resolved?.definition,
      extraThemes: resolved === void 0 ? await readablePackDefinitions() : void 0
    });
  } else {
    schema = irJsonSchema();
  }
  return opts.pretty ? JSON.stringify(schema, null, 2) : JSON.stringify(schema);
}
function runIcons(asJson) {
  return asJson ? JSON.stringify([...PPTX_ICON_NAMES], null, 2) : PPTX_ICON_NAMES.join("\n");
}
function menuFaces(menu) {
  const content = {};
  for (const kind of offeredContentKinds(menu)) content[kind] = menu.content[kind].face;
  return { cover: menu.cover.face, chapter: menu.chapter.face, ending: menu.ending.face, content };
}
async function readInstalledPackThemes() {
  const reads = [];
  for (const id of await installedPackIds()) {
    const dir = join11(packsRoot(), id);
    try {
      const pack = await readInstalledPack(dir, id);
      const themes = [];
      for (const theme2 of pack.themes) {
        let file;
        let definition;
        try {
          file = await readThemeFile(theme2.path);
          definition = compileThemeDefinition(file);
        } catch (e) {
          if (!(e instanceof PptwiseError)) throw e;
          throw damagedPackError(dir, e.message);
        }
        if (CANONICAL_THEME_IDS.includes(file.id)) {
          throw damagedPackError(dir, `it ships theme "${file.id}", which is a factory preset name`);
        }
        const renamed = RETIRED_THEME_IDS[file.id] ?? foldedThemeTarget(file.id);
        if (renamed !== void 0) {
          throw damagedPackError(dir, `it ships theme "${file.id}", a retired id (now "${renamed}")`);
        }
        themes.push({ file, definition });
      }
      reads.push({ ok: true, id, themes });
    } catch (e) {
      if (!(e instanceof PptwiseError)) throw e;
      reads.push({ ok: false, id, error: e.message });
    }
  }
  const owners = /* @__PURE__ */ new Map();
  for (const read of reads) {
    if (!read.ok) continue;
    for (const { file } of read.themes) owners.set(file.id, [...owners.get(file.id) ?? [], read.id]);
  }
  return reads.map((read) => {
    if (!read.ok) return read;
    const shared = read.themes.find(({ file }) => (owners.get(file.id) ?? []).length > 1);
    if (shared === void 0) return read;
    const where2 = owners.get(shared.file.id).map((owner) => join11(packsRoot(), owner)).join(" and ");
    const error = damagedPackError(
      join11(packsRoot(), read.id),
      `theme "${shared.file.id}" is shipped by more than one installed pack (${where2})`
    ).message;
    return { ok: false, id: read.id, error };
  });
}
async function readablePackDefinitions() {
  const definitions = [];
  for (const read of await readInstalledPackThemes()) {
    if (read.ok) definitions.push(...read.themes.map(({ definition }) => definition));
    else process.stderr.write(`schema --kind: left out ${read.error}
`);
  }
  return definitions;
}
function packThemeRows(read) {
  if (!read.ok) return [{ source: "pack", pack: read.id, error: read.error }];
  return read.themes.map(({ file, definition }) => ({
    id: file.id,
    label: file.label ?? file.id,
    colors: { ...file.style.colors },
    occasions: file.occasions ?? [],
    identity: file.identity ?? null,
    source: "pack",
    pack: read.id,
    menu: menuFaces(definition.menu)
  }));
}
async function runThemes(asJson) {
  const rows = listThemes().map((t) => {
    const rec = Object.hasOwn(THEME_OCCASIONS, t.id) ? THEME_OCCASIONS[t.id] : void 0;
    return {
      id: t.id,
      label: t.label,
      colors: t.colors,
      occasions: rec?.occasions ?? [],
      identity: rec?.identity ?? null,
      source: "builtin",
      menu: menuFaces(THEME_DEFINITIONS[t.id].menu)
    };
  });
  for (const read of await readInstalledPackThemes()) rows.push(...packThemeRows(read));
  if (asJson) return JSON.stringify(rows, null, 2);
  return rows.map((t) => {
    if ("error" in t) return `(pack ${t.pack}) ${t.error.replace(/\s*\n\s*/g, " ")}`;
    const line = `${t.id.padEnd(12)} ${t.label}`;
    return t.pack === void 0 ? line : `${line}  (pack ${t.pack})`;
  }).join("\n");
}
function layoutCapacity(slots) {
  let sum = 0;
  let any = false;
  for (const slot of slots) {
    if (slot.capacity !== void 0) {
      sum += slot.capacity;
      any = true;
    }
  }
  return any ? sum : void 0;
}
function listLayouts() {
  return Object.values(LAYOUT_REGISTRY).map((layout) => {
    const capacity = layoutCapacity(layout.slots);
    const row = {
      id: layout.id,
      slideTypes: layout.slideTypes,
      slots: layout.slots.map((slot) => {
        const compact = { name: slot.name, accepts: slot.accepts };
        if (slot.capacity !== void 0) compact.capacity = slot.capacity;
        return compact;
      })
    };
    if (capacity !== void 0) row.capacity = capacity;
    return row;
  });
}
function runLayouts(asJson) {
  const layouts = listLayouts();
  if (asJson) return JSON.stringify(layouts, null, 2);
  const rows = layouts.map((l) => ({
    id: l.id,
    types: l.slideTypes.join(","),
    cap: l.capacity !== void 0 ? String(l.capacity) : "-",
    slots: l.slots.map((s) => s.name).join(", ")
  }));
  const idWidth = Math.max(...rows.map((r) => r.id.length));
  const typesWidth = Math.max(...rows.map((r) => r.types.length));
  const capWidth = Math.max(...rows.map((r) => r.cap.length));
  return rows.map(
    (r) => `${r.id.padEnd(idWidth + 2)}${r.types.padEnd(typesWidth + 2)}${r.cap.padEnd(capWidth + 2)}${r.slots}`
  ).join("\n");
}
function defaultThemeIdFor(output) {
  return slugify(basename5(output).replace(/\.theme\.json$|\.json$/i, ""));
}
async function defaultThemeOutputPath(id, cwd) {
  assertThemeId(id);
  const project = await findConfig(cwd);
  const root = project !== null ? dirname6(project.path) : resolve7(cwd);
  return join11(root, WORKSPACE_THEMES_DIRNAME, `${id}.theme.json`);
}
async function resolveThemeWriteTarget(opts) {
  if (opts.output !== void 0) {
    const output = resolve7(opts.cwd, opts.output);
    const id = opts.id ?? defaultThemeIdFor(output);
    assertThemeId(id);
    return { id, output };
  }
  if (opts.id !== void 0) {
    assertThemeId(opts.id);
    return { id: opts.id, output: await defaultThemeOutputPath(opts.id, opts.cwd) };
  }
  throw new PptwiseError("pass --id or -o so the theme file has a name");
}
async function themeFileFromResolved(resolved, identity) {
  if (resolved.kind === "builtin") {
    return themeFileFromPreset(resolved.id, identity);
  }
  const copy = structuredClone(resolved.file);
  copy.id = identity.id;
  copy.style = { ...copy.style, id: identity.id };
  if (identity.label !== void 0) copy.label = identity.label;
  return ThemeFileSchema.parse(copy);
}
function rethrowBrandColorError(error, id) {
  const message = error instanceof Error ? error.message : String(error);
  if (/colors\.|contrast ratio|calibrate/i.test(message)) {
    throw new PptwiseError(
      `${message}. Run \`pptwise theme new --from <preset> --id ${id}\`, adjust the copied theme colors by hand, then bind that theme`
    );
  }
  throw error;
}
async function runBrandExtract(file, opts) {
  let bytes;
  try {
    bytes = await readFile7(file);
  } catch {
    throw new PptwiseError(`cannot read template file: ${file}`);
  }
  const id = opts.id ?? defaultThemeIdFor(opts.output);
  assertThemeId(id);
  const from = opts.from ?? "bulletin";
  const cwd = dirname6(resolve7(opts.output));
  const donor = await resolveThemeByName(from, { startDir: cwd });
  let result;
  try {
    result = await extractBrandTheme(bytes, {
      id,
      label: opts.label,
      from: donor.kind === "builtin" ? donor.id : donor.file,
      brandFonts: opts.brandFonts === true
    });
  } catch (error) {
    rethrowBrandColorError(error, id);
  }
  const theme2 = result.file;
  const outPath = resolve7(opts.output);
  await writeThemeFile(outPath, theme2, opts.force === true);
  const c = theme2.style.colors;
  const lines = [
    `wrote ${opts.output} (theme "${theme2.id}", label "${theme2.label}", from "${from}")`,
    ...result.placement.brand.neutral ? ["  the template has no colored brand color: its accent1 is a grey, a black or a white"] : [],
    ...describePlacement(result.placement, "the template's accent1"),
    `  colors: primary ${c.primary}, accent ${c.accent}, ${c.chartPalette.length} chart colors. bg ${c.bg}, text ${c.text}, surface ${c.surface} stay ${from}'s`,
    opts.brandFonts !== true ? `  fonts: ${from}'s own, heading "${resolveFontFace(theme2.style.fonts.heading, "heading")}", body "${resolveFontFace(theme2.style.fonts.body, "body")}" (--brand-fonts puts the template's Latin fonts first)` : `  fonts: heading "${theme2.style.fonts.heading[0]}", body "${theme2.style.fonts.body[0]}" from the template, Chinese text in ${from}'s own faces`,
    ...result.fontNotes.map((note) => `  ${note}`),
    `Drop the file in a deck ${THEME_FILENAME} or workspace themes/ and set spec.theme to "${theme2.id}".`
  ];
  return lines.join("\n");
}
async function runThemeNew(opts) {
  const cwd = opts.cwd ?? process.cwd();
  const { id, output } = await resolveThemeWriteTarget({ id: opts.id, output: opts.output, cwd });
  const resolved = await resolveThemeByName(opts.from, { startDir: cwd });
  const file = await themeFileFromResolved(resolved, { id, label: opts.label });
  await writeThemeFile(output, file, opts.force === true);
  return `wrote ${output} (theme "${file.id}"). Set spec.theme to "${file.id}".`;
}
var FORK_ANCHOR_FLAGS = ["primary", "accent", "bg", "text", "surface"];
async function runThemeFork(name, opts) {
  const anchors = FORK_ANCHOR_FLAGS.filter((flag) => opts[flag] !== void 0);
  if (opts.brand !== void 0 && anchors.length > 0) {
    throw new PptwiseError(
      `--brand repaints the theme around a brand color and cannot be combined with ${anchors.map((flag) => `--${flag}`).join(", ")}. Use --brand alone, or set the tokens exactly with --primary and friends`
    );
  }
  if (opts.brand === void 0 && opts.primary === void 0) {
    throw new PptwiseError("pptwise theme fork needs --brand <hex>, or --primary <hex> to set the tokens exactly");
  }
  const cwd = opts.cwd ?? process.cwd();
  const { id, output } = await resolveThemeWriteTarget({ id: opts.id, output: opts.output, cwd });
  const resolved = await resolveThemeByName(name, { startDir: cwd });
  const source = await themeFileFromResolved(resolved, { id, label: opts.label });
  if (opts.brand !== void 0) {
    const result = regenerateFromBrand(source, parseBrandOption(opts.brand), { id, label: opts.label ?? source.label });
    await writeThemeFile(output, result.file, opts.force === true);
    return [
      `wrote ${output} (theme "${result.file.id}"). Set spec.theme to "${result.file.id}".`,
      ...describePlacement(result.placement, "--brand")
    ].join("\n");
  }
  const file = forkTheme(
    source,
    { primary: opts.primary, bg: opts.bg, accent: opts.accent, text: opts.text, surface: opts.surface },
    { id, label: opts.label ?? source.label }
  );
  await writeThemeFile(output, file, opts.force === true);
  return `wrote ${output} (theme "${file.id}"). Set spec.theme to "${file.id}".`;
}
function themeTryShortlist(occasion) {
  const occasions = [];
  let strategy;
  for (const word of (occasion ?? "").split(",").map((part) => part.trim()).filter((part) => part.length > 0)) {
    if (Object.hasOwn(OCCASION_VOCAB, word)) {
      occasions.push(word);
      continue;
    }
    if (Object.hasOwn(NARRATIVE_PRESETS, word) || STRATEGY_VALUES.includes(word)) {
      if (strategy !== void 0) throw new PptwiseError(`--occasion names two narratives, "${strategy}" and "${word}". Keep one`);
      strategy = word;
      continue;
    }
    throw new PptwiseError(
      `unknown --occasion "${word}". Use occasion words (${Object.keys(OCCASION_VOCAB).join(", ")}) or a narrative preset (${Object.keys(NARRATIVE_PRESETS).join(", ")})`
    );
  }
  return themeShortlist({ occasions, ...strategy !== void 0 ? { strategy } : {} });
}
function parseThemeTryIds(raw) {
  const ids = raw.split(",").map((part) => part.trim()).filter((part) => part.length > 0);
  if (ids.length < 2 || ids.length > 4) {
    throw new PptwiseError(`pptwise theme try expects 2-4 theme ids, got ${ids.length}`);
  }
  const seen = /* @__PURE__ */ new Set();
  for (const id of ids) {
    if (seen.has(id)) throw new PptwiseError(`pptwise theme try has duplicate theme id "${id}"`);
    seen.add(id);
  }
  return ids;
}
function contactSheetSlidesFromIr(ir, svgs) {
  return ir.slides.map((slide, index) => {
    const type = slide.type ?? "content";
    const label = type === "content" && typeof slide.kind === "string" ? slide.kind : type;
    return { type, label, svg: svgs[index] };
  });
}
async function runThemeTry(idsRaw, opts = {}) {
  const named = idsRaw !== void 0 && idsRaw.trim() !== "";
  if (opts.title !== void 0) {
    if (named && opts.occasion !== void 0) {
      throw new PptwiseError("--occasion picks the themes when none are named. Pass theme ids or --occasion, not both");
    }
    return runThemeWall(named ? idsRaw : themeTryShortlist(opts.occasion).join(","), { ...opts, title: opts.title });
  }
  const needsTitle = [
    ["--subtitle", opts.subtitle],
    ["--lang", opts.lang],
    ["--page", opts.page],
    ["--json", opts.json || void 0],
    ["--occasion", opts.occasion]
  ].filter(([, value]) => value !== void 0);
  if (needsTitle.length > 0) {
    throw new PptwiseError(`${needsTitle.map(([flag]) => flag).join(", ")} draw the caller's own pages and need --title`);
  }
  if (!named) throw new PptwiseError("pptwise theme try expects 2-4 theme ids, or --title to draw your own cover");
  const cwd = opts.cwd ?? process.cwd();
  const ids = parseThemeTryIds(idsRaw);
  const columns = [];
  for (const name of ids) {
    const resolved = await resolveThemeByName(name, { startDir: cwd });
    const raw = structuredClone(THEME_TRY_SAMPLE_IR);
    raw.theme = { id: resolved.id };
    const offered = new Set(offeredContentKinds(resolved.definition.menu));
    raw.slides = raw.slides.filter((slide) => slide.type !== "content" || offered.has(slide.kind ?? ""));
    const v2 = validateIr(raw, { theme: resolved.definition });
    if (!v2.ok) throw new PptwiseError(`invalid IR:
${formatIssues(v2.errors)}`);
    const ir = v2.ir;
    const svgs = ir.slides.map((_, index) => renderSlideSvg(ir, index, { theme: resolved.definition }));
    columns.push({ id: resolved.id, slides: contactSheetSlidesFromIr(ir, svgs) });
  }
  const { resolvedOut, extraNotes } = await themeTryOutDir(cwd, opts);
  const htmlPath = join11(resolvedOut, "contact-sheet.html");
  await writeFile7(htmlPath, buildContactSheetHtml({ title: "theme try", themes: columns }));
  const ok = `wrote contact sheet to ${htmlPath}`;
  return extraNotes.length > 0 ? `${ok}
${extraNotes.join("\n")}` : ok;
}
async function themeTryOutDir(cwd, opts) {
  if (opts.output !== void 0) {
    const resolvedOut = resolve7(cwd, opts.output);
    await mkdir6(resolvedOut, { recursive: true });
    return { resolvedOut, extraNotes: [] };
  }
  const projectHit = await findConfig(cwd);
  const location = resolveWorkspaceLocation({
    cwd,
    projectConfigPath: projectHit?.path,
    target: "theme-try",
    isDir: true
  });
  const extraNotes = await prepareWorkspaceDir(location, { gitIgnore: opts.gitIgnore, runGit: opts.runGit });
  return { resolvedOut: location.dir, extraNotes };
}
async function themeWallNames(raw) {
  if (raw.trim() === "all") {
    return [...CANONICAL_THEME_IDS, ...(await readablePackDefinitions()).map((definition) => definition.id)];
  }
  const ids = raw.split(",").map((part) => part.trim()).filter((part) => part.length > 0);
  if (ids.length === 0) throw new PptwiseError("pptwise theme try expects theme ids, or all");
  const seen = /* @__PURE__ */ new Set();
  for (const id of ids) {
    if (seen.has(id)) throw new PptwiseError(`pptwise theme try has duplicate theme id "${id}"`);
    seen.add(id);
  }
  return ids;
}
async function runThemeWall(idsRaw, opts) {
  const cwd = opts.cwd ?? process.cwd();
  const title = opts.title.trim();
  if (title === "") throw new PptwiseError("--title is empty. Pass the deck's cover title");
  const names = await themeWallNames(idsRaw);
  const themes = [];
  for (const name of names) {
    const resolved = await resolveThemeByName(name, { startDir: cwd });
    const source = resolved.kind === "builtin" ? "builtin" : resolved.pack !== void 0 ? "pack" : "file";
    themes.push({ id: resolved.id, label: resolved.definition.label ?? resolved.id, source, definition: resolved.definition });
  }
  let contentPage;
  if (opts.page !== void 0) {
    const pagePath = resolve7(cwd, opts.page);
    let text;
    try {
      text = await readFile7(pagePath, "utf8");
    } catch {
      throw new PptwiseError(`cannot read --page file: ${pagePath}`);
    }
    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch (e) {
      throw new PptwiseError(`--page file is not JSON: ${pagePath}: ${e instanceof Error ? e.message : String(e)}`);
    }
    contentPage = themeWallContentPage(parsed, pagePath);
  }
  const subtitle = opts.subtitle?.trim();
  const wall = buildThemeWall({
    title,
    ...subtitle ? { subtitle } : {},
    lang: themeWallLang(title, opts.lang),
    ...contentPage !== void 0 ? { contentPage } : {},
    themes
  });
  const { resolvedOut, extraNotes } = await themeTryOutDir(cwd, opts);
  for (const theme2 of themes) {
    for (const type of ["cover", "content"]) await rm3(join11(resolvedOut, `${theme2.id}-${type}.svg`), { force: true });
  }
  for (const file of wall.files) await writeFile7(join11(resolvedOut, file.name), file.svg);
  await writeFile7(
    join11(resolvedOut, THEME_WALL_SHEET_FILE),
    buildThemeWallHtml({ title, columns: ["cover", "content"], rows: wall.rows })
  );
  await writeFile7(join11(resolvedOut, THEME_WALL_MANIFEST_FILE), `${JSON.stringify(wall.manifest, null, 2)}
`);
  if (opts.json) {
    const notes = themeWallSkipNotes(wall.manifest.themes);
    return JSON.stringify({ dir: resolvedOut, ...wall.manifest, ...notes.length > 0 ? { notes } : {} }, null, 2);
  }
  const summary = formatThemeWall(wall.manifest, resolvedOut);
  return extraNotes.length > 0 ? `${summary}
${extraNotes.join("\n")}` : summary;
}
function runNarratives(asJson) {
  if (asJson) {
    return JSON.stringify(
      {
        presets: NARRATIVE_PRESETS,
        strategies: STRATEGY_DEFINITIONS,
        pacings: PACING_BUDGETS,
        audiences: AUDIENCE_VALUES
      },
      null,
      2
    );
  }
  const rows = Object.values(NARRATIVE_PRESETS).map((p) => ({
    id: p.id,
    axes: `${p.axes.strategy}/${p.axes.pacing}/${p.axes.audience}`,
    themes: p.themeRecommendations.join(", ")
  }));
  const idWidth = Math.max(...rows.map((r) => r.id.length));
  const axesWidth = Math.max(...rows.map((r) => r.axes.length));
  return rows.map((r) => `${r.id.padEnd(idWidth + 2)}${r.axes.padEnd(axesWidth + 2)}${r.themes}`).join("\n");
}
var CONFIG_TEMPLATE = {};
async function runInit(cwd = process.cwd()) {
  const target = join11(cwd, CONFIG_FILENAME);
  try {
    await writeFile7(target, JSON.stringify(CONFIG_TEMPLATE, null, 2) + "\n", { flag: "wx" });
  } catch (e) {
    if (e.code === "EEXIST") {
      throw new PptwiseError(`${target} already exists \u2014 edit it instead`);
    }
    throw e;
  }
  return `wrote ${target} \u2014 themes: \`pptwise themes\``;
}
var DeckBuildError = class extends PptwiseError {
  themeInputs;
  constructor(cause, themeInputs) {
    super(cause instanceof Error ? cause.message : String(cause), { cause });
    this.themeInputs = themeInputs;
  }
};
async function renderDeckSlides(target, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  let location;
  let projectHit;
  try {
    ;
    [projectHit] = await readConfigs(cwd);
    location = await locateDeckTarget(target, cwd);
  } catch (e) {
    throw new DeckBuildError(e, unreadThemeInputs(e));
  }
  const themeInputs = await collectThemeInputs({ startDir: cwd, ...location });
  try {
    const { raw, baseDir, isDir, resolvedTarget, workspaceAssetsDir, missingAssetPath } = await readDeckTarget(location, themeInputs, cwd, projectHit);
    const theme2 = (await applyDeckConfig(raw, themeInputs))?.definition;
    const v2 = validateIr(raw, { theme: theme2, missingAssetPath });
    if (!v2.ok) throw new PptwiseError(`invalid IR:
${formatIssues(v2.errors)}`);
    await resolveLocalAssets(v2.ir, baseDir, workspaceAssetsDir);
    const ir = v2.ir;
    const svgs = ir.slides.map((_, i) => renderSlideSvg(ir, i, { theme: theme2 }));
    return { ir, theme: theme2, themeInputs, svgs, resolvedTarget, isDir, normalized: v2.normalized };
  } catch (e) {
    throw new DeckBuildError(e, themeInputs);
  }
}
function buildDeckAuditAndHtml(ir, svgs, theme2) {
  const hasPlaceholder = ir.slides.some((slide) => slide.placeholder);
  const auditReport = hasPlaceholder ? void 0 : auditDeck(ir, { theme: theme2 });
  const findings = auditReport?.findings ?? [];
  const html = buildPreviewHtml({
    title: ir.filename,
    slides: ir.slides.map((slide, i) => ({
      index: i,
      id: slide.id,
      type: slide.type,
      svg: svgs[i],
      placeholder: slide.placeholder
    })),
    findings: findings.map((f) => ({ page: f.page, slideId: f.slideId, code: f.code, message: f.message })),
    auditNote: hasPlaceholder ? "audit overlay skipped \u2014 deck has unfilled placeholder pages; fill every page and re-run `pptwise preview --html` to see audit findings" : void 0,
    checks: auditReport?.checks
  });
  return { html, findings, checks: auditReport?.checks };
}
async function buildDeckPreview(target, opts = {}) {
  const rendered = await renderDeckSlides(target, opts);
  try {
    const { html, findings, checks } = buildDeckAuditAndHtml(rendered.ir, rendered.svgs, rendered.theme);
    return { ...rendered, html, findings, checks };
  } catch (e) {
    throw new DeckBuildError(e, rendered.themeInputs);
  }
}
async function resolvePreviewOutDir(cwd, outDir, resolvedTarget, isDir, opts) {
  if (outDir !== void 0) {
    const resolvedOut = resolve7(cwd, outDir);
    await mkdir6(resolvedOut, { recursive: true });
    return { resolvedOut, extraNotes: [] };
  }
  const projectHit = await findConfig(cwd);
  const location = resolveWorkspaceLocation({
    cwd,
    projectConfigPath: projectHit?.path,
    target: resolvedTarget,
    isDir
  });
  const extraNotes = await prepareWorkspaceDir(location, { gitIgnore: opts.gitIgnore, runGit: opts.runGit });
  await pruneRenderedSvgs(location.dir);
  return { resolvedOut: location.dir, extraNotes };
}
var DROP_MARK = /data-dropped="(\d+)"(?:\s+data-dropped-kind="([a-z-]+)")?/g;
function droppedContentNote(ir, svgs) {
  const refs = [];
  svgs.forEach((svg, i) => {
    const byKind = /* @__PURE__ */ new Map();
    for (const m of svg.matchAll(DROP_MARK)) {
      const count = Number(m[1]);
      if (count <= 0) continue;
      const kind = parseDropKind(m[2]);
      byKind.set(kind, (byKind.get(kind) ?? 0) + count);
    }
    if (byKind.size === 0) return;
    const id = ir.slides[i]?.id;
    const where2 = id ? `${id} (page ${i + 1})` : `page ${i + 1}`;
    refs.push(`${where2}: ${Array.from(byKind, ([kind, count]) => dropPhrase(kind, count)).join(", ")}`);
  });
  if (refs.length === 0) return null;
  return `note: ${refs.length} page${refs.length === 1 ? " drops" : "s drop"} content that does not fit, and render will refuse the deck until ${refs.length === 1 ? "it fits" : "they fit"}. ${refs.join(". ")}. Shorten the content or split the page in two`;
}
async function writeSlideSvgs(outDir, ir, svgs) {
  const svgNames = [];
  for (let i = 0; i < ir.slides.length; i++) {
    const name = `${String(i + 1).padStart(3, "0")}-${ir.slides[i].type}.svg`;
    svgNames.push(name);
    await writeFile7(join11(outDir, name), svgs[i]);
  }
  return svgNames;
}
async function writePreviewReview(outDir, ir, svgs, svgNames, theme2) {
  const { html, findings, checks } = buildDeckAuditAndHtml(ir, svgs, theme2);
  const htmlPath = join11(outDir, "preview.html");
  await writeFile7(htmlPath, html);
  const hasPlaceholder = ir.slides.some((s) => s.placeholder);
  const manifest = buildPreviewManifest({
    title: ir.filename,
    pptwiseVersion: VERSION,
    width: CANVAS_W_PX,
    height: CANVAS_H_PX,
    slides: ir.slides.map((slide, i) => ({
      index: i,
      type: slide.type ?? "content",
      id: slide.id,
      placeholder: slide.placeholder,
      file: svgNames[i]
    })),
    findings: findings.map((f) => ({ page: f.page, code: f.code, message: f.message })),
    checks,
    auditNote: hasPlaceholder ? "audit skipped \u2014 deck has unfilled placeholder pages" : void 0
  });
  const manifestPath = join11(outDir, "manifest.json");
  await writeFile7(manifestPath, `${JSON.stringify(manifest, null, 2)}
`);
  return { htmlPath, manifestPath, findings, ...checks !== void 0 ? { checks } : {} };
}
async function runPreview(irPath, outDir, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  const { ir, theme: theme2, svgs, normalized, isDir, resolvedTarget } = await renderDeckSlides(irPath, {
    cwd
  });
  const { resolvedOut, extraNotes } = await resolvePreviewOutDir(cwd, outDir, resolvedTarget, isDir, opts);
  const svgNames = await writeSlideSvgs(resolvedOut, ir, svgs);
  const ok = `wrote ${ir.slides.length} SVG files to ${resolvedOut}`;
  const notes = [...extraNotes];
  const aliasNote = normalizedNote(normalized);
  if (aliasNote) notes.push(aliasNote);
  const dropNote = droppedContentNote(ir, svgs);
  if (dropNote) notes.push(dropNote);
  if (opts.htmlOut) {
    const { htmlPath, manifestPath, findings } = await writePreviewReview(resolvedOut, ir, svgs, svgNames, theme2);
    notes.push(`note: wrote self-contained preview to ${htmlPath}`);
    notes.push(`note: wrote machine-readable page manifest to ${manifestPath}`);
    if (findings.length > 0) {
      notes.push(`note: audit found ${findings.length} finding${findings.length === 1 ? "" : "s"} \u2014 see preview.html`);
    }
  }
  return notes.length > 0 ? `${ok}
${notes.join("\n")}` : ok;
}
async function runBuild(target, opts = {}) {
  const report = await buildDeck(target, opts);
  return {
    output: opts.json ? JSON.stringify(report, null, 2) : formatBuildReport(report),
    ok: report.status === "ok"
  };
}
async function specPageIds(deckDir) {
  try {
    const spec2 = JSON.parse(await readFile7(join11(deckDir, SPEC_FILENAME), "utf8"));
    return Array.isArray(spec2.pages) ? spec2.pages.map((page) => typeof page?.id === "string" ? page.id : "") : [];
  } catch {
    return [];
  }
}
function drawnAsReport(ir, theme2) {
  const definition = resolveIrTheme(ir, theme2);
  const out = [];
  ir.slides.forEach((slide, index) => {
    if (slide.type !== "content") return;
    const served = resolveEffectiveFace(ir, slide, definition).servedKind;
    if (served === void 0 || served === slide.kind) return;
    out.push({ page: index + 1, ...slide.id !== void 0 ? { pageId: slide.id } : {}, kind: slide.kind, drawnAs: served });
  });
  return out;
}
function themeSourceOf(resolved) {
  if (resolved.kind === "builtin") return "builtin";
  return resolved.pack !== void 0 ? "pack" : "file";
}
async function wantsAlternatives(flag, resolved, workspaceDir) {
  if (flag !== void 0) return flag;
  if (resolved?.kind !== "builtin") return false;
  return !await pathExists(join11(workspaceDir, ALTERNATIVES_DIRNAME, "manifest.json"));
}
var SWITCH_DECLARED_AUDIT_CODES = /* @__PURE__ */ new Set(["content-truncated", "content-dropped", "stepped-aside"]);
function signatureReport(ir, theme2, svgs, isDir) {
  const perPage = [];
  ir.slides.forEach((slide, i) => {
    const use = pageSignatureUse(ir, slide, theme2, svgs[i]);
    if (use === void 0) return;
    perPage.push({
      page: i + 1,
      ...slide.id !== void 0 ? { pageId: slide.id } : {},
      ...slide.id !== void 0 && isDir ? { file: `${PAGES_DIRNAME}/${slide.id}.json` } : {},
      drawnBy: use.drawnBy,
      ...use.nearest !== void 0 ? { nearest: use.nearest } : {}
    });
  });
  return { pages: ir.slides.length, offered: perPage.length, drawn: perPage.filter((entry) => entry.drawnBy !== null).length, perPage };
}
async function buildDeck(target, opts) {
  const cwd = opts.cwd ?? process.cwd();
  const [projectHit] = await readConfigs(cwd);
  const location = await locateDeckTarget(target, cwd);
  const { isDir, resolvedTarget } = location;
  if (!await pathExists(resolvedTarget)) {
    throw new PptwiseError(`nothing to build at ${resolvedTarget}: pass a deck project directory or an IR JSON file`);
  }
  const workspace = resolveWorkspaceLocation({
    cwd,
    projectConfigPath: projectHit?.path,
    target: resolvedTarget,
    isDir
  });
  const report = {
    status: "needs_revision",
    target: resolvedTarget,
    theme: void 0,
    pageCount: void 0,
    audited: false,
    errors: [],
    warnings: [],
    preview: null,
    pptx: null,
    notes: []
  };
  const needsRevision = async (errors2) => {
    await removeFinalPptx(workspace.dir);
    return { ...report, status: "needs_revision", errors: errors2 };
  };
  const themeInputs = await collectThemeInputs({ startDir: cwd, ...location });
  let loaded;
  let theme2;
  let resolvedTheme;
  try {
    loaded = await readDeckTarget(location, themeInputs, cwd, projectHit);
    resolvedTheme = await applyDeckConfig(loaded.raw, themeInputs);
    theme2 = resolvedTheme?.definition;
  } catch (e) {
    if (!(e instanceof PptwiseError)) throw e;
    return needsRevision(assembleIssues(e.message, isDir ? await specPageIds(resolvedTarget) : []));
  }
  const writtenFor = isDir ? await readWrittenFor(workspace.dir) : void 0;
  const v2 = validateIr(loaded.raw, { theme: theme2, missingAssetPath: loaded.missingAssetPath, ...writtenFor !== void 0 ? { writtenFor } : {} });
  report.warnings = (v2.warnings ?? []).map((issue) => validateIssue(issue, isDir));
  if (!v2.ok) return needsRevision(v2.errors.map((issue) => validateIssue(issue, isDir)));
  const ir = v2.ir;
  report.theme = ir.theme.id;
  if (resolvedTheme !== void 0) report.themeSource = themeSourceOf(resolvedTheme);
  report.pageCount = ir.slides.length;
  const drawnAs = drawnAsReport(ir, theme2);
  if (drawnAs.length > 0) report.drawnAs = drawnAs;
  try {
    await resolveLocalAssets(ir, loaded.baseDir, loaded.workspaceAssetsDir);
  } catch (e) {
    if (!(e instanceof PptwiseError)) throw e;
    return needsRevision([{ stage: "validate", message: e.message }]);
  }
  const svgs = ir.slides.map((_, i) => renderSlideSvg(ir, i, { theme: theme2 }));
  if (theme2 !== void 0) report.signature = signatureReport(ir, theme2, svgs, isDir);
  report.notes.push(...await prepareWorkspaceDir(workspace, { gitIgnore: opts.gitIgnore, runGit: opts.runGit }));
  await pruneRenderedSvgs(workspace.dir);
  const svgNames = await writeSlideSvgs(workspace.dir, ir, svgs);
  const review = await writePreviewReview(workspace.dir, ir, svgs, svgNames, theme2);
  report.audited = review.checks !== void 0;
  report.preview = {
    dir: workspace.dir,
    html: review.htmlPath,
    manifest: review.manifestPath,
    pages: ir.slides.map((slide, i) => ({
      page: i + 1,
      ...slide.id !== void 0 ? { id: slide.id } : {},
      type: slide.type ?? "content",
      file: join11(workspace.dir, svgNames[i])
    }))
  };
  if (await wantsAlternatives(opts.alternatives, resolvedTheme, workspace.dir)) {
    report.alternatives = await writeBuildAlternatives(ir, resolveIrTheme(ir, theme2), workspace.dir);
  }
  const switched = writtenFor !== void 0 && writtenFor !== ir.theme.id;
  const shortHere = switched ? review.findings.filter((finding) => SWITCH_DECLARED_AUDIT_CODES.has(finding.code)) : [];
  report.warnings.push(...shortHere.map((finding) => auditIssue(finding, isDir)));
  const drawnShort = v2.switchedFrom !== void 0 || shortHere.length > 0;
  const errors = [...placeholderIssues(ir, isDir), ...review.findings.filter((finding) => !shortHere.includes(finding)).map((finding) => auditIssue(finding, isDir))];
  if (errors.length > 0) return needsRevision(errors);
  let bytes;
  try {
    bytes = await generatePptx(ir, { theme: theme2, ...drawnShort ? { allowDroppedContent: true } : {} });
  } catch (e) {
    if (!(e instanceof PptwiseError)) throw e;
    return needsRevision([{ stage: "render", message: e.message }]);
  }
  await removeFinalPptx(workspace.dir);
  const pptxPath = join11(workspace.dir, finalPptxName(deckFilename(loaded), workspace.name));
  await writeFile7(pptxPath, bytes);
  if (isDir && !drawnShort) await writeWrittenFor(workspace.dir, ir.theme.id);
  if (drawnShort) report.writtenFor = writtenFor;
  return { ...report, status: "ok", pptx: pptxPath };
}
function withRewrittenAssetPaths(ir, deckDir, outDir) {
  const images2 = Object.fromEntries(
    Object.entries(ir.assets.images).map(([id, asset]) => {
      if (asset.src.startsWith("data:") || /^https?:\/\//.test(asset.src)) return [id, asset];
      return [id, { ...asset, src: relative3(outDir, join11(deckDir, asset.src)) }];
    })
  );
  return { ...ir, assets: { images: images2 } };
}
async function runAssemble(target, opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  const dir = await resolveDeckTarget(target, cwd);
  if (await pathExists(dir) && !await isDeckDirectory(dir)) {
    throw new PptwiseError(`expected a deck project directory: ${dir}`);
  }
  const themeInputs = await isDeckDirectory(dir) ? await collectThemeInputs({ startDir: cwd, resolvedTarget: dir, isDir: true }) : void 0;
  const { ir, deckDir } = await readDeckDir(dir, {
    theme: themeInputs && themeFromInputs(themeInputs)?.definition,
    spec: themeInputs && sourceFromInputs(themeInputs)
  });
  const outPath = opts.output ? resolve7(cwd, opts.output) : join11(deckDir, "deck.json");
  const outDir = dirname6(outPath);
  const outIr = outDir === deckDir ? ir : withRewrittenAssetPaths(ir, deckDir, outDir);
  await mkdir6(outDir, { recursive: true });
  await writeFile7(outPath, JSON.stringify(outIr, null, 2) + "\n");
  const placeholderCount = outIr.slides.filter((s) => s.placeholder).length;
  const summary = `wrote ${outPath} (${outIr.slides.length} slides, ${placeholderCount} placeholder${placeholderCount === 1 ? "" : "s"})`;
  return summary;
}
async function runDisassemble(irPath, outDir) {
  const raw = await loadIrFile(irPath);
  const v2 = validateIr(raw);
  if (!v2.ok) throw new PptwiseError(`invalid IR:
${formatIssues(v2.errors)}`);
  const { spec: spec2, pages } = disassembleDeck(v2.ir);
  const ids = Object.keys(pages);
  for (const id of ids) assertSafeFileSegment(id, "slide id");
  const specPath = join11(outDir, "deck.spec.json");
  await mkdir6(outDir, { recursive: true });
  try {
    await writeFile7(specPath, JSON.stringify(spec2, null, 2) + "\n", { flag: "wx" });
  } catch (e) {
    if (e.code === "EEXIST") {
      throw new PptwiseError(`${specPath} already exists \u2014 refusing to overwrite an existing deck project`);
    }
    throw e;
  }
  const pagesDir = join11(outDir, "pages");
  try {
    if (ids.length > 0) {
      await mkdir6(pagesDir, { recursive: true });
      await Promise.all(
        ids.map((id) => {
          const content = pages[id];
          return writeFile7(join11(pagesDir, `${id}.json`), JSON.stringify(content, null, 2) + "\n");
        })
      );
    }
    const { count: assetCount, assetsDir } = await writeDeckAssets(
      v2.ir.assets.images,
      outDir,
      dirname6(resolve7(irPath))
    );
    const pagesNote = ids.length > 0 ? `${ids.length} page file${ids.length === 1 ? "" : "s"} to ${pagesDir}` : "no pages (every slide was a placeholder)";
    const assetsNote = assetCount > 0 ? `, and ${assetCount} asset file${assetCount === 1 ? "" : "s"} to ${assetsDir}` : "";
    return `wrote ${specPath}, ${pagesNote}${assetsNote}`;
  } catch (e) {
    await rm3(specPath, { force: true }).catch(() => {
    });
    throw e;
  }
}

// src/cli/secret-input.ts
import readline from "readline";
async function readSecret(prompt, io = { stdin: process.stdin, stderr: process.stderr }) {
  const { stdin, stderr } = io;
  const isTTY = Boolean(stdin.isTTY);
  if (!isTTY) {
    const line = await readFirstLine(stdin);
    if (line === "") throw new PptwiseError("API key cannot be empty");
    return line;
  }
  return await readHiddenTty(prompt, stdin, stderr);
}
function readFirstLine(stdin) {
  return new Promise((resolve11, reject) => {
    const encoding = stdin.readableEncoding ?? "utf8";
    let buf = "";
    const onData = (chunk) => {
      buf += typeof chunk === "string" ? chunk : chunk.toString(encoding);
      const nl = buf.indexOf("\n");
      if (nl === -1) return;
      cleanup();
      resolve11(buf.slice(0, nl).replace(/\r$/, "").trim());
    };
    const onEnd = () => {
      cleanup();
      resolve11(buf.replace(/\r$/, "").trim());
    };
    const onError = (e) => {
      cleanup();
      reject(e);
    };
    const cleanup = () => {
      stdin.off("data", onData);
      stdin.off("end", onEnd);
      stdin.off("error", onError);
    };
    stdin.on("data", onData);
    stdin.on("end", onEnd);
    stdin.on("error", onError);
  });
}
function readHiddenTty(prompt, stdin, stderr) {
  return new Promise((resolve11, reject) => {
    const rl = readline.createInterface({ input: stdin, output: stderr, terminal: true });
    const mutable = rl;
    mutable._writeToOutput = () => {
    };
    stderr.write(prompt);
    let settled = false;
    const finish = (fn) => {
      if (settled) return;
      settled = true;
      fn();
    };
    rl.question("", (answer) => {
      finish(() => {
        rl.close();
        stderr.write("\n");
        const value = answer.trim();
        if (value === "") reject(new PptwiseError("API key cannot be empty"));
        else resolve11(value);
      });
    });
    rl.on("SIGINT", () => {
      finish(() => {
        rl.close();
        stderr.write("\n");
        reject(new PptwiseError("cancelled"));
      });
    });
    rl.on("close", () => {
      finish(() => reject(new PptwiseError("cancelled")));
    });
  });
}

// src/cli/config-cmd.ts
function canOmitValue(key) {
  return key.endsWith(".apiKey") || key.endsWith(".clientSecret");
}
async function runConfigSet(key, value, opts = {}) {
  if (value === void 0 && !canOmitValue(key)) {
    throw new PptwiseError(`${key} needs a value: pptwise config set ${key} <value>`);
  }
  const parsed = parseCliConfigKey(key);
  let resolved = value;
  if (resolved === void 0) {
    const read = opts.readSecret ?? readSecret;
    resolved = await read(`${key} (input hidden): `, opts.io);
  }
  const stored = parseCliConfigValue(parsed, resolved);
  const path2 = await persistUserConfigValue(parsed.path, stored);
  return `Saved ${key} to ${path2}`;
}
async function runConfigShow(opts = {}) {
  const path2 = userConfigPath();
  const hit = await findUserConfig();
  const file = hit?.config ?? null;
  const keys = resolveImageKeys({ file, env: opts.env ?? process.env });
  const lines = [`User config: ${path2}`, ""];
  for (const provider of ["pexels", "pixabay"]) {
    const label = `${provider}.apiKey`;
    const entry = keys[provider];
    if (!entry.apiKey) {
      lines.push(`${label}  missing`);
      continue;
    }
    const src = entry.source === null ? "" : ` (${entry.source})`;
    lines.push(`${label}  ${maskKey(entry.apiKey)}${src}`);
  }
  const ov = keys.openverse;
  const ovSrc = ov.source === null ? "" : ` (${ov.source})`;
  if (ov.clientId) lines.push(`openverse.clientId  ${maskKey(ov.clientId)}${ovSrc}`);
  else lines.push("openverse.clientId  missing");
  if (ov.clientSecret) lines.push(`openverse.clientSecret  ${maskKey(ov.clientSecret)}${ovSrc}`);
  else lines.push("openverse.clientSecret  missing");
  const gens = resolveGenerators({ file });
  lines.push("");
  for (const id of GENERATOR_IDS) {
    lines.push(`images.generators.${id}.enabled  ${gens.enabled[id] ? "true" : "false"}`);
  }
  const rawGens = file?.images?.generators;
  if (rawGens?.order) lines.push(`images.generators.order  ${rawGens.order.join(",")}`);
  if (rawGens?.timeoutMs !== void 0) lines.push(`images.generators.timeoutMs  ${rawGens.timeoutMs}`);
  return lines.join("\n");
}

// src/cli/doctor.ts
import { lstatSync as lstatSync2 } from "fs";
import { access, readFile as readFile8, readdir as readdir5 } from "fs/promises";
import { homedir } from "os";
import { basename as basename6, join as join13 } from "path";

// src/cli/image-generators.ts
import { copyFile as copyFile2, readdir as readdir4, stat as stat3 } from "fs/promises";
import { join as join12 } from "path";
var GENERATOR_PROBE_TIMEOUT_MS = 2e3;
var BIN_NAMES = {
  grok: ["grok"],
  codex: ["codex"],
  antigravity: ["antigravity", "agy"]
};
async function locateGeneratorBin(id, env) {
  for (const name of BIN_NAMES[id]) {
    const found = await findOnPath(name, env);
    if (found) return found;
  }
  return null;
}
function parseGeneratorVersion(stdout) {
  const line = stdout.trim().split("\n")[0] ?? "";
  const m = /(\d+\.\d+\.\d+\S*)/.exec(line);
  return m?.[1] ?? line;
}
async function defaultProcessRunner(req) {
  try {
    return await runChild(req.command, req.args, {
      cwd: req.cwd,
      env: req.env,
      timeoutMs: req.timeoutMs
    });
  } catch (error) {
    if (error instanceof ChildTimeoutError) {
      throw new PptwiseError(`image generator timed out after ${req.timeoutMs}ms`);
    }
    const message = error instanceof Error ? error.message : String(error);
    return { code: 1, stdout: "", stderr: message };
  }
}
async function probeGenerators(opts) {
  const env = opts.env ?? process.env;
  const run = opts.run ?? defaultProcessRunner;
  const probes = [];
  for (const id of GENERATOR_IDS) {
    const bin = await locateGeneratorBin(id, env);
    let version = null;
    if (bin) {
      try {
        const result = await run({ command: bin, args: ["--version"], cwd: void 0, timeoutMs: GENERATOR_PROBE_TIMEOUT_MS, env });
        if (result.code === 0) version = parseGeneratorVersion(result.stdout);
      } catch {
        version = null;
      }
    }
    probes.push({ id, found: bin !== null, bin, version, enabled: opts.enabled[id] === true });
  }
  return probes;
}
function destContractPrompt(userPrompt, destAbs, toolName) {
  return [
    `Generate exactly one image with the ${toolName} tool using this prompt:`,
    userPrompt,
    `Then copy or move the saved file to ${destAbs} so that path exists as a real image file.`,
    "Print DONE when that path exists. Edit no other files."
  ].join("\n");
}
async function isSniffedImage(path2) {
  try {
    const { readFile: readFile11 } = await import("fs/promises");
    const bytes = await readFile11(path2);
    return sniffImageFormat(bytes) !== null;
  } catch {
    return false;
  }
}
async function collectFiles(dir, acc) {
  let entries;
  try {
    entries = await readdir4(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    const full = join12(dir, entry.name);
    if (entry.isDirectory()) {
      await collectFiles(full, acc);
    } else if (entry.isFile()) {
      try {
        const st = await stat3(full);
        acc.push({ path: full, mtime: st.mtimeMs });
      } catch {
      }
    }
  }
}
async function harvestNewestImage(workdir, dest) {
  const files = [];
  await collectFiles(workdir, files);
  const images2 = [];
  for (const file of files) {
    if (file.path === dest) continue;
    if (await isSniffedImage(file.path)) images2.push(file);
  }
  images2.sort((a, b) => b.mtime - a.mtime);
  const newest = images2[0];
  if (!newest) return false;
  await copyFile2(newest.path, dest);
  return isSniffedImage(dest);
}
var WRITE_DENIED = /operation not permitted|FS_PERMISSION_DENIED|\bEPERM\b|\bEACCES\b|permission denied|read-only file system|\bEROFS\b/i;
var GeneratorWriteDenied = class extends PptwiseError {
  constructor(detail) {
    super(`refused a file write: ${detail}`);
    this.detail = detail;
  }
  detail;
};
function writeDeniedMessage(id, detail) {
  return `${id} could not write its own home folder, which this sandbox does not allow (${detail}). Run pptwise images generate outside the sandbox, or allow ${id} to write its home folder in the host's sandbox settings. Do not copy, move or redirect any of its login files to get around this.`;
}
async function settleDest(req, result) {
  if (await isSniffedImage(req.dest)) return;
  if (await harvestNewestImage(req.workdir, req.dest)) return;
  const detail = (result.stderr || result.stdout).trim().slice(0, 400);
  if (result.code !== 0 && WRITE_DENIED.test(detail)) throw new GeneratorWriteDenied(detail);
  throw new PptwiseError(
    result.code === 0 ? `produced no image file at ${req.dest}${detail ? `: ${detail}` : ""}` : `exited ${result.code}${detail ? `: ${detail}` : ""}`
  );
}
async function runGrokAdapter(req) {
  const result = await req.run({
    command: req.bin,
    args: [
      "-p",
      destContractPrompt(req.prompt, req.dest, "image_gen"),
      "--cwd",
      req.workdir,
      "--permission-mode",
      "bypassPermissions",
      "--max-turns",
      "12"
    ],
    cwd: req.workdir,
    timeoutMs: req.timeoutMs
  });
  await settleDest(req, result);
}
async function runCodexAdapter(req) {
  const result = await req.run({
    command: req.bin,
    args: [
      "exec",
      "--dangerously-bypass-approvals-and-sandbox",
      "--skip-git-repo-check",
      "--ephemeral",
      "-C",
      req.workdir,
      destContractPrompt(req.prompt, req.dest, "image_gen__imagegen")
    ],
    cwd: req.workdir,
    timeoutMs: req.timeoutMs
  });
  await settleDest(req, result);
}
async function runAntigravityAdapter(req) {
  const seconds = Math.max(1, Math.ceil(req.timeoutMs / 1e3));
  const result = await req.run({
    command: req.bin,
    args: [
      "-p",
      destContractPrompt(req.prompt, req.dest, "generate_image"),
      "--dangerously-skip-permissions",
      "--print-timeout",
      `${seconds}s`
    ],
    cwd: req.workdir,
    timeoutMs: req.timeoutMs
  });
  await settleDest(req, result);
}
var GENERATOR_ADAPTERS = {
  grok: runGrokAdapter,
  codex: runCodexAdapter,
  antigravity: runAntigravityAdapter
};

// src/cli/update.ts
var PACKAGE_NAME = "@liustack/pptwise";
function normalizeVersion(version) {
  const normalized = version.trim().replace(/^v/i, "").split("-")[0];
  if (!normalized) throw new Error(`invalid version: ${version}`);
  return normalized;
}
function parseVersion(version) {
  return normalizeVersion(version).split(".").map((segment) => {
    const value = Number.parseInt(segment, 10);
    if (!Number.isFinite(value)) throw new Error(`invalid version segment: ${segment}`);
    return value;
  });
}
function compareVersions(left, right) {
  const l = parseVersion(left);
  const r = parseVersion(right);
  for (let i = 0; i < Math.max(l.length, r.length); i++) {
    const a = l[i] ?? 0;
    const b = r[i] ?? 0;
    if (a !== b) return a < b ? -1 : 1;
  }
  return 0;
}
var runCommand = async (command, args) => {
  const { code, stdout, stderr } = await runChild(command, args);
  if (code !== 0) throw new Error(stderr.trim() || `exited ${code}`);
  return stdout.trim();
};
async function checkForUpdate({
  currentVersion,
  packageName = PACKAGE_NAME,
  run = runCommand
}) {
  const current = normalizeVersion(currentVersion);
  try {
    const latest = normalizeVersion(await run("npm", ["view", packageName, "version"]));
    return {
      packageName,
      currentVersion: current,
      latestVersion: latest,
      updateAvailable: compareVersions(current, latest) < 0,
      checked: true
    };
  } catch (error) {
    return {
      packageName,
      currentVersion: current,
      latestVersion: null,
      updateAvailable: false,
      checked: false,
      error: error instanceof Error ? error.message : String(error)
    };
  }
}
function createSelfUpdater(run = runCommand) {
  return async ({
    currentVersion,
    packageName = PACKAGE_NAME
  }) => {
    const info = await checkForUpdate({ currentVersion, packageName, run });
    if (!info.checked) throw new Error(`unable to check for updates: ${info.error ?? "unknown error"}`);
    if (!info.updateAvailable) return { ...info, updated: false };
    await run("npm", ["install", "-g", `${packageName}@latest`]);
    return { ...info, updated: true };
  };
}

// src/cli/doctor.ts
var MIN_NODE = "22.19";
var SKILL_DIR_NAME = "pptwise";
var LEGACY_SKILL_DIR_NAMES = ["pptpress", "pptfast"];
var SKILL_COPY_FILES = [
  "SKILL.md",
  "SKILL.zh-CN.md",
  "scripts/run.sh",
  "scripts/run.ps1",
  "references/spec.md",
  "references/spec.zh-CN.md",
  "references/layouts.md",
  "references/layouts.zh-CN.md",
  "references/components.md",
  "references/components.zh-CN.md",
  "references/density.md",
  "references/density.zh-CN.md",
  "references/branding.md",
  "references/branding.zh-CN.md",
  "references/images.md",
  "references/images.zh-CN.md",
  "references/validate.md",
  "references/validate.zh-CN.md"
];
var SKILL_ROOTS = [
  { harness: "Claude Code", relative: join13(".claude", "skills") },
  { harness: "Codex", relative: join13(".codex", "skills") },
  { harness: "Pi, OpenCode", relative: join13(".agents", "skills") }
];
var SELF_TEST_DECK = {
  version: "5",
  filename: "pptwise-doctor-self-test.pptx",
  theme: { id: "brief" },
  slides: [
    { type: "cover", heading: "pptwise doctor", subheading: "self-test render" },
    {
      type: "content",
      kind: "points",
      heading: "Core chain",
      components: [{ type: "bullets", items: ["validate the IR", "render a slide to SVG", "generate the .pptx bytes"] }]
    }
  ]
};
function readPinnedVersion(launcher) {
  return /^PINNED="([^"]+)"/m.exec(launcher)?.[1] ?? null;
}
function isOlder(version, current) {
  try {
    return compareVersions(version, current) < 0;
  } catch {
    return false;
  }
}
async function pathExists2(target) {
  try {
    await access(target);
    return true;
  } catch {
    return false;
  }
}
async function scanSkillCopies(home, currentVersion) {
  const scanned = [];
  const copies = [];
  for (const { harness, relative: relative4 } of SKILL_ROOTS) {
    const root = join13(home, relative4);
    scanned.push(root);
    for (const { dirName, legacy } of [
      { dirName: SKILL_DIR_NAME, legacy: false },
      ...LEGACY_SKILL_DIR_NAMES.map((dirName2) => ({ dirName: dirName2, legacy: true }))
    ]) {
      const copyDir = join13(root, dirName);
      if (!await pathExists2(copyDir)) continue;
      const launcherPath = join13(copyDir, "scripts", "run.sh");
      let pinned = null;
      let launcher = null;
      try {
        pinned = readPinnedVersion(await readFile8(launcherPath, "utf8"));
        launcher = launcherPath;
      } catch {
      }
      const missing = [];
      for (const rel of SKILL_COPY_FILES) {
        if (!await pathExists2(join13(copyDir, rel))) missing.push(rel);
      }
      copies.push({
        harness,
        root,
        path: copyDir,
        launcher,
        pinned,
        stale: legacy || pinned !== null && isOlder(pinned, currentVersion),
        missing,
        legacy
      });
    }
  }
  return { scanned, copies };
}
function installedPluginDir(profileDir) {
  return join13(profileDir, "node_modules", ...PACKAGE_NAME.split("/"));
}
async function readInstalledPluginVersion(profileDir) {
  const pkgPath = join13(installedPluginDir(profileDir), "package.json");
  try {
    const pkg = JSON.parse(await readFile8(pkgPath, "utf8"));
    return typeof pkg.version === "string" ? pkg.version : null;
  } catch {
    return null;
  }
}
async function inspectDsh(home, currentVersion) {
  const dshHome = join13(home, ".dsh");
  if (!await pathExists2(dshHome)) return { applicable: false, home: dshHome, profiles: [] };
  const profilesDir = join13(dshHome, "profiles");
  let entries;
  try {
    const dirents = await readdir5(profilesDir, { withFileTypes: true });
    entries = dirents.filter((d) => d.isDirectory() && d.name !== "node_modules").map((d) => d.name);
  } catch {
    return { applicable: true, home: dshHome, profiles: [] };
  }
  const profiles = [];
  for (const name of entries.sort()) {
    const profileDir = join13(profilesDir, name);
    let declared;
    try {
      const pkg = JSON.parse(await readFile8(join13(profileDir, "package.json"), "utf8"));
      declared = pkg.dependencies?.[PACKAGE_NAME];
    } catch {
      continue;
    }
    const installedVersion2 = await readInstalledPluginVersion(profileDir);
    const declaredVersion = typeof declared === "string" && /^\d+\.\d+\.\d+/.test(declared) ? declared.match(/^\d+\.\d+\.\d+/)[0] : null;
    const version = installedVersion2 ?? declaredVersion;
    const installed = installedVersion2 !== null || declared !== void 0;
    profiles.push({
      name,
      path: profileDir,
      installed,
      version,
      source: installedVersion2 !== null ? "node_modules" : declaredVersion !== null ? "package.json" : null,
      stale: installed && version !== null && isOlder(version, currentVersion),
      engineMissing: installedVersion2 !== null && !await pathExists2(join13(installedPluginDir(profileDir), "dist", "cli.js"))
    });
  }
  return { applicable: true, home: dshHome, profiles };
}
function dshInstallCommand(profile, version) {
  const spec2 = `${PACKAGE_NAME}@${version}`;
  if (profile === "desktop") {
    return `in DeepSeek Harness Desktop open Plugins, choose Add plugin and enter ${spec2} (or quit Desktop and run \`dsh plugin --profile desktop add ${spec2}\`)`;
  }
  return `npx -y @deepseek-ai/dsh plugin --profile ${profile} add ${spec2}`;
}
async function inspectCapabilities(env) {
  const capabilities = [];
  let sharpAvailable = false;
  let sharpError = null;
  try {
    await import("sharp");
    sharpAvailable = true;
  } catch (e) {
    sharpError = isMissingModuleError(e) ? "not installed" : e instanceof Error ? e.message : String(e);
  }
  capabilities.push({
    name: "sharp",
    available: sharpAvailable,
    detail: sharpAvailable ? "importable \u2014 preview rasterization and `audit --pixels` are available" : `${sharpError} \u2014 preview rasterization and \`audit --pixels\` are unavailable. Plain SVG preview and .pptx rendering are unaffected`,
    fix: sharpAvailable ? void 0 : "npm i sharp (optional dependency \u2014 install it only if you want the pixel checks)"
  });
  const soffice = await findOnPath("soffice", env);
  capabilities.push({
    name: "soffice",
    available: soffice !== null,
    detail: soffice !== null ? `found at ${soffice} \u2014 the PDF export path is available` : "not on PATH \u2014 the PDF export path is unavailable. Rendering and validating .pptx files are unaffected",
    fix: soffice !== null ? void 0 : "install LibreOffice (https://libreoffice.org) and make sure `soffice` is on PATH"
  });
  return capabilities;
}
function posixBitsApply() {
  return typeof process.getuid === "function";
}
async function inspectImages(env) {
  const configPath = userConfigPath();
  let configExists = false;
  let groupOrOtherReadable = false;
  try {
    const st = lstatSync2(configPath);
    configExists = true;
    if (posixBitsApply() && !st.isSymbolicLink()) {
      groupOrOtherReadable = (st.mode & 63) !== 0;
    }
  } catch {
    configExists = false;
  }
  let file = null;
  try {
    file = await findUserConfig();
  } catch {
    file = null;
  }
  const keys = resolveImageKeys({ file: file?.config ?? null, env });
  const providers = ["pexels", "pixabay"].map((provider) => ({
    provider,
    present: Boolean(keys[provider].apiKey),
    source: keys[provider].source
  }));
  providers.push({
    provider: "openverse",
    present: keys.openverse.ready,
    source: keys.openverse.ready ? keys.openverse.source : null
  });
  return { configPath, configExists, groupOrOtherReadable, providers };
}
async function inspectGenerators(env, run) {
  let file = null;
  try {
    file = await findUserConfig();
  } catch {
    file = null;
  }
  const flags = resolveGenerators({ file: file?.config ?? null });
  return probeGenerators({ env, run, enabled: flags.enabled });
}
async function runSelfTest() {
  const started = performance.now();
  const elapsed = () => Math.round(performance.now() - started);
  try {
    const v2 = validateIr(SELF_TEST_DECK);
    if (!v2.ok) throw new Error(`the built-in self-test deck failed validation:
${formatIssues(v2.errors)}`);
    const svg = renderSlideSvg(v2.ir, 0);
    if (!svg.includes("<svg")) throw new Error("the SVG renderer produced no <svg> element");
    const bytes = await generatePptx(v2.ir);
    if (bytes.length === 0) throw new Error("the PPTX generator produced zero bytes");
    return { ok: true, elapsedMs: elapsed(), slides: v2.ir.slides.length, bytes: bytes.length };
  } catch (e) {
    return {
      ok: false,
      elapsedMs: elapsed(),
      slides: SELF_TEST_DECK.slides.length,
      bytes: null,
      error: e instanceof Error ? e.message : String(e)
    };
  }
}
function skillRefreshCommand(copyDir) {
  return `rm -rf /tmp/pptwise-src && git clone --depth 1 https://github.com/liustack/pptwise.git /tmp/pptwise-src && cp -R /tmp/pptwise-src/skills/${SKILL_DIR_NAME}/. ${copyDir}/`;
}
async function buildDoctorReport(input = {}) {
  const version = input.version ?? VERSION;
  const home = input.home ?? homedir();
  const env = input.env ?? process.env;
  const nodeVersion = input.nodeVersion ?? process.version;
  const cwd = input.cwd ?? process.cwd();
  const [skills, dsh, capabilities, selfTest, projectHit, images2, generators] = await Promise.all([
    scanSkillCopies(home, version),
    inspectDsh(home, version),
    inspectCapabilities(env),
    runSelfTest(),
    findConfig(cwd),
    inspectImages(env),
    inspectGenerators(env, input.runProcess)
  ]);
  const workspace = await inspectWorkspace({
    cwd,
    projectConfigPath: projectHit?.path,
    runGit: input.runGit
  });
  let meetsMinimum = true;
  try {
    meetsMinimum = compareVersions(nodeVersion, MIN_NODE) >= 0;
  } catch {
    meetsMinimum = true;
  }
  const runtime = {
    node: nodeVersion,
    bun: process.versions.bun ?? null,
    minimum: MIN_NODE,
    meetsMinimum
  };
  const errors = [];
  const warnings = [];
  if (!runtime.meetsMinimum) {
    errors.push({
      check: "runtime",
      message: `Node ${runtime.node} is below the ${MIN_NODE} floor pptwise needs`,
      fix: `install Node ${MIN_NODE}+ from https://nodejs.org (or \`nvm install 22\`), open a new shell, then re-run \`pptwise doctor\``
    });
  }
  if (!selfTest.ok) {
    errors.push({
      check: "self-test",
      message: `the self-test render failed: ${selfTest.error}`,
      fix: `reinstall the CLI: npm install -g ${PACKAGE_NAME}`
    });
  }
  for (const copy of skills.copies) {
    if (copy.legacy) {
      warnings.push({
        check: "skill copy",
        message: `${copy.path} is a leftover ${basename6(copy.path)} skill copy`,
        fix: `remove it and install the pptwise skill in ${join13(copy.root, SKILL_DIR_NAME)}`
      });
    } else if (copy.stale) {
      warnings.push({
        check: "skill copy",
        message: `${copy.path} pins ${copy.pinned}, behind this CLI's ${version}`,
        fix: `re-run the install to overwrite the copy in place: ${skillRefreshCommand(copy.path)}`
      });
    } else if (copy.pinned === null) {
      warnings.push({
        check: "skill copy",
        message: `${copy.path} has ${copy.launcher === null ? "no scripts/run.sh" : "a scripts/run.sh with no PINNED line"} \u2014 version unknown, so drift cannot be ruled out`,
        fix: `re-run the install to restore a complete copy: ${skillRefreshCommand(copy.path)}`
      });
    }
    if (copy.missing.length > 0) {
      warnings.push({
        check: "skill copy",
        message: `${copy.path} is missing ${copy.missing.join(", ")}`,
        fix: `re-run the install to restore a complete copy: ${skillRefreshCommand(copy.path)}`
      });
    }
  }
  for (const profile of dsh.profiles) {
    if (profile.engineMissing) {
      warnings.push({
        check: "dsh plugin",
        message: `profile "${profile.name}" has ${PACKAGE_NAME} without its built engine (dist/cli.js), so it cannot make a deck. This is what adding it from the GitHub address leaves`,
        fix: `remove it, then add it by package name: ${dshInstallCommand(profile.name, version)}`
      });
    } else if (profile.stale) {
      warnings.push({
        check: "dsh plugin",
        message: `profile "${profile.name}" has ${PACKAGE_NAME} ${profile.version}, behind this CLI's ${version}`,
        fix: dshInstallCommand(profile.name, version)
      });
    }
  }
  for (const capability of capabilities) {
    if (!capability.available) {
      warnings.push({ check: "capability", message: `${capability.name}: ${capability.detail}`, fix: capability.fix });
    }
  }
  if (images2.groupOrOtherReadable) {
    warnings.push({
      check: "images",
      message: `${images2.configPath} is group/other-readable \u2014 API keys should be mode 0600`,
      fix: `chmod 600 ${images2.configPath}`
    });
  }
  return { version, runtime, skills, dsh, capabilities, selfTest, workspace, images: images2, generators, errors, warnings };
}
function mark(state) {
  return state === "ok" ? "[ok]" : state === "warn" ? "[!]" : state === "fail" ? "[!!]" : "[-]";
}
function renderDoctorReport(report) {
  const lines = [];
  lines.push(`pptwise doctor \u2014 CLI ${report.version}`);
  lines.push("(local diagnostics only: nothing is written, no network call is made)");
  lines.push("");
  lines.push("Installed skill copies (a copy keeps its install-time version forever)");
  if (report.skills.copies.length === 0) {
    lines.push("  [-] no installed skill copy found \u2014 the CLI runs fine on its own, and dsh ships the");
    lines.push("      skill inside the plugin instead");
    lines.push(`      looked in: ${report.skills.scanned.join(", ")}`);
  } else {
    for (const copy of report.skills.copies) {
      const state = copy.legacy || copy.stale || copy.pinned === null || copy.missing.length > 0 ? "warn" : "ok";
      const pin = copy.legacy ? `leftover ${basename6(copy.path)} copy` : copy.pinned === null ? "version unknown" : `pins ${copy.pinned}`;
      lines.push(`  ${mark(state)} ${copy.harness}: ${copy.path} \u2014 ${pin}${copy.stale && !copy.legacy ? " (stale)" : ""}`);
      if (copy.legacy) {
        lines.push(`      fix: remove it and install the pptwise skill in ${join13(copy.root, SKILL_DIR_NAME)}`);
      } else if (copy.stale) {
        lines.push(`      fix: ${skillRefreshCommand(copy.path)}`);
      } else if (copy.pinned === null) {
        lines.push(`      ${copy.launcher === null ? "no scripts/run.sh in this copy" : "scripts/run.sh carries no PINNED line"}`);
        lines.push(`      fix: ${skillRefreshCommand(copy.path)}`);
      }
      if (copy.missing.length > 0) {
        lines.push(`      missing: ${copy.missing.join(", ")}`);
        lines.push(`      fix: ${skillRefreshCommand(copy.path)}`);
      }
    }
  }
  lines.push("");
  lines.push("DSH plugin");
  if (!report.dsh.applicable) {
    lines.push(`  ${mark("n/a")} no ${report.dsh.home} \u2014 not a dsh machine, this check does not apply`);
  } else if (report.dsh.profiles.length === 0) {
    lines.push(`  ${mark("n/a")} ${report.dsh.home} exists but has no profiles to inspect`);
  } else {
    for (const profile of report.dsh.profiles) {
      if (!profile.installed) {
        lines.push(`  ${mark("n/a")} ${profile.name}: ${PACKAGE_NAME} not installed in this profile`);
        continue;
      }
      const version = profile.version ?? "version unknown";
      if (profile.engineMissing) {
        lines.push(`  ${mark("warn")} ${profile.name}: ${version} (no built engine, cannot make a deck)`);
        lines.push(`      fix: remove it, then add it by package name: ${dshInstallCommand(profile.name, report.version)}`);
        continue;
      }
      lines.push(`  ${mark(profile.stale ? "warn" : "ok")} ${profile.name}: ${version}${profile.source ? ` (via ${profile.source})` : ""}${profile.stale ? " (behind this CLI)" : ""}`);
      if (profile.stale) {
        lines.push(`      fix: ${dshInstallCommand(profile.name, report.version)}`);
      }
    }
  }
  lines.push("");
  lines.push("Runtime");
  lines.push(`  ${mark(report.runtime.meetsMinimum ? "ok" : "fail")} Node ${report.runtime.node} (minimum ${report.runtime.minimum})`);
  if (report.runtime.bun !== null) {
    lines.push(`  ${mark("ok")} running under Bun ${report.runtime.bun}`);
  }
  lines.push("");
  lines.push("Optional capabilities (neither is needed by the main flow)");
  for (const capability of report.capabilities) {
    lines.push(`  ${mark(capability.available ? "ok" : "warn")} ${capability.name}: ${capability.detail}`);
    if (capability.fix) lines.push(`      fix: ${capability.fix}`);
  }
  lines.push("");
  lines.push("Self-test render (a built-in deck through the real pipeline, in memory)");
  lines.push(
    report.selfTest.ok ? `  ${mark("ok")} ${report.selfTest.slides} slides validated, rendered, and packed into ${report.selfTest.bytes} bytes in ${report.selfTest.elapsedMs}ms` : `  ${mark("fail")} failed after ${report.selfTest.elapsedMs}ms: ${report.selfTest.error}`
  );
  lines.push("");
  lines.push("Workspace artifacts (where render/preview write when -o is omitted)");
  lines.push(`  ${mark("ok")} anchor ${report.workspace.anchor}`);
  lines.push(`  ${mark("ok")} output ${report.workspace.root}`);
  if (report.workspace.ignore === "ignored") {
    lines.push(`  ${mark("ok")} git-ignored`);
  } else if (report.workspace.ignore === "not-ignored") {
    lines.push(`  ${mark("n/a")} not git-ignored \u2014 the first render will write .pptwise/.gitignore and a local exclude line`);
  } else {
    lines.push(`  ${mark("n/a")} not a git repository`);
  }
  lines.push("");
  lines.push("Images (optional stock-photo search \u2014 rendering PPTX still needs no credentials)");
  lines.push(`  ${mark("ok")} config ${report.images.configPath}${report.images.configExists ? "" : " (missing)"}`);
  if (report.images.groupOrOtherReadable) {
    lines.push(`  ${mark("warn")} file is group/other-readable \u2014 chmod 600`);
  }
  for (const provider of report.images.providers) {
    if (provider.present) {
      lines.push(`  ${mark("ok")} ${provider.provider}: present (${provider.source})`);
    } else if (provider.provider === "openverse") {
      lines.push(`  ${mark("n/a")} openverse: missing \u2014 pptwise config set openverse.clientId`);
    } else {
      lines.push(`  ${mark("n/a")} ${provider.provider}: missing \u2014 pptwise config set ${provider.provider}.apiKey`);
    }
  }
  lines.push("");
  lines.push("Image generators (optional, off until enabled)");
  for (const gen of report.generators) {
    if (!gen.found) {
      lines.push(`  ${mark("n/a")} ${gen.id}: not found`);
      continue;
    }
    const ver = gen.version ? `, ${gen.version}` : "";
    const state = gen.enabled ? "enabled" : "disabled";
    const hint = gen.enabled ? "" : ` \u2014 pptwise config set images.generators.${gen.id}.enabled true`;
    lines.push(`  ${mark("ok")} ${gen.id}: found (${gen.bin}${ver}) ${state}${hint}`);
  }
  lines.push("");
  lines.push(
    `${report.errors.length} error${report.errors.length === 1 ? "" : "s"}, ${report.warnings.length} warning${report.warnings.length === 1 ? "" : "s"}`
  );
  for (const error of report.errors) {
    lines.push(`  [!!] ${error.check}: ${error.message}`);
    if (error.fix) lines.push(`       fix: ${error.fix}`);
  }
  for (const warning of report.warnings) {
    lines.push(`  [!] ${warning.check}: ${warning.message}`);
  }
  if (report.errors.length === 0) {
    lines.push(report.warnings.length === 0 ? "pptwise is healthy on this machine" : "nothing blocking \u2014 the warnings above are worth fixing when convenient");
  }
  return lines.join("\n");
}
async function runDoctor(opts = {}) {
  const report = await buildDoctorReport(opts);
  return {
    output: opts.json ? JSON.stringify(report, null, 2) : renderDoctorReport(report),
    hasErrors: report.errors.length > 0
  };
}

// src/cli/images.ts
import { mkdir as mkdir7, mkdtemp, readFile as readFile9, readdir as readdir6, rename as rename2, rm as rm4, unlink as unlink2, writeFile as writeFile8 } from "fs/promises";
import { tmpdir } from "os";
import { join as join14, resolve as resolve8 } from "path";

// src/cli/redact.ts
var KEY_QUERY = /([?&](?:api_)?key=)[^&\s"'<>]*/gi;
var CLIENT_SECRET_QUERY = /(client_secret=)[^&\s"'<>]*/gi;
function redactSecrets(text, knownSecrets = []) {
  let out = text;
  const secrets = knownSecrets.filter((s) => s.length >= 6).sort((a, b) => b.length - a.length);
  for (const secret of secrets) {
    out = out.split(secret).join("[redacted]");
  }
  out = out.replace(KEY_QUERY, "$1[redacted]");
  out = out.replace(CLIENT_SECRET_QUERY, "$1[redacted]");
  return out;
}

// src/cli/image-openverse.ts
var OPENVERSE_SEARCH_URL = "https://api.openverse.org/v1/images/";
var OPENVERSE_TOKEN_URL = "https://api.openverse.org/v1/auth_tokens/token/";
var OPENVERSE_PAGE_SIZE = 8;
var TOKEN_SKEW_MS = 3e4;
var defaultSleep = (ms) => new Promise((resolve11) => setTimeout(resolve11, ms));
var tokenCache = /* @__PURE__ */ new Map();
function userAgent() {
  return `pptwise/${VERSION} (+https://pptwise.com)`;
}
function asRecord(value) {
  if (typeof value === "object" && value !== null && !Array.isArray(value)) {
    return value;
  }
  return null;
}
function asString(value) {
  return typeof value === "string" && value !== "" ? value : void 0;
}
function asNumber(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : void 0;
}
function isCc0OrPdm(license2) {
  const token = (license2 ?? "").toLowerCase();
  return token === "cc0" || token === "pdm";
}
function retryDelayMs(res, attempt) {
  const raw = res.headers.get("Retry-After");
  if (raw !== null && raw !== "") {
    const seconds = Number(raw);
    if (Number.isFinite(seconds) && seconds >= 0) return Math.round(seconds * 1e3);
  }
  return attempt === 0 ? 500 : 1500;
}
async function fetchOpenverseJson(url, init, fetchImpl, secrets, sleep) {
  let attempt = 0;
  while (true) {
    let res;
    try {
      res = await fetchImpl(url, init);
    } catch (e) {
      throw new PptwiseError(
        redactSecrets(`stock image request failed: ${e instanceof Error ? e.message : String(e)}`, secrets)
      );
    }
    const text = await res.text();
    if (res.status === 429) {
      if (attempt >= 2) {
        throw new PptwiseError(
          `stock image API rate-limited (HTTP 429): ${redactSecrets(text.slice(0, 800), secrets)}`
        );
      }
      await sleep(retryDelayMs(res, attempt));
      attempt += 1;
      continue;
    }
    if (!res.ok) {
      throw new PptwiseError(`stock image API HTTP ${res.status}: ${redactSecrets(text.slice(0, 800), secrets)}`);
    }
    try {
      return JSON.parse(text);
    } catch {
      throw new PptwiseError(`stock image API returned non-JSON (HTTP ${res.status})`);
    }
  }
}
async function getOpenverseAccessToken(clientId, clientSecret, fetchImpl, secrets, sleep, now = Date.now) {
  const cached = tokenCache.get(clientId);
  if (cached && now() < cached.expiresAt - TOKEN_SKEW_MS) return cached.accessToken;
  const body = new URLSearchParams({
    grant_type: "client_credentials",
    client_id: clientId,
    client_secret: clientSecret
  }).toString();
  const json = await fetchOpenverseJson(
    OPENVERSE_TOKEN_URL,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": userAgent()
      },
      body
    },
    fetchImpl,
    secrets,
    sleep
  );
  const rec = asRecord(json);
  const accessToken = asString(rec?.access_token);
  const expiresIn = asNumber(rec?.expires_in) ?? 3600;
  if (!accessToken) throw new PptwiseError("Openverse token response was missing access_token");
  tokenCache.set(clientId, { accessToken, expiresAt: now() + expiresIn * 1e3 });
  return accessToken;
}
async function authHeaders(creds, fetchImpl, secrets, sleep) {
  const headers = { "User-Agent": userAgent() };
  if (creds.clientId && creds.clientSecret) {
    const token = await getOpenverseAccessToken(creds.clientId, creds.clientSecret, fetchImpl, secrets, sleep);
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}
function parseHit(raw) {
  const photo = asRecord(raw);
  if (!photo) return null;
  const id = asString(photo.id);
  const url = asString(photo.url);
  if (!id || !url) return null;
  const license2 = (asString(photo.license) ?? "").toLowerCase();
  if (!isCc0OrPdm(license2)) return null;
  const source = asString(photo.source) ?? asString(photo.provider) ?? "openverse";
  return {
    id,
    url,
    foreignLandingUrl: asString(photo.foreign_landing_url) ?? "",
    creator: asString(photo.creator) ?? "unknown",
    license: license2,
    attribution: asString(photo.attribution) ?? "",
    source,
    width: asNumber(photo.width) ?? 0,
    height: asNumber(photo.height) ?? 0,
    thumbnail: asString(photo.thumbnail) ?? ""
  };
}
function matchesOrientation(hit, orientation) {
  if (!orientation) return true;
  if (orientation === "landscape") return hit.width > hit.height;
  if (orientation === "portrait") return hit.height > hit.width;
  return hit.width === hit.height;
}
async function searchOpenverse(opts) {
  const url = new URL(OPENVERSE_SEARCH_URL);
  url.searchParams.set("q", opts.query);
  url.searchParams.set("license_type", "commercial");
  url.searchParams.set("license", "cc0,pdm");
  url.searchParams.set("page_size", String(OPENVERSE_PAGE_SIZE));
  const headers = await authHeaders(
    { clientId: opts.clientId, clientSecret: opts.clientSecret },
    opts.fetch,
    opts.secrets,
    opts.sleep
  );
  const json = await fetchOpenverseJson(url.toString(), { headers }, opts.fetch, opts.secrets, opts.sleep);
  const root = asRecord(json);
  const list = Array.isArray(root?.results) ? root.results : [];
  const hits = [];
  for (const raw of list) {
    const hit = parseHit(raw);
    if (!hit) continue;
    if (opts.minWidth !== void 0 && hit.width < opts.minWidth) continue;
    if (opts.minHeight !== void 0 && hit.height < opts.minHeight) continue;
    if (!matchesOrientation(hit, opts.orientation)) continue;
    hits.push(hit);
    if (hits.length >= OPENVERSE_PAGE_SIZE) break;
  }
  return hits;
}
async function loadOpenverseDetail(id, creds, fetchImpl, secrets, sleep) {
  const url = `${OPENVERSE_SEARCH_URL}${encodeURIComponent(id)}/`;
  const headers = await authHeaders(creds, fetchImpl, secrets, sleep);
  const json = await fetchOpenverseJson(url, { headers }, fetchImpl, secrets, sleep);
  const license2 = asString(asRecord(json)?.license);
  if (!isCc0OrPdm(license2)) {
    throw new PptwiseError(
      `Openverse photo ${id} is licensed "${license2 ?? "unknown"}", not cc0/pdm \u2014 refusing to download`
    );
  }
  const hit = parseHit(json);
  if (!hit) throw new PptwiseError(`Openverse photo ${id} was not found`);
  return hit;
}

// src/cli/ssrf.ts
import { lookup as dnsLookup } from "dns/promises";
import { isIP } from "net";
import { Agent, fetch as undiciFetch } from "undici";
async function defaultDnsLookup(hostname) {
  return dnsLookup(hostname, { all: true, verbatim: true });
}
var BLOCKED_HOSTNAMES = /* @__PURE__ */ new Set([
  "localhost",
  "localhost.localdomain",
  "metadata.google.internal",
  "metadata.amazonaws.com",
  "metadata.azure.internal"
]);
function isBlockedHostname(hostname) {
  const normalized = hostname.trim().toLowerCase();
  if (!normalized) return true;
  if (BLOCKED_HOSTNAMES.has(normalized)) return true;
  if (normalized.endsWith(".localhost")) return true;
  return false;
}
function isPrivateIpAddress(ipAddress) {
  const normalized = ipAddress.trim().toLowerCase();
  const family = isIP(normalized);
  if (family === 4) return isPrivateIPv4(normalized);
  if (family === 6) return isPrivateIPv6(normalized);
  return true;
}
async function assertSafeRemoteTarget(url, lookup) {
  if (isBlockedHostname(url.hostname)) {
    throw new Error(blockedMessage(url.hostname));
  }
  const hostname = stripIpv6Brackets(url.hostname);
  const ipFamily = isIP(hostname);
  if (ipFamily > 0) {
    if (isPrivateIpAddress(hostname)) throw new Error(blockedMessage(hostname));
    return { hostname, address: hostname, family: ipFamily };
  }
  if (!lookup) return { hostname, address: hostname, family: 0 };
  let resolved;
  try {
    resolved = await lookup(hostname);
  } catch (error) {
    throw new Error(
      `DNS lookup failed for host ${hostname}: ${error instanceof Error ? error.message : String(error)}`
    );
  }
  if (resolved.length === 0) {
    throw new Error(`Host ${hostname} did not resolve to any IP address.`);
  }
  const blocked = resolved.find((record) => isPrivateIpAddress(record.address));
  if (blocked) throw new Error(blockedMessage(`${hostname} -> ${blocked.address}`));
  const [chosen] = resolved;
  return { hostname, address: chosen.address, family: chosen.family };
}
async function pinnedFetch(url, pin, init) {
  const dispatcher = new Agent({
    connect: {
      lookup: (_hostname, options, callback) => {
        const record = { address: pin.address, family: pin.family };
        if (options?.all) callback(null, [record]);
        else callback(null, pin.address, pin.family);
      }
    }
  });
  try {
    const response = await undiciFetch(url, {
      ...init,
      dispatcher
    });
    const buffered = Buffer.from(await response.arrayBuffer());
    await dispatcher.close();
    return new Response(buffered, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers
    });
  } catch (error) {
    await dispatcher.close().catch(() => {
    });
    throw error;
  }
}
function blockedMessage(target) {
  return `Blocked private or reserved download target: ${target}. pptwise does not download from private addresses.`;
}
function stripIpv6Brackets(hostname) {
  if (hostname.startsWith("[") && hostname.endsWith("]")) return hostname.slice(1, -1);
  return hostname;
}
function isPrivateIPv4(ipAddress) {
  const octets = ipAddress.split(".").map((part) => Number.parseInt(part, 10));
  if (octets.length !== 4 || octets.some((value2) => !Number.isFinite(value2) || value2 < 0 || value2 > 255)) {
    return true;
  }
  const value = octets[0] * 256 ** 3 + octets[1] * 256 ** 2 + octets[2] * 256 + octets[3];
  return inRange(value, "0.0.0.0", "0.255.255.255") || inRange(value, "10.0.0.0", "10.255.255.255") || inRange(value, "100.64.0.0", "100.127.255.255") || inRange(value, "127.0.0.0", "127.255.255.255") || inRange(value, "169.254.0.0", "169.254.255.255") || inRange(value, "172.16.0.0", "172.31.255.255") || inRange(value, "192.0.0.0", "192.0.0.255") || inRange(value, "192.168.0.0", "192.168.255.255") || inRange(value, "198.18.0.0", "198.19.255.255") || inRange(value, "224.0.0.0", "255.255.255.255");
}
function inRange(value, start, end) {
  return value >= ipv4ToNumber(start) && value <= ipv4ToNumber(end);
}
function ipv4ToNumber(ipAddress) {
  const octets = ipAddress.split(".").map((part) => Number.parseInt(part, 10));
  return octets[0] * 256 ** 3 + octets[1] * 256 ** 2 + octets[2] * 256 + octets[3];
}
function isPrivateIPv6(ipAddress) {
  const groups = expandIpv6(ipAddress);
  if (groups !== null && hasMappedV4Prefix(groups)) {
    const mapped2 = [groups[6] >> 8, groups[6] & 255, groups[7] >> 8, groups[7] & 255].join(".");
    return isPrivateIPv4(mapped2);
  }
  const normalized = ipAddress.split("%")[0];
  const mapped = extractMappedIpv4(normalized);
  if (mapped && isPrivateIPv4(mapped)) return true;
  const value = ipv6ToBigInt(normalized);
  if (value === null) return true;
  return inIpv6Range(value, "::", 128) || inIpv6Range(value, "::1", 128) || inIpv6Range(value, "fc00::", 7) || inIpv6Range(value, "fe80::", 10) || inIpv6Range(value, "ff00::", 8) || inIpv6Range(value, "2001:db8::", 32);
}
function hasMappedV4Prefix(groups) {
  return groups.slice(0, 5).every((group) => group === 0) && groups[5] === 65535;
}
function extractMappedIpv4(ipAddress) {
  const lower = ipAddress.toLowerCase();
  const marker = "::ffff:";
  if (!lower.startsWith(marker)) return null;
  const candidate = lower.slice(marker.length);
  return isIP(candidate) === 4 ? candidate : null;
}
function inIpv6Range(value, start, prefixLength) {
  const startValue = ipv6ToBigInt(start);
  if (startValue === null) return false;
  const mask = prefixLength === 0 ? 0n : (1n << BigInt(prefixLength)) - 1n << BigInt(128 - prefixLength);
  return (value & mask) === (startValue & mask);
}
function ipv6ToBigInt(ipAddress) {
  const expanded = expandIpv6(ipAddress);
  if (!expanded) return null;
  return expanded.reduce((acc, group) => (acc << 16n) + BigInt(group), 0n);
}
function expandIpv6(ipAddress) {
  const value = ipAddress.toLowerCase();
  if (value.includes("::")) {
    const [left, right] = value.split("::");
    const leftGroups = left ? left.split(":").filter(Boolean) : [];
    const rightGroups = right ? right.split(":").filter(Boolean) : [];
    if (leftGroups.length + rightGroups.length > 8) return null;
    const middle = new Array(8 - leftGroups.length - rightGroups.length).fill("0");
    return parseIpv6Groups([...leftGroups, ...middle, ...rightGroups]);
  }
  return parseIpv6Groups(value.split(":"));
}
function parseIpv6Groups(groups) {
  if (groups.length !== 8) return null;
  const parsed = groups.map((group) => Number.parseInt(group || "0", 16));
  if (parsed.some((value) => !Number.isFinite(value) || value < 0 || value > 65535)) return null;
  return parsed;
}

// src/cli/images.ts
var BYTE_CAP = 15 * 1024 * 1024;
var MAX_LONG_EDGE = 1920;
var PER_PAGE = 8;
function userAgent2() {
  return `pptwise/${VERSION} (+https://pptwise.com)`;
}
function asRecord2(value) {
  if (typeof value === "object" && value !== null && !Array.isArray(value)) {
    return value;
  }
  return null;
}
function asString2(value) {
  return typeof value === "string" && value !== "" ? value : void 0;
}
function asNumber2(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : void 0;
}
async function loadKeys(env) {
  const hit = await findUserConfig();
  return resolveImageKeys({ file: hit?.config ?? null, env });
}
async function fetchJson(url, init, fetchImpl, secrets) {
  let res;
  try {
    res = await fetchImpl(url, init);
  } catch (e) {
    throw new PptwiseError(
      redactSecrets(`stock image request failed: ${e instanceof Error ? e.message : String(e)}`, secrets)
    );
  }
  const text = await res.text();
  const redacted = redactSecrets(text.slice(0, 800), secrets);
  if (!res.ok) {
    if (res.status === 429) {
      throw new PptwiseError(`stock image API rate-limited (HTTP 429): ${redacted}`);
    }
    throw new PptwiseError(`stock image API HTTP ${res.status}: ${redacted}`);
  }
  try {
    return JSON.parse(text);
  } catch {
    throw new PptwiseError(`stock image API returned non-JSON (HTTP ${res.status})`);
  }
}
function pexelsHeaders(apiKey) {
  return { Authorization: apiKey, "User-Agent": userAgent2() };
}
var ORIENTATIONS = /* @__PURE__ */ new Set(["landscape", "portrait", "square"]);
function parseOrientation(raw) {
  if (raw === void 0 || raw === "") return void 0;
  if (!ORIENTATIONS.has(raw)) {
    throw new PptwiseError(`invalid --orientation "${raw}" \u2014 expected landscape, portrait, or square`);
  }
  return raw;
}
function clientFilter(hits, minWidth, minHeight) {
  return hits.filter((hit) => {
    if (minWidth !== void 0 && hit.width < minWidth) return false;
    if (minHeight !== void 0 && hit.height < minHeight) return false;
    return true;
  });
}
function parsePexelsPhotos(json) {
  const root = asRecord2(json);
  const photos = Array.isArray(root?.photos) ? root.photos : [];
  const hits = [];
  for (const raw of photos) {
    const photo = asRecord2(raw);
    if (!photo) continue;
    const id = photo.id;
    const photoId = typeof id === "number" || typeof id === "string" ? String(id) : "";
    if (!photoId) continue;
    const src = asRecord2(photo.src) ?? {};
    const author = asString2(photo.photographer) ?? "unknown";
    const pageUrl = asString2(photo.url) ?? `https://www.pexels.com/photo/${photoId}/`;
    hits.push({
      id: `pexels:${photoId}`,
      provider: "pexels",
      photoId,
      thumb: asString2(src.medium) ?? asString2(src.tiny) ?? "",
      width: asNumber2(photo.width) ?? 0,
      height: asNumber2(photo.height) ?? 0,
      author,
      license: "Pexels License",
      pageUrl,
      attribution: `Photo by ${author} on Pexels`
    });
  }
  return hits.slice(0, PER_PAGE);
}
function parsePixabayHits(json) {
  const root = asRecord2(json);
  const list = Array.isArray(root?.hits) ? root.hits : [];
  const hits = [];
  for (const raw of list) {
    const photo = asRecord2(raw);
    if (!photo) continue;
    const photoId = photo.id !== void 0 ? String(photo.id) : "";
    if (!photoId) continue;
    const author = asString2(photo.user) ?? "unknown";
    const pageUrl = asString2(photo.pageURL) ?? `https://pixabay.com/photos/${photoId}/`;
    hits.push({
      id: `pixabay:${photoId}`,
      provider: "pixabay",
      photoId,
      thumb: asString2(photo.previewURL) ?? "",
      width: asNumber2(photo.imageWidth) ?? 0,
      height: asNumber2(photo.imageHeight) ?? 0,
      author,
      license: "Pixabay License",
      pageUrl,
      attribution: `Photo by ${author} on Pixabay`
    });
  }
  return hits.slice(0, PER_PAGE);
}
async function searchPexels(query, apiKey, opts, fetchImpl, secrets) {
  const url = new URL("https://api.pexels.com/v1/search");
  url.searchParams.set("query", query);
  url.searchParams.set("locale", "zh-CN");
  url.searchParams.set("per_page", String(PER_PAGE));
  const orientation = parseOrientation(opts.orientation);
  if (orientation) url.searchParams.set("orientation", orientation);
  if (opts.color) url.searchParams.set("color", opts.color);
  const json = await fetchJson(url.toString(), { headers: pexelsHeaders(apiKey) }, fetchImpl, secrets);
  return clientFilter(parsePexelsPhotos(json), opts.minWidth, opts.minHeight);
}
function pixabayOrientation(orientation) {
  if (orientation === "landscape") return "horizontal";
  if (orientation === "portrait") return "vertical";
  return void 0;
}
async function searchPixabay(query, apiKey, opts, fetchImpl, secrets) {
  const url = new URL("https://pixabay.com/api/");
  url.searchParams.set("key", apiKey);
  url.searchParams.set("q", query.slice(0, 100));
  url.searchParams.set("lang", "zh");
  url.searchParams.set("per_page", String(PER_PAGE));
  url.searchParams.set("safesearch", "true");
  const mapped = pixabayOrientation(parseOrientation(opts.orientation));
  if (mapped) url.searchParams.set("orientation", mapped);
  if (opts.color) url.searchParams.set("colors", opts.color);
  if (opts.minWidth !== void 0) url.searchParams.set("min_width", String(opts.minWidth));
  if (opts.minHeight !== void 0) url.searchParams.set("min_height", String(opts.minHeight));
  const json = await fetchJson(url.toString(), { headers: { "User-Agent": userAgent2() } }, fetchImpl, secrets);
  return parsePixabayHits(json);
}
function formatHits(hits) {
  return hits.map((hit) => {
    const thumb = hit.thumb ? `
  ${hit.thumb}` : "";
    const source = hit.source ? `  ${hit.source}` : "";
    return `${hit.id}  ${hit.width}x${hit.height}  ${hit.author}  ${hit.license}${source}${thumb}
  ${hit.attribution}
  ${hit.pageUrl}`;
  }).join("\n");
}
function openverseNotes(anonymous, pixabaySkipped) {
  const lines = ["Openverse does not verify individual licenses. Results are filtered to cc0/pdm."];
  if (anonymous) {
    lines.push(
      "Anonymous Openverse quota is very low. Set credentials with `pptwise config set openverse.clientId` and `pptwise config set openverse.clientSecret`."
    );
  }
  if (pixabaySkipped) {
    lines.push("Pixabay is unconfigured \u2014 pptwise config set pixabay.apiKey");
  }
  return lines;
}
async function runImagesSearch(query, opts = {}) {
  const q = query.trim();
  if (q === "") throw new PptwiseError("search query must not be empty");
  const env = opts.env ?? process.env;
  const keys = await loadKeys(env);
  const secrets = knownSecretsFrom(keys);
  const fetchImpl = opts.fetch ?? proxyFetch;
  const sleep = opts.sleep ?? defaultSleep;
  if (keys.pexels.apiKey) {
    const pexelsHits = await searchPexels(q, keys.pexels.apiKey, opts, fetchImpl, secrets);
    if (pexelsHits.length > 0) return formatHits(pexelsHits);
  }
  if (keys.pixabay.apiKey) {
    const pixabayHits = await searchPixabay(q, keys.pixabay.apiKey, opts, fetchImpl, secrets);
    if (pixabayHits.length > 0) return formatHits(pixabayHits);
  }
  const orientation = parseOrientation(opts.orientation);
  const ovHits = await searchOpenverse({
    query: q,
    orientation,
    minWidth: opts.minWidth,
    minHeight: opts.minHeight,
    clientId: keys.openverse.ready ? keys.openverse.clientId : void 0,
    clientSecret: keys.openverse.ready ? keys.openverse.clientSecret : void 0,
    fetch: fetchImpl,
    secrets,
    sleep
  });
  const notes = openverseNotes(!keys.openverse.ready, !keys.pixabay.apiKey);
  if (ovHits.length === 0) {
    return ["No photos found.", ...notes].join("\n");
  }
  const hits = ovHits.map((hit) => ({
    id: `openverse:${hit.id}`,
    provider: "openverse",
    photoId: hit.id,
    thumb: hit.thumbnail,
    width: hit.width,
    height: hit.height,
    author: hit.creator,
    license: hit.license,
    pageUrl: hit.foreignLandingUrl,
    attribution: hit.attribution,
    source: hit.source
  }));
  return [...notes, formatHits(hits)].join("\n");
}
function parsePhotoRef(ref) {
  const m = /^(pexels|pixabay|openverse):(.+)$/.exec(ref.trim());
  if (!m) {
    throw new PptwiseError(`invalid photo ref "${ref}" \u2014 expected pexels:<id>, pixabay:<id>, or openverse:<id>`);
  }
  const photoId = m[2].trim();
  if (photoId === "" || photoId.includes("/") || photoId.includes("\\") || photoId.includes("..")) {
    throw new PptwiseError(`invalid photo id in "${ref}"`);
  }
  return { provider: m[1], photoId };
}
async function resolveImageHome(deckArg, cwd) {
  const { location, isDir, target } = await resolveDeckWorkspace(deckArg, cwd);
  const workspace = join14(location.dir, ASSETS_DIRNAME);
  if (!isDir) return { assetsDir: workspace };
  return { assetsDir: join14(resolve8(target), ASSETS_DIRNAME), earlier: workspace };
}
async function resolveDeckWorkspace(deckArg, cwd) {
  const projectHit = await findConfig(cwd);
  const target = await resolveDeckTarget(deckArg, cwd);
  const isDir = await isDeckDirectory(target);
  const location = resolveWorkspaceLocation({
    cwd,
    projectConfigPath: projectHit?.path,
    target,
    isDir
  });
  return { location, isDir, target };
}
function assertSafeDownloadUrl(url) {
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    throw new PptwiseError("invalid download URL");
  }
  if (parsed.protocol !== "https:") {
    throw new PptwiseError("refusing non-HTTPS download URL");
  }
  if (parsed.username !== "" || parsed.password !== "") {
    throw new PptwiseError("refusing download URL with embedded userinfo");
  }
  return parsed;
}
async function downloadBytes(url, fetchImpl, secrets, lookup) {
  const parsed = assertSafeDownloadUrl(url);
  let pin;
  try {
    pin = await assertSafeRemoteTarget(parsed, lookup);
  } catch (e) {
    throw new PptwiseError(redactSecrets(e instanceof Error ? e.message : String(e), secrets));
  }
  let res;
  try {
    const init = { headers: { "User-Agent": userAgent2() } };
    res = fetchImpl ? await fetchImpl(parsed.toString(), init) : await pinnedFetch(parsed, pin, init);
  } catch (e) {
    throw new PptwiseError(
      redactSecrets(`download failed: ${e instanceof Error ? e.message : String(e)}`, secrets)
    );
  }
  if (!res.ok) {
    throw new PptwiseError(`download HTTP ${res.status}`);
  }
  const declared = Number(res.headers.get("content-length") ?? "0");
  if (declared > BYTE_CAP) {
    throw new PptwiseError(`download exceeds the ${BYTE_CAP} byte cap`);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.byteLength > BYTE_CAP) {
    throw new PptwiseError(`download exceeds the ${BYTE_CAP} byte cap`);
  }
  return buf;
}
async function defaultResizeToJpeg(bytes, maxLongEdge) {
  let sharpMod;
  try {
    sharpMod = (await import("sharp")).default;
  } catch (e) {
    if (isMissingModuleError(e)) {
      throw new PptwiseError(`Resizing stock photos requires the optional dependency "sharp" (npm i sharp)`);
    }
    throw e;
  }
  const image = sharpMod(bytes);
  const meta = await image.metadata();
  const width = meta.width ?? 0;
  const height = meta.height ?? 0;
  const long = Math.max(width, height);
  const pipeline = long > maxLongEdge ? width >= height ? image.resize({ width: maxLongEdge }) : image.resize({ height: maxLongEdge }) : image;
  return pipeline.jpeg({ quality: 85 }).toBuffer();
}
async function toJpeg(bytes, apiLongEdge, resize) {
  const format = sniffImageFormat(bytes);
  if (format === null) {
    throw new PptwiseError("downloaded bytes are not a recognized image (png/jpeg/gif/webp)");
  }
  if (format === "jpeg" && apiLongEdge !== void 0 && apiLongEdge <= MAX_LONG_EDGE) {
    return bytes;
  }
  return resize(bytes, MAX_LONG_EDGE);
}
async function loadPexelsPhoto(photoId, apiKey, fetchImpl, secrets) {
  const url = `https://api.pexels.com/v1/photos/${encodeURIComponent(photoId)}`;
  const json = await fetchJson(url, { headers: pexelsHeaders(apiKey) }, fetchImpl, secrets);
  const photo = asRecord2(json);
  if (!photo) throw new PptwiseError(`Pexels photo ${photoId} was not found`);
  const src = asRecord2(photo.src) ?? {};
  const original = asString2(src.original);
  const large2x = asString2(src.large2x);
  const downloadUrl = original ?? large2x;
  if (!downloadUrl) throw new PptwiseError(`Pexels photo ${photoId} has no download URL`);
  const author = asString2(photo.photographer) ?? "unknown";
  return {
    author,
    pageUrl: asString2(photo.url) ?? `https://www.pexels.com/photo/${photoId}/`,
    license: "Pexels License",
    downloadUrl,
    fallbackUrl: original ? large2x : void 0,
    width: asNumber2(photo.width),
    height: asNumber2(photo.height)
  };
}
async function loadPixabayPhoto(photoId, apiKey, fetchImpl, secrets) {
  const url = new URL("https://pixabay.com/api/");
  url.searchParams.set("key", apiKey);
  url.searchParams.set("id", photoId);
  const json = await fetchJson(url.toString(), { headers: { "User-Agent": userAgent2() } }, fetchImpl, secrets);
  const hits = parsePixabayHits(json);
  const hit = hits[0];
  const root = asRecord2(json);
  const rawHits = Array.isArray(root?.hits) ? root.hits : [];
  const raw = asRecord2(rawHits[0]);
  const downloadUrl = asString2(raw?.largeImageURL);
  if (!hit || !downloadUrl) throw new PptwiseError(`Pixabay photo ${photoId} was not found`);
  return {
    author: hit.author,
    pageUrl: hit.pageUrl,
    license: "Pixabay License",
    downloadUrl,
    width: hit.width,
    height: hit.height
  };
}
async function readSidecar(path2) {
  try {
    const raw = JSON.parse(await readFile9(path2, "utf8"));
    const rec = asRecord2(raw);
    if (!rec) return null;
    const provider = asString2(rec.provider);
    const known = provider === "pexels" || provider === "pixabay" || provider === "openverse" || provider === "grok" || provider === "codex" || provider === "antigravity";
    if (!known || !provider) return null;
    const photoId = asString2(rec.photo_id);
    if ((provider === "pexels" || provider === "pixabay") && !photoId) return null;
    return {
      provider,
      photo_id: photoId,
      license: asString2(rec.license) ?? "",
      author: asString2(rec.author),
      page_url: asString2(rec.page_url),
      attribution: asString2(rec.attribution),
      source: asString2(rec.source),
      query: asString2(rec.query),
      prompt: asString2(rec.prompt),
      downloaded_at: asString2(rec.downloaded_at),
      generated_at: asString2(rec.generated_at)
    };
  } catch {
    return null;
  }
}
async function runImagesFetch(ref, opts) {
  const { provider, photoId } = parsePhotoRef(ref);
  assertSafeFileSegment(opts.as, "asset id");
  const cwd = opts.cwd ?? process.cwd();
  const env = opts.env ?? process.env;
  const keys = await loadKeys(env);
  const secrets = knownSecretsFrom(keys);
  if (provider !== "openverse") {
    const apiKey = keys[provider].apiKey;
    if (!apiKey) throw missingKeysError(provider);
  }
  const { assetsDir } = await resolveImageHome(opts.deck, cwd);
  const jpgPath = join14(assetsDir, `${opts.as}.jpg`);
  const jsonPath = join14(assetsDir, `${opts.as}.json`);
  if (await pathExists(jpgPath) && await pathExists(jsonPath)) {
    const existing = await readSidecar(jsonPath);
    if (existing && existing.photo_id === photoId && existing.provider === provider) {
      return `already pinned ${provider}:${photoId} as ${opts.as} \u2014 skipped`;
    }
  }
  const fetchImpl = opts.fetch ?? proxyFetch;
  const sleep = opts.sleep ?? defaultSleep;
  const downloadFetch = opts.fetch;
  const lookup = opts.lookup ?? (opts.fetch ? void 0 : defaultDnsLookup);
  let meta;
  if (provider === "openverse") {
    const hit = await loadOpenverseDetail(
      photoId,
      {
        clientId: keys.openverse.ready ? keys.openverse.clientId : void 0,
        clientSecret: keys.openverse.ready ? keys.openverse.clientSecret : void 0
      },
      fetchImpl,
      secrets,
      sleep
    );
    meta = {
      author: hit.creator,
      pageUrl: hit.foreignLandingUrl,
      license: hit.license,
      downloadUrl: hit.url,
      width: hit.width,
      height: hit.height,
      attribution: hit.attribution,
      source: hit.source
    };
  } else {
    const apiKey = keys[provider].apiKey;
    meta = provider === "pexels" ? await loadPexelsPhoto(photoId, apiKey, fetchImpl, secrets) : await loadPixabayPhoto(photoId, apiKey, fetchImpl, secrets);
  }
  let bytes;
  try {
    bytes = await downloadBytes(meta.downloadUrl, downloadFetch, secrets, lookup);
  } catch (e) {
    if (meta.fallbackUrl) {
      bytes = await downloadBytes(meta.fallbackUrl, downloadFetch, secrets, lookup);
    } else {
      throw e;
    }
  }
  const apiLong = meta.width !== void 0 && meta.height !== void 0 ? Math.max(meta.width, meta.height) : void 0;
  const resize = opts.resizeToJpeg ?? defaultResizeToJpeg;
  const jpeg = await toJpeg(bytes, apiLong, resize);
  await mkdir7(assetsDir, { recursive: true });
  await writeFile8(jpgPath, jpeg);
  const sidecar = {
    provider,
    photo_id: photoId,
    license: meta.license,
    author: meta.author,
    page_url: meta.pageUrl,
    downloaded_at: (opts.now ?? (() => /* @__PURE__ */ new Date()))().toISOString()
  };
  if (opts.query) sidecar.query = opts.query;
  if (meta.attribution) sidecar.attribution = meta.attribution;
  if (meta.source) sidecar.source = meta.source;
  const json = JSON.stringify(sidecar, null, 2) + "\n";
  if (/"apiKey"\s*:/.test(json) || /"key"\s*:/.test(json) || /"clientSecret"\s*:/.test(json)) {
    throw new PptwiseError("internal error: sidecar would have contained a key field");
  }
  await writeFile8(jsonPath, json);
  return `pinned ${provider}:${photoId} as ${opts.as} \u2192 ${jpgPath}`;
}
async function runImagesList(opts) {
  const cwd = opts.cwd ?? process.cwd();
  const { assetsDir, earlier } = await resolveImageHome(opts.deck, cwd);
  const lines = [];
  const listed = /* @__PURE__ */ new Set();
  for (const dir of earlier === void 0 ? [assetsDir] : [assetsDir, earlier]) {
    for (const name of await sidecarNames(dir)) {
      const assetId = name.slice(0, -".json".length);
      if (listed.has(assetId)) continue;
      const sidecar = await readSidecar(join14(dir, name));
      if (!sidecar) continue;
      listed.add(assetId);
      const id = sidecar.photo_id ? `${sidecar.provider}:${sidecar.photo_id}` : sidecar.provider;
      const rest = [sidecar.author, sidecar.license, sidecar.page_url ?? sidecar.generated_at].filter(Boolean);
      lines.push(`${assetId}  ${id}  ${rest.join("  ")}`);
    }
  }
  return lines.length === 0 ? "No pinned stock photos." : lines.join("\n");
}
async function sidecarNames(dir) {
  try {
    return (await readdir6(dir)).filter((n) => n.endsWith(".json") && !n.startsWith(".")).sort();
  } catch (e) {
    if (e.code === "ENOENT") return [];
    throw e;
  }
}
async function writePinnedAsset(assetsDir, assetId, jpeg, sidecar) {
  await mkdir7(assetsDir, { recursive: true });
  const jpgPath = join14(assetsDir, `${assetId}.jpg`);
  const jsonPath = join14(assetsDir, `${assetId}.json`);
  const tmpJpg = join14(assetsDir, `.${assetId}.jpg.tmp`);
  const tmpJson = join14(assetsDir, `.${assetId}.json.tmp`);
  const json = JSON.stringify(sidecar, null, 2) + "\n";
  if (/"apiKey"\s*:/.test(json) || /"key"\s*:/.test(json) || /"clientSecret"\s*:/.test(json)) {
    throw new PptwiseError("internal error: sidecar would have contained a key field");
  }
  try {
    await writeFile8(tmpJpg, jpeg);
    await writeFile8(tmpJson, json);
    await rename2(tmpJpg, jpgPath);
    await rename2(tmpJson, jsonPath);
  } catch (e) {
    await unlink2(tmpJpg).catch(() => void 0);
    await unlink2(tmpJson).catch(() => void 0);
    await unlink2(jpgPath).catch(() => void 0);
    throw e;
  }
  return jpgPath;
}
async function defaultResolvePrompt(opts) {
  const { ir, theme: theme2 } = await loadValidatedDeckIr(opts.deck, opts.cwd);
  const brief = buildAssetBrief(ir, { theme: theme2 });
  const item = brief.items.find((entry) => entry.asset_id === opts.as && entry.suggested_prompt.trim() !== "");
  return item?.suggested_prompt;
}
async function runImagesGenerate(opts) {
  assertSafeFileSegment(opts.as, "asset id");
  const cwd = opts.cwd ?? process.cwd();
  const env = opts.env ?? process.env;
  const hit = await findUserConfig();
  const gens = resolveGenerators({ file: hit?.config ?? null });
  const fromFlag = opts.prompt?.trim();
  const prompt = fromFlag && fromFlag !== "" ? fromFlag : await (opts.resolvePrompt ?? defaultResolvePrompt)({ deck: opts.deck, as: opts.as, cwd });
  if (!prompt) {
    throw new PptwiseError(`no prompt for asset "${opts.as}" \u2014 pass --prompt`);
  }
  const bins = {};
  for (const id of GENERATOR_IDS) {
    bins[id] = await locateGeneratorBin(id, env);
  }
  const anyEnabled = GENERATOR_IDS.some((id) => gens.enabled[id]);
  if (!anyEnabled) {
    const foundDisabled = GENERATOR_IDS.filter((id) => bins[id] !== null);
    if (foundDisabled.length === 0) {
      throw new PptwiseError(
        "No image generator is enabled. Looked for grok, codex, antigravity. None were found on PATH."
      );
    }
    const listed = foundDisabled.map((id) => `${id} \u2014 pptwise config set images.generators.${id}.enabled true`).join("; ");
    throw new PptwiseError(`No image generator is enabled. Found but disabled: ${listed}`);
  }
  const { assetsDir } = await resolveImageHome(opts.deck, cwd);
  const workdir = await mkdtemp(join14(tmpdir(), "pptwise-gen-"));
  const dest = join14(workdir, "generated.jpg");
  const run = opts.run ?? defaultProcessRunner;
  const attempts = [];
  try {
    for (const id of gens.order) {
      if (!gens.enabled[id]) continue;
      const bin = bins[id];
      if (!bin) continue;
      try {
        await GENERATOR_ADAPTERS[id]({
          bin,
          workdir,
          dest,
          prompt,
          timeoutMs: gens.timeoutMs,
          run
        });
        const bytes = await readFile9(dest);
        if (sniffImageFormat(bytes) === null) {
          throw new PptwiseError("produced bytes that are not a recognized image");
        }
        const resize = opts.resizeToJpeg ?? defaultResizeToJpeg;
        const jpeg = await toJpeg(bytes, void 0, resize);
        const sidecar = {
          provider: id,
          license: "user-generated",
          prompt,
          generated_at: (opts.now ?? (() => /* @__PURE__ */ new Date()))().toISOString()
        };
        const pinned = await writePinnedAsset(assetsDir, opts.as, jpeg, sidecar);
        return `pinned ${id} as ${opts.as} \u2192 ${pinned}`;
      } catch (e) {
        attempts.push(
          e instanceof GeneratorWriteDenied ? writeDeniedMessage(id, e.detail) : `${id}: ${e instanceof Error ? e.message : String(e)}`
        );
      }
    }
    if (attempts.length === 0) {
      throw new PptwiseError(
        "No enabled image generator was found on PATH. Looked for grok, codex, antigravity."
      );
    }
    throw new PptwiseError(`All image generators failed: ${attempts.join("; ")}`);
  } finally {
    await rm4(workdir, { recursive: true, force: true });
  }
}

// src/cli/packs/license.ts
import { chmod, lstat, mkdir as mkdir8, readFile as readFile10, rm as rm5, writeFile as writeFile9 } from "fs/promises";
import { join as join15 } from "path";
var LICENSE_FILENAME = "license.json";
var LICENSE_KEY_PATTERN = /^ptw_[a-z2-7]{32}$/;
var KEY_SHAPE = 'a license key is "ptw_" followed by 32 characters from a-z and 2-7';
var SET_HINT = "pptwise license set <key>";
function licensePath() {
  return join15(pptwiseHome(), LICENSE_FILENAME);
}
async function readLicenseKey() {
  const path2 = licensePath();
  let text;
  try {
    text = await readFile10(path2, "utf8");
  } catch (e) {
    if (e.code === "ENOENT") return void 0;
    throw e;
  }
  let raw;
  try {
    raw = JSON.parse(text);
  } catch {
    throw new PptwiseError(`${path2} is not valid JSON. Set the key again with \`${SET_HINT}\`.`);
  }
  const key = typeof raw === "object" && raw !== null ? raw.key : void 0;
  if (typeof key !== "string" || !LICENSE_KEY_PATTERN.test(key)) {
    throw new PptwiseError(`${path2} holds no valid license key. Set the key again with \`${SET_HINT}\`.`);
  }
  return key;
}
function licenseKeyPrefix(key) {
  return `${key.slice(0, 8)}\u2026`;
}
async function assertNotSymlink2(path2) {
  try {
    if ((await lstat(path2)).isSymbolicLink()) throw new PptwiseError(`refusing to write ${path2}: it is a symlink`);
  } catch (e) {
    if (e.code === "ENOENT") return;
    throw e;
  }
}
async function runLicenseSet(value) {
  const key = value.trim();
  if (!LICENSE_KEY_PATTERN.test(key)) {
    throw new PptwiseError(`that is not a pptwise license key: ${KEY_SHAPE}. Copy the whole key again and retry.`);
  }
  const path2 = licensePath();
  await mkdir8(pptwiseHome(), { recursive: true });
  await assertNotSymlink2(path2);
  await writeFile9(path2, `${JSON.stringify({ key }, null, 2)}
`, { encoding: "utf8", mode: 384 });
  try {
    await chmod(path2, 384);
  } catch {
  }
  return `Saved license ${licenseKeyPrefix(key)} to ${path2}. Run \`pptwise packs sync\` to install your packs.`;
}
async function runLicenseStatus() {
  const key = await readLicenseKey();
  if (key === void 0) return `No license configured. Set one with \`${SET_HINT}\`.`;
  return `License ${licenseKeyPrefix(key)} configured in ${licensePath()}.`;
}
async function runLicenseClear() {
  const path2 = licensePath();
  try {
    await lstat(path2);
  } catch (e) {
    if (e.code === "ENOENT") return "No license configured. Nothing to clear.";
    throw e;
  }
  await rm5(path2, { force: true });
  return `Removed ${path2}. Installed packs stay in place.`;
}

// src/cli/packs/sync.ts
import { createHash as createHash3 } from "crypto";
import { join as join17 } from "path";
import { z as z4 } from "zod";

// src/cli/packs/install.ts
import { randomBytes as randomBytes2 } from "crypto";
import { mkdir as mkdir9, rename as rename3, rm as rm6, writeFile as writeFile10 } from "fs/promises";
import { dirname as dirname7, join as join16, resolve as resolve9, sep as sep2 } from "path";
import JSZip from "jszip";

// src/cli/packs/semver-range.ts
var NUM = "0|[1-9]\\d*";
var PRE_ID = "(?:0|[1-9]\\d*|\\d*[A-Za-z-][0-9A-Za-z-]*)";
var PRERELEASE = `${PRE_ID}(?:\\.${PRE_ID})*`;
var BUILD = "[0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*";
var FULL_VERSION = new RegExp(`^v?(${NUM})\\.(${NUM})\\.(${NUM})(?:-(${PRERELEASE}))?(?:\\+${BUILD})?$`);
var X = `${NUM}|x|X|\\*`;
var PARTIAL = new RegExp(`^[v=]*(${X})(?:\\.(${X})(?:\\.(${X})(?:-(${PRERELEASE}))?(?:\\+${BUILD})?)?)?$`);
var OPERATOR = /^(<=|>=|<|>|=)?(.*)$/;
function invalidRange(range) {
  return new Error(`invalid semver range "${range}"`);
}
function parsePrerelease(raw) {
  if (raw === void 0) return [];
  return raw.split(".").map((id) => /^\d+$/.test(id) ? Number(id) : id);
}
function parseVersion2(version) {
  const m = FULL_VERSION.exec(version.trim());
  if (m === null) throw new Error(`invalid version "${version}"`);
  return { major: Number(m[1]), minor: Number(m[2]), patch: Number(m[3]), prerelease: parsePrerelease(m[4]) };
}
function compareIds(a, b) {
  if (typeof a === "number" && typeof b === "number") return a === b ? 0 : a < b ? -1 : 1;
  if (typeof a === "number") return -1;
  if (typeof b === "number") return 1;
  return a === b ? 0 : a < b ? -1 : 1;
}
function compare(a, b) {
  for (const key of ["major", "minor", "patch"]) {
    if (a[key] !== b[key]) return a[key] < b[key] ? -1 : 1;
  }
  if (a.prerelease.length === 0 || b.prerelease.length === 0) {
    return a.prerelease.length === b.prerelease.length ? 0 : a.prerelease.length === 0 ? 1 : -1;
  }
  for (let i = 0; ; i++) {
    const x = a.prerelease[i];
    const y = b.prerelease[i];
    if (x === void 0 && y === void 0) return 0;
    if (x === void 0) return -1;
    if (y === void 0) return 1;
    const c = compareIds(x, y);
    if (c !== 0) return c;
  }
}
function parsePartial(raw, range) {
  const m = PARTIAL.exec(raw);
  if (m === null) throw invalidRange(range);
  const num2 = (s) => s === void 0 || /^[xX*]$/.test(s) ? void 0 : Number(s);
  const major = num2(m[1]);
  const minor = major === void 0 ? void 0 : num2(m[2]);
  const patch = minor === void 0 ? void 0 : num2(m[3]);
  return { major, minor, patch, prerelease: patch === void 0 ? [] : parsePrerelease(m[4]) };
}
function v(major, minor, patch, prerelease = []) {
  return { major, minor, patch, prerelease };
}
function below(major, minor, patch) {
  return { op: "<", version: v(major, minor, patch, [0]) };
}
var NOTHING = below(0, 0, 0);
function primitive(op, p) {
  const { major, minor, patch } = p;
  if (major === void 0) return op === "<" || op === ">" ? [NOTHING] : [void 0];
  if (minor !== void 0 && patch !== void 0) return [{ op, version: v(major, minor, patch, p.prerelease) }];
  if (op === "=") return xRange(p);
  if (op === ">") return [{ op: ">=", version: minor === void 0 ? v(major + 1, 0, 0) : v(major, minor + 1, 0) }];
  if (op === ">=") return [{ op: ">=", version: v(major, minor ?? 0, 0) }];
  if (op === "<") return [below(major, minor ?? 0, 0)];
  return [minor === void 0 ? below(major + 1, 0, 0) : below(major, minor + 1, 0)];
}
function xRange(p) {
  const { major, minor, patch } = p;
  if (major === void 0) return [void 0];
  if (minor === void 0) return [{ op: ">=", version: v(major, 0, 0) }, below(major + 1, 0, 0)];
  if (patch === void 0) return [{ op: ">=", version: v(major, minor, 0) }, below(major, minor + 1, 0)];
  return [{ op: "=", version: v(major, minor, patch, p.prerelease) }];
}
function tilde(p) {
  const { major, minor, patch } = p;
  if (major === void 0) return [void 0];
  if (minor === void 0) return xRange(p);
  if (patch === void 0) return xRange(p);
  return [{ op: ">=", version: v(major, minor, patch, p.prerelease) }, below(major, minor + 1, 0)];
}
function caret(p) {
  const { major, minor, patch } = p;
  if (major === void 0) return [void 0];
  if (minor === void 0) return xRange(p);
  if (patch === void 0) {
    return [{ op: ">=", version: v(major, minor, 0) }, major === 0 ? below(0, minor + 1, 0) : below(major + 1, 0, 0)];
  }
  const floor = { op: ">=", version: v(major, minor, patch, p.prerelease) };
  if (major !== 0) return [floor, below(major + 1, 0, 0)];
  if (minor !== 0) return [floor, below(0, minor + 1, 0)];
  return [floor, below(0, 0, patch + 1)];
}
function hyphen(fromRaw, toRaw, range) {
  const from = parsePartial(fromRaw, range);
  const to = parsePartial(toRaw, range);
  const out = [];
  if (from.major !== void 0) {
    out.push({ op: ">=", version: v(from.major, from.minor ?? 0, from.patch ?? 0, from.prerelease) });
  }
  if (to.major !== void 0) {
    if (to.minor === void 0) out.push(below(to.major + 1, 0, 0));
    else if (to.patch === void 0) out.push(below(to.major, to.minor + 1, 0));
    else out.push({ op: "<=", version: v(to.major, to.minor, to.patch, to.prerelease) });
  }
  return out.length === 0 ? [void 0] : out;
}
function simple(token, range) {
  if (token.startsWith("~>")) return tilde(parsePartial(token.slice(2), range));
  if (token.startsWith("~")) return tilde(parsePartial(token.slice(1), range));
  if (token.startsWith("^")) return caret(parsePartial(token.slice(1), range));
  const [, op, rest] = OPERATOR.exec(token);
  const partial = parsePartial(rest, range);
  return op === void 0 ? xRange(partial) : primitive(op, partial);
}
var HYPHEN = /^(\S+)\s+-\s+(\S+)$/;
function parseSet(raw, range) {
  const set = raw.trim();
  if (set === "") return [void 0];
  const h = HYPHEN.exec(set);
  if (h !== null) return hyphen(h[1], h[2], range);
  const joined = set.replace(/(<=|>=|<|>|=|~>|~|\^)\s+/g, "$1");
  return joined.split(/\s+/).flatMap((token) => simple(token, range));
}
function parseRange(range) {
  return range.split("||").map((set) => parseSet(set, range));
}
function test(c, version) {
  if (c === void 0) return true;
  const cmp = compare(version, c.version);
  switch (c.op) {
    case "=":
      return cmp === 0;
    case "<":
      return cmp < 0;
    case "<=":
      return cmp <= 0;
    case ">":
      return cmp > 0;
    case ">=":
      return cmp >= 0;
  }
}
function testSet(set, version) {
  if (!set.every((c) => test(c, version))) return false;
  if (version.prerelease.length === 0) return true;
  return set.some(
    (c) => c !== void 0 && c.version.prerelease.length > 0 && c.version.major === version.major && c.version.minor === version.minor && c.version.patch === version.patch
  );
}
function satisfiesRange(version, range) {
  const parsed = parseVersion2(version);
  return parseRange(range).some((set) => testSet(set, parsed));
}

// src/cli/packs/install.ts
var S_IFMT = 61440;
var S_IFLNK = 40960;
function refuse(detail) {
  return new PptwiseError(detail);
}
async function openArchive(bytes) {
  try {
    return await JSZip.loadAsync(bytes);
  } catch (e) {
    throw refuse(`the download is not a readable zip archive (${e.message})`);
  }
}
function checkEntries(zip) {
  const entries = Object.values(zip.files);
  for (const entry of [...entries.filter((e) => !e.dir), ...entries.filter((e) => e.dir)]) {
    const original = entry.unsafeOriginalName ?? entry.name;
    const path2 = entry.dir ? original.replace(/\/+$/, "") : original;
    if (entry.dir && path2 === "") continue;
    const unsafe = unsafePackPathReason(path2);
    if (unsafe !== void 0) throw refuse(`archive entry "${original}" ${unsafe}`);
    const mode = entry.unixPermissions;
    if (typeof mode === "number" && (mode & S_IFMT) === S_IFLNK) {
      throw refuse(`archive entry "${original}" is a symbolic link, and packs may not contain links`);
    }
  }
}
async function readManifest(zip) {
  const entry = zip.file(PACK_MANIFEST_FILENAME);
  if (entry === null) throw refuse(`the archive has no ${PACK_MANIFEST_FILENAME} at its root`);
  let raw;
  try {
    raw = JSON.parse(await entry.async("string"));
  } catch {
    throw refuse(`${PACK_MANIFEST_FILENAME} is not valid JSON`);
  }
  return parsePackManifest(raw, PACK_MANIFEST_FILENAME);
}
function checkManifest(manifest, target, engineVersion) {
  if (manifest.id !== target.id) {
    throw refuse(`${PACK_MANIFEST_FILENAME} names pack "${manifest.id}", but the catalog entry is "${target.id}"`);
  }
  if (manifest.version !== target.version) {
    throw refuse(`${PACK_MANIFEST_FILENAME} says version ${manifest.version}, but the catalog entry is ${target.version}`);
  }
  let fits;
  try {
    fits = satisfiesRange(engineVersion, manifest.engine);
  } catch {
    throw refuse(`${PACK_MANIFEST_FILENAME} has an engine range pptwise cannot read: "${manifest.engine}"`);
  }
  if (!fits) throw refuse(`the pack needs pptwise ${manifest.engine}, and this is ${engineVersion}`);
}
async function checkThemes(zip, manifest, root) {
  const owners = /* @__PURE__ */ new Map();
  for (const pack of await listInstalledPacks(root, { except: manifest.id })) {
    for (const theme2 of pack.themes) owners.set(theme2.id, pack.id);
  }
  const ids = [];
  for (const rel of manifest.themes) {
    const unsafe = unsafePackPathReason(rel);
    if (unsafe !== void 0) throw refuse(`theme path "${rel}" in ${PACK_MANIFEST_FILENAME} ${unsafe}`);
    const entry = zip.file(rel);
    if (entry === null) throw refuse(`${PACK_MANIFEST_FILENAME} lists theme "${rel}", which is not in the archive`);
    let raw;
    try {
      raw = JSON.parse(await entry.async("string"));
    } catch {
      throw refuse(`theme file ${rel} is not valid JSON`);
    }
    const file = parseBrandThemeFile(raw, rel);
    const retired = retiredThemeIdMessage(file.id);
    if (retired !== void 0) throw refuse(`theme file ${rel}: ${retired}`);
    if (CANONICAL_THEME_IDS.includes(file.id)) {
      throw refuse(`theme "${file.id}" in ${rel} has the id of a built-in preset, and a pack may not replace one`);
    }
    if (ids.includes(file.id)) throw refuse(`theme "${file.id}" appears twice in the pack`);
    const owner = owners.get(file.id);
    if (owner !== void 0) throw refuse(`theme "${file.id}" in ${rel} is already installed by pack "${owner}"`);
    try {
      compileThemeDefinition(file);
    } catch (e) {
      throw refuse(`theme file ${rel}: ${e.message}`);
    }
    ids.push(file.id);
  }
  return ids;
}
async function unpack(zip, dir) {
  const base = resolve9(dir);
  await mkdir9(base, { recursive: true });
  for (const entry of Object.values(zip.files)) {
    const target = resolve9(base, ...entry.name.split("/").filter((part) => part.length > 0));
    if (target !== base && !target.startsWith(base + sep2)) throw refuse(`archive entry "${entry.name}" resolves outside the pack`);
    if (entry.dir) {
      await mkdir9(target, { recursive: true });
      continue;
    }
    await mkdir9(dirname7(target), { recursive: true });
    await writeFile10(target, await entry.async("uint8array"));
  }
}
async function swapIn(staging, dir, suffix) {
  const retired = join16(dirname7(dir), `.retired-${suffix}`);
  let moved = false;
  try {
    await rename3(dir, retired);
    moved = true;
  } catch (e) {
    if (e.code !== "ENOENT") throw e;
  }
  try {
    await rename3(staging, dir);
  } catch (e) {
    if (moved) await rename3(retired, dir);
    throw e;
  }
  if (moved) await rm6(retired, { recursive: true, force: true });
}
async function installPack(bytes, target, opts) {
  const root = opts.root ?? packsRoot();
  const zip = await openArchive(bytes);
  checkEntries(zip);
  const manifest = await readManifest(zip);
  checkManifest(manifest, target, opts.engineVersion);
  const themes = await checkThemes(zip, manifest, root);
  const suffix = `${target.id}-${randomBytes2(6).toString("hex")}`;
  const staging = join16(root, `.staging-${suffix}`);
  const dir = join16(root, target.id);
  try {
    await unpack(zip, staging);
    await swapIn(staging, dir, suffix);
  } finally {
    await rm6(staging, { recursive: true, force: true });
  }
  return { dir, themes };
}

// src/cli/packs/sync.ts
var DEFAULT_PACKS_URL = "https://pptwise.com";
var CATALOG_TIMEOUT_MS = 3e4;
var DOWNLOAD_TIMEOUT_MS = 3e5;
var CatalogSchema = z4.object({
  catalog: z4.literal(1),
  packs: z4.array(
    z4.object({
      id: z4.string(),
      version: z4.string(),
      title: z4.string(),
      size: z4.number(),
      sha256: z4.string(),
      engine: z4.string()
    })
  )
});
var SET_HINT2 = "pptwise license set <key>";
var UNCHANGED = "Installed packs are unchanged.";
var LOOPBACK_HOSTS = /* @__PURE__ */ new Set(["localhost", "127.0.0.1", "[::1]"]);
function packsServerUrl(env = process.env) {
  const raw = resolveProductEnv("PACKS_URL", env) ?? DEFAULT_PACKS_URL;
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new PptwiseError(`PPTWISE_PACKS_URL is not a URL: "${raw}"`);
  }
  if (url.protocol === "http:" && !LOOPBACK_HOSTS.has(url.hostname)) {
    throw new PptwiseError(
      `PPTWISE_PACKS_URL "${raw}" uses plain http to ${url.host}, and the license key would travel unencrypted. Use an https address. Plain http is allowed only on localhost, 127.0.0.1, or ::1.`
    );
  }
  if (url.protocol !== "https:" && url.protocol !== "http:") {
    throw new PptwiseError(`PPTWISE_PACKS_URL must be an https URL, got "${raw}"`);
  }
  return raw.replace(/\/+$/, "");
}
var ServerRefusal = class extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
  status;
};
async function serverMessage(res) {
  try {
    const body = await res.json();
    return typeof body.error === "string" && body.error.length > 0 ? body.error.slice(0, 300) : void 0;
  } catch {
    return void 0;
  }
}
async function get(url, key, timeoutMs) {
  const res = await proxyFetch(url, {
    headers: { authorization: `Bearer ${key}`, "user-agent": `pptwise/${VERSION}` },
    signal: AbortSignal.timeout(timeoutMs)
  });
  if (res.ok) return res;
  const said = await serverMessage(res);
  throw new ServerRefusal(res.status, said === void 0 ? `HTTP ${res.status}` : `HTTP ${res.status}: ${said}`);
}
function describeError(e) {
  const message = e instanceof Error ? e.message : String(e);
  const cause = e instanceof Error ? e.cause : void 0;
  const detail = typeof cause?.code === "string" ? cause.code : typeof cause?.message === "string" ? cause.message : void 0;
  return detail !== void 0 && detail.length > 0 && !message.includes(detail) ? `${message} (${detail})` : message;
}
function reachFailure(server, e) {
  return `could not reach the pack server at ${new URL(server).host}: ${describeError(e)}`;
}
function catalogFailure(server, e) {
  if (e instanceof ServerRefusal) {
    switch (e.status) {
      case 401:
        return `the pack server did not accept this license key (${e.message}). Check it with \`pptwise license status\` and set it again with \`${SET_HINT2}\`. ${UNCHANGED}`;
      case 403:
        return `this license key has been revoked (${e.message}). ${UNCHANGED}`;
      case 503:
        return `the pack server is not available right now (${e.message}). Try again later. ${UNCHANGED}`;
      default:
        return `the pack server refused the catalog request (${e.message}). ${UNCHANGED}`;
    }
  }
  return `${reachFailure(server, e)}. ${UNCHANGED}`;
}
async function fetchCatalog(server, key) {
  const res = await get(`${server}/api/packs/catalog`, key, CATALOG_TIMEOUT_MS);
  let body;
  try {
    body = await res.json();
  } catch {
    throw new PptwiseError("the pack catalog is not valid JSON");
  }
  const parsed = CatalogSchema.safeParse(body);
  if (!parsed.success) {
    const detail = parsed.error.issues.map((i) => `${i.path.join(".") || "(root)"}: ${i.message}`).join(". ");
    throw new PptwiseError(`the pack catalog is not one this pptwise can read (${detail})`);
  }
  return parsed.data.packs;
}
function malformedEntry(entry) {
  if (!PACK_ID_PATTERN.test(entry.id)) return `the catalog entry has an unusable pack id "${entry.id}"`;
  if (!PACK_VERSION_PATTERN.test(entry.version)) return `the catalog entry has an unusable version "${entry.version}"`;
  if (!/^[0-9a-f]{64}$/.test(entry.sha256)) return "the catalog entry has no usable sha256";
  return void 0;
}
function engineMismatch(entry, engineVersion) {
  let fits;
  try {
    fits = satisfiesRange(engineVersion, entry.engine);
  } catch {
    return `needs a pptwise that reads the engine range "${entry.engine}", and this is ${engineVersion}. Run \`pptwise self-update\``;
  }
  if (fits) return void 0;
  return `needs pptwise ${entry.engine}, and this is ${engineVersion}. Run \`pptwise self-update\``;
}
async function installedVersion(root, id) {
  try {
    return (await readInstalledPack(join17(root, id), id)).version;
  } catch {
    return void 0;
  }
}
async function syncOne(entry, ctx) {
  const item = { id: entry.id, version: entry.version, title: entry.title, status: "failed" };
  const malformed = malformedEntry(entry);
  if (malformed !== void 0) return { ...item, reason: malformed };
  const previous = await installedVersion(ctx.root, entry.id);
  const incompatible = engineMismatch(entry, ctx.engineVersion);
  if (incompatible !== void 0) {
    const kept = previous !== void 0 ? `. Version ${previous} stays installed` : "";
    return { ...item, status: "incompatible", reason: `${incompatible}${kept}` };
  }
  if (previous === entry.version) return { ...item, status: "current" };
  let bytes;
  try {
    const res = await get(`${ctx.server}/api/packs/${entry.id}/${entry.version}.zip`, ctx.key, DOWNLOAD_TIMEOUT_MS);
    bytes = new Uint8Array(await res.arrayBuffer());
  } catch (e) {
    const reason = e instanceof ServerRefusal ? `the download was refused (${e.message})` : `the download failed (${describeError(e)})`;
    return { ...item, reason };
  }
  const digest = createHash3("sha256").update(bytes).digest("hex");
  if (digest !== entry.sha256) {
    return { ...item, reason: `the download's sha256 is ${digest}, but the catalog says ${entry.sha256}` };
  }
  try {
    const result = await installPack(bytes, { id: entry.id, version: entry.version }, { root: ctx.root, engineVersion: ctx.engineVersion });
    const done = { ...item, status: previous === void 0 ? "installed" : "updated", themes: result.themes };
    if (previous !== void 0) done.previous = previous;
    return done;
  } catch (e) {
    return { ...item, reason: e instanceof Error ? e.message : String(e) };
  }
}
async function syncPacks(opts = {}) {
  const key = await readLicenseKey();
  if (key === void 0) return { license: false, ok: true, packs: [] };
  const server = packsServerUrl(opts.env ?? process.env);
  let catalog;
  try {
    catalog = await fetchCatalog(server, key);
  } catch (e) {
    const error = e instanceof PptwiseError ? `${e.message}. ${UNCHANGED}` : catalogFailure(server, e);
    return { license: true, ok: false, server, error, packs: [] };
  }
  const ctx = { server, key, root: packsRoot(), engineVersion: opts.engineVersion ?? VERSION };
  const packs2 = [];
  for (const entry of catalog) packs2.push(await syncOne(entry, ctx));
  return { license: true, ok: packs2.every((p) => p.status !== "failed"), server, packs: packs2 };
}
function formatItem(item, width) {
  const head = `  ${`${item.id} ${item.version}`.padEnd(width)}  `;
  switch (item.status) {
    case "installed":
      return `${head}installed (themes: ${item.themes.join(", ") || "none"})`;
    case "updated":
      return `${head}updated from ${item.previous} (themes: ${item.themes.join(", ") || "none"})`;
    case "current":
      return `${head}up to date`;
    case "incompatible":
      return `${head}skipped: ${item.reason}`;
    case "failed":
      return `${head}not installed: ${item.reason}`;
  }
}
function formatPackSyncReport(report) {
  if (!report.license) return `No license configured, so there are no packs to sync. Set one with \`${SET_HINT2}\`.`;
  if (report.packs.length === 0) return `The pack catalog at ${report.server} lists no packs.`;
  const width = Math.max(...report.packs.map((p) => `${p.id} ${p.version}`.length));
  return [`Packs from ${report.server}:`, ...report.packs.map((p) => formatItem(p, width))].join("\n");
}
async function runPacksSync(opts = {}) {
  const report = await syncPacks(opts);
  if (opts.json) return { output: JSON.stringify(report, null, 2), failed: !report.ok };
  if (report.error !== void 0) throw new PptwiseError(`packs sync failed: ${report.error}`);
  return { output: formatPackSyncReport(report), failed: !report.ok };
}
async function runPacksList(opts = {}) {
  const packs2 = await listInstalledPacks();
  if (opts.json) return JSON.stringify(packs2, null, 2);
  if (packs2.length === 0) return "No packs installed. With a license configured, run `pptwise packs sync`.";
  const width = Math.max(...packs2.map((p) => `${p.id} ${p.version}`.length));
  return packs2.map((p) => {
    const themes = p.themes.length > 0 ? p.themes.map((t) => `    ${t.id}`).join("\n") : "    (no themes)";
    return `${`${p.id} ${p.version}`.padEnd(width)}  ${p.title}
${themes}`;
  }).join("\n");
}

// src/cli/serve.ts
import { statSync as statSync2, watch } from "fs";
import { createServer } from "http";
import { platform as osPlatform } from "os";
import { basename as basename7, dirname as dirname8, join as join18, resolve as resolve10, sep as sep3 } from "path";
var DEFAULT_PORT = 4400;
var DEBOUNCE_MS = 200;
var HEARTBEAT_MS = 3e4;
var THEME_POLL_MS = 2e3;
function watchRoots(resolvedTarget, isDir, extra = []) {
  const roots = isDir ? [
    { path: join18(resolvedTarget, SPEC_FILENAME), kind: "file" },
    { path: join18(resolvedTarget, PAGES_DIRNAME), kind: "dir" },
    { path: join18(resolvedTarget, ASSETS_DIRNAME), kind: "dir" },
    { path: join18(resolvedTarget, THEME_FILENAME), kind: "file" }
  ] : [{ path: resolvedTarget, kind: "file" }];
  return [...roots, ...extra];
}
function themeWatchRoots(themeName, opts) {
  if (themeName === void 0 || !THEME_ID_PATTERN.test(themeName)) return [];
  const ceiling = resolve10(opts.ceilingDir);
  const withinCeiling = /* @__PURE__ */ new Set();
  for (let dir = resolve10(opts.startDir); ; dir = dirname8(dir)) {
    withinCeiling.add(dir);
    if (dir === ceiling || dirname8(dir) === dir) break;
  }
  return themeCandidates(themeName, opts).filter((candidate) => candidate.deck || withinCeiling.has(resolve10(candidate.anchor))).map((candidate) => ({ path: candidate.path, kind: "file" }));
}
function watchTree(roots, onChange, onError, options = {}) {
  let rules = /* @__PURE__ */ new Map();
  const watchers = /* @__PURE__ */ new Map();
  const ceiling = options.ceilingDir === void 0 ? void 0 : resolve10(options.ceilingDir);
  const isEnoent = (e) => e.code === "ENOENT";
  const isDenied = (e) => {
    const code = e.code;
    return code === "EACCES" || code === "EPERM";
  };
  let closed = false;
  function ruleFor(dir) {
    let rule = rules.get(dir);
    if (!rule) {
      rule = { files: /* @__PURE__ */ new Set(), allFiles: false, children: /* @__PURE__ */ new Set() };
      rules.set(dir, rule);
    }
    return rule;
  }
  function linkToParent(dir) {
    const parent = dirname8(dir);
    if (parent === dir) return void 0;
    ruleFor(parent).children.add(basename7(dir));
    return parent;
  }
  function insideCeiling(dir) {
    if (ceiling === void 0 || dir === ceiling) return false;
    return dir.startsWith(ceiling.endsWith(sep3) ? ceiling : ceiling + sep3);
  }
  function linkAncestors(dir) {
    for (let child = dir; ; child = dirname8(child)) {
      const parent = dirname8(child);
      if (parent === child) return;
      if (!insideCeiling(child) && !rules.has(parent)) return;
      ruleFor(parent).children.add(basename7(child));
    }
  }
  function inodeOf(dir) {
    try {
      const st = statSync2(dir, { bigint: true });
      return st.isDirectory() ? st.ino : void 0;
    } catch (e) {
      if (isEnoent(e)) return void 0;
      throw e;
    }
  }
  function stillWatchesItsDirectory(dir, ino) {
    try {
      return inodeOf(dir) === ino;
    } catch (e) {
      if (e.code === "ENOTDIR") return false;
      throw e;
    }
  }
  function detach(dir) {
    for (const [key, entry] of watchers) {
      if (key === dir || key.startsWith(dir + sep3)) {
        entry.watcher.close();
        watchers.delete(key);
      }
    }
  }
  function attach(dir) {
    if (watchers.has(dir)) return;
    const rule = ruleFor(dir);
    let watcher;
    try {
      watcher = watch(dir, (_event, filename) => {
        try {
          onEvent(dir, filename);
        } catch (e) {
          onError(e);
        }
      });
    } catch (e) {
      if (isDenied(e)) {
        rules.delete(dir);
        return;
      }
      if (!isEnoent(e)) throw e;
      const parent = linkToParent(dir);
      if (parent !== void 0) attach(parent);
      return;
    }
    let ino;
    try {
      ino = inodeOf(dir);
    } catch (e) {
      watcher.close();
      throw e;
    }
    if (ino === void 0) {
      watcher.close();
      const parent = linkToParent(dir);
      if (parent !== void 0) attach(parent);
      return;
    }
    watcher.on("error", () => detach(dir));
    watchers.set(dir, { watcher, ino });
    for (const child of rule.children) attach(join18(dir, child));
  }
  function refreshChild(dir) {
    const current = watchers.get(dir);
    const ino = inodeOf(dir);
    if (current !== void 0 && current.ino === ino) return;
    detach(dir);
    attach(dir);
  }
  function onEvent(dir, filename) {
    const rule = rules.get(dir);
    if (rule === void 0) return;
    if (filename === null) {
      for (const child of rule.children) refreshChild(join18(dir, child));
      onChange();
      return;
    }
    const name = basename7(filename.toString());
    let matters = rule.allFiles || rule.files.has(name);
    if (rule.children.has(name)) {
      refreshChild(join18(dir, name));
      matters = true;
    }
    if (matters) onChange();
  }
  function update(list) {
    if (closed) return;
    rules = /* @__PURE__ */ new Map();
    for (const root of list) {
      const abs = resolve10(root.path);
      if (root.kind === "file") {
        ruleFor(dirname8(abs)).files.add(basename7(abs));
      } else {
        ruleFor(abs).allFiles = true;
        linkToParent(abs);
      }
    }
    for (const dir of [...rules.keys()]) linkAncestors(dir);
    try {
      for (const [dir, entry] of [...watchers]) {
        if (!watchers.has(dir)) continue;
        if (!stillWatchesItsDirectory(dir, entry.ino)) detach(dir);
      }
      for (const dir of [...rules.keys()]) attach(dir);
    } finally {
      for (const [dir, entry] of watchers) {
        if (rules.has(dir)) continue;
        entry.watcher.close();
        watchers.delete(dir);
      }
    }
  }
  function close() {
    closed = true;
    for (const entry of watchers.values()) entry.watcher.close();
    watchers.clear();
  }
  try {
    update(roots);
  } catch (e) {
    close();
    throw e;
  }
  return { update, close };
}
var SERVE_CLIENT_SCRIPT_ID = "pptwise-serve-client";
var SERVE_CLIENT_JS = `
(function () {
  // Live reload is the whole of this client (the revision-request submit
  // that used to sit beside it was removed on 2026-08-16 \u2014 see this
  // module's own header). It keeps its own function and its own try/catch
  // at the call site below: an EventSource construction that throws in some
  // unusual embedding must degrade to a page that simply does not
  // auto-refresh, not abort the IIFE.

  function setUpLiveReload() {
    var es = new EventSource('/events')
    es.addEventListener('reload', function () { location.reload() })

    var banner = document.createElement('div')
    banner.id = 'pptwise-serve-error-banner'
    banner.setAttribute('role', 'alert')
    banner.style.cssText =
      'display:none;position:fixed;top:0;left:0;right:0;z-index:2147483647;' +
      'background:#dc2626;color:#fff;font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;' +
      'padding:8px 16px;text-align:center'
    document.body.appendChild(banner)

    function showBanner(message) {
      banner.textContent = 'pptwise serve: ' + message
      banner.style.display = 'block'
    }

    es.addEventListener('error', function (e) {
      if (!e || typeof e.data !== 'string') return // a real connection hiccup, not the server's own rebuild-failed frame
      var message = 'rebuild failed'
      try {
        var parsed = JSON.parse(e.data)
        if (parsed && typeof parsed.message === 'string') message = parsed.message
      } catch (err) {}
      showBanner(message)
    })

    // A page opened (or reloaded by hand) after a failed rebuild is the last
    // good build, not the current source. The SSE error frame for that
    // failure went out before this page existed, so ask once.
    if (typeof fetch === 'function') {
      fetch('/status')
        .then(function (res) { return res.json() })
        .then(function (status) {
          if (status && status.latestOk === false) {
            showBanner((typeof status.error === 'string' ? status.error : 'rebuild failed') + ' (showing the last successful build)')
          }
        })
        .catch(function () {})
    }
  }

  try {
    setUpLiveReload()
  } catch (e) {
    console.error('pptwise serve: failed to set up live reload', e)
  }
})()
`.trim();
function buildServeClientScriptTag() {
  return `<script id="${SERVE_CLIENT_SCRIPT_ID}">${SERVE_CLIENT_JS}</script>`;
}
function injectServeClient(html) {
  if (html.includes(SERVE_CLIENT_SCRIPT_ID)) return html;
  return html.replace("</body>", `${buildServeClientScriptTag()}
</body>`);
}
async function createServeServer(options) {
  const cwd = options.cwd ?? process.cwd();
  const requestedPort = options.port ?? DEFAULT_PORT;
  if (!Number.isInteger(requestedPort) || requestedPort < 0 || requestedPort > 65535) {
    throw new PptwiseError(`invalid port ${requestedPort} \u2014 expected an integer between 0 and 65535`);
  }
  const located = await locateDeck(options.target, { cwd });
  const projectHit = await findConfig(cwd);
  const watchCeiling = projectHit !== null ? dirname8(projectHit.path) : cwd;
  let cachedHtml = "";
  let latestRevision = 0;
  let servedRevision = 0;
  let latestError;
  const sseClients = /* @__PURE__ */ new Set();
  function status() {
    return latestError === void 0 ? { latestRevision, servedRevision, latestOk: true } : { latestRevision, servedRevision, latestOk: false, error: latestError };
  }
  function writeToAll(chunk) {
    for (const res of sseClients) {
      try {
        res.write(chunk);
      } catch {
      }
    }
  }
  function broadcast(event, data) {
    writeToAll(`event: ${event}
data: ${JSON.stringify(data)}

`);
  }
  const messageOf2 = (e) => e instanceof Error ? e.message : String(e);
  let watchedTarget = located;
  let watchedThemeName;
  function currentWatchRoots() {
    const { resolvedTarget, isDir } = watchedTarget;
    const deckDir = isDir ? resolvedTarget : dirname8(resolvedTarget);
    const workspaceAssets = join18(
      resolveWorkspaceLocation({
        cwd,
        projectConfigPath: projectHit?.path,
        target: resolvedTarget,
        isDir
      }).dir,
      ASSETS_DIRNAME
    );
    return watchRoots(resolvedTarget, isDir, [
      { path: workspaceAssets, kind: "dir" },
      ...themeWatchRoots(watchedThemeName, { startDir: cwd, deckDir, ceilingDir: watchCeiling })
    ]);
  }
  let lastThemeInputsKey = "";
  let buildGeneration = 0;
  let building = false;
  let closed = false;
  function recordThemeInputs(inputs) {
    lastThemeInputsKey = inputs.key;
    watchedThemeName = boundThemeName(inputs) ?? watchedThemeName;
  }
  async function buildOnce() {
    const revision = latestRevision + 1;
    let html;
    let error;
    building = true;
    try {
      try {
        const result = await buildDeckPreview(options.target, { cwd });
        html = injectServeClient(result.html);
        recordThemeInputs(result.themeInputs);
      } catch (e) {
        if (!(e instanceof DeckBuildError)) throw e;
        error = e.message;
        recordThemeInputs(e.themeInputs);
      }
      if (watchers === void 0) throw new Error("pptwise serve: a rebuild ran before the watchers were attached");
      watchers.update(currentWatchRoots());
    } catch (e) {
      error ??= messageOf2(e);
    } finally {
      latestRevision = revision;
      latestError = error;
      if (html !== void 0) {
        cachedHtml = html;
        servedRevision = revision;
      }
      buildGeneration++;
      building = false;
    }
    if (error === void 0) broadcast("reload", { revision });
    else broadcast("error", { revision, message: error });
  }
  let openBuildQueue;
  let buildQueue = new Promise((resolveOpen) => openBuildQueue = resolveOpen);
  function rebuild() {
    const run = buildQueue.then(buildOnce).catch((e) => {
      latestError = messageOf2(e);
      building = false;
      broadcast("error", { revision: latestRevision, message: latestError });
    });
    buildQueue = run;
    return run;
  }
  let debounceTimer;
  function scheduleRebuild() {
    if (closed) return;
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      debounceTimer = void 0;
      void rebuild();
    }, DEBOUNCE_MS);
  }
  let themeCheckInFlight = false;
  async function checkThemeSource() {
    if (themeCheckInFlight) return;
    themeCheckInFlight = true;
    const generation = buildGeneration;
    try {
      const current = (await collectDeckThemeInputs(options.target, { cwd })).key;
      if (closed || building || generation !== buildGeneration) return;
      if (current !== lastThemeInputsKey) scheduleRebuild();
    } finally {
      themeCheckInFlight = false;
    }
  }
  const server = createServer((req, res) => {
    const pathname = (req.url ?? "/").split("?")[0];
    if (req.method === "GET" && pathname === "/") {
      const current = status();
      res.writeHead(200, {
        "Content-Type": "text/html; charset=utf-8",
        "X-Pptwise-Build-Status": current.latestOk ? "ok" : "failed",
        "X-Pptwise-Served-Revision": String(current.servedRevision),
        "X-Pptwise-Latest-Revision": String(current.latestRevision)
      });
      res.end(cachedHtml);
      return;
    }
    if (req.method === "GET" && pathname === "/status") {
      res.writeHead(200, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" });
      res.end(JSON.stringify(status()));
      return;
    }
    if (req.method === "GET" && pathname === "/events") {
      res.writeHead(200, {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache, no-transform",
        Connection: "keep-alive"
      });
      res.write("retry: 2000\n\n");
      sseClients.add(res);
      res.on("close", () => sseClients.delete(res));
      res.on("error", () => sseClients.delete(res));
      return;
    }
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("not found");
  });
  let watchers;
  let heartbeat;
  let themePoll;
  function teardownWatchersAndTimers() {
    closed = true;
    if (heartbeat) clearInterval(heartbeat);
    if (themePoll) clearInterval(themePoll);
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = void 0;
    watchers?.close();
  }
  function onWatchError(e) {
    if (closed) return;
    latestError = messageOf2(e);
    broadcast("error", { revision: latestRevision, message: latestError });
    scheduleRebuild();
  }
  try {
    watchers = watchTree(currentWatchRoots(), scheduleRebuild, onWatchError, { ceilingDir: watchCeiling });
    const initial = await buildDeckPreview(options.target, { cwd });
    cachedHtml = injectServeClient(initial.html);
    latestRevision = 1;
    servedRevision = 1;
    recordThemeInputs(initial.themeInputs);
    watchedTarget = { resolvedTarget: initial.resolvedTarget, isDir: initial.isDir };
    watchers.update(currentWatchRoots());
    heartbeat = setInterval(() => writeToAll(": heartbeat\n\n"), HEARTBEAT_MS);
    themePoll = setInterval(() => void checkThemeSource(), THEME_POLL_MS);
    await new Promise((resolveListen, rejectListen) => {
      const onError = (err) => {
        server.removeListener("listening", onListening);
        rejectListen(err);
      };
      const onListening = () => {
        server.removeListener("error", onError);
        resolveListen();
      };
      server.once("error", onError);
      server.once("listening", onListening);
      server.listen(requestedPort, "127.0.0.1");
    });
  } catch (e) {
    teardownWatchersAndTimers();
    if (e.code === "EADDRINUSE") {
      throw new PptwiseError(`port ${requestedPort} is already in use \u2014 pick a different one with --port`);
    }
    throw e;
  }
  openBuildQueue();
  const address = server.address();
  const actualPort = typeof address === "object" && address !== null ? address.port : requestedPort;
  let serverClosed = false;
  async function close() {
    if (serverClosed) return;
    serverClosed = true;
    teardownWatchersAndTimers();
    for (const res of sseClients) res.end();
    sseClients.clear();
    if (typeof server.closeIdleConnections === "function") server.closeIdleConnections();
    if (typeof server.closeAllConnections === "function") server.closeAllConnections();
    await new Promise((resolveClose, rejectClose) => {
      server.close((err) => err ? rejectClose(err) : resolveClose());
    });
  }
  return { server, rebuild, status, close, url: `http://127.0.0.1:${actualPort}`, port: actualPort };
}
function openBrowser(url) {
  const command = osPlatform() === "darwin" ? "open" : "xdg-open";
  try {
    const child = spawnHidden(command, [url], { stdio: "ignore", detached: true });
    child.on("error", () => {
    });
    child.unref();
  } catch {
  }
}
async function runServe(target, opts = {}) {
  const handle = await createServeServer({ target, port: opts.port, cwd: opts.cwd });
  console.log(`pptwise serve: ${handle.url} (Ctrl+C to stop)`);
  if (opts.open !== false) openBrowser(handle.url);
  process.on("SIGINT", () => {
    void handle.close().then(
      () => process.exit(0),
      () => process.exit(1)
    );
  });
}

// src/cli.ts
installNodePlatform();
var program = new Command();
program.name("pptwise").description("Stable, editable PPTX generation for AI agents \u2014 semantic IR in, native DrawingML out").version(VERSION).showHelpAfterError();
function fail(e) {
  console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
}
program.command("render").description("Render an IR JSON file or deck project directory to a .pptx").argument("<target>", "IR JSON file or deck project directory").option("-o, --output <file>", "output .pptx path (default: .pptwise/<deck>/<deck>.pptx under the project root)").option("--draft", "allow unfilled placeholder pages (skip the draft gate)").option(
  "--allow-dropped-content",
  "export anyway when a page holds more than fits and the layout drops blocks (skip the content-drop gate)"
).option("--no-git-ignore", "do not write .pptwise/.gitignore or add .pptwise/ to this repository's local exclude file").action(
  async (target, opts) => {
    try {
      console.log(
        await runRender(target, {
          output: opts.output,
          draft: opts.draft,
          allowDroppedContent: opts.allowDroppedContent,
          gitIgnore: opts.gitIgnore,
          cwd: process.cwd()
        })
      );
    } catch (e) {
      fail(e);
    }
  }
);
program.command("build").description(
  "Assemble, validate, audit, preview and render a deck in one pass. Writes the pages and, only when every check passes, the deck's one .pptx under .pptwise/<deck>/ \u2014 exits 1 when the deck needs revision"
).argument("<target>", "deck project directory or IR JSON file").option("--json", "print the full report: status, every problem with its page, file and field, which pages the theme's signature layouts drew and the nearest recipe for the rest, the preview, and the .pptx path").option("--no-git-ignore", "do not write .pptwise/.gitignore or add .pptwise/ to this repository's local exclude file").option(
  "--alternatives",
  "also draw the deck's cover and one or two content pages in up to 3 other themes, under .pptwise/<deck>/alternatives/ (done once by default, on the first build of a deck on a built-in theme)"
).option("--no-alternatives", "do not draw the deck in other themes, even on its first build").addHelpText("after", "\nExample:\n  $ pptwise build my-deck/ --json").action(async (target, opts) => {
  try {
    const { output, ok } = await runBuild(target, {
      json: opts.json,
      gitIgnore: opts.gitIgnore,
      alternatives: opts.alternatives,
      cwd: process.cwd()
    });
    console.log(output);
    if (!ok) process.exitCode = 1;
  } catch (e) {
    fail(e);
  }
});
program.command("validate").description("Validate an IR JSON file or deck project directory against the schema").argument("<target>", "IR JSON file or deck project directory").action(async (target) => {
  try {
    console.log(await runValidate(target, process.cwd()));
  } catch (e) {
    fail(e);
  }
});
program.command("audit").description(
  "Deterministic geometry audit (overflow, out-of-bounds, low-contrast, overlap, content-truncated, content-dropped, stepped-aside, monotony), plus an optional --pixels contrast pass \u2014 exits 1 when it finds anything"
).argument("<target>", "IR JSON file or deck project directory").option("--json", "machine-readable output (the full AuditReport)").option("--pixels", "also run the optional pixel-contrast pass over image-backed text (requires sharp)").action(async (target, opts) => {
  try {
    const { output, hasFindings } = await runAudit(target, {
      json: opts.json,
      pixels: opts.pixels
    });
    console.log(output);
    if (hasFindings) process.exit(1);
  } catch (e) {
    fail(e);
  }
});
program.command("asset-brief").description(
  "Image-generation brief for every image slot in a deck: the real rendered frame, fit/crop mode, suggested pixel size, theme palette/mood, and a paste-ready prompt"
).argument("<target>", "IR JSON file or deck project directory").option("--json", "machine-readable output (the full AssetBrief)").action(async (target, opts) => {
  try {
    console.log(await runAssetBrief(target, { json: opts.json }));
  } catch (e) {
    fail(e);
  }
});
program.command("schema").description("Print the IR JSON Schema (feed this to a model before it writes IR)").option("--spec", "print the deck spec schema instead").option("--component <type>", "print one component's schema with the $defs it needs").option("--kind <kind>", "print the components a page of this kind may hold, with their schemas").option("--theme <name>", "with --kind: answer for one theme instead of every built-in theme (deck theme.json, then workspace themes/, then installed packs, then presets)").option("--deck <dir>", "with --theme: the deck project directory to read a deck-local theme from (default: the cwd when it holds deck.spec.json or a deck-local theme file for the name)").option("--pretty", "indent the JSON (default output is one line)").addHelpText(
  "after",
  "\nExamples:\n  $ pptwise schema --spec\n  $ pptwise schema --kind fact --theme brief\n  $ pptwise schema --kind quote --theme acme --deck my-deck/\n  $ pptwise schema --component kpi_cards\n\nOne page of a deck project, with the keys its page file takes and the components its face draws:\n  $ pptwise inspect <deck> --page <id>"
).action(async (opts) => {
  try {
    console.log(await runSchema(opts));
  } catch (e) {
    fail(e);
  }
});
program.command("inspect").description(
  "Show one page's fill contract: the spec's locked fields, the page file's fields, the components its face draws, the theme's signature layouts for the page with the recipe to write for each, the counts validate holds it to, and validate's findings on it. Exits 1 when the page has an error"
).argument("<deck>", "deck project directory").requiredOption("--page <id>", "the page id in deck.spec.json").option("--component <type>", "expand one component the page may hold: its story, its limits on this page, and its schema").option("--fit", "draw the page and report whether its content fits, as render's content-drop gate would judge it. Exits 1 when it does not").option("--json", "print the report as one line of JSON").addHelpText(
  "after",
  "\nExamples:\n  $ pptwise inspect my-deck/ --page growth\n  $ pptwise inspect my-deck/ --page growth --component chart\n  $ pptwise inspect my-deck/ --page growth --fit"
).action(async (target, opts) => {
  try {
    const { output, failed } = await runInspect(target, {
      page: opts.page,
      component: opts.component,
      fit: opts.fit,
      json: opts.json
    });
    console.log(output);
    if (failed) process.exit(1);
  } catch (e) {
    fail(e);
  }
});
program.command("icons").description("List every icon name an `icon` field accepts").option("--json", "machine-readable output").action((opts) => console.log(runIcons(Boolean(opts.json))));
var spec = program.command("spec").description("Deck spec commands (spec \xA76)");
spec.command("validate").description("Validate a deck spec JSON file against the schema and strategy-aware hard gates").argument("<spec.json>").option("--json", "print the result as JSON: the pages in order (number, id, type, kind, heading, summary), theme, narrative and warnings, or every error").action(async (specPath, opts) => {
  try {
    if (opts.json) {
      const { output, ok } = await runSpecValidateJson(specPath);
      console.log(output);
      if (!ok) process.exitCode = 1;
      return;
    }
    console.log(await runSpecValidate(specPath));
  } catch (e) {
    fail(e);
  }
});
program.command("assemble").description("Assemble a deck project directory (deck.spec.json + pages/ + assets/) into an IR JSON file").argument("<dir>", "deck project directory").option("-o, --output <file>", "output IR JSON path (default: <dir>/deck.json)").action(async (target, opts) => {
  try {
    console.log(await runAssemble(target, { output: opts.output }));
  } catch (e) {
    fail(e);
  }
});
program.command("disassemble").description("Split an IR JSON file into a deck project directory (deck.spec.json + pages/)").argument("<ir.json>", "path to the IR file").requiredOption("-o, --output <dir>", "output deck project directory").action(async (irPath, opts) => {
  try {
    console.log(await runDisassemble(irPath, opts.output));
  } catch (e) {
    fail(e);
  }
});
program.command("themes").description("List the built-in presets and the themes of installed content packs").option("--json", "machine-readable output (each theme's source is builtin or pack)").action(async (opts) => {
  try {
    console.log(await runThemes(Boolean(opts.json)));
  } catch (e) {
    fail(e);
  }
});
var theme = program.command("theme").description("Copy, fork, and compare themes");
theme.command("new").description("Copy a preset or named theme into a self-contained v2 theme file").requiredOption("--from <preset>", "preset or theme name to copy").option("-o, --output <path>", "output theme JSON path").option("--id <id>", "theme id (default: slug of the output filename)").option("--label <label>", "human-readable theme label").option("--force", "overwrite an existing theme file").addHelpText("after", "\nExample:\n  $ pptwise theme new --from brief -o themes/acme.theme.json").action(async (opts) => {
  try {
    console.log(await runThemeNew({ from: opts.from, output: opts.output, id: opts.id, label: opts.label, force: opts.force, cwd: process.cwd() }));
  } catch (e) {
    fail(e);
  }
});
theme.command("fork").description("Copy a theme and repaint it: around one brand color with --brand, or with exact anchor colors").argument("<name>", "preset or theme name to fork").option(
  "--brand <hex[,hex]>",
  "brand color, and optionally the company's second color after a comma: the theme keeps its ground and text, the brand takes its most visible color slot, and the other colors are drawn from it"
).option("--primary <hex>", "set colors.primary exactly (instead of --brand)").option("--bg <hex>", "set colors.bg exactly (with --primary)").option("--accent <hex>", "set colors.accent exactly (with --primary)").option("--text <hex>", "set colors.text exactly (with --primary)").option("--surface <hex>", "set colors.surface exactly (with --primary)").option("-o, --output <path>", "output theme JSON path").option("--id <id>", "theme id (default: slug of the output filename)").option("--label <label>", "human-readable theme label").option("--force", "overwrite an existing theme file").addHelpText(
  "after",
  "\nPass --brand alone, or --primary with any of --accent, --bg, --text, --surface. The two ways do not mix: --brand decides every color slot itself, the anchor flags set the slots you name exactly.\n\nExamples:\n  $ pptwise theme fork ink --brand #C8102E -o themes/acme.theme.json\n  $ pptwise theme fork brief --brand '#156082,#E97132' -o themes/acme.theme.json\n  $ pptwise theme fork acme --primary #0B5FFF -o themes/acme-blue.theme.json"
).action(
  async (name, opts) => {
    try {
      console.log(
        await runThemeFork(name, {
          brand: opts.brand,
          primary: opts.primary,
          bg: opts.bg,
          accent: opts.accent,
          text: opts.text,
          surface: opts.surface,
          output: opts.output,
          id: opts.id,
          label: opts.label,
          force: opts.force,
          cwd: process.cwd()
        })
      );
    } catch (e) {
      fail(e);
    }
  }
);
theme.command("try").description(
  "Render the fitting-room sample across 2-4 themes into a contact sheet, or, with --title, your own cover and one content page in any number of themes as SVG files with a manifest"
).argument("[ids]", "comma-separated theme ids (2-4 for the fixed sample), or all with --title. With --title and no ids, a shortlist of four to six").option("-o, --output <dir>", "output directory (default: .pptwise/theme-try/)").option("--title <text>", "draw this cover title, plus one content page, instead of the fixed sample").option("--subtitle <text>", "with --title: the cover's subheading").option("--lang <lang>", "with --title: language of the default content page, zh or en (default: zh when the title has Chinese, Japanese or Korean characters)").option("--page <file>", "with --title: one content page as a deck page carries it (type, kind, heading, components), in place of the default").option("--json", "with --title: print the manifest as JSON").option("--occasion <words>", "with --title and no ids: occasion words or a narrative preset, comma-separated, that pick the shortlist").addHelpText(
  "after",
  '\nExamples:\n  $ pptwise theme try brief,swiss,memo\n  $ pptwise theme try all --title "Q3 review" --subtitle "Board meeting" --json\n  $ pptwise theme try --title "Q3 review" --occasion business --json'
).action(
  async (ids, opts) => {
    try {
      console.log(
        await runThemeTry(ids, {
          output: opts.output,
          cwd: process.cwd(),
          title: opts.title,
          subtitle: opts.subtitle,
          lang: opts.lang,
          page: opts.page,
          json: opts.json,
          occasion: opts.occasion
        })
      );
    } catch (e) {
      fail(e);
    }
  }
);
program.command("layouts").description("List registered layouts").option("--json", "machine-readable output").action((opts) => console.log(runLayouts(Boolean(opts.json))));
var brand = program.command("brand").description("Brand asset commands \u2014 extract your company's colors/fonts from an Office template");
brand.command("extract").description(
  "Read the brand color (accent1) and its second color (accent2) from a .thmx/.potx/.pptx file and repaint a theme around them, into a pptwise theme file \u2014 runs entirely locally, the file never leaves your machine"
).argument("<file>", "a .thmx theme, .potx template, or .pptx presentation").requiredOption("-o, --output <file>", "output theme JSON path (e.g. my-brand.theme.json)").option("--id <id>", "theme id to register under (default: slug of the output filename)").option("--label <label>", "human-readable theme label (default: the source theme's color-scheme name)").option("--from <preset>", "theme to repaint around the template's brand color, keeping its ground, text, fonts, and menu (default: bulletin)").option(
  "--brand-fonts",
  "put the template's Latin heading and body fonts ahead of the theme's own (Chinese text keeps the theme's faces). A font off the safe font list never reaches the slides, and one without an exact width table may overflow: the command warns about both"
).option("--force", "overwrite an existing theme file").addHelpText("after", "\nExample:\n  $ pptwise brand extract corp.pptx -o themes/acme.theme.json --from bulletin").action(async (file, opts) => {
  try {
    console.log(await runBrandExtract(file, {
      output: opts.output,
      id: opts.id,
      label: opts.label,
      from: opts.from,
      brandFonts: opts.brandFonts,
      force: opts.force
    }));
  } catch (e) {
    fail(e);
  }
});
program.command("narratives").description("List named narrative presets (strategy/pacing/audience axes + theme recommendations)").option("--json", "machine-readable output").action((opts) => console.log(runNarratives(Boolean(opts.json))));
var config = program.command("config").description("User-level settings (API keys for optional stock-photo search)");
config.command("set <key> [value]").description("Set a user config value. Omit the value for an apiKey or clientSecret to enter it at a hidden prompt").action(async (key, value) => {
  try {
    console.log(await runConfigSet(key, value));
  } catch (e) {
    fail(e);
  }
});
config.command("show").description("Show the effective user config (API keys masked)").action(async () => {
  try {
    console.log(await runConfigShow());
  } catch (e) {
    fail(e);
  }
});
var license = program.command("license").description("The license key that unlocks content packs");
license.command("set <key>").description("Save a license key to $PPTWISE_HOME/license.json (readable by you only)").action(async (key) => {
  try {
    console.log(await runLicenseSet(key));
  } catch (e) {
    fail(e);
  }
});
license.command("status").description("Show whether a license key is configured (first 8 characters only)").action(async () => {
  try {
    console.log(await runLicenseStatus());
  } catch (e) {
    fail(e);
  }
});
license.command("clear").description("Remove the saved license key. Installed packs stay in place").action(async () => {
  try {
    console.log(await runLicenseClear());
  } catch (e) {
    fail(e);
  }
});
var packs = program.command("packs").description("Content packs: extra themes installed under $PPTWISE_HOME/packs");
packs.command("sync").description(
  "Install or update every pack your license covers. Without a license it prints a one-line note and exits 0. A failed sync leaves installed packs as they were"
).option("--json", "machine-readable output").action(async (opts) => {
  try {
    const { output, failed } = await runPacksSync({ json: opts.json });
    console.log(output);
    if (failed) process.exitCode = 1;
  } catch (e) {
    fail(e);
  }
});
packs.command("list").description("List installed packs and the themes each one ships").option("--json", "machine-readable output").action(async (opts) => {
  try {
    console.log(await runPacksList({ json: opts.json }));
  } catch (e) {
    fail(e);
  }
});
function parsePositiveInt(raw, flag) {
  if (!/^[0-9]+$/.test(raw)) {
    fail(new Error(`invalid ${flag} "${raw}" \u2014 expected a positive integer`));
  }
  return Number(raw);
}
var images = program.command("images").description("Search and pin stock photos into workspace assets");
images.command("search <query>").description("Search Pexels, then Pixabay, then Openverse (cc0/pdm) and print attribution lines").option("--orientation <orientation>", "landscape, portrait, or square").option("--color <color>", "color name or hex for the search API").option("--min-width <px>", "client-side minimum width in pixels").option("--min-height <px>", "client-side minimum height in pixels").action(
  async (query, opts) => {
    try {
      console.log(
        await runImagesSearch(query, {
          orientation: opts.orientation,
          color: opts.color,
          minWidth: opts.minWidth !== void 0 ? parsePositiveInt(opts.minWidth, "--min-width") : void 0,
          minHeight: opts.minHeight !== void 0 ? parsePositiveInt(opts.minHeight, "--min-height") : void 0
        })
      );
    } catch (e) {
      fail(e);
    }
  }
);
images.command("fetch <ref>").description("Download a photo (pexels:<id>, pixabay:<id>, or openverse:<id>) into .pptwise/<deck>/assets/").requiredOption("--deck <dir>", "deck project directory or IR JSON file").requiredOption("--as <asset_id>", "local asset id (filename without extension)").option("--query <text>", "search query that produced this pick (stored in the sidecar)").action(async (ref, opts) => {
  try {
    console.log(
      await runImagesFetch(ref, { deck: opts.deck, as: opts.as, query: opts.query, cwd: process.cwd() })
    );
  } catch (e) {
    fail(e);
  }
});
images.command("list").description("List pinned stock photos for a deck").requiredOption("--deck <dir>", "deck project directory or IR JSON file").action(async (opts) => {
  try {
    console.log(await runImagesList({ deck: opts.deck, cwd: process.cwd() }));
  } catch (e) {
    fail(e);
  }
});
images.command("generate").description("Generate an image with a local CLI (grok, codex, or antigravity) and pin it").requiredOption("--deck <dir>", "deck project directory or IR JSON file").requiredOption("--as <asset_id>", "local asset id (filename without extension)").option("--prompt <text>", "image prompt (otherwise taken from asset-brief)").action(async (opts) => {
  try {
    console.log(
      await runImagesGenerate({ deck: opts.deck, as: opts.as, prompt: opts.prompt, cwd: process.cwd() })
    );
  } catch (e) {
    fail(e);
  }
});
program.command("init").description("Scaffold a pptwise.config.json in the current directory").action(async () => {
  try {
    console.log(await runInit());
  } catch (e) {
    fail(e);
  }
});
program.command("preview").description("Render each slide to an SVG file for visual self-check").argument("<target>", "IR JSON file or deck project directory").option("-o, --output <dir>", "output directory (default: .pptwise/<deck>/ under the project root)").option("--html", "also write a self-contained preview.html (all slides inlined \u2014 thumbnail strip, keyboard navigation) for human review").option("--no-git-ignore", "do not write .pptwise/.gitignore or add .pptwise/ to this repository's local exclude file").action(async (target, opts) => {
  try {
    console.log(
      await runPreview(target, opts.output, {
        htmlOut: opts.html,
        gitIgnore: opts.gitIgnore,
        cwd: process.cwd()
      })
    );
  } catch (e) {
    fail(e);
  }
});
program.command("serve").description("Serve a live-reloading HTML preview of an IR JSON file or deck project directory over HTTP").argument("<target>", "IR JSON file or deck project directory").option("--port <number>", `port to listen on (default ${DEFAULT_PORT})`).option("--no-open", "do not open the URL in a browser after starting").action(async (target, opts) => {
  try {
    let port;
    if (opts.port !== void 0) {
      port = Number(opts.port);
      if (!Number.isInteger(port)) {
        fail(new Error(`invalid --port value "${opts.port}" \u2014 expected an integer`));
      }
    }
    await runServe(target, { port, open: opts.open });
  } catch (e) {
    fail(e);
  }
});
program.command("doctor").description(
  "Diagnose this machine's install: installed skill copies and what each pins, dsh plugin status, Node/Bun against the engines floor, the optional sharp/soffice capabilities, and a self-test render \u2014 exits 1 only on a hard failure"
).option("--json", "machine-readable output (the full DoctorReport)").action(async (opts) => {
  try {
    const { output, hasErrors } = await runDoctor({ json: opts.json });
    console.log(output);
    if (hasErrors) process.exit(1);
  } catch (e) {
    fail(e);
  }
});
program.command("check-update").description("Check npm for a newer pptwise release").action(async () => {
  const info = await checkForUpdate({ currentVersion: VERSION });
  if (!info.checked) fail(new Error(`update check failed: ${info.error}`));
  console.log(
    info.updateAvailable ? `update available: ${info.currentVersion} \u2192 ${info.latestVersion} (run \`pptwise self-update\`)` : `pptwise ${info.currentVersion} is up to date`
  );
});
program.command("self-update").description("Update the global pptwise install to the latest release").action(async () => {
  try {
    const result = await createSelfUpdater()({ currentVersion: VERSION });
    console.log(
      result.updated ? `updated: ${result.currentVersion} \u2192 ${result.latestVersion}` : `already at the latest version (${result.currentVersion})`
    );
  } catch (e) {
    fail(e);
  }
});
program.parseAsync(process.argv, { from: "node" }).catch(fail);
//# sourceMappingURL=cli.js.map