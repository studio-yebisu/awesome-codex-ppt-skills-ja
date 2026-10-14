/*
 * <deck-stage> - the presentation engine.
 *
 * A zero-dependency custom element that turns a list of <section> slides into a
 * navigable, auto-scaling deck. Slides are authored on a fixed design canvas
 * (default 1920x1080) that the engine scales to fit any screen.
 *
 * Operating modes:
 *   windowed     default; shows the thumbnail rail on the left.
 *   full screen  the "f" key or button; rail hidden, controls fade when idle.
 *   presenter    the "p" key or button; opens an audience window (full-screen
 *                slide) and shows a presenter sidebar here (next-slide preview,
 *                speaker notes, wall clock and timers).
 *
 * Speaker notes: add <aside class="notes"> inside a slide; it shows only in the
 * presenter sidebar, never to the audience.
 *
 * Progressive reveal: add class="fragment" to elements to reveal them one click
 * at a time before moving on to the next slide.
 *
 * Motion: the canvas carries data-motion (the level), data-transition (this
 * slide's transition) and data-dir (next / prev); motion.css and the
 * components animate off those. data-count numbers count up here, in JS.
 *
 * Attributes on <deck-stage>:
 *   width / height   design canvas size (default 1920x1080)
 *   transition       default slide transition: none, fade (default), slide,
 *                    zoom, rise, blur, flip - a slide's data-transition wins
 *   motion           none, subtle, balanced (default), lively, extra
 *   exit-hint        toast text shown when entering single-screen full screen
 *   no-rail          always hide the thumbnail rail
 *
 * Render mode, for scripts/check_deck.py: ?pf=shot#3 shows slide 3 alone and
 * finished; ?pf=sheet shows every slide on one contact sheet. Both write a
 * layout report (overflowing content, broken images) into the page, as a
 * JSON script element with the id pf-report.
 */
