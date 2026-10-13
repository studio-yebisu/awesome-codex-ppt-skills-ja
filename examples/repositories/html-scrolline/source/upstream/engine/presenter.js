/** 발표 키(CONTRACTS C12). */
import { EVENTS, PRESENTER_TRAVEL } from './constants.js';

const focusConsumesSpace = (doc) => {
  const active = doc?.activeElement;
  const tag = active?.tagName?.toLowerCase();
  return active?.isContentEditable || ['a', 'button', 'input', 'select', 'textarea'].includes(tag);
};
const customEvent = (type, detail) => new CustomEvent(type, { detail });

/**
 * @param {import('./types.js').ScrollDriver} driver
 * @param {{ reduce: boolean, target?: EventTarget, doc?: Document }} opts
 * @returns {import('./types.js').Presenter}
 */
export function createPresenter(driver, { reduce, target = window, doc = globalThis.document } = {}) {
  let blackoutOn = false;
  let pendingTime = null;
  let arrivalTimer = null;
  const stops = () => driver.stops();
  const current = () => pendingTime ?? driver.time();
  const dispatchStop = (stop) => {
    const index = stops().findIndex((candidate) => candidate.name === stop.name);
    target.dispatchEvent(customEvent(EVENTS.stop, { name: stop.name, index, beat: stop.beat }));
  };
  const move = (stop) => {
    if (!stop) return;
    const from = current();
    const deltaY = Math.abs(stop.y - driver.timeToY(from));
    const duration = Math.min(
      PRESENTER_TRAVEL.max,
      PRESENTER_TRAVEL.base +
        (deltaY / Math.max(1, globalThis.innerHeight || 1)) * PRESENTER_TRAVEL.perScreen,
    );
    if (arrivalTimer !== null) clearTimeout(arrivalTimer);
    pendingTime = stop.t;
    driver.seek(stop.t, reduce ? { immediate: true } : { duration });
    if (reduce) {
      pendingTime = null;
      dispatchStop(stop);
      return;
    }
    arrivalTimer = setTimeout(() => {
      pendingTime = null;
      arrivalTimer = null;
      dispatchStop(stop);
    }, duration * 1000);
  };
  const goto = (name) => move(stops().find((stop) => stop.name === name || stop.label === name));
  const next = () => move(stops().find((stop) => stop.t >= current() + PRESENTER_TRAVEL.minGap));
  const prev = () =>
    move([...stops()].reverse().find((stop) => stop.t <= current() - PRESENTER_TRAVEL.minGap));
  const first = () => move(stops()[0]);
  const last = () => move(stops().at(-1));
  const blackout = (on) => {
    blackoutOn = on ?? !blackoutOn;
    target.dispatchEvent(customEvent(EVENTS.blackout, { on: blackoutOn }));
  };
  const fullscreen = () => {
    if (doc?.fullscreenElement) doc.exitFullscreen?.();
    else doc?.documentElement?.requestFullscreen?.();
  };
  const onKeydown = (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    const space = event.key === ' ' || event.code === 'Space';
    if ((space || event.key === 'Enter') && focusConsumesSpace(doc)) return;
    let action;
    if (space) action = event.shiftKey ? prev : next;
    else if (!event.shiftKey && ['ArrowRight', 'ArrowDown', 'PageDown'].includes(event.key)) action = next;
    else if (!event.shiftKey && ['ArrowLeft', 'ArrowUp', 'PageUp'].includes(event.key)) action = prev;
    else if (!event.shiftKey && event.key === 'Home') action = first;
    else if (!event.shiftKey && event.key === 'End') action = last;
    else if (!event.shiftKey && (event.key === 'b' || event.key === '.')) action = blackout;
    else if (!event.shiftKey && event.key === 'f') action = fullscreen;
    if (!action) return;
    event.preventDefault();
    action();
  };
  target.addEventListener('keydown', onKeydown);
  return {
    next,
    prev,
    first,
    last,
    goto,
    blackout,
    destroy() {
      target.removeEventListener('keydown', onKeydown);
      if (arrivalTimer !== null) clearTimeout(arrivalTimer);
    },
  };
}
