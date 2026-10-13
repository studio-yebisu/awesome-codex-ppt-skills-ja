/** Aim at one port before a zoom dive. Used by zoom decks. */
import { colorOf } from '../_shared/color.js';
import { drawOn, line, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';

const SVG = 'http://www.w3.org/2000/svg';
const HUD = ['title', 'dek', 'note', 'source', 'legend', 'caption', 'verdict'];

/**
 * Parts to dim: everything but the port, its ancestors (dimming an <svg> would dim the port inside it) and its
 * descendants; a node whose ancestor is already dimmed is left alone so opacity never multiplies. Dimming is a
 * fold inside the step span, so it also applies to parts a link handed over (C5 v2.2, #48).
 */
function others(ctx, port) {
  const all = Object.values(ctx.beat.parts)
    .flat()
    .filter((node) => node !== port && !node.contains(port) && !port.contains(node));
  const unique = [...new Set(all)];
  return unique.filter((node) => !unique.some((other) => other !== node && other.contains(node)));
}

export default {
  id: 'port-aim',
  family: 'emphasis',
  role: 'step',
  accepts: ['chart', 'number', 'compare', 'photo', 'video', 'text'],
  sources: ['focus-contraction', 'spotlight', 'annotation-callout', 'zoom-to-detail'],
  reduce: 'fade',
  params: {
    part: { type: 'part', default: '', doc: '조준할 포트 part(비우면 primary)' },
    index: { type: 'integer', default: 0, min: 0, max: 31, doc: '대상 요소 index' },
    box: { type: 'object', default: { x: 0, y: 0, w: 1, h: 1 }, doc: '포트 내부 정규화 상자' },
    label: { type: 'string', default: '', doc: '짧은 숫자 주석' },
    labelSide: { type: 'enum', default: 'right', values: ['right', 'left', 'top'], doc: '주석 방향' },
    duration: { type: 'number', default: 1.2, min: 0.6, max: 2, doc: 'u' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      anchor = ctx.beat.anchor(params.part, params.index),
      rect = anchor.rect;
    const box = params.box,
      port = { x: rect.x + rect.w * box.x, y: rect.y + rect.h * box.y, w: rect.w * box.w, h: rect.h * box.h };
    // 링 = 포트 모양 그대로의 사각 틀(숫자 획·막대·화면·버튼 띠마다 모양이 다르다). 넓고 옅은 판에서 조여든다
    const pad = px(ctx, ctx.tokens.ringPad ?? 12);
    const far = px(ctx, ctx.tokens.ringStart ?? 420) / 4;
    const end = { x: port.x - pad, y: port.y - pad, width: port.w + pad * 2, height: port.h + pad * 2 };
    const start = { x: end.x - far, y: end.y - far, width: end.width + far * 2, height: end.height + far * 2 };
    const accent = colorOf(ctx, 'accent'),
      svg = svgLayer(ctx);
    const ring = document.createElementNS(SVG, 'rect');
    ring.setAttribute('class', 'sl-port-aim__ring');
    ring.setAttribute('rx', String(px(ctx, 2)));
    ring.setAttribute('fill', accent);
    ring.setAttribute('stroke', accent);
    ring.setAttribute('stroke-width', String(px(ctx, ctx.tokens.ringStroke ?? 2)));
    svg.append(ring);
    const gap = px(ctx, 64);
    const side = params.labelSide;
    const leadStart =
      side === 'top'
        ? { x: end.x + end.width / 2, y: end.y }
        : { x: side === 'left' ? end.x : end.x + end.width, y: end.y + end.height / 2 };
    const leadEnd =
      side === 'top'
        ? { x: leadStart.x, y: leadStart.y - gap }
        : { x: leadStart.x + (side === 'left' ? -gap : gap), y: leadStart.y };
    const leader = params.label
      ? line(svg, leadStart.x, leadStart.y, leadEnd.x, leadEnd.y, {
          stroke: accent,
          'stroke-width': px(ctx, ctx.tokens.leaderWidth ?? 1.5),
        })
      : null;
    const label = params.label ? document.createElement('div') : null;
    if (label) {
      label.className = 'sl-port-aim__label';
      label.textContent = params.label;
      Object.assign(label.style, {
        position: 'absolute',
        left: `${leadEnd.x}px`,
        top: `${leadEnd.y}px`,
        padding: side === 'top' ? `0 0 ${px(ctx, 8)}px` : `0 ${px(ctx, 12)}px`,
        color: accent,
        fontWeight: '700',
      });
      ctx.overlay.append(label);
    }
    ctx.initial(ring, { attr: start, fillOpacity: 0.18, strokeOpacity: 0 });
    if (leader) ctx.initial(leader, { strokeDashoffset: 1 });
    // 기준점 정렬은 xPercent·yPercent로(gsap이 transform을 쓰면 CSS translate는 지워진다)
    const anchorAt = side === 'top' ? { xPercent: -50, yPercent: -100 } : { xPercent: side === 'left' ? -100 : 0, yPercent: -50 };
    if (label) ctx.initial(label, { ...anchorAt, autoAlpha: 0, y: px(ctx, 8) });
    const hudNames = ctx.beat.type === 'number' ? [...HUD, 'label'] : HUD;
    const dim = others(ctx, anchor.node);
    const hud = dim.filter((node) => hudNames.includes(node.dataset.part));
    const rest = dim.filter((node) => !hud.includes(node));
    if (rest.length)
      tl.to(rest, { opacity: ctx.tokens.dimOthers ?? 0.22, duration: d * 0.35, ease: ctx.ease('out') }, 0);
    if (hud.length) tl.to(hud, { opacity: 0.6, duration: d * 0.35, ease: ctx.ease('out') }, 0);
    tl.to(
      ring,
      { attr: end, fillOpacity: 0, strokeOpacity: 1, duration: d * 0.45, ease: ctx.ease('inout') },
      d * 0.15,
    );
    if (params.label) {
      drawOn(tl, leader, { at: d * 0.45, duration: d * 0.35, ease: 'none' });
      tl.to(label, { autoAlpha: 1, y: 0, duration: d * 0.2, ease: ctx.ease('out') }, d * 0.6);
    }
  },
};
