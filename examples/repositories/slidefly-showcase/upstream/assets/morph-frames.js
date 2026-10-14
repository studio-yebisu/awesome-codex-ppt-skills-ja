/* MORPH-SLIDES FRAMES (pairs with morph-frames.css). Load before morph-engine.js.
   - adds the .frame-panel element a frame draws its colour block with (appended, so the
     title stays :first-child), aria-hidden;
   - marks text lying on an accent panel (.on-panel) so it takes --on-accent;
   - frames with a panel get a clear stage unless the slide sets data-stage: the panel is the decoration. */
(() => {
  const PANEL = ['split-left', 'split-right', 'poster', 'band', 'rail', 'bottom', 'stack', 'corner', 'diagonal', 'frame', 'media-left', 'media-right', 'magazine', 'spotlight'];
  const ON_PANEL = { 'split-left': '.highlight', 'split-right': '.highlight', diagonal: '.highlight' };
  document.querySelectorAll('.deck-stage > .slide[data-frame]').forEach((slide) => {
    const frame = slide.dataset.frame;
    if (PANEL.includes(frame) && !slide.querySelector(':scope > .frame-panel')) {
      const panel = Object.assign(document.createElement('div'), { className: 'frame-panel' });
      panel.setAttribute('aria-hidden', 'true');
      slide.append(panel);
      if (!slide.dataset.stage) slide.dataset.stage = 'clear';
    }
    if (frame === 'stairs' && !slide.dataset.stage) slide.dataset.stage = 'clear';   // the steps run into the zone actors use
    if (ON_PANEL[frame]) slide.querySelectorAll(ON_PANEL[frame]).forEach((el) => el.classList.add('on-panel'));
  });
})();
