/**
 * 계약 상수 정본(메인 동결). 바꾸려면 plan/CONTRACTS.md와 같은 커밋으로.
 */

export const VERSION = 2;

/** 계약 판(v2 = 2026-10-08 개정). VERSION은 window.__deck 판이라 따로 둔다 */
export const CONTRACT_VERSION = 2;

/** 정지점 라벨 접두(C6) */
export const STOP_PREFIX = 'stop:';

/** beat·move·stop 이름 형식(C3, C5) */
export const ID_PATTERN = /^[a-z0-9][a-z0-9-]*$/;

/** deck id(C3 v2): `_`로 시작하면 내부 덱(갤러리·다양성 게이트 제외) */
export const DECK_ID_PATTERN = /^_?[a-z0-9][a-z0-9-]*$/;

/** move role(C5) */
export const ROLES = Object.freeze(['enter', 'exit', 'link', 'step', 'camera', 'ambient']);

/** beat type(C4) */
export const BEAT_TYPES = Object.freeze([
  'text',
  'photo',
  'video',
  'number',
  'chart',
  'chronology',
  'compare',
  'quote',
  'prompt',
  'code',
  'sequence',
]);

/** 화면 slot(C8) */
export const SLOTS = Object.freeze(['center', 'left', 'right', 'top', 'bottom', 'full', 'lower-third']);

/** move family. 'engine'은 내장 move 전용(C6) */
export const FAMILIES = Object.freeze([
  'reveal',
  'type',
  'morph',
  'camera',
  'rail',
  'data',
  'media',
  'assemble',
  'emphasis',
  'engine',
]);

/** 내장 move id(C6). registry가 항상 포함 */
export const ENGINE_MOVES = Object.freeze([
  'engine:fade-in',
  'engine:fade-out',
  'engine:crossfade',
  'engine:none',
]);

/** 「움직임 없음」 내장 move(C6 v2): 모든 role에 쓸 수 있고 role·반복 검사 면제 */
export const NO_MOVE = 'engine:none';

/** reduced-motion 'fade' 대체표(C6) */
export const REDUCE_FALLBACK = Object.freeze({
  enter: 'engine:fade-in',
  exit: 'engine:fade-out',
  link: 'engine:crossfade',
  step: 'engine:fade-in',
  ambient: 'engine:none',
});

/** timing 기본값(C6). 순서: 이것 → concept.timing → deck.timing */
export const ENGINE_TIMING_DEFAULTS = Object.freeze({ unit: 0.55, hold: 0.6, overlap: 0.2, tail: 0.8 });

/** 뷰포트 기준(C2) */
export const VIEWPORT = Object.freeze({ designW: 1920, portraitW: 760, aspect: 16 / 9, maxDpr: 2 });

/**
 * slot 기본 배치(C8 v2). x·y = 화면 비율 위치, ax·ay = 블록 안 기준점(0 = 왼쪽·위 끝, 1 = 오른쪽·아래 끝).
 * concept.slots[slot]이 키 단위로 덮어씀. full은 inset 0(위치 무시)
 */
export const SLOT_DEFAULTS = Object.freeze({
  center: Object.freeze({ x: 0.5, y: 0.5, ax: 0.5, ay: 0.5 }),
  left: Object.freeze({ x: 0.0625, y: 0.5, ax: 0, ay: 0.5 }),
  right: Object.freeze({ x: 0.9375, y: 0.5, ax: 1, ay: 0.5 }),
  top: Object.freeze({ x: 0.5, y: 0.0625, ax: 0.5, ay: 0 }),
  bottom: Object.freeze({ x: 0.5, y: 0.9375, ax: 0.5, ay: 1 }),
  full: Object.freeze({ x: 0, y: 0, ax: 0, ay: 0 }),
  'lower-third': Object.freeze({ x: 0.0625, y: 0.9, ax: 0, ay: 1 }),
});

/** beat tone(C3 v2): 루트 data-tone, tokens.css가 C11 변수만 재정의 */
export const TONE_RANGE = Object.freeze({ min: 0, max: 5 });

