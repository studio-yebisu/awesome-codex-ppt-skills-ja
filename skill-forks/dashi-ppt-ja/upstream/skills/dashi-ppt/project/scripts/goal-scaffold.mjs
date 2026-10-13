#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import {
  compactJson,
  isCoverCandidate,
  isCoverLikeLayout,
  inspectLayout,
  listLayouts,
  parseArgs,
} from './skill-workflow-utils.mjs';
import {
  hashSeed,
  listLayoutsForContentPacks,
  materializeTemplateProjection,
} from './workflow/layout-query.mjs';
import { allocateDeckLayouts } from './workflow/layout-allocation.mjs';
import {
  beginWorkflowStage,
  workflowRunIdForScaffold,
  workflowTelemetryPath,
} from './workflow-telemetry.mjs';
import {
  BESPOKE_CHART_POINT_LIMIT,
  BESPOKE_LIST_ITEM_LIMIT,
  classifyPageIntent,
  normalizePageContentPack,
  pageContentProjectionItems,
} from '../src/variant-contract.mjs';
import { validateGoalSpec } from './validate-goal-spec.mjs';

const BESPOKE_VARIANT_ID = 'v4';
const BESPOKE_MEDIA_LIMITS = { statement: 0, metric: 0, ledger: 0, chart: 4, media: 8 };
let lastAllocationDiagnostics = null;
let lastGenerationMetrics = null;

// 相对路径按调用方目录解析:npm run(含 --prefix)会把脚本 cwd 切到项目根,INIT_CWD 才是用户所在目录。
const CALLER_CWD = process.env.INIT_CWD || process.cwd();

const DEFAULT_BODY_ROLES = [
  'statement',
  'breakdown',
  'context',
  'metrics',
  'comparison',
  'distribution',
  'relationship',
  'case',
  'image',
  'trend',
  'process',
  'risks',
  'actions',
  'result',
];

const BODY_ROLES = new Set([
  ...DEFAULT_BODY_ROLES,
  'transition',
  'observation',
  'ambient',
  'team',
]);

const args = parseArgs(process.argv.slice(2));

if (args.help || args.h) {
  printUsage();
  process.exit(0);
}

const contentPlanArg = args.contentPlan || args['content-plan'];
const scaffoldOut = typeof args.out === 'string' && args.out.trim()
  ? path.resolve(CALLER_CWD, args.out)
  : null;
const scaffoldRunId = contentPlanArg && scaffoldOut
  ? workflowRunIdForScaffold(scaffoldOut)
  : null;
const scaffoldTelemetry = scaffoldRunId
  ? beginWorkflowStage({
      goalPath: scaffoldOut,
      telemetryFile: workflowTelemetryPath(scaffoldOut),
      runId: scaffoldRunId,
      stage: 'scaffold',
    })
  : null;

try {
  run();
  scaffoldTelemetry?.finish({ ok: true, metrics: lastGenerationMetrics });
} catch (error) {
  scaffoldTelemetry?.finish({ ok: false, error });
  console.error(error.message);
  process.exit(1);
}

