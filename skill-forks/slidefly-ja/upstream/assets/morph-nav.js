/* ===========================================================
   MORPH-SLIDES NAVIGATION (load after morph-engine.js)
   Keys: Right/Down/PageDown/Space/Enter = next,
         Left/Up/PageUp/Backspace = back, Home/End, F = fullscreen.
   Two edge buttons (left = back, right = next). Clicking the slide itself
   does nothing, so text can be selected and copied while presenting;
   the mouse wheel does not page either. One-finger swipe. Editing the
   #hash jumps to that slide.
   =========================================================== */
(() => {
  const deck = window.deck;
  if (!deck) return;
  const isEditable = (t) => t.closest?.('a, button, input, textarea, select, [contenteditable]');

  addEventListener('keydown', (e) => {
    // leave browser shortcuts alone (Ctrl+F, Alt+Left, ...)
    if (e.ctrlKey || e.metaKey || e.altKey || isEditable(e.target)) return;
    const k = e.key;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(k)) { e.preventDefault(); deck.next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); deck.prev(); }
    else if (k === 'Home') deck.go(0);
    else if (k === 'End') deck.go(deck.count - 1);
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen?.();
    }
  });

  // edge buttons live outside the stage; screenshots by automated browsers leave them out
  if (!navigator.webdriver) {
    [['prev', '\u2039', 'Slide trước'], ['next', '\u203A', 'Slide sau']].forEach(([dir, mark, label]) => {
      const b = Object.assign(document.createElement('button'), { className: `deck-edge ${dir}`, type: 'button' });
      b.setAttribute('aria-label', label);
      b.innerHTML = `<span aria-hidden="true">${mark}</span>`;
      b.addEventListener('mousedown', (e) => e.preventDefault()); // keep focus off, so Space/Enter still page
      b.addEventListener('click', () => deck[dir]());
      document.body.append(b);
    });
  }

  let touch = null;
  addEventListener('touchstart', (e) => {
    touch = e.touches.length === 1 ? { x: e.touches[0].clientX, y: e.touches[0].clientY } : null;
  }, { passive: true });
  addEventListener('touchend', (e) => {
    if (!touch || e.touches.length) { touch = null; return; } // pinch / multi-finger: ignore
    const dx = e.changedTouches[0].clientX - touch.x;
    const dy = e.changedTouches[0].clientY - touch.y;
    touch = null;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 50) return;
    const forward = Math.abs(dx) > Math.abs(dy) ? dx < 0 : dy < 0;
    (forward ? deck.next : deck.prev)();
  });

  addEventListener('hashchange', () => {
    const n = parseInt(location.hash.slice(1), 10);
    if (n) deck.go(n - 1);
  });
})();
