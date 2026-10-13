// 계약 표면 검사: engine/index.js가 CONTRACTS.md C19 이름을 전부 내보내고, 상수가 계약 값과 같은지.
import { describe, it, expect } from 'vitest';
import * as api from './index.js';
import { beatTypes } from './beats/index.js';

const FUNCTIONS = [
  'createStage',
  'computeViewport',
  'el',
  'words',
  'chars',
  'createRng',
  'hashSeed',
  'resolveParams',
  'validateSchema',
  'prefersReducedMotion',
  'createA11y',
  'plan',
  'build',
  'resolveTiming',
  'createRegistry',
  'validateDeck',
  'createScrollDriver',
  'createPresenter',
  'measure',
  'defaultMeasure',
  'anchorOf',
  'rectIn',
  'toInset',
  'transferVars',
  'frameSequence',
  'videoClip',
  'textMask',
  'preloadImages',
  'pickTier',
  'loadOrder',
  'exportPath',
  'buildExportTimeline',
  'toExportSeconds',
  'boot',
];
const CONSTANTS = [
  'VERSION',
  'STOP_PREFIX',
  'ID_PATTERN',
  'ROLES',
  'BEAT_TYPES',
  'SLOTS',
  'FAMILIES',
  'ENGINE_MOVES',
  'REDUCE_FALLBACK',
  'ENGINE_TIMING_DEFAULTS',
  'VIEWPORT',
  'MAX_TILT',
  'CAMERA_ONLY_PROPS',
  'EVENTS',
  'PRESENTER_KEYS',
  'PRESENTER_TRAVEL',
  'RESIZE',
  'CSS_VARS',
  'PLACEHOLDER_PATTERNS',
  'EXPORT_DEFAULTS',
  'FRAMES',
  'ENGINE_MOVE_DEFS',
  'SchemaError',
  'beatTypes',
];

describe('engine 공개 API', () => {
  it.each(FUNCTIONS)('%s 함수를 내보낸다', (name) => {
    expect(typeof api[name]).toBe('function');
  });
  it.each(CONSTANTS)('%s 를 내보낸다', (name) => {
    expect(api[name]).toBeDefined();
  });
  it('계약 밖 이름을 내보내지 않는다', () => {
    expect(Object.keys(api).sort()).toEqual([...FUNCTIONS, ...CONSTANTS].sort());
  });
});

describe('계약 상수', () => {
  it('timing 기본값', () => {
    expect(api.ENGINE_TIMING_DEFAULTS).toEqual({ unit: 0.55, hold: 0.6, overlap: 0.2, tail: 0.8 });
    expect(api.resolveTiming({ hold: 1 }, { unit: 0.4 })).toEqual({
      unit: 0.4,
      hold: 1,
      overlap: 0.2,
      tail: 0.8,
    });
  });
  it('이벤트 이름', () => {
    expect(Object.values(api.EVENTS)).toEqual([
      'scrolline:ready',
      'scrolline:rebuild',
      'scrolline:stop',
      'scrolline:active',
      'scrolline:blackout',
      'scrolline:export-ready',
    ]);
  });
  it('자리표 패턴 13종이 대표 문자열을 잡고 정상 문장은 통과', () => {
    expect(api.PLACEHOLDER_PATTERNS).toHaveLength(13);
    const bad = [
      '',
      '  ',
      'TODO 채우기',
      'TBD',
      'Lorem',
      'ipsum',
      'xxx',
      '「x」',
      '???',
      '{{name}}',
      '<placeholder>',
      '자리표',
      '예시 문구입니다',
    ];
    for (const s of bad)
      expect(
        api.PLACEHOLDER_PATTERNS.some((p) => p.test(s)),
        s,
      ).toBe(true);
    for (const s of ['매출이 3년 만에 두 배', 'Q4 revenue doubled', 'todo 앱 출시']) {
      expect(
        api.PLACEHOLDER_PATTERNS.some((p) => p.test(s)),
        s,
      ).toBe(false);
    }
  });
  it('id 형식', () => {
    expect(api.ID_PATTERN.test('match-cut')).toBe(true);
    expect(api.ID_PATTERN.test('Match_Cut')).toBe(false);
  });
});

describe('beat type 표', () => {
  it('sequence를 뺀 10종이 C4 순서로 있다', () => {
    expect(Object.keys(beatTypes)).toEqual(api.BEAT_TYPES.filter((t) => t !== 'sequence'));
  });
  it.each(Object.entries(beatTypes))('%s: type·primary·fields·render 형식', (type, def) => {
    expect(def.type).toBe(type);
    expect(typeof def.primary).toBe('string');
    expect(typeof def.render).toBe('function');
    for (const [k, f] of Object.entries(def.fields)) {
      expect(typeof f.doc, `${type}.${k}.doc`).toBe('string');
      expect(typeof f.type, `${type}.${k}.type`).toBe('string');
    }
  });
});
