// Gallery runtime: language switch, preview playback, still cycling, copy button, moves filter.
(() => {
  const root = document.documentElement;
  const store = {
    get: (k) => {
      try {
        return localStorage.getItem(k);
      } catch {
        return null;
      }
    },
    set: (k, v) => {
      try {
        localStorage.setItem(k, v);
      } catch {
        /* private mode */
      }
    },
  };

  function setLang(lang) {
    root.dataset.lang = lang;
    root.lang = lang;
    store.set('scrolline-lang', lang);
    const t = document.querySelector('meta[name="sl-title-' + lang + '"]');
    if (t) document.title = t.content;
    for (const el of document.querySelectorAll('[data-ph-' + lang + ']'))
      el.placeholder = el.getAttribute('data-ph-' + lang);
  }
  const fromUrl = new URLSearchParams(location.search).get('lang');
  const saved = store.get('scrolline-lang');
  const guess = (navigator.language || 'en').toLowerCase().startsWith('ko') ? 'ko' : 'en';
  setLang(['ko', 'en'].includes(fromUrl) ? fromUrl : saved || guess);
  for (const b of document.querySelectorAll('.lang [data-set]'))
    b.addEventListener('click', () => setLang(b.dataset.set));

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Previews only run while on screen.
  const cyclers = new Map();
  function cycler(box) {
    const imgs = [...box.querySelectorAll('img')];
    let i = 0;
    let timer = 0;
    const period = Number(box.dataset.period || 1800);
    return {
      start() {
        if (timer || imgs.length < 2 || reduce) return;
        timer = setInterval(() => {
          imgs[i].classList.remove('on');
          i = (i + 1) % imgs.length;
          const next = imgs[i];
          if (next.dataset.src) {
            next.src = next.dataset.src;
            delete next.dataset.src;
          }
          next.classList.add('on');
        }, period);
      },
      stop() {
        clearInterval(timer);
        timer = 0;
      },
    };
  }
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        const el = e.target;
        if (el.tagName === 'VIDEO') {
          if (e.isIntersecting && !reduce) el.play().catch(() => {});
          else el.pause();
        } else {
          if (!cyclers.has(el)) cyclers.set(el, cycler(el));
          cyclers.get(el)[e.isIntersecting ? 'start' : 'stop']();
        }
      }
    },
    { threshold: 0.25 },
  );
  for (const v of document.querySelectorAll('.preview video')) io.observe(v);
  for (const s of document.querySelectorAll('.preview.stills')) io.observe(s);

  // Copy the quick-start lines.
  for (const btn of document.querySelectorAll('.copy')) {
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy || '';
      try {
        await navigator.clipboard.writeText(text);
      } catch {
        const ta = Object.assign(document.createElement('textarea'), { value: text });
        document.body.append(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
      }
      btn.classList.add('done');
      setTimeout(() => btn.classList.remove('done'), 1400);
    });
  }

  // Moves filter: family chip + text query, mirrored into the URL hash.
  const list = document.querySelector('.moves');
  if (list) {
    const rows = [...list.querySelectorAll('.move')];
    const chips = [...document.querySelectorAll('.filters [data-family]')];
    const input = document.querySelector('.search input');
    const count = document.querySelector('.count [data-n]');
    const none = document.querySelector('.none');
    let family = (location.hash.match(/family=([a-z]+)/) || [])[1] || 'all';
    function apply() {
      const q = (input.value || '').trim().toLowerCase();
      let n = 0;
      for (const r of rows) {
        const show =
          (family === 'all' || r.dataset.family === family) && (!q || r.dataset.search.includes(q));
        r.hidden = !show;
        if (show) n += 1;
      }
      for (const c of chips) c.setAttribute('aria-pressed', String(c.dataset.family === family));
      count.textContent = String(n);
      none.hidden = n > 0;
    }
    for (const c of chips)
      c.addEventListener('click', () => {
        family = c.dataset.family;
        history.replaceState(
          null,
          '',
          family === 'all' ? location.pathname + location.search : '#family=' + family,
        );
        apply();
      });
    input.addEventListener('input', apply);
    apply();
  }
})();