function run() {
  const title = String(args.title || '').trim() || 'PPT';
  const goal = String(args.goal || '').trim() || title;
  const themePack = String(args.theme || args.themePack || '').trim();
  const pageCount = Math.max(1, Math.min(50, Number(args.pages || args.pageCount || args['page-count']) || 0));
  const chunkSize = Number(args.chunkSize || args['chunk-size']) || 0;
  const layoutVariantsArg = args.layoutVariants ?? args['layout-variants'];
  const layoutVariants = layoutVariantsArg === undefined ? 3 : Number(layoutVariantsArg);
  const out = String(args.out || '').trim();
  const mediaIntent = parseMediaIntent(args);
  const contentPlan = contentPlanArg ? readContentPlan(contentPlanArg, pageCount) : null;

  if (!themePack) throw new Error('Missing --theme <themePack>');
  if (!pageCount) throw new Error('Missing --pages <n>');
  if (!out) throw new Error('Missing --out <goal.json>');
  if (layoutVariantsArg === true || ![1, 3].includes(layoutVariants)) {
    throw new Error('--layout-variants must be 1 or 3');
  }
  if (contentPlan && layoutVariants !== 3) {
    throw new Error('--content-plan requires --layout-variants 3');
  }
  if (!contentPlan && layoutVariants === 3) {
    throw new Error('--layout-variants 3 requires --content-plan <PageContentPack JSON>');
  }

  const { roles, explicit: rolesExplicit } = contentPlan
    ? { roles: [], explicit: false }
    : parseRoles(args.roles, Math.max(0, pageCount - 2));
  // 选页 seed:同分候选随机打散,让不同用户/不同次 scaffold 的骨架不再成片雷同;
  // --seed 显式传入时可复现同一份骨架。
  const seed = args.seed !== undefined && args.seed !== true ? String(args.seed) : String(Math.floor(Math.random() * 0xffffffff));
  const slides = buildSlides({
    themePack,
    pageCount,
    roles,
    rolesExplicit,
    mediaIntent,
    seed,
    layoutVariants,
    contentPlan,
  });
  const spec = {
    ...(layoutVariants === 3
      ? {
          schemaVersion: 2,
          variantOutputMode: 'comparison',
        }
      : {}),
    title,
    goal,
    themePack,
    pageCount,
    randomSeed: seed,
    ...(scaffoldRunId ? { workflowRunId: scaffoldRunId } : {}),
    slides,
  };
  const errors = validateGoalSpec(spec, contentPlan ? {} : {
    allowUnfilledMediaIntent: true,
    allowUnfilledBespoke: true,
    allowUnfilledContent: true,
  });
  if (errors.length) throw new Error(`Scaffold failed goal spec validation:\n- ${errors.join('\n- ')}`);

  writeJson(out, spec);
  const fillPlanOut = writeFillPlan(out, spec);
  writeChunks(out, spec, chunkSize);
  process.stdout.write(compactJson({
    out: path.resolve(CALLER_CWD, out),
    fillPlanOut,
    themePack,
    pageCount,
    layoutVariants,
    slideCount: slides.length,
    chunkSize: chunkSize || null,
    ...(lastAllocationDiagnostics ? { allocation: lastAllocationDiagnostics } : {}),
  }));
}

function buildSlides({
  themePack,
  pageCount,
  roles,
  rolesExplicit,
  mediaIntent,
  seed = null,
  layoutVariants = 3,
  contentPlan = null,
}) {
  if (contentPlan) {
    return buildContentPlanSlides({ themePack, contentPlan, seed });
  }
  if (layoutVariants !== 1) throw new Error('Schema v2 scaffolding requires --content-plan');
  const used = new Set();
  let mediaAssigned = false;
  const slides = Array.from({ length: pageCount }, (_, index) => {
    const isCover = index === 0;
    const isClosing = pageCount > 1 && index === pageCount - 1;
    const isBody = !isCover && !isClosing;
    const bodyIndex = index - 1;
    const useMediaIntent = Boolean(mediaIntent && !mediaAssigned && isBody);
    let role = isCover
      ? 'cover'
      : isClosing
        ? 'closing'
        : rolesExplicit
          ? roles[bodyIndex]
          : roles[bodyIndex % roles.length];
    if (useMediaIntent) role = 'image';

    const layout = pickLayout({
      themePack,
      role,
      used,
      body: !isCover,
      mediaIntent: useMediaIntent ? mediaIntent : null,
      seed: `${seed}:slide-${index + 1}`,
    });
    used.add(layout);
    if (useMediaIntent) mediaAssigned = true;
    return {
      layout,
      props: {},
      ...(useMediaIntent ? { [mediaIntent.field]: mediaIntent.value } : {}),
    };
  });
  if (mediaIntent && !mediaAssigned) {
    throw new Error(`No body slide available for ${mediaIntent.field}; use --pages 3 or more`);
  }
  return slides;
}


