/* MORPH-SLIDES MOCKS: timing for morph-mock.css. Load after the slides.
   Inside each .mock, units (.msg, .type, .lines) play one after another;
   the chain restarts in every data-step, because a click resets the clock.
   .type  -> each letter becomes <span class="ch" style="--k:n">; typing
             speed adapts so a long prompt still types in about 2.6 s.
   .lines -> each child gets --j (line order); .think adds the dots first.
   Every unit gets --d0 = when it starts, in seconds after its trigger. */
(() => {
  const SPEED = 0.035;  // s per letter for short texts
  const MAX = 2.6;      // s: longest typing time
  const LINE = 0.35;    // s between two lines (matches --line-gap)
  const THINK = 0.9;    // s of "..." before the lines (matches --think-t)
  const GAP = 0.25;     // s pause between two units

  /* wrap every letter in a span; keeps inline tags such as <b> and <code> */
  function split(el) {
    const nodes = [];
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) nodes.push(walker.currentNode);
    // pre / pre-wrap text keeps its line breaks (a prompt someone will copy)
    const raw = getComputedStyle(el).whiteSpace.startsWith('pre');
    let k = 0;
    nodes.forEach((node) => {
      const text = node.textContent.normalize('NFC');
      if (!raw && !text.trim()) return;
      const frag = document.createDocumentFragment();
      for (const c of raw ? text : text.replace(/\s+/g, ' ')) {
        const s = document.createElement('span');
        s.className = 'ch';
        s.style.setProperty('--k', k++);
        s.textContent = c;
        frag.append(s);
      }
      node.replaceWith(frag);
    });
    return k;
  }

  document.querySelectorAll('.mock').forEach((mock) => {
    if (mock.parentElement?.closest('.mock')) return;      // a chat inside a phone is timed with the phone
    const clock = new Map();                                // step -> seconds used so far
    mock.querySelectorAll('.msg, .type, .lines').forEach((u) => {
      const key = u.closest('[data-step]')?.dataset.step || '0';
      let t = clock.get(key) || 0;
      u.style.setProperty('--d0', `${t.toFixed(2)}s`);
      const typed = u.classList.contains('type');
      const lined = u.classList.contains('lines');
      if (typed && !u.querySelector('.ch')) {
        const n = split(u);
        const per = Math.min(SPEED, MAX / Math.max(n, 1));
        u.style.setProperty('--per', `${per.toFixed(4)}s`);
        t += n * per + GAP;
      }
      if (lined) {
        if (u.classList.contains('think') && !u.querySelector(':scope > .dots')) {
          const dots = Object.assign(document.createElement('span'), { className: 'dots', innerHTML: '<i></i><i></i><i></i>' });
          dots.setAttribute('aria-hidden', 'true');
          u.prepend(dots);
          t += THINK;
        }
        const kids = [...u.children].filter((c) => !c.classList.contains('dots'));
        kids.forEach((c, j) => c.style.setProperty('--j', j));
        t += kids.length * LINE + GAP;
      }
      if (!typed && !lined && !u.querySelector('.type, .lines')) t += 2 * GAP; // a plain bubble
      clock.set(key, t);
    });
  });
})();
