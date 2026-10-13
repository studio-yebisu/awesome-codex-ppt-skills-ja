export const BESPOKE_SCHEMA_VERSION = 2;
export const BESPOKE_LIST_ITEM_LIMIT = 8;
export const BESPOKE_CHART_POINT_LIMIT = 12;
export const TEMPLATE_VARIANT_COUNT = 3;
export const TOTAL_VARIANT_COUNT = 4;

const TEMPLATE_KIND = 'template';
const BESPOKE_KIND = 'bespoke';
const PAGE_INTENT_ALIASES = new Map([
  ...['cover', 'title', 'opening', 'opener', '封面', '首页', '开场'].map(value => [value, 'cover']),
  ...['closing', 'close', 'ending', 'end', '封底', '结尾', '结束', '收尾'].map(value => [value, 'closing']),
  ...['body', 'content', 'main', 'interior', '正文', '内容', '主体', '内页'].map(value => [value, 'body']),
]);
const UNSAFE_KEYS = new Set(['__proto__', 'prototype', 'constructor']);
const FORBIDDEN_COMPOSITION_KEYS = new Set(['html', 'jsx', 'style', 'classname', 'controls']);
const PATH_PATTERN = /^[A-Za-z_$][A-Za-z0-9_$-]*(?:\[(?:0|[1-9]\d*)\]|\.[A-Za-z_$][A-Za-z0-9_$-]*)*$/;
const PATH_TOKEN_PATTERN = /([A-Za-z_$][A-Za-z0-9_$-]*)|\[(\d+)\]/g;
const MAX_PATH_INDEX = 9999;

const BACKGROUNDS = new Set(['default', 'surface', 'muted', 'accent', 'dark', 'light']);
const ELEMENT_TYPES = new Set(['text', 'metric', 'list', 'quote', 'media', 'shape', 'chart']);
const ELEMENT_TONES = new Set(['default', 'muted', 'accent', 'positive', 'warning', 'critical', 'inverse']);
const TEXT_ROLES = new Set(['kicker', 'title', 'subtitle', 'body', 'caption', 'label']);
const TEXT_ALIGNS = new Set(['left', 'center', 'right']);
const MEDIA_FITS = new Set(['cover', 'contain']);
const SHAPES = new Set(['rect', 'circle', 'line', 'panel']);
const CHART_TYPES = new Set(['bar', 'line', 'donut', 'progress']);
const DESIGN_INTENT_FIELDS = ['objective', 'audience', 'narrativeRole', 'emphasis', 'rationale'];
const GRID_FIELDS = ['column', 'row', 'width', 'height'];
const COMMON_ELEMENT_FIELDS = new Set(['id', 'type', 'grid', 'tone']);
const ELEMENT_FIELDS = {
  text: new Set([...COMMON_ELEMENT_FIELDS, 'text', 'role', 'align']),
  metric: new Set([...COMMON_ELEMENT_FIELDS, 'sourceId', 'value', 'label', 'detail', 'trend']),
  list: new Set([...COMMON_ELEMENT_FIELDS, 'items', 'ordered']),
  quote: new Set([...COMMON_ELEMENT_FIELDS, 'quote', 'attribution']),
  media: new Set([...COMMON_ELEMENT_FIELDS, 'src', 'alt', 'fit']),
  shape: new Set([...COMMON_ELEMENT_FIELDS, 'shape']),
  chart: new Set([...COMMON_ELEMENT_FIELDS, 'chartType', 'data', 'showValues']),
};

export function getVariantKind(variant) {
  if (!variant || typeof variant !== 'object' || Array.isArray(variant)) return null;
  if (variant.kind === TEMPLATE_KIND || variant.kind === BESPOKE_KIND) return variant.kind;
  if (variant.kind != null) return null;
  return typeof (variant.layout || variant.layoutName) === 'string'
    && String(variant.layout || variant.layoutName).trim()
    ? TEMPLATE_KIND
    : null;
}