function buildContentPlanSlides({ themePack, contentPlan, seed }) {
  const bespokeFamilies = planBespokeFamilies(contentPlan);
  const bespokeVariants = contentPlan.map((page, pageIndex) => buildCanonicalBespoke(
    page.presentation,
    { pageIndex, family: bespokeFamilies[pageIndex], logicalId: page.id },
  ));
  const candidateMatrix = listLayoutsForContentPacks({
    theme: themePack,
    pages: contentPlan,
    limit: 50,
    seed,
  });
  const descriptors = contentPlan.map((page, pageIndex) => {
    const wantsCover = classifyPageIntent(page.presentation.pageIntent) === 'cover';
    const coverCandidates = candidateMatrix[pageIndex].filter(item => isCoverCandidate(item.layout));
    const bodyCandidates = candidateMatrix[pageIndex].filter(item => !isCoverCandidate(item.layout) && !isCoverLikeLayout(item.layout));
    const candidates = wantsCover && supportsThreeTemplateCompositions(coverCandidates)
      ? coverCandidates
      : bodyCandidates;
    if (candidates.length < 3) {
      throw new Error(`PageContentPack ${page.id} has ${candidates.length} compatible template layouts in ${themePack}; required 3`);
    }
    return { ...page, candidates };
  });
  const { assignments, diagnostics } = allocateDeckLayouts(
    descriptors.map(item => item.candidates),
    seed,
  );
  lastAllocationDiagnostics = diagnostics;
  lastGenerationMetrics = {
    planningPasses: 1,
    layoutQueryPasses: 1,
    projectionPlansEvaluated: candidateMatrix.reduce((sum, candidates) => sum + candidates.length, 0),
    allocationPasses: 1,
    materializationPasses: 1,
    materializedVariants: descriptors.length * 3,
    pageCount: descriptors.length,
  };
  return descriptors.map((page, pageIndex) => ({
    id: page.id,
    content: { presentation: page.presentation },
    selectedVariant: 'v1',
    variants: [
      ...assignments[pageIndex].map((candidate, variantIndex) => {
        const projection = materializeTemplateProjection(candidate, page.presentation, variantIndex);
        return {
          id: `v${variantIndex + 1}`,
          kind: 'template',
          layout: candidate.layout,
          contentMap: projection.contentMap,
          projection: {
            chartMode: projection.projectionPlan.chartMode,
            contentPaths: projection.contentPaths,
            projectedItemIds: projection.projectedItemIds,
            chartBindings: projection.chartBindings,
            structure: projection.structure,
          },
        };
      }),
      bespokeVariants[pageIndex],
    ],
  }));
}

function supportsThreeTemplateCompositions(candidates) {
  return candidates.length >= 3 && new Set(candidates.map(item => (
    item.structureFingerprint?.composition || item.layout
  ))).size >= 3;
}

function buildCanonicalBespoke(presentation, options = {}) {
  const chartData = presentation.chartData || [];
  if (chartData.length > BESPOKE_CHART_POINT_LIMIT) throw new Error(`Bespoke slide ${options.logicalId || 'unknown'} has ${chartData.length} chart points; limit=${BESPOKE_CHART_POINT_LIMIT}`);
  assertBespokeFamilyCapacity(presentation, options.family, options.logicalId);
  return buildBespokeFamily(presentation, options);
}

function planBespokeFamilies(contentPlan) {
  const counts = new Map();
  let previous = null;
  return contentPlan.map(({ presentation }) => {
    const eligible = eligibleBespokeFamilies(presentation);
    const family = eligible
      .map((value, index) => ({ value, index }))
      .sort((left, right) => (
        Number(left.value === previous) - Number(right.value === previous)
        || (counts.get(left.value) || 0) - (counts.get(right.value) || 0)
        || left.index - right.index
      ))[0].value;
    counts.set(family, (counts.get(family) || 0) + 1);
    previous = family;
    return family;
  });
}

function eligibleBespokeFamilies(presentation) {
  if (presentation.chartData?.length) return ['chart'];
  if (presentation.media?.length) return ['media'];
  const items = pageContentProjectionItems(presentation);
  if (!items.length) return ['statement'];
  const valued = items.filter(item => item.hasValue);
  return [
    ...(valued.length ? ['metric'] : []),
    'statement',
    'ledger',
  ];
}

function assertBespokeFamilyCapacity(presentation, family, logicalId) {
  const mediaCount = presentation.media?.length || 0;
  const limit = BESPOKE_MEDIA_LIMITS[family];
  if (limit == null) throw new Error(`Bespoke slide ${logicalId || 'unknown'} has unknown family "${family}"`);
  if (mediaCount > limit) throw new Error(`Bespoke slide ${logicalId || 'unknown'} family ${family} supports at most ${limit} media items; received ${mediaCount}`);
}

