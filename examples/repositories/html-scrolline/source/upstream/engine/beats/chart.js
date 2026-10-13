/**
 * beat 'chart'(CONTRACTS C4). parts: plot, axis, mark, label, legend, source, title, dek, note, baseline.
 * 렌더 = 정지점 완성 상태 DOM. 움직임 0. 루트 <section class="sl-beat sl-beat--chart" data-beat="<id>">는 build가 id를 채운다.
 */

import { BASE_STATE } from '../constants.js';
import { add, node, root } from './helpers.js';

const BOX = Object.freeze({ left: 160, right: 1460, top: 160, bottom: 760 });

function sourceLabel(rc, source) {
  const ids = Array.isArray(source) ? source : [source];
  return ids
    .filter(Boolean)
    .map((id) => rc.sources?.[id]?.short ?? rc.sources?.[id]?.title ?? id)
    .join(' · ');
}

function valueRange(series, domain = {}) {
  // domain(v2.2)은 값 영역을 넓히기만 한다: [min(domain.min, 최소값, 0), max(domain.max, 최대값, 0)].
  const values = series.flatMap((item) => item.values);
  const min = Math.min(0, ...values, domain.min ?? 0);
  const rawMax = Math.max(0, ...values, domain.max ?? 0);
  return rawMax === min ? { min: 0, max: 1 } : { min, max: rawMax };
}

function stateLayers(data) {
  const layers = [{ name: BASE_STATE, title: data.title, dek: data.dek, notes: data.notes, unit: data.unit }];
  for (const state of data.states ?? []) {
    const previous = layers.at(-1);
    layers.push({
      name: state.name,
      title: state.title ?? previous.title,
      dek: state.dek ?? previous.dek,
      notes: state.notes ?? previous.notes,
      unit: state.unit ?? previous.unit,
    });
  }
  return layers;
}

function setState(element, name) {
  element.dataset.state = name;
  if (name !== BASE_STATE) {
    element.style.visibility = 'hidden';
    element.style.opacity = '0';
  }
}

function seriesIndex(series, value) {
  if (typeof value === 'number') return value;
  return series.findIndex((item) => item.name === value);
}

function notePosition(point) {
  const left = Math.min(98, Math.max(0, (point.x / 1600) * 100 + 1));
  const top = Math.min(98, Math.max(0, (point.y / 900) * 100 - 2));
  return { left: `${left}%`, top: `${top}%` };
}

