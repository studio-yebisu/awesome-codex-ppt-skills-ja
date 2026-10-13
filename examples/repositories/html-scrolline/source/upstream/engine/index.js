/**
 * engine 공개 API(메인 동결). moves·concepts·decks는 이 파일만 import한다(CONTRACTS C1 R2).
 * 테스트 harness는 별도 진입점 engine/testing.js(*.test.js 전용).
 * v2: constants.js는 이름을 골라 내보낸다. C19 밖 상수(DECK_ID_PATTERN·SLOT_DEFAULTS 등)는 engine 내부 전용.
 */

export {
  VERSION,
  STOP_PREFIX,
  ID_PATTERN,
  ROLES,
  BEAT_TYPES,
  SLOTS,
  FAMILIES,
  ENGINE_MOVES,
  REDUCE_FALLBACK,
  ENGINE_TIMING_DEFAULTS,
  VIEWPORT,
  MAX_TILT,
  CAMERA_ONLY_PROPS,
  EVENTS,
  PRESENTER_KEYS,
  PRESENTER_TRAVEL,
  RESIZE,
  CSS_VARS,
  PLACEHOLDER_PATTERNS,
  EXPORT_DEFAULTS,
  FRAMES,
} from './constants.js';
export { createStage, computeViewport } from './stage.js';
export { el, words, chars } from './util/dom.js';
export { createRng, hashSeed } from './util/rng.js';
export { resolveParams, validateSchema, SchemaError } from './util/schema.js';
export { prefersReducedMotion, createA11y } from './a11y.js';
export { plan, build, resolveTiming, ENGINE_MOVE_DEFS } from './timeline.js';
export { createRegistry } from './registry.js';
export { validateDeck } from './deck-schema.js';
export { createScrollDriver } from './scroll.js';
export { createPresenter } from './presenter.js';
export { measure, defaultMeasure, anchorOf, rectIn, toInset, transferVars } from './handoff.js';
export { frameSequence, videoClip, textMask, preloadImages, pickTier, loadOrder } from './media.js';
export { exportPath, buildExportTimeline, toExportSeconds } from './export.js';
export { beatTypes } from './beats/index.js';
export { boot } from './boot.js';
