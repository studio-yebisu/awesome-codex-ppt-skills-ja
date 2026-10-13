// @ts-check
// layout-query 域:按 role/关键词/媒体需求筛选并打分候选版式(listLayouts 的实现)。
import {
  THEME_PAGES,
  getLayoutRecord,
  isBodyContentCandidate,
  isCoverCandidate,
  valueAtPath,
} from './theme-registry.mjs';
import {
  getMediaSlotsForLayout,
  isWritableMediaSlot,
  mediaSlotsCanFit,
  normalizeMediaKind,
  slotAcceptsKind,
} from './media-slots.mjs';
import {
  ROLE_KEYWORDS,
  hasAmbientBackground,
  inspectLayout,
  normalizeProps,
  pageMatches,
  pageSearchText,
} from './inspect-fillplan.mjs';
import { charLength } from './copy-contract.mjs';
import {
  classifyPageIntent,
  formatPageContentValue,
  normalizePageContentPack,
  pageContentProjectionItems,
  requiredPageContentFacts,
  resolveContentMap,
  summarizePageChartData,
} from '../../src/variant-contract.mjs';

const ROLE_ALIASES = {
  agenda: 'breakdown',
  summary: 'statement',
  insight: 'observation',
  quote: 'observation',
  // 批测实证的直觉词(codex 多轮使用未命中):映射到最接近的既有 role。
  numbers: 'metrics',
  section: 'transition',
  chapter: 'transition',
  list: 'breakdown',
  product: 'case',
  feature: 'case',
  faq: 'risks',
  content: 'content',
  body: 'content',
  main: 'content',
  inner: 'content',
  interior: 'content',
  '正文': 'content',
  '内容': 'content',
  '主体': 'content',
  '内页': 'content',
  chart: 'metrics',
  timeline: 'trend',
  compare: 'comparison',
  flow: 'process',
  roadmap: 'actions',
  visual: 'image',
  gallery: 'image',
  media: 'image',
  picture: 'image',
  photo: 'image',
  atmosphere: 'ambient',
  background: 'ambient',
  dynamic: 'ambient',
};

/** @typedef {import('../../src/types').ListLayoutsOptions & {contentPack?: unknown}} ContentAwareListLayoutsOptions */
/** @param {ContentAwareListLayoutsOptions} [options] */
export function listLayouts({
  theme,
  role,
  keyword,
  contentPack = null,
  needsMedia = false,
  plannedImages = false,
  providedImages = false,
  providedMedia = false,
  imageGen = false,
  needsVisual = false,
  mediaCount = null,
  mediaKind = null,
  requireInitialMedia = false,
  limit = 12,
  seed = null,
} = {}) {
  const requestedRole = role ? String(role).trim().toLowerCase() : '';
  const normalizedRole = requestedRole ? ROLE_ALIASES[requestedRole] || requestedRole : '';
  const keywords = normalizedRole ? ROLE_KEYWORDS[normalizedRole] || [normalizedRole] : [];
  const keywordText = String(keyword || '').trim().toLowerCase();
  const requestedMediaCount = getRequestedMediaCount({ plannedImages, providedImages, providedMedia, imageGen, needsVisual, mediaCount });
  const normalizedMediaKind = normalizeMediaKind(mediaKind);
  const needsInitialMedia = Boolean(requireInitialMedia || providedImages || providedMedia);
  const normalizedContentPack = contentPack ? normalizePageContentPack(contentPack) : null;
  const requiresMedia = needsMedia || requestedMediaCount > 0 || (!normalizedContentPack && normalizedRole === 'image') || needsInitialMedia || Boolean(normalizedMediaKind);

  const rows = listLayoutsForMediaCount({ theme, normalizedRole, keywords, keywordText, contentPack: normalizedContentPack, requiresMedia, requestedMediaCount, normalizedMediaKind, needsInitialMedia, seed });
  return rows.slice(0, Math.max(1, Math.min(50, Number(limit) || 12)));
}

/** @param {{theme?: string, pages?: any[], limit?: number, seed?: string}} [options] */
export function listLayoutsForContentPacks({ theme, pages, limit = 50, seed = 'deck-content' } = {}) {
  if (!Array.isArray(pages)) throw new Error('pages must be an array of PageContentPack entries');
  const themePages = THEME_PAGES.filter(page => !theme || page.themeKey === theme);
  const bodyLayouts = new Set(themePages.filter(isBodyContentCandidate).map(page => page.key));
  const inspected = themePages.map(page => inspectLayout(page.key)).filter(Boolean);
  return pages.map((entry, pageIndex) => {
    const contentPack = normalizePageContentPack(entry?.presentation || entry);
    const normalizedIntent = classifyPageIntent(contentPack.pageIntent);
    const normalizedRole = ROLE_ALIASES[normalizedIntent] || normalizedIntent;
    const requestedMediaCount = contentPack.media?.length || 0;
    const needsInitialMedia = requestedMediaCount > 0;
    const rows = inspected
      .filter(row => !requestedMediaCount || mediaSlotsCanFit(
        getMediaSlotsForLayout(row.layout),
        requestedMediaCount,
        { requireInitialMedia: true, exactCount: true },
      ))
      .map(row => {
        const projectionPlan = buildTemplateProjectionPlan(row, contentPack);
        return { ...row, projectionPlan, structureFingerprint: projectionPlan.structureFingerprint };
      })
      .filter(row => row.projectionPlan.requiredFits)
      .map(compactLayoutCandidate)
      .map(row => ({
        ...row,
        queryScore: scoreLayout(row, {
          normalizedRole,
          keywordText: '',
          contentPack,
          requiresMedia: requestedMediaCount > 0,
          requestedMediaCount,
          normalizedMediaKind: '',
          needsInitialMedia,
        }),
      }))
      .sort((left, right) => (
        right.queryScore - left.queryScore
        || hashSeed(`${seed}:page-${pageIndex + 1}:${right.layout}`) - hashSeed(`${seed}:page-${pageIndex + 1}:${left.layout}`)
      ));
    const boundedLimit = Math.max(1, Math.min(50, Number(limit) || 50));
    if (normalizedIntent !== 'cover') return rows.slice(0, boundedLimit);
    const coverRows = rows.filter(row => isCoverCandidate(row.layout)).slice(0, boundedLimit);
    const bodyRows = rows.filter(row => bodyLayouts.has(row.layout)).slice(0, boundedLimit);
    return [...coverRows, ...bodyRows];
  });
}

function listLayoutsForMediaCount({ theme, normalizedRole, keywords, keywordText, contentPack, requiresMedia, requestedMediaCount, normalizedMediaKind, needsInitialMedia, seed }) {
  const rows = THEME_PAGES
    .filter(page => !theme || page.themeKey === theme)
    .filter(page => {
      if (contentPack || !normalizedRole) return true;
      if (normalizedRole === 'cover') return isCoverCandidate(page.key);
      if (normalizedRole === 'content') return isBodyContentCandidate(page);
      if (normalizedRole === 'image') return inspectLayout(page.key, { compact: true })?.mediaSlots.some(slot => slot.canPresetMedia);
      if (normalizedRole === 'ambient') return hasAmbientBackground(page);
      return pageMatches(page, keywords);
    })
    .filter(page => !keywordText || pageSearchText(page).includes(keywordText))
    .map(page => inspectLayout(page.key))
    .filter(Boolean)
    .filter(row => !requiresMedia || mediaSlotsCanFit(
      getMediaSlotsForLayout(row.layout),
      requestedMediaCount || contentPack?.media?.length || 1,
      {
        requireInitialMedia: needsInitialMedia || Boolean(contentPack?.media?.length),
        mediaKind: normalizedMediaKind,
        exactCount: requestedMediaCount > 0 || Boolean(contentPack?.media?.length),
      },
    ))
    .map(row => {
      if (!contentPack) return row;
      const projectionPlan = buildTemplateProjectionPlan(row, contentPack);
      return {
        ...row,
        projectionPlan,
        structureFingerprint: projectionPlan.structureFingerprint,
      };
    })
    .filter(row => !contentPack || /** @type {any} */ (row).projectionPlan.requiredFits)
    .map(compactLayoutCandidate);

  // 同分候选用 seed 随机打散:打分只表达"是否更匹配",同等匹配的页面之间没有天然
  // 优先级。历史上并列项按页码稳定排序,所有调用方(Agent 与 goal:scaffold)都贪婪
  // 取列表最前,导致不同用户生成的 deck 大量选中同一批"前面的页",成片雷同。
  const tieBreakSeed = seed === null || seed === undefined || seed === '' ? String(Math.floor(Math.random() * 0xffffffff)) : String(seed);
  const scored = rows.map(row => ({
    ...row,
    queryScore: scoreLayout(row, { normalizedRole, keywordText, contentPack, requiresMedia, requestedMediaCount, normalizedMediaKind, needsInitialMedia }),
  }));
  return scored.sort((a, b) => {
    const diff = b.queryScore - a.queryScore;
    if (diff !== 0) return diff;
    return hashSeed(`${tieBreakSeed}:${b.layout}`) - hashSeed(`${tieBreakSeed}:${a.layout}`);
  });
}