/** @type {import('../types.js').BeatTypeDef} */
export default {
  type: 'chart',
  primary: 'plot',
  fields: {
    kind: { type: 'enum', values: ['bar', 'line', 'area', 'dot'], required: true, doc: '차트 종류' },
    categories: { type: 'array', of: { type: 'string', doc: '범주' }, required: true, doc: 'x축 범주' },
    series: {
      type: 'array',
      required: true,
      doc: '계열',
      of: {
        type: 'object',
        doc: '계열 1개',
        fields: {
          name: { type: 'string', required: true, doc: '계열 이름' },
          values: {
            type: 'array',
            required: true,
            of: { type: 'number', doc: '값' },
            doc: 'categories와 같은 길이',
          },
        },
      },
    },
    unit: { type: 'string', doc: '값 단위' },
    title: { type: 'string', doc: '결론(L1)' },
    dek: { type: 'string', doc: '보충(L2)' },
    notes: {
      type: 'array',
      doc: '표식 주석',
      of: {
        type: 'object',
        fields: {
          index: { type: 'integer', required: true, doc: '범주 index' },
          series: { type: 'any', doc: '계열 index 또는 이름' },
          text: { type: 'string', required: true, doc: '주석' },
        },
      },
    },
    orient: { type: 'enum', values: ['v', 'h'], default: 'v', doc: 'bar 방향' },
    domain: {
      type: 'object',
      fields: {
        min: { type: 'number', doc: '값 영역 최소(데이터보다 작을 때만 넓힘)' },
        max: { type: 'number', doc: '값 영역 최대(데이터보다 클 때만 넓힘)' },
      },
      doc: '값 영역 고정(전후 비교 차트가 같은 눈금을 쓰게)',
    },
    highlight: {
      type: 'object',
      fields: {
        series: { type: 'string', doc: '강조 계열' },
        index: { type: 'integer', doc: '강조 범주 index' },
      },
      doc: '강조',
    },
    states: {
      type: 'array',
      doc: 'steps에서 바뀌는 상태',
      of: {
        type: 'object',
        doc: '상태',
        fields: {
          name: { type: 'string', required: true, doc: '상태 이름(step name과 대응)' },
          kind: { type: 'enum', values: ['bar', 'line', 'area', 'dot'], doc: '바뀐 종류' },
          series: { type: 'any', doc: '바뀐 계열' },
          title: { type: 'string', doc: '상태 결론' },
          dek: { type: 'string', doc: '상태 보충' },
          notes: { type: 'any', doc: '상태 주석' },
          unit: { type: 'string', doc: '상태 단위' },
        },
      },
    },
    source: { type: 'any', doc: '출처 id 또는 id 배열' },
  },
  render(data, rc) {
    const parts = {};
    const view = root('chart', rc);
    const range = valueRange(data.series, data.domain);
    const horizontal = data.kind === 'bar' && data.orient === 'h';
    const categoryCount = data.categories.length;
    const categorySpace = horizontal
      ? (BOX.bottom - BOX.top) / Math.max(1, categoryCount)
      : (BOX.right - BOX.left) / Math.max(1, categoryCount - 1);
    const pointByKey = new Map();
    const valueToX = (value) =>
      BOX.left + ((value - range.min) / (range.max - range.min)) * (BOX.right - BOX.left);
    const valueToY = (value) =>
      BOX.bottom - ((value - range.min) / (range.max - range.min)) * (BOX.bottom - BOX.top);
    const baseline = horizontal ? valueToX(0) : valueToY(0);

    for (const layer of stateLayers(data)) {
      if (layer.title != null) {
        const title = add(parts, 'title', node(rc, 'h2', 'sl-chart__title', view, layer.title));
        setState(title, layer.name);
      }
      if (layer.dek != null) {
        const dek = add(parts, 'dek', node(rc, 'p', 'sl-chart__dek', view, layer.dek));
        setState(dek, layer.name);
      }
      if (layer.unit != null) {
        const unit = add(parts, 'unit', node(rc, 'small', 'sl-chart__unit', view, layer.unit));
        setState(unit, layer.name);
      }
    }

    const svg = add(parts, 'plot', node(rc, 'svg', 'sl-chart', view));
    svg.setAttribute('viewBox', '0 0 1600 900');
    // move가 같은 눈금으로 값→좌표를 환산하도록 실제 값 영역을 내보낸다.
    svg.dataset.min = String(range.min);
    svg.dataset.max = String(range.max);
    svg.setAttribute('role', 'img');
    const axis = add(parts, 'axis', node(rc, 'g', 'sl-chart__axis', svg));
    const axisLine = node(rc, 'line', null, axis);
    axisLine.setAttribute('x1', String(BOX.left));
    axisLine.setAttribute('x2', String(horizontal ? BOX.left : BOX.right));
    axisLine.setAttribute('y1', String(BOX.bottom));
    axisLine.setAttribute('y2', String(horizontal ? BOX.top : BOX.bottom));

    if (range.min < 0) {
      const line = add(parts, 'baseline', node(rc, 'line', 'sl-chart__baseline', svg));
      line.setAttribute('x1', String(horizontal ? baseline : BOX.left));
      line.setAttribute('x2', String(horizontal ? baseline : BOX.right));
      line.setAttribute('y1', String(horizontal ? BOX.top : baseline));
      line.setAttribute('y2', String(horizontal ? BOX.bottom : baseline));
    }

    data.categories.forEach((category, index) => {
      const label = add(parts, 'label', node(rc, 'text', 'sl-chart__label', svg, category));
      if (horizontal) {
        label.setAttribute('x', '20');
        label.setAttribute('y', String(BOX.top + categorySpace * (index + 0.5)));
      } else {
        label.setAttribute('x', String(BOX.left + index * categorySpace));
        label.setAttribute('y', '820');
      }
    });

    data.series.forEach((series, si) => {
      add(parts, 'legend', node(rc, 'span', 'sl-chart__legend', view, series.name));
      const points = series.values.map((value, index) => ({
        x: horizontal ? valueToX(value) : BOX.left + index * categorySpace,
        y: horizontal ? BOX.top + categorySpace * (index + 0.5) : valueToY(value),
        value,
      }));
      if (!horizontal && (data.kind === 'line' || data.kind === 'area')) {
        const path = add(parts, 'mark', node(rc, 'path', `sl-chart__mark sl-chart__mark--${data.kind}`, svg));
        path.setAttribute(
          'd',
          `M ${points.map((point) => `${point.x} ${point.y}`).join(' L ')}` +
            (data.kind === 'area' ? ` L ${BOX.right} ${BOX.bottom} L ${BOX.left} ${BOX.bottom} Z` : ''),
        );
        path.dataset.series = String(si);
        path.dataset.index = 'all';
        path.dataset.sign = points.every((point) => point.value < 0) ? 'neg' : 'pos';
      }
      points.forEach((point, index) => {
        const mark = add(
          parts,
          'mark',
          node(
            rc,
            data.kind === 'bar' ? 'rect' : 'circle',
            `sl-chart__mark sl-chart__mark--${data.kind}`,
            svg,
          ),
        );
        mark.dataset.series = String(si);
        mark.dataset.index = String(index);
        mark.dataset.sign = point.value < 0 ? 'neg' : 'pos';
        pointByKey.set(`${si}/${index}`, point);
        if (data.kind === 'bar') {
          if (horizontal) {
            const y = BOX.top + categorySpace * index + si * 50 + 8;
            mark.setAttribute('x', String(Math.min(baseline, point.x)));
            mark.setAttribute('y', String(y));
            mark.setAttribute('width', String(Math.abs(point.x - baseline)));
            mark.setAttribute('height', '44');
          } else {
            const x = point.x - 24 + si * 50;
            mark.setAttribute('x', String(x));
            mark.setAttribute('y', String(Math.min(baseline, point.y)));
            mark.setAttribute('width', '44');
            mark.setAttribute('height', String(Math.abs(baseline - point.y)));
          }
        } else {
          mark.setAttribute('cx', String(point.x));
          mark.setAttribute('cy', String(point.y));
          mark.setAttribute('r', '11');
        }
      });
    });

    for (const layer of stateLayers(data)) {
      for (const noteData of layer.notes ?? []) {
        const si = seriesIndex(data.series, noteData.series ?? 0);
        const point = pointByKey.get(`${si}/${noteData.index}`);
        if (!point) continue;
        const note = add(parts, 'note', node(rc, 'p', 'sl-chart__note', view, noteData.text));
        note.dataset.index = String(noteData.index);
        note.dataset.series = String(si);
        Object.assign(note.style, notePosition(point));
        setState(note, layer.name);
      }
    }
    if (data.source)
      add(parts, 'source', node(rc, 'small', 'sl-chart__source', view, sourceLabel(rc, data.source)));
    return { root: view, parts };
  },
};