export function isTemplateVariant(variant) {
  return getVariantKind(variant) === TEMPLATE_KIND;
}

export function isBespokeVariant(variant) {
  return getVariantKind(variant) === BESPOKE_KIND;
}

export function isExpandedVariantSlide(slide, schemaVersion = BESPOKE_SCHEMA_VERSION) {
  if (Number(schemaVersion) !== BESPOKE_SCHEMA_VERSION) return false;
  const variants = slide?.variants;
  if (!Array.isArray(variants) || variants.length !== TOTAL_VARIANT_COUNT) return false;
  return variants
    .slice(0, TEMPLATE_VARIANT_COUNT)
    .every(variant => variant?.kind === TEMPLATE_KIND)
    && variants[TEMPLATE_VARIANT_COUNT]?.kind === BESPOKE_KIND;
}

export function validateContentMap(contentMap, content) {
  const errors = [];
  if (contentMap == null) return errors;
  if (!isPlainRecord(contentMap)) {
    return ['contentMap: expected an object of target path -> content path'];
  }

  let safeContent = content;
  if (content !== undefined) {
    try {
      safeContent = safeDeepClone(content, 'content');
    } catch (error) {
      errors.push(error.message);
      safeContent = undefined;
    }
  }

  for (const [targetPath, sourcePath] of Object.entries(contentMap)) {
    const targetTokens = parseMappedPath(targetPath, `contentMap target "${targetPath}"`, errors);
    if (typeof sourcePath !== 'string' || !sourcePath.trim()) {
      errors.push(`contentMap target "${targetPath}": source path must be a non-empty string`);
      continue;
    }
    const sourceTokens = parseMappedPath(sourcePath, `contentMap source "${sourcePath}"`, errors);
    if (!targetTokens || !sourceTokens || safeContent === undefined) continue;
    if (!readPath(safeContent, sourceTokens).found) {
      errors.push(`contentMap target "${targetPath}": missing source path "${sourcePath}"`);
    }
  }
  return errors;
}

export function resolveContentMap(content, contentMap, base = {}) {
  const errors = validateContentMap(contentMap, content);
  if (errors.length) throw new Error(errors.join('\n'));
  const safeContent = safeDeepClone(content ?? {}, 'content');
  const resolved = safeDeepClone(base ?? {}, 'contentMap base');
  if (!isPlainRecord(resolved)) {
    throw new Error('contentMap base: expected an object');
  }

  for (const [targetPath, sourcePath] of Object.entries(contentMap || {})) {
    const targetTokens = parsePath(targetPath);
    const sourceTokens = parsePath(sourcePath);
    const source = readPath(safeContent, sourceTokens);
    if (!source.found) {
      throw new Error(`contentMap target "${targetPath}": missing source path "${sourcePath}"`);
    }
    writePath(resolved, targetTokens, safeDeepClone(source.value, `content.${sourcePath}`), targetPath);
  }
  return resolved;
}


