/** Move contract checker used from tests without importing Vitest. */
import { createRegistry, resolveParams } from '../../engine/index.js';
import { carriedRect } from './link.js';
const snapshot = (h, nodes) =>
  nodes.map((node) => ({
    props: ['x', 'y', 'scaleX', 'scaleY', 'opacity'].map((p) => h.run?.ctx?.gsap?.getProperty(node, p)),
    style: node.getAttribute('style') ?? '',
    text: node.textContent,
  }));
export function checkMove(move, scenario, createHarness) {
  const failures = [];
  let h;
  try {
    createRegistry([move]);
  } catch (error) {
    failures.push(`registry: ${error.message}`);
    return failures;
  }
  const make = (reduce = false) => {
    const value = createHarness({
      beats: scenario.beats,
      rects: scenario.rects,
      viewport: scenario.viewport,
      concept: scenario.concept,
      reduce,
    });
    scenario.prepare?.(value);
    return value;
  };
  try {
    h = make();
    // timing·handoff는 build와 같은 값(테스트 params + schema 기본값)으로 본다(C5 1·2번).
    const params = resolveParams(move.params, scenario.run.params ?? {});
    const data =
      scenario.run.role === 'link'
        ? { from: h.beats.get(scenario.run.from).data, to: h.beats.get(scenario.run.beat).data }
        : h.beats.get(scenario.run.beat).data;
    const one = move.timing(params, data),
      two = move.timing(params, data);
    if (JSON.stringify(one) !== JSON.stringify(two)) failures.push('timing is not pure');
    if (move.role !== 'ambient' && !(one.duration > 0)) failures.push('timing duration must be positive');
    if (move.role !== 'ambient' && one.duration === 'fill') failures.push('fill is ambient only');
    if (move.handoff && scenario.run.role === 'link') {
      const a = move.handoff(params, data),
        b = move.handoff(params, data);
      if (JSON.stringify(a) !== JSON.stringify(b)) failures.push('handoff is not pure');
    }
    const result = h.runMove(move, scenario.run);
    if (result.tl.duration() > result.timing.duration + 0.001)
      failures.push('timeline exceeds timing duration');
    const nodes =
      scenario.nodes?.(h, result.ctx) ??
      [...h.beats.values()]
        .flatMap((beat) => Object.values(beat.parts).flat())
        .concat([...result.ctx.overlay.querySelectorAll('*')]);
    const snap = () =>
      nodes.map((node) => ({
        props: ['x', 'y', 'scaleX', 'scaleY', 'opacity'].map((p) => result.ctx.gsap.getProperty(node, p)),
        style: node.getAttribute('style') ?? '',
        text: node.textContent,
      }));
    const d = result.timing.duration;
    h.seek(0.37 * d);
    const a = snap();
    h.seek(0.81 * d);
    h.seek(0.37 * d);
    if (JSON.stringify(a) !== JSON.stringify(snap())) failures.push('seek is not deterministic');
    h.seek(0);
    const zero = snap();
    h.seek(d);
    h.seek(0);
    if (JSON.stringify(zero) !== JSON.stringify(snap()))
      failures.push('rewind does not restore initial state');
    if (scenario.run.role === 'link') {
      h.seek(d);
      const { from, to } = result.ctx.handoff;
      if (
        Number(result.ctx.gsap.getProperty(to.node, 'opacity')) !== 1 ||
        to.node.style.visibility === 'hidden' ||
        Number(result.ctx.gsap.getProperty(from.node, 'opacity')) !== 0
      )
        failures.push('link end visibility');
      if (scenario.carry !== null) {
        const carry = scenario.carry?.(h, result.ctx) ?? from.node;
        const rect = carry.dataset?.slRect
          ? carriedRect(carry, result.ctx.gsap)
          : carry.getBoundingClientRect();
        const target = to.rect;
        if (
          ['x', 'y', 'w', 'h'].some(
            (key) =>
              Math.abs(
                (rect[key] ?? rect[{ x: 'left', y: 'top', w: 'width', h: 'height' }[key]]) - target[key],
              ) > 1,
          )
        )
          failures.push('link carry rect');
      }
    }
    h.destroy();
    // C17 8번: enter·step에서 skipNodes(link가 넘긴 요소)는 build가 상태를 바꾸지 않는다(initial·들여오기 금지).
    // step이 지나간 대상을 접는 tween은 허용(#48)이라 정지 0 시점의 값만 본다.
    if (scenario.run.role === 'enter' || scenario.run.role === 'step') {
      h = make();
      const beat = h.beats.get(scenario.run.beat);
      const skip = scenario.skip?.(h) ?? beat.part(beat.primary).slice(0, 1);
      if (skip.length) {
        const noop = { ...move, params: {}, timing: () => ({ duration: 1 }), build: () => {} };
        const gsap = h.runMove(noop, { role: scenario.run.role, beat: scenario.run.beat }).ctx.gsap;
        const props = (node) =>
          ['x', 'y', 'scaleX', 'scaleY', 'rotation', 'opacity', 'visibility'].map((p) => String(gsap.getProperty(node, p)));
        const before = skip.map(props);
        h.runMove(move, { ...scenario.run, skipNodes: skip });
        h.seek(0);
        if (skip.some((node, i) => JSON.stringify(props(node)) !== JSON.stringify(before[i])))
          failures.push('skipNodes changed by build');
      }
      h.destroy();
    }
    h = make(true);
    const reduced = h.runMove(move, scenario.run);
    for (const t of [0, reduced.timing.duration / 2, reduced.timing.duration]) {
      h.seek(t);
      const all = [...h.stage.root.querySelectorAll('*')];
      if (all.some((node) => /blur\((?!0(?:px)?\))/.test(node.getAttribute('style') ?? '')))
        failures.push('reduce leaves blur');
      const threeD = ['rotate' + 'X', 'rotate' + 'Y', 'translate' + 'Z', 'per' + 'spective', 'matrix3d'];
      if (
        move.family !== 'camera' &&
        all.some((node) => threeD.some((key) => (node.getAttribute('style') ?? '').includes(key)))
      )
        failures.push('non-camera uses 3d');
    }
  } catch (error) {
    failures.push(`run: ${error.message}`);
  } finally {
    h?.destroy();
  }
  return [...new Set(failures)];
}