(() => {
  "use strict";

  const VERSION = "1.0.0";

  const DESIGN_W = 1920;
  const DESIGN_H = 1080;
  const IDLE_MS = 2500;
  const TOAST_MS = 2800;
  const DEFAULT_EXIT_HINT = "Press Esc to exit full screen.";

  const INTERACTIVE =
    'a[href], button, input, select, textarea, summary, label, ' +
    'video[controls], audio[controls], [role="button"], [onclick], [tabindex]';

  // Text blocks the Edit mode may change: build.py decides which and stamps
  // them (data-pf-edit), so the same rules find them again when it pulls the
  // edits back into slides/. The notes carry data-pf-notes the same way.
  const EDITABLE = "[data-pf-edit]";
  // Count-ups run from this level up (see countUp below).
  const COUNT_LEVELS = ["balanced", "lively", "extra"];
  const DRAW_SHAPES = "path, line, polyline, polygon, circle, rect, ellipse";

  const ICONS = {
    prev:     '<svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>',
    next:     '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
    expand:   '<svg viewBox="0 0 24 24"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M16 3h3a2 2 0 0 1 2 2v3"/><path d="M21 16v3a2 2 0 0 1-2 2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/></svg>',
    compress: '<svg viewBox="0 0 24 24"><path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/><path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg>',
    present:  '<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="13" rx="2"/><path d="M8 21h8M12 16v5"/><path d="M7 10h1m3-3v6m3-4v4"/></svg>',
    editNotes:'<svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    play:     '<svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
    pause:    '<svg viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>',
    reset:    '<svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>',
    draw:     '<svg viewBox="0 0 24 24"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>',
    erase:    '<svg viewBox="0 0 24 24"><path d="M20 20H7L3 16l11-11 7 7-4 4"/><path d="m6.5 17.5 5-5"/></svg>',
    laser:    '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3" fill="currentColor"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M16.9 16.9l2.1 2.1M19.1 4.9l-2.1 2.1M7.1 16.9l-2.1 2.1"/></svg>',
    help:     '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><circle cx="12" cy="17" r=".5" fill="currentColor"/></svg>',
    exit:     '<svg viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
    editText: '<svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4z"/></svg>',
    save:     '<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>',
  };

  const el = (tag, cls) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    return n;
  };

  const mkBtn = (cls, label, svg, onClick) => {
    const b = el("button", "pf-btn " + cls);
    b.type = "button";
    b.setAttribute("aria-label", label);
    b.title = label;
    b.innerHTML = svg;
    b.addEventListener("click", onClick);
    return b;
  };

  const pad2 = (n) => String(n).padStart(2, "0");
  const fsEl = () => document.fullscreenElement || document.webkitFullscreenElement || null;

  /* Speaker notes are authored as HTML (paragraphs and lists) but edited in a
     plain <textarea>. These two translate between the forms so an edit keeps
     the notes' structure: one line per paragraph, "- " for a bullet, "1. " for
     a numbered item. Inline formatting (<em>, <code>...) is only lost on notes
     someone actually edits - untouched notes are never rewritten. */
  const NOTE_BLOCKS = new Set(["P", "DIV", "UL", "OL", "BLOCKQUOTE", "PRE", "H1", "H2", "H3", "H4", "H5", "H6"]);
  const squash = (s) => s.replace(/\s+/g, " ").trim();

  const notesToText = (aside) => {
    const lines = [];
    let run = "";   // consecutive inline content (text, <em>, <code>...) = one paragraph
    const flush = () => {
      const text = squash(run);
      if (text) lines.push(text);
      run = "";
    };
    aside.childNodes.forEach((node) => {
      if (node.nodeType === Node.TEXT_NODE) { run += node.textContent; return; }
      if (node.nodeType !== Node.ELEMENT_NODE) return;              // comments
      if (node.tagName === "BR") { flush(); return; }
      if (!NOTE_BLOCKS.has(node.tagName)) { run += node.textContent; return; }
      flush();
      if (node.tagName === "UL" || node.tagName === "OL") {
        let n = 0;
        Array.from(node.children).forEach((li) => {
          if (li.tagName !== "LI") return;
          lines.push((node.tagName === "OL" ? `${++n}. ` : "- ") + squash(li.textContent));
        });
      } else {
        run = node.textContent;
        flush();
      }
    });
    flush();
    return lines.join("\n");
  };

  const textToNotes = (aside, text) => {
    aside.textContent = "";
    let list = null;   // the <ul>/<ol> consecutive list lines are appended to
    text.split("\n").forEach((raw) => {
      const line = raw.trim();
      if (!line) { list = null; return; }
      const m = /^(?:([-*•])|\d+[.)])\s+(.*)$/.exec(line);
      if (!m) {
        list = null;
        aside.appendChild(document.createElement("p")).textContent = line;
        return;
      }
      const tag = m[1] ? "UL" : "OL";
      if (!list || list.tagName !== tag) list = aside.appendChild(document.createElement(tag));
      list.appendChild(document.createElement("li")).textContent = m[2];
    });
  };

  /* Count a figure up from 0 to the number in its text, then put the exact
     original text back. The real figure stays in the markup, so thumbnails,
     print and a copy without JS all show it. Self-contained (no outer names):
     the audience window gets a copy of this very function. */
  function countUp(el, lang) {
    if (el.children.length) return;                     // plain-text figures only
    if (el.__pfFinal === undefined) el.__pfFinal = el.textContent;
    var text = el.__pfFinal;
    var m = /\d(?:[\d\s\u00a0\u202f.,']*\d)?/.exec(text);
    if (!m) return;
    var raw = m[0];
    var compact = raw.replace(/[\s\u00a0\u202f']/g, "");
    var grouped = compact.length !== raw.length;
    var dot = compact.lastIndexOf("."), comma = compact.lastIndexOf(",");
    var sep = Math.max(dot, comma), decimals = 0, value;
    var locDec = "."; try { locDec = (1.5).toLocaleString(lang).replace(/\d/g, ""); } catch (e) {}
    if (sep >= 0) {
      var ch = compact.charAt(sep), after = compact.length - sep - 1;
      // "1,250" is a thousands group in English, "3,5" a decimal in French.
      var single = compact.indexOf(ch) === sep;
      if ((dot >= 0 && comma >= 0) || (single && (after !== 3 || ch === locDec))) decimals = after;
      else grouped = true;
    }
    if (decimals) value = parseFloat(compact.slice(0, sep).replace(/[.,]/g, "") + "." + compact.slice(sep + 1));
    else value = parseFloat(compact.replace(/[.,]/g, ""));
    if (!isFinite(value)) return;
    var fmt;
    try { fmt = new Intl.NumberFormat(lang, { minimumFractionDigits: decimals, maximumFractionDigits: decimals, useGrouping: grouped }); }
    catch (e) { fmt = new Intl.NumberFormat(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals, useGrouping: grouped }); }
    var head = text.slice(0, m.index), tail = text.slice(m.index + raw.length);
    var token = {}, start = null, dur = 1400;
    el.__pfCount = token;
    el.textContent = head + fmt.format(0) + tail;
    requestAnimationFrame(function frame(now) {
      if (el.__pfCount !== token) return;               // restarted or stopped
      if (start === null) start = now;
      var t = Math.min(1, (now - start) / dur);
      if (t < 1) {
        el.textContent = head + fmt.format(value * (1 - Math.pow(1 - t, 3))) + tail;
        requestAnimationFrame(frame);
      } else {
        el.textContent = text;
        el.__pfCount = null;
      }
    });
  }

  const countStop = (el) => {
    el.__pfCount = null;
    if (el.__pfFinal !== undefined) el.textContent = el.__pfFinal;
  };

  const escAttr = (v) => String(v == null ? "" : v).replace(/&/g, "&amp;").replace(/"/g, "&quot;");

  class DeckStage extends HTMLElement {
    connectedCallback() {
      if (this._ready) return;
      this._ready = true;

      this.designW = Number(this.getAttribute("width")) || DESIGN_W;
      this.designH = Number(this.getAttribute("height")) || DESIGN_H;
      this.exitHint = this.getAttribute("exit-hint") || DEFAULT_EXIT_HINT;
      this._motion = this.getAttribute("motion") || "balanced";
      this._lang = document.documentElement.getAttribute("lang") || undefined;

      // Render mode (scripts/check_deck.py): the slides alone, finished, still.
      const pf = new URLSearchParams(location.search).get("pf");
      this._render = pf === "shot" || pf === "sheet" ? pf : null;
      if (this._render) {
        this._motion = "none";
        this.classList.add("pf-render");
        if (this._render === "sheet") this.classList.add("pf-sheet");
      }
      this.style.setProperty("--design-w", this.designW + "px");
      this.style.setProperty("--design-h", this.designH + "px");

      this.slides = Array.from(this.children).filter((c) => c.nodeType === 1);

      // Shapes that draw themselves (data-anim="draw") share one stroke length.
      this.querySelectorAll('[data-anim="draw"]').forEach((el) =>
        el.querySelectorAll(DRAW_SHAPES).forEach((s) => s.setAttribute("pathLength", "1")));

      // Create overlay and toast before builders so _buildStage can place
      // the overlay inside .pf-stage (centres it on the slide, not the viewport).
      this.overlay = el("div", "pf-overlay");
      // Announce slide changes to screen readers via the counter pill.
      this.overlay.setAttribute("role", "status");
      this.overlay.setAttribute("aria-live", "polite");
      this.toast   = el("div", "pf-toast");

      this._step           = 0;        // fragments revealed on the current slide
      this._fragmentEls    = [];       // .fragment elements of the current slide
      this._blank          = null;     // null | "black" | "white"
      this._warnedOverflow = new Set();

      // Saving back to disk only makes sense for a deck opened as a local
      // file: a hosted copy has no real "this file" to write to, and the
      // picker would just confuse people into choosing an unrelated file.
      this._canEdit = !this._render && "showOpenFilePicker" in window && location.protocol === "file:";

      this._buildRail();
      this._buildStage();    // appends overlay to this.stage
      this._buildControls();
      if (this._canEdit) this._buildEditing();
      this.append(this.toast);

      this.index = this._indexFromHash();
      this.show(this.index, { updateHash: false });
      this._layout();
      this._scaleThumbs();
      if (this._render) this._startRender();

      this._onResize = () => {
        this._layout();
        this._scaleThumbs();
        if (this._overview && this._overview.classList.contains("is-open")) this._scaleOverview();
      };
      this._onKey    = (e) => this._onKeyDown(e);
      this._onHash   = () => this.show(this._indexFromHash(), { updateHash: false });
      this._onMove   = () => this._markActive();
      this._onFs     = () => this._onFullscreenChange();

      window.addEventListener("resize",          this._onResize);
      window.addEventListener("keydown",         this._onKey);
      window.addEventListener("hashchange",      this._onHash);
      this.addEventListener("mousemove",         this._onMove);
      document.addEventListener("fullscreenchange",        this._onFs);
      document.addEventListener("webkitfullscreenchange",  this._onFs);
      if (!this._render) this._bindTouch();
    }

    disconnectedCallback() {
      window.removeEventListener("resize",     this._onResize);
      window.removeEventListener("keydown",    this._onKey);
      window.removeEventListener("hashchange", this._onHash);
      document.removeEventListener("fullscreenchange",       this._onFs);
      document.removeEventListener("webkitfullscreenchange", this._onFs);
      this._unbindDrawEvents();
      if (this._laserOnMove) this.stage.removeEventListener("mousemove", this._laserOnMove);
    }

    /* ------------------------------------------------------------------ */
    /* DOM construction                                                     */
    /* ------------------------------------------------------------------ */

    _buildStage() {
      this.stage  = el("div", "pf-stage");
      this.canvas = el("div", "pf-canvas");
      this.canvas.style.width  = this.designW + "px";
      this.canvas.style.height = this.designH + "px";
      this.canvas.setAttribute("data-motion", this._motion);
      this.canvas.setAttribute("data-dir", "next");
      this.slides.forEach((slide, i) => {
        slide.setAttribute("data-index", String(i));
        slide.setAttribute("role", "group");
        slide.setAttribute("aria-roledescription", "slide");
        this.canvas.appendChild(slide);
      });
      this.stage.appendChild(this.canvas);

      // Draw SVG overlay - same position/transform as canvas, scaled in sync.
      this._drawSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      this._drawSvg.setAttribute("class", "pf-draw-svg");
      this._drawSvg.setAttribute("viewBox", `0 0 ${this.designW} ${this.designH}`);
      this._drawSvg.style.width  = this.designW + "px";
      this._drawSvg.style.height = this.designH + "px";
      this.stage.appendChild(this._drawSvg);

      // Laser dot - tracks mouse, synced to audience.
      this._laserDot = el("div", "pf-laser-dot");
      this.stage.appendChild(this._laserDot);

      // Overlay lives inside the stage so left:50% centres it on the slide area.
      this.stage.appendChild(this.overlay);

      // Per-slide timer (visible in presenter mode only).
      this._slideTimerEl = el("div", "pf-slide-timer");
      this._slideTimerEl.textContent = "00:00";
      this.stage.appendChild(this._slideTimerEl);

      // Progress bar at the bottom of the stage.
      this._progressBar = el("div", "pf-progress-bar");
      this.stage.appendChild(this._progressBar);

      // Blank screen overlay (B = black, W = white).
      this._blankEl = el("div", "pf-blank");
      this.stage.appendChild(this._blankEl);

      // Keyboard shortcuts overlay.
      this._buildShortcuts();

      this._buildNotesUI();
      this.appendChild(this.stage);
    }

    _buildNotesUI() {
      // Backdrop: full-stage transparent div that sits above the slide but below
      // the panel. A click on it means "clicked outside the panel" -> close.
      this.notesBackdrop = el("div", "pf-notes-backdrop");
      this.notesBackdrop.addEventListener("click", () => this._closeNotes());

      // Floating panel: appears above the notes button (bottom-left).
      this.notesPanel = el("div", "pf-notes-panel");

      const header = el("div", "pf-notes-header");
      const heading = el("span", "pf-notes-heading");
      heading.textContent = "Speaker notes";

      const closeBtn = document.createElement("button");
      closeBtn.type      = "button";
      closeBtn.className = "pf-notes-close";
      closeBtn.setAttribute("aria-label", "Close notes");
      closeBtn.title     = "Close notes";
      closeBtn.textContent = "×";
      closeBtn.addEventListener("click", () => this._closeNotes());

      header.append(heading, closeBtn);

      this.notesTA = document.createElement("textarea");
      this.notesTA.className   = "pf-notes-ta";
      this.notesTA.setAttribute("aria-label", "Speaker notes");
      if (this._canEdit) {
        this.notesTA.placeholder = "Speaker notes for this slide. Start a line with - for a bullet.";
      } else {
        // No real save path here (hosted page, or a browser without the
        // File System Access API) - offer reading notes, never editing ones
        // that would silently be lost on reload.
        this.notesTA.placeholder = "No speaker notes for this slide.";
        this.notesTA.readOnly = true;
      }

      this.notesPanel.append(header, this.notesTA);

      // Toggle button (bottom-left of stage).
      this.notesBtn = document.createElement("button");
      this.notesBtn.type      = "button";
      this.notesBtn.className = "pf-btn pf-notes-btn";
      this.notesBtn.setAttribute("aria-label", "Speaker notes");
      this.notesBtn.title     = "Speaker notes";
      this.notesBtn.innerHTML = ICONS.editNotes;
      this.notesBtn.addEventListener("click", () => {
        if (this.notesPanel.classList.contains("is-open")) {
          this._closeNotes();
        } else {
          this._openNotes();
        }
      });

      this.stage.append(this.notesBackdrop, this.notesPanel, this.notesBtn);
    }

    _openNotes() {
      this._loadNotesForCurrentSlide();
      this.notesPanel.classList.add("is-open");
      this.notesBackdrop.classList.add("is-open");
      this.notesBtn.classList.add("is-active");
      requestAnimationFrame(() => this.notesTA.focus());
    }

    _closeNotes() {
      if (!this.notesPanel.classList.contains("is-open")) return;
      this._saveNotes();
      this.notesPanel.classList.remove("is-open");
      this.notesBackdrop.classList.remove("is-open");
      this.notesBtn.classList.remove("is-active");
    }

    _buildRail() {
      this.rail   = el("div", "pf-rail");
      this.thumbs = this.slides.map((slide, i) => {
        const thumb = el("button", "pf-thumb");
        thumb.type  = "button";
        thumb.setAttribute("aria-label", "Go to slide " + (i + 1));

        const num   = el("span", "pf-thumb-num");
        num.textContent = String(i + 1);

        const frame = el("span", "pf-thumb-frame");
        const mini  = el("span", "pf-thumb-canvas");
        mini.style.width  = this.designW + "px";
        mini.style.height = this.designH + "px";

        const clone = this._cloneSlide(slide);
        clone.removeAttribute("data-index");
        clone.removeAttribute("id");
        clone.querySelectorAll("[id]").forEach((n) => n.removeAttribute("id"));
        clone.querySelectorAll("aside.notes").forEach((n) => n.remove());

        mini.appendChild(clone);
        frame.appendChild(mini);
        thumb.append(num, frame);
        thumb.addEventListener("click", () => this.show(i));
        this.rail.appendChild(thumb);
        return thumb;
      });
      this.appendChild(this.rail);

      // Drag handle between rail and stage.
      this.resizer = el("div", "pf-rail-resizer");
      this.appendChild(this.resizer);
      this._bindRailResize();
    }

    _buildControls() {
      this.controls      = el("div", "pf-controls");
      this.prevBtn       = mkBtn("pf-prev",    "Previous slide",        ICONS.prev,    () => this.prev());
      this.nextBtn       = mkBtn("pf-next",    "Next slide",            ICONS.next,    () => this.next());
      this.drawBtn       = mkBtn("pf-draw",    "Draw mode (D)",         ICONS.draw,    () => this._toggleDraw());
      this.eraseBtn      = mkBtn("pf-erase",   "Clear drawing",         ICONS.erase,   () => this._clearDraw());
      this.laserBtn      = mkBtn("pf-laser",   "Laser pointer (L)",     ICONS.laser,   () => this._toggleLaser());
      this.helpBtn       = mkBtn("pf-help",    "Keyboard shortcuts (?)",ICONS.help,    () => this._toggleShortcuts());
      this.presenterBtn  = mkBtn("pf-present", "Presenter mode",        ICONS.present, () => this.togglePresenter());
      this.fsBtn         = mkBtn("pf-fs",      "Full screen",           ICONS.expand,  () => this.toggleFullscreen());
      this.controls.append(
        this.prevBtn, this.nextBtn,
        this.drawBtn, this.eraseBtn, this.laserBtn,
        this.helpBtn,
        this.presenterBtn, this.fsBtn
      );
      this.appendChild(this.controls);
    }

    /* ---- In-place text editing (local file, supporting browser only) - */
    /* Only built when the page can actually write the result back to    */
    /* disk: window.showOpenFilePicker exists AND this is a local file    */
    /* (a hosted copy has no real "this file" to save over).             */

    _buildEditing() {
      this._editing    = false;
      this._fileHandle = null;
      // What a block held when it got focus, so Esc can put it back exactly
      // (inline markup included) - kept out of the DOM so it is never saved.
      this._editOrig = new WeakMap();
      this._onEditableFocus = (e) => {
        const node = e.currentTarget;
        this._editOrig.set(node, { html: node.innerHTML, changed: node.hasAttribute("data-pf-changed") });
      };
      // data-pf-changed tells build.py which blocks to pull back into slides/.
      this._onEditableInput = (e) => e.currentTarget.setAttribute("data-pf-changed", "");
      this._onEditableKeyDown = (e) => {
        const node = e.currentTarget;
        if (e.key === "Enter") {
          e.preventDefault();
          node.blur();
        } else if (e.key === "Escape") {
          e.preventDefault();
          const orig = this._editOrig.get(node);
          if (orig) {
            node.innerHTML = orig.html;
            if (!orig.changed) node.removeAttribute("data-pf-changed");
          }
          node.blur();
        }
      };

      this.editBtn = mkBtn("pf-edit", "Edit", ICONS.editText, () => this._toggleEdit());
      this.saveBtn = mkBtn("pf-save", "Save", ICONS.save,     () => this._persistToDisk());
      this.editControls = el("div", "pf-edit-controls");
      this.editControls.append(this.editBtn, this.saveBtn);
      this.appendChild(this.editControls);
    }

    /* Resolve (once) the on-disk file we are allowed to write back to.
       Returns true once we hold read-write permission, false if the person
       cancelled the picker or declined the permission prompt. */
    async _ensureFileHandle() {
      if (this._fileHandle) return true;
      try {
        const name = decodeURIComponent(location.pathname.split("/").pop() || "index.html");
        this._showToast(`Choose "${name}" in the next window to turn on editing.`);
        const [handle] = await window.showOpenFilePicker({
          multiple: false,
          types: [{ description: "Presentation", accept: { "text/html": [".html", ".htm"] } }],
        });
        const perm = await handle.requestPermission({ mode: "readwrite" });
        if (perm !== "granted") {
          this._showToast("Editing needs permission to save this file.");
          return false;
        }
        this._fileHandle = handle;
        return true;
      } catch (err) {
        // AbortError = the person closed the picker; not a real error.
        if (err && err.name !== "AbortError") {
          this._showToast("Could not open that file for editing.");
        }
        return false;
      }
    }

    /* Every block build.py stamped as editable, across every slide. */
    _editableElements() {
      const all = [];
      this.slides.forEach((slide) => all.push(...slide.querySelectorAll(EDITABLE)));
      return all;
    }

    async _toggleEdit() {
      if (this._editing) {
        await this._exitEditMode();
      } else {
        if (!(await this._ensureFileHandle())) return;
        this._enterEditMode();
      }
    }

    _enterEditMode() {
      this._editing = true;
      this.classList.add("is-editing");
      this.editBtn.classList.add("is-active");
      this.editBtn.innerHTML = ICONS.exit;
      this.editBtn.title = "Done";
      this.editBtn.setAttribute("aria-label", "Done editing");

      // Figures show their real value while being edited, never a count.
      this.querySelectorAll("[data-count]").forEach(countStop);
      this._editableElements().forEach((node) => {
        // plaintext-only: typing and pasting add text, never stray markup.
        try { node.contentEditable = "plaintext-only"; } catch (_) { node.contentEditable = "true"; }
        node.classList.add("pf-editable");
        node.addEventListener("keydown", this._onEditableKeyDown);
        node.addEventListener("focus",   this._onEditableFocus);
        node.addEventListener("input",   this._onEditableInput);
      });
    }

    async _exitEditMode() {
      this._editing = false;
      this.classList.remove("is-editing");
      this.editBtn.classList.remove("is-active");
      this.editBtn.innerHTML = ICONS.editText;
      this.editBtn.title = "Edit";
      this.editBtn.setAttribute("aria-label", "Edit");

      this._editableElements().forEach((node) => {
        node.removeAttribute("contenteditable");
        node.classList.remove("pf-editable");
        if (!node.classList.length) node.removeAttribute("class");
        node.removeEventListener("keydown", this._onEditableKeyDown);
        node.removeEventListener("focus",   this._onEditableFocus);
        node.removeEventListener("input",   this._onEditableInput);
      });
      // A figure may have been edited: count to whatever it says now.
      this.querySelectorAll("[data-count]").forEach((el) => { el.__pfFinal = undefined; });

      await this._persistToDisk();
    }

    /* Write the deck back to disk, exactly as build.py would have produced it
       (plus whatever text was just edited) - never the live, JS-grown DOM. */
    async _persistToDisk() {
      if (!this._fileHandle) return;
      try {
        const html = this._serializeForSave();
        const writable = await this._fileHandle.createWritable();
        await writable.write(html);
        await writable.close();
        this._showToast("Saved.");
      } catch (err) {
        this._showToast("Could not save - check the file is still there and try again.");
      }
    }

    _serializeForSave() {
      // Engine state is stripped; the build's data-pf-* stamps and the
      // data-pf-changed marks stay, so build.py can pull the edits back.
      const cleanSlide = (slide) => {
        const clone = this._cloneSlide(slide);
        clone.removeAttribute("data-index");
        clone.removeAttribute("role");
        clone.removeAttribute("aria-roledescription");
        clone.querySelectorAll("[contenteditable]").forEach((n) => n.removeAttribute("contenteditable"));
        clone.querySelectorAll(".pf-editable").forEach((n) => {
          n.classList.remove("pf-editable");
          if (!n.classList.length) n.removeAttribute("class");
        });
        clone.querySelectorAll(".fragment").forEach((n) => n.classList.remove("is-visible", "pf-instant"));
        return clone.outerHTML;
      };

      const slidesHtml = this.slides.map(cleanSlide).join("\n");
      const script = document.querySelector("body > script:not([src])");
      const lang = document.documentElement.getAttribute("lang") || "en";
      const stageAttrs = ["width", "height", "transition", "motion", "exit-hint"]
        .filter((a) => this.hasAttribute(a))
        .map((a) => `${a}="${escAttr(this.getAttribute(a))}"`)
        .join(" ");

      return (
        "<!doctype html>\n" +
        `<html lang="${escAttr(lang)}">\n` +
        document.head.outerHTML + "\n" +
        "<body>\n" +
        `<deck-stage ${stageAttrs}>\n` +
        slidesHtml + "\n" +
        "</deck-stage>\n" +
        (script ? script.outerHTML : "") + "\n" +
        "</body>\n</html>\n"
      );
    }

    /* ------------------------------------------------------------------ */
    /* Navigation                                                           */
    /* ------------------------------------------------------------------ */

    get count() { return this.slides.length; }
    _clamp(i)   { return Math.max(0, Math.min(this.count - 1, i)); }

    _indexFromHash() {
      const raw = decodeURIComponent(location.hash.replace("#", ""));
      if (!raw) return 0;
      // Named anchor first (#intro), then slide number (#3).
      const byId = this.slides.findIndex((s) => s.id === raw);
      if (byId >= 0) return byId;
      const n = parseInt(raw, 10);
      return Number.isFinite(n) ? this._clamp(n - 1) : 0;
    }

    show(i, { updateHash = true, revealAll = false } = {}) {
      // Auto-save notes for the slide we are leaving, then reload for the new one.
      const editorOpen = this.notesPanel && this.notesPanel.classList.contains("is-open");
      if (editorOpen) this._saveNotes();
      // Leaving a slide while editing text writes it to disk too.
      if (this._editing) this._persistToDisk();

      const prevIndex = this.index;

      // Stop any media on the slide we are leaving (sound shouldn't linger).
      if (this.slides[prevIndex]) {
        this.slides[prevIndex].querySelectorAll("video, audio").forEach((m) => {
          try { m.pause(); } catch (_) {}
        });
      }
      // Changing slide clears a blanked screen (the _syncAudience below carries
      // the cleared state, so no separate sync is needed here).
      this._blank = null;
      this._blankEl.className = "pf-blank";

      this.index = this._clamp(i);
      const slide = this.slides[this.index];

      // Motion keys off the canvas: the direction (a slide already seen shows
      // finished, transitions mirror) and this slide's own transition. Set
      // before data-active so the incoming slide animates with them.
      const forward = this.index >= prevIndex || prevIndex === undefined;
      this.canvas.setAttribute("data-dir", forward ? "next" : "prev");
      this.canvas.setAttribute("data-transition",
        slide.getAttribute("data-transition") || this.getAttribute("transition") || "fade");

      this.slides.forEach((s, n) =>
        n === this.index ? s.setAttribute("data-active", "") : s.removeAttribute("data-active")
      );

      // Fragments: forward arrival reveals none, backward arrival reveals all,
      // at once (pf-instant), since those points were already made.
      this._fragmentEls = Array.from(slide.querySelectorAll(".fragment"));
      this._step = revealAll ? this._fragmentEls.length : 0;
      this._fragmentEls.forEach((f) => f.classList.toggle("pf-instant", revealAll));
      this._applyFragments();
      if (forward) this._runCounts(slide);

      this.thumbs.forEach((t, n) => t.classList.toggle("is-active", n === this.index));

      const active = this.thumbs[this.index];
      if (active) {
        // scrollIntoView with options: Safari 15+. Fallback for older browsers.
        try { active.scrollIntoView({ block: "nearest" }); }
        catch (_) { active.scrollIntoView(false); }
      }

      this.overlay.textContent = `${this.index + 1} / ${this.count}`;
      this.prevBtn.disabled = this.index === 0;
      this.nextBtn.disabled = this.index === this.count - 1;

      this._markActive();
      this._syncAudience(this.index);
      this._updatePresenterView();
      this._updateProgressBar();
      if (this._overview) this._highlightOverview();

      if (editorOpen) this._loadNotesForCurrentSlide();
      requestAnimationFrame(() => this._checkOverflow());

      if (updateHash) {
        const id = this.slides[this.index].id;
        const h = "#" + (id || (this.index + 1));
        if (location.hash !== h) history.replaceState(null, "", h);
      }
    }

    next() {
      if (this._blank) { this._setBlank(null); return; }   // a key resumes from blank
      if (this._revealNext()) return;                       // reveal a fragment, stay
      if (this.index < this.count - 1) this.show(this.index + 1);
    }

    prev() {
      if (this._blank) { this._setBlank(null); return; }
      if (this._revealPrev()) return;                       // hide a fragment, stay
      if (this.index > 0) this.show(this.index - 1, { revealAll: true });
    }

    /* ---- fragments (progressive reveal) ---- */

    _applyFragments() {
      this._fragmentEls.forEach((f, n) => f.classList.toggle("is-visible", n < this._step));
    }

    _revealNext() {
      if (this._step >= this._fragmentEls.length) return false;
      const frag = this._fragmentEls[this._step];
      frag.classList.remove("pf-instant");
      this._step++;
      this._applyFragments();
      this._runCounts(frag);
      this._syncAudience(this.index);
      this._updatePresenterView();
      return true;
    }

    _revealPrev() {
      if (this._step <= 0) return false;
      this._step--;
      this._applyFragments();
      this._syncAudience(this.index);
      this._updatePresenterView();
      return true;
    }

    /* ---- blank screen (B / W) ---- */

    _setBlank(color) {
      this._blank = color || null;
      this._blankEl.className = "pf-blank" + (this._blank ? " is-" + this._blank : "");
      this._syncAudience(this.index);
    }

    _toggleBlank(color) {
      this._setBlank(this._blank === color ? null : color);
    }

    /* ---- dev overflow warning ---- */

    _checkOverflow() {
      const s = this.slides[this.index];
      if (!s || this._warnedOverflow.has(this.index)) return;
      if (s.scrollHeight > this.designH + 2) {
        this._warnedOverflow.add(this.index);
        console.warn(
          `[deck-stage] Slide ${this.index + 1} overflows the ${this.designW}×${this.designH} ` +
          `canvas (content is ${s.scrollHeight}px tall) and will be clipped.`
        );
      }
    }

    _onKeyDown(e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      // Let the user type freely in the notes textarea, any input, or a text
      // block being edited in place. Checked on e.target, not activeElement:
      // Enter / Esc blur an edited block before this listener runs.
      const t = e.target;
      if (t && (t.tagName === "TEXTAREA" || t.tagName === "INPUT" || t.isContentEditable)) return;
      switch (e.key) {
        case "ArrowRight": case "ArrowDown": case "PageDown": case " ":
          e.preventDefault(); this.next(); break;
        case "ArrowLeft": case "ArrowUp": case "PageUp":
          e.preventDefault(); this.prev(); break;
        case "Home": e.preventDefault(); this.show(0);              break;
        case "End":  e.preventDefault(); this.show(this.count - 1); break;
        case "f": case "F":
          e.preventDefault(); this.toggleFullscreen(); break;
        case "p": case "P":
          e.preventDefault(); this.togglePresenter(); break;
        case "d": case "D":
          e.preventDefault(); this._toggleDraw(); break;
        case "l": case "L":
          e.preventDefault(); this._toggleLaser(); break;
        case "b": case "B":
          e.preventDefault(); this._toggleBlank("black"); break;
        case "w": case "W":
          e.preventDefault(); this._toggleBlank("white"); break;
        case "o": case "O":
          e.preventDefault(); this._toggleOverview(); break;
        case "?":
          e.preventDefault(); this._toggleShortcuts(); break;
        case "Escape":
          if (this._overview && this._overview.classList.contains("is-open")) {
            e.preventDefault(); this._toggleOverview(false); break;
          }
          if (this._shortcutsOverlay && this._shortcutsOverlay.classList.contains("is-open")) {
            e.preventDefault(); this._toggleShortcuts(false); break;
          }
          if (this._blank) { e.preventDefault(); this._setBlank(null); break; }
          // Intercept Esc in presenter mode before the browser acts on it.
          if (this._presenterActive) {
            e.preventDefault();
            e.stopImmediatePropagation();
            this.exitPresenterMode();
          }
          break;
        default:
          if (/^[1-9]$/.test(e.key)) { e.preventDefault(); this.show(Number(e.key) - 1); }
      }
    }

    _bindTouch() {
      if (!matchMedia("(hover: none)").matches) return;
      let x0 = 0, y0 = 0;
      this.stage.addEventListener("touchstart", (e) => {
        const t = e.changedTouches[0];
        x0 = t.clientX; y0 = t.clientY;
      }, { passive: true });
      this.stage.addEventListener("touchend", (e) => {
        if (e.target.closest(INTERACTIVE)) return;
        const t  = e.changedTouches[0];
        const dx = t.clientX - x0, dy = t.clientY - y0;
        // Horizontal swipe wins; otherwise a tap on the left/right half navigates.
        if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) {
          dx < 0 ? this.next() : this.prev();
        } else if (Math.abs(dx) < 12 && Math.abs(dy) < 12) {
          const r = this.stage.getBoundingClientRect();
          t.clientX < r.left + r.width / 2 ? this.prev() : this.next();
        }
      }, { passive: true });
    }

    /* ------------------------------------------------------------------ */
    /* Full screen & presenter mode                                        */
    /* ------------------------------------------------------------------ */

    // ⤢ button / f key - single-screen full screen on all browsers.
    toggleFullscreen() {
      if (this._presenterActive) return; // presenter mode has its own exit button
      if (fsEl()) {
        (document.exitFullscreen || document.webkitExitFullscreen).call(document);
        return;
      }
      // Request fullscreen on `this` (the whole <deck-stage>), NOT on a child
      // div. Safari only shows the fullscreen element + its descendants, so
      // requesting on a child would hide the sibling controls and toast.
      const req = this.requestFullscreen || this.webkitRequestFullscreen;
      if (req) req.call(this).catch(() => {});
    }

    // 🖥 button / p key - presenter mode on all browsers.
    // Opens a popup audience window (place it on the second screen).
    // screen.isExtended (Chrome-only) is no longer used for detection -
    // the user triggers this explicitly, so it works on Safari and Firefox too.
    togglePresenter() {
      if (this._presenterActive) {
        this.exitPresenterMode();
      } else {
        this._openPresenter();
      }
    }

    _onFullscreenChange() {
      if (this._presenterActive) return;
      // !!fsEl() is sufficient - we are the only caller of requestFullscreen.
      const on = !!fsEl();
      this.classList.toggle("is-fullscreen", on);
      this.fsBtn.innerHTML = on ? ICONS.compress : ICONS.expand;
      const label = on ? "Exit full screen" : "Full screen";
      this.fsBtn.setAttribute("aria-label", label);
      this.fsBtn.title = label;
      if (on) {
        this._showToast(this.exitHint);
        // Make buttons visible immediately; they fade after IDLE_MS without movement.
        this._markActive();
        // Close the notes panel - not available in full-screen mode.
        this._closeNotes();
      }
      requestAnimationFrame(() => { this._layout(); this._scaleThumbs(); });
    }

    /* ---- Presenter mode --------------------------------------------- */

    async _openPresenter() {
      // 1. Open the popup SYNCHRONOUSLY (before any await) so that popup
      //    blockers in Safari and Firefox see the user-gesture context.
      //    about:blank is always same-origin with the opener - no restrictions.
      const left = (window.screen.availLeft || 0) + window.screen.availWidth;
      const top  = window.screen.availTop  || 0;
      const w    = window.screen.availWidth;
      const h    = window.screen.availHeight;
      const features = `left=${left},top=${top},width=${w},height=${h},popup=1`;
      const win = window.open("about:blank", "_blank", features);

      if (!win) {
        // Popup blocked - fall back to single-screen fullscreen.
        const req = this.requestFullscreen || this.webkitRequestFullscreen;
        if (req) req.call(this).catch(() => {});
        return;
      }

      // 2. Now we can await - try to move the popup to the secondary screen.
      if ("getScreenDetails" in window) {
        try {
          const details   = await window.getScreenDetails();
          const secondary = details.screens.find((s) => !s.isPrimary);
          if (secondary && !win.closed) {
            try { win.moveTo(secondary.availLeft, secondary.availTop); }   catch {}
            try { win.resizeTo(secondary.availWidth, secondary.availHeight); } catch {}
          }
        } catch { /* permission denied - initial offset heuristic stands */ }
      }

      if (win.closed) return;

      // 3. Write the audience document into the same-origin about:blank window.
      win.document.write(this._buildAudienceHTML());
      win.document.close();

      win.addEventListener("beforeunload", () => {
        if (this._presenterActive) this.exitPresenterMode();
      });

      // Forward navigation commands sent by the audience window keyboard handler.
      this._audienceKeyHandler = (e) => {
        if (!this._presenterActive || !e.data || !e.data.pfKeyNav) return;
        switch (e.data.pfKeyNav) {
          case "next":           this.next();                    break;
          case "prev":           this.prev();                    break;
          case "first":          this.show(0);                   break;
          case "last":           this.show(this.count - 1);      break;
          case "exit-presenter": this.exitPresenterMode();       break;
        }
      };
      window.addEventListener("message", this._audienceKeyHandler);

      this._audienceWin     = win;
      this._presenterActive = true;
      this.classList.add("is-presenter");
      this.presenterBtn.innerHTML = ICONS.compress;
      this.presenterBtn.setAttribute("aria-label", "Exit presenter mode");
      this.presenterBtn.title = "Exit presenter mode";
      this._buildPresenterSidebar();
      // Rescale the main slide now that the stage shares its width with the
      // sidebar - otherwise the canvas keeps its windowed scale and gets clipped.
      requestAnimationFrame(() => this._layout());
      // Sync the current slide index. Also re-sync after a short delay in case
      // the audience window is still loading when the first postMessage is sent.
      this._syncAudience(this.index);
      setTimeout(() => this._syncAudience(this.index), 600);
      this._updatePresenterView();
    }

    exitPresenterMode() {
      if (!this._presenterActive) return;
      this._presenterActive = false;
      this.classList.remove("is-presenter");

      const win = this._audienceWin;
      this._audienceWin = null;
      if (win && !win.closed) win.close();

      if (this._audienceKeyHandler) {
        window.removeEventListener("message", this._audienceKeyHandler);
        this._audienceKeyHandler = null;
      }

      // Turn off any active tool before tearing down the sidebar buttons.
      if (this._laserActive) this._setLaser(false);
      if (this._drawActive)  this._setDraw(false);

      if (this._presenterResizer) { this._presenterResizer.remove(); this._presenterResizer = null; }
      if (this._presenterSidebar) { this._presenterSidebar.remove(); this._presenterSidebar = null; }
      this._presenterDrawBtn = this._presenterLaserBtn = null;
      clearInterval(this._timerInterval);
      clearInterval(this._slideTimerInterval);
      clearInterval(this._scrollInterval);
      this._scrollActive = false;
      this._lastPresenterIndex = undefined;

      this.presenterBtn.innerHTML = ICONS.present;
      this.presenterBtn.setAttribute("aria-label", "Presenter mode");
      this.presenterBtn.title = "Presenter mode";

      requestAnimationFrame(() => { this._layout(); this._scaleThumbs(); });
    }

    _syncAudience(i) {
      if (this._audienceWin && !this._audienceWin.closed) {
        const notesEl = this.slides[i] && this.slides[i].querySelector("aside.notes");
        this._audienceWin.postMessage({
          pfSlide: i,
          pfStep:  this._step || 0,
          pfNotes: notesEl ? notesEl.innerHTML : "",
          pfBlank: this._blank || null,
          pfDir:   this.canvas.getAttribute("data-dir"),
          pfTransition: this.canvas.getAttribute("data-transition"),
        }, "*");
      }
    }

    /* ---- Rail resize ------------------------------------------------- */

    _bindRailResize() {
      this.resizer.addEventListener("mousedown", (e) => {
        e.preventDefault();
        const startX = e.clientX;
        const startW = this.rail.offsetWidth;
        this.resizer.classList.add("is-dragging");
        document.body.style.cursor    = "col-resize";
        document.body.style.userSelect = "none";

        const onMove = (ev) => {
          const w = Math.max(160, Math.min(600, startW + ev.clientX - startX));
          this.rail.style.flex = `0 0 ${w}px`;
          this._layout();
          this._scaleThumbs();
        };
        const onUp = () => {
          this.resizer.classList.remove("is-dragging");
          document.body.style.cursor    = "";
          document.body.style.userSelect = "";
          window.removeEventListener("mousemove", onMove);
          window.removeEventListener("mouseup",   onUp);
        };
        window.addEventListener("mousemove", onMove);
        window.addEventListener("mouseup",   onUp);
      });
    }

    _loadNotesForCurrentSlide() {
      const slide   = this.slides[this.index];
      const notesEl = slide && slide.querySelector("aside.notes");
      this.notesTA.value = notesEl ? notesToText(notesEl) : "";
      this._notesLoaded  = this.notesTA.value;
    }

    _saveNotes() {
      const slide = this.slides[this.index];
      if (!slide) return;
      // Nothing typed: leave the authored notes, and their HTML, untouched.
      if (this.notesTA.value === this._notesLoaded) return;
      this._notesLoaded = this.notesTA.value;
      let notesEl  = slide.querySelector("aside.notes");
      const text   = this.notesTA.value.trim();
      // The data-pf-* marks below are what build.py reads to pull the change
      // back into the slide file.
      if (text) {
        if (!notesEl) {
          notesEl = document.createElement("aside");
          notesEl.className = "notes";
          // Notes cleared then written again are an edit of the original ones.
          const removed = slide.getAttribute("data-pf-notes-removed");
          if (removed) {
            notesEl.setAttribute("data-pf-notes", removed);
            slide.removeAttribute("data-pf-notes-removed");
          }
          slide.appendChild(notesEl);
        }
        textToNotes(notesEl, text);
        notesEl.setAttribute("data-pf-changed", "");
      } else if (notesEl) {
        const original = notesEl.getAttribute("data-pf-notes");
        if (original) slide.setAttribute("data-pf-notes-removed", original);
        notesEl.remove();
      }
      this._updatePresenterView();
      // Notes only reach disk once editing has been turned on at least once
      // (that's the one action that asks for file permission) - never prompt
      // a file picker just because someone closed the notes panel.
      if (this._fileHandle) this._persistToDisk();
    }

    /* ---- Presenter sidebar ------------------------------------------ */

    _buildPresenterSidebar() {
      this._presenterSidebar = el("div", "pf-presenter-sidebar");

      // --- Next slide section ---
      const nextLabel = el("p", "pf-presenter-label");
      nextLabel.textContent = "Next slide";

      this._nextFrame  = el("div", "pf-next-frame");
      this._nextCanvas = el("div", "pf-next-canvas");
      this._nextCanvas.style.width  = this.designW + "px";
      this._nextCanvas.style.height = this.designH + "px";
      this._nextSlot   = el("div", "pf-next-slot");
      this._nextCanvas.appendChild(this._nextSlot);
      this._nextFrame.appendChild(this._nextCanvas);

      // --- Notes section ---
      const notesLabel = el("p", "pf-presenter-label");
      notesLabel.textContent = "Notes";

      // Auto-scroll + font-size controls
      const scrollBar = el("div", "pf-scroll-bar");
      this._scrollActive = false;
      this._scrollSpeed  = "medium";
      this._scrollBtn = mkBtn("pf-scroll-toggle", "Auto-scroll notes", ICONS.play, () => this._toggleScroll());
      const speedSel = document.createElement("select");
      speedSel.className = "pf-scroll-speed";
      speedSel.setAttribute("aria-label", "Scroll speed");
      [["slow", "Slow"], ["medium", "Medium"], ["fast", "Fast"]].forEach(([val, lbl]) => {
        const opt = document.createElement("option");
        opt.value = val;
        opt.textContent = lbl;
        if (val === "medium") opt.selected = true;
        speedSel.appendChild(opt);
      });
      speedSel.addEventListener("change", (e) => { this._scrollSpeed = e.target.value; });

      const spacer = el("span", "pf-scroll-spacer");
      if (this._notesFontSize === undefined) this._notesFontSize = 17;
      const fontDown = el("button", "pf-font-btn"); fontDown.type = "button";
      fontDown.textContent = "A-"; fontDown.title = "Smaller notes text";
      fontDown.setAttribute("aria-label", "Smaller notes text");
      const fontUp = el("button", "pf-font-btn"); fontUp.type = "button";
      fontUp.textContent = "A+"; fontUp.title = "Larger notes text";
      fontUp.setAttribute("aria-label", "Larger notes text");
      fontDown.addEventListener("click", () => this._setNotesFont(this._notesFontSize - 2));
      fontUp.addEventListener("click",   () => this._setNotesFont(this._notesFontSize + 2));
      scrollBar.append(this._scrollBtn, speedSel, spacer, fontDown, fontUp);

      this._notesEl = el("div", "pf-notes");
      this._notesEl.style.fontSize = this._notesFontSize + "px";

      // --- Tools row: pen / eraser / laser (synced to the audience) ---
      const toolsRow = el("div", "pf-presenter-tools");
      this._presenterDrawBtn  = mkBtn("", "Draw mode (D)",     ICONS.draw,  () => this._toggleDraw());
      const presenterEraseBtn = mkBtn("", "Clear drawing",     ICONS.erase, () => this._clearDraw());
      this._presenterLaserBtn = mkBtn("", "Laser pointer (L)", ICONS.laser, () => this._toggleLaser());
      if (this._drawActive)  this._presenterDrawBtn.classList.add("is-active");
      if (this._laserActive) this._presenterLaserBtn.classList.add("is-active");
      toolsRow.append(this._presenterDrawBtn, presenterEraseBtn, this._presenterLaserBtn);

      // --- Bar: prev/count/next | timer + reset | exit ---
      const bar = el("div", "pf-presenter-bar");

      this._presenterPrev  = mkBtn("", "Previous slide", ICONS.prev, () => this.prev());
      this._presenterNext  = mkBtn("", "Next slide",      ICONS.next, () => this.next());
      this._presenterCount = el("span", "pf-presenter-count");
      this._clockEl        = el("span", "pf-clock");      // wall-clock time
      this._timerEl        = el("span", "pf-timer");      // elapsed time

      // Reset both timers together: resetting the global presentation timer
      // also restarts the per-slide timer, so the two stay in sync from zero.
      const resetBtn = mkBtn("pf-timer-reset", "Reset timer", ICONS.reset, () => {
        const now = Date.now();
        this._timerStart = now;
        this._updateTimer();
        this._slideTimerStart = now;
        if (this._slideTimerEl) this._slideTimerEl.textContent = "00:00";
      });

      const exitBtn = mkBtn("pf-exit-btn", "Exit presentation", ICONS.exit,
        () => this._showExitConfirm(true));
      bar.append(this._presenterPrev, this._presenterCount, this._presenterNext, this._clockEl, this._timerEl, resetBtn, exitBtn);

      // Exit confirmation popover (hidden until the exit button is clicked).
      this._exitConfirm = el("div", "pf-exit-confirm");
      const exitMsg = el("p", "pf-exit-confirm-msg");
      exitMsg.textContent = "Exit the presentation?";
      const exitYes = el("button", "pf-exit-confirm-yes"); exitYes.type = "button";
      exitYes.textContent = "Exit";
      exitYes.addEventListener("click", () => this.exitPresenterMode());
      const exitNo = el("button", "pf-exit-confirm-no"); exitNo.type = "button";
      exitNo.textContent = "Cancel";
      exitNo.addEventListener("click", () => this._showExitConfirm(false));
      const exitBtns = el("div", "pf-exit-confirm-btns");
      exitBtns.append(exitNo, exitYes);
      this._exitConfirm.append(exitMsg, exitBtns);

      this._presenterSidebar.append(nextLabel, this._nextFrame, notesLabel, scrollBar, this._notesEl, toolsRow, bar, this._exitConfirm);

      // Draggable divider so the user can adjust the slide / sidebar split.
      this._presenterResizer = el("div", "pf-presenter-resizer");
      this._bindPresenterResize();
      this.appendChild(this._presenterResizer);
      this.appendChild(this._presenterSidebar);

      // Global presentation timer + wall clock
      this._timerStart = Date.now();
      this._updateTimer();
      this._updateClock();
      this._timerInterval = setInterval(() => { this._updateTimer(); this._updateClock(); }, 1000);

      // Per-slide timer (ticks against this._slideTimerStart, reset on slide change)
      this._slideTimerStart = Date.now();
      this._slideTimerInterval = setInterval(() => {
        if (!this._slideTimerEl) return;
        const s = Math.floor((Date.now() - this._slideTimerStart) / 1000);
        this._slideTimerEl.textContent = `${pad2(Math.floor(s / 60))}:${pad2(s % 60)}`;
      }, 1000);

      requestAnimationFrame(() => this._scaleNextPreview());
    }

    _setNotesFont(px) {
      this._notesFontSize = Math.max(11, Math.min(34, px));
      if (this._notesEl) this._notesEl.style.fontSize = this._notesFontSize + "px";
    }

    _showExitConfirm(show) {
      if (this._exitConfirm) this._exitConfirm.classList.toggle("is-open", show);
    }

    _bindPresenterResize() {
      this._presenterResizer.addEventListener("mousedown", (e) => {
        e.preventDefault();
        const startX = e.clientX;
        const startW = this._presenterSidebar.offsetWidth;
        this._presenterResizer.classList.add("is-dragging");
        document.body.style.cursor     = "col-resize";
        document.body.style.userSelect = "none";

        const onMove = (ev) => {
          // Sidebar is on the right: dragging left widens it.
          const max = window.innerWidth * 0.75;
          const w   = Math.max(280, Math.min(max, startW - (ev.clientX - startX)));
          this._presenterSidebar.style.flex = `0 0 ${w}px`;
          this._layout();
        };
        const onUp = () => {
          this._presenterResizer.classList.remove("is-dragging");
          document.body.style.cursor     = "";
          document.body.style.userSelect = "";
          window.removeEventListener("mousemove", onMove);
          window.removeEventListener("mouseup",   onUp);
        };
        window.addEventListener("mousemove", onMove);
        window.addEventListener("mouseup",   onUp);
      });
    }

    _updatePresenterView() {
      if (!this._presenterActive || !this._presenterSidebar) return;

      const indexChanged = this._lastPresenterIndex !== this.index;
      this._lastPresenterIndex = this.index;

      // Next slide preview
      const next = this.slides[this.index + 1];
      this._nextSlot.innerHTML = "";
      if (next) {
        const clone = this._cloneSlide(next);
        clone.querySelectorAll("aside.notes").forEach((n) => n.remove());
        this._nextSlot.appendChild(clone);
        this._nextCanvas.style.opacity = "1";
      } else {
        const msg = el("div", "pf-next-end");
        msg.textContent = "End of presentation";
        this._nextSlot.appendChild(msg);
        this._nextCanvas.style.opacity = "0.4";
      }
      this._scaleNextPreview();

      // Notes
      const curr      = this.slides[this.index];
      const notesNode = curr && curr.querySelector("aside.notes");
      this._notesEl.innerHTML = notesNode
        ? notesNode.innerHTML
        : '<span class="pf-no-notes">No notes for this slide.</span>';

      // On slide change: reset scroll, stop auto-scroll, reset per-slide timer.
      if (indexChanged) {
        this._notesEl.scrollTop = 0;
        if (this._scrollActive) this._toggleScroll();
        this._slideTimerStart = Date.now();
        if (this._slideTimerEl) this._slideTimerEl.textContent = "00:00";
      }

      // Counter (+ fragment step when the slide has fragments) + buttons state
      const total = this._fragmentEls ? this._fragmentEls.length : 0;
      let label = `${this.index + 1} / ${this.count}`;
      if (total) label += `  ·  step ${this._step}/${total}`;
      this._presenterCount.textContent = label;
      this._presenterPrev.disabled     = this.index === 0;
      this._presenterNext.disabled     = this.index === this.count - 1;
    }

    _scaleNextPreview() {
      if (!this._nextFrame) return;
      const w = this._nextFrame.clientWidth;
      if (!w) return;
      const scale = w / this.designW;
      this._nextCanvas.style.transform       = `scale(${scale})`;
      this._nextCanvas.style.transformOrigin = "top left";
    }

    _updateTimer() {
      if (!this._timerEl) return;
      const s = Math.floor((Date.now() - this._timerStart) / 1000);
      this._timerEl.textContent = `${pad2(Math.floor(s / 60))}:${pad2(s % 60)}`;
    }

    _updateClock() {
      if (!this._clockEl) return;
      const d = new Date();
      this._clockEl.textContent = `${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
    }

    _toggleScroll() {
      if (this._scrollActive) {
        this._scrollActive = false;
        clearInterval(this._scrollInterval);
        if (this._scrollBtn) {
          this._scrollBtn.innerHTML = ICONS.play;
          this._scrollBtn.classList.remove("is-scrolling");
        }
      } else {
        this._scrollActive = true;
        if (this._scrollBtn) {
          this._scrollBtn.innerHTML = ICONS.pause;
          this._scrollBtn.classList.add("is-scrolling");
        }
        this._startScroll();
      }
    }

    _startScroll() {
      clearInterval(this._scrollInterval);
      const pxPerTick = { slow: 0.5, medium: 1.2, fast: 2.8 }[this._scrollSpeed] || 1.2;
      this._scrollInterval = setInterval(() => {
        if (!this._notesEl) return;
        this._notesEl.scrollTop += pxPerTick;
        const atEnd = this._notesEl.scrollTop + this._notesEl.clientHeight >= this._notesEl.scrollHeight - 1;
        if (atEnd) this._toggleScroll();
      }, 16);
    }

    /* ---- Copies of a slide, and figures that count ---------------------- */

    /* A copy for the rail, the overview, the next-slide preview, the audience
       window or a save: a figure caught mid-count shows its real value. */
    _cloneSlide(slide) {
      const clone = slide.cloneNode(true);
      clone.removeAttribute("data-active");
      const live = slide.querySelectorAll("[data-count]");
      if (live.length) {
        const copies = clone.querySelectorAll("[data-count]");
        live.forEach((n, k) => {
          if (n.__pfFinal !== undefined && copies[k]) copies[k].textContent = n.__pfFinal;
        });
      }
      return clone;
    }

    _countsAllowed() {
      return COUNT_LEVELS.indexOf(this._motion) >= 0 &&
        !matchMedia("(prefers-reduced-motion: reduce)").matches;
    }

    /* Count up the figures in root (a slide, or a fragment just revealed),
       skipping those still hidden in a fragment. */
    _runCounts(root) {
      if (!root || this._editing || !this._countsAllowed()) return;
      const els = Array.from(root.querySelectorAll("[data-count]"));
      if (root.matches("[data-count]")) els.unshift(root);
      els.forEach((n) => {
        if (!n.closest(".fragment:not(.is-visible)")) countUp(n, this._lang);
      });
    }

    /* ---- Render mode: screenshots and the layout report ----------------- */

    _startRender() {
      // The slide as it finally looks: every fragment shown, nothing moving.
      this._step = this._fragmentEls.length;
      this._applyFragments();
      if (this._render === "sheet") {
        this._toggleOverview(true);
        this._scaleOverview();
      }
      const fonts = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
      fonts.then(() => new Promise((r) => setTimeout(r, 150))).then(() => {
        const issues = this._layoutIssues();
        if (this._render === "sheet") {
          issues.forEach((it) => this._ovCells[it.slide - 1].classList.add("is-flagged"));
        }
        const report = {
          slides: this.count,
          files: this.slides.map((sl) => sl.getAttribute("data-pf-src") || ""),
          issues,
          sheetHeight: this._overview ? Math.ceil(this._overview.scrollHeight) : 0,
        };
        const tag = document.createElement("script");
        tag.type = "application/json";
        tag.id = "pf-report";
        tag.textContent = JSON.stringify(report).replace(/</g, "\\u003c");
        document.body.appendChild(tag);
      });
    }

    /* What a careful reviewer would flag on each slide: content poking out of
       the 1920x1080 canvas, content cut off inside its own box (a long code
       line, a fixed-height card), and images that failed to load. Decoration
       (aria-hidden, .fx, empty boxes) and speaker notes are ignored. */
    _layoutIssues() {
      const TOL = 2;
      const issues = [];
      const label = (n) => {
        const cls = Array.from(n.classList).filter((c) => !/^(pf-|is-visible)/.test(c));
        const text = (n.textContent || "").replace(/\s+/g, " ").trim().slice(0, 70);
        return { element: n.tagName.toLowerCase() + (cls.length ? "." + cls.join(".") : ""), text };
      };
      this.slides.forEach((slide, i) => {
        const box = slide.getBoundingClientRect();
        if (!box.width) return;
        const k = box.width / this.designW;           // rendered px per design px
        const base = { slide: i + 1, file: slide.getAttribute("data-pf-src") || "" };
        const out = [];
        // Only what a viewer would miss: text, images, media. An empty box
        // that is hidden or bleeds off on purpose is decoration.
        const shows = (n) => (n.textContent || "").trim() !== "" ||
          n.matches("img, svg, video, canvas, iframe") || !!n.querySelector("img, svg, video, canvas, iframe");
        const clips = new Map();     // element -> does it cut off its overflow?
        const clipsOverflow = (n) => {
          if (!clips.has(n)) {
            const cs = getComputedStyle(n);
            clips.set(n, cs.overflowX !== "visible" || cs.overflowY !== "visible");
          }
          return clips.get(n);
        };
        // Inside a box that cuts it off, an element can't show past the slide;
        // that box reports the cut instead.
        const insideClip = (n) => {
          for (let a = n.parentElement; a && a !== slide; a = a.parentElement) {
            if (clipsOverflow(a)) return true;
          }
          return false;
        };
        slide.querySelectorAll("*").forEach((n) => {
          if (n.closest('aside.notes, [aria-hidden="true"], .fx, script, style') || !shows(n)) return;
          const r = n.getBoundingClientRect();
          if (!r.width && !r.height) return;
          const edges = {
            top: (box.top - r.top) / k,
            bottom: (r.bottom - box.bottom) / k,
            left: (box.left - r.left) / k,
            right: (r.right - box.right) / k,
          };
          const edge = Object.keys(edges).reduce((a, b) => (edges[b] > edges[a] ? b : a));
          if (edges[edge] > TOL && !insideClip(n)) out.push({ n, edge, px: Math.round(edges[edge]) });
          if (clipsOverflow(n) &&
              (n.scrollWidth > n.clientWidth + TOL || n.scrollHeight > n.clientHeight + TOL)) {
            const px = Math.max(n.scrollWidth - n.clientWidth, n.scrollHeight - n.clientHeight);
            issues.push(Object.assign({ kind: "clipped", px: Math.round(px / k) }, base, label(n)));
          }
          if (n.tagName === "IMG" && n.complete && !n.naturalWidth) {
            issues.push(Object.assign({ kind: "image" }, base, { element: "img", text: (n.getAttribute("src") || "").slice(0, 70) }));
          }
        });
        // Report only the outermost element that pokes out: its children
        // follow it and would only repeat the same problem.
        out.filter((o) => !out.some((p) => p !== o && p.n.contains(o.n))).forEach((o) => {
          issues.push(Object.assign({ kind: "overflow", edge: o.edge, px: o.px }, base, label(o.n)));
        });
      });
      return issues;
    }

    /* ---- Progress bar ------------------------------------------------- */

    _updateProgressBar() {
      if (!this._progressBar) return;
      const pct = this.count > 1 ? (this.index / (this.count - 1)) * 100 : 100;
      this._progressBar.style.width = pct + "%";
    }

    /* ---- Keyboard shortcuts overlay ----------------------------------- */

    _buildShortcuts() {
      this._shortcutsOverlay = el("div", "pf-shortcuts-overlay");
      const box   = el("div", "pf-shortcuts-box");
      const title = el("p",   "pf-shortcuts-title");
      title.textContent = "Keyboard shortcuts";

      const grid = el("div", "pf-shortcuts-grid");
      [
        ["→ / ↓ / Space",  "Next slide"],
        ["← / ↑",          "Previous slide"],
        ["Home",            "First slide"],
        ["End",             "Last slide"],
        ["1 - 9",           "Jump to slide"],
        ["f",               "Toggle fullscreen"],
        ["p",               "Toggle presenter mode"],
        ["o",               "Overview (all slides)"],
        ["d",               "Toggle draw mode"],
        ["l",               "Toggle laser pointer"],
        ["b / w",           "Black / white screen"],
        ["?",               "Show/hide this overlay"],
        ["Esc",             "Close overlay / exit presenter"],
      ].forEach(([key, label]) => {
        const k = el("kbd", "pf-shortcut-key");   k.textContent = key;
        const l = el("span", "pf-shortcut-label"); l.textContent = label;
        grid.append(k, l);
      });

      const closeRow = el("div", "pf-shortcuts-close-row");
      const closeBtn = document.createElement("button");
      closeBtn.type = "button";
      closeBtn.className = "pf-btn pf-shortcuts-close-btn";
      closeBtn.textContent = "Close";
      closeBtn.addEventListener("click", () => this._toggleShortcuts(false));
      closeRow.appendChild(closeBtn);
      box.append(title, grid, closeRow);
      this._shortcutsOverlay.appendChild(box);

      // Click outside the box to close.
      this._shortcutsOverlay.addEventListener("click", (e) => {
        if (e.target === this._shortcutsOverlay) this._toggleShortcuts(false);
      });
      this.stage.appendChild(this._shortcutsOverlay);
    }

    _toggleShortcuts(force) {
      const show = force !== undefined ? force : !this._shortcutsOverlay.classList.contains("is-open");
      this._shortcutsOverlay.classList.toggle("is-open", show);
    }

    /* ---- Overview (grid of all slides) -------------------------------- */

    _toggleOverview(force) {
      if (!this._overview) this._buildOverview();
      const open = force !== undefined ? force : !this._overview.classList.contains("is-open");
      this._overview.classList.toggle("is-open", open);
      if (open) {
        this._highlightOverview();
        requestAnimationFrame(() => this._scaleOverview());
      }
    }

    _buildOverview() {
      this._overview = el("div", "pf-overview");
      this._ovCells = this.slides.map((slide, i) => {
        const cell = el("button", "pf-ov-cell");
        cell.type = "button";
        cell.setAttribute("aria-label", "Go to slide " + (i + 1));

        const frame  = el("span", "pf-ov-frame");
        const canvas = el("span", "pf-ov-canvas");
        canvas.style.width  = this.designW + "px";
        canvas.style.height = this.designH + "px";

        const clone = this._cloneSlide(slide);
        clone.querySelectorAll("aside.notes").forEach((n) => n.remove());
        clone.querySelectorAll(".fragment").forEach((f) => f.classList.add("is-visible"));
        canvas.appendChild(clone);
        frame.appendChild(canvas);

        const num = el("span", "pf-ov-num");
        num.textContent = String(i + 1);
        // On the contact sheet, name the file too: that is what gets fixed.
        if (this._render && slide.getAttribute("data-pf-src")) {
          num.textContent += "  ·  " + slide.getAttribute("data-pf-src");
        }

        cell.append(frame, num);
        cell.addEventListener("click", () => { this.show(i); this._toggleOverview(false); });
        this._overview.appendChild(cell);
        return cell;
      });
      this.stage.appendChild(this._overview);
    }

    _scaleOverview() {
      if (!this._ovCells || !this._ovCells.length) return;
      const frame = this._ovCells[0].querySelector(".pf-ov-frame");
      const w = frame && frame.clientWidth;
      if (!w) return;
      const scale = w / this.designW;
      this._ovCells.forEach((c) => {
        c.querySelector(".pf-ov-canvas").style.transform = `scale(${scale})`;
      });
    }

    _highlightOverview() {
      if (this._ovCells) this._ovCells.forEach((c, i) => c.classList.toggle("is-current", i === this.index));
    }

    /* ---- Draw mode ---------------------------------------------------- */

    _toggleDraw() { this._setDraw(!this._drawActive); }

    _setDraw(on) {
      // Pen and laser are mutually exclusive - turning one on turns the other off.
      if (on && this._laserActive) this._setLaser(false);
      this._drawActive = on;
      [this.drawBtn, this._presenterDrawBtn].forEach((b) => b && b.classList.toggle("is-active", on));
      this._drawSvg.style.pointerEvents = on ? "all" : "none";
      this.stage.classList.toggle("pf-draw-mode", on);
      if (on) this._bindDrawEvents();
      else    this._unbindDrawEvents();
    }

    _bindDrawEvents() {
      this._drawOnDown = (e) => {
        if (e.buttons !== 1) return;
        e.preventDefault();
        const pt = this._svgPt(e);
        this._drawCurrentPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
        this._drawCurrentPath.setAttribute("stroke", "#ff3030");
        this._drawCurrentPath.setAttribute("stroke-width", "6");
        this._drawCurrentPath.setAttribute("stroke-linecap", "round");
        this._drawCurrentPath.setAttribute("stroke-linejoin", "round");
        this._drawCurrentPath.setAttribute("fill", "none");
        this._drawD = `M${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`;
        this._drawCurrentPath.setAttribute("d", this._drawD);
        this._drawSvg.appendChild(this._drawCurrentPath);
        this._syncDraw({ type: "start", x: pt.x, y: pt.y });
      };
      this._drawOnMove = (e) => {
        if (!this._drawCurrentPath || e.buttons !== 1) return;
        e.preventDefault();
        const pt = this._svgPt(e);
        this._drawD += ` L${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`;
        this._drawCurrentPath.setAttribute("d", this._drawD);
        this._syncDraw({ type: "move", x: pt.x, y: pt.y });
      };
      this._drawOnUp = () => {
        if (this._drawCurrentPath) {
          this._syncDraw({ type: "end" });
          this._drawCurrentPath = null;
          this._drawD = "";
        }
      };
      this._drawSvg.addEventListener("mousedown", this._drawOnDown);
      this._drawSvg.addEventListener("mousemove", this._drawOnMove);
      window.addEventListener("mouseup", this._drawOnUp);
    }

    _unbindDrawEvents() {
      if (this._drawOnDown) { this._drawSvg.removeEventListener("mousedown", this._drawOnDown); this._drawOnDown = null; }
      if (this._drawOnMove) { this._drawSvg.removeEventListener("mousemove", this._drawOnMove); this._drawOnMove = null; }
      if (this._drawOnUp)   { window.removeEventListener("mouseup", this._drawOnUp); this._drawOnUp = null; }
    }

    _clearDraw() {
      while (this._drawSvg.firstChild) this._drawSvg.removeChild(this._drawSvg.firstChild);
      this._drawCurrentPath = null;
      this._drawD = "";
      this._syncDraw({ type: "clear" });
    }

    _svgPt(e) {
      // Map a screen (client) point into the SVG's design-space coordinates.
      // We deliberately avoid getScreenCTM(): on WebKit/Safari it does not
      // account for the CSS transform that scales the draw overlay, so the pen
      // would draw offset from the cursor (works on Chrome/Firefox, not Safari).
      // getBoundingClientRect() reflects the real rendered box on every browser;
      // since the viewBox matches the design size with no letterboxing, a linear
      // rect-to-viewBox mapping is exact.
      const r = this._drawSvg.getBoundingClientRect();
      return {
        x: r.width  ? (e.clientX - r.left) / r.width  * this.designW : 0,
        y: r.height ? (e.clientY - r.top)  / r.height * this.designH : 0,
      };
    }

    _syncDraw(data) {
      if (this._audienceWin && !this._audienceWin.closed) {
        this._audienceWin.postMessage({ pfDraw: data }, "*");
      }
    }

    /* ---- Laser pointer ------------------------------------------------ */

    _toggleLaser() { this._setLaser(!this._laserActive); }

    _setLaser(on) {
      // Pen and laser are mutually exclusive.
      if (on && this._drawActive) this._setDraw(false);
      this._laserActive = on;
      [this.laserBtn, this._presenterLaserBtn].forEach((b) => b && b.classList.toggle("is-active", on));
      this._laserDot.classList.toggle("is-active", on);
      if (on) {
        this._laserOnMove = (e) => {
          const r  = this.stage.getBoundingClientRect();
          const mx = e.clientX - r.left;
          const my = e.clientY - r.top;
          this._laserDot.style.left = mx + "px";
          this._laserDot.style.top  = my + "px";
          // Normalized canvas coordinates sent to audience.
          const s  = Math.min(r.width / this.designW, r.height / this.designH);
          const cx = r.width  / 2 - this.designW * s / 2;
          const cy = r.height / 2 - this.designH * s / 2;
          const nx = (mx - cx) / (this.designW * s);
          const ny = (my - cy) / (this.designH * s);
          if (this._audienceWin && !this._audienceWin.closed) {
            this._audienceWin.postMessage({ pfLaser: { x: nx, y: ny } }, "*");
          }
        };
        this.stage.addEventListener("mousemove", this._laserOnMove);
      } else {
        if (this._laserOnMove) { this.stage.removeEventListener("mousemove", this._laserOnMove); this._laserOnMove = null; }
        if (this._audienceWin && !this._audienceWin.closed) {
          this._audienceWin.postMessage({ pfLaser: null }, "*");
        }
      }
    }

    /* ---- Audience window HTML ---------------------------------------- */

    _collectCSS() {
      // Primary: read inline <style> tag content - always works everywhere,
      // including Safari on file:// where cssRules access is blocked by
      // the browser's cross-origin security model. This also covers the bundle
      // case where build.py has already inlined all stylesheets as <style> tags.
      let css = Array.from(document.querySelectorAll("style"))
        .map((s) => s.textContent)
        .join("\n");

      // Secondary: try linked <link rel=stylesheet> via cssRules - works on
      // same-origin HTTP servers, but throws SecurityError on file:// in Safari.
      Array.from(document.styleSheets).forEach((ss) => {
        if (!ss.href) return; // already collected from the <style> tag above
        try {
          css += "\n" + Array.from(ss.cssRules).map((r) => r.cssText).join("\n");
        } catch { /* cross-origin restriction - skip */ }
      });

      return css;
    }

    _buildAudienceHTML() {
      // Carry the deck's styles into the popup. A built deck inlines everything,
      // so the <style> text collected by _collectCSS() is the source that always
      // works; we also forward any <link rel=stylesheet> for the unbundled case.
      const linkTags = Array.from(document.querySelectorAll("link[rel=stylesheet]"))
        .map((l) => `<link rel="stylesheet" href="${l.href}">`)
        .join("\n");

      const inlineCSS = this._collectCSS();

      const slidesHTML = this.slides.map((s) => {
        const c = this._cloneSlide(s);
        c.querySelectorAll("aside.notes").forEach((n) => n.remove());
        return c.outerHTML;
      }).join("\n");
      const countsOn = this._countsAllowed();

      const W = this.designW, H = this.designH;
      return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{margin:0;height:100%;overflow:hidden;background:#000}
.pf-canvas{position:fixed;left:50%;top:50%;-webkit-transform-origin:center center;transform-origin:center center;width:${W}px;height:${H}px}
.pf-canvas>*{position:absolute;top:0;right:0;bottom:0;left:0;visibility:hidden;opacity:0;-webkit-transition:opacity .35s ease;transition:opacity .35s ease;background:#fff;color:#000}
.pf-canvas>[data-active]{visibility:visible;opacity:1}
.pf-canvas .fragment{opacity:0;-webkit-transition:opacity .3s ease;transition:opacity .3s ease}
.pf-canvas .fragment.is-visible{opacity:1}
aside.notes{display:none!important}
#aud-blank{display:none;position:fixed;top:0;right:0;bottom:0;left:0;z-index:60}
#aud-blank.is-black{display:block;background:#000}
#aud-blank.is-white{display:block;background:#fff}
@media (prefers-reduced-motion: reduce){*,::before,::after{-webkit-transition-duration:.001ms!important;transition-duration:.001ms!important;-webkit-animation-duration:.001ms!important;animation-duration:.001ms!important}}
#aud-draw{position:fixed;left:50%;top:50%;pointer-events:none;overflow:visible;-webkit-transform-origin:center center;transform-origin:center center;width:${W}px;height:${H}px}
#aud-laser{display:none;position:fixed;width:16px;height:16px;border-radius:50%;background:rgba(255,30,30,0.88);border:2px solid rgba(255,255,255,0.7);-webkit-transform:translate(-50%,-50%);transform:translate(-50%,-50%);pointer-events:none;z-index:50;box-shadow:0 0 8px rgba(255,30,30,0.6)}
#aud-notes{display:none;position:fixed;bottom:0;left:0;right:0;padding:14px 20px 14px 20px;background:rgba(8,12,25,0.93);color:#dce8f8;font-size:15px;line-height:1.6;max-height:30vh;overflow-y:auto;z-index:40;box-sizing:border-box;border-top:1px solid rgba(255,255,255,0.12)}
#aud-notes-close{position:absolute;top:8px;right:12px;background:none;border:none;color:#fff;font-size:20px;cursor:pointer;opacity:0.5;padding:4px 8px}
#aud-notes-close:hover{opacity:1}
${inlineCSS}
</style>
${linkTags}
</head>
<body>
<div class="pf-canvas" id="c" data-motion="${escAttr(this._motion)}" data-dir="next">${slidesHTML}</div>
<svg id="aud-draw" viewBox="0 0 ${W} ${H}"></svg>
<div id="aud-laser"></div>
<div id="aud-blank"></div>
<div id="aud-notes"><button id="aud-notes-close" onclick="toggleNotes()">×</button><div id="aud-notes-body"></div></div>
<script>
(function(){
  var C=document.getElementById('c'), slides=C.querySelectorAll(':scope>*');
  var drawSvg=document.getElementById('aud-draw');
  var laserDot=document.getElementById('aud-laser');
  var notesPanel=document.getElementById('aud-notes');
  var notesBody=document.getElementById('aud-notes-body');
  var blankEl=document.getElementById('aud-blank');
  var W=${W}, H=${H};
  var drawPath=null, drawD='', notesVisible=false, cur=-1;
  var LANG=${JSON.stringify(this._lang || "")} || undefined, COUNTS=${countsOn};
  ${countUp.toString()}
  function runCounts(root){
    if(!COUNTS) return;
    if(root.matches('[data-count]')) countUp(root, LANG);
    var els=root.querySelectorAll('[data-count]');
    for(var k=0;k<els.length;k++) if(!els[k].closest('.fragment:not(.is-visible)')) countUp(els[k], LANG);
  }

  function scale(){
    var s=Math.min(innerWidth/W,innerHeight/H);
    var t='translate(-50%,-50%) scale('+s+')';
    C.style.transform=t; drawSvg.style.transform=t;
  }
  // instant: arriving back on a slide shows its fragments at once.
  function applyFragments(i, step, instant){
    var act=slides[i]; if(!act) return;
    var frags=act.querySelectorAll('.fragment');
    for(var k=0;k<frags.length;k++){
      var f=frags[k], vis=k<step, was=f.classList.contains('is-visible');
      if(instant!==undefined) f.classList.toggle('pf-instant', instant && vis);
      else if(vis && !was) f.classList.remove('pf-instant');
      f.classList.toggle('is-visible', vis);
      if(vis && !was && instant===undefined) runCounts(f);
    }
  }
  function show(i, step, d){
    if(d.pfTransition) C.setAttribute('data-transition', d.pfTransition);
    if(d.pfDir) C.setAttribute('data-dir', d.pfDir);
    if(i===cur){ applyFragments(i, step); return; }
    cur=i;
    slides.forEach(function(s,n){ n===i?s.setAttribute('data-active',''):s.removeAttribute('data-active') });
    var back=d.pfDir==='prev';
    applyFragments(i, step, back);
    if(!back) runCounts(slides[i]);
  }
  function handleBlank(b){ blankEl.className = b ? ('is-'+b) : ''; }

  window.toggleNotes=function(){
    notesVisible=!notesVisible;
    notesPanel.style.display=notesVisible?'block':'none';
  };

  function handleDraw(d){
    if(d.type==='clear'){ while(drawSvg.firstChild) drawSvg.removeChild(drawSvg.firstChild); drawPath=null; drawD=''; return; }
    if(d.type==='start'){
      drawPath=document.createElementNS('http://www.w3.org/2000/svg','path');
      drawPath.setAttribute('stroke','#ff3030'); drawPath.setAttribute('stroke-width','6');
      drawPath.setAttribute('stroke-linecap','round'); drawPath.setAttribute('stroke-linejoin','round');
      drawPath.setAttribute('fill','none');
      drawD='M'+d.x.toFixed(1)+' '+d.y.toFixed(1); drawPath.setAttribute('d',drawD);
      drawSvg.appendChild(drawPath);
    } else if(d.type==='move'&&drawPath){
      drawD+=' L'+d.x.toFixed(1)+' '+d.y.toFixed(1); drawPath.setAttribute('d',drawD);
    } else if(d.type==='end'){ drawPath=null; drawD=''; }
  }

  function handleLaser(l){
    if(!l){ laserDot.style.display='none'; return; }
    var s=Math.min(innerWidth/W,innerHeight/H);
    var cx=innerWidth/2-W*s/2, cy=innerHeight/2-H*s/2;
    laserDot.style.display='block';
    laserDot.style.left=(cx+l.x*W*s)+'px';
    laserDot.style.top=(cy+l.y*H*s)+'px';
  }

  window.addEventListener('resize', scale);
  scale(); show(0, 0, {});
  window.addEventListener('message', function(e){
    if(!e.data) return;
    if(typeof e.data.pfSlide==='number') show(e.data.pfSlide, e.data.pfStep||0, e.data);
    else if(typeof e.data.pfStep==='number') applyFragments(cur, e.data.pfStep);
    if(typeof e.data.pfNotes!=='undefined') notesBody.innerHTML=e.data.pfNotes||'';
    if('pfBlank' in e.data) handleBlank(e.data.pfBlank);
    if(e.data.pfDraw) handleDraw(e.data.pfDraw);
    if('pfLaser' in e.data) handleLaser(e.data.pfLaser);
  });
  window.addEventListener('keydown', function(e){
    if(!window.opener || e.metaKey || e.ctrlKey || e.altKey) return;
    if(e.key==='n'||e.key==='N'){ window.toggleNotes(); return; }
    var nav=null;
    if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '||e.key==='PageDown') nav='next';
    else if(e.key==='ArrowLeft'||e.key==='ArrowUp'||e.key==='PageUp') nav='prev';
    else if(e.key==='Home') nav='first';
    else if(e.key==='End')  nav='last';
    else if(e.key==='Escape') nav='exit-presenter';
    if(nav){ e.preventDefault(); window.opener.postMessage({pfKeyNav:nav},'*'); }
  });
  // Esc in fullscreen is captured by the browser to leave fullscreen and never
  // reaches keydown above. Treat "left fullscreen" as the exit signal: notify
  // the opener (returns to the windowed deck) and close this audience window.
  var wasFs=false;
  function onFs(){
    var fs=document.fullscreenElement||document.webkitFullscreenElement;
    if(fs){ wasFs=true; }
    else if(wasFs){
      wasFs=false;
      if(window.opener) window.opener.postMessage({pfKeyNav:'exit-presenter'},'*');
      window.close();
    }
  }
  document.addEventListener('fullscreenchange', onFs);
  document.addEventListener('webkitfullscreenchange', onFs);
  try{ document.documentElement.requestFullscreen() }catch(e){}
})();
<\/script>
</body>
</html>`;
    }

    /* ------------------------------------------------------------------ */
    /* Presentation mechanics                                               */
    /* ------------------------------------------------------------------ */

    _layout() {
      const w     = this.stage.clientWidth;
      const h     = this.stage.clientHeight;
      const scale = Math.min(w / this.designW, h / this.designH);
      const t = `translate(-50%, -50%) scale(${scale})`;
      this.canvas.style.transform = t;
      if (this._drawSvg) this._drawSvg.style.transform = t;
      if (this._presenterActive) this._scaleNextPreview();
    }

    _scaleThumbs() {
      if (!this.thumbs.length) return;
      const frame = this.thumbs[0].querySelector(".pf-thumb-frame");
      const w = frame.clientWidth;
      if (!w) return;
      const scale = w / this.designW;
      this.thumbs.forEach((t) => {
        t.querySelector(".pf-thumb-canvas").style.transform = `scale(${scale})`;
      });
    }

    _markActive() {
      this.classList.add("is-active-ui");
      clearTimeout(this._idleTimer);
      this._idleTimer = setTimeout(
        () => this.classList.remove("is-active-ui"),
        IDLE_MS
      );
    }

    _showToast(text) {
      if (!text) return;
      this.toast.textContent = text;
      this.toast.classList.add("is-visible");
      clearTimeout(this._toastTimer);
      this._toastTimer = setTimeout(
        () => this.toast.classList.remove("is-visible"),
        TOAST_MS
      );
    }
  }

  DeckStage.version = VERSION;

  if (!customElements.get("deck-stage")) {
    customElements.define("deck-stage", DeckStage);
  }
})();
