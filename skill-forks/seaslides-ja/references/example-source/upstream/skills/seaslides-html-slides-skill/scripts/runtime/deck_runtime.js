/* SeaSlides deck runtime: browser-only, dependency-free, safe to inline. */
(function installSeaSlidesRuntime(window, document) {
  'use strict';

  if (!window || !document || window.SeaSlidesRuntime) return;

  var VERSION = '1.0.0';
  var EVENT = 'seaslides-runtime';
  var STORAGE_KEY = 'seaslides-runtime-low-power';
  var state = {
    lowPower: false,
    reducedMotion: false,
    overview: null,
    ownsOverview: false,
    lastFocus: null,
    ready: false
  };
  var resolveReady;
  var ready = new Promise(function (resolve) { resolveReady = resolve; });

  function emit(type, detail) {
    var payload = { type: type, version: VERSION, time: Date.now() };
    var key;
    if (detail) {
      for (key in detail) {
        if (Object.prototype.hasOwnProperty.call(detail, key)) payload[key] = detail[key];
      }
    }
    window.dispatchEvent(new CustomEvent(EVENT, { detail: payload }));
    return payload;
  }

  function storageGet() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (_) { return null; }
  }

  function storageSet(value) {
    try { window.localStorage.setItem(STORAGE_KEY, value ? '1' : '0'); } catch (_) { /* private mode */ }
  }

  function isEditable(target) {
    if (!target || !target.closest) return false;
    return !!target.closest('input, textarea, select, [contenteditable=""], [contenteditable="true"]');
  }

  function ensureStyle() {
    if (document.getElementById('seaslides-runtime-style')) return;
    var style = document.createElement('style');
    style.id = 'seaslides-runtime-style';
    style.textContent = [
      'body.seaslides-low-power, body.low-power { scroll-behavior: auto !important; }',
      'body.seaslides-low-power *, body.seaslides-low-power *::before, body.seaslides-low-power *::after { animation: none !important; transition: none !important; }',
      'body.seaslides-low-power [data-anim], body.seaslides-low-power [data-animation], body.seaslides-low-power [data-animate], .seaslides-export-settled [data-anim], .seaslides-export-settled [data-animation], .seaslides-export-settled [data-animate] { opacity: 1 !important; visibility: visible !important; transform: none !important; }',
      '.seaslides-runtime-overview { position: fixed; inset: 0; z-index: 2147483646; overflow: auto; padding: 3rem; background: rgba(18, 20, 25, .97); color: #fff; }',
      '.seaslides-runtime-overview[hidden] { display: none !important; }',
      '.seaslides-runtime-overview__bar { display: flex; align-items: center; justify-content: space-between; gap: 1rem; max-width: 1500px; margin: 0 auto 1.5rem; }',
      '.seaslides-runtime-overview__title { margin: 0; font: 600 1.1rem/1.2 system-ui, sans-serif; }',
      '.seaslides-runtime-overview__close { border: 1px solid currentColor; border-radius: .35rem; background: transparent; color: inherit; padding: .45rem .7rem; font: inherit; cursor: pointer; }',
      '.seaslides-runtime-overview__grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; max-width: 1500px; margin: 0 auto; }',
      '.seaslides-runtime-overview__card { display: block; min-width: 0; padding: 0; overflow: hidden; border: 2px solid rgba(255,255,255,.38); border-radius: .4rem; background: #fff; color: #111; text-align: left; cursor: pointer; }',
      '.seaslides-runtime-overview__card:focus-visible, .seaslides-runtime-overview__close:focus-visible { outline: 3px solid #7dd3fc; outline-offset: 3px; }',
      '.seaslides-runtime-overview__preview { position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: #fff; pointer-events: none; }',
      '.seaslides-runtime-overview__label { display: block; padding: .55rem .7rem; font: 600 .8rem/1 system-ui, sans-serif; }'
    ].join('\n');
    (document.head || document.documentElement).appendChild(style);
  }

  function finalState(root) {
    if (!root || !root.querySelectorAll) return;
    var nodes = root.querySelectorAll('[data-anim], [data-animation], [data-animate]');
    Array.prototype.forEach.call(nodes, function (node) {
      node.style.setProperty('opacity', '1', 'important');
      node.style.setProperty('visibility', 'visible', 'important');
      node.style.setProperty('transform', 'none', 'important');
      node.style.setProperty('animation', 'none', 'important');
      node.style.setProperty('transition', 'none', 'important');
    });
  }

  function stopAnimations() {
    if (!document.getAnimations) return;
    document.getAnimations().forEach(function (animation) {
      try { animation.finish(); } catch (_) {
        try { animation.cancel(); } catch (_) { /* best effort */ }
      }
    });
  }

  function applyLowPower() {
    if (!document.body) return;
    document.body.classList.toggle('low-power', state.lowPower);
    document.body.classList.toggle('seaslides-low-power', state.lowPower);
    window.__lowPowerMode = state.lowPower;
    if (state.lowPower) {
      finalState(document);
      stopAnimations();
    }
  }

  function setLowPower(on, options) {
    options = options || {};
    var next = !!on;
    var changed = next !== state.lowPower;
    state.lowPower = next;
    applyLowPower();
    if (options.persist !== false) storageSet(next);

    // Existing templates use this hook for theme-specific effects (for example WebGL).
    if (typeof window.__setLowPowerMode === 'function' && window.__setLowPowerMode !== setLowPower) {
      try { window.__setLowPowerMode(next, { persist: false, source: 'seaslides-runtime' }); } catch (_) { /* optional hook */ }
    }
    if (changed || options.forceEvent) emit('low-power-change', { lowPower: next, source: options.source || 'api' });
    return next;
  }

  function existingOverview() {
    var element = document.querySelector('[data-seaslides-overview], #overview');
    if (element && element !== state.overview) {
      state.overview = element;
      state.ownsOverview = false;
    }
    return state.overview;
  }

  function slideElements() {
    return Array.prototype.slice.call(document.querySelectorAll('#deck .slide, .slide'))
      .filter(function (slide, index, all) { return all.indexOf(slide) === index && !slide.closest('.seaslides-runtime-overview'); });
  }

  function cloneSlide(slide, preview) {
    var rect = slide.getBoundingClientRect();
    var width = rect.width || window.innerWidth || 1280;
    var height = rect.height || window.innerHeight || 720;
    var scale = Math.min(preview.clientWidth / width, preview.clientHeight / height) || 0.2;
    var clone = slide.cloneNode(true);
    clone.removeAttribute('id');
    Array.prototype.forEach.call(clone.querySelectorAll('[id]'), function (node) { node.removeAttribute('id'); });
    clone.setAttribute('aria-hidden', 'true');
    clone.setAttribute('data-seaslides-preview-width', String(width));
    clone.setAttribute('data-seaslides-preview-height', String(height));
    clone.style.cssText += ';position:absolute!important;inset:0 auto auto 0!important;width:' + width + 'px!important;height:' + height + 'px!important;max-width:none!important;max-height:none!important;transform:scale(' + scale + ')!important;transform-origin:top left!important;pointer-events:none!important;';
    finalState(clone);
    return clone;
  }

  function scaleOverviewPreviews(element) {
    if (!element) return;
    Array.prototype.forEach.call(element.querySelectorAll('.seaslides-runtime-overview__preview'), function (preview) {
      var clone = preview.firstElementChild;
      if (!clone) return;
      var width = Number(clone.getAttribute('data-seaslides-preview-width')) || 1280;
      var height = Number(clone.getAttribute('data-seaslides-preview-height')) || 720;
      var scale = Math.min(preview.clientWidth / width, preview.clientHeight / height);
      if (Number.isFinite(scale) && scale > 0) {
        clone.style.setProperty('transform', 'scale(' + scale + ')', 'important');
      }
    });
  }

  function navigateTo(index) {
    var go = window.__goToSlide || window.__navigateToSlide || window.go;
    if (typeof go === 'function') {
      try { go(index); return true; } catch (_) { /* try a navigation control */ }
    }
    var control = document.querySelector('#nav [data-i="' + index + '"], [data-slide-index="' + index + '"]');
    if (control && typeof control.click === 'function') { control.click(); return true; }
    emit('navigate-request', { index: index });
    return false;
  }

  function buildOverview(element) {
    if (element.querySelector('.seaslides-runtime-overview__grid')) return;
    var slides = slideElements();
    var bar = document.createElement('div');
    var title = document.createElement('h2');
    var close = document.createElement('button');
    var grid = document.createElement('div');
    bar.className = 'seaslides-runtime-overview__bar';
    title.className = 'seaslides-runtime-overview__title';
    title.textContent = 'Slide overview';
    close.type = 'button';
    close.className = 'seaslides-runtime-overview__close';
    close.textContent = 'Close overview';
    close.addEventListener('click', hideOverview);
    bar.appendChild(title);
    bar.appendChild(close);
    grid.className = 'seaslides-runtime-overview__grid';

    slides.forEach(function (slide, index) {
      var card = document.createElement('button');
      var preview = document.createElement('span');
      var label = document.createElement('span');
      card.type = 'button';
      card.className = 'seaslides-runtime-overview__card';
      card.setAttribute('aria-label', 'Go to slide ' + (index + 1));
      preview.className = 'seaslides-runtime-overview__preview';
      label.className = 'seaslides-runtime-overview__label';
      label.textContent = 'Slide ' + (index + 1) + ' of ' + slides.length;
      preview.appendChild(cloneSlide(slide, preview));
      card.appendChild(preview);
      card.appendChild(label);
      card.addEventListener('click', function () { hideOverview(); navigateTo(index); });
      grid.appendChild(card);
    });
    element.appendChild(bar);
    element.appendChild(grid);
  }

  function overviewElement() {
    var compatible = existingOverview();
    if (compatible) return compatible;
    var element = document.createElement('section');
    element.className = 'seaslides-runtime-overview';
    element.setAttribute('data-seaslides-overview', 'runtime');
    element.setAttribute('role', 'dialog');
    element.setAttribute('aria-modal', 'true');
    element.setAttribute('aria-label', 'Slide overview');
    element.tabIndex = -1;
    element.hidden = true;
    (document.body || document.documentElement).appendChild(element);
    state.overview = element;
    state.ownsOverview = true;
    return element;
  }

  function showOverview() {
    if (!document.body) return false;
    ensureStyle();
    var element = overviewElement();
    state.lastFocus = document.activeElement;
    if (state.ownsOverview || !element.children.length) buildOverview(element);
    element.hidden = false;
    element.style.display = 'block';
    element.setAttribute('aria-hidden', 'false');
    if (!element.hasAttribute('role')) element.setAttribute('role', 'dialog');
    if (!element.hasAttribute('aria-label')) element.setAttribute('aria-label', 'Slide overview');
    if (!element.hasAttribute('tabindex')) element.tabIndex = -1;
    window.setTimeout(function () {
      scaleOverviewPreviews(element);
      try { element.focus({ preventScroll: true }); } catch (_) { element.focus(); }
    }, 0);
    emit('overview-change', { open: true, owned: state.ownsOverview });
    return true;
  }

  function hideOverview() {
    var element = state.overview || existingOverview();
    if (!element) return false;
    element.hidden = true;
    element.style.display = 'none';
    element.setAttribute('aria-hidden', 'true');
    if (state.lastFocus && typeof state.lastFocus.focus === 'function') {
      try { state.lastFocus.focus({ preventScroll: true }); } catch (_) { state.lastFocus.focus(); }
    }
    emit('overview-change', { open: false, owned: state.ownsOverview });
    return true;
  }

  function overviewIsOpen() {
    var element = state.overview || existingOverview();
    return !!(element && !element.hidden && window.getComputedStyle(element).display !== 'none');
  }

  function nextFrame() {
    return new Promise(function (resolve) {
      (window.requestAnimationFrame || function (callback) { return window.setTimeout(callback, 16); })(resolve);
    });
  }

  function dynamicPromises(diagnostics) {
    var names = ['__SeaSlidesDynamicReady', '__seaslidesDynamicReady', '__seaslidesDynamicContent', '__dynamicContentReady'];
    var promises = [];
    names.forEach(function (name) {
      var value = window[name];
      if (typeof value === 'function') {
        try { value = value(); } catch (error) { promises.push(Promise.reject(error)); return; }
      }
      if (value && typeof value.then === 'function') {
        diagnostics.dynamic.push(name);
        promises.push(Promise.resolve(value));
      }
    });
    if (typeof window.__typesetMath === 'function') {
      try {
        diagnostics.dynamic.push('__typesetMath');
        promises.push(Promise.resolve(window.__typesetMath(document.body)));
      } catch (error) { promises.push(Promise.reject(error)); }
    }
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
      diagnostics.dynamic.push('MathJax.startup.promise');
      promises.push(Promise.resolve(window.MathJax.startup.promise));
    }
    return promises;
  }

  function waitForImages(timeout, diagnostics) {
    var images = Array.prototype.slice.call(document.images || []);
    diagnostics.images.total = images.length;
    return Promise.all(images.map(function (image) {
      image.loading = 'eager';
      return new Promise(function (resolve) {
        var done = false;
        function finish(status) {
          if (done) return;
          done = true;
          image.removeEventListener('load', onLoad);
          image.removeEventListener('error', onError);
          if (status === 'loaded') diagnostics.images.loaded += 1;
          else {
            diagnostics.images.broken.push(image.currentSrc || image.src || '(missing src)');
          }
          resolve();
        }
        function onLoad() { finish(image.naturalWidth > 0 ? 'loaded' : 'broken'); }
        function onError() { finish('broken'); }
        if (image.complete) { finish(image.naturalWidth > 0 ? 'loaded' : 'broken'); return; }
        image.addEventListener('load', onLoad, { once: true });
        image.addEventListener('error', onError, { once: true });
        window.setTimeout(function () { finish('timeout'); }, timeout);
      });
    }));
  }

  function exportError(message, diagnostics) {
    var error = new Error(message);
    error.name = 'SeaSlidesExportError';
    error.diagnostics = diagnostics;
    return error;
  }

  function waitWithTimeout(promise, timeout, diagnostics) {
    return new Promise(function (resolve, reject) {
      var complete = false;
      var timer = window.setTimeout(function () {
        if (complete) return;
        complete = true;
        diagnostics.timeouts.push('dynamic content or fonts');
        reject(new Error('Timed out waiting for dynamic content or fonts'));
      }, timeout);
      Promise.resolve(promise).then(function (value) {
        if (complete) return;
        complete = true;
        window.clearTimeout(timer);
        resolve(value);
      }, function (error) {
        if (complete) return;
        complete = true;
        window.clearTimeout(timer);
        reject(error);
      });
    });
  }

  function settleForExport(options) {
    options = options || {};
    var timeout = Math.max(0, Number(options.timeout) || 10000);
    var diagnostics = {
      version: VERSION,
      images: { total: 0, loaded: 0, broken: [] },
      fonts: { supported: !!document.fonts, ready: false },
      dynamic: [],
      timeouts: [],
      frames: 0,
      lowPower: state.lowPower
    };
    return ready.then(function () {
      var waits = dynamicPromises(diagnostics);
      if (document.fonts && document.fonts.ready) {
        waits.push(Promise.resolve(document.fonts.ready).then(function () { diagnostics.fonts.ready = true; }));
      }
      waits.push(waitForImages(timeout, diagnostics));
      return waitWithTimeout(Promise.all(waits), timeout, diagnostics).then(function () {
        document.documentElement.classList.add('seaslides-export-settled');
        finalState(document);
        stopAnimations();
        return nextFrame().then(function () { diagnostics.frames += 1; return nextFrame(); }).then(function () {
          diagnostics.frames += 1;
          diagnostics.settledAt = Date.now();
          if (diagnostics.images.broken.length) throw exportError('Broken or timed-out image assets', diagnostics);
          emit('export-settled', { diagnostics: diagnostics });
          return diagnostics;
        });
      }).catch(function (error) {
        var failure = error && error.diagnostics ? error : exportError('Dynamic content failed to settle: ' + (error && error.message || error), diagnostics);
        emit('export-settle-error', { diagnostics: diagnostics, message: failure.message });
        throw failure;
      });
    });
  }

  var runtime = { version: VERSION, ready: ready, settleForExport: settleForExport, setLowPower: setLowPower, showOverview: showOverview, hideOverview: hideOverview };
  Object.defineProperties(runtime, {
    lowPower: { enumerable: true, get: function () { return state.lowPower; } },
    reducedMotion: { enumerable: true, get: function () { return state.reducedMotion; } }
  });
  Object.defineProperty(runtime, '__seaSlidesRuntime', { value: true });
  window.SeaSlidesRuntime = runtime;

  function initialize() {
    ensureStyle();
    var stored = storageGet();
    var legacy = typeof window.__lowPowerMode === 'boolean' ? window.__lowPowerMode : null;
    var media = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
    state.reducedMotion = !!(media && media.matches);
    state.lowPower = stored === '1' || (stored === null && (legacy === null ? state.reducedMotion : legacy));
    applyLowPower();
    if (media) {
      var onMediaChange = function (event) {
        state.reducedMotion = !!event.matches;
        emit('reduced-motion-change', { reducedMotion: state.reducedMotion });
        if (storageGet() === null) setLowPower(state.reducedMotion, { persist: false, source: 'media' });
      };
      if (media.addEventListener) media.addEventListener('change', onMediaChange);
      else if (media.addListener) media.addListener(onMediaChange);
    }
    window.addEventListener('keydown', function (event) {
      var themeOverview = document.querySelector('[data-seaslides-overview]:not([data-seaslides-overview="runtime"]), #overview');
      // A few themes already own a specialized overview.  Let their handler
      // keep keyboard ownership instead of toggling the same panel twice.
      if (event.key === 'Escape' && themeOverview && !state.ownsOverview) {
        return;
      } else if (event.key === 'Escape' && overviewIsOpen()) {
        event.preventDefault();
        event.stopImmediatePropagation();
        hideOverview();
      } else if (event.key === 'Escape' && !isEditable(event.target)) {
        event.preventDefault();
        event.stopImmediatePropagation();
        showOverview();
      } else if (event.key && event.key.toLowerCase() === 'b' && !event.metaKey && !event.ctrlKey && !event.altKey && !isEditable(event.target)) {
        event.preventDefault();
        event.stopImmediatePropagation();
        setLowPower(!state.lowPower, { source: 'keyboard' });
      }
    });
    window.addEventListener('resize', function () {
      if (overviewIsOpen()) scaleOverviewPreviews(state.overview);
    });
    state.ready = true;
    resolveReady(runtime);
    emit('ready', { lowPower: state.lowPower, reducedMotion: state.reducedMotion });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})(window, document);
