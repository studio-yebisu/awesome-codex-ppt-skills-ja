#!/usr/bin/env node
/**
 * browser_dom_audit.mjs - Measure export-ready HTML slides in Chromium.
 *
 * The audit deliberately measures the settled browser DOM, one fixed export
 * canvas at a time. It is a mechanical companion to visual review: blockers
 * identify broken assets or real clipping/overflow, while spacing findings are
 * review prompts rather than automatic failures.
 *
 * Usage:
 *   node browser_dom_audit.mjs index.html -o output/dom-audit.json
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const DEFAULT_WIDTH = 1280;
const DEFAULT_HEIGHT = 720;
const DEFAULT_TIMEOUT = 120_000;
const SCHEMA = 'seaslides.browser-dom-audit';
const VERSION = 1;

function parseArgs(argv) {
  const args = {
    input: null,
    output: null,
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    timeout: DEFAULT_TIMEOUT,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '-o' || arg === '--output') {
      args.output = argv[++index];
    } else if (arg === '--width') {
      args.width = Number.parseInt(argv[++index], 10);
    } else if (arg === '--height') {
      args.height = Number.parseInt(argv[++index], 10);
    } else if (arg === '--timeout') {
      args.timeout = Number.parseInt(argv[++index], 10);
    } else if (arg === '-h' || arg === '--help') {
      printHelp();
      process.exit(0);
    } else if (!args.input) {
      args.input = arg;
    } else {
      throw new Error(`Unexpected argument: ${arg}`);
    }
  }

  if (!args.input) throw new Error('Missing input HTML file.');
  if (!args.output) throw new Error('Missing JSON output path. Use -o <file>.');
  for (const [flag, value] of [
    ['--width', args.width],
    ['--height', args.height],
    ['--timeout', args.timeout],
  ]) {
    if (!Number.isInteger(value) || value <= 0) {
      throw new Error(`${flag} must be a positive integer.`);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node browser_dom_audit.mjs <input.html> -o <audit.json>

Options:
  -o, --output <file>  JSON audit receipt
  --width <px>         Export canvas width (default: ${DEFAULT_WIDTH})
  --height <px>        Export canvas height (default: ${DEFAULT_HEIGHT})
  --timeout <ms>       Browser operation timeout (default: ${DEFAULT_TIMEOUT})
`);
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function findBrowserExecutable() {
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  ];
  for (const candidate of candidates) {
    if (await fileExists(candidate)) return candidate;
  }
  return null;
}

async function withTimeout(promise, timeout, label) {
  let timer;
  const timed = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`${label} timed out after ${timeout}ms.`)), timeout);
  });
  try {
    return await Promise.race([promise, timed]);
  } finally {
    clearTimeout(timer);
  }
}

async function settlePage(page, timeout) {
  await withTimeout(page.evaluate(async (settleTimeout) => {
    if (window.SeaSlidesRuntime?.settleForExport) {
      await window.SeaSlidesRuntime.settleForExport({ timeout: settleTimeout });
      return;
    }
    const ready = window.__dynamicContentReady;
    if (ready && typeof ready.then === 'function') await ready;

    if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
    if (window.MathJax?.typesetPromise) await window.MathJax.typesetPromise([document.body]);
    if (document.fonts?.ready) await document.fonts.ready;

    await Promise.all(Array.from(document.images, (image) => {
      if (image.complete) return Promise.resolve();
      return new Promise((resolve) => {
        image.addEventListener('load', resolve, { once: true });
        image.addEventListener('error', resolve, { once: true });
      });
    }));
  }, timeout), timeout, 'Browser content settlement');
}

async function auditSlide(page, slideIndex, width, height) {
  return page.evaluate(({ targetIndex, canvasWidth, canvasHeight }) => {
    const TOLERANCE = 4;
    const CLIP_TOLERANCE = 4;
    // Browser glyph boxes may overlap adjacent line boxes by several pixels
    // (notably MathJax and pseudocode).  Only treat substantial independent
    // block intersections as deterministic overlap; smaller intersections are
    // still visible in the exported PNG and belong to visual review.
    const TEXT_OVERLAP_TOLERANCE = 10;
    const className = (element) => typeof element.className === 'string' ? element.className : '';
    const number = (value) => Math.round(value * 100) / 100;
    const rectObject = (rect) => ({
      left: number(rect.left),
      top: number(rect.top),
      right: number(rect.right),
      bottom: number(rect.bottom),
      width: number(rect.width),
      height: number(rect.height),
    });
    const elementLabel = (element) => {
      const tag = element.tagName.toLowerCase();
      const id = element.id ? `#${element.id}` : '';
      const classes = className(element).trim().split(/\s+/).filter(Boolean).slice(0, 3);
      return `${tag}${id}${classes.length ? `.${classes.join('.')}` : ''}`;
    };
    const briefText = (element) => Array.from(
      (element.innerText || element.getAttribute('alt') || '').replace(/\s+/g, ' ').trim()
    ).slice(0, 120).join('');
    const slides = Array.from(document.querySelectorAll('section.slide'));
    const slide = slides[targetIndex];
    if (!slide) throw new Error(`Slide ${targetIndex + 1} no longer exists.`);

    const original = {
      deck: document.getElementById('deck'),
      deckStyle: document.getElementById('deck')?.getAttribute('style') ?? null,
      slides: slides.map((candidate) => ({
        className: candidate.className,
        style: candidate.getAttribute('style'),
      })),
    };

    const restore = () => {
      if (original.deck) {
        if (original.deckStyle === null) original.deck.removeAttribute('style');
        else original.deck.setAttribute('style', original.deckStyle);
      }
      slides.forEach((candidate, index) => {
        candidate.className = original.slides[index].className;
        const previousStyle = original.slides[index].style;
        if (previousStyle === null) candidate.removeAttribute('style');
        else candidate.setAttribute('style', previousStyle);
      });
    };

    try {
      window.scrollTo(0, 0);
      if (original.deck) {
        const deckStyle = original.deck.style;
        deckStyle.setProperty('transition', 'none', 'important');
        deckStyle.setProperty('transform', 'none', 'important');
        deckStyle.setProperty('width', `${canvasWidth}px`, 'important');
        deckStyle.setProperty('height', `${canvasHeight}px`, 'important');
        deckStyle.setProperty('position', 'fixed', 'important');
        deckStyle.setProperty('inset', '0', 'important');
        deckStyle.setProperty('overflow', 'hidden', 'important');
        deckStyle.setProperty('display', 'block', 'important');
      }

      slides.forEach((candidate, index) => {
        const selected = index === targetIndex;
        const style = candidate.style;
        const computedDisplay = getComputedStyle(candidate).display;
        style.setProperty('transition', 'none', 'important');
        candidate.classList.toggle('active', selected);
        candidate.classList.toggle('present', selected);
        if (!selected) {
          style.setProperty('display', 'none', 'important');
          return;
        }
        candidate.classList.remove('past', 'future');
        if (computedDisplay === 'none') style.setProperty('display', 'block', 'important');
        style.setProperty('position', 'fixed', 'important');
        style.setProperty('left', '0', 'important');
        style.setProperty('top', '0', 'important');
        style.setProperty('width', `${canvasWidth}px`, 'important');
        style.setProperty('height', `${canvasHeight}px`, 'important');
        style.setProperty('min-width', `${canvasWidth}px`, 'important');
        style.setProperty('min-height', `${canvasHeight}px`, 'important');
        style.setProperty('max-width', `${canvasWidth}px`, 'important');
        style.setProperty('max-height', `${canvasHeight}px`, 'important');
        style.setProperty('margin', '0', 'important');
        style.setProperty('opacity', '1', 'important');
        style.setProperty('visibility', 'visible', 'important');
        style.setProperty('transform', 'none', 'important');
        style.setProperty('box-sizing', 'border-box', 'important');
      });

      // Force a layout pass after the isolation styles take effect.
      void slide.offsetWidth;
      const slideComputedStyle = getComputedStyle(slide);
      const cssNumberMetric = (name, fallback) => {
        const parsed = Number.parseFloat(slideComputedStyle.getPropertyValue(name));
        return Number.isFinite(parsed) && parsed >= 0 ? parsed : fallback;
      };
      const cssLengthMetric = (name, fallback) => {
        const raw = slideComputedStyle.getPropertyValue(name).trim();
        if (!raw) return fallback;
        const probe = document.createElement('span');
        probe.setAttribute('data-audit-ignore', '');
        probe.style.cssText = [
          'position:absolute',
          'visibility:hidden',
          'pointer-events:none',
          'width:0',
          'padding:0',
          'border:0',
          `height:var(${name})`,
        ].join(';');
        slide.appendChild(probe);
        const resolved = probe.getBoundingClientRect().height;
        probe.remove();
        return Number.isFinite(resolved) && resolved >= 0 ? resolved : fallback;
      };
      // Geometry reviews are theme-owned policy.  A zero fallback keeps a
      // generic audit from inventing one spacing system for every design.
      const reviewEdge = cssLengthMetric('--seaslides-edge-safe-min', 0);
      const reviewTitleGap = cssLengthMetric('--seaslides-title-gap-min', 0);
      const attributeMetric = (attribute, fallback = 0) => {
        const attributeValue = slide.getAttribute(attribute);
        if (attributeValue !== null && attributeValue.trim() !== '') {
          const parsed = Number.parseFloat(attributeValue);
          if (Number.isFinite(parsed) && parsed >= 0) return parsed;
        }
        return fallback;
      };
      const lengthReviewMetric = (attribute, cssName) => (
        attributeMetric(attribute, cssLengthMetric(cssName, 0))
      );
      const numberReviewMetric = (attribute, cssName) => (
        attributeMetric(attribute, cssNumberMetric(cssName, 0))
      );
      // Composition checks are explicit, theme-owned review contracts. A
      // slide must opt into `top-to-bottom`; zero disables each threshold so sparse
      // heroes, quotes, and editorial pages never inherit a universal quota.
      const compositionMode = slide.getAttribute('data-audit-composition') || 'observe';
      const reviewBalanceBottom = lengthReviewMetric(
        'data-audit-bottom-gap-max',
        '--seaslides-audit-bottom-gap-max',
      );
      const reviewBalanceActive = numberReviewMetric(
        'data-audit-active-height-min',
        '--seaslides-audit-active-height-min',
      );
      const reviewBalanceGap = lengthReviewMetric(
        'data-audit-vertical-gap-max',
        '--seaslides-audit-vertical-gap-max',
      );
      const reviewNavSafeBottom = lengthReviewMetric(
        'data-audit-nav-safe-bottom',
        '--seaslides-nav-safe-bottom',
      );
      const fontRoleThresholds = {
        body: cssLengthMetric('--seaslides-audit-font-min-body', 0),
        code: cssLengthMetric('--seaslides-audit-font-min-code', 0),
        label: cssLengthMetric('--seaslides-audit-font-min-label', 0),
      };

      const isExcluded = (element) => {
        for (let node = element; node && node !== slide; node = node.parentElement) {
          if (
            node.getAttribute('aria-hidden') === 'true'
            || node.hasAttribute('data-export-ignore')
            || node.hasAttribute('data-audit-ignore')
          ) return true;
          if (node.tagName === 'NAV' || node.getAttribute('role') === 'navigation') return true;
          const marker = `${node.tagName || ''} ${node.id || ''} ${className(node)}`.toLowerCase();
          if (/(^|[-_\s])(nav|navigation|hint|controls?|progress|decorative|decoration|ornament|background|ghost|assistive|sr-only|screen-reader|visually-hidden)([-_\s]|$)/.test(marker)) {
            return true;
          }
        }
        return false;
      };
      const visible = (element, style = getComputedStyle(element)) => {
        const rect = element.getBoundingClientRect();
        return style.display !== 'none'
          && style.visibility !== 'hidden'
          && Number.parseFloat(style.opacity || '1') > 0
          && rect.width > TOLERANCE
          && rect.height > TOLERANCE;
      };
      const hasDirectText = (element) => Array.from(element.childNodes).some((node) => (
        node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0
      ));
      const meaningfulGraphic = (element) => {
        if (element.tagName !== 'SVG' && element.tagName !== 'CANVAS') return false;
        const role = (element.getAttribute('role') || '').toLowerCase();
        if (role === 'presentation' || role === 'none') return false;
        const svgTitle = element.tagName === 'SVG'
          ? element.querySelector(':scope > title')?.textContent?.trim()
          : '';
        return element.hasAttribute('data-audit-meaningful')
          || role === 'img'
          || !!element.getAttribute('aria-label')?.trim()
          || !!element.getAttribute('aria-labelledby')?.trim()
          || !!element.getAttribute('title')?.trim()
          || !!svgTitle;
      };
      const semanticTags = new Set([
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'P', 'LI', 'IMG', 'FIGURE', 'FIGCAPTION',
        'TABLE', 'TD', 'TH', 'BLOCKQUOTE', 'PRE', 'CODE', 'VIDEO',
      ]);
      const rangeRect = (element, fallback) => {
        if (!(element.innerText || '').trim()) return fallback;
        const range = document.createRange();
        range.selectNodeContents(element);
        const textRect = range.getBoundingClientRect();
        range.detach();
        return textRect.width > 0 && textRect.height > 0 ? textRect : fallback;
      };
      const candidateElements = [];
      const allDescendants = Array.from(slide.querySelectorAll('*'));
      for (const element of allDescendants) {
        if (isExcluded(element)) continue;
        const style = getComputedStyle(element);
        if (!visible(element, style)) continue;
        const rect = element.getBoundingClientRect();
        if (
          semanticTags.has(element.tagName)
          || hasDirectText(element)
          || meaningfulGraphic(element)
          || element.hasAttribute('data-audit-meaningful')
        ) {
          candidateElements.push({ element, style, rect, visualRect: rangeRect(element, rect) });
        }
      }

      const issues = [];
      const brokenImages = [];
      for (const image of Array.from(slide.querySelectorAll('img'))) {
        if (isExcluded(image)) continue;
        if (!image.complete || image.naturalWidth === 0 || image.naturalHeight === 0) {
          const asset = {
            element: elementLabel(image),
            src: image.currentSrc || image.getAttribute('src') || '',
            alt: image.getAttribute('alt') || '',
          };
          brokenImages.push(asset);
          issues.push({
            severity: 'blocker',
            code: 'broken_image',
            message: `Image failed to load: ${asset.src || '(missing src)'}.`,
            ...asset,
          });
        }
      }

      const slideRect = slide.getBoundingClientRect();
      const clientWidth = slide.clientWidth;
      const clientHeight = slide.clientHeight;
      const scrollWidth = slide.scrollWidth;
      const scrollHeight = slide.scrollHeight;
      const scrollOverflowX = scrollWidth > clientWidth + CLIP_TOLERANCE;
      const scrollOverflowY = scrollHeight > clientHeight + CLIP_TOLERANCE;

      const outsideCandidates = candidateElements
        .map(({ element, visualRect }) => ({
          element,
          visualRect,
          bounds: {
            left: visualRect.left - slideRect.left,
            top: visualRect.top - slideRect.top,
            right: visualRect.right - slideRect.left,
            bottom: visualRect.bottom - slideRect.top,
          },
        }))
        .filter(({ bounds }) => (
          bounds.left < -TOLERANCE
          || bounds.top < -TOLERANCE
          || bounds.right > canvasWidth + TOLERANCE
          || bounds.bottom > canvasHeight + TOLERANCE
        ));
      const ownerSelector = [
        '[data-audit-owner]', 'pre', 'table', 'figure', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li',
        '.slide-body', '.frame', '.body-text', '.ps-root', '.canvas-card',
        '.col-block', '.duo-side',
      ].join(',');
      const ownerGroups = new Map();
      for (const candidate of outsideCandidates) {
        const owner = candidate.element.closest(ownerSelector) || candidate.element;
        const existing = ownerGroups.get(owner);
        if (existing) {
          existing.bounds.left = Math.min(existing.bounds.left, candidate.bounds.left);
          existing.bounds.top = Math.min(existing.bounds.top, candidate.bounds.top);
          existing.bounds.right = Math.max(existing.bounds.right, candidate.bounds.right);
          existing.bounds.bottom = Math.max(existing.bounds.bottom, candidate.bounds.bottom);
          existing.descendantCount += 1;
        } else {
          ownerGroups.set(owner, {
            element: elementLabel(owner),
            text: briefText(owner),
            bounds: { ...candidate.bounds },
            descendantCount: 1,
          });
        }
      }
      const outsideCanvas = Array.from(ownerGroups.values());
      if (outsideCanvas.length > 0) {
        issues.push({
          severity: 'blocker',
          code: 'content_outside_canvas',
          message: `${outsideCanvas.length} meaningful element(s) extend beyond the export canvas.`,
          elements: outsideCanvas,
          // Scroll dimensions are supporting geometry for the same escaped
          // content.  Do not emit a second blocker for this condition: one
          // owner-level issue is enough for a reviewer to locate and fix it.
          scroll: {
            scrollWidth,
            scrollHeight,
            clientWidth,
            clientHeight,
            overflowX: scrollOverflowX,
            overflowY: scrollOverflowY,
          },
        });
      }

      const clipped = [];
      for (const element of allDescendants) {
        if (isExcluded(element)) continue;
        const style = getComputedStyle(element);
        if (!visible(element, style)) continue;
        const ownsContent = (element.textContent || '').trim().length > 0
          || candidateElements.some((candidate) => (
            candidate.element !== element && element.contains(candidate.element)
          ));
        if (!ownsContent) continue;
        const clipsX = ['hidden', 'clip', 'scroll', 'auto'].includes(style.overflowX);
        const clipsY = ['hidden', 'clip', 'scroll', 'auto'].includes(style.overflowY);
        const clippedX = clipsX && element.scrollWidth > element.clientWidth + CLIP_TOLERANCE;
        const clippedY = clipsY && element.scrollHeight > element.clientHeight + CLIP_TOLERANCE;
        if (!clippedX && !clippedY) continue;
        const elementRect = element.getBoundingClientRect();
        const meaningfulRects = candidateElements
          .filter((candidate) => candidate.element !== element && element.contains(candidate.element))
          .map((candidate) => ({
            element: elementLabel(candidate.element),
            text: briefText(candidate.element),
            rect: candidate.visualRect,
          }));
        if (hasDirectText(element)) {
          meaningfulRects.push({
            element: elementLabel(element),
            text: briefText(element),
            rect: rangeRect(element, elementRect),
          });
        }
        const escapedContent = meaningfulRects.filter(({ rect }) => (
          (clippedX && (rect.left < elementRect.left - CLIP_TOLERANCE || rect.right > elementRect.right + CLIP_TOLERANCE))
          || (clippedY && (rect.top < elementRect.top - CLIP_TOLERANCE || rect.bottom > elementRect.bottom + CLIP_TOLERANCE))
        ));
        if (escapedContent.length === 0) continue;
        const finding = {
          element: elementLabel(element),
          text: briefText(element),
          scrollWidth: element.scrollWidth,
          scrollHeight: element.scrollHeight,
          clientWidth: element.clientWidth,
          clientHeight: element.clientHeight,
          overflowX: style.overflowX,
          overflowY: style.overflowY,
          clippedX,
          clippedY,
          escapedContent: escapedContent.map(({ element: label, text, rect }) => ({
            element: label,
            text,
            bounds: rectObject(rect),
          })),
        };
        clipped.push(finding);
        issues.push({
          severity: 'blocker',
          code: 'internal_clipping',
          message: `${finding.element} clips descendant content.`,
          ...finding,
        });
      }

      const blockTextTags = new Set(['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'P', 'LI', 'TD', 'TH', 'PRE', 'BLOCKQUOTE', 'FIGCAPTION']);
      const textBlocks = candidateElements.filter(({ element }) => (
        blockTextTags.has(element.tagName)
        && (element.innerText || '').trim()
        && !element.querySelector('h1, h2, h3, h4, h5, h6, p, li, td, th, pre, blockquote, figcaption')
      ));
      const textNoiseRoot = (element) => element.closest([
        'mjx-container', '.MathJax', '.MathJax_Display', '[class*="MathJax"]', '[class*="mjx-"]',
        'pre', 'code', '[class*="prism"]', '[class*="language-"]',
        '.ps-root', '[class*="pseudocode"]',
      ].join(','));
      const textOwner = (element) => element.closest([
        '[data-audit-owner]', '.slide-body', '.frame', '.body-text', '.canvas-card', '.col-block', '.duo-side',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'td', 'th', 'pre', 'blockquote', 'figcaption',
      ].join(',')) || element;
      const textOverlaps = [];
      const headingLineBoxIntersections = [];
      const headingOverlapGroups = new Map();
      const ownerIds = new Map();
      let nextOwnerId = 1;
      const ownerId = (owner) => {
        if (!ownerIds.has(owner)) ownerIds.set(owner, nextOwnerId++);
        return ownerIds.get(owner);
      };
      for (let leftIndex = 0; leftIndex < textBlocks.length; leftIndex += 1) {
        const left = textBlocks[leftIndex];
        for (let rightIndex = leftIndex + 1; rightIndex < textBlocks.length; rightIndex += 1) {
          const right = textBlocks[rightIndex];
          if (left.element.contains(right.element) || right.element.contains(left.element)) continue;
          const leftNoiseRoot = textNoiseRoot(left.element);
          const rightNoiseRoot = textNoiseRoot(right.element);
          // MathJax/Prism boxes and one pseudocode tree frequently have
          // intentional, browser-specific line-box intersections. They are
          // not independent slide text collisions.
          if (leftNoiseRoot && leftNoiseRoot === rightNoiseRoot) continue;
          const overlapWidth = Math.min(left.visualRect.right, right.visualRect.right)
            - Math.max(left.visualRect.left, right.visualRect.left);
          const overlapHeight = Math.min(left.visualRect.bottom, right.visualRect.bottom)
            - Math.max(left.visualRect.top, right.visualRect.top);
          if (overlapWidth <= 4 || overlapHeight <= TEXT_OVERLAP_TOLERANCE) continue;
          const overlapRatio = overlapHeight / Math.max(
            1,
            Math.min(left.visualRect.height, right.visualRect.height),
          );
          // Small intersections between adjacent flow line boxes are common
          // with browser font metrics.  Require a material share of the
          // smaller block before treating non-heading text as a collision.
          const headingRelated = /^H[1-6]$/.test(left.element.tagName)
            || /^H[1-6]$/.test(right.element.tagName);
          if ((!headingRelated && overlapRatio < 0.5) || (headingRelated && overlapRatio < 0.25)) continue;
          const finding = {
            first: { element: elementLabel(left.element), text: briefText(left.element), bounds: rectObject(left.visualRect) },
            second: { element: elementLabel(right.element), text: briefText(right.element), bounds: rectObject(right.visualRect) },
            overlap: { width: number(overlapWidth), height: number(overlapHeight), ratio: number(overlapRatio) },
          };
          if (headingRelated) {
            headingLineBoxIntersections.push(finding);
            const adjacentFlowSiblings = left.element.parentElement === right.element.parentElement
              && (
                left.element.nextElementSibling === right.element
                || right.element.nextElementSibling === left.element
              )
              && ['static', 'relative'].includes(left.style.position)
              && ['static', 'relative'].includes(right.style.position)
              && left.style.transform === 'none'
              && right.style.transform === 'none';
            // Adjacent heading/lead line boxes can intersect even when their
            // visible glyphs do not. Preserve the measurement as telemetry;
            // the theme-owned title-gap metric and PNG review own this case.
            if (adjacentFlowSiblings) continue;
            const firstOwner = textOwner(left.element);
            const secondOwner = textOwner(right.element);
            if (firstOwner === secondOwner) continue;
            const ownerKey = [ownerId(firstOwner), ownerId(secondOwner)].sort((a, b) => a - b).join(' <> ');
            const group = headingOverlapGroups.get(ownerKey);
            if (group) {
              group.pairCount += 1;
              group.maxOverlap.width = Math.max(group.maxOverlap.width, finding.overlap.width);
              group.maxOverlap.height = Math.max(group.maxOverlap.height, finding.overlap.height);
            } else {
              headingOverlapGroups.set(ownerKey, {
                owners: [
                  { element: elementLabel(firstOwner), text: briefText(firstOwner) },
                  { element: elementLabel(secondOwner), text: briefText(secondOwner) },
                ],
                pairCount: 1,
                maxOverlap: { ...finding.overlap },
                example: finding,
              });
            }
          } else {
            textOverlaps.push(finding);
          }
        }
      }
      if (textOverlaps.length > 0) {
        issues.push({
          severity: 'blocker',
          code: 'text_overlap',
          message: `${textOverlaps.length} pair(s) of independent text blocks overlap.`,
          overlaps: textOverlaps,
        });
      }
      const textOverlapReviews = Array.from(headingOverlapGroups.values());
      if (textOverlapReviews.length > 0) {
        issues.push({
          severity: 'review',
          code: 'heading_text_overlap',
          message: `${textOverlapReviews.length} heading-related text owner pair(s) substantially overlap.`,
          overlaps: textOverlapReviews,
        });
      }

      // Adjacent inline elements can accidentally concatenate two English
      // sentences when their source boundary contains no whitespace.  This is
      // lexical/visual review rather than an overlap blocker, and flex/grid
      // component rows are deliberately excluded because their CSS gap owns
      // the separation.
      const continuityFindings = [];
      const continuityParents = Array.from(
        slide.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li, blockquote, figcaption')
      ).filter((element) => !isExcluded(element) && !textNoiseRoot(element));
      for (const parent of continuityParents) {
        const parentDisplay = getComputedStyle(parent).display;
        if (parentDisplay.includes('flex') || parentDisplay.includes('grid')) continue;
        const children = Array.from(parent.children);
        for (let index = 0; index + 1 < children.length; index += 1) {
          const left = children[index];
          const right = children[index + 1];
          if (isExcluded(left) || isExcluded(right) || textNoiseRoot(left) || textNoiseRoot(right)) continue;
          const leftStyle = getComputedStyle(left);
          const rightStyle = getComputedStyle(right);
          if (!leftStyle.display.startsWith('inline') || !rightStyle.display.startsWith('inline')) continue;

          let hasSourceSeparator = false;
          for (let node = left.nextSibling; node && node !== right; node = node.nextSibling) {
            if (node.nodeType === Node.TEXT_NODE && /\s/.test(node.textContent || '')) {
              hasSourceSeparator = true;
              break;
            }
            if (node.nodeType === Node.ELEMENT_NODE && ['BR', 'WBR'].includes(node.tagName)) {
              hasSourceSeparator = true;
              break;
            }
          }
          if (hasSourceSeparator) continue;

          const leftText = (left.textContent || '').trimEnd();
          const rightText = (right.textContent || '').trimStart();
          if (!/[.!?;:]$/.test(leftText) || !/^[A-Za-z0-9]/.test(rightText)) continue;
          if (Number.parseFloat(rightStyle.marginLeft || '0') > 2) continue;
          const leftRect = left.getBoundingClientRect();
          const rightRect = right.getBoundingClientRect();
          const sameLine = Math.min(leftRect.bottom, rightRect.bottom)
            - Math.max(leftRect.top, rightRect.top) > 2;
          if (sameLine && rightRect.left - leftRect.right > 2) continue;

          continuityFindings.push({
            parent: elementLabel(parent),
            first: { element: elementLabel(left), text: briefText(left) },
            second: { element: elementLabel(right), text: briefText(right) },
          });
        }
      }
      if (continuityFindings.length > 0) {
        issues.push({
          severity: 'review',
          code: 'text_continuity_review',
          message: `${continuityFindings.length} adjacent inline boundary/boundaries may concatenate English sentences.`,
          boundaries: continuityFindings,
        });
      }

      const contentRects = candidateElements.map(({ visualRect }) => visualRect);
      let contentBounds = null;
      let verticalBalance = null;
      if (contentRects.length > 0) {
        const left = Math.min(...contentRects.map((rect) => rect.left - slideRect.left));
        const top = Math.min(...contentRects.map((rect) => rect.top - slideRect.top));
        const right = Math.max(...contentRects.map((rect) => rect.right - slideRect.left));
        const bottom = Math.max(...contentRects.map((rect) => rect.bottom - slideRect.top));
        contentBounds = {
          left: number(left),
          top: number(top),
          right: number(right),
          bottom: number(bottom),
          width: number(right - left),
          height: number(bottom - top),
          bottomWhitespace: number(Math.max(0, canvasHeight - bottom)),
          activeHeightRatio: number(Math.min(1, Math.max(0, (bottom - top) / canvasHeight))),
        };
        const edgeClearance = {
          left: contentBounds.left,
          top: contentBounds.top,
          right: number(Math.max(0, canvasWidth - contentBounds.right)),
          bottom: contentBounds.bottomWhitespace,
        };
        const tightEdges = Object.entries(edgeClearance)
          .filter(([, clearance]) => clearance < reviewEdge)
          .map(([edge]) => edge);
        if (reviewEdge > 0 && tightEdges.length > 0) {
          issues.push({
            severity: 'review',
            code: 'edge_clearance_low',
            message: `Meaningful content is within ${reviewEdge}px of the ${tightEdges.join(', ')} edge.`,
            clearance: edgeClearance,
          });
        }
      }

      const contentRoots = Array.from(slide.querySelectorAll('[data-audit-content]'))
        .filter((element) => !isExcluded(element));
      const compositionSource = contentRoots.length > 0 ? 'explicit' : 'inferred';
      const compositionChromeSelector = '[data-audit-chrome], [data-audit-balance-ignore]';
      const excludedChromeCount = candidateElements.filter(({ element }) => (
        Boolean(element.closest(compositionChromeSelector))
      )).length;
      const balanceCandidates = candidateElements.filter(({ element }) => {
        if (element.closest(compositionChromeSelector)) return false;
        if (contentRoots.length === 0) return true;
        return contentRoots.some((root) => root === element || root.contains(element));
      });
      const balanceIntervals = balanceCandidates
        .map(({ element, visualRect }) => ({
          top: Math.max(0, visualRect.top - slideRect.top),
          bottom: Math.min(canvasHeight, visualRect.bottom - slideRect.top),
          element: elementLabel(element),
          text: briefText(element),
        }))
        .filter(({ top, bottom }) => bottom - top > TOLERANCE)
        .sort((left, right) => left.top - right.top || left.bottom - right.bottom);
      if (balanceIntervals.length > 0) {
        const bands = [];
        for (const interval of balanceIntervals) {
          const previous = bands[bands.length - 1];
          if (previous && interval.top <= previous.bottom + TOLERANCE) {
            if (interval.bottom > previous.bottom) {
              previous.bottom = interval.bottom;
              previous.after = { element: interval.element, text: interval.text };
            }
          } else {
            bands.push({
              top: interval.top,
              bottom: interval.bottom,
              before: { element: interval.element, text: interval.text },
              after: { element: interval.element, text: interval.text },
            });
          }
        }
        const gaps = [];
        for (let index = 1; index < bands.length; index += 1) {
          const previous = bands[index - 1];
          const current = bands[index];
          gaps.push({
            top: previous.bottom,
            bottom: current.top,
            height: current.top - previous.bottom,
            before: previous.after,
            after: current.before,
          });
        }
        const top = bands[0].top;
        const bottom = bands[bands.length - 1].bottom;
        const occupiedHeight = bands.reduce((total, band) => total + band.bottom - band.top, 0);
        const largestGap = gaps.sort((left, right) => right.height - left.height)[0] || null;
        const explicitFrameTop = contentRoots.length > 0
          ? Math.min(...contentRoots.map((root) => root.getBoundingClientRect().top - slideRect.top))
          : 0;
        const frameTop = Math.min(canvasHeight, Math.max(0, explicitFrameTop));
        const safeBottom = Math.max(frameTop, canvasHeight - reviewNavSafeBottom);
        const usableHeight = Math.max(1, safeBottom - frameTop);
        const bottomGap = Math.max(0, safeBottom - bottom);
        const topGap = Math.max(0, top - frameTop);
        const activeHeightRatio = Math.min(1, Math.max(0, (bottom - top) / usableHeight));
        verticalBalance = {
          mode: compositionMode,
          source: compositionSource,
          candidateCount: balanceCandidates.length,
          contentRootCount: contentRoots.length,
          excludedChromeCount,
          ignoredSelector: compositionChromeSelector,
          frame: {
            top: number(frameTop),
            safeBottom: number(safeBottom),
            usableHeight: number(usableHeight),
          },
          occupied: {
            top: number(top),
            bottom: number(bottom),
            height: number(Math.max(0, bottom - top)),
          },
          topGap: number(topGap),
          bottomGap: number(bottomGap),
          activeHeightRatio: number(activeHeightRatio),
          occupiedHeightRatio: number(Math.min(1, Math.max(0, occupiedHeight / usableHeight))),
          topHeavyBias: number((bottomGap - topGap) / usableHeight),
          navSafeIntrusion: number(Math.max(0, bottom - safeBottom)),
          anchorMaskPx: number(Math.max(0, (contentBounds?.bottom ?? bottom) - bottom)),
          largestGap: largestGap ? {
            top: number(largestGap.top),
            bottom: number(largestGap.bottom),
            height: number(largestGap.height),
            before: largestGap.before,
            after: largestGap.after,
          } : null,
          thresholds: {
            bottomGapMax: reviewBalanceBottom || null,
            activeHeightMin: reviewBalanceActive || null,
            verticalGapMax: reviewBalanceGap || null,
            navSafeBottom: reviewNavSafeBottom || null,
          },
        };

        const balanceReasons = [];
        const topHeavy = compositionMode === 'top-to-bottom'
          && compositionSource === 'explicit'
          && reviewBalanceBottom > 0
          && reviewBalanceActive > 0
          && reviewBalanceActive <= 1
          && verticalBalance.bottomGap > reviewBalanceBottom
          && verticalBalance.activeHeightRatio < reviewBalanceActive;
        if (topHeavy) {
          balanceReasons.push({
            metric: 'topHeavyComposition',
            bottomGap: verticalBalance.bottomGap,
            bottomGapMax: reviewBalanceBottom,
            activeHeightRatio: verticalBalance.activeHeightRatio,
            activeHeightMin: reviewBalanceActive,
          });
        }
        if (
          compositionMode === 'top-to-bottom'
          && compositionSource === 'explicit'
          && reviewBalanceGap > 0
          && verticalBalance.largestGap
          && verticalBalance.largestGap.height > reviewBalanceGap
        ) {
          balanceReasons.push({
            metric: 'largestVerticalGap',
            actual: verticalBalance.largestGap.height,
            threshold: reviewBalanceGap,
          });
        }
        if (balanceReasons.length > 0) {
          issues.push({
            severity: 'review',
            code: 'vertical_balance_review',
            message: 'Theme-owned vertical-composition thresholds need visual review.',
            reasons: balanceReasons,
            verticalBalance,
          });
        }
        if (
          compositionSource === 'explicit'
          && reviewNavSafeBottom > 0
          && verticalBalance.navSafeIntrusion > CLIP_TOLERANCE
        ) {
          issues.push({
            severity: 'review',
            code: 'nav_safe_intrusion',
            message: 'Meaningful composition content enters the theme-owned navigation safe area.',
            intrusion: verticalBalance.navSafeIntrusion,
            safeBottom: verticalBalance.frame.safeBottom,
          });
        }
      }

      const titleCandidate = candidateElements.find(({ element }) => /^H[1-6]$/.test(element.tagName));
      let title = null;
      if (titleCandidate) {
        const titleRect = titleCandidate.rect;
        const following = candidateElements
          .filter(({ element, rect }) => {
            if (element === titleCandidate.element || rect.top < titleRect.bottom - TOLERANCE) return false;
            const overlap = Math.max(0, Math.min(rect.right, titleRect.right) - Math.max(rect.left, titleRect.left));
            return overlap >= Math.min(rect.width, titleRect.width) * 0.2;
          })
          .sort((a, b) => a.rect.top - b.rect.top)[0];
        const gap = following ? Math.max(0, following.rect.top - titleRect.bottom) : null;
        title = {
          text: briefText(titleCandidate.element),
          bounds: rectObject(titleRect),
          gapToNextContent: gap === null ? null : number(gap),
        };
        if (reviewTitleGap > 0 && gap !== null && gap < reviewTitleGap) {
          issues.push({
            severity: 'review',
            code: 'title_gap_low',
            message: `Title-to-content gap is ${number(gap)}px; review hierarchy and spacing.`,
            gap: number(gap),
            threshold: reviewTitleGap,
          });
        }
      }

      const fontSizes = candidateElements
        .filter(({ element }) => hasDirectText(element) || /^H[1-6]$/.test(element.tagName) || element.tagName === 'P' || element.tagName === 'LI' || element.tagName === 'TD' || element.tagName === 'TH' || element.tagName === 'CODE')
        .map(({ style }) => Number.parseFloat(style.fontSize))
        .filter((size) => Number.isFinite(size) && size > 0);
      const fontRoleFindings = candidateElements
        .filter(({ element }) => hasDirectText(element) || !element.children.length)
        .map(({ element, style }) => {
          const role = style.getPropertyValue('--seaslides-audit-font-role').trim().toLowerCase();
          const threshold = fontRoleThresholds[role] || 0;
          const fontSize = Number.parseFloat(style.fontSize);
          if (!threshold || !Number.isFinite(fontSize) || fontSize + 0.25 >= threshold) return null;
          return {
            role,
            element: elementLabel(element),
            text: briefText(element),
            fontSize: number(fontSize),
            threshold: number(threshold),
          };
        })
        .filter(Boolean);
      if (fontRoleFindings.length > 0) {
        issues.push({
          severity: 'review',
          code: 'font_role_size_review',
          message: `${fontRoleFindings.length} theme-declared text role(s) render below their advisory size.`,
          elements: fontRoleFindings,
        });
      }

      return {
        index: targetIndex + 1,
        id: slide.id || null,
        className: className(slide),
        canvas: { width: canvasWidth, height: canvasHeight },
        scroll: {
          clientWidth,
          clientHeight,
          scrollWidth,
          scrollHeight,
          overflowX: scrollOverflowX,
          overflowY: scrollOverflowY,
        },
        contentBounds,
        bottomWhitespace: contentBounds?.bottomWhitespace ?? canvasHeight,
        verticalBalance,
        title,
        titleGap: title?.gapToNextContent ?? null,
        minFontSize: fontSizes.length ? number(Math.min(...fontSizes)) : null,
        fontRoleReview: {
          thresholds: fontRoleThresholds,
          findings: fontRoleFindings,
        },
        brokenImages,
        internalClipping: clipped,
        headingLineBoxIntersections,
        issues,
      };
    } finally {
      restore();
    }
  }, { targetIndex: slideIndex, canvasWidth: width, canvasHeight: height });
}

async function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const input = path.resolve(args.input);
    const output = path.resolve(args.output);
    if (!(await fileExists(input))) throw new Error(`Input HTML file does not exist: ${input}`);

    const browserPath = await findBrowserExecutable();
    const launchOptions = {
      headless: true,
      timeout: args.timeout,
      args: ['--allow-file-access-from-files'],
    };
    if (browserPath) launchOptions.executablePath = browserPath;

    const browser = await chromium.launch(launchOptions);
    let receipt;
    try {
      const page = await browser.newPage({ viewport: { width: args.width, height: args.height } });
      page.setDefaultTimeout(args.timeout);
      const pageErrors = [];
      page.on('pageerror', (error) => pageErrors.push(error));

      await page.goto(pathToFileURL(input).href, { waitUntil: 'load', timeout: args.timeout });
      await settlePage(page, args.timeout);
      if (pageErrors.length > 0) {
        throw new Error(`Page execution error: ${pageErrors.map((error) => error.message).join('; ')}`);
      }

      const slideCount = await page.locator('section.slide').count();
      if (slideCount === 0) throw new Error('No section.slide elements found in the assembled HTML.');

      const slides = [];
      for (let index = 0; index < slideCount; index += 1) {
        slides.push(await auditSlide(page, index, args.width, args.height));
      }
      const issues = slides.flatMap((slide) => slide.issues.map((issue) => ({ slide: slide.index, ...issue })));
      const blockerCount = issues.filter((issue) => issue.severity === 'blocker').length;
      const reviewCount = issues.filter((issue) => issue.severity === 'review').length;
      receipt = {
        schema: SCHEMA,
        version: VERSION,
        input,
        viewport: { width: args.width, height: args.height },
        summary: {
          status: blockerCount > 0 ? 'blocker' : reviewCount > 0 ? 'review' : 'pass',
          slideCount,
          issueCount: issues.length,
          blockerCount,
          reviewCount,
        },
        issues,
        slides,
      };
    } finally {
      await browser.close();
    }

    await fs.mkdir(path.dirname(output), { recursive: true });
    await fs.writeFile(output, `${JSON.stringify(receipt, null, 2)}\n`, 'utf-8');
    console.log(`-> ${path.relative(process.cwd(), output)}`);
    console.log(`Done! ${receipt.summary.slideCount} slide(s), ${receipt.summary.blockerCount} blocker(s), ${receipt.summary.reviewCount} review item(s).`);
    return receipt.summary.blockerCount > 0 ? 2 : 0;
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    return 1;
  }
}

process.exitCode = await main();