export function validatePageContentPack(value) {
  const errors = [];
  if (!isPlainRecord(value)) return ['presentation: expected a PageContentPack object'];
  for (const field of ['pageIntent', 'coreMessage']) {
    if (!isNonEmptyString(value[field])) errors.push(`presentation.${field}: expected a non-empty string`);
  }
  validateTextPair(value.title, 'presentation.title', errors);
  validateTextPair(value.summary, 'presentation.summary', errors);

  const itemsById = new Map();
  if (!Array.isArray(value.items)) {
    errors.push('presentation.items: expected an array');
  } else {
    const ids = new Set();
    value.items.forEach((item, index) => {
      const path = `presentation.items[${index}]`;
      if (!isPlainRecord(item)) {
        errors.push(`${path}: expected an object`);
        return;
      }
      if (!isNonEmptyString(item.id)) errors.push(`${path}.id: expected a stable non-empty string`);
      else if (ids.has(item.id)) errors.push(`${path}.id: duplicate id "${item.id}"`);
      else {
        ids.add(item.id);
        itemsById.set(item.id, item);
      }
      if (!isNonEmptyString(item.label)) errors.push(`${path}.label: expected a non-empty string`);
      validateOptionalTextPair(item.detail, `${path}.detail`, errors);
      validateFactValue(item, path, errors);
      if (item.required != null && typeof item.required !== 'boolean') {
        errors.push(`${path}.required: expected a boolean`);
      }
      if (item.priority != null && !isNonEmptyString(item.priority)) {
        errors.push(`${path}.priority: expected a non-empty string`);
      }
    });
  }

  if (value.chartData != null) {
    if (!Array.isArray(value.chartData)) {
      errors.push('presentation.chartData: expected an array');
    } else {
      const ids = new Set();
      value.chartData.forEach((item, index) => {
        const path = `presentation.chartData[${index}]`;
        if (!isPlainRecord(item)) {
          errors.push(`${path}: expected an object`);
          return;
        }
        if (!isNonEmptyString(item.id)) errors.push(`${path}.id: expected a stable non-empty string`);
        else if (ids.has(item.id)) errors.push(`${path}.id: duplicate id "${item.id}"`);
        else ids.add(item.id);
        if (!isNonEmptyString(item.label)) errors.push(`${path}.label: expected a non-empty string`);
        if (typeof item.value !== 'number' || !Number.isFinite(item.value)) {
          errors.push(`${path}.value: expected a finite number`);
        }
        validateFactValue(item, path, errors);
        const matchingItem = itemsById.get(item.id);
        if (matchingItem && !sameFactIdentity(matchingItem, item)) {
          errors.push(`${path}.id: conflicts with presentation.items id "${item.id}"; label/value/unit must match exactly`);
        }
      });
    }
  }

  if (value.media != null) {
    if (!Array.isArray(value.media)) {
      errors.push('presentation.media: expected an array');
    } else {
      value.media.forEach((item, index) => {
        const path = `presentation.media[${index}]`;
        if (!isPlainRecord(item) || !isNonEmptyString(item.src)) {
          errors.push(`${path}.src: expected a non-empty staged media source`);
        }
      });
    }
  }
  return unique(errors);
}

export function classifyPageIntent(value) {
  const normalized = String(value || '').normalize('NFKC').trim().toLowerCase();
  return PAGE_INTENT_ALIASES.get(normalized) || 'body';
}

export function normalizePageContentPack(value) {
  const errors = validatePageContentPack(value);
  if (errors.length) throw new Error(errors.join('\n'));
  return {
    pageIntent: value.pageIntent.trim(),
    coreMessage: value.coreMessage.trim(),
    title: normalizeTextPair(value.title),
    summary: normalizeTextPair(value.summary),
    items: value.items.map(item => ({
      id: item.id.trim(),
      label: item.label.trim(),
      detail: normalizeOptionalTextPair(item.detail),
      ...(item.value !== undefined ? { value: item.value } : {}),
      ...(item.displayValue !== undefined ? { displayValue: String(item.displayValue).trim() } : {}),
      ...(item.unit !== undefined ? { unit: String(item.unit).trim() } : {}),
      ...(item.required !== undefined ? { required: item.required } : {}),
      ...(item.priority !== undefined ? { priority: item.priority.trim() } : {}),
    })),
    ...(Array.isArray(value.chartData) ? {
      chartData: value.chartData.map(item => ({
        id: item.id.trim(),
        label: item.label.trim(),
        value: item.value,
        ...(item.displayValue !== undefined ? { displayValue: String(item.displayValue).trim() } : {}),
        ...(item.unit !== undefined ? { unit: String(item.unit).trim() } : {}),
      })),
    } : {}),
    ...(Array.isArray(value.media) ? {
      media: value.media.map(item => ({
        src: item.src.trim(),
        ...(item.kind ? { kind: String(item.kind).trim() } : {}),
        ...(item.type ? { type: String(item.type).trim() } : {}),
        ...(item.alt ? { alt: String(item.alt).trim() } : {}),
      })),
    } : {}),
  };
}

