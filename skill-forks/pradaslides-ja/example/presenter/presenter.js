(() => {
  'use strict';

  const fallbackDeck = {
    meta: { title: 'PradaSlides', status: 'draft', storageKey: 'pradaslides-empty' },
    design: {},
    slides: [{
      id: 'P01', role: 'cover', topology: 'stage', layout: 'hero-decision', tone: 'dark',
      density: 'air', title: 'Author the deck in deck.js', kicker: 'PRADASLIDES', html: '',
      notes: 'This scaffold is not a final presentation.', authoring: { incomplete: true },
    }],
  };
  const deck = window.PRADA_DECK && Array.isArray(window.PRADA_DECK.slides)
    ? window.PRADA_DECK
    : fallbackDeck;
  const slides = deck.slides.length ? deck.slides : fallbackDeck.slides;
  const stageWidth = Number(deck.design?.canvas?.width_px || 1600);
  const stageHeight = Number(deck.design?.canvas?.height_px || 900);
  const storageKey = deck.meta?.storageKey || `pradaslides:${slug(deck.meta?.title || 'deck')}`;
  const furnitureKeys = [
    ['kicker', 'Kicker'],
    ['pageNumber', 'Page number'],
    ['progress', 'Progress line'],
    ['frameCorners', 'Frame corners'],
    ['sectionRail', 'Section rail'],
    ['ghostMarker', 'Ghost marker'],
    ['metricStrip', 'Metric strip'],
    ['pageHint', 'Page-turn hint'],
    ['sourceLine', 'Source line'],
  ];
  const defaultFurniture = {
    kicker: true,
    pageNumber: true,
    progress: true,
    frameCorners: true,
    sectionRail: false,
    ghostMarker: false,
    metricStrip: false,
    pageHint: false,
    sourceLine: true,
  };
  const state = {
    index: 0,
    uiTheme: 'dark',
    panels: true,
    notes: true,
    overrides: {},
    ...loadState(),
  };
  state.index = clamp(Number(state.index) || 0, 0, slides.length - 1);
  const query = new URLSearchParams(window.location.search);
  const requestedSlide = Number(query.get('slide') || query.get('page'));
  const capturePresentation = query.get('present') === '1';
  if (Number.isFinite(requestedSlide) && requestedSlide > 0) {
    state.index = clamp(requestedSlide - 1, 0, slides.length - 1);
  }

  const dom = {
    console: document.getElementById('console'),
    deckTitle: document.getElementById('deck-title'),
    toolbarCounter: document.getElementById('toolbar-counter'),
    stageCounter: document.getElementById('stage-counter'),
    stageLabel: document.getElementById('stage-label'),
    stageSection: document.getElementById('stage-section'),
    slideCount: document.getElementById('slide-count'),
    thumbnails: document.getElementById('thumbnail-list'),
    activeSlide: document.getElementById('active-slide'),
    viewport: document.getElementById('stage-viewport'),
    scaler: document.getElementById('stage-scaler'),
    previous: document.getElementById('previous-button'),
    next: document.getElementById('next-button'),
    present: document.getElementById('present-button'),
    print: document.getElementById('print-button'),
    stateDownload: document.getElementById('state-button'),
    reset: document.getElementById('reset-button'),
    uiTheme: document.getElementById('ui-theme-button'),
    panels: document.getElementById('panels-button'),
    transition: document.getElementById('transition-select'),
    tone: document.getElementById('tone-control'),
    density: document.getElementById('density-control'),
    furniture: document.getElementById('furniture-controls'),
    notesToggle: document.getElementById('notes-toggle'),
    notes: document.getElementById('notes-copy'),
    slideMeta: document.getElementById('slide-meta'),
    printDeck: document.getElementById('print-deck'),
    live: document.getElementById('live-region'),
    draft: document.getElementById('draft-badge'),
  };

  applyDesignTokens();
  initialize();

  function initialize() {
    document.title = `${deck.meta?.title || 'PradaSlides'} — Presenter`;
    if (capturePresentation) document.body.classList.add('present-mode');
    if (deck.meta?.previewMode === 'render-parity') document.body.classList.add('render-preview-mode');
    dom.deckTitle.textContent = deck.meta?.title || 'PradaSlides';
    if (dom.stageLabel) dom.stageLabel.textContent = deck.meta?.stageLabel || deck.meta?.title || 'PradaSlides';
    dom.slideCount.textContent = String(slides.length);
    dom.scaler.style.width = `${stageWidth}px`;
    dom.scaler.style.height = `${stageHeight}px`;
    dom.scaler.style.transform = 'translate(-50%, -50%) scale(.05)';
    document.documentElement.style.setProperty('--stage-w', `${stageWidth}px`);
    document.documentElement.style.setProperty('--stage-h', `${stageHeight}px`);
    scaleStage();
    buildFurnitureControls();
    buildPrintDeck();
    bindEvents();
    renderAll();
    syncRoute();
    requestAnimationFrame(scaleStage);
  }

  function applyDesignTokens() {
    const design = deck.design || {};
    const root = document.documentElement;
    const color = design.color || {};
    const type = design.typography || {};
    if (color.accent) root.style.setProperty('--accent', color.accent);
    if (color.positive) root.style.setProperty('--positive', color.positive);
    if (color.warning) root.style.setProperty('--warning', color.warning);
    if (color.negative) root.style.setProperty('--negative', color.negative);
    if (type.display_family) root.style.setProperty('--font-display', type.display_family);
    if (type.body_family) root.style.setProperty('--font-body', type.body_family);
    if (type.mono_family) root.style.setProperty('--font-mono', type.mono_family);
    const tones = color.tones || {};
    for (const toneName of ['light', 'dark', 'accent']) {
      const tone = tones[toneName];
      if (!tone) continue;
      const selector = `.prada-slide.tone-${toneName}`;
      const style = document.createElement('style');
      style.textContent = `${selector}{--page-bg:${tone.background};--page-surface:${tone.surface};--page-text:${tone.text};--page-muted:${tone.muted};--page-line:${tone.line};}`;
      document.head.appendChild(style);
    }
  }

  function buildFurnitureControls() {
    dom.furniture.replaceChildren();
    for (const [key, label] of furnitureKeys) {
      const row = document.createElement('label');
      row.className = 'toggle-row';
      const text = document.createElement('span');
      text.textContent = label;
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.dataset.furniture = key;
      input.addEventListener('change', () => setOverride('furniture', key, input.checked));
      const track = document.createElement('span');
      track.className = 'toggle-track';
      track.setAttribute('aria-hidden', 'true');
      row.append(text, input, track);
      dom.furniture.append(row);
    }
  }

  function bindEvents() {
    dom.previous.addEventListener('click', () => navigate(-1));
    dom.next.addEventListener('click', () => navigate(1));
    dom.present.addEventListener('click', enterPresentation);
    dom.print.addEventListener('click', () => {
      buildPrintDeck();
      closeExportMenu();
      setTimeout(() => window.print(), 40);
    });
    dom.stateDownload.addEventListener('click', downloadState);
    dom.reset.addEventListener('click', resetState);
    dom.uiTheme.addEventListener('click', () => {
      state.uiTheme = state.uiTheme === 'dark' ? 'light' : 'dark';
      saveState();
      renderConsoleState();
    });
    dom.panels.addEventListener('click', () => {
      state.panels = !state.panels;
      saveState();
      renderConsoleState();
      requestAnimationFrame(scaleStage);
    });
    dom.transition.addEventListener('change', () => setOverride('transition', null, dom.transition.value));
    dom.tone.addEventListener('click', event => {
      const button = event.target.closest('button[data-value]');
      if (button) setOverride('tone', null, button.dataset.value);
    });
    dom.density.addEventListener('click', event => {
      const button = event.target.closest('button[data-value]');
      if (button) setOverride('density', null, button.dataset.value);
    });
    dom.notesToggle.addEventListener('click', () => {
      state.notes = !state.notes;
      saveState();
      renderNotes();
    });
    window.addEventListener('resize', scaleStage);
    // Console rails can resize independently of the browser window. Observe the
    // actual stage region so the 16:9 canvas never retains a stale scale.
    if (typeof ResizeObserver === 'function') {
      const viewportObserver = new ResizeObserver(() => requestAnimationFrame(scaleStage));
      viewportObserver.observe(dom.viewport);
    }
    window.addEventListener('keydown', handleKeydown);
    document.addEventListener('fullscreenchange', () => {
      if (!document.fullscreenElement && document.body.classList.contains('present-mode')) exitPresentation();
    });
    document.addEventListener('click', event => {
      if (!event.target.closest('.export-menu')) closeExportMenu();
    });
  }

  function handleKeydown(event) {
    const tag = event.target?.tagName?.toLowerCase();
    if (['input', 'select', 'textarea'].includes(tag)) return;
    if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') {
      event.preventDefault();
      navigate(1);
    } else if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
      event.preventDefault();
      navigate(-1);
    } else if (event.key === 'Home') {
      event.preventDefault();
      goTo(0);
    } else if (event.key === 'End') {
      event.preventDefault();
      goTo(slides.length - 1);
    } else if (event.key.toLowerCase() === 'f') {
      event.preventDefault();
      document.body.classList.contains('present-mode') ? exitPresentation() : enterPresentation();
    } else if (event.key === 'Escape' && document.body.classList.contains('present-mode')) {
      exitPresentation();
    }
  }

  function renderAll() {
    renderConsoleState();
    renderActiveSlide();
    renderThumbnails();
    renderInspector();
    requestAnimationFrame(scaleStage);
    renderNotes();
    renderDraftStatus();
  }

  function renderConsoleState() {
    dom.console.classList.toggle('ui-light', state.uiTheme === 'light');
    dom.console.classList.toggle('panels-hidden', !state.panels);
  }

  function renderActiveSlide() {
    const slide = slides[state.index];
    dom.activeSlide.replaceChildren(createSlideElement(slide, state.index, true));
    const counter = `${pad(state.index + 1)} / ${pad(slides.length)}`;
    dom.stageCounter.textContent = counter;
    dom.toolbarCounter.textContent = `${state.index + 1}/${slides.length}`;
    if (dom.stageSection) dom.stageSection.textContent = slide.section || slide.role || slide.title || `Slide ${state.index + 1}`;
    dom.previous.disabled = state.index === 0;
    dom.next.disabled = state.index === slides.length - 1;
    dom.slideMeta.textContent = `${slide.id || pad(state.index + 1)} · ${slide.topology || 'custom'} · ${slide.layout || 'unregistered'}`;
    dom.live.textContent = `Slide ${state.index + 1} of ${slides.length}: ${slide.title || ''}`;
  }

  function renderThumbnails() {
    dom.thumbnails.replaceChildren();
    slides.forEach((slide, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'thumbnail-button';
      button.setAttribute('aria-label', `Go to slide ${index + 1}: ${slide.title || ''}`);
      button.setAttribute('aria-current', index === state.index ? 'true' : 'false');
      button.addEventListener('click', () => goTo(index));
      const badge = document.createElement('span');
      badge.className = 'thumb-index';
      badge.textContent = `${pad(index + 1)}/${pad(slides.length)}`;
      const viewport = document.createElement('span');
      viewport.className = 'thumb-canvas';
      viewport.append(createSlideElement(slide, index, false));
      button.append(badge, viewport);
      dom.thumbnails.append(button);
    });
    const active = dom.thumbnails.querySelector('[aria-current="true"]');
    active?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  function renderInspector() {
    const slide = effectiveSlide(slides[state.index], state.index);
    dom.transition.value = slide.transition;
    setSegmented(dom.tone, slide.tone);
    setSegmented(dom.density, slide.density);
    for (const input of dom.furniture.querySelectorAll('input[data-furniture]')) {
      input.checked = Boolean(slide.furniture[input.dataset.furniture]);
    }
  }

  function renderNotes() {
    const slide = slides[state.index];
    dom.notes.textContent = slide.notes || 'No speaker notes for this slide.';
    dom.notes.classList.toggle('is-hidden', !state.notes);
    dom.notesToggle.textContent = state.notes ? 'Hide' : 'Show';
  }

  function renderDraftStatus() {
    const isDraft = deck.meta?.status === 'draft' || slides.some(slide => slide.authoring?.incomplete);
    dom.draft.hidden = !isDraft;
  }

  function createSlideElement(source, index, animate) {
    const slide = effectiveSlide(source, index);
    const page = document.createElement('section');
    const authoredClasses = Array.isArray(source.classes)
      ? source.classes.map(safeClass).filter(Boolean)
      : [];
    page.className = [
      'prada-slide',
      `role-${slide.role || 'content'}`,
      `topology-${slide.topology || 'custom'}`,
      `layout-${slide.layout || 'custom'}`,
      `tone-${slide.tone}`,
      `density-${slide.density}`,
      animate && slide.transition !== 'none' ? `transition-${slide.transition}` : '',
      ...authoredClasses,
    ].filter(Boolean).join(' ');
    page.dataset.slideId = source.id || `P${pad(index + 1)}`;
    page.dataset.topology = source.topology || 'custom';
    page.dataset.layout = source.layout || 'custom';
    const referenceIds = Array.isArray(source.referenceIds)
      ? source.referenceIds
      : source.referenceId
        ? [source.referenceId]
        : [];
    if (referenceIds.length) page.dataset.referenceIds = referenceIds.map(String).join(',');
    const semanticTitle = String(source.title || 'Untitled slide').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    page.setAttribute('role', 'group');
    page.setAttribute('aria-roledescription', 'slide');
    page.setAttribute('aria-label', `Slide ${index + 1} of ${slides.length}: ${semanticTitle}`);

    if (source.background?.src) {
      const background = document.createElement('div');
      background.className = 'slide-background';
      background.style.backgroundImage = `url("${escapeCssUrl(source.background.src)}")`;
      background.style.backgroundPosition = source.background.position || 'center';
      background.style.setProperty('--background-overlay', String(source.background.overlay ?? .64));
      if (source.background.assetId) background.dataset.assetId = String(source.background.assetId);
      if (source.background.alt) { background.setAttribute('role', 'img'); background.setAttribute('aria-label', String(source.background.alt)); }
      else if (source.background.decorative) background.setAttribute('aria-hidden', 'true');
      page.append(background);
    }

    const inner = document.createElement('div');
    inner.className = 'slide-inner';
    const header = document.createElement('header');
    header.className = 'slide-header';
    if (slide.furniture.kicker && source.kicker) {
      const kicker = document.createElement('p');
      kicker.className = 'slide-kicker';
      kicker.textContent = source.kicker;
      header.append(kicker);
    }
    if (source.title) {
      const title = document.createElement('h1');
      title.className = 'slide-title';
      title.innerHTML = source.titleHtml || escapeHtml(source.title);
      header.append(title);
    }
    const body = document.createElement('div');
    body.className = 'slide-body';
    if (source.html) body.innerHTML = source.html;
    else {
      const empty = document.createElement('div');
      empty.className = 'authoring-empty';
      empty.setAttribute('aria-hidden', 'true');
      body.append(empty);
    }
    const footer = document.createElement('footer');
    footer.className = 'slide-footer';
    const sourceLine = document.createElement('span');
    sourceLine.className = 'slide-source';
    sourceLine.textContent = slide.furniture.sourceLine ? (source.source || '') : '';
    const pageNumber = document.createElement('span');
    pageNumber.className = 'slide-page';
    pageNumber.textContent = slide.furniture.pageNumber ? pad(index + 1) : '';
    footer.append(sourceLine, pageNumber);
    inner.append(header, body, footer);
    page.append(inner);

    if (slide.furniture.progress) {
      const progress = document.createElement('div');
      progress.className = 'slide-progress';
      progress.style.setProperty('--progress', `${((index + 1) / slides.length) * 100}%`);
      progress.append(document.createElement('span'));
      page.append(progress);
    }
    if (slide.furniture.frameCorners) addFrameCorners(page);
    if (slide.furniture.sectionRail) {
      const rail = document.createElement('div');
      rail.className = 'section-rail';
      rail.textContent = source.rail || source.kicker || source.role || 'section';
      page.append(rail);
    }
    if (slide.furniture.ghostMarker && source.ghostMarker) {
      const ghost = document.createElement('div');
      ghost.className = 'ghost-marker';
      ghost.textContent = source.ghostMarker;
      page.append(ghost);
    }
    if (slide.furniture.pageHint) {
      const hint = document.createElement('div');
      hint.className = 'page-hint';
      hint.textContent = source.pageHint || 'Next';
      page.append(hint);
    }
    if (slide.furniture.metricStrip && Array.isArray(source.metrics) && source.metrics.length) {
      page.append(createMetricStrip(source.metrics));
    }
    return page;
  }

  function createMetricStrip(metrics) {
    const wrapper = document.createElement('div');
    wrapper.className = 'furniture-metric-strip';
    const strip = document.createElement('div');
    strip.className = 'prada-metrics';
    strip.style.setProperty('--metric-count', String(Math.min(metrics.length, 4)));
    metrics.slice(0, 4).forEach(metric => {
      const item = document.createElement('div');
      item.className = 'prada-metric';
      const value = document.createElement('strong');
      value.textContent = metric.value || '';
      const label = document.createElement('span');
      label.textContent = metric.label || '';
      item.append(value, label);
      strip.append(item);
    });
    wrapper.append(strip);
    return wrapper;
  }

  function addFrameCorners(page) {
    for (const position of ['tl', 'tr', 'bl', 'br']) {
      const corner = document.createElement('span');
      corner.className = `frame-corner ${position}`;
      corner.setAttribute('aria-hidden', 'true');
      page.append(corner);
    }
  }

  function effectiveSlide(slide, index) {
    const override = state.overrides?.[slide.id || index] || {};
    return {
      ...slide,
      tone: override.tone || slide.tone || 'light',
      density: override.density || slide.density || 'standard',
      transition: override.transition || slide.transition || deck.meta?.transition || 'none',
      furniture: {
        ...defaultFurniture,
        ...(deck.meta?.furniture || {}),
        ...(slide.furniture || {}),
        ...(override.furniture || {}),
      },
    };
  }

  function setOverride(field, nestedKey, value) {
    const slide = slides[state.index];
    const key = slide.id || state.index;
    state.overrides[key] = state.overrides[key] || {};
    if (nestedKey) {
      state.overrides[key][field] = state.overrides[key][field] || {};
      state.overrides[key][field][nestedKey] = value;
    } else {
      state.overrides[key][field] = value;
    }
    saveState();
    renderActiveSlide();
    renderThumbnails();
    renderInspector();
  }

  function navigate(delta) { goTo(state.index + delta); }
  function goTo(index) {
    const next = clamp(index, 0, slides.length - 1);
    if (next === state.index) return;
    state.index = next;
    saveState();
    syncRoute();
    renderActiveSlide();
    renderThumbnails();
    renderInspector();
    renderNotes();
    requestAnimationFrame(scaleStage);
  }

  async function enterPresentation() {
    document.body.classList.add('present-mode');
    syncRoute();
    requestAnimationFrame(scaleStage);
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen?.();
    } catch (_) {
      // Presentation mode remains useful when fullscreen permission is unavailable.
    }
  }

  async function exitPresentation() {
    document.body.classList.remove('present-mode');
    syncRoute();
    if (document.fullscreenElement) {
      try { await document.exitFullscreen?.(); } catch (_) { /* no-op */ }
    }
    requestAnimationFrame(scaleStage);
  }

  function scaleStage() {
    const rect = dom.viewport.getBoundingClientRect();
    const scale = Math.max(.05, Math.min(rect.width / stageWidth, rect.height / stageHeight));
    dom.scaler.style.transform = `translate(-50%, -50%) scale(${scale})`;
  }

  function buildPrintDeck() {
    dom.printDeck.replaceChildren();
    slides.forEach((slide, index) => dom.printDeck.append(createSlideElement(slide, index, false)));
  }

  function downloadState() {
    const payload = {
      deck: deck.meta?.title || 'PradaSlides',
      exportedAt: new Date().toISOString(),
      note: 'Preview controls only; source deck remains deck.js.',
      state,
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = `${slug(deck.meta?.title || 'pradaslides')}-preview-state.json`;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 500);
    closeExportMenu();
  }

  function resetState() {
    localStorage.removeItem(storageKey);
    state.index = 0;
    state.uiTheme = 'dark';
    state.panels = true;
    state.notes = true;
    state.overrides = {};
    renderAll();
    syncRoute();
    requestAnimationFrame(scaleStage);
  }

  function syncRoute() {
    try {
      const url = new URL(window.location.href);
      url.searchParams.delete('page');
      url.searchParams.set('slide', String(state.index + 1));
      if (document.body.classList.contains('present-mode')) url.searchParams.set('present', '1');
      else url.searchParams.delete('present');
      history.replaceState(null, '', url);
    } catch (_) { /* file/runtime policy may forbid history updates */ }
  }

  function loadState() {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return value && typeof value === 'object' ? value : {};
    } catch (_) { return {}; }
  }
  function saveState() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) { /* file sandbox */ }
  }
  function setSegmented(container, value) {
    container.querySelectorAll('button[data-value]').forEach(button => {
      button.classList.toggle('is-active', button.dataset.value === value);
    });
  }
  function closeExportMenu() { document.querySelector('.export-menu')?.removeAttribute('open'); }
  function pad(value) { return String(value).padStart(2, '0'); }
  function clamp(value, minimum, maximum) { return Math.min(maximum, Math.max(minimum, value)); }
  function slug(value) { return String(value).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'deck'; }
  function safeClass(value) { const match = String(value).match(/^[a-z][a-z0-9-]{0,48}$/i); return match ? match[0] : ''; }
  function escapeHtml(value) {
    return String(value).replace(/[&<>"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[character]));
  }
  function escapeCssUrl(value) { return String(value).replace(/["\\\n\r]/g, character => `\\${character}`); }
})();