function buildBespokeFamily(presentation, { pageIndex = 0, family = 'ledger', logicalId } = {}) {
  const items = pageContentProjectionItems(presentation);
  const metricItems = family === 'metric' ? items.filter(item => item.hasValue).slice(0, 2) : [];
  const metricIds = new Set(metricItems.map(item => item.id));
  const itemIds = new Set(items.map(item => item.id));
  const factSourceItems = selectBespokeListItems(items.filter(item => !metricIds.has(item.id)), logicalId);
  const chartFactItems = family === 'chart' ? [] : (presentation.chartData || []).filter(item => !itemIds.has(item.id));
  const factCount = factSourceItems.length + chartFactItems.length;
  const compositionIndex = pageIndex % 3;
  const mirror = pageIndex % 2 === 1;
  const prefix = `bespoke-${family}`;
  const text = (slot, grid, role = 'body') => ({ id: `${prefix}-${slot}`, type: 'text', grid, role });
  const elements = [];
  if (family === 'statement') {
    const statementColumn = mirror ? 4 : 1;
    elements.push(
      text('kicker', { column: mirror ? 9 : 1, row: 1, width: 4, height: 1 }, 'kicker'),
      text('title', { column: statementColumn, row: 2, width: 8, height: 1 }, 'title'),
      { id: `${prefix}-core`, type: 'quote', grid: { column: statementColumn, row: 3, width: mirror || factCount ? 9 : 12, height: 5 } },
    );
    if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: mirror ? 1 : 10, row: 3, width: 3, height: 5 }, ordered: true });
  } else if (family === 'metric') {
    const heroColumn = mirror ? 6 : 1;
    const sideColumn = mirror ? 1 : 8;
    elements.push(
      text('kicker', { column: 1, row: 1, width: 3, height: 1 }, 'kicker'),
      text('title', { column: 4, row: 1, width: 9, height: 1 }, 'title'),
      text('core', { column: 1, row: 2, width: 8, height: 1 }, 'subtitle'),
      text('summary', { column: 9, row: 2, width: 4, height: 1 }, 'caption'),
    );
    metricItems.forEach((_, index) => elements.push({
      id: `${prefix}-value-${index + 1}`,
      type: 'metric',
      grid: index === 0
        ? { column: heroColumn, row: 3, width: 7, height: 5 }
        : { column: sideColumn, row: 3, width: 5, height: 2 },
      tone: index === 0 ? 'inverse' : 'accent',
    }));
    if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: sideColumn, row: metricItems.length > 1 ? 5 : 3, width: 5, height: metricItems.length > 1 ? 3 : 5 }, ordered: true });
  } else if (family === 'chart') {
    const media = presentation.media || [];
    if (compositionIndex === 0) {
      const chartColumn = mirror ? 5 : 1;
      const factsColumn = mirror ? 1 : 9;
      elements.push(
        text('kicker', { column: 1, row: 1, width: 3, height: 1 }, 'kicker'),
        text('title', { column: 4, row: 1, width: 9, height: 1 }, 'title'),
        text('core', { column: 1, row: 2, width: 8, height: 1 }, 'subtitle'),
        text('summary', { column: 9, row: 2, width: 4, height: 1 }, 'caption'),
        { id: `${prefix}-plot`, type: 'chart', grid: { column: chartColumn, row: 3, width: factCount ? 8 : 12, height: media.length ? 4 : 6 }, chartType: 'bar', showValues: true },
      );
      if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: factsColumn, row: 3, width: 4, height: media.length ? 4 : 6 }, ordered: true });
      addHorizontalMedia(elements, prefix, media, 0, { column: 1, row: 7, width: 12, height: 2 });
    } else if (compositionIndex === 1) {
      elements.push(
        text('kicker', { column: 1, row: 1, width: 4, height: 1 }, 'kicker'),
        text('title', { column: 1, row: 2, width: 4, height: 2 }, 'title'),
        text('core', { column: 1, row: 4, width: 4, height: 2 }, 'subtitle'),
        text('summary', { column: 1, row: 6, width: 4, height: 1 }, 'caption'),
        { id: `${prefix}-plot`, type: 'chart', grid: { column: 5, row: 1, width: 8, height: media.length ? 6 : 8 }, chartType: 'line', showValues: true },
      );
      if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: 1, row: 7, width: 4, height: 2 }, ordered: true });
      addHorizontalMedia(elements, prefix, media, 0, { column: 5, row: 7, width: 8, height: 2 });
    } else {
      elements.push(
        text('kicker', { column: 1, row: 1, width: 3, height: 1 }, 'kicker'),
        text('title', { column: 4, row: 1, width: 9, height: 1 }, 'title'),
        text('core', { column: 1, row: 2, width: 7, height: 1 }, 'subtitle'),
        text('summary', { column: 8, row: 2, width: 5, height: 1 }, 'caption'),
        { id: `${prefix}-plot`, type: 'chart', grid: { column: 1, row: 3, width: 12, height: factCount || media.length ? 4 : 6 }, chartType: 'line', showValues: true },
      );
      if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: 1, row: 7, width: media.length ? 4 : 12, height: 2 }, ordered: true });
      addHorizontalMedia(elements, prefix, media, 0, { column: factCount ? 5 : 1, row: 7, width: factCount ? 8 : 12, height: 2 });
    }
  } else if (family === 'media') {
    const media = presentation.media || [];
    if (compositionIndex === 0) {
      const mediaColumn = mirror ? 1 : 6;
      const textColumn = mirror ? 8 : 1;
      elements.push(
        text('kicker', { column: textColumn, row: 1, width: 5, height: 1 }, 'kicker'),
        text('title', { column: textColumn, row: 2, width: 5, height: 2 }, 'title'),
        text('core', { column: textColumn, row: 4, width: 5, height: 2 }, 'subtitle'),
        text('summary', { column: textColumn, row: 6, width: 5, height: 1 }, 'caption'),
      );
      if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: textColumn, row: 7, width: 5, height: 2 }, ordered: true });
      addVerticalMedia(elements, prefix, media, { column: mediaColumn, row: 1, width: 7, height: 8 });
    } else if (compositionIndex === 1) {
      elements.push(
        text('kicker', { column: 1, row: 1, width: 4, height: 1 }, 'kicker'),
        text('title', { column: 1, row: 2, width: 4, height: 2 }, 'title'),
        text('core', { column: 1, row: 4, width: 4, height: 2 }, 'subtitle'),
        text('summary', { column: 1, row: 6, width: 4, height: 1 }, 'caption'),
        { id: `${prefix}-media-1`, type: 'media', grid: { column: 5, row: 1, width: 8, height: media.length > 1 ? 6 : 8 }, fit: 'cover' },
      );
      if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: 1, row: 7, width: 4, height: 2 }, ordered: true });
      addHorizontalMedia(elements, prefix, media, 1, { column: 5, row: 7, width: 8, height: 2 });
    } else {
      elements.push(
        text('kicker', { column: 1, row: 1, width: 3, height: 1 }, 'kicker'),
        text('title', { column: 4, row: 1, width: 9, height: 1 }, 'title'),
        text('core', { column: 1, row: 2, width: 7, height: 1 }, 'subtitle'),
        text('summary', { column: 8, row: 2, width: 5, height: 1 }, 'caption'),
      );
      if (factCount) elements.push({ id: `${prefix}-facts`, type: 'list', grid: { column: 1, row: 3, width: 3, height: 6 }, ordered: true });
      addMediaGrid(elements, prefix, media, { column: factCount ? 4 : 1, row: 3, width: factCount ? 9 : 12, height: 6 });
    }
  } else {
    const coreColumn = mirror ? 6 : 1;
    const summaryColumn = mirror ? 1 : 8;
    elements.push(
      text('kicker', { column: mirror ? 10 : 1, row: 1, width: 3, height: 1 }, 'kicker'),
      text('title', { column: mirror ? 1 : 4, row: 1, width: 9, height: 1 }, 'title'),
      text('core', { column: coreColumn, row: 2, width: 7, height: 1 }, 'subtitle'),
      text('summary', { column: summaryColumn, row: 2, width: 5, height: 1 }, 'caption'),
      { id: `${prefix}-facts`, type: 'list', grid: { column: 1, row: 3, width: 12, height: 6 }, ordered: true },
    );
  }

  const contentMap = {};
  elements.forEach((element, index) => {
    if (element.id === `${prefix}-kicker`) contentMap[`elements[${index}].text`] = 'presentation.pageIntent';
    if (element.id === `${prefix}-title`) contentMap[`elements[${index}].text`] = 'presentation.title.short';
    if (element.id === `${prefix}-core`) contentMap[`elements[${index}].${element.type === 'quote' ? 'quote' : 'text'}`] = 'presentation.coreMessage';
    if (element.id === `${prefix}-summary`) contentMap[`elements[${index}].text`] = 'presentation.summary.short';
    if (element.type === 'quote' && element.id === `${prefix}-core`) contentMap[`elements[${index}].attribution`] = 'presentation.summary.short';
  });
  const itemBindings = [];
  metricItems.forEach((item, index) => {
    const elementIndex = elements.findIndex(element => element.id === `${prefix}-value-${index + 1}`);
    if (elementIndex >= 0) itemBindings.push({ id: item.id, target: `elements[${elementIndex}]` });
  });
  const factsIndex = elements.findIndex(element => element.id === `${prefix}-facts`);
  if (factsIndex >= 0) factSourceItems.forEach((item, index) => itemBindings.push({ id: item.id, target: `elements[${factsIndex}].items[${index}]` }));
  const chartBindings = factsIndex < 0 ? [] : chartFactItems.map((item, index) => ({
    mode: 'summary',
    sourceIds: [item.id],
    target: `elements[${factsIndex}].items[${factSourceItems.length + index}]`,
  }));
  const chartIndex = elements.findIndex(element => element.id === `${prefix}-plot`);
  if (chartIndex >= 0) (presentation.chartData || []).forEach((item, index) => chartBindings.push({
    mode: 'point',
    sourceIds: [item.id],
    target: `elements[${chartIndex}].data[${index}]`,
  }));
  const mediaBindings = [];
  elements.forEach((element, index) => {
    if (element.type === 'media') mediaBindings.push({ sourceIndex: mediaBindings.length, target: `elements[${index}]` });
  });
  if (mediaBindings.length !== (presentation.media?.length || 0)) {
    throw new Error(`Bespoke slide ${logicalId || 'unknown'} family ${family} did not define every media binding`);
  }
  return {
    id: BESPOKE_VARIANT_ID,
    kind: 'bespoke',
    adjustable: false,
    composition: {
      designIntent: {
        objective: '呈现单页核心信息',
        audience: '当前演示文稿受众',
        narrativeRole: '推进单页叙事',
        emphasis: '突出内容层级与证据关系',
        rationale: `${family}-${compositionIndex + 1} 结构投影`,
      },
      background: 'default',
      elements,
    },
    projection: { itemBindings, chartBindings, mediaBindings },
    contentMap,
  };
}

