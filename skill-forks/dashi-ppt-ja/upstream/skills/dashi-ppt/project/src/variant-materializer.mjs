import {
  formatPageContentValue,
  pageContentProjectionItems,
  summarizePageChartData,
} from './variant-contract.mjs';

export function materializeTemplateVariantProps(presentation, structure = {}) {
  if (!presentation) throw new Error('Template source content is missing.');
  const props = {};
  const sources = projectionSources(presentation);
  const valueEntries = structure.values || [];
  for (const entry of valueEntries) {
    const source = entry.sourceId ? sources.get(entry.sourceId) : null;
    if (entry.sourceId && !source) throw new Error(`Template projection source "${entry.sourceId}" is missing.`);
    writeProjectionPath(props, entry.path, entry.sourceId
      ? projectionValue(source, entry.semantic, scalarBindingFields(valueEntries, entry), true)
      : cloneValue(entry.value));
  }
  for (const group of structure.arrays || []) {
    const values = (group.items || []).map((entry) => {
      const source = sources.get(entry.sourceId);
      if (!source) throw new Error(`Template projection source "${entry.sourceId}" is missing.`);
      return materializeProjectionItem(group.fields || [], source, entry.structure);
    });
    writeProjectionPath(props, group.path, values);
    if (group.countPath) writeProjectionPath(props, group.countPath, values.length);
  }
  if (structure.media) {
    const media = (presentation.media || []).map(item => ({
      src: item.src,
      ...(item.kind ? { kind: item.kind } : {}),
      ...(item.type ? { type: item.type } : {}),
    }));
    writeProjectionPath(props, structure.media.path, media);
    if (structure.media.countPath) writeProjectionPath(props, structure.media.countPath, media.length);
  }
  return props;
}

function scalarBindingFields(entries, entry) {
  const parent = projectionPathParent(entry.path);
  return entries
    .filter(candidate => candidate.sourceId === entry.sourceId && projectionPathParent(candidate.path) === parent)
    .map(candidate => ({ semantic: candidate.semantic }));
}

function projectionPathParent(pathName) {
  const value = String(pathName || '');
  const separator = value.lastIndexOf('.');
  return separator < 0 ? '' : value.slice(0, separator);
}

export function materializeBespokeComposition(composition, presentation, projection = {}) {
  const materialized = cloneValue(composition || {});
  const hasBindings = ['itemBindings', 'chartBindings', 'mediaBindings']
    .some(key => Array.isArray(projection?.[key]) && projection[key].length);
  if (!hasBindings) return materialized;
  if (!presentation) throw new Error('Bespoke source content is missing.');
  const items = new Map(pageContentProjectionItems(presentation).map(item => [item.id, item]));
  const chart = new Map((presentation.chartData || []).map(item => [item.id, item]));
  for (const binding of projection.itemBindings || []) {
    const source = items.get(binding.id);
    const value = binding.target.includes('.items[')
      ? { sourceId: source?.id, title: source?.label, body: [source?.detailShort || source?.detailFull, source?.formattedValue].filter(Boolean).join(' · ') }
      : { sourceId: source?.id, label: source?.label, value: source?.formattedValue, ...(source?.detailShort || source?.detailFull ? { detail: source.detailShort || source.detailFull } : {}) };
    if (!source || !writeBespokeBinding(materialized, binding.target, value)) throw new Error(`Bespoke item binding "${binding.id}" is invalid.`);
  }
  for (const binding of projection.chartBindings || []) {
    const source = chart.get(binding.sourceIds?.[0]);
    const value = binding.mode === 'point'
      ? { sourceId: source?.id, label: source?.label, value: source?.value, ...(source?.displayValue !== undefined ? { displayValue: source.displayValue } : {}), ...(source?.unit !== undefined ? { unit: source.unit } : {}) }
      : binding.target.includes('.items[')
        ? { sourceId: source?.id, title: source?.label, body: formatPageContentValue(source) }
        : { sourceId: source?.id, label: source?.label, value: formatPageContentValue(source) };
    if (!source || !writeBespokeBinding(materialized, binding.target, value)) throw new Error(`Bespoke chart binding "${binding.sourceIds?.[0] || ''}" is invalid.`);
  }
  for (const binding of projection.mediaBindings || []) {
    const source = presentation.media?.[binding.sourceIndex];
    if (!source || !writeBespokeBinding(materialized, binding.target, { src: source.src, alt: source.alt || presentation.title.short })) {
      throw new Error(`Bespoke media binding "${binding.sourceIndex}" is invalid.`);
    }
  }
  return materialized;
}