export function pageContentProjectionItems(value) {
  const pack = normalizePageContentPack(value);
  return pack.items.map((item, index) => projectionItem(item, index));
}

export function summarizePageChartData(value) {
  const pack = normalizePageContentPack(value);
  const points = pack.chartData || [];
  if (!points.length) return '';
  const ordered = [...points].sort((left, right) => left.value - right.value || left.label.localeCompare(right.label));
  return `${points.length}点｜${formatPageContentValue(ordered[0])}–${formatPageContentValue(ordered.at(-1))}`;
}

export function requiredPageContentFacts(value) {
  const pack = normalizePageContentPack(value);
  const facts = [pack.title.short, pack.coreMessage];
  for (const item of pageContentProjectionItems(pack)) {
    if (item.authoredRequired) facts.push(item.label);
    if (item.hasValue) facts.push(item.formattedValue);
  }
  return unique(facts.map(item => String(item || '').trim()).filter(Boolean));
}

export function requiredPageChartFacts(value) {
  const pack = normalizePageContentPack(value);
  return unique((pack.chartData || []).flatMap(item => [item.label, formatPageContentValue(item)]).filter(Boolean));
}

export function formatPageContentValue(item = {}) {
  const unit = isNonEmptyString(item.unit) ? item.unit.trim() : '';
  const raw = isNonEmptyString(item.displayValue)
    ? item.displayValue.trim()
    : isStringOrFiniteNumber(item.value)
      ? String(item.value).trim()
      : '';
  if (!raw || !unit) return raw;
  let normalized = raw;
  while (normalized.endsWith(`${unit}${unit}`)) normalized = normalized.slice(0, -unit.length);
  return normalized.endsWith(unit) ? normalized : `${normalized}${unit}`;
}

function projectionItem(item, sourceIndex) {
  const formattedValue = formatPageContentValue(item);
  return {
    id: item.id,
    label: item.label,
    detailFull: item.detail?.full || '',
    detailShort: item.detail?.short || '',
    ...(item.value !== undefined ? { value: item.value } : {}),
    ...(item.displayValue !== undefined ? { displayValue: item.displayValue } : {}),
    ...(item.unit !== undefined ? { unit: item.unit } : {}),
    formattedValue,
    hasValue: Boolean(formattedValue),
    authoredRequired: item.required === true,
    pinned: item.required === true || Boolean(formattedValue) || String(item.priority || '').toLowerCase() === 'critical',
    required: item.required === true,
    priority: item.priority || '',
    chartFact: false,
    sourceIndex,
  };
}

function validateTextPair(value, path, errors) {
  if (!isPlainRecord(value)) {
    errors.push(`${path}: expected {full,short}`);
    return;
  }
  for (const field of ['full', 'short']) {
    if (!isNonEmptyString(value[field])) errors.push(`${path}.${field}: expected a non-empty string`);
  }
}

function validateOptionalTextPair(value, path, errors) {
  if (value == null) return;
  if (!isPlainRecord(value)) {
    errors.push(`${path}: expected {full,short} when provided`);
    return;
  }
  for (const field of ['full', 'short']) {
    if (value[field] != null && typeof value[field] !== 'string') {
      errors.push(`${path}.${field}: expected a string when provided`);
    }
  }
}

function normalizeTextPair(value) {
  return { full: value.full.trim(), short: value.short.trim() };
}

function normalizeOptionalTextPair(value) {
  return {
    full: typeof value?.full === 'string' ? value.full.trim() : '',
    short: typeof value?.short === 'string' ? value.short.trim() : '',
  };
}

function sameFactIdentity(left, right) {
  return String(left?.label || '').trim() === String(right?.label || '').trim()
    && formatPageContentValue(left) === formatPageContentValue(right)
    && String(left?.unit || '').trim() === String(right?.unit || '').trim();
}