function addHorizontalMedia(elements, prefix, media, startIndex, area) {
  const count = Math.max(0, media.length - startIndex);
  if (!count) return;
  const width = Math.max(1, Math.floor(area.width / count));
  media.slice(startIndex).forEach((_, offset) => elements.push({
    id: `${prefix}-media-${startIndex + offset + 1}`,
    type: 'media',
    grid: { column: area.column + offset * width, row: area.row, width: offset === count - 1 ? area.width - offset * width : width, height: area.height },
    fit: 'cover',
  }));
}

function addVerticalMedia(elements, prefix, media, area) {
  const height = Math.max(1, Math.floor(area.height / Math.max(1, media.length)));
  media.forEach((_, index) => elements.push({
    id: `${prefix}-media-${index + 1}`,
    type: 'media',
    grid: { column: area.column, row: area.row + index * height, width: area.width, height: index === media.length - 1 ? area.height - index * height : height },
    fit: 'cover',
  }));
}

function addMediaGrid(elements, prefix, media, area) {
  const columns = media.length <= 2 ? Math.max(1, media.length) : media.length <= 4 ? 2 : 4;
  const rows = Math.max(1, Math.ceil(media.length / columns));
  const width = Math.max(1, Math.floor(area.width / columns));
  const height = Math.max(1, Math.floor(area.height / rows));
  media.forEach((_, index) => {
    const columnIndex = index % columns;
    const rowIndex = Math.floor(index / columns);
    elements.push({
      id: `${prefix}-media-${index + 1}`,
      type: 'media',
      grid: {
        column: area.column + columnIndex * width,
        row: area.row + rowIndex * height,
        width: columnIndex === columns - 1 ? area.width - columnIndex * width : width,
        height: rowIndex === rows - 1 ? area.height - rowIndex * height : height,
      },
      fit: 'cover',
    });
  });
}

