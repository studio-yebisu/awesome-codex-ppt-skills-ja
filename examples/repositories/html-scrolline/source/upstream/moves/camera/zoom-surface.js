/** Surface from a deep frame into its port inside the enclosing beat. */
import { colorOf } from '../_shared/color.js';
import { finishLink } from '../_shared/link.js';
import { px } from '../_shared/timeline.js';

const boxRect = (rect, box) => ({
  x: rect.x + rect.w * box.x,
  y: rect.y + rect.h * box.y,
  w: rect.w * box.w,
  h: rect.h * box.h,
});
const center = (rect) => ({ x: rect.x + rect.w / 2, y: rect.y + rect.h / 2 });
const originFor = (rect, fixed) => `${fixed.x - rect.x}px ${fixed.y - rect.y}px`;
const unique = (nodes) => [...new Set(nodes)];
const rectFor = (beat, node) => {
  for (const [name, nodes] of Object.entries(beat.parts)) {
    const index = nodes.indexOf(node);
    if (index >= 0) return beat.anchor(name, index).rect;
  }
  return { x: 0, y: 0, w: 0, h: 0 };
};
const worldParts = (beat, hud, ctx) => {
  const all = unique(
    Object.entries(beat.parts)
      .filter(([name]) => !hud.has(name) && !ctx.skipParts.includes(name))
      .flatMap(([, nodes]) => nodes)
      .filter((node) => !ctx.skipNodes?.includes(node)),
  );
  return all.filter((node) => !all.some((other) => other !== node && other.contains(node)));
};
const hudParts = (beat, names, ctx) =>
  unique(names.flatMap((name) => beat.part(name))).filter(
    (node) => !ctx.skipParts.includes(node.dataset.part) && !ctx.skipNodes?.includes(node),
  );
const autoK = (port, frame, tokens) =>
  Math.min(
    tokens.diveKMax ?? 40,
    1 / ((tokens.diveFill ?? 0.86) * Math.min(port.w / frame.w, port.h / frame.h)),
  );
/** Linear-in-scale ease whose scale reads k^(−z): (1 − k^−base(p)) / (1 − 1/k). */
export const expEaseOut = (gsap, k, ease) => {
  const base = gsap.parseEase(ease) ?? ((p) => p);
  return (p) => (1 - k ** -base(p)) / (1 - 1 / k);
};
/** An 'out' ease that holds 0 for the first `wait` of the tween: B's fade starts at span start (no flash of an
 * earlier initial) but becomes visible only after the wait. */
const late = (ctx, wait) => {
  const out = ctx.gsap.parseEase(ctx.ease('out')) ?? ((p) => p);
  return (p) => (p <= wait ? 0 : out((p - wait) / (1 - wait)));
};
const linkOverlays = (ctx, beat) =>
  [...ctx.stage.overlay.children].filter((node) => (node.dataset.overlayKey ?? '').startsWith(`${beat.id}:link:`));
const stepOverlays = (ctx, beat) =>
  [...ctx.stage.overlay.children].filter((node) => (node.dataset.overlayKey ?? '').startsWith(`${beat.id}:step:`));

/** 「방금 거기」 표시: 네 모서리 꺾쇠(viewfinder와 같은 말투). 상자 테두리는 카드처럼 보여서 쓰지 않는다 */
function ring(ctx, rect) {
  const pad = px(ctx, 10),
    far = px(ctx, 28),
    stroke = px(ctx, ctx.tokens.ringStroke ?? 2),
    accent = colorOf(ctx, 'accent');
  const len = Math.min(px(ctx, ctx.tokens.cornerLen ?? 28), (Math.min(rect.w, rect.h) + pad * 2) * 0.45);
  const node = document.createElement('div');
  node.className = 'sl-zoom-ring';
  Object.assign(node.style, { position: 'absolute', pointerEvents: 'none' });
  for (const [column, row] of [
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1],
  ]) {
    const corner = document.createElement('i');
    Object.assign(corner.style, {
      position: 'absolute',
      [column ? 'right' : 'left']: '0',
      [row ? 'bottom' : 'top']: '0',
      width: `${len}px`,
      height: `${len}px`,
      borderColor: accent,
      borderStyle: 'solid',
      borderWidth: `${row ? 0 : stroke}px ${column ? stroke : 0}px ${row ? stroke : 0}px ${column ? 0 : stroke}px`,
    });
    node.append(corner);
  }
  ctx.overlay.append(node);
  return {
    node,
    start: { left: rect.x - far, top: rect.y - far, width: rect.w + far * 2, height: rect.h + far * 2 },
    end: { left: rect.x - pad, top: rect.y - pad, width: rect.w + pad * 2, height: rect.h + pad * 2 },
  };
}

