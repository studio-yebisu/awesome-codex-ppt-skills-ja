/* MORPH-SLIDES STEPS: click-by-click build. Load after morph-engine.js.
   Elements with data-step="n" wait for the n-th "next" on their slide;
   the slide gets data-at="<steps shown>" so CSS can style each state.
   "Back" first takes the last shown step away (its effect plays in reverse),
   then goes to the previous slide, which arrives finished. Automated browsers
   (deck.audit()) always see every step. */
(() => {
  const deck = window.deck;
  const stage = document.querySelector('.deck-stage');
  if (!deck || !stage) return;
  const slides = [...stage.querySelectorAll(':scope > .slide')];
  const auto = navigator.webdriver;
  const last = (s) => Math.max(0, ...[...s.querySelectorAll('[data-step]')].map((e) => +e.dataset.step || 0));
  const show = (s, n) => {
    s.dataset.at = n;
    s.querySelectorAll('[data-step]').forEach((e) => e.classList.toggle('pending', +e.dataset.step > n));
  };
  const enter = () => {
    const s = slides[deck.index];
    if (s) show(s, auto || stage.dataset.dir === 'back' ? last(s) : 0);
  };
  const { next, prev, go } = deck;
  deck.next = () => {
    const s = slides[deck.index];
    if (!s) return next();
    const at = +s.dataset.at || 0;
    if (at < last(s)) show(s, at + 1); else { next(); enter(); }
  };
  deck.prev = () => {
    const s = slides[deck.index];
    const at = +s?.dataset.at || 0;
    if (s && at > 0) show(s, at - 1); else { prev(); enter(); }
  };
  deck.go = (n) => { go(n); enter(); };
  slides.forEach((s) => show(s, auto ? last(s) : 0));
  new MutationObserver(enter).observe(stage, { attributes: true, attributeFilter: ['data-slide'] });
})();
