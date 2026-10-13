/**
 * beat type 표(CONTRACTS C4). 'sequence'는 덱이 boot({sequences})로 넘긴다.
 */
import text from './text.js';
import photo from './photo.js';
import video from './video.js';
import number from './number.js';
import chart from './chart.js';
import chronology from './chronology.js';
import compare from './compare.js';
import quote from './quote.js';
import prompt from './prompt.js';
import code from './code.js';

/** @type {Record<string, import('../types.js').BeatTypeDef>} */
export const beatTypes = Object.freeze({
  text,
  photo,
  video,
  number,
  chart,
  chronology,
  compare,
  quote,
  prompt,
  code,
});