/** 상태 층 기본 이름(C4 v2 chart.states). states[].name으로 못 씀 */
export const BASE_STATE = 'base';

/** 출처 감사 대상 beat type(C3 v2). compare는 items[].value가 하나라도 있을 때만 */
export const SOURCED_TYPES = Object.freeze(['number', 'quote', 'photo', 'chart', 'compare']);

/** 카메라 tilt 상한(°)(C8, C10) */
export const MAX_TILT = 12;

/** 3D 속성: camera family 밖 사용 금지(C10) */
export const CAMERA_ONLY_PROPS = Object.freeze([
  'rotationX',
  'rotationY',
  'rotateX',
  'rotateY',
  'z',
  'translateZ',
  'transformPerspective',
  'perspective',
]);

/** window CustomEvent 이름(C12) */
export const EVENTS = Object.freeze({
  ready: 'scrolline:ready',
  rebuild: 'scrolline:rebuild',
  stop: 'scrolline:stop',
  active: 'scrolline:active',
  blackout: 'scrolline:blackout',
  exportReady: 'scrolline:export-ready',
});

/** 발표 키(C12). 'Shift+ '는 Shift+Space */
export const PRESENTER_KEYS = Object.freeze({
  next: ['ArrowRight', 'ArrowDown', 'PageDown', ' '],
  prev: ['ArrowLeft', 'ArrowUp', 'PageUp', 'Shift+ '],
  first: ['Home'],
  last: ['End'],
  blackout: ['b', '.'],
  fullscreen: ['f'],
});

/** 발표 키 이동 규칙(C12) */
export const PRESENTER_TRAVEL = Object.freeze({
  minGap: 0.01,
  base: 0.9,
  perScreen: 0.35,
  max: 2.6,
  settleMs: 150,
  stopEps: 0.02,
});

/** resize 재빌드 규칙(C12) */
export const RESIZE = Object.freeze({ debounceMs: 200, heightTolerance: 0.15 });

/** CSS 변수 이름(C2, C11) */
export const CSS_VARS = Object.freeze({
  engine: Object.freeze(['--px', '--vw-px', '--vh-px', '--sl-portrait']),
  concept: Object.freeze([
    '--sl-bg',
    '--sl-fg',
    '--sl-fg-muted',
    '--sl-accent',
    '--sl-accent-2',
    '--sl-rule',
    '--sl-scrim',
    '--sl-font-display',
    '--sl-font-text',
    '--sl-font-mono',
    '--sl-weight-display',
    '--sl-weight-text',
    '--sl-size-xl',
    '--sl-size-l',
    '--sl-size-m',
    '--sl-size-s',
    '--sl-size-caption',
    '--sl-leading-display',
    '--sl-leading-text',
    '--sl-tracking-display',
    '--sl-perspective',
    '--sl-gutter',
    '--sl-radius',
    '--sl-caption-left',
    '--sl-caption-bottom',
    '--sl-caption-width',
  ]),
});

/** 내용 감사 패턴 13종(C3). 문자열 필드 하나라도 맞으면 오류 */
export const PLACEHOLDER_PATTERNS = Object.freeze([
  /^\s*$/,
  /\bTODO\b/,
  /\bTBD\b/,
  /lorem/i,
  /ipsum/i,
  /x{3,}/i,
  /「\s*x\s*」/i,
  /\?{3,}/,
  /\{\{/,
  /\}\}/,
  /<placeholder>/i,
  /자리표/,
  /예시 문구/,
]);

/** 덱 → MP4 발표 경로 기본값(C14) */
export const EXPORT_DEFAULTS = Object.freeze({
  width: 1920,
  height: 1080,
  fps: 30,
  secondsPerUnit: 0.5,
  stopHold: 1.6,
  travelMin: 0.6,
  travelMax: 5,
  lead: 0.4,
  tail: 1.2,
  ease: 'power1.inOut',
  compositionId: 'scrolline',
});

/** 프레임 시퀀스 로딩 규칙(C13) */
export const FRAMES = Object.freeze({ coarseStep: 8, window: 12, bigTierMinPx: 1400, smallTier: 960 });
