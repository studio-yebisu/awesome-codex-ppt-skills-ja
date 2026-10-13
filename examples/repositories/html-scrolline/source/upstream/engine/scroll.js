/** Lenis + ScrollTrigger 스크롤 드라이버(CONTRACTS C2, C12). */
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { EVENTS, PRESENTER_TRAVEL } from './constants.js';

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

function emitStop(map, time) {
  const index = map.stops.findIndex((stop) => Math.abs(stop.t - time) <= PRESENTER_TRAVEL.stopEps);
  if (index < 0 || typeof window === 'undefined') return;
  const stop = map.stops[index];
  window.dispatchEvent(new CustomEvent(EVENTS.stop, { detail: { name: stop.name, index, beat: stop.beat } }));
}

/**
 * @param {{ track: HTMLElement, tl: object, map: import('./types.js').TimelineMap,
 *           viewport: import('./types.js').Viewport, reduce: boolean }} opts
 * @returns {import('./types.js').ScrollDriver}
 */
export function createScrollDriver({ track, tl, map, viewport, reduce }) {
  const lenis = new Lenis(
    reduce ? { smoothWheel: false, lerp: 1 } : { lerp: 0.1, wheelMultiplier: 0.9, smoothWheel: true },
  );
  let st = null;
  let attached = false;
  let stopTimer = null;
  const ticker = (time) => lenis.raf(time * 1000);
  const range = () => ({ start: Number(st?.start ?? 0), end: Number(st?.end ?? 0) });
  const timeToY = (time) => {
    const { start, end } = range();
    if (!map.duration || end === start) return start;
    return start + (clamp(time, 0, map.duration) / map.duration) * (end - start);
  };
  const yToTime = (y) => {
    const { start, end } = range();
    if (end === start) return 0;
    return clamp(((y - start) / (end - start)) * map.duration, 0, map.duration);
  };
  const time = () => Number(typeof tl.time === 'function' ? tl.time() : 0);
  const onScroll = () => {
    ScrollTrigger.update();
    if (stopTimer !== null) clearTimeout(stopTimer);
    stopTimer = setTimeout(() => emitStop(map, time()), PRESENTER_TRAVEL.settleMs);
  };
  function attach() {
    if (attached) return;
    attached = true;
    track.style.height = `${viewport.h + map.duration * viewport.h * map.unit}px`;
    gsap.registerPlugin(ScrollTrigger);
    st = ScrollTrigger.create({
      trigger: track,
      start: 'top top',
      end: 'bottom bottom',
      scrub: true,
      animation: tl,
    });
    // ScrollTrigger는 start·end를 다음 refresh까지 미룬다. 그 전에 seek(boot의 ?t·?stop, rebuild 복귀)하면
    // timeToY가 0을 돌려 스크롤이 맨 위에 남고 scrub이 timeline을 0으로 되돌린다.
    st.refresh?.();
    lenis.on('scroll', onScroll);
    gsap.ticker.add(ticker);
    gsap.ticker.lagSmoothing(0);
  }
  function detach() {
    if (!attached) return;
    attached = false;
    if (stopTimer !== null) clearTimeout(stopTimer);
    stopTimer = null;
    lenis.off?.('scroll', onScroll);
    gsap.ticker.remove(ticker);
    st?.kill?.();
    st = null;
    lenis.destroy?.();
  }
  function seek(targetTime, options = {}) {
    const target = clamp(targetTime, 0, map.duration);
    const immediate = options.immediate ?? false;
    const duration = options.duration;
    lenis.scrollTo(timeToY(target), { immediate, ...(duration === undefined ? {} : { duration }) });
    tl.seek?.(target);
  }
  return {
    attach,
    detach,
    timeToY,
    yToTime,
    time,
    seek,
    stops: () => map.stops.map((stop) => ({ ...stop, y: timeToY(stop.t) })),
    lenis,
    get st() {
      return st;
    },
  };
}
