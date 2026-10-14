(() => {
  document.documentElement.classList.add('js');

  const STAGE_WIDTH = 1600;
  const STAGE_HEIGHT = 900;
  const stage = document.querySelector('#stage');
  const slides = [...document.querySelectorAll('.slide')];
  const current = document.querySelector('[data-current]');
  const total = document.querySelector('[data-total]');
  const step = document.querySelector('[data-step]');
  const progress = document.querySelector('[data-progress]');
  const revealedCounts = slides.map(() => 0);
  let index = 0;

  if (!stage || slides.length === 0) return;

  const clamp = (value) => Math.max(0, Math.min(value, slides.length - 1));
  const fragmentsFor = (slideIndex) => [...slides[slideIndex].querySelectorAll('.fragment')];

  const slideIndexFromHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const found = slides.findIndex((slide) => slide.dataset.slideId === id);
    return found >= 0 ? found : 0;
  };

  const syncFragments = (slideIndex) => {
    const fragments = fragmentsFor(slideIndex);
    const revealed = Math.max(0, Math.min(revealedCounts[slideIndex], fragments.length));
    revealedCounts[slideIndex] = revealed;
    fragments.forEach((fragment, fragmentIndex) => {
      const visible = fragmentIndex < revealed;
      fragment.classList.toggle('is-revealed', visible);
      fragment.setAttribute('aria-hidden', String(!visible));
    });
    if (slideIndex === index && step) {
      step.textContent = fragments.length > 0 ? `· ${revealed} / ${fragments.length}` : '';
    }
  };

  const render = (nextIndex, updateHash = true) => {
    index = clamp(nextIndex);
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === index;
      slide.classList.toggle('is-active', active);
      slide.hidden = !active;
      slide.setAttribute('aria-hidden', String(!active));
      syncFragments(slideIndex);
    });

    if (current) current.textContent = String(index + 1);
    if (total) total.textContent = String(slides.length);
    if (progress) progress.style.width = `${((index + 1) / slides.length) * 100}%`;
    if (updateHash) history.replaceState(null, '', `#${encodeURIComponent(slides[index].dataset.slideId)}`);
  };

  const advance = () => {
    const fragments = fragmentsFor(index);
    if (revealedCounts[index] < fragments.length) {
      revealedCounts[index] += 1;
      syncFragments(index);
      return;
    }
    if (index < slides.length - 1) render(index + 1);
  };

  const retreat = () => {
    if (revealedCounts[index] > 0) {
      revealedCounts[index] -= 1;
      syncFragments(index);
      return;
    }
    if (index > 0) {
      const previousIndex = index - 1;
      revealedCounts[previousIndex] = fragmentsFor(previousIndex).length;
      render(previousIndex);
    }
  };

  const resize = () => {
    const scale = Math.min(innerWidth / STAGE_WIDTH, innerHeight / STAGE_HEIGHT);
    stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
  };

  const isInteractiveTarget = (target) => Boolean(target.closest('a, button, input, textarea, select, [contenteditable="true"]'));

  addEventListener('keydown', (event) => {
    if (isInteractiveTarget(event.target)) return;
    if (['ArrowRight', 'PageDown', ' '].includes(event.key)) {
      event.preventDefault();
      advance();
    } else if (['ArrowLeft', 'PageUp'].includes(event.key)) {
      event.preventDefault();
      retreat();
    } else if (event.key === 'Home') {
      event.preventDefault();
      revealedCounts[0] = 0;
      render(0);
    } else if (event.key === 'End') {
      event.preventDefault();
      revealedCounts[slides.length - 1] = 0;
      render(slides.length - 1);
    }
  });

  document.querySelector('[data-action="previous"]')?.addEventListener('click', retreat);
  document.querySelector('[data-action="next"]')?.addEventListener('click', advance);
  document.querySelector('[data-action="fullscreen"]')?.addEventListener('click', async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await document.documentElement.requestFullscreen();
    } catch (error) {
      console.warn('Unable to toggle fullscreen mode.', error);
    }
  });

  addEventListener('hashchange', () => render(slideIndexFromHash(), false));
  addEventListener('resize', resize);
  resize();
  render(slideIndexFromHash(), false);
})();