function compactLayoutCandidate(row) {
  if (!row) return row;
  const {
    copyBudgets,
    propShapes,
    fieldContracts,
    copyRoles,
    countBindings,
    defaultVisibleCounts,
    fillPlan,
    lengthBindings,
    themeDisplayName,
    themeScenario,
    themeAudience,
    ...candidate
  } = row;
  const copyKeys = (row.copyKeys || []).slice(0, 6);
  return {
    ...candidate,
    themeDisplayName,
    copyKeys,
    copyBudgets: compactCopyBudgets(row.copyBudgets, copyKeys),
    arrayMeta: (row.arrayMeta || []).map(compactCandidateArrayMeta),
    mediaSlots: (row.mediaSlots || []).map(compactQueryMediaSlot),
  };
}

function compactCopyBudgets(copyBudgets = {}, copyKeys = []) {
  return Object.fromEntries((copyKeys || [])
    .map(key => [key, copyBudgets?.[key]])
    .filter(([, budget]) => budget?.maxChars)
    .map(([key, budget]) => [key, { maxChars: budget.maxChars }]));
}

function compactCandidateArrayMeta(meta) {
  return {
    key: meta.key,
    role: meta.role,
    defaultVisibleCount: meta.defaultVisibleCount,
    maxCount: meta.maxCount,
    countKey: meta.countKey,
    maxFromKey: meta.maxFromKey,
    maxFromKeyOffset: meta.maxFromKeyOffset,
    maxByKey: meta.maxByKey,
    maxByValue: meta.maxByValue,
  };
}

function compactQueryMediaSlot(slot) {
  return {
    role: slot.role,
    field: slot.field,
    fieldPath: slot.fieldPath,
    writableProp: slot.writableProp,
    countKey: slot.countKey,
    publicCountKey: slot.publicCountKey || slot.countKey,
    defaultVisibleCount: slot.defaultVisibleCount,
    max: slot.max,
    maxFromKey: slot.maxFromKey,
    maxFromKeyOffset: slot.maxFromKeyOffset,
    maxByKey: slot.maxByKey,
    maxByValue: slot.maxByValue,
    maxCount: slot.maxCount,
    acceptedKinds: slot.acceptedKinds,
    acceptedKindsSource: slot.acceptedKindsSource,
    initialSrcSupported: slot.initialSrcSupported,
    canPresetMedia: slot.canPresetMedia,
    presetProp: slot.presetProp,
    emptySlotBehavior: slot.emptySlotBehavior,
  };
}

function compactCandidateFillPlan(plan) {
  return {
    arrays: (plan.arrays || []).slice(0, 4).map(item => ({
      key: item.key,
      role: item.role,
      visibleCount: item.visibleCount,
      maxCount: item.maxCount,
      countKey: item.countKey,
      ...(item.itemShape === 'string' ? { itemShape: item.itemShape } : {}),
      ...(item.item?.maxChars ? { item: item.item } : {}),
      ...(item.nestedArrays && Object.keys(item.nestedArrays).length ? { nestedArrays: item.nestedArrays } : {}),
    })),
    media: (plan.media || []).slice(0, 2),
  };
}

export function hashSeed(value) {
  let hash = 2166136261;
  for (let i = 0; i < value.length; i += 1) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  // FNV-1a 对仅末字符不同的 key(themeNN_page010/011…)雪崩不足,直接用会让"随机"
  // 顺序呈现大片连续页码;补一轮 murmur3 终混(fmix32)打散。
  hash ^= hash >>> 16;
  hash = Math.imul(hash, 0x85ebca6b);
  hash ^= hash >>> 13;
  hash = Math.imul(hash, 0xc2b2ae35);
  hash ^= hash >>> 16;
  return hash >>> 0;
}

/** @param {import('../../src/types').CompactLayoutCandidate} layout */
export function scoreLayout(layout, { normalizedRole, keywordText, contentPack = null, requiresMedia, requestedMediaCount, normalizedMediaKind, needsInitialMedia }) {
  let score = 0;
  if (normalizedRole && (
    layout.roles.includes(normalizedRole)
    || (normalizedRole === 'cover' && isCoverCandidate(layout.layout))
  )) score += 20;
  if (keywordText && `${layout.label} ${layout.slot}`.toLowerCase().includes(keywordText)) score += 10;
  if (requiresMedia && layout.mediaSlots.some(isWritableMediaSlot)) score += 8;
  if (needsInitialMedia && layout.mediaSlots.some(slot => isWritableMediaSlot(slot) && slot.initialSrcSupported)) score += 6;
  if (normalizedMediaKind && layout.mediaSlots.some(slot => isWritableMediaSlot(slot) && slotAcceptsKind(slot, normalizedMediaKind))) score += 4;
  if (requestedMediaCount && layout.mediaSlots.some(slot => isWritableMediaSlot(slot) && Number(slot.defaultCount) === requestedMediaCount)) score += 3;
  if (contentPack) {
    const candidate = /** @type {any} */ (layout);
    const plan = candidate.projectionPlan || buildTemplateProjectionPlan(inspectLayout(layout.layout), contentPack);
    score += plan.requiredFits ? 40 : -200;
    score += Math.max(0, 12 - Number(plan.primaryContentContainer?.slack || 0));
    if (plan.primaryContentContainer?.supportsDetail) score += 5;
    if (contentPack.chartData?.length && plan.primaryContentContainer?.supportsValue) score += 10;
  }
  return score;
}


export function contentShapeFromPageContentPack(value) {
  const pack = normalizePageContentPack(value);
  const items = pageContentProjectionItems(pack);
  const authoredRequired = items.filter(item => item.authoredRequired);
  const pinned = items.filter(item => item.pinned);
  return {
    titleChars: charLength(pack.title.short),
    coreMessageChars: charLength(pack.coreMessage),
    itemCount: items.length,
    requiredItemCount: authoredRequired.length,
    pinnedItemCount: pinned.length,
    valueItemCount: items.filter(item => item.hasValue).length,
    unitItemCount: items.filter(item => item.unit).length,
    chartPointCount: pack.chartData?.length || 0,
    mediaCount: pack.media?.length || 0,
  };
}