export default {
  id: 'zoom-surface',
  family: 'camera',
  role: 'link',
  accepts: ['chart', 'number', 'compare', 'photo', 'video', 'text'],
  sources: ['infinite-zoom', 'scale-swap', 'zoom-to-detail', 'focus-contraction'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 2.2, min: 1.2, max: 4, doc: '전체 길이(u)' },
    fromPart: { type: 'part', default: '', doc: 'A frame part. 비우면 primary' },
    toPart: { type: 'part', default: '', doc: 'B 포트 part. 비우면 primary' },
    toIndex: { type: 'integer', default: 0, min: 0, max: 31, doc: 'B 포트 요소 index' },
    toBox: { type: 'object', default: { x: 0, y: 0, w: 1, h: 1 }, doc: '포트 부분 상자(0..1)' },
    k: { type: 'number', default: 0, min: 0, max: 60, doc: '0=자동, 아니면 4..60 배율' },
    hudParts: {
      type: 'array',
      default: ['title', 'dek', 'note', 'source', 'legend', 'caption', 'verdict'],
      doc: 'A에서 배율을 받지 않고 먼저 사라지는 HUD part(number는 label 자동 추가)',
    },
    toHudParts: {
      type: 'array',
      default: ['title', 'dek', 'note', 'source', 'legend', 'caption', 'verdict'],
      doc: 'B에서 배율을 받지 않고 끝에 초점이 맞는 HUD part(number는 label 자동 추가)',
    },
    ease: { type: 'ease', default: 'dive', doc: 'dive | none | in | out' },
    keepRing: { type: 'boolean', default: true, doc: '끝난 뒤 링을 남긴다' },
    portFade: { type: 'number', default: 0.25, min: 0, max: 1, doc: '줄어드는 A를 받는 동안 포트의 불투명도(창)' },
  },
  handoff(params) {
    return {
      from: { part: params.fromPart || undefined },
      to: { part: params.toPart || undefined, index: params.toIndex },
    };
  },
  timing(params) {
    return { duration: params.duration, stops: [] };
  },
  build(tl, ctx, params) {
    const d = params.duration;
    const port = boxRect(ctx.handoff.to.rect, params.toBox),
      frame = ctx.handoff.from.rect;
    const k = Math.max(1.01, params.k || autoK(port, frame, ctx.tokens));
    const P = center(port),
      F = center(frame);
    const fixed = { x: (k * P.x - F.x) / (k - 1), y: (k * P.y - F.y) / (k - 1) };
    const fromHudNames = new Set(params.hudParts),
      toHudNames = new Set(params.toHudParts);
    if (ctx.from.type === 'number') fromHudNames.add('label');
    if (ctx.beat.type === 'number') toHudNames.add('label');
    const free = { ...ctx, skipParts: [], skipNodes: [] };
    const fromWorld = worldParts(ctx.from, fromHudNames, free);
    const toWorld = worldParts(ctx.beat, toHudNames, free);
    const fromHud = hudParts(ctx.from, [...fromHudNames], free);
    const toHud = hudParts(ctx.beat, [...toHudNames], free);
    const portNode = ctx.handoff.to.node;
    const focusRing = ring(ctx, port);
    // A의 step이 남긴 글자(strike-swap의 새 숫자)가 지금 화면의 주인공이면, 그것이 포트로 줄어든다.
    // 바뀌기 전 원래 world(지운 숫자)는 먼저 빠지고, 그 밖의 step 표식(취소선·label)은 곧바로 사라진다
    const steppedLayers = stepOverlays(ctx, ctx.from);
    const stepped = steppedLayers.flatMap((node) => [...node.children]);
    const carried = stepped.filter((node) => node.classList.contains('sl-strike-swap__value'));
    const dropped = stepped.filter((node) => !carried.includes(node));
    const partial = ['x', 'y'].some((key) => params.toBox[key] !== 0) || ['w', 'h'].some((key) => params.toBox[key] !== 1);
    // A 쪽 초기값은 앞 link의 B 초기값과 같은 요소에 겹칠 수 있다: B 쪽 등장은 전부 fromTo라 순서와 무관하다
    ctx.initial(fromWorld, { autoAlpha: 1 });
    ctx.initial(toWorld, { autoAlpha: 0 });
    ctx.initial(toHud, { autoAlpha: 0, y: px(ctx, ctx.tokens.hudRise ?? 16), filter: ctx.reduce ? 'none' : 'blur(4px)' });
    ctx.initial(focusRing.node, { ...focusRing.start, autoAlpha: 0 });
    if (dropped.length) tl.to(dropped, { opacity: 0, duration: d * 0.1, ease: ctx.ease('in') }, 0);
    // A에 남아 있던 「방금 거기」 링(앞 link가 남긴 것)은 A와 함께 떠난다
    const leftRings = linkOverlays(ctx, ctx.from).flatMap((node) => [...node.children]);
    if (leftRings.length) tl.to(leftRings, { opacity: 0, duration: d * 0.12, ease: ctx.ease('in') }, 0);
    if (ctx.reduce) {
      tl.to(fromWorld, { autoAlpha: 0, duration: d * 0.5, ease: ctx.ease('in') }, 0);
      tl.fromTo(toWorld, { autoAlpha: 0 }, { autoAlpha: 1, duration: d * 0.5, ease: ctx.ease('out'), immediateRender: false }, d * 0.5);
    } else {
      // 배율: A world part = k^−z(포트 크기로 줄어듦), B world part = k^(1−z)(거대하던 바깥이 모여듦)
      const ease = expEaseOut(ctx.gsap, k, ctx.ease(params.ease));
      const zoom = (nodes, beat, a, b) =>
        nodes.forEach((node) => {
          const transformOrigin = originFor(rectFor(beat, node), fixed);
          tl.fromTo(
            node,
            { scale: a, transformOrigin },
            { scale: b, transformOrigin, duration: d, ease, force3D: false, immediateRender: false },
            0,
          );
        });
      zoom(fromWorld, ctx.from, 1, 1 / k);
      if (carried.length)
        steppedLayers.forEach((node) =>
          tl.fromTo(
            node,
            { scale: 1, transformOrigin: `${fixed.x}px ${fixed.y}px` },
            { scale: 1 / k, transformOrigin: `${fixed.x}px ${fixed.y}px`, duration: d, ease, force3D: false, immediateRender: false },
            0,
          ),
        );
      zoom(toWorld, ctx.beat, k, 1);
      // 포트 요소 자신(숫자·막대)은 A가 다 줄어든 끝에 A와 바통을 넘긴다(finishLink). 그 전에 켜지면 A와 겹쳐 보인다
      const outside = toWorld.filter((node) => partial || node !== portNode);
      // 대신 포트는 옅은 창(portFade)으로 먼저 켜져 A가 어디로 들어가는지 틀이 되어 준다(zoom-dive의 거꾸로)
      if (!partial)
        tl.fromTo(portNode, { autoAlpha: 0 }, { autoAlpha: params.portFade, duration: d * 0.4, ease: late(ctx, 0.1 / 0.4), immediateRender: false }, 0);
      if (outside.length)
        tl.fromTo(outside, { autoAlpha: 0 }, { autoAlpha: 1, duration: d * 0.4, ease: late(ctx, 0.05 / 0.4), immediateRender: false }, 0);
      if (carried.length) {
        tl.to(fromWorld, { autoAlpha: 0, duration: d * 0.12, ease: ctx.ease('in') }, 0);
        tl.to(carried, { opacity: 0, duration: d * 0.3, ease: ctx.ease('in') }, d * 0.35);
      } else tl.to(fromWorld, { autoAlpha: 0, duration: d * 0.22, ease: ctx.ease('in') }, d * 0.74);
    }
    tl.to(fromHud, { y: -px(ctx, 12), autoAlpha: 0, duration: d * 0.1, ease: ctx.ease('in') }, 0);
    tl.to(toHud, { y: 0, autoAlpha: 1, filter: 'blur(0px)', duration: d * 0.12, ease: ctx.ease('out') }, d * 0.88);
    tl.to(
      focusRing.node,
      { ...focusRing.end, autoAlpha: params.keepRing ? 0.9 : 0, duration: d * 0.35, ease: ctx.ease('out') },
      d * 0.6,
    );
    // A의 사다리(ambient)는 B의 사다리가 같은 자리에 켜지기 직전(d − 0.1u)에 내려 둘이 겹쳐 보이지 않게 한다.
    // 덱은 B의 depth-ladder appearAfter를 link 길이 − 0.1로 맞춘다
    const leftLadders = [...ctx.stage.overlay.children]
      .filter((node) => (node.dataset.overlayKey ?? '').startsWith(`${ctx.from.id}:ambient:`))
      .flatMap((node) => [...node.children]);
    if (leftLadders.length) tl.set(leftLadders, { opacity: 0 }, Math.max(0, d - 0.1));
    // 포트가 요소의 일부 상자(영상 속 버튼 띠)면 요소 자체는 B world와 함께 보여야 한다
    finishLink(tl, ctx, { at: d, cross: 0.15, from: [ctx.handoff.from.node], to: partial ? [] : [portNode] });
    tl.set(toWorld, { autoAlpha: 1 }, d);
  },
};