function selectBespokeListItems(items, logicalId) {
  const pinnedCount = items.filter(item => item.pinned).length;
  if (pinnedCount > BESPOKE_LIST_ITEM_LIMIT) {
    throw new Error(`Bespoke slide ${logicalId || 'unknown'} has ${pinnedCount} list-bound pinned facts; limit=${BESPOKE_LIST_ITEM_LIMIT}`);
  }
  let optionalSlots = BESPOKE_LIST_ITEM_LIMIT - pinnedCount;
  return items.filter(item => item.pinned || optionalSlots-- > 0);
}

function readContentPlan(file, expectedCount) {
  if (file === true) throw new Error('--content-plan requires a JSON file');
  const resolved = path.resolve(CALLER_CWD, String(file));
  const parsed = JSON.parse(readFileSync(resolved, 'utf8'));
  const pages = Array.isArray(parsed) ? parsed : parsed?.pages;
  if (!Array.isArray(pages)) throw new Error('--content-plan must contain an array or {pages:[...]}');
  if (pages.length !== expectedCount) {
    throw new Error(`--content-plan must contain exactly ${expectedCount} pages, found ${pages.length}`);
  }
  const ids = new Set();
  return pages.map((entry, index) => {
    const source = entry?.presentation || entry;
    let presentation;
    try {
      presentation = normalizePageContentPack(source);
    } catch (error) {
      throw new Error(`content plan page ${index + 1}: ${error.message}`);
    }
    const id = String(entry?.id || '').trim();
    if (!id) throw new Error(`content plan page ${index + 1}: stable id is required`);
    if (ids.has(id)) throw new Error(`content plan contains duplicate logical page id "${id}"`);
    ids.add(id);
    return { id, presentation };
  });
}