export function buildTemplateProjectionPlan(layoutInput, value) {
  const layout = layoutInput?.fillPlan ? layoutInput : inspectLayout(layoutInput?.layout || layoutInput);
  const pack = normalizePageContentPack(value);
  const shape = contentShapeFromPageContentPack(pack);
  const canonicalItems = pageContentProjectionItems(pack);
  const arrayFields = primaryArrayFields(layout);
  const chartTarget = (pack.chartData?.length
    ? arrayFields.map(field => chartArrayContainer(layout, field, pack.chartData)).filter(Boolean)
    : [])
    .sort((left, right) => right.score - left.score || left.key.localeCompare(right.key))[0] || null;
  const chartMode = pack.chartData?.length ? (chartTarget ? 'full' : 'summary') : 'none';
  const emptyItemsBodyProjection = !pack.items.length && !pack.chartData?.length && !isCoverCandidate(layout.layout)
    && isBodyContentCandidate(getLayoutRecord(layout.layout).page);
  const items = projectionItemsForPlan(pack, chartMode, emptyItemsBodyProjection);
  const pinnedItems = items.filter(item => item.pinned);
  const arrays = arrayFields
    .filter(field => arrayRegionKey(field.key) !== arrayRegionKey(chartTarget?.key))
    .map(field => arrayContainer(layout, field, pinnedItems, items));
  const scalarItems = emptyItemsBodyProjection ? items : canonicalItems;
  const scalarGroup = chartMode === 'summary'
    ? null
    : scalarGroupContainer(layout, scalarItems.filter(item => item.pinned), scalarItems);
  const candidates = [...arrays, scalarGroup]
    .filter(Boolean)
    .sort((left, right) => right.score - left.score || left.key.localeCompare(right.key));
  const arrayRegions = businessArrayRegions(layout);
  const chartRegion = arrayRegionKey(chartTarget?.key);
  const needsPrimaryContent = pack.items.length > 0 || pinnedItems.length > 0;
  const primaryContentContainer = needsPrimaryContent
    ? candidates.find(item => item.requiredFits && arrayRegions.every(region => (
      region.key === arrayRegionKey(item.kind === 'array' ? item.key : '')
      || region.key === chartRegion
      || region.visibleCount <= 0
      || Boolean(disabledArrayProp(layout, region.field) && arrayFieldAcceptsEmptyValue(layout, region.field))
    ))) || null
    : null;
  const reserved = new Set(primaryContentContainer?.targetPaths || []);
  const textFields = (layout?.fillPlan?.text || []).filter(field => !field.type || field.type === 'string');
  const titleTarget = textFields
    .filter(field => !reserved.has(field.key))
    .filter(field => projectionSemantic(field.key, field.type, field.role) === 'label')
    .filter(field => Number(field.maxChars || 0) >= shape.titleChars)
    .sort((left, right) => titleFieldScore(right) - titleFieldScore(left))[0] || null;
  if (titleTarget) reserved.add(titleTarget.key);
  const summaryTarget = textFields
    .filter(field => !reserved.has(field.key))
    .filter(field => ['label', 'detail'].includes(projectionSemantic(field.key, field.type, field.role)))
    .filter(field => Number(field.maxChars || 0) >= shape.coreMessageChars)
    .sort((left, right) => (
      Number(isBodyTextField(right)) - Number(isBodyTextField(left))
      || Number(right.maxChars || 0) - Number(left.maxChars || 0)
    ))[0] || null;
  if (summaryTarget) reserved.add(summaryTarget.key);

  const supportingTargets = [];
  const usedValues = new Set([pack.title.short, pack.coreMessage]);
  const disabledProps = [];
  for (const field of textFields.filter(item => !reserved.has(item.key))) {
    const semantic = projectionSemantic(field.key, field.type, field.role);
    const source = ['value', 'displayValue', 'unit'].includes(semantic)
      ? null
      : supportingTextSource(field, pack, items, usedValues);
    if (source) {
      supportingTargets.push({ target: field.key, ...source });
      usedValues.add(String(source.value));
    } else {
      // Explicitly blank an unused authored string slot so component defaults never leak.
      supportingTargets.push({ target: field.key, value: '' });
    }
  }

  let auxiliaryFits = true;
  const primaryRegion = arrayRegionKey(primaryContentContainer?.kind === 'array' ? primaryContentContainer.key : '');
  for (const region of arrayRegions) {
    if (region.key === primaryRegion || region.key === chartRegion || region.visibleCount <= 0) continue;
    const disabled = disabledArrayProp(layout, region.field);
    if (!disabled || !arrayFieldAcceptsEmptyValue(layout, region.field)) {
      auxiliaryFits = false;
      break;
    }
    disabledProps.push(
      { prop: region.field.key, value: [] },
      disabled,
    );
  }

  const scalarFits = (layout?.fillPlan?.text || [])
    .filter(field => field.type && field.type !== 'string')
    .every(field => ['ordinal', 'decorative'].includes(projectionSemantic(field.key, field.type, field.role)) || reserved.has(field.key));
  const contentCountKeys = new Set([
    primaryContentContainer?.countKey,
    chartTarget?.countKey,
  ].filter(Boolean));
  const mediaPlan = buildMediaProjectionPlan(layout, pack, contentCountKeys);
  const requiredFits = Boolean(titleTarget && summaryTarget)
    && (!needsPrimaryContent || Boolean(primaryContentContainer?.requiredFits))
    && auxiliaryFits
    && scalarFits
    && mediaPlan.requiredFits;
  const plan = {
    requiredFits,
    contentShape: shape,
    titleTarget: titleTarget?.key || null,
    summaryTarget: summaryTarget?.key || null,
    primaryContentContainer,
    chartTarget,
    chartMode,
    emptyItemsBodyProjection,
    chartSummary: chartMode === 'summary' ? summarizePageChartData(pack) : '',
    supportingTargets,
    disabledProps: [...disabledProps, ...mediaPlan.disabledProps],
    mediaTarget: mediaPlan.mediaTarget,
  };
  plan.structureFingerprint = structureFingerprint(layout, plan);
  if (plan.requiredFits && !projectionPlanFitsPropContract(layout, pack, plan)) plan.requiredFits = false;
  return plan;
}

export function materializeTemplateProjection(layoutInput, value, variantIndex = 0) {
  const layout = layoutInput?.fillPlan ? layoutInput : inspectLayout(layoutInput?.layout || layoutInput);
  const pack = normalizePageContentPack(value);
  const plan = layoutInput?.projectionPlan?.requiredFits
    ? layoutInput.projectionPlan
    : buildTemplateProjectionPlan(layout, pack);
  if (!plan.requiredFits) throw new Error(`Layout ${layout?.layout || layoutInput} cannot project the PageContentPack`);
  return materializeProjectionWithPlan(layout, pack, variantIndex, plan);
}

function materializeProjectionWithPlan(layout, pack, variantIndex, plan) {
  const props = {};
  const contentMap = {
    [plan.titleTarget]: 'presentation.title.short',
    [plan.summaryTarget]: 'presentation.coreMessage',
  };
  const contentPaths = [];
  const projectedItemIds = [];
  const chartBindings = [];
  const structureArrays = [];
  const structureValues = [];
  const canonicalItemIds = new Set(pack.items.map(item => item.id));
  let ordered = orderProjectionItems(projectionItemsForPlan(pack, plan.chartMode, plan.emptyItemsBodyProjection), variantIndex);
  const primary = plan.primaryContentContainer;
  if (primary) {
    const accepted = new Set(primary.acceptedItemIds || []);
    if (accepted.size) ordered = ordered.filter(item => accepted.has(item.id));
    const optionalCount = variantIndex === 1 ? 1 : variantIndex === 2 ? 2 : 0;
    const count = primary.kind === 'scalar-group'
      ? primary.capacity
      : Math.min(
        primary.capacity,
        Math.max(
          primary.minimumCapacity || 0,
          ordered.filter(item => item.pinned).length + optionalCount,
          (pack.items.length || plan.emptyItemsBodyProjection) ? 1 : 0,
        ),
      );
    const selected = takeProjectionItems(ordered, count);
    projectedItemIds.push(...selected.map(item => item.id).filter(id => canonicalItemIds.has(id)));
    if (primary.kind === 'scalar-group') {
      selected.forEach((item, index) => {
        const slot = primary.slots[index];
        slot.fields.forEach(field => {
          structureValues.push({ path: field.key, sourceId: item.id, semantic: field.semantic });
          setObjectPath(props, field.key, projectionFieldValue(item, field.semantic, slot.fields, true));
          contentPaths.push(field.key);
        });
        if (item.chartSourceIds?.length) {
          const target = slot.fields.find(field => field.semantic === 'label')?.key || slot.fields[0].key;
          chartBindings.push({ mode: 'summary', sourceIds: item.chartSourceIds, target });
        }
      });
    } else {
      selected.forEach((item, index) => {
        if (!item.chartSourceIds?.length) return;
        chartBindings.push({ mode: 'summary', sourceIds: item.chartSourceIds, target: `${primary.key}[${index}]` });
      });
      structureArrays.push(structuralArrayProjection(primary, selected));
      setObjectPath(props, primary.key, selected.map((item, index) => materializeArrayItem(primary, item, index)));
      contentPaths.push(primary.key);
      if (primary.countKey) {
        props[primary.countKey] = selected.length;
        contentPaths.push(primary.countKey);
      }
    }
  }
  if (plan.chartTarget) {
    const chartItems = chartProjectionItems(pack);
    chartItems.forEach((item, index) => {
      chartBindings.push({ mode: 'point', sourceIds: [pack.chartData[index].id], target: `${plan.chartTarget.key}[${index}]` });
    });
    structureArrays.push(structuralArrayProjection(plan.chartTarget, chartItems));
    setObjectPath(props, plan.chartTarget.key, chartItems.map((item, index) => materializeArrayItem(plan.chartTarget, item, index)));
    contentPaths.push(plan.chartTarget.key);
    if (plan.chartTarget.countKey) {
      props[plan.chartTarget.countKey] = chartItems.length;
      contentPaths.push(plan.chartTarget.countKey);
    }
  }
  for (const target of plan.supportingTargets) {
    if (target.source) contentMap[target.target] = target.source;
    else {
      structureValues.push(target.sourceId
        ? { path: target.target, sourceId: target.sourceId, semantic: target.semantic }
        : { path: target.target, value: target.value });
      setObjectPath(props, target.target, target.value);
      contentPaths.push(target.target);
    }
  }
  for (const item of plan.disabledProps) {
    if (!item.prop) continue;
    structureValues.push({ path: item.prop, value: item.value });
    setObjectPath(props, item.prop, item.value);
    contentPaths.push(item.prop);
  }
  if (plan.mediaTarget) {
    setObjectPath(props, plan.mediaTarget.path, pack.media.map(item => ({
      src: item.src,
      ...(item.kind ? { kind: item.kind } : {}),
      ...(item.type ? { type: item.type } : {}),
    })));
    contentPaths.push(plan.mediaTarget.path);
    if (plan.mediaTarget.countKey) {
      props[plan.mediaTarget.countKey] = pack.media.length;
      contentPaths.push(plan.mediaTarget.countKey);
    }
  }
  return {
    props,
    contentMap,
    resolvedProps: resolveContentMap({ presentation: pack }, contentMap, props),
    contentPaths: [...new Set([...contentPaths, ...Object.keys(contentMap)])],
    projectedItemIds: [...new Set(projectedItemIds)],
    chartBindings,
    structure: {
      arrays: structureArrays,
      values: structureValues,
      ...(plan.mediaTarget ? {
        media: {
          path: plan.mediaTarget.path,
          ...(plan.mediaTarget.countKey ? { countPath: plan.mediaTarget.countKey } : {}),
        },
      } : {}),
    },
    projectionPlan: plan,
  };
}

