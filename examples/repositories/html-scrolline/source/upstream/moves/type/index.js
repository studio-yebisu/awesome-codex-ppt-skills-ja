/**
 * move family 'type'(CONTRACTS C5·C16). 메인 소유: W3 잡이 move를 병합할 때 메인이 import 한 줄 + 배열 항목 하나를 추가한다.
 * 규칙: default export = MoveDef 배열, id 알파벳 순, 이 폴더 밖 import 금지(./<id>.js만). 목록 정본 = plan/MOVES.md §3.
 */
import caretBlink from './caret-blink.js';
import glyphRise from './glyph-rise.js';
import halfSplit from './half-split.js';
import lineFocus from './line-focus.js';
import lineMaskRise from './line-mask-rise.js';
import mapLabelSettle from './map-label-settle.js';
import phraseFold from './phrase-fold.js';
import pushBuild from './push-build.js';
import resultStream from './result-stream.js';
import scrambleOut from './scramble-out.js';
import scrambleSwap from './scramble-swap.js';
import slotPick from './slot-pick.js';
import sweepOut from './sweep-out.js';
import trackingClose from './tracking-close.js';
import typeOn from './type-on.js';
import wordSlam from './word-slam.js';

export default [
  caretBlink,
  glyphRise,
  halfSplit,
  lineFocus,
  lineMaskRise,
  mapLabelSettle,
  phraseFold,
  pushBuild,
  resultStream,
  scrambleOut,
  scrambleSwap,
  slotPick,
  sweepOut,
  trackingClose,
  typeOn,
  wordSlam,
];
