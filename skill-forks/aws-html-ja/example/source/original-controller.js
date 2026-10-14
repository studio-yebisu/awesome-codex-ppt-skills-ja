/* === SLIDE CONTROLLER === */
(function () {
    var slides = document.querySelectorAll('.slide');
    var bar = document.getElementById('progressBar');
    var dotsContainer = document.getElementById('navDots');
    var total = slides.length, current = 0;

    /* HUD index overlays */
    slides.forEach(function (s, i) {
        var idx = s.querySelector('.hud-index');
        if (idx) idx.textContent = 'IDX ' + String(i + 1).padStart(2, '0') + '/' + String(total).padStart(2, '0');
    });

    /* Intersection Observer -> reveal + one-shot FX */
    var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
            if (e.isIntersecting) {
                e.target.classList.add('visible');
                current = [].indexOf.call(slides, e.target);
                updateUI();
                if (window.runFX) window.runFX(e.target);
            }
        });
    }, { threshold: 0.5 });
    slides.forEach(function (s) { obs.observe(s); });

    /* Nav dots */
    slides.forEach(function (_, i) {
        var d = document.createElement('button');
        d.className = 'nav-dot' + (i === 0 ? ' active' : '');
        d.setAttribute('aria-label', 'Slide ' + (i + 1));
        d.addEventListener('click', function () { go(i); });
        dotsContainer.appendChild(d);
    });
    var dots = dotsContainer.querySelectorAll('.nav-dot');

    function updateUI() {
        bar.style.width = ((current + 1) / total * 100) + '%';
        dots.forEach(function (d, i) { d.classList.toggle('active', i === current); });
    }
    function go(i) {
        if (i < 0 || i >= total) return;
        current = i; slides[i].scrollIntoView({ behavior: 'smooth' }); updateUI();
    }

    document.addEventListener('keydown', function (e) {
        if (['ArrowDown', 'ArrowRight', ' ', 'PageDown'].includes(e.key)) { e.preventDefault(); go(current + 1); }
        else if (['ArrowUp', 'ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); go(current - 1); }
        else if (e.key === 'Home') { e.preventDefault(); go(0); }
        else if (e.key === 'End') { e.preventDefault(); go(total - 1); }
    });

    var wt = null;
    document.addEventListener('wheel', function (e) {
        if (wt) return;
        wt = setTimeout(function () { wt = null; }, 800);
        if (e.deltaY > 30) go(current + 1); else if (e.deltaY < -30) go(current - 1);
    }, { passive: true });

    var ty = 0;
    document.addEventListener('touchstart', function (e) { ty = e.touches[0].clientY; }, { passive: true });
    document.addEventListener('touchend', function (e) {
        var d = ty - e.changedTouches[0].clientY;
        if (Math.abs(d) > 50) go(current + (d > 0 ? 1 : -1));
    }, { passive: true });

    updateUI();
})();

/* === SLIDE FX (counters, typing, scramble, spotlight/tilt) === */
(function initSlideFX() {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

    /* (a) counters — ease-out-cubic 0 -> data-count over 1.2s */
    function runCounters(root) {
        root.querySelectorAll('.count').forEach(function (el) {
            var target = parseFloat(el.getAttribute('data-count')) || 0;
            var suffix = el.getAttribute('data-suffix') || '';
            if (reduce) { el.textContent = target + suffix; return; }
            var dur = 1200, t0 = 0;
            function step(now) {
                if (!t0) t0 = now;
                var p = Math.min(1, (now - t0) / dur);
                var eased = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.round(target * eased) + suffix;
                if (p < 1) requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
        });
    }

    /* (b) typing — sequential across [data-type] in the slide */
    function runTyping(root) {
        var targets = [].slice.call(root.querySelectorAll('[data-type]'));
        if (!targets.length) return;
        if (reduce) {
            targets.forEach(function (el) {
                var full = el.getAttribute('data-type') || '';
                if (el.classList.contains('term-line')) el.textContent = full;
                else { el.innerHTML = esc(full).replace(/\n/g, '<br>') + '<span class="cursor"></span>'; }
            });
            return;
        }
        var i = 0;
        (function nextEl() {
            if (i >= targets.length) return;
            var el = targets[i], full = el.getAttribute('data-type') || '';
            var isTerm = el.classList.contains('term-line');
            var caret = null;
            if (isTerm) { el.textContent = ''; el.classList.add('active'); }
            else { el.innerHTML = ''; caret = document.createElement('span'); caret.className = 'cursor'; el.appendChild(caret); }
            var pos = 0;
            (function typeChar() {
                pos++;
                var s = full.slice(0, pos);
                if (isTerm) el.textContent = s;
                else { el.innerHTML = esc(s).replace(/\n/g, '<br>'); el.appendChild(caret); }
                if (pos < full.length) { setTimeout(typeChar, 28); }
                else {
                    if (isTerm) el.classList.remove('active');
                    i++; setTimeout(nextEl, isTerm ? 90 : 30);
                }
            })();
        })();
    }

    /* (c) scramble — 900ms left->right decode */
    function runScramble(root) {
        var CHARS = "!<>-_\\/[]{}—=+*^?#0123456789";
        root.querySelectorAll('.scramble').forEach(function (el) {
            var full = el.getAttribute('data-text') || el.textContent;
            if (reduce) { el.textContent = full; return; }
            var dur = 900, t0 = 0;
            function frame(now) {
                if (!t0) t0 = now;
                var p = Math.min(1, (now - t0) / dur);
                var revealed = Math.floor(full.length * p), out = '';
                for (var k = 0; k < full.length; k++) {
                    out += k < revealed ? full[k] : (full[k] === ' ' ? ' ' : CHARS[(Math.random() * CHARS.length) | 0]);
                }
                el.textContent = out;
                if (p < 1) requestAnimationFrame(frame); else el.textContent = full;
            }
            requestAnimationFrame(frame);
        });
    }

    /* runFX — one-shot per slide, guarded by dataset.fx */
    window.runFX = function (slide) {
        if (slide.dataset.fx) return;
        slide.dataset.fx = '1';
        runCounters(slide); runTyping(slide); runScramble(slide);
    };

    /* (d) spotlight + 3D tilt — bound once at init */
    document.querySelectorAll('.spot-card').forEach(function (card) {
        card.addEventListener('pointermove', function (e) {
            var r = card.getBoundingClientRect();
            var mx = e.clientX - r.left, my = e.clientY - r.top;
            card.style.setProperty('--mx', mx + 'px');
            card.style.setProperty('--my', my + 'px');
            if (reduce || !card.classList.contains('tilt')) return;
            var rx = ((my / r.height) - 0.5) * -12, ry = ((mx / r.width) - 0.5) * 12;
            card.style.transform = 'perspective(700px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg)';
        });
        card.addEventListener('pointerleave', function () { card.style.transform = ''; });
    });

    /* Fire FX for any slide already visible at load (usually slide 1) */
    document.querySelectorAll('.slide.visible').forEach(function (s) { window.runFX(s); });
})();