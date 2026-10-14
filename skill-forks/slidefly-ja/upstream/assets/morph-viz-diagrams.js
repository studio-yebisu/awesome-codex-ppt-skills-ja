/* MORPH-SLIDES DIAGRAMS, pack 2: matrix, network, funnel, compare.
   Registers into window.sfVizKinds; load BEFORE morph-viz.js, which renders.
     <div class="viz" data-viz="matrix"  data-cols data-rows data-cells data-hot>
     <div class="viz" data-viz="network" data-hub data-nodes data-sub data-on data-off>
     <div class="viz" data-viz="funnel"  data-stages data-dots="p,0,1,p">
     <div class="viz" data-viz="compare"><div>before</div><div>after</div></div>   */
(() => {
  // data-* text is shown as text, never parsed as HTML ("<tên>" must stay visible)
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const list = (s) => (s || '').split('|').map(esc);
  const nums = (s) => (s || '').split(',').map((x) => x.trim()).filter(Boolean).map(Number).filter(Number.isFinite);
  const NS = 'http://www.w3.org/2000/svg';
  const d = (x) => x.toFixed(2);

  /* matrix: header row + row heads, cells pop in along the diagonal.
     data-hot = cell index (0-based) that the slide's click spotlights. */
  function matrix(el) {
    const cols = list(el.dataset.cols), rows = list(el.dataset.rows), cells = list(el.dataset.cells), hot = el.dataset.hot;
    el.style.gridTemplateColumns = `var(--mx-head, 280px) repeat(${cols.length}, 1fr)`;
    let h = '<span></span>' + cols.map((c, j) => `<b class="mx-col fx fx-up" style="--d:${d(0.1 * j)}">${c}</b>`).join('');
    rows.forEach((r, i) => {
      h += `<b class="mx-row fx fx-left" style="--d:${d(0.2 + 0.15 * i)}">${r}</b>`;
      cols.forEach((_, j) => {
        const k = i * cols.length + j;
        h += `<span class="mx-cell fx fx-pop${String(k) === hot ? ' hot' : ''}" style="--d:${d(0.45 + 0.15 * (i + j))}">${cells[k] || ''}</span>`;
      });
    });
    el.innerHTML = h;
  }

  /* network: hub in the middle, nodes on an ellipse, spokes draw out.
     data-on = nodes (1-based) a click keeps lit; data-off = nodes shown dashed. */
  function network(el) {
    const names = list(el.dataset.nodes), sub = list(el.dataset.sub), on = nums(el.dataset.on), off = nums(el.dataset.off);
    const W = el.clientWidth, H = el.clientHeight, cx = W / 2, cy = H / 2, rx = W / 2 - 190, ry = H / 2 - 70;
    const pts = names.map((_, i) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / names.length;
      return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)];
    });
    const cls = (i) => (on.includes(i + 1) ? ' on' : '') + (off.includes(i + 1) ? ' off' : '');
    const edges = pts.map(([x, y], i) => `<path class="edge ${off.includes(i + 1) ? 'fx' : 'draw'}${cls(i)}"${off.includes(i + 1) ? '' : ' pathLength="1"'} d="M${cx} ${cy}L${d(x)} ${d(y)}" style="--d:${d(0.3 + 0.08 * i)}"/>`).join('');
    const nodes = pts.map(([x, y], i) => `<div class="nd fx fx-pop${cls(i)}" style="left:${d(x)}px;top:${d(y)}px;--d:${d(0.7 + 0.08 * i)}"><b>${names[i]}</b><span>${sub[i] || ''}</span></div>`).join('');
    el.innerHTML = `<svg xmlns="${NS}" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${edges}</svg>${nodes}
      <div class="hub fx fx-pop" style="left:${cx}px;top:${cy}px;--d:.1">${esc(el.dataset.hub)}</div>`;
  }

  /* funnel: stacked layers narrowing down. Each dot falls from the top and
     stops where it is caught (layer index) or passes to the bottom ("p").
     The dots illustrate the idea only: they are not counts. */
  function funnel(el) {
    const st = list(el.dataset.stages), dots = (el.dataset.dots || '').split(',').map((x) => x.trim()).filter(Boolean);
    const W = el.clientWidth, H = el.clientHeight, n = st.length, lh = H / n, gap = 14, bot = W * 0.34;
    const wAt = (y) => W - ((W - bot) * y) / H;
    const poly = (i) => {
      const y0 = i * lh, y1 = (i + 1) * lh - gap, a = wAt(y0), b = wAt(y1);
      return `${d((W - a) / 2)},${d(y0)} ${d((W + a) / 2)},${d(y0)} ${d((W + b) / 2)},${d(y1)} ${d((W - b) / 2)},${d(y1)}`;
    };
    const layers = st.map((s, i) => `<polygon class="ly fx fx-up" points="${poly(i)}" style="--d:${d(0.15 * i)}"/>`).join('');
    const labels = st.map((s, i) => `<span class="ly-t fx fx-up" style="top:${d(i * lh + (lh - gap) / 2)}px;--d:${d(0.15 * i + 0.2)}">${s}</span>`).join('');
    const rest = {};
    const balls = dots.map((t, k) => {
      const i = t === 'p' ? n - 1 : +t, y = (i + 1) * lh - gap - 22;
      const slot = (rest[i] = (rest[i] || 0) + 1), w = wAt(y) - 120;
      const x = W / 2 + ((slot % 2 ? -1 : 1) * Math.ceil(slot / 2) * Math.min(56, w / 6));
      return `<i class="dot fx fx-from${t === 'p' ? '' : ' caught'}" style="left:${d(x)}px;top:${d(y)}px;--from:translateY(${d(-y - 80)}px);--d:${d(1 + 0.25 * k)}"></i>`;
    }).join('');
    el.innerHTML = `<svg xmlns="${NS}" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${layers}</svg>${labels}${balls}`;
  }

  /* compare: the "after" panel wipes over the "before" panel on the slide's click */
  function compare(el) {
    const [a, b] = el.children;
    a?.classList.add('cmp-a');
    b?.classList.add('cmp-b');
    el.insertAdjacentHTML('beforeend', '<i class="cmp-knob"></i>');
  }

  window.sfVizKinds = Object.assign(window.sfVizKinds || {}, { matrix, network, funnel, compare });
})();