function validateFactValue(item, path, errors) {
  if (item.value !== undefined && !isStringOrFiniteNumber(item.value)) {
    errors.push(`${path}.value: expected a non-empty string or finite number`);
  }
  if (item.displayValue !== undefined && !isNonEmptyString(item.displayValue)) {
    errors.push(`${path}.displayValue: expected a non-empty string`);
  }
  if (item.unit !== undefined && !isNonEmptyString(item.unit)) {
    errors.push(`${path}.unit: expected a non-empty string`);
  }
  if (item.unit !== undefined && item.value === undefined && item.displayValue === undefined) {
    errors.push(`${path}.unit: unit requires value or displayValue`);
  }
}

export function validateBespokeComposition(composition) {
  const errors = [];
  scanForbiddenKeys(composition, 'composition', errors);
  if (!isPlainRecord(composition)) {
    errors.push('composition: expected an object');
    return unique(errors);
  }
  rejectUnknownFields(composition, new Set(['designIntent', 'background', 'elements']), 'composition', errors);
  validateDesignIntent(composition.designIntent, errors);

  if (!BACKGROUNDS.has(composition.background)) {
    errors.push(`composition.background: expected one of ${[...BACKGROUNDS].join(', ')}`);
  }
  if (!Array.isArray(composition.elements)) {
    errors.push('composition.elements: expected a non-empty array');
    return unique(errors);
  }
  if (composition.elements.length < 1) {
    errors.push('composition.elements: expected at least 1 element');
  }
  if (composition.elements.length > 32) {
    errors.push('composition.elements: expected at most 32 elements');
  }

  const ids = new Set();
  composition.elements.forEach((element, index) => {
    validateElement(element, index, ids, errors);
  });
  return unique(errors);
}

function validateDesignIntent(value, errors) {
  const path = 'composition.designIntent';
  if (!isPlainRecord(value)) {
    errors.push(`${path}: expected an object`);
    return;
  }
  rejectUnknownFields(value, new Set(DESIGN_INTENT_FIELDS), path, errors);
  for (const field of DESIGN_INTENT_FIELDS) {
    if (!isNonEmptyString(value[field])) {
      errors.push(`${path}.${field}: expected a non-empty string`);
    }
  }
}

function validateElement(element, index, ids, errors) {
  const path = `composition.elements[${index}]`;
  if (!isPlainRecord(element)) {
    errors.push(`${path}: expected an object`);
    return;
  }

  const id = isNonEmptyString(element.id) ? element.id.trim() : '';
  if (!id) {
    errors.push(`${path}.id: expected a non-empty string`);
  } else if (ids.has(id)) {
    errors.push(`${path}.id: duplicate element id "${id}"`);
  } else {
    ids.add(id);
  }

  const type = element.type;
  if (!ELEMENT_TYPES.has(type)) {
    errors.push(`${path}.type: expected one of ${[...ELEMENT_TYPES].join(', ')}`);
  }
  rejectUnknownFields(element, ELEMENT_FIELDS[type] || COMMON_ELEMENT_FIELDS, path, errors);
  validateGrid(element.grid, `${path}.grid`, errors);

  if (element.tone != null && !ELEMENT_TONES.has(element.tone)) {
    errors.push(`${path}.tone: expected one of ${[...ELEMENT_TONES].join(', ')}`);
  }

  if (type === 'text') validateTextElement(element, path, errors);
  if (type === 'metric') validateMetricElement(element, path, errors);
  if (type === 'list') validateListElement(element, path, errors);
  if (type === 'quote') validateQuoteElement(element, path, errors);
  if (type === 'media') validateMediaElement(element, path, errors);
  if (type === 'shape') validateShapeElement(element, path, errors);
  if (type === 'chart') validateChartElement(element, path, errors);
}

