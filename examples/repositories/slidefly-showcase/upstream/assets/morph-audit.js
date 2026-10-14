/* ===========================================================
   MORPH-SLIDES AUDIT: how well each slide fills space. Run in the console or a test tool: deck.audit()
   - biggest empty band (gapY/gapX) and ink past the safe margins; display slides only for overflow.
   - charts carry data-source; at most 6 icons, none missing; photo slides credit their picture.
   - text under 3:1 (WCAG) against the solid actor or its own box below it: "chữ khó đọc trên hình".
   - 3 inner slides in a row with the same look (layout, pose, diagrams, verbs) = monotone.
   - whole deck (8+ inner slides): one skeleton (kind, frame, title mode, body blocks) at most
     max(3, 20%) times; 10+ inner slides use at least 3 frames.
   Run it outside a live talk: it briefly shows steps not yet clicked.
   =========================================================== */
(() => {
  const stage = document.querySelector('.deck-stage');
  if (!stage || !window.deck) return;
  const SAFE = { x0: 80, x1: 1840, y0: 60, y1: 1020 };
  const LIMIT = { gapY: 0.28, gapX: 0.3 };
  // big-number slides are meant to breathe around the figures
  const LIMIT_Y_BY_LAYOUT = { stats: 0.34, bento: 0.34, process: 0.38, 'before-after': 0.38 };   // airy by design
  const DISPLAY = ['cover', 'section', 'quote', 'closing', 'photo', 'big-number', 'qa', 'portrait-quote', 'chapter', 'statement', 'cta', 'split-photo', 'free'];

  /* text line boxes + images/svg, in stage coordinates */
  function inkRects(slide) {
    const s = stage.getBoundingClientRect();
    const k = s.width / 1920;
    const out = [];
    const push = (r) => r.width >= 1 && r.height >= 1 && out.push({ x0: (r.left - s.left) / k, x1: (r.right - s.left) / k, y0: (r.top - s.top) / k, y1: (r.bottom - s.top) / k });
    const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!node.textContent.trim() || node.parentElement.closest('[aria-hidden="true"]')) continue;   // decoration (chapter numeral)
      const range = document.createRange(); range.selectNodeContents(node);
      [...range.getClientRects()].forEach(push);
    }
    slide.querySelectorAll(':is(img, svg, video, canvas):not(.photo-bg, .split-img, svg[aria-hidden="true"])').forEach((el) => push(el.getBoundingClientRect()));
    // decorative art of two-layer styles (svg aria-hidden) may bleed off the edge on purpose: count it, clipped to the safe area
    slide.querySelectorAll('svg[aria-hidden="true"]').forEach((el) => { if (el.parentElement.closest('svg')) return; if (push(el.getBoundingClientRect())) { const o = out.at(-1); o.x0 = Math.max(o.x0, SAFE.x0); o.x1 = Math.min(o.x1, SAFE.x1); o.y0 = Math.max(o.y0, SAFE.y0); o.y1 = Math.min(o.y1, SAFE.y1); } });
    // a frame's colour block fills space on purpose and may bleed off the edge: count it, clipped to the safe area
    slide.querySelectorAll('.frame-panel').forEach((el) => { if (push(el.getBoundingClientRect())) { const o = out.at(-1); o.x0 = Math.max(o.x0, SAFE.x0); o.x1 = Math.min(o.x1, SAFE.x1); o.y0 = Math.max(o.y0, SAFE.y0); o.y1 = Math.min(o.y1, SAFE.y1); } });
    return out;
  }

  /* solid actors in the pose this slide would have (same attributes the engine sets) */
  function actorRects(slide, k, s) {
    Object.assign(stage.dataset, {
      layout: slide.dataset.stage || slide.dataset.layout || 'content', pose: slide.dataset.pose || '',
      parity: slide.dataset.pose ? 'none' : slide.dataset.parity, variant: slide.dataset.variant,
    });
    window.deck.ink?.();   // text colour on accent fills follows this slide's accent
    return [...stage.querySelectorAll('.actor')].flatMap((a) => {
      const cs = getComputedStyle(a);
      // soft glows, faint shapes and masked/clipped drawings (pins: the box is not the shape) are skipped
      const soft = (/radial-gradient/.test(cs.backgroundImage) && clear(cs.backgroundColor)) || /blur/.test(cs.filter) || +cs.opacity < 0.6
        || cs.maskImage !== 'none' || cs.webkitMaskImage !== 'none' || cs.clipPath !== 'none';
      const fill = soft ? null : fillLum(cs);
      const r = a.getBoundingClientRect();
      if (fill === null || r.width / k < 24 || r.height / k < 24) return [];
      return [{ name: a.dataset.actor, lum: fill, x0: (r.left - s.left) / k, x1: (r.right - s.left) / k, y0: (r.top - s.top) / k, y1: (r.bottom - s.top) / k }];
    });
  }

  /* brightness of what a shape paints: its plain fill (paper with grain counts as paper), or an
     opaque gradient (sticky notes). Patterns with see-through stops (grid lines) and pictures cover nothing. */
  function fillLum(cs) {
    const rgbs = (str) => [...str.matchAll(/rgba?\(([^)]+)\)/g)].map((m) => m[1].split(/[\s,/]+/).map(Number));
    if (!clear(cs.backgroundColor)) return lum(rgbs(cs.backgroundColor)[0]);
    const img = cs.backgroundImage;
    // one gradient layer stretched over the whole shape; tiles, corners and multi-layer drawings are patterns
    if (!/^linear-gradient/.test(img) || /url\(|transparent/.test(img) || (img.match(/gradient\(/g) || []).length > 1) return null;
    if (!/^(auto( auto)?|100% 100%|cover)$/.test(cs.backgroundSize)) return null;
    const stops = rgbs(img);
    if (!stops.length || stops.some((c) => c.length > 3 && c[3] < 0.9)) return null;
    return stops.reduce((sum, c) => sum + lum(c), 0) / stops.length;
  }

  /* WCAG relative luminance and contrast ratio */
  const lum = ([r, g, b]) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; })
    .reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
  const ratio = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  const clear = (c) => c === 'transparent' || /rgba\(.*,\s*0(\.0*[0-2]\d*)?\)$/.test(c);
  /* text on its own box (card, band, window, or a filled shape of a drawn diagram) is shielded from the actors behind */
  const boxed = (e) => { const cs = getComputedStyle(e); return e instanceof SVGGeometryElement ? !/none/.test(cs.fill) && !clear(cs.fill) && +cs.fillOpacity > 0.5 : !clear(cs.backgroundColor) || /gradient|url\(/.test(cs.backgroundImage); };
  const boxOf = (el, slide) => { for (let e = el; e && e !== slide; e = e.parentElement) if (boxed(e)) return e; return null; };
  // ...but the box itself must contrast with its text: an opaque plain fill is measured (tints, gradients, pictures are not)
  const boxLum = (e) => { const c = rgbOf(getComputedStyle(e).backgroundColor); return c && (c[3] ?? 1) >= 0.9 ? lum(c) : null; };
  // computed colours come as rgb(0-255) or, from color-mix(), as color(srgb 0-1 0-1 0-1 / a)
  function rgbOf(c) { const m = c.match(/color\(srgb ([^)]+)\)/); if (!m) return c.match(/[\d.]+/g)?.map(Number); const v = m[1].split(/[\s/]+/).map(Number); return [v[0] * 255, v[1] * 255, v[2] * 255, v[3] ?? 1]; }

  /* text that ends the slide hidden (pieces gathered away, opacity 0) is not read */
  const faded = (el, slide) => {
    let o = 1; for (let e = el; e && e !== slide; e = e.parentElement) o *= +getComputedStyle(e).opacity;
    return o < 0.2 || getComputedStyle(el).visibility === 'hidden'; };

  /* text lines lying (even partly) on a solid actor of too similar a brightness */
  function crossings(slide) {
    const s = stage.getBoundingClientRect();
    const k = s.width / 1920;
    // styles may pose actors by what the active slide holds (:has(.slide.active .takeaway))
    const was = stage.querySelector(':scope > .slide.active');
    was?.classList.remove('active');
    slide.classList.add('active');
    const shapes = slide.querySelector('.photo-bg') ? [] : actorRects(slide, k, s);   // a full-bleed photo hides the actors
    const hits = new Map();   // actor -> first text found on it
    const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (!node.textContent.trim() || node.parentElement.closest('.mock, svg') || faded(node.parentElement, slide)) continue;
      const tcs = getComputedStyle(node.parentElement);
      if (parseFloat(tcs.webkitTextStrokeWidth) > 0 || tcs.textShadow !== 'none') continue; // outlined text carries its own contrast
      const ink = lum(rgbOf(tcs.color));
      const need = parseFloat(tcs.fontSize) >= 60 ? 2.4 : 3;   // very large type stays readable at lower contrast
      const box = boxOf(node.parentElement, slide), bl = box && boxLum(box);
      if (box && bl !== null && ratio(ink, bl) < need) hits.set(`nền ${String(box.className.baseVal ?? box.className).split(' ')[0] || box.tagName.toLowerCase()}`, node.textContent.trim().slice(0, 24));
      if (box) continue;
      const range = document.createRange(); range.selectNodeContents(node);
      [...range.getClientRects()].forEach((r) => {
        const l = { x0: (r.left - s.left) / k, x1: (r.right - s.left) / k, y0: (r.top - s.top) / k, y1: (r.bottom - s.top) / k };
        const area = (l.x1 - l.x0) * (l.y1 - l.y0);
        if (area < 50) return;
        // three points along the line; under each, only the topmost actor (DOM order = z-order) counts
        const y = (l.y0 + l.y1) / 2;
        [0.1, 0.5, 0.9].forEach((f) => {
          const x = l.x0 + (l.x1 - l.x0) * f;
          // a box of the slide under the text (pill, band, card drawn in the slide) shields it
          if (document.elementsFromPoint(s.left + x * k, s.top + y * k).some((e) => e !== slide && slide.contains(e) && boxed(e))) return;
          const top = shapes.findLast((a) => x > a.x0 && x < a.x1 && y > a.y0 && y < a.y1);
          if (top && ratio(ink, top.lum) < need && !hits.has(top.name)) hits.set(top.name, node.textContent.trim().slice(0, 24));
        });
      });
    }
    slide.classList.remove('active');
    was?.classList.add('active');
    return [...hits].map(([name, text]) => `${name} ("${text}")`);
  }

  /* biggest uncovered interval of [lo, hi] given covered spans */
  function maxGap(spans, lo, hi) {
    const sorted = spans.map(([a, b]) => [Math.max(a, lo), Math.min(b, hi)]).filter(([a, b]) => b > a).sort((p, q) => p[0] - q[0]);
    let gap = 0, cursor = lo;
    for (const [a, b] of sorted) { gap = Math.max(gap, a - cursor); cursor = Math.max(cursor, b); }
    return Math.max(gap, hi - cursor);
  }

  function auditSlide(slide, i) {
    const layout = slide.dataset.kind || slide.dataset.layout || 'content';   // new layouts report their own name
    const ink = inkRects(slide);
    const issues = [];
    const out = ink.filter((r) => r.x0 < SAFE.x0 - 40 || r.x1 > SAFE.x1 + 40 || r.y0 < SAFE.y0 - 30 || r.y1 > SAFE.y1 + 30);
    if (out.length) issues.push(`tràn khung (${out.length} dòng)`);
    // text overflow = a text line box past its container (decorative pseudo-elements are ignored)
    slide.querySelectorAll('.col, .takeaway, .highlight').forEach((box) => {
      const b = box.getBoundingClientRect();
      const range = document.createRange();
      range.selectNodeContents(box);
      const past = [...range.getClientRects()].some((r) => r.height && (r.bottom > b.bottom + 2 || r.right > b.right + 2));
      if (past) issues.push(`chữ tràn hộp .${box.className.split(' ')[0]}`);
    });
    slide.querySelectorAll('.viz[data-viz]').forEach((v) => {
      if (/\d/.test(['values', 'top', 'bottom', 'left', 'right'].map((k) => v.dataset[k] || '').join('')) && !v.dataset.source) issues.push(`biểu đồ ${v.dataset.viz} thiếu data-source`);
    });
    if (slide.querySelector('.photo-bg, .split-img') && !slide.querySelector('.photo-credit')) issues.push('ảnh thiếu .photo-credit (tác giả, nguồn, giấy phép)');
    const icons = slide.querySelectorAll('.ico');
    if (icons.length > 6) issues.push(`quá nhiều icon (${icons.length}, tối đa 6)`);
    const lost = [...slide.querySelectorAll('.ico[data-missing]')].map((e) => e.dataset.icon);
    if (lost.length) issues.push(`icon không tồn tại: ${lost.join(', ')}`);
    const cut = crossings(slide);
    if (cut.length) issues.push(`chữ khó đọc trên hình ${cut.join(', ')}`);
    const gapY = maxGap(ink.map((r) => [r.y0, r.y1]), SAFE.y0, SAFE.y1) / (SAFE.y1 - SAFE.y0);
    const gapX = maxGap(ink.map((r) => [r.x0, r.x1]), SAFE.x0, SAFE.x1) / (SAFE.x1 - SAFE.x0);
    const display = DISPLAY.includes(layout);
    if (!display && gapY > (slide.dataset.frame === 'spotlight' ? 0.38 : LIMIT_Y_BY_LAYOUT[layout] || LIMIT.gapY)) issues.push(`trống dọc ${Math.round(gapY * 100)}%`);
    if (!display && gapX > (slide.dataset.frame === 'stairs' ? 0.42 : LIMIT.gapX)) issues.push(`trống ngang ${Math.round(gapX * 100)}%`);
    return {
      slide: i + 1, layout, density: slide.dataset.density || '',
      gapY: `${Math.round(gapY * 100)}%`, gapX: `${Math.round(gapX * 100)}%`,
      status: issues.length ? 'SỬA' : 'OK', issues: issues.join('; '),
    };
  }

  /* look of a slide = what the eye recognises: layout, pose, diagram and mock kinds, motion verbs */
  const VERB = /^(fx-[a-z]+|draw|count|slam|shake|strike|ping|travel|gather)$/;
  function lookOf(slide) {
    const kinds = [...slide.querySelectorAll('.viz[data-viz]')].map((v) => v.dataset.viz)
      .concat([...slide.querySelectorAll('.mock')].map((m) => [...m.classList].find((c) => c.startsWith('mock-')) || 'mock')).sort();
    const verbs = new Set([...slide.querySelectorAll('[class]')].flatMap((e) => [...e.classList].filter((c) => VERB.test(c))));
    return [slide.dataset.kind || slide.dataset.layout || 'content', slide.dataset.pose || '', slide.dataset.frame || '', kinds.join('+'), [...verbs].sort().join('+')].join('|');
  }

  /* skeleton = what the eye reads as "that slide again", whatever the words, colours or motion verbs */
  const BODY = ['bullets', 'cols', 'stats', 'timeline', 'agenda-list', 'bento', 'process', 'ctable', 'ba', 'countdown', 'ico-grid', 'viz', 'mock', 'highlight'];
  function skeletonOf(slide) {
    const vizKinds = [...new Set([...slide.querySelectorAll('.viz[data-viz]')].map((v) => v.dataset.viz))].sort().join(',');   // a funnel and a matrix look different; mock windows do not
    const body = BODY.filter((c) => slide.querySelector('.' + c)).map((c) => (c === 'viz' && vizKinds ? `viz:${vizKinds}` : c)).join('+');
    // no standard block: a hand-drawn figure (venn, axis, pipe...) is its own look, named by its first element's class
    const own = body ? '' : [...slide.children].find((c) => !c.matches('.title, .frame-panel, [aria-hidden="true"]'))?.classList[0] || 'text';
    return [slide.dataset.kind || slide.dataset.layout || 'content', slide.dataset.frame || 'no-frame', slide.dataset.title || 'top', body || own].join(' | ');
  }
  function deckRepeats(report, slides) {
    const inner = report.map((r, i) => i).filter((i) => !DISPLAY.includes(report[i].layout));
    const n = inner.length;
    const flag = (i, msg) => { const r = report[i]; r.issues = [r.issues, msg].filter(Boolean).join('; '); r.status = 'SỬA'; };
    if (n >= 8) {
      const cap = Math.max(3, Math.ceil(n * 0.2)), seen = {};
      inner.forEach((i) => {
        const k = skeletonOf(slides[i]);
        seen[k] = (seen[k] || 0) + 1;
        if (seen[k] > cap) flag(i, `nhàm toàn deck: dáng "${k}" lần thứ ${seen[k]} (tối đa ${cap} trên ${n} slide trong)`);
      });
    }
    const framable = inner.filter((i) => report[i].layout !== 'diagram');   // a full-body diagram does not take a frame
    const frames = new Set(framable.map((i) => slides[i].dataset.frame).filter(Boolean));
    if (framable.length >= 10 && frames.size < 3) flag(framable[0], `ít khung: deck có ${framable.length} slide trong (không tính sơ đồ) mới dùng ${frames.size} khung (data-frame), nên dùng ít nhất 3`);
  }

  window.deck.audit = () => {
    stage.classList.add('auditing');
    const saved = { ...stage.dataset };
    const slides = [...stage.querySelectorAll(':scope > .slide')];
    const report = slides.map(auditSlide);
    const looks = slides.map(lookOf);
    report.forEach((r, i) => {
      if (i < 2 || DISPLAY.includes(r.layout) || looks[i] !== looks[i - 1] || looks[i] !== looks[i - 2]) return;
      r.issues = [r.issues, 'nhàm: giống hệt 2 slide trước'].filter(Boolean).join('; ');
      r.status = 'SỬA';
    });
    deckRepeats(report, slides);
    ['layout', 'pose', 'parity', 'variant'].forEach((key) => { stage.dataset[key] = saved[key] ?? ''; });
    window.deck.ink?.();
    stage.classList.remove('auditing');
    console.table(report);
    return report;
  };
})();