function structuralArrayProjection(container, items) {
  return {
    path: container.key,
    fields: container.fields.map(({ key, semantic }) => ({ key, semantic })),
    items: items.map((item, index) => ({
      sourceId: item.id,
      ...(item.chartSourceIds?.length ? { sourceIds: item.chartSourceIds } : {}),
      ...(Object.keys(container.itemStructures?.[index] || {}).length
        ? { structure: container.itemStructures[index] }
        : {}),
    })),
    ...(container.countKey ? { countPath: container.countKey } : {}),
  };
}

function projectionPlanFitsPropContract(layout, pack, plan) {
  try {
    return [0, 1, 2].every(variantIndex => {
      const projection = materializeProjectionWithPlan(layout, pack, variantIndex, plan);
      return normalizeProps(layout.layout, projection.resolvedProps).errors.length === 0;
    });
  } catch {
    return false;
  }
}

export function validateMaterializedTemplateProjection(layoutInput, value, props = {}, contentMap = {}, projection = null) {
  const layout = layoutInput?.fillPlan ? layoutInput : inspectLayout(layoutInput?.layout || layoutInput);
  const pack = normalizePageContentPack(value);
  const resolved = resolveContentMap({ presentation: pack }, contentMap, props);
  const normalized = normalizeProjectionText(JSON.stringify(resolved));
  const normalizedRuns = projectionFactRuns(resolved).map(normalizeProjectionText);
  const includesFact = fact => {
    const normalizedFact = normalizeProjectionText(fact);
    return normalized.includes(normalizedFact) || normalizedRuns.some(run => run.includes(normalizedFact));
  };
  const errors = [];
  if (projection && typeof projection === 'object') {
    const allowedChartModes = new Set(pack.chartData?.length ? ['full', 'summary'] : ['none']);
    if (!allowedChartModes.has(projection.chartMode)) errors.push(`invalid recorded chartMode ${projection.chartMode}`);
    for (const field of projection.contentPaths || []) {
      if (!objectPathFound(resolved, field)) errors.push(`recorded projection path ${field} is missing`);
    }
  }
  for (const fact of requiredPageContentFacts(pack)) {
    if (!includesFact(fact)) errors.push(`missing canonical required fact "${fact}"`);
  }
  if (pack.chartData?.length) {
    const full = pack.chartData.every(point => (
      includesFact(point.label)
      && includesFact(formatPageContentValue(point))
    ));
    const summary = normalizeProjectionText(summarizePageChartData(pack));
    const summarized = normalized.includes(summary) || normalizedRuns.some(run => run.includes(summary));
    if (!full && !summarized) errors.push('chartData must be projected in full or as the deterministic bounded summary');
    if (projection?.chartMode === 'full' && !full) errors.push('recorded full chart projection is incomplete');
    if (projection?.chartMode === 'summary' && !summarized) errors.push('recorded chart summary is missing');
  }
  for (const region of businessArrayRegions(layout)) {
    if (region.visibleCount <= 0 || objectPathFound(resolved, region.key)) continue;
    const disabled = disabledArrayProp(layout, region.field);
    if (disabled && sameScalarValue(objectPathValue(resolved, disabled.prop), disabled.value)) continue;
    errors.push(`visible business array ${region.key} is neither projected nor safely disabled`);
  }
  return errors;
}

export function layoutFamily(candidate) {
  return candidate?.structureFingerprint?.family
    || candidate?.projectionPlan?.structureFingerprint?.family
    || 'editorial';
}

function projectionItemsForPlan(pack, chartMode, emptyItemsBodyProjection = false) {
  const items = pageContentProjectionItems(pack);
  const chartItems = chartMode === 'summary' ? chartSummaryProjectionItems(pack) : [];
  const supporting = (emptyItemsBodyProjection ? [
    { id: 'support:summary-short', label: pack.summary.short, detailFull: '', detailShort: '', sourceIndex: 19_999, pinned: true },
    { id: 'support:core', label: pack.coreMessage, detailFull: '', detailShort: '', sourceIndex: 20_000 },
    { id: 'support:title-short', label: pack.title.short, detailFull: '', detailShort: '', sourceIndex: 20_001 },
  ] : [
    { id: 'support:summary', label: pack.summary.short, detailFull: pack.summary.full, detailShort: '', sourceIndex: 20_000 },
    ...(pack.title.full !== pack.title.short
      ? [{ id: 'support:title', label: pack.title.full, detailFull: '', detailShort: '', sourceIndex: 20_001 }]
      : []),
  ]).map(item => ({ formattedValue: '', hasValue: false, authoredRequired: false, pinned: false, required: false, priority: 'low', chartFact: false, ...item }));
  return [...items, ...chartItems, ...supporting]
    .filter((item, index, all) => all.findIndex(candidate => candidate.id === item.id) === index);
}

function chartSummaryProjectionItems(pack) {
  const points = pack.chartData || [];
  const summary = summarizePageChartData(pack);
  if (!summary) return [];
  const rows = [
    { id: 'chart-summary', label: summary, pinned: true, chartSourceIds: points.map(item => item.id) },
    { id: 'chart-first', label: `首值｜${points[0].label}${formatPageContentValue(points[0])}`, pinned: false, chartSourceIds: [points[0].id] },
    { id: 'chart-last', label: `末值｜${points.at(-1).label}${formatPageContentValue(points.at(-1))}`, pinned: false, chartSourceIds: [points.at(-1).id] },
  ];
  return rows.filter((item, index) => rows.findIndex(candidate => candidate.label === item.label) === index).map((item, index) => ({
    ...item,
    detailFull: '',
    detailShort: '',
    formattedValue: '',
    hasValue: false,
    authoredRequired: false,
    required: false,
    priority: item.pinned ? 'high' : 'low',
    chartFact: true,
    sourceIndex: 10_000 + index,
  }));
}

function chartProjectionItems(pack) {
  return (pack.chartData || []).map((item, index) => ({
    id: `chart:${item.id}`,
    label: item.label,
    detailFull: '',
    detailShort: '',
    value: item.value,
    ...(item.displayValue !== undefined ? { displayValue: item.displayValue } : {}),
    ...(item.unit !== undefined ? { unit: item.unit } : {}),
    formattedValue: formatPageContentValue(item),
    hasValue: true,
    authoredRequired: false,
    pinned: true,
    required: false,
    priority: 'high',
    chartFact: true,
    sourceIndex: index,
  }));
}

function scalarGroupContainer(layout, pinnedItems, allItems) {
  const slots = scalarGroupSlots(layout);
  if (!slots.length) return null;
  const capacity = slots.length;
  const acceptedItems = allItems.filter(item => slots.every(slot => scalarSlotFitsItem(item, slot.fields)));
  const acceptedIds = new Set(acceptedItems.map(item => item.id));
  const supportsValue = slots.some(slot => slot.fields.some(field => ['value', 'displayValue'].includes(field.semantic)));
  const supportsDetail = slots.some(slot => slot.fields.some(field => field.semantic === 'detail'));
  const requiredFits = pinnedItems.length <= capacity
    && acceptedItems.length >= capacity
    && pinnedItems.every(item => acceptedIds.has(item.id));
  return {
    kind: 'scalar-group',
    key: `scalar:${slots.map(slot => slot.key).join('|')}`,
    slots,
    capacity,
    minimumCapacity: capacity,
    countKey: null,
    supportsValue,
    supportsDetail,
    chartCapable: false,
    hasBusinessFields: true,
    acceptedItemIds: acceptedItems.map(item => item.id),
    slack: Math.max(0, capacity - pinnedItems.length),
    requiredFits,
    targetPaths: slots.flatMap(slot => slot.fields.map(field => field.key)),
    score: Number(requiredFits) * 120 + Number(supportsDetail) * 10 + Number(supportsValue) * 8 - Math.max(0, capacity - pinnedItems.length),
  };
}

