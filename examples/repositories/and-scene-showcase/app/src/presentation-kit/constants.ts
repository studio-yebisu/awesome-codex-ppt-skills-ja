/** Shared timing and geometry constants for the scene kit. */

// Easing for layout morphs and reveals — slow, confident, presentation-grade.
export const EASE = [0.22, 1, 0.36, 1] as const
export const LAYOUT_T = { duration: 0.7, ease: EASE }

// A newcomer waits this long before fading in, so the pieces already on screen
// have visibly moved to their new spots first. Without it, a new element pops in
// at full strength while the old ones are mid-morph, and the eye can't tell what
// arrived from what just shifted. See the Appear helper in nodes.
export const ENTER_DELAY = 0.4
export const ENTER_T = { duration: 0.45, ease: EASE, delay: ENTER_DELAY }

// The diagram is laid out once in this fixed "design canvas" and then scaled
// uniformly to fit the viewport (see useFitScale). A fixed coordinate space
// means the composition never reflows and the scale is constant during a
// morph — so layoutId transitions stay clean at every viewport size.
export const DESIGN_W = 880
export const DESIGN_H = 380
export const MIN_SCALE = 0.35

/**
 * Per-mode stage geometry. Scale is constant *within* a mode, so step→step
 * layoutId morphs stay clean; toggling modes is a re-render, not a morph.
 *
 *  - browse  reserves generous chrome for the multi-line caption + nav at the
 *            bottom; the title sits at the top. Fits the full design canvas.
 *  - present carries the same top title but no caption — only progress dots sit
 *            at the bottom — so it keeps the title's headroom up top and trims
 *            the bottom band, fitting the diagram to a narrower width (~790)
 *            so a wide step doesn't shrink the rest. A higher max-scale lets the
 *            diagram grow on taller (16:9/4:3) screens.
 *
 * `fitW` is both the width fed to the fit calc and the canvas width, so the
 * scaled canvas always equals the available width (no horizontal overflow).
 */
export const STAGE_LAYOUT = {
  browse: { top: 96, bottom: 188, padX: 32, fitW: DESIGN_W, maxScale: 1.8 },
  present: { top: 104, bottom: 76, padX: 20, fitW: 790, maxScale: 2.6 },
} as const

export type StageLayout = (typeof STAGE_LAYOUT)[keyof typeof STAGE_LAYOUT]