function pickLayout({ themePack, role, used, body, mediaIntent = null, seed = null }) {
  const mediaQuery = mediaIntent ? mediaIntentQuery(mediaIntent) : {};
  const roleCandidates = listLayouts({ theme: themePack, role, ...mediaQuery, limit: 80, seed });
  const fallbackCandidates = listLayouts({ theme: themePack, ...mediaQuery, limit: 200, seed });
  const seen = new Set();
  const candidates = [...roleCandidates, ...fallbackCandidates]
    .map(item => item.layout)
    .filter(Boolean)
    .filter(layout => {
      if (seen.has(layout)) return false;
      seen.add(layout);
      return true;
    })
    .filter(layout => !used.has(layout))
    .filter(layout => (
      body
        ? !isCoverCandidate(layout) && !isCoverLikeLayout(layout)
        : isCoverCandidate(layout)
    ));
  if (!candidates.length) throw new Error(`No unused ${body ? 'body' : 'cover'} layout available for role "${role}" in ${themePack}`);
  // 从前 5 名合格候选里 seeded 随机挑:打分只有一两个精确命中时,永远取第一会让
  // 不同用户的骨架在这些 role 上完全一致;候选都已通过过滤(均"符合"),前几名之间
  // 的分差只是相关性排序,随机采样是多样性与相关性的折衷。
  const pool = candidates.slice(0, 5);
  const layout = pool[hashSeed(`${seed}:${role}:${used.size}`) % pool.length];
  return layout;
}

function parseMediaIntent(args) {
  const plannedImages = mediaIntentCount(args['planned-images'] ?? args.plannedImages);
  if (plannedImages) return { field: 'plannedImages', value: plannedImages, count: plannedImages };
  if (args['image-gen'] === true || args.imageGen === true) return { field: 'imageGen', value: true, count: 1 };
  if (args['needs-visual'] === true || args.needsVisual === true) return { field: 'needsVisual', value: true, count: 1 };
  return null;
}

function mediaIntentQuery(intent) {
  if (!intent) return {};
  if (intent.field === 'plannedImages') return { plannedImages: intent.count, mediaCount: intent.count };
  if (intent.field === 'imageGen') return { imageGen: true, mediaCount: intent.count };
  if (intent.field === 'needsVisual') return { needsVisual: true, mediaCount: intent.count };
  return {};
}

function mediaIntentCount(value) {
  if (value === true) return 1;
  const count = Number(value);
  if (Number.isFinite(count) && count > 0) return Math.round(count);
  return 0;
}