function scalarSlotFitsItem(item, fields) {
  const semantics = new Set(fields.map(field => field.semantic));
  if (item.hasValue && !semantics.has('value') && !semantics.has('displayValue')) return false;
  if (item.unit && semantics.has('value') && !semantics.has('unit') && !semantics.has('displayValue')) return false;
  return itemFitsFields(item, fields, true);
}

function scalarGroupSlots(layout) {
  const fields = (layout?.fillPlan?.text || [])
    .filter(field => !String(field?.key || '').includes('[]'))
    .filter(field => ['string', 'number'].includes(field.type || 'string'))
    .map(field => {
      const pathName = String(field.key || '');
      const parts = pathName.split('.');
      const leaf = parts.pop() || '';
      const semantic = projectionSemantic(leaf, field.type || 'string', field.role);
      return {
        key: pathName,
        parent: parts.join('.'),
        leaf,
        semantic,
        type: field.type || 'string',
        maxChars: field.maxChars || 0,
        numericBounds: field.numericBounds || null,
        role: field.role,
      };
    })
    .filter(field => ['label', 'value', 'displayValue', 'unit', 'detail'].includes(field.semantic));
  const slots = [...numberedScalarSlots(fields), ...nestedScalarSlots(fields)];
  const usedPaths = new Set();
  return slots
    .sort((left, right) => left.key.localeCompare(right.key))
    .filter(slot => {
      if (slot.fields.some(field => usedPaths.has(field.key))) return false;
      slot.fields.forEach(field => usedPaths.add(field.key));
      return true;
    });
}

function numberedScalarSlots(fields) {
  const parents = new Map();
  for (const field of fields) {
    const match = /^(.*?)(\d+)$/.exec(field.leaf);
    if (!match || !match[1]) continue;
    const semantic = projectionSemantic(match[1], field.type, field.role);
    if (!['label', 'value', 'displayValue', 'unit', 'detail'].includes(semantic)) continue;
    const index = Number(match[2]);
    const groups = parents.get(field.parent) || new Map();
    groups.set(index, [...(groups.get(index) || []), { ...field, semantic }]);
    parents.set(field.parent, groups);
  }
  const slots = [];
  for (const [parent, groups] of parents) {
    const indices = [...groups.keys()].sort((left, right) => left - right);
    if (indices.length < 2 || indices.some((value, index) => index && value !== indices[index - 1] + 1)) continue;
    const candidates = indices.map(index => scalarSlot(`${parent || '<root>'}#${index}`, groups.get(index)));
    if (candidates.every(Boolean)) slots.push(...candidates);
  }
  return slots;
}

function nestedScalarSlots(fields) {
  const parents = new Map();
  for (const field of fields) {
    if (!field.parent) continue;
    parents.set(field.parent, [...(parents.get(field.parent) || []), field]);
  }
  return [...parents.entries()].map(([parent, items]) => scalarSlot(parent, items)).filter(Boolean);
}

function scalarSlot(key, fields) {
  const semantics = fields.map(field => field.semantic);
  if (new Set(semantics).size !== semantics.length) return null;
  if (!semantics.includes('label') || !semantics.some(value => ['value', 'displayValue', 'detail'].includes(value))) return null;
  const order = { label: 0, value: 1, displayValue: 1, unit: 2, detail: 3 };
  return { key, fields: [...fields].sort((left, right) => order[left.semantic] - order[right.semantic] || left.key.localeCompare(right.key)) };
}

function primaryArrayFields(layout) {
  return (layout?.fillPlan?.arrays || []).filter(field => (
    !String(field?.key || '').includes('[]')
    && arrayDepth(field?.itemShape) <= 1
  ));
}

function arrayContainer(layout, field, pinnedItems, allItems) {
  const fields = arrayProjectionFields(field);
  if (!fields) return null;
  const capacity = Number(field.maxCount || field.visibleCount || field.fixedLength || 0);
  if (!capacity) return null;
  const itemStructures = arrayItemStructures(layout, field, fields, capacity);
  if (!itemStructures) return null;
  const minimumCapacity = arrayMinimumCount(layout, field);
  const acceptedItems = allItems.filter(item => itemFitsFields(item, fields));
  const acceptedIds = new Set(acceptedItems.map(item => item.id));
  const selectedCount = Math.max(pinnedItems.length, minimumCapacity, allItems.length ? 1 : 0);
  const supportsValue = fields.some(item => ['value', 'displayValue'].includes(item.semantic));
  const supportsDetail = fields.some(item => item.semantic === 'detail');
  const allowsLabelOnly = Array.isArray(field.itemShape) && String(field.role || '').toLowerCase() === 'metric';
  const requiredFits = pinnedItems.length <= capacity
    && acceptedItems.length >= Math.max(minimumCapacity, allItems.length ? 1 : 0)
    && (!supportsValue || pinnedItems.some(item => item.hasValue) || allowsLabelOnly)
    && pinnedItems.every(item => acceptedIds.has(item.id));
  return {
    kind: 'array',
    key: field.key,
    field,
    fields,
    itemStructures,
    capacity,
    minimumCapacity,
    countKey: field.countKey || null,
    supportsValue,
    supportsDetail,
    chartCapable: supportsValue && isChartDataContainer(layout, field),
    hasBusinessFields: true,
    acceptedItemIds: acceptedItems.map(item => item.id),
    slack: Math.max(0, capacity - selectedCount),
    requiredFits,
    targetPaths: [field.key],
    score: Number(requiredFits) * 100 + Number(supportsDetail) * 10 + Number(supportsValue) * 8 - Math.max(0, capacity - selectedCount),
  };
}

function chartArrayContainer(layout, field, chartData) {
  const fields = arrayProjectionFields(field);
  if (!fields || !isChartDataContainer(layout, field)) return null;
  const capacity = Number(field.maxCount || field.visibleCount || field.fixedLength || 0);
  const itemStructures = arrayItemStructures(layout, field, fields, capacity);
  if (!itemStructures) return null;
  const minimumCapacity = arrayMinimumCount(layout, field);
  const items = chartProjectionItems({ chartData });
  if (!capacity || items.length < minimumCapacity || items.length > capacity) return null;
  if (!fields.some(item => ['value', 'displayValue'].includes(item.semantic))) return null;
  if (!items.every(item => itemFitsFields(item, fields))) return null;
  return {
    kind: 'chart-array',
    key: field.key,
    field,
    fields,
    itemStructures,
    capacity,
    minimumCapacity,
    countKey: field.countKey || null,
    supportsValue: true,
    supportsDetail: fields.some(item => item.semantic === 'detail'),
    chartCapable: true,
    hasBusinessFields: true,
    requiredFits: true,
    targetPaths: [field.key],
    score: 200 + Math.max(0, 20 - (capacity - items.length)),
  };
}

function arrayProjectionFields(field) {
  if (field.itemShape === 'string') {
    return [{ key: null, semantic: 'label', type: 'string', maxChars: field.item?.maxChars || 0 }];
  }
  if (Array.isArray(field.itemShape)) {
    if (String(field.role || '').toLowerCase() !== 'metric' || !field.itemShape.length) return null;
    if (field.itemShape.some(type => !['string', 'number'].includes(type))) return null;
    return field.itemShape.map((type, index) => ({
      key: index,
      semantic: index === 0 ? 'label' : index === 1 ? (type === 'number' ? 'value' : 'displayValue') : index === 2 ? 'unit' : 'optional',
      type,
      maxChars: field.item?.maxChars || 0,
      numericBounds: null,
    }));
  }
  if (!field.itemShape || typeof field.itemShape !== 'object' || Array.isArray(field.itemShape)) return null;
  const contracts = field.itemFields || {};
  const fields = [];
  for (const [key, typeValue] of Object.entries(field.itemShape)) {
    if (typeValue && typeof typeValue === 'object') return null;
    const type = contracts[key]?.type || typeValue;
    if (!['string', 'number'].includes(type)) continue;
    const role = contracts[key]?.role;
    let semantic = projectionSemantic(key, type, role);
    if (semantic === 'ordinal' && type === 'string' && role) semantic = 'label';
    if (['decorative', 'ordinal'].includes(semantic)) continue;
    if (!semantic) {
      if (type !== 'string') return null;
      semantic = 'optional';
    }
    if (['label', 'detail'].includes(semantic) && fields.some(item => item.semantic === semantic)) semantic = 'optional';
    fields.push({
      key,
      semantic,
      type,
      maxChars: contracts[key]?.maxChars || 0,
      numericBounds: contracts[key]?.numericBounds || null,
    });
  }
  if (fields.filter(item => item.semantic === 'value').length > 1) return null;
  if (fields.filter(item => item.semantic === 'displayValue').length > 1) return null;
  if (!fields.some(item => item.semantic === 'label')) {
    const fallback = fields.find(item => item.semantic === 'optional' && item.type === 'string');
    if (fallback) fallback.semantic = 'label';
  }
  return fields.some(item => item.semantic === 'label') ? fields : null;
}

