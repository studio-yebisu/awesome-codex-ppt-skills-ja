/** Digit reel construction and deterministic rolling. */
export function buildReel(host, text) {
  host.replaceChildren();
  const cols = [];
  [...String(text)].forEach((char, place) => {
    const node = document.createElement('span');
    if (/\d/.test(char)) {
      node.className = 'sl-reel__col';
      node.dataset.place = String(place);
      node.dataset.digit = char;
      for (let d = 0; d < 10; d += 1) {
        const digit = document.createElement('span');
        digit.textContent = String(d);
        node.append(digit);
      }
      cols.push(node);
    } else {
      node.className = 'sl-reel__fixed';
      node.textContent = char;
    }
    host.append(node);
  });
  return { cols, text: String(text) };
}
export function reelFrom(counterEl) {
  return { cols: [...counterEl.querySelectorAll('[data-place]')], text: counterEl.textContent ?? '' };
}
export function rollReel(
  tl,
  reel,
  fromText,
  toText,
  { at, duration, ease, stagger = 0, steps = false } = {},
) {
  const from = String(fromText),
    to = String(toText),
    changed = [];
  const offset = Math.max(0, to.length - from.length);
  reel.cols.forEach((col, index) => {
    const place = Number(col.dataset.place ?? index),
      target = to[place],
      source = from[place - offset] ?? '';
    if (/\d/.test(target) && target !== source)
      changed.push({ col, source: Number(source) || 0, target: Number(target) });
  });
  changed.forEach(({ col, source, target }, i) => {
    const vars = {
      yPercent: -target * 10,
      duration,
      ease: steps ? `steps(${Math.max(1, Math.abs(target - source))})` : ease,
      immediateRender: false,
    };
    tl.fromTo(col, { yPercent: -source * 10 }, vars, at + i * stagger);
  });
  if (to.length > from.length)
    reel.cols
      .slice(0, to.length - from.length)
      .forEach((col) => tl.fromTo(col, { width: 0 }, { width: 1, duration, immediateRender: false }, at));
}
