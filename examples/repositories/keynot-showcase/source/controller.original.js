// Fullscreen
  function toggleFS() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      document.getElementById('fsBtn').innerHTML = '&#x2715;';
    } else {
      document.exitFullscreen();
      document.getElementById('fsBtn').innerHTML = '&#x26F6;';
    }
  }
  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement)
      document.getElementById('fsBtn').innerHTML = '&#x26F6;';
  });

  // Deep-link & session persistence helpers
  function parseHash() {
    const m = location.hash.match(/^#slide-(\d+)$/);
    if (!m) return -1;
    const idx = parseInt(m[1], 10) - 1;
    return (idx >= 0 && idx < document.querySelectorAll('.slide').length) ? idx : -1;
  }
  function initialSlide() {
    const fromHash = parseHash();
    if (fromHash >= 0) return fromHash;
    const stored = sessionStorage.getItem('keynot-slide');
    if (stored !== null) {
      const idx = parseInt(stored, 10);
      if (idx >= 0 && idx < document.querySelectorAll('.slide').length) return idx;
    }
    return 0;
  }
  function persistSlide(idx) {
    sessionStorage.setItem('keynot-slide', idx);
    history.replaceState(null, '', '#slide-' + (idx + 1));
  }

  // Navigation
  const slides = document.querySelectorAll('.slide');
  const dotsEl = document.getElementById('dots');
  const counter = document.getElementById('counter');
  let cur = initialSlide();

  // Clear default active class, then activate the correct slide
  slides.forEach(s => s.classList.remove('active'));

  slides.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'dot';
    d.addEventListener('click', () => go(i));
    dotsEl.appendChild(d);
  });

  slides[cur].classList.add('active');
  dotsEl.children[cur].classList.add('active');
  counter.textContent = `${cur + 1} / ${slides.length}`;
  persistSlide(cur);

  function go(n) {
    slides[cur].classList.remove('active');
    dotsEl.children[cur].classList.remove('active');
    cur = (n + slides.length) % slides.length;
    slides[cur].classList.add('active');
    dotsEl.children[cur].classList.add('active');
    counter.textContent = `${cur + 1} / ${slides.length}`;
    persistSlide(cur);
  }

  window.addEventListener('hashchange', () => {
    const idx = parseHash();
    if (idx >= 0 && idx !== cur) go(idx);
  });

  document.getElementById('next').addEventListener('click', () => go(cur + 1));
  document.getElementById('prev').addEventListener('click', () => go(cur - 1));

  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') go(cur + 1);
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                     go(cur - 1);
    if (e.key === 'f' || e.key === 'F') toggleFS();
  });

  // Auto-hide nav
  const nav = document.querySelector('.nav');
  let hideTimer;
  function showNav() {
    nav.classList.remove('nav-hidden');
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => nav.classList.add('nav-hidden'), 1800);
  }
  document.addEventListener('mousemove', showNav);
  document.addEventListener('touchstart', showNav, { passive: true });
  document.addEventListener('keydown', showNav);
  showNav();

  // Swipe
  let tx = 0;
  document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 50) go(dx < 0 ? cur + 1 : cur - 1);
  }, { passive: true });