function arrayItemStructures(layout, field, fields, capacity) {
  if (field.itemShape === 'string' || Array.isArray(field.itemShape)) return [];
  const projectedKeys = new Set(fields.map(item => item.key).filter(Boolean));
  const structuralFields = Object.entries(field.itemShape || {})
    .filter(([key]) => !projectedKeys.has(key))
    .map(([key, shape]) => ({
      key,
      shape,
      semantic: projectionSemantic(key, field.itemFields?.[key]?.type || shape, field.itemFields?.[key]?.role),
    }));
  if (!structuralFields.length) return Array.from({ length: capacity }, () => ({}));
  const defaults = valueAtPath(getLayoutRecord(layout?.layout)?.defaultProps || {}, field.key);
  if (!Array.isArray(defaults) || !defaults.length) return null;
  const structures = [];
  for (let index = 0; index < capacity; index += 1) {
    const source = defaults[index] || defaults[index % defaults.length];
    if (!source || typeof source !== 'object' || Array.isArray(source)) return null;
    const structure = {};
    for (const { key, shape, semantic } of structuralFields) {
      const value = source[key];
      const fallback = defaults.map(item => item?.[key]).find(item => scalarMatchesShape(item, shape));
      const structuralValue = safeStructuralValue({ key, shape, semantic, value, fallback, index });
      if (structuralValue === undefined) return null;
      structure[key] = structuralValue;
    }
    structures.push(structure);
  }
  return structures;
}

function safeStructuralValue({ key, shape, semantic, value, fallback, index }) {
  const type = String(shape || '');
  if (type === 'boolean') return typeof value === 'boolean' ? value : false;
  if (semantic === 'ordinal') return type === 'number' ? index + 1 : String(index + 1);
  if (type === 'string') {
    if (semantic !== 'decorative') return '';
    if (!/^(?:align|alignment|icon|position|side|style)$/i.test(key)) return undefined;
  }
  if (scalarMatchesShape(value, shape)) return value;
  if (scalarMatchesShape(fallback, shape)) return fallback;
  return undefined;
}

function scalarMatchesShape(value, shape) {
  if (value === undefined || value === null) return false;
  return String(shape || '').split('|').map(item => item.trim()).includes(typeof value);
}

function projectionSemantic(key, type, role = '') {
  const name = String(key || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const normalizedRole = String(role || '').toLowerCase();
  if (/color|colour|tone|icon|style|fill|stroke|accent|kind|type|align|position|side/.test(name)) return 'decorative';
  if (isOrdinalKey(name)) return 'ordinal';
  if (/unit|suffix/.test(name)) return 'unit';
  if (type === 'number') return 'value';
  if (/value|amount|score|rate|percent|pct|metric|stat|delta|count|axismax|axismin|target|baseline|bignumber|^v$|^big$/.test(name) || normalizedRole === 'metric') {
    return 'displayValue';
  }
  if (/detail|desc|description|body|summary|sub|note|meta|explain|content|^ds$/.test(name) || ['body', 'paragraph'].includes(normalizedRole)) return 'detail';
  if (/label|title|name|heading|topic|category|item|text|copy|statement|caption|tag|role|round|period|phase|stage|^t$|^e$|^en$|^cn$|^lb$|^q$/.test(name) || ['title', 'eyebrow', 'list-item'].includes(normalizedRole)) return 'label';
  return null;
}

function isOrdinalKey(name) {
  return /^(?:no|num|number|index|ordinal|rank|page|pg|date|year|month|day|n|navcurrent|pagecurrent)$/.test(name)
    || /(?:index|ordinal|rank|pageno|pageindex|year|month|day)$/.test(name);
}

function itemFitsFields(item, fields, exact = false) {
  return fields.every(field => projectionFieldAvailable(item, field, fields, exact));
}

function projectionFieldAvailable(item, target, fields = [], exact = false) {
  const value = projectionFieldValue(item, target.semantic, fields, exact);
  if (target.semantic === 'value') {
    if (!(typeof value === 'number' && Number.isFinite(value))) return false;
    const bounds = target.numericBounds;
    if (bounds?.enforced && (
      (Number.isFinite(bounds.min) && value < bounds.min)
      || (Number.isFinite(bounds.max) && value > bounds.max)
    )) return false;
  } else if (target.semantic === 'label' && !String(value || '').trim()) {
    return false;
  } else if (target.semantic === 'displayValue' && item.hasValue && !String(value || '').trim()) {
    return false;
  }
  return !value || !target.maxChars || charLength(String(value)) <= target.maxChars;
}

function projectionFieldValue(item, semantic, fields = [], exact = false) {
  const hasSeparateValue = fields.some(field => ['value', 'displayValue'].includes(field.semantic));
  const hasSeparateUnit = fields.some(field => field.semantic === 'unit');
  const hasDetail = fields.some(field => field.semantic === 'detail');
  if (semantic === 'label') {
    if (exact) return item.label || '';
    return [
      item.label,
      !hasDetail ? item.detailShort || item.detailFull : '',
      item.hasValue && (!hasSeparateValue || (item.unit && !hasSeparateUnit)) ? item.formattedValue : '',
    ].filter(Boolean).join(' · ');
  }
  if (semantic === 'detail') return exact
    ? item.detailShort || item.detailFull || ''
    : item.detailShort || item.detailFull || (!hasSeparateValue ? item.formattedValue : '') || '';
  if (semantic === 'unit') return item.unit || '';
  if (semantic === 'value') return item.value;
  if (semantic === 'displayValue') {
    if (!item.hasValue) return '';
    if (!hasSeparateUnit) return item.formattedValue;
    let display = item.displayValue !== undefined ? String(item.displayValue) : String(item.value ?? '');
    if (item.unit) while (display.endsWith(item.unit)) display = display.slice(0, -item.unit.length).trimEnd();
    return display;
  }
  return '';
}

function materializeArrayItem(container, item, index) {
  if (container.field.itemShape === 'string') return projectionFieldValue(item, 'label', container.fields);
  if (Array.isArray(container.field.itemShape)) {
    return container.fields.map(field => projectionFieldValue(item, field.semantic, container.fields));
  }
  return {
    ...(container.itemStructures?.[index] || {}),
    ...Object.fromEntries(container.fields.map(field => [field.key, projectionFieldValue(item, field.semantic, container.fields)])),
  };
}

function orderProjectionItems(items, variantIndex) {
  const pinned = items.filter(item => item.pinned);
  const optional = items.filter(item => !item.pinned);
  if (variantIndex % 3 === 1) {
    return [...pinned].sort((a, b) => Number(b.hasValue) - Number(a.hasValue) || b.sourceIndex - a.sourceIndex)
      .concat([...optional].reverse());
  }
  if (variantIndex % 3 === 2) {
    return [...pinned].sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority) || a.label.localeCompare(b.label))
      .concat(optional);
  }
  return [...pinned, ...optional].sort((a, b) => a.sourceIndex - b.sourceIndex);
}

function priorityRank(value) {
  return ({ critical: 0, high: 1, medium: 2, low: 3 })[String(value || '').toLowerCase()] ?? 4;
}

function takeProjectionItems(items, count) {
  const selected = items.slice(0, count);
  const pinned = items.filter(item => item.pinned);
  for (const item of pinned) {
    if (selected.some(candidate => candidate.id === item.id)) continue;
    const replaceIndex = selected.findLastIndex(candidate => !candidate.pinned);
    if (replaceIndex < 0) throw new Error(`Projection capacity cannot preserve pinned fact ${item.id}`);
    selected[replaceIndex] = item;
  }
  return selected;
}