function validateGrid(grid, path, errors) {
  if (!isPlainRecord(grid)) {
    errors.push(`${path}: expected {column,row,width,height}`);
    return;
  }
  rejectUnknownFields(grid, new Set(GRID_FIELDS), path, errors);
  for (const field of GRID_FIELDS) {
    if (!Number.isInteger(grid[field])) {
      errors.push(`${path}.${field}: expected an integer`);
    }
  }
  if (!Number.isInteger(grid.column) || !Number.isInteger(grid.row)
    || !Number.isInteger(grid.width) || !Number.isInteger(grid.height)) return;

  if (grid.column < 1 || grid.column > 12) {
    errors.push(`${path}.column: expected an integer from 1 to 12`);
  }
  if (grid.row < 1 || grid.row > 8) {
    errors.push(`${path}.row: expected an integer from 1 to 8`);
  }
  if (grid.width < 1 || grid.width > 12) {
    errors.push(`${path}.width: expected an integer from 1 to 12`);
  }
  if (grid.height < 1 || grid.height > 8) {
    errors.push(`${path}.height: expected an integer from 1 to 8`);
  }
  if (grid.column >= 1 && grid.width >= 1 && grid.column + grid.width - 1 > 12) {
    errors.push(`${path}: exceeds 12-column grid`);
  }
  if (grid.row >= 1 && grid.height >= 1 && grid.row + grid.height - 1 > 8) {
    errors.push(`${path}: exceeds 8-row grid`);
  }
}

function validateTextElement(element, path, errors) {
  if (!isNonEmptyString(element.text)) errors.push(`${path}.text: expected a non-empty string`);
  if (element.role != null && !TEXT_ROLES.has(element.role)) {
    errors.push(`${path}.role: expected one of ${[...TEXT_ROLES].join(', ')}`);
  }
  if (element.align != null && !TEXT_ALIGNS.has(element.align)) {
    errors.push(`${path}.align: expected one of ${[...TEXT_ALIGNS].join(', ')}`);
  }
}

function validateMetricElement(element, path, errors) {
  validateOptionalString(element.sourceId, `${path}.sourceId`, errors);
  if (!isStringOrFiniteNumber(element.value)) {
    errors.push(`${path}.value: expected a non-empty string or finite number`);
  }
  if (!isNonEmptyString(element.label)) errors.push(`${path}.label: expected a non-empty string`);
  validateOptionalString(element.detail, `${path}.detail`, errors);
  validateOptionalString(element.trend, `${path}.trend`, errors);
}

function validateListElement(element, path, errors) {
  if (element.ordered != null && typeof element.ordered !== 'boolean') {
    errors.push(`${path}.ordered: expected a boolean`);
  }
  if (!Array.isArray(element.items) || !element.items.length) {
    errors.push(`${path}.items: expected a non-empty array`);
    return;
  }
  if (element.items.length > BESPOKE_LIST_ITEM_LIMIT) {
    errors.push(`${path}.items: expected at most ${BESPOKE_LIST_ITEM_LIMIT} items`);
  }
  element.items.forEach((item, index) => {
    const itemPath = `${path}.items[${index}]`;
    if (isNonEmptyString(item)) return;
    if (!isPlainRecord(item)) {
      errors.push(`${itemPath}: expected a non-empty string or {title,body}`);
      return;
    }
    rejectUnknownFields(item, new Set(['sourceId', 'title', 'body']), itemPath, errors);
    validateOptionalString(item.sourceId, `${itemPath}.sourceId`, errors);
    if (!isNonEmptyString(item.title) && !isNonEmptyString(item.body)) {
      errors.push(`${itemPath}: expected a non-empty title or body`);
    }
    validateOptionalString(item.title, `${itemPath}.title`, errors);
    validateOptionalString(item.body, `${itemPath}.body`, errors);
  });
}

function validateQuoteElement(element, path, errors) {
  if (!isNonEmptyString(element.quote)) errors.push(`${path}.quote: expected a non-empty string`);
  validateOptionalString(element.attribution, `${path}.attribution`, errors);
}

