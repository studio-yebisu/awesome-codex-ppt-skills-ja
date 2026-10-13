/**
 * move family 'rail'(CONTRACTS C5·C16). 메인 소유: W3 잡이 move를 병합할 때 메인이 import 한 줄 + 배열 항목 하나를 추가한다.
 * 규칙: default export = MoveDef 배열, id 알파벳 순, 이 폴더 밖 import 금지(./<id>.js만). 목록 정본 = plan/MOVES.md §3.
 */
import counterHandoff from './counter-handoff.js';
import eraShift from './era-shift.js';
import foldToRail from './fold-to-rail.js';
import railAdvance from './rail-advance.js';
import railCompress from './rail-compress.js';
import railDraw from './rail-draw.js';
import railDrop from './rail-drop.js';
import railLift from './rail-lift.js';
import railSplitOpen from './rail-split-open.js';
import railSurface from './rail-surface.js';

export default [
  counterHandoff,
  eraShift,
  foldToRail,
  railAdvance,
  railCompress,
  railDraw,
  railDrop,
  railLift,
  railSplitOpen,
  railSurface,
];
