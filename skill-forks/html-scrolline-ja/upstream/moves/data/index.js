/**
 * move family 'data'(CONTRACTS C5·C16). 메인 소유: W3 잡이 move를 병합할 때 메인이 import 한 줄 + 배열 항목 하나를 추가한다.
 * 규칙: default export = MoveDef 배열, id 알파벳 순, 이 폴더 밖 import 금지(./<id>.js만). 목록 정본 = plan/MOVES.md §3.
 */
import aggregateSplit from './aggregate-split.js';
import annotationPin from './annotation-pin.js';
import baselineGrow from './baseline-grow.js';
import countRoll from './count-roll.js';
import divergeGrow from './diverge-grow.js';
import dotMultiply from './dot-multiply.js';
import dotSeed from './dot-seed.js';
import dotsPour from './dots-pour.js';
import forecastExtend from './forecast-extend.js';
import inkIn from './ink-in.js';
import lineDraw from './line-draw.js';
import lineToWaffle from './line-to-waffle.js';
import markMorph from './mark-morph.js';
import numberSlam from './number-slam.js';
import pointFocus from './point-focus.js';
import rankReorder from './rank-reorder.js';
import strikeSwap from './strike-swap.js';
import thresholdLine from './threshold-line.js';
import waffleRecount from './waffle-recount.js';

export default [
  aggregateSplit,
  annotationPin,
  baselineGrow,
  countRoll,
  divergeGrow,
  dotMultiply,
  dotSeed,
  dotsPour,
  forecastExtend,
  inkIn,
  lineDraw,
  lineToWaffle,
  markMorph,
  numberSlam,
  pointFocus,
  rankReorder,
  strikeSwap,
  thresholdLine,
  waffleRecount,
];