function validateMediaElement(element, path, errors) {
  if (!isNonEmptyString(element.src)) errors.push(`${path}.src: expected a non-empty string`);
  validateOptionalString(element.alt, `${path}.alt`, errors);
  if (element.fit != null && !MEDIA_FITS.has(element.fit)) {
    errors.push(`${path}.fit: expected one of ${[...MEDIA_FITS].join(', ')}`);
  }
}

function validateShapeElement(element, path, errors) {
  if (!SHAPES.has(element.shape)) {
    errors.push(`${path}.shape: expected one of ${[...SHAPES].join(', ')}`);
  }
}

function validateChartElement(element, path, errors) {
  if (!CHART_TYPES.has(element.chartType)) {
    errors.push(`${path}.chartType: expected one of ${[...CHART_TYPES].join(', ')}`);
  }
  if (element.showValues != null && typeof element.showValues !== 'boolean') {
    errors.push(`${path}.showValues: expected a boolean`);
  }
  if (!Array.isArray(element.data) || !element.data.length) {
    errors.push(`${path}.data: expected a non-empty array`);
    return;
  }
  if (element.data.length > BESPOKE_CHART_POINT_LIMIT) {
    errors.push(`${path}.data: expected at most ${BESPOKE_CHART_POINT_LIMIT} points`);
  }
  const units = new Set();
  element.data.forEach((item, index) => {
    const itemPath = `${path}.data[${index}]`;
    if (!isPlainRecord(item)) {
      errors.push(`${itemPath}: expected {sourceId,label,value,displayValue,unit}`);
      return;
    }
    rejectUnknownFields(item, new Set(['sourceId', 'label', 'value', 'displayValue', 'unit']), itemPath, errors);
    validateOptionalString(item.sourceId, `${itemPath}.sourceId`, errors);
    if (!isNonEmptyString(item.label)) errors.push(`${itemPath}.label: expected a non-empty string`);
    if (typeof item.value !== 'number' || !Number.isFinite(item.value)) {
      errors.push(`${itemPath}.value: expected a finite number`);
    } else if (['donut', 'progress'].includes(element.chartType) && item.value < 0) {
      errors.push(`${itemPath}.value: ${element.chartType} charts require non-negative values`);
    }
    validateOptionalString(item.displayValue, `${itemPath}.displayValue`, errors);
    validateOptionalString(item.unit, `${itemPath}.unit`, errors);
    units.add(typeof item.unit === 'string' ? item.unit.normalize('NFKC').trim() : '');
  });
  if (units.size > 1) errors.push(`${path}.data: all chart units must match or all be empty`);
}

function validateOptionalString(value, path, errors) {
  if (value != null && !isNonEmptyString(value)) errors.push(`${path}: expected a non-empty string`);
}

function parseMappedPath(value, label, errors) {
  try {
    return parsePath(value);
  } catch (error) {
    errors.push(`${label}: ${error.message}`);
    return null;
  }
}

function parsePath(value) {
  const path = String(value || '').trim();
  if (!PATH_PATTERN.test(path)) {
    throw new Error(`invalid path "${path}" (use dot paths and numeric [n] indices)`);
  }
  const tokens = [];
  for (const match of path.matchAll(PATH_TOKEN_PATTERN)) {
    const token = match[1] ?? Number(match[2]);
    if (typeof token === 'string' && UNSAFE_KEYS.has(token)) {
      throw new Error(`unsafe path segment "${token}"`);
    }
    if (typeof token === 'number' && (!Number.isSafeInteger(token) || token > MAX_PATH_INDEX)) {
      throw new Error(`array index ${match[2]} is outside the supported range`);
    }
    tokens.push(token);
  }
  return tokens;
}

