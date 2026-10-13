/**
 * 측정 스냅샷·anchor·좌표 변환(CONTRACTS C7).
 */

function px(value) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

/**
 * node의 root 기준 layout rect(getBoundingClientRect 차이). transform은 측정 전에 없어야 한다.
 * @param {Element} node
 * @param {Element} root
 * @returns {import('./types.js').Rect}
 */
export function defaultMeasure(node, root) {
  if (!node?.getBoundingClientRect || !root?.getBoundingClientRect)
    throw new TypeError('defaultMeasure expects Elements');
  const transformed = [];
  for (let current = node; current; current = current.parentElement) {
    transformed.push([current.style, current.style.transform]);
    current.style.transform = 'none';
    if (current === root) break;
  }
  try {
    const box = node.getBoundingClientRect();
    const base = root.getBoundingClientRect();
    return { x: box.left - base.left, y: box.top - base.top, w: box.width, h: box.height };
  } finally {
    for (const [style, transform] of transformed) style.transform = transform;
  }
}

/** rectIn = defaultMeasure 별칭(J조 dom.js 이름 계승) */
export function rectIn(node, root) {
  return defaultMeasure(node, root);
}

/**
 * 모든 beat의 모든 part 요소 rect 스냅샷. build ②에서 1회.
 * @param {Element} root
 * @param {Array<{ root: Element, parts: Record<string, Element[]> }>} beats
 * @param {(node: Element, root: Element) => import('./types.js').Rect} [measureFn]
 * @returns {import('./types.js').MeasureSnapshot}
 */
export function measure(root, beats, measureFn = defaultMeasure) {
  const snapshot = new Map();
  for (const beat of beats)
    for (const nodes of Object.values(beat.parts ?? {}))
      for (const node of nodes) {
        if (!snapshot.has(node)) snapshot.set(node, { ...measureFn(node, root) });
      }
  return snapshot;
}

/**
 * @param {{ id: string, parts: Record<string, Element[]> }} beat
 * @param {string} part  비면 primary
 * @param {import('./types.js').MeasureSnapshot} snapshot
 * @param {string} [primary]
 * @param {number} [index]
 * @returns {import('./types.js').Handoff}
 */
export function anchorOf(beat, part, snapshot, primary, index = 0) {
  const name = part || primary || beat.primary || Object.keys(beat.parts ?? {})[0];
  const nodes = beat.parts?.[name] ?? [];
  const normalized = index < 0 ? nodes.length + index : index;
  const node = nodes[normalized];
  if (!name || !node) throw new Error(`Beat "${beat.id}" has no ${name ?? ''}[${normalized}]`);
  const rect = snapshot.get(node);
  if (!rect) throw new Error(`Anchor "${beat.id}.${name}" was not measured`);
  const computed = globalThis.getComputedStyle?.(node);
  return {
    beat: beat.id,
    part: name,
    index: normalized,
    kind: node.getAttribute?.('data-handoff-kind') === 'point' ? 'point' : 'rect',
    rect: { ...rect },
    point: { x: rect.x + rect.w / 2, y: rect.y + rect.h / 2 },
    node,
    style: {
      color: computed?.color ?? '',
      radius: px(computed?.borderRadius),
      fontSize: px(computed?.fontSize),
    },
  };
}

/**
 * clip-path inset 문자열: `inset(${y}px ${W-x-w}px ${H-y-h}px ${x}px)`
 * @param {import('./types.js').Rect} rect
 * @param {{ w: number, h: number }} viewport
 * @returns {string}
 */
export function toInset(rect, viewport) {
  return `inset(${rect.y}px ${viewport.w - rect.x - rect.w}px ${viewport.h - rect.y - rect.h}px ${rect.x}px)`;
}

/**
 * from 요소를 to 자리로 보내는 GSAP vars: { x, y, scaleX, scaleY, transformOrigin: '0 0' }
 * @param {import('./types.js').Rect} fromRect
 * @param {import('./types.js').Rect} toRect
 * @returns {{ x: number, y: number, scaleX: number, scaleY: number, transformOrigin: string }}
 */
export function transferVars(fromRect, toRect) {
  return {
    x: toRect.x - fromRect.x,
    y: toRect.y - fromRect.y,
    scaleX: fromRect.w === 0 ? 1 : toRect.w / fromRect.w,
    scaleY: fromRect.h === 0 ? 1 : toRect.h / fromRect.h,
    transformOrigin: '0 0',
  };
}
