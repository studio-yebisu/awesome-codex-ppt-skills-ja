/* MORPH-SLIDES DIAGRAMS: turns short data-* markup into geometry,
   so a slide states WHAT the numbers are and the kit draws them.
   Load order: morph-viz-diagrams.js, morph-viz.js, then
   morph-engine.js (the engine measures the finished DOM).
   Every chart with numbers needs data-source (audit checks it).
     <div class="viz" data-viz="span"   data-values data-labels data-sub>
     <div class="viz" data-viz="donut"  data-values>
     <div class="viz" data-viz="plan"   data-w data-h data-top data-bottom data-left data-right>
     <div class="viz" data-viz="gather" data-n>                                   */
(() => {
  const nums = (s) => (s || '').split(',').map((x) => x.trim()).filter(Boolean).map(Number).filter(Number.isFinite);
  // data-* text is shown as text, never parsed as HTML
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const list = (s) => (s || '').split('|').map(esc);
  const sum = (a) => a.reduce((x, y) => x + y, 0);
  const NS = 'http://www.w3.org/2000/svg';
  const svg = (w, h, inner) => `<svg xmlns="${NS}" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${inner}</svg>`;

  /* span: proportional bar (time, budget...). Notes alternate above / below
     the bar, start at their segment and never run into the next note. */
  function span(el) {
    const v = nums(el.dataset.values), lab = list(el.dataset.labels), sub = list(el.dataset.sub);
    const W = el.clientWidth || 1680, tot = sum(v) || 1, cap = +el.dataset.cap || 420;
    const morphId = el.dataset.morphId ? esc(el.dataset.morphId) : '';
    el.removeAttribute('data-morph-id');   // only the segment below carries it
    let acc = 0;
    const segs = v.map((n, i) => { const s = { i, n, x: (acc / tot) * W, w: (n / tot) * W }; acc += n; return s; });
    const bar = segs.map((s) => `<div class="seg fx fx-growx${s.i === +el.dataset.hot ? ' hot' : ''}" style="left:${s.x}px;width:${s.w}px;--d:${(0.15 * s.i).toFixed(2)}">
      ${s.i === +el.dataset.morphSeg ? `<i class="morph-src" data-morph-id="${morphId}"></i>` : ''}<b>${s.n}</b></div>`).join('');
    const end = { above: 0, below: 0 };   // right edge of the last note on each side
    const notes = segs.map((s) => {
      const side = s.i % 2 ? 'below' : 'above';
      const nxt = segs.find((o) => o.i > s.i && o.i % 2 === s.i % 2);
      let x = s.x, w = Math.min(cap, (nxt ? nxt.x : W) - s.x - 24), flip = false;
      if (!nxt && w < 220) { flip = true; w = Math.min(cap, s.x + s.w - end[side] - 24); x = s.x + s.w - w; }
      end[side] = x + w;
      return `<div class="note ${side}${flip ? ' flip' : ''} fx fx-up" style="left:${x}px;width:${w}px;--d:${(0.3 + 0.15 * s.i).toFixed(2)}">
        <span class="mono">${sub[s.i] || ''}</span><span>${lab[s.i] || ''}</span></div>`;
    }).join('');
    el.innerHTML = `<div class="bar">${bar}</div>${notes}`;
  }

  /* donut: arcs drawn one after another, numbered at their middle */
  function donut(el) {
    const v = nums(el.dataset.values), tot = sum(v) || 1, R = 300, r = 220, c = R + 40, gap = 0.5;
    let acc = 0;
    const arcs = v.map((n, i) => {
      const p = (n / tot) * 100, mid = ((acc + n / 2) / tot) * 2 * Math.PI - Math.PI / 2;
      const out = `<circle class="arc" cx="${c}" cy="${c}" r="${r + 40}" pathLength="100"
          style="--v:${(p - gap).toFixed(2)};--off:${(-(acc / tot) * 100).toFixed(2)};--d:${(0.25 * i).toFixed(2)};--k:${i}"/>
        <text class="arc-n fx fx-pop" x="${c + Math.cos(mid) * (R + 34)}" y="${c + Math.sin(mid) * (R + 34)}" style="--d:${(0.25 * i + 0.4).toFixed(2)}">${i + 1}</text>`;
      acc += n;
      return out;
    }).join('');
    el.innerHTML = svg(2 * c, 2 * c, arcs);
  }

  /* plan: building outline + four dimension chains, ticks at every
     cumulative mark. A chain that does not close is drawn hot and
     gets a lens on the gap. Scale fits the element height. */
  function plan(el) {
    const Wmm = +el.dataset.w, Hmm = +el.dataset.h, k = Math.max(10, el.clientHeight - 200) / Hmm;
    const w = Wmm * k, h = Hmm * k, ox = 110, oy = 100, off = 52, t = 11;
    const chain = (key, horiz, far, d) => {
      if (!el.dataset[key]) return '';
      const seg = nums(el.dataset[key]), full = horiz ? Wmm : Hmm, ok = Math.abs(sum(seg) - full) < 1e-6;
      const at = (mm) => (horiz ? ox + mm * k : oy + mm * k);
      const base = horiz ? (far ? oy + h + off : oy - off) : (far ? ox + w + off : ox - off);
      let marks = [0], a = 0;
      seg.forEach((s) => { a += s; marks.push(a); });
      const line = horiz ? `M${at(0)} ${base}H${at(sum(seg))}` : `M${base} ${at(0)}V${at(sum(seg))}`;
      const ticks = marks.map((m) => (horiz ? `M${at(m) - t} ${base + t}L${at(m) + t} ${base - t}` : `M${base - t} ${at(m) + t}L${base + t} ${at(m) - t}`)).join('');
      const cls = ok ? '' : ' hot';
      // lens: magnify the end of a chain that does not close
      const ex = horiz ? at(full) : base, ey = horiz ? base : at(full), miss = full - sum(seg);
      const lens = ok ? '' : `<g class="lens fx fx-pop shake" style="--d:${d + 1.6};transform-origin:${ex + 90}px ${ey + 70}px">
        <line x1="${ex}" y1="${ey}" x2="${ex + 46}" y2="${ey + 30}"/><circle cx="${ex + 90}" cy="${ey + 70}" r="62"/>
        <path d="M${ex + 52} ${ey + 52}h76M${ex + 52} ${ey + 88}h76"/><text x="${ex + 90}" y="${ey + 78}">${miss} mm</text></g>`;
      return `<path class="dim draw${cls}" pathLength="1" d="${line}" style="--d:${d}"/><path class="tick fx${cls}" d="${ticks}" style="--d:${d + 0.9}"/>${lens}`;
    };
    const vx = ox + (+el.dataset.wall || 0) * k, vw = (+el.dataset.wallW || 0) * k;
    el.innerHTML = svg(w + 2 * ox, h + 2 * oy, `
      <rect class="wall draw" pathLength="1" x="${ox}" y="${oy}" width="${w}" height="${h}" style="--d:0"/>
      ${vw ? `<rect class="part fx fx-growy" x="${vx}" y="${oy}" width="${vw}" height="${h}" style="--d:.8"/>` : ''}
      ${chain('top', true, false, 0.3)}${chain('bottom', true, true, 0.5)}${chain('left', false, false, 0.7)}${chain('right', false, true, 0.9)}`);
  }

  /* gather: n small pieces on a grid, each knows the way to the centre */
  function gather(el) {
    const n = +el.dataset.n, cols = +el.dataset.cols || 6, s = 64, g = 22;
    const rows = Math.ceil(n / cols), W = cols * s + (cols - 1) * g, H = rows * s + (rows - 1) * g;
    el.style.width = `${W}px`; el.style.height = `${H}px`;
    el.innerHTML = Array.from({ length: n }, (_, i) => {
      const x = (i % cols) * (s + g), y = Math.floor(i / cols) * (s + g);
      return `<span class="gather piece" style="left:${x}px;top:${y}px;--i:${i};--to:translate(${W / 2 - s / 2 - x}px, ${H / 2 - s / 2 - y}px) scale(.4)">${i + 1}</span>`;
    }).join('');
  }

  // kind packs (morph-viz-diagrams.js) load before this file and register in window.sfVizKinds
  const kinds = Object.assign({ span, donut, plan, gather }, window.sfVizKinds);
  document.querySelectorAll('.viz[data-viz]').forEach((el) => {
    const make = kinds[el.dataset.viz];
    if (!make) return console.warn('sf-viz: unknown kind', el.dataset.viz);
    if (/\d/.test(['values', 'top', 'bottom', 'left', 'right'].map((k) => el.dataset[k] || '').join('')) && !el.dataset.source) console.warn('sf-viz: chart without data-source', el);
    make(el);
  });
})();
