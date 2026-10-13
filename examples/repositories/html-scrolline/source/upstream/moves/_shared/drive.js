/**
 * Seek-safe side effects. GSAP's seek()/pause(t) suppress callbacks, so work done in a tween's onUpdate
 * (frame scrub, number text, canvas paint) is skipped on every jump: presenter keys, smoke stops, export.
 * Here the tween writes an accessor property directly and the setter applies the value, which runs on
 * every render whatever suppressEvents says.
 */
export function driveValue(tl, apply, { from, to, at, duration, ease }) {
  let value = from;
  const proxy = {
    get v() {
      return value;
    },
    set v(next) {
      value = next;
      apply(next);
    },
  };
  // ease 생략 = GSAP 기본값(호출부가 이전과 같은 곡선을 유지하도록)
  const vars = { v: to, duration, immediateRender: false, lazy: false, ...(ease === undefined ? {} : { ease }) };
  tl.fromTo(proxy, { v: from }, vars, at);
  return proxy;
}