function readPath(value, tokens) {
  let current = value;
  for (const token of tokens) {
    if (typeof token === 'number') {
      if (!Array.isArray(current) || !Object.prototype.hasOwnProperty.call(current, token)) {
        return { found: false, value: undefined };
      }
    } else if (!isPlainRecord(current) || !Object.prototype.hasOwnProperty.call(current, token)) {
      return { found: false, value: undefined };
    }
    current = current[token];
  }
  return { found: true, value: current };
}

function writePath(target, tokens, value, targetPath) {
  let current = target;
  for (let index = 0; index < tokens.length - 1; index += 1) {
    const token = tokens[index];
    const nextToken = tokens[index + 1];
    assertWritableContainer(current, token, targetPath);
    if (!Object.prototype.hasOwnProperty.call(current, token) || current[token] == null) {
      current[token] = typeof nextToken === 'number' ? [] : {};
    }
    const expectedArray = typeof nextToken === 'number';
    if ((expectedArray && !Array.isArray(current[token]))
      || (!expectedArray && !isPlainRecord(current[token]))) {
      throw new Error(`contentMap target "${targetPath}": cannot traverse non-container segment "${String(token)}"`);
    }
    current = current[token];
  }
  const last = tokens.at(-1);
  assertWritableContainer(current, last, targetPath);
  current[last] = value;
}

function assertWritableContainer(container, token, targetPath) {
  if (typeof token === 'number') {
    if (!Array.isArray(container)) {
      throw new Error(`contentMap target "${targetPath}": array index [${token}] requires an array`);
    }
    return;
  }
  if (!isPlainRecord(container)) {
    throw new Error(`contentMap target "${targetPath}": property "${token}" requires an object`);
  }
}

function safeDeepClone(value, path, active = new WeakSet()) {
  if (value == null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) throw new Error(`${path}: expected a finite number`);
    return value;
  }
  if (typeof value !== 'object') {
    throw new Error(`${path}: expected JSON-compatible content`);
  }
  if (active.has(value)) throw new Error(`${path}: circular values are not supported`);
  active.add(value);
  try {
    if (Array.isArray(value)) {
      for (const key of Object.keys(value)) {
        if (UNSAFE_KEYS.has(key)) throw new Error(`${path}: unsafe object key "${key}"`);
        if (!/^(?:0|[1-9]\d*)$/.test(key)) {
          throw new Error(`${path}: array contains unsupported property "${key}"`);
        }
      }
      return value.map((item, index) => safeDeepClone(item, `${path}[${index}]`, active));
    }
    if (!isPlainRecord(value)) throw new Error(`${path}: expected a plain object`);
    const clone = {};
    for (const [key, item] of Object.entries(value)) {
      if (UNSAFE_KEYS.has(key)) throw new Error(`${path}: unsafe object key "${key}"`);
      clone[key] = safeDeepClone(item, `${path}.${key}`, active);
    }
    return clone;
  } finally {
    active.delete(value);
  }
}

function scanForbiddenKeys(value, path, errors, active = new WeakSet()) {
  if (!value || typeof value !== 'object' || active.has(value)) return;
  active.add(value);
  for (const [key, item] of Object.entries(value)) {
    const itemPath = Array.isArray(value) ? `${path}[${key}]` : `${path}.${key}`;
    if (UNSAFE_KEYS.has(key)) errors.push(`${itemPath}: unsafe object key`);
    if (FORBIDDEN_COMPOSITION_KEYS.has(key.toLowerCase())) {
      errors.push(`${itemPath}: forbidden composition field`);
    }
    scanForbiddenKeys(item, itemPath, errors, active);
  }
  active.delete(value);
}

function rejectUnknownFields(value, allowed, path, errors) {
  for (const key of Object.keys(value || {})) {
    if (!allowed.has(key)) errors.push(`${path}.${key}: unknown field`);
  }
}

function isPlainRecord(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

function isStringOrFiniteNumber(value) {
  return isNonEmptyString(value) || (typeof value === 'number' && Number.isFinite(value));
}

function unique(values) {
  return [...new Set(values)];
}