function businessArrayRegions(layout) {
  const regions = new Map();
  for (const field of layout?.fillPlan?.arrays || []) {
    const key = arrayRegionKey(field.key);
    if (!key) continue;
    const current = regions.get(key);
    if (!current || String(field.key) === key) {
      regions.set(key, { key, field, visibleCount: arrayVisibleCount(layout, field) });
    }
  }
  return [...regions.values()];
}

function arrayRegionKey(value) {
  return String(value || '').replace(/\[\]$/, '');
}


function arrayVisibleCount(layout, field) {
  const control = (layout?.controls || []).find(item => (
    item.key === field.countKey || item.publicKey === field.countKey
  ));
  return Number(field.visibleCount ?? field.fixedLength ?? control?.default ?? 0) || 0;
}

function objectPathFound(target, pathName) {
  let cursor = target;
  for (const part of String(pathName || '').split('.').filter(Boolean)) {
    if (!cursor || typeof cursor !== 'object' || !Object.prototype.hasOwnProperty.call(cursor, part)) return false;
    cursor = cursor[part];
  }
  return true;
}

function objectPathValue(target, pathName) {
  let cursor = target;
  for (const part of String(pathName || '').split('.').filter(Boolean)) {
    if (!cursor || typeof cursor !== 'object') return undefined;
    cursor = cursor[part];
  }
  return cursor;
}

function sameScalarValue(left, right) {
  return String(left) === String(right);
}

