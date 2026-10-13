#!/usr/bin/env node
// Optional object measurement for template-port componentization.
//
// Loads a prepared (slots-mode) deck render in headless Chrome at a fixed
// viewport, then for every [data-edit-slot] node reports:
//   * an absolute slide-object style (% of slide), using the SAME formula as
//     slotRectToObjectStyle() in examples/editable-deck-reference.html;
//   * a `safe` flag: whether the node can be lifted out of normal flow into an
//     absolutely-positioned draggable object WITHOUT disturbing its template
//     layout. Interwoven content (a flex/grid sibling of a decorative box, or
//     text inside a bordered/filled card/panel) is NOT safe and stays a locked
//     in-place slot. Free-standing headings / paragraphs / images ARE safe and
//     become swiss-style draggable slide-objects.
//
// Emits JSON { "<edit-slot-id>": { "style": "...", "safe": true|false } } on
// stdout so the Python builder can optionally produce a coarse-grained,
// swiss-like component model. The default port build preserves native upstream
// layout and does not invoke this script.
//
// Usage: node measure-template-objects.mjs <chrome> <html-file> <width> <height>

import puppeteer from 'puppeteer-core';
import { resolve } from 'node:path';

async function main() {
  const [chromePath, htmlFile, widthArg, heightArg] = process.argv.slice(2);
  if (!chromePath || !htmlFile) {
    process.stderr.write('usage: measure-template-objects.mjs <chrome> <html-file> [width] [height]\n');
    process.exit(2);
  }
  const width = parseInt(widthArg || '1280', 10);
  const height = parseInt(heightArg || '720', 10);
  const fileUrl = 'file://' + resolve(htmlFile);

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars'],
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width, height, deviceScaleFactor: 1 });
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 45000 });
    await page.evaluate(() => (document.fonts ? document.fonts.ready : Promise.resolve()));

    const result = await page.evaluate(() => {
      // Mirror of slotRectToObjectStyle() in editable-deck-reference.html, with
      // one addition: clamp `top` so the object's measured height cannot push it
      // past the slide bottom (near-bottom lifted text otherwise overshoots).
      function rectToStyle(el, slide) {
        const rect = el.getBoundingClientRect();
        const slideRect = slide.getBoundingClientRect();
        const left = Math.max(0, Math.min(96, ((rect.left - slideRect.left) / slideRect.width) * 100));
        let top = Math.max(0, Math.min(96, ((rect.top - slideRect.top) / slideRect.height) * 100));
        const w = Math.max(12, Math.min(92 - left, (rect.width / slideRect.width) * 100));
        const minH = Math.max(3, Math.min(12, rect.height / 16));
        const heightPct = (rect.height / slideRect.height) * 100;
        top = Math.max(0, Math.min(top, 100 - heightPct));
        return 'left:' + left.toFixed(2) + '%;top:' + top.toFixed(2) + '%;width:' + w.toFixed(2) + '%;min-height:' + minH.toFixed(2) + 'rem;';
      }

      function hasVisibleBox(cs) {
        const bg = cs.backgroundColor;
        const opaqueBg = bg && bg !== 'transparent' && bg !== 'rgba(0, 0, 0, 0)';
        const hasBorder = ['Top', 'Right', 'Bottom', 'Left'].some((side) => {
          const w = parseFloat(cs['border' + side + 'Width']);
          const style = cs['border' + side + 'Style'];
          return w > 0 && style && style !== 'none';
        });
        const hasShadow = cs.boxShadow && cs.boxShadow !== 'none';
        return opaqueBg || hasBorder || hasShadow;
      }

      function decorativeSibling(el) {
        const parent = el.parentElement;
        if (!parent) return false;
        for (const sib of parent.children) {
          if (sib === el) continue;
          // An element sibling that renders a visual box but carries no text is
          // decoration whose layout slot depends on `el` staying in flow.
          if (!sib.textContent || !sib.textContent.trim()) {
            const r = sib.getBoundingClientRect();
            if (r.width > 0 && r.height > 0) return true;
          }
        }
        return false;
      }

      function horizontalTextSibling(el) {
        // True when a text-bearing sibling sits on roughly the same row (their
        // vertical spans overlap). Lifting one of two side-by-side inline labels
        // to absolute position drops the flex gap and they collide, so such
        // nodes must stay in flow (edited in place).
        const parent = el.parentElement;
        if (!parent) return false;
        const r = el.getBoundingClientRect();
        for (const sib of parent.children) {
          if (sib === el) continue;
          if (!sib.textContent || !sib.textContent.trim()) continue;
          const s = sib.getBoundingClientRect();
          if (s.width <= 0 || s.height <= 0) continue;
          const vOverlap = Math.min(r.bottom, s.bottom) - Math.max(r.top, s.top);
          if (vOverlap > Math.min(r.height, s.height) * 0.5) return true;
        }
        return false;
      }

      function liftRootOf(leaf, slide) {
        // The unit we actually lift. Walk up from the text leaf; promote the lift
        // root to the OUTERMOST block-sized ancestor that paints its own visual
        // box (a card / panel). Such a box is a self-contained unit that can be
        // lifted whole (border + content together) without collapsing — this is
        // what makes bordered/brutalist templates draggable. If no box ancestor
        // exists, the leaf itself is the lift root (plain free-standing text).
        const sr = slide.getBoundingClientRect();
        let root = leaf;
        let node = leaf.parentElement;
        while (node && node !== slide) {
          const cs = getComputedStyle(node);
          const rr = node.getBoundingClientRect();
          const blockSized = sr.width > 0 && sr.height > 0
            && rr.width <= sr.width * 0.98 && rr.height <= sr.height * 0.98;
          if (hasVisibleBox(cs) && blockSized) root = node;
          node = node.parentElement;
        }
        return root;
      }

      function isSafeToLift(el, slide, isCard) {
        // A lifted object reflows to its measured width and can render slightly
        // taller than it did in flow; if it already sits against the slide bottom
        // it would overflow. Keep bottom-anchored content as an in-place slot.
        const r0 = el.getBoundingClientRect();
        const sr0 = slide.getBoundingClientRect();
        if (sr0.height > 0 && (r0.bottom - sr0.top) / sr0.height > 0.93) return false;
        // Walk ancestors up to (not including) the slide section. Unsafe when the
        // lift unit lives INSIDE another card/panel that paints its own visual box
        // — removing it would shrink or empty that outer box. (The unit's own box,
        // if it is a card, is fine; we only check ancestors above it.)
        let node = el.parentElement;
        while (node && node !== slide) {
          const cs = getComputedStyle(node);
          if (hasVisibleBox(cs)) return false;
          node = node.parentElement;
        }
        // A card is a self-contained box: the leaf-only guards below (decorative
        // sibling, side-by-side labels, orphaned sibling text) target inline/text
        // fragments and would wrongly veto whole cards, so skip them for cards.
        if (isCard) return true;
        // A direct decorative sibling (e.g. a progress-bar track paired with a
        // value) depends on this node holding its layout slot — keep it in flow.
        if (decorativeSibling(el)) return false;
        // Side-by-side text labels rely on flex/grid gap for separation; lifting
        // one to absolute position collides it with its row-mate.
        if (horizontalTextSibling(el)) return false;
        // Don't strip a body-text container of editable coverage. If this node's
        // direct parent holds text that is NOT inside any slot/object descendant
        // (a bare sibling label, caption, or source line), lifting this node out
        // would orphan that text as uneditable — keep this slot in flow instead.
        // Only the immediate parent is checked: deeper ancestors legitimately mix
        // many independent slots, and walking up would suppress nearly everything.
        function uncoveredText(node) {
          let acc = '';
          for (const child of node.childNodes) {
            if (child.nodeType === 3) {
              acc += child.textContent || '';
            } else if (child.nodeType === 1) {
              if (child.hasAttribute('data-edit-slot') || child.hasAttribute('data-slide-object')) continue;
              acc += uncoveredText(child);
            }
          }
          return acc;
        }
        const parent = el.parentElement;
        if (parent && parent !== slide
            && !parent.hasAttribute('data-edit-slot') && !parent.hasAttribute('data-slide-object')) {
          const remainder = uncoveredText(parent).replace(/\s+/g, ' ').trim();
          const selfTxt = (el.textContent || '').replace(/\s+/g, ' ').trim();
          const leftover = remainder.split(selfTxt).join('').trim();
          if (leftover) return false;
        }
        return true;
      }

      const out = {};
      const slides = document.querySelectorAll('.slides-offset > section.slide');
      slides.forEach((slide) => {
        // Many templates show only the .active slide (`.slide{display:none}`),
        // so inactive slides have zero-size content and can't be measured. Force
        // this slide visible (overriding template + active-class CSS) just for the
        // measurement, then restore. We mutate inline style with !important.
        const prevStyle = slide.getAttribute('style');
        slide.style.setProperty('display', 'flex', 'important');
        slide.style.setProperty('opacity', '1', 'important');
        slide.style.setProperty('visibility', 'visible', 'important');
        slide.style.setProperty('position', 'relative', 'important');
        slide.style.setProperty('transform', 'none', 'important');
        // Force layout flush.
        void slide.getBoundingClientRect();
        slide.querySelectorAll('[data-edit-slot]').forEach((el) => {
          const id = el.getAttribute('data-edit-slot');
          const root = liftRootOf(el, slide);
          const isCard = root !== el;
          const target = root;
          const rect = target.getBoundingClientRect();
          if (rect.width <= 0 || rect.height <= 0) {
            out[id] = { style: null, safe: false };
            return;
          }
          out[id] = {
            style: rectToStyle(target, slide),
            safe: isSafeToLift(target, slide, isCard),
            liftNi: target.getAttribute('data-ni') || null,
            isCard: isCard,
          };
        });
        if (prevStyle === null) slide.removeAttribute('style');
        else slide.setAttribute('style', prevStyle);
      });
      return out;
    });

    process.stdout.write(JSON.stringify(result));
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  process.stderr.write(String((err && err.stack) || err) + '\n');
  process.exit(1);
});