function projectionSources(presentation) {
  const sources = new Map(pageContentProjectionItems(presentation).map(item => [item.id, item]));
  const add = (id, value) => { if (!sources.has(id)) sources.set(id, { id, ...value }); };
  const points = presentation.chartData || [];
  points.forEach((item) => {
    const value = {
      label: item.label,
      value: item.value,
      ...(item.displayValue !== undefined ? { displayValue: item.displayValue } : {}),
      ...(item.unit !== undefined ? { unit: item.unit } : {}),
      formattedValue: formatPageContentValue(item),
      hasValue: true,
    };
    add(item.id, value);
    add(`chart:${item.id}`, value);
  });
  if (points.length) {
    add('chart-summary', { label: summarizePageChartData(presentation), formattedValue: '', hasValue: false });
    add('chart-first', { label: `首值｜${points[0].label}${formatPageContentValue(points[0])}`, formattedValue: '', hasValue: false });
    add('chart-last', { label: `末值｜${points.at(-1).label}${formatPageContentValue(points.at(-1))}`, formattedValue: '', hasValue: false });
  }
  add('support:summary-short', { label: presentation.summary.short, formattedValue: '', hasValue: false });
  add('support:core', { label: presentation.coreMessage, formattedValue: '', hasValue: false });
  add('support:title-short', { label: presentation.title.short, formattedValue: '', hasValue: false });
  add('support:summary', { label: presentation.summary.short, detailFull: presentation.summary.full, formattedValue: '', hasValue: false });
  if (presentation.title.full !== presentation.title.short) add('support:title', { label: presentation.title.full, formattedValue: '', hasValue: false });
  return sources;
}

function materializeProjectionItem(fields, item, structure = {}) {
  if (fields.length === 1 && fields[0].key == null) return projectionValue(item, 'label', fields);
  if (fields.length && fields.every(field => typeof field.key === 'number')) {
    return fields.map(field => projectionValue(item, field.semantic, fields));
  }
  return {
    ...cloneValue(structure),
    ...Object.fromEntries(fields.map(field => [field.key, projectionValue(item, field.semantic, fields)])),
  };
}

function projectionValue(item, semantic, fields = [], exact = false) {
  if (semantic === 'formattedValue') return item.formattedValue || '';
  const hasValue = fields.some(field => ['value', 'displayValue'].includes(field.semantic));
  const hasUnit = fields.some(field => field.semantic === 'unit');
  const hasDetail = fields.some(field => field.semantic === 'detail');
  if (semantic === 'label') {
    if (exact) return item.label || '';
    return [
      item.label,
      !hasDetail ? item.detailShort || item.detailFull : '',
      item.hasValue && (!hasValue || (item.unit && !hasUnit)) ? item.formattedValue : '',
    ].filter(Boolean).join(' · ');
  }
  if (semantic === 'detail') return exact
    ? item.detailShort || item.detailFull || ''
    : item.detailShort || item.detailFull || (!hasValue ? item.formattedValue : '') || '';
  if (semantic === 'unit') return item.unit || '';
  if (semantic === 'value') return item.value;
  if (semantic !== 'displayValue' || !item.hasValue) return '';
  if (!hasUnit) return item.formattedValue;
  let display = item.displayValue !== undefined ? String(item.displayValue) : String(item.value ?? '');
  if (item.unit) while (display.endsWith(item.unit)) display = display.slice(0, -item.unit.length).trimEnd();
  return display;
}

function writeBespokeBinding(composition, target, value) {
  const match = /^elements\[(\d+)\](?:\.(items|data)\[(\d+)\])?$/.exec(String(target || ''));
  const element = match ? composition?.elements?.[Number(match[1])] : null;
  if (!element) return false;
  if (!match[2]) Object.assign(element, value);
  else (element[match[2]] ||= [])[Number(match[3])] = value;
  return true;
}

function writeProjectionPath(target, pathName, value) {
  const parts = [];
  String(pathName || '').replace(/([A-Za-z_$][A-Za-z0-9_$-]*)|\[(\d+)\]/g, (_, name, index) => {
    parts.push(name ?? Number(index));
    return '';
  });
  if (!parts.length) throw new Error(`Invalid projection path "${pathName}".`);
  let cursor = target;
  parts.forEach((part, index) => {
    if (index === parts.length - 1) cursor[part] = value;
    else cursor = cursor[part] ||= typeof parts[index + 1] === 'number' ? [] : {};
  });
}

function cloneValue(value) {
  if (Array.isArray(value)) return value.map(cloneValue);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, cloneValue(item)]));
  return value;
}
