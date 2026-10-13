/** Extends observed line data into a visibly dashed forecast interval.
 *  전망 열에 빗금 띠가 먼저 깔리고(여기부터 실측 아님), 마지막 실측점에서 점선이 전망값까지 이어진다.
 *  끝점은 속 빈 주홍 원 + 값 표, 상태 층 주석은 끝점 아래. */
import { colorOf } from '../_shared/color.js';
import { polyline, svgLayer } from '../_shared/stroke.js';
import { px } from '../_shared/timeline.js';
import { draw, layers, plotBox, pointAt, swapLayers, tag } from './annotation-pin.js';
import { valueText } from './ink-in.js';

const NS = 'http://www.w3.org/2000/svg';
export default {
  id: 'forecast-extend',
  family: 'data',
  role: 'step',
  accepts: ['chart'],
  sources: ['confidence-band-reveal', 'point-to-point-build'],
  reduce: 'self',
  params: {
    duration: { type: 'number', default: 1.8, min: 0.6, max: 3, doc: '전체 길이(u)' },
    fromIndex: { type: 'integer', default: 0, min: 0, max: 40, doc: '마지막 실측 범주 index' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      R = ctx.reduce ? 0.001 : 1,
      data = ctx.beat.data,
      values = data.series[0].values,
      n = values.length,
      from = Math.min(params.fromIndex, n - 1),
      box = plotBox(ctx.beat),
      step = n > 1 ? box.w / (n - 1) : box.w,
      accent = colorOf(ctx, 'accent'),
      rule = colorOf(ctx, 'rule');
    // 빗금 띠: 실측 끝과 전망 사이 중간부터 오른쪽 끝까지
    const band = document.createElement('div');
    const left = box.x + (from + 0.5) * step;
    Object.assign(band.style, {
      position: 'absolute',
      left: `${left}px`,
      top: `${box.y - px(ctx, 20)}px`,
      width: `${box.x + box.w + step * 0.5 - left}px`,
      height: `${box.h + px(ctx, 20)}px`,
      backgroundImage: `repeating-linear-gradient(135deg, transparent 0 ${px(ctx, 9)}px, ${rule} ${px(ctx, 9)}px ${px(ctx, 11)}px)`,
      borderLeft: `${px(ctx, 2)}px dashed ${colorOf(ctx, 'fg-muted')}`,
    });
    ctx.overlay.append(band);
    ctx.initial(band, { autoAlpha: 0, clipPath: 'inset(0% 100% 0% 0%)' });
    tl.to(band, { autoAlpha: 1, clipPath: 'inset(0% 0% 0% 0%)', duration: d * 0.3 * R, ease: ctx.ease('inout') }, 0);
    // 숨겨 둔 전망 범주 이름표
    const later = ctx.beat.part('label').filter((_, i) => i > from);
    tl.to(later, { autoAlpha: 1, duration: d * 0.2 * R, ease: ctx.ease('out') }, d * 0.15);
    // 점선
    const pts = values.slice(from).map((v, k) => pointAt(ctx.beat, from + k, v));
    const svg = svgLayer(ctx);
    const dash = polyline(svg, pts, { stroke: accent, 'stroke-width': px(ctx, 5), 'stroke-linecap': 'round' });
    // drawOn이 쓰는 dasharray(1 1) 대신 점선 패턴: 마스크로 그리기
    const mask = document.createElementNS(NS, 'mask');
    mask.id = `sl-fc-${ctx.beat.id}`;
    const reveal = polyline(svg, pts, { stroke: '#fff', 'stroke-width': px(ctx, 14) });
    mask.append(reveal);
    svg.append(mask);
    dash.setAttribute('stroke-dasharray', `${px(ctx, 2)} ${px(ctx, 14)}`);
    dash.setAttribute('stroke-dashoffset', '0');
    dash.removeAttribute('pathLength');
    dash.setAttribute('mask', `url(#${mask.id})`);
    ctx.reduce ? tl.set(reveal, { strokeDashoffset: 0 }, 0) : draw(tl, ctx, reveal, { at: d * 0.3, duration: d * 0.35, ease: ctx.ease('inout') });
    const end = pts.at(-1);
    const ring = document.createElementNS(NS, 'circle');
    ring.setAttribute('cx', String(end.x));
    ring.setAttribute('cy', String(end.y));
    ring.setAttribute('r', String(px(ctx, 12)));
    ring.setAttribute('fill', colorOf(ctx, 'bg'));
    ring.setAttribute('stroke', accent);
    ring.setAttribute('stroke-width', String(px(ctx, 5)));
    svg.append(ring);
    ctx.initial(ring, { autoAlpha: 0, attr: { r: px(ctx, 4) } });
    tl.to(ring, { autoAlpha: 1, attr: { r: px(ctx, 12) }, duration: d * 0.15 * R, ease: ctx.ease('settle') }, d * 0.62);
    const value = tag(ctx, valueText(values.at(-1), data.unit ?? ''), { x: end.x, y: end.y - px(ctx, 26), align: 'center', valign: 'bottom', size: 44, weight: 900, color: 'accent' });
    ctx.initial(value, { autoAlpha: 0, y: px(ctx, 8) });
    tl.to(value, { autoAlpha: 1, y: 0, duration: d * 0.15 * R, ease: ctx.ease('settle') }, d * 0.66);
    // 상태 층 주석(전망 출처)은 빗금 띠 왼쪽 아래 빈자리에 오른쪽 맞춤
    const { fresh } = layers(ctx, ['note']);
    fresh.forEach((node) => {
      const nr = ctx.beat.anchor('note', ctx.beat.part('note').indexOf(node)).rect;
      const dx = left - px(ctx, 20) - nr.w - nr.x,
        dy = box.y + box.h - px(ctx, 24) - nr.h - nr.y;
      ctx.initial(node, { autoAlpha: 0, x: dx, y: dy, color: colorOf(ctx, 'fg-muted') });
      tl.to(node, { autoAlpha: 1, duration: d * 0.15 * R }, d * 0.75);
    });
    swapLayers(tl, ctx, d * 0.45, d * 0.3 * R, ['title', 'dek', 'unit']);
  },
};