function normalizeProjectionText(value) {
  return String(value || '').normalize('NFKC').toLowerCase().replace(/[\s"'`，。；、,:;·｜]/g, '');
}

function projectionFactRuns(value, result = []) {
  if (Array.isArray(value)) value.forEach(item => projectionFactRuns(item, result));
  else if (value && typeof value === 'object') {
    const fields = Object.entries(value).filter(([, item]) => ['string', 'number'].includes(typeof item));
    fields.forEach(([, item]) => result.push(String(item)));
    const values = fields.filter(([key, item]) => ['value', 'displayValue'].includes(projectionSemantic(key, typeof item)));
    const units = fields.filter(([key, item]) => projectionSemantic(key, typeof item) === 'unit');
    projectionFactPairs(values, units).forEach(([[, item], [, unit]]) => result.push(formatPageContentValue({ displayValue: String(item), unit: String(unit) })));
    Object.values(value).forEach(item => {
      if (item && typeof item === 'object') projectionFactRuns(item, result);
    });
  }
  return result;
}

function projectionFactPairs(values, units) {
  if (values.length === 1 && units.length === 1) {
    const valueSlot = projectionFieldSlot(values[0][0], 'value');
    const unitSlot = projectionFieldSlot(units[0][0], 'unit');
    const bothUnslotted = valueSlot === '' && unitSlot === '';
    const sameExplicitSlot = valueSlot !== '' && valueSlot === unitSlot;
    return bothUnslotted || sameExplicitSlot ? [[values[0], units[0]]] : [];
  }
  const valueSlots = projectionFieldsBySlot(values, 'value');
  const unitSlots = projectionFieldsBySlot(units, 'unit');
  const pairs = [];
  for (const [slot, candidates] of valueSlots) {
    const matchingUnits = unitSlots.get(slot) || [];
    if (candidates.length === 1 && matchingUnits.length === 1) {
      pairs.push([candidates[0], matchingUnits[0]]);
    }
  }
  return pairs;
}

function projectionFieldsBySlot(fields, semantic) {
  const grouped = new Map();
  for (const field of fields) {
    const slot = projectionFieldSlot(field[0], semantic);
    grouped.set(slot, [...(grouped.get(slot) || []), field]);
  }
  return grouped;
}

function projectionFieldSlot(key, semantic) {
  const name = String(key || '').normalize('NFKC').toLowerCase().replace(/[^a-z0-9]/g, '');
  const markers = semantic === 'unit'
    ? ['suffix', 'unit']
    : ['displayvalue', 'bignumber', 'axismax', 'axismin', 'baseline', 'percent', 'amount', 'score', 'metric', 'stat', 'delta', 'count', 'target', 'value', 'rate', 'pct', 'big', 'v'];
  if (markers.includes(name)) return '';
  for (const marker of markers) {
    if (name.startsWith(marker) && name.length > marker.length) return name.slice(marker.length);
    if (name.endsWith(marker) && name.length > marker.length) return name.slice(0, -marker.length);
  }
  return semantic === 'value' ? name : '';
}

function supportingTextSource(field, pack, items, usedValues) {
  if (isOrdinalTextField(field)) return null;
  const semantic = projectionSemantic(field.key, field.type, field.role);
  if (!semantic || semantic === 'decorative') return null;
  const itemFacts = pack.items.map((item, index) => ({
    item,
    projected: items.find(candidate => candidate.id === item.id),
    root: `presentation.items[${index}]`,
  }));
  const chartFacts = (pack.chartData || []).map((item, index) => ({
    item,
    projected: items.find(candidate => candidate.id === item.id || candidate.id === `chart:${item.id}`),
    root: `presentation.chartData[${index}]`,
  }));
  const facts = [...itemFacts, ...chartFacts];
  /** @type {Array<
   * | { source: string, value: string | number }
   * | { sourceId: string, semantic: 'formattedValue', value: string }
   * >} */
  let candidates = [];
  if (semantic === 'value') {
    candidates = facts
      .filter(({ item }) => typeof item.value === 'number' && Number.isFinite(item.value))
      .map(({ item, root }) => ({ source: `${root}.value`, value: item.value }));
  } else if (semantic === 'displayValue') {
    candidates = facts.flatMap(({ item, projected, root }) => {
      /** @type {typeof candidates} */
      const matches = item.displayValue
        ? [{ source: `${root}.displayValue`, value: item.displayValue }]
        : projected?.formattedValue
          ? [{ sourceId: projected.id, semantic: 'formattedValue', value: projected.formattedValue }]
          : [];
      return matches;
    });
  } else if (semantic === 'unit') {
    candidates = facts
      .filter(({ item }) => item.unit)
      .map(({ item, root }) => ({ source: `${root}.unit`, value: item.unit }));
  } else if (semantic === 'detail') {
    candidates = [
      { source: 'presentation.summary.short', value: pack.summary.short },
      { source: 'presentation.summary.full', value: pack.summary.full },
      ...itemFacts.flatMap(({ item, root }) => [
        { source: `${root}.detail.short`, value: item.detail.short },
        { source: `${root}.detail.full`, value: item.detail.full },
      ]),
    ];
  } else {
    candidates = [
      { source: 'presentation.title.full', value: pack.title.full },
      { source: 'presentation.summary.short', value: pack.summary.short },
      { source: 'presentation.pageIntent', value: pack.pageIntent },
      ...itemFacts.map(({ item, root }) => ({ source: `${root}.label`, value: item.label })),
      ...chartFacts.map(({ item, root }) => ({ source: `${root}.label`, value: item.label })),
    ];
  }
  const budget = Number(field.maxChars || 0);
  return candidates.find(candidate => (
    candidate.value !== undefined
    && candidate.value !== null
    && String(candidate.value).trim()
    && !usedValues.has(String(candidate.value))
    && (!budget || charLength(String(candidate.value)) <= budget)
  )) || null;
}

function titleFieldScore(field) {
  const key = String(field?.key || '').toLowerCase();
  const role = String(field?.role || '').toLowerCase();
  return Number(role === 'title') * 100 + Number(/title|headline|heading/.test(key)) * 30 + Number(field.maxChars || 0) / 100;
}

function isBodyTextField(field) {
  return ['body', 'paragraph'].includes(String(field?.role || '').toLowerCase())
    || /summary|body|desc|description|sub|takeaway/.test(String(field?.key || '').toLowerCase());
}

function isOrdinalTextField(field) {
  const key = String(field?.key || '').split('.').at(-1)?.toLowerCase().replace(/[^a-z0-9]/g, '') || '';
  return isOrdinalKey(key);
}

function disabledTextProp(layout, field) {
  const names = [field?.key, String(field?.key || '').split('.').at(-1)]
    .map(value => String(value || '').toLowerCase().replace(/[^a-z0-9]/g, ''))
    .filter(Boolean);
  const toggle = (layout?.controls || []).find(control => {
    if (control.type !== 'toggle') return false;
    const key = String(control.publicKey || control.key || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    const subject = key.startsWith('show') ? key.slice(4) : '';
    return subject && names.some(name => name.includes(subject) || subject.includes(name));
  });
  return toggle ? { prop: toggle.publicKey || toggle.key, value: false } : null;
}

function arrayMinimumCount(layout, field) {
  if (!field.countKey) return Number(field.fixedLength || field.visibleCount || 0);
  const binding = (layout?.countBindings || []).find(item => item.key === field.countKey || item.publicKey === field.countKey);
  return Number(binding?.min || 0);
}

function isChartDataContainer(layout, field) {
  const text = `${layout?.slot || ''} ${layout?.label || ''} ${(layout?.roles || []).join(' ')} ${field?.key || ''}`.toLowerCase();
  return /chart|trend|distribution|relationship|comparison|ranking|treemap|radar|donut|waterfall|sankey|scatter|plot|bar|line|area|图|趋势|分布|关系|对比|排行|矩形树|雷达|瀑布/.test(text);
}

function arrayFieldAcceptsEmptyValue(layout, field) {
  const pathName = String(field?.key || '');
  if (!pathName || pathName.includes('[]')) return false;
  if (field.fixedLength || field.fixedLengths || field.sameLengthAs) return false;
  const binding = (layout?.countBindings || []).find(item => (
    item.key === field.countKey || item.publicKey === field.countKey
  ));
  const minimum = field.min ?? binding?.min;
  if (minimum != null && Number(minimum) > 0) return false;
  return Array.isArray(objectPathValue(layout?.propShapes || {}, pathName));
}

function disabledArrayProp(layout, field) {
  if (Number(field.visibleCount || 0) === 0) return { prop: field.countKey || '', value: 0 };
  const binding = (layout?.countBindings || []).find(item => item.key === field.countKey || item.publicKey === field.countKey);
  const minimum = field.min ?? binding?.min;
  if (field.countKey && minimum != null && Number(minimum) === 0) return { prop: field.countKey, value: 0 };
  return disabledArrayToggleProp(layout, field);
}

function disabledArrayToggleProp(layout, field) {
  const names = [field?.key, String(field?.key || '').split('.').at(-1)]
    .map(value => String(value || '').toLowerCase().replace(/[^a-z0-9]/g, ''))
    .filter(Boolean);
  const toggle = (layout?.controls || []).find(control => {
    if (control.type !== 'toggle') return false;
    const key = String(control.publicKey || control.key || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    const subject = key.startsWith('show') ? key.slice(4) : '';
    return subject && names.some(name => name.startsWith(subject) || subject.startsWith(name));
  });
  return toggle ? { prop: toggle.publicKey || toggle.key, value: false } : null;
}

function buildMediaProjectionPlan(layout, pack, contentCountKeys = new Set()) {
  const media = pack.media || [];
  const slots = layout?.mediaSlots || [];
  const disabledProps = [];
  if (media.length) {
    const slot = slots.find(item => (
      item.canPresetMedia
      && mediaCapacity(item) >= media.length
      && media.every(mediaItem => slotAcceptsKind(item, pageContentMediaKind(mediaItem)))
    ));
    if (!slot) return { requiredFits: false, disabledProps, mediaTarget: null };
    return {
      requiredFits: true,
      disabledProps,
      mediaTarget: {
        path: String(slot.presetProp || slot.writableProp || slot.fieldPath || '').replace(/^props\./, ''),
        countKey: slot.publicCountKey || slot.countKey || null,
      },
    };
  }
  for (const slot of slots) {
    if (Number(slot.defaultVisibleCount ?? slot.defaultCount ?? 0) <= 0) continue;
    const countKey = slot.publicCountKey || slot.countKey || null;
    const field = { key: slot.field, countKey, visibleCount: slot.defaultVisibleCount ?? slot.defaultCount, min: slot.min };
    const disabled = countKey && contentCountKeys.has(countKey)
      ? disabledArrayToggleProp(layout, field)
      : disabledArrayProp(layout, field);
    if (!disabled) return { requiredFits: false, disabledProps, mediaTarget: null };
    disabledProps.push(disabled);
  }
  return { requiredFits: true, disabledProps, mediaTarget: null };
}

function pageContentMediaKind(item) {
  const declared = normalizeMediaKind(item?.kind);
  if (declared === 'image' || declared === 'video') return declared;
  return String(item?.type || '').toLowerCase().startsWith('video/') ? 'video' : 'image';
}

function mediaCapacity(slot) {
  return Number(slot.maxCount || slot.max || slot.defaultVisibleCount || slot.defaultCount || 0);
}

function structureFingerprint(layout, plan) {
  const primary = plan.primaryContentContainer;
  const label = `${layout?.slot || ''} ${layout?.label || ''} ${(layout?.roles || []).join(' ')}`.toLowerCase();
  let family = 'editorial';
  if (/table|ranking|leaderboard|表|排行|清单/.test(label)) family = 'table';
  else if (/matrix|quadrant|矩阵|象限/.test(label)) family = 'matrix';
  else if (/timeline|roadmap|process|step|sequence|时间|路线|流程|阶段/.test(label)) family = 'sequence';
  else if (/compare|versus|comparison|对比|竞品|差异/.test(label)) family = 'comparison';
  else if (/chart|trend|radar|donut|waterfall|plot|图|趋势|雷达|瀑布/.test(label)) family = 'chart';
  else if (/hero|statement|quote|封面|宣言|观点/.test(label)) family = 'hero';
  else if (/card|grid|list|tile|卡|网格|列表/.test(label)) family = 'cards';
  else if (primary?.supportsValue) family = 'metrics';
  else if ((primary?.capacity || 0) >= 3) family = 'cards';
  else if (layout?.mediaSlots?.length) family = 'media';
  const primaryShape = primary
    ? `${primary.kind}:${primary.supportsValue ? 'value' : 'text'}:${primary.supportsDetail ? 'detail' : 'compact'}:${primary.capacity}`
    : 'none';
  const composition = primary || isCoverCandidate(layout.layout)
    ? `${family}:${primary?.kind || 'none'}:${primary?.capacity || 0}`
    : `${family}:empty:${layoutSkeletonShape(layout)}`;
  return { family, primaryShape, composition };
}

function layoutSkeletonShape(layout) {
  const text = (layout?.fillPlan?.text || []).map(field => {
    const semantic = projectionSemantic(field.key, field.type || 'string', field.role);
    if (!semantic || ['decorative', 'ordinal'].includes(semantic)) return null;
    return `${semantic}:${String(field.role || 'copy').toLowerCase()}:${Math.ceil(Number(field.maxChars || 0) / 20)}`;
  }).filter(Boolean).sort();
  const arrays = businessArrayRegions(layout).map(({ field, visibleCount }) => {
    const semantics = (arrayProjectionFields(field) || [])
      .map(item => item.semantic).filter(value => value !== 'optional').sort().join('+');
    return `${String(field.role || 'array').toLowerCase()}:${semantics || 'opaque'}:${visibleCount}`;
  }).sort();
  const scalars = scalarGroupSlots(layout)
    .map(slot => slot.fields.map(field => field.semantic).sort().join('+')).sort();
  const media = (layout?.mediaSlots || [])
    .filter(slot => Number(slot.defaultVisibleCount ?? slot.defaultCount ?? 0) > 0)
    .map(slot => `${String(slot.role || 'media').toLowerCase()}:${mediaCapacity(slot)}:${Array.from(slot.acceptedKinds || []).sort().join('+') || 'any'}`)
    .sort();
  return `t=${text.join(',') || 'none'};a=${arrays.join(',') || 'none'};s=${scalars.join(',') || 'none'};m=${media.join(',') || 'none'}`;
}

function setObjectPath(target, pathName, value) {
  const parts = String(pathName || '').split('.').filter(Boolean);
  let cursor = target;
  parts.forEach((part, index) => {
    if (index === parts.length - 1) cursor[part] = value;
    else cursor = cursor[part] ||= {};
  });
}

function arrayDepth(value) {
  if (Array.isArray(value)) return 1 + arrayDepth(value[0]);
  if (!value || typeof value !== 'object') return 0;
  return Object.values(value).reduce((max, child) => Math.max(max, arrayDepth(child)), 0);
}

function getRequestedMediaCount({ plannedImages, providedImages, providedMedia, imageGen, needsVisual, mediaCount }) {
  const explicit = Number(mediaCount);
  if (Number.isFinite(explicit) && explicit > 0) return Math.round(explicit);
  const provided = mediaIntentCount(providedImages) || mediaIntentCount(providedMedia);
  if (provided) return provided;
  const planned = mediaIntentCount(plannedImages);
  if (planned) return planned;
  if (imageGen || needsVisual) return 1;
  return 0;
}

function mediaIntentCount(value) {
  if (Array.isArray(value)) return value.length;
  if (value === true) return 1;
  const number = Number(value);
  if (Number.isFinite(number) && number > 0) return Math.round(number);
  return 0;
}
