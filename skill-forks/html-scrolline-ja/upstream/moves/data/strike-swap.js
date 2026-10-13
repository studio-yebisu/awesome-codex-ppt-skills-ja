/** Replaces a number in place, retaining the struck old value as context. */
import { colorOf } from '../_shared/color.js';
import { driveValue } from '../_shared/drive.js';
import { px } from '../_shared/timeline.js';

const format = (value, decimals, lang) =>
  new Intl.NumberFormat(lang ?? 'ko', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
// 지운 값 접기는 step 구간 안의 「지나간 것으로 접는」 tween이라 link가 넘겨준 숫자에도 허용된다(C5 v2.2, #48)
const part = (ctx, name) => ctx.beat.part(name);
/** Overlay copy of a beat element at its measured rect: same classes, so the same type style. */
function copyAt(ctx, node, rect, minWidth = 0) {
  const width = Math.max(rect.w, minWidth);
  const copy = node.cloneNode(true);
  for (const el of [copy, ...copy.querySelectorAll('[data-part]')]) el.removeAttribute('data-part');
  copy.removeAttribute('style');
  Object.assign(copy.style, {
    position: 'absolute',
    left: `${rect.x + rect.w / 2 - width / 2}px`,
    top: `${rect.y}px`,
    width: `${width}px`,
    margin: '0',
    textAlign: 'center',
  });
  ctx.overlay.append(copy);
  return copy;
}

export default {
  id: 'strike-swap',
  family: 'data',
  role: 'step',
  accepts: ['number'],
  sources: ['strikethrough-replace', 'rolling-digits', 'count-up'],
  reduce: 'self',
  params: {
    to: { type: 'number', default: 0, doc: '새 값' },
    decimals: { type: 'integer', default: 0, min: 0, max: 4, doc: 'decimals(안무 설명의 같은 이름)' },
    suffix: { type: 'string', default: '', doc: '새 값 뒤 단위. 비우면 data.format.suffix' },
    label: { type: 'string', default: '', doc: '새 label 한 줄. 비우면 기존 유지' },
    duration: { type: 'number', default: 1.6, min: 0.8, max: 3, doc: 'u' },
  },
  timing: (params) => ({ duration: params.duration, stops: [] }),
  build(tl, ctx, params) {
    const d = params.duration,
      data = ctx.beat.data,
      oldValue = part(ctx, 'value')[0],
      oldDigits = part(ctx, 'digits')[0];
    if (!oldValue || !oldDigits) return;
    const valueRect = ctx.beat.anchor('value').rect,
      digitsRect = ctx.beat.anchor('digits').rect;
    const fontSize = Number.parseFloat(globalThis.getComputedStyle?.(oldValue).fontSize) || digitsRect.h;
    // 지운 값은 위로 작게 물러나며 새 값 자리를 비운다. 취소선은 그 값과 함께 움직이도록 같은 틀(carrier) 안에 그린다
    const lift = ctx.reduce ? 0 : -(0.5 + 0.21) * valueRect.h - px(ctx, 20),
      shrink = ctx.reduce ? 1 : 0.42;
    const carrier = document.createElement('div');
    carrier.className = 'sl-strike-swap__carrier';
    Object.assign(carrier.style, {
      position: 'absolute',
      left: `${valueRect.x}px`,
      top: `${valueRect.y}px`,
      width: `${valueRect.w}px`,
      height: `${valueRect.h}px`,
      pointerEvents: 'none',
    });
    const strike = document.createElement('i');
    Object.assign(strike.style, {
      position: 'absolute',
      left: `${digitsRect.x - valueRect.x - fontSize * 0.04}px`,
      top: `${digitsRect.y - valueRect.y + digitsRect.h * 0.52}px`,
      width: `${digitsRect.w + fontSize * 0.08}px`,
      height: `${Math.max(2, fontSize * 0.035)}px`,
      background: colorOf(ctx, 'accent'),
      transformOrigin: 'left center',
    });
    carrier.append(strike);
    ctx.overlay.append(carrier);
    ctx.initial(strike, { scaleX: 0 });
    tl.to(strike, { scaleX: 1, duration: d * 0.3, ease: ctx.ease('out') }, 0);
    const back = { y: lift, scale: shrink, duration: d * 0.3, ease: ctx.ease('inout') };
    // 앞 link가 남긴 고정점 transform-origin이 아니라 숫자 자신의 가운데를 기준으로 물러난다
    tl.to(oldValue, { ...back, transformOrigin: '50% 50%', autoAlpha: ctx.reduce ? 0 : 0.35 }, d * 0.25);
    tl.to(carrier, { ...back, autoAlpha: ctx.reduce ? 0 : 0.6 }, d * 0.25);

    const fresh = copyAt(ctx, oldValue, valueRect);
    fresh.classList.add('sl-strike-swap__value');
    fresh.style.color = colorOf(ctx, 'accent-2');
    const freshDigits = fresh.querySelector('.sl-number__digits') ?? fresh;
    freshDigits.classList.add('sl-strike-swap__digits');
    const suffix = params.suffix || data.format?.suffix;
    const freshSuffix = fresh.querySelector('.sl-number__suffix');
    if (freshSuffix && suffix) freshSuffix.textContent = suffix;
    freshDigits.textContent = format(data.value, params.decimals, data.lang);
    ctx.initial(fresh, { autoAlpha: 0, y: ctx.reduce ? 0 : px(ctx, 24) });
    tl.to(fresh, { autoAlpha: 1, y: 0, duration: d * 0.45, ease: ctx.ease('out') }, d * 0.4);
    // 숫자 굴림은 seek에도 그려지는 접근자 tween으로(onUpdate는 seek에서 건너뛴다)
    const roll = (v) => {
      freshDigits.textContent = format(v, params.decimals, data.lang);
    };
    if (!ctx.reduce)
      driveValue(tl, roll, { from: data.value, to: params.to, at: d * 0.4, duration: d * 0.45, ease: ctx.ease('out') });
    else tl.set(freshDigits, { textContent: format(params.to, params.decimals, data.lang) }, d * 0.4);
    tl.set(freshDigits, { textContent: format(params.to, params.decimals, data.lang) }, d * 0.85);
    const labels = part(ctx, 'label');
    tl.to(labels, { autoAlpha: 0, duration: d * 0.25, ease: ctx.ease('out') }, d * 0.6);
    if (params.label) {
      const old = labels[0];
      const label = old
        ? copyAt(ctx, old, ctx.beat.anchor('label').rect, px(ctx, 1280))
        : Object.assign(document.createElement('p'), {});
      if (!old) {
        Object.assign(label.style, { position: 'absolute', left: `${valueRect.x}px`, top: `${valueRect.y + valueRect.h}px` });
        ctx.overlay.append(label);
      }
      label.classList.add('sl-strike-swap__label');
      label.textContent = params.label;
      ctx.initial(label, { autoAlpha: 0, y: ctx.reduce ? 0 : px(ctx, 10) });
      tl.to(label, { autoAlpha: 1, y: 0, duration: d * 0.4, ease: ctx.ease('out') }, d * 0.6);
    }
  },
};