function parseRoles(value, expectedCount) {
  if (value === undefined) {
    return { roles: DEFAULT_BODY_ROLES, explicit: false };
  }
  if (value === true) throw new Error('Missing value for --roles');
  const roles = String(value)
    .split(',')
    .map(item => item.trim());
  if (roles.some(role => !role)) {
    throw new Error('--roles must be a comma-separated sequence without empty entries');
  }
  const structural = roles.filter(role => role === 'cover' || role === 'closing');
  if (structural.length) {
    throw new Error(`--roles only accepts body roles; cover and closing are automatic (received ${structural.join(', ')})`);
  }
  const unknown = [...new Set(roles.filter(role => !BODY_ROLES.has(role)))];
  if (unknown.length) {
    throw new Error(`Unknown --roles value(s): ${unknown.join(', ')}. Allowed body roles: ${[...BODY_ROLES].join(', ')}`);
  }
  if (roles.length !== expectedCount) {
    throw new Error(
      `--roles must provide exactly ${expectedCount} body roles for the requested page count; `
      + `cover and closing are automatic (received ${roles.length})`,
    );
  }
  return { roles, explicit: true };
}

function writeChunks(out, spec, chunkSize) {
  if (!Number.isFinite(chunkSize) || chunkSize <= 0) return;
  const size = Math.max(1, Math.round(chunkSize));
  const total = Math.ceil(spec.slides.length / size);
  const parsed = path.parse(out);
  for (let index = 0; index < total; index += 1) {
    const start = index * size;
    const end = Math.min(spec.slides.length, start + size);
    const chunkPath = path.join(parsed.dir, `${parsed.name}.part-${String(index + 1).padStart(2, '0')}.json`);
    const chunkSpec = {
      ...(spec.schemaVersion != null ? { schemaVersion: spec.schemaVersion } : {}),
      ...(spec.variantOutputMode ? { variantOutputMode: spec.variantOutputMode } : {}),
      title: spec.title,
      goal: spec.goal,
      themePack: spec.themePack,
      pageCount: spec.pageCount,
      ...(spec.randomSeed != null ? { randomSeed: spec.randomSeed } : {}),
      part: {
        index: index + 1,
        total,
        startSlide: start + 1,
        endSlide: end,
      },
      slides: spec.slides.slice(start, end),
    };
    writeJson(chunkPath, chunkSpec);
    writeFillPlan(chunkPath, chunkSpec);
  }
}

function writeJson(file, value) {
  const target = path.resolve(CALLER_CWD, file);
  mkdirSync(path.dirname(target), { recursive: true });
  writeFileSync(target, compactJson(value));
}

function writeFillPlan(goalPath, spec) {
  const out = fillPlanPath(goalPath);
  writeJson(out, {
    goal: path.resolve(CALLER_CWD, goalPath),
    themePack: spec.themePack,
    slideCount: spec.slides.length,
    ...(spec.part ? { part: spec.part } : {}),
    slides: spec.slides.map((slide, index) => ({
      slide: (spec.part?.startSlide || 1) + index,
      ...(Array.isArray(slide.variants)
        ? {
            selectedVariant: slide.selectedVariant,
            variants: slide.variants.map(item => inspectFillPlan(item)),
          }
        : inspectFillPlan(slide)),
    })),
  });
  return path.resolve(CALLER_CWD, out);
}

function fillPlanPath(goalPath) {
  const parsed = path.parse(goalPath);
  return path.join(parsed.dir, `${parsed.name}.fill-plan.json`);
}

function inspectFillPlan(slide) {
  if (slide?.kind === 'bespoke') {
    return {
      id: slide.id || BESPOKE_VARIANT_ID,
      kind: 'bespoke',
      adjustable: false,
      designTask: {
        status: 'generated',
        instruction: '保留 scaffold 生成的 composition 结构与 projection bindings；业务值只修改 slide.content.presentation，不写回 composition。',
      },
    };
  }
  const inspected = inspectLayout(slide.layout, { compact: true });
  return {
    ...(slide.id ? { id: slide.id } : {}),
    ...(slide.kind ? { kind: slide.kind } : {}),
    layout: slide.layout,
    label: inspected?.label || null,
    roles: inspected?.roles || [],
    fillPlan: inspected?.fillPlan || null,
  };
}

function printUsage() {
  console.error('Usage: node scripts/goal-scaffold.mjs --title <title> --goal <goal> --theme <themeXX> --pages <n> --out output/<deck>/goal.json [--layout-variants 1|3] [--roles <one-body-role-per-page>] [--content-plan <pages.json>] [--chunk-size 5]');
}
