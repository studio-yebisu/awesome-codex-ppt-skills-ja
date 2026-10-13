/**
 * move family 'reveal'(CONTRACTS C5·C16). 메인 소유: W3 잡이 move를 병합할 때 메인이 import 한 줄 + 배열 항목 하나를 추가한다.
 * 규칙: default export = MoveDef 배열, id 알파벳 순, 이 폴더 밖 import 금지(./<id>.js만). 목록 정본 = plan/MOVES.md §3.
 */
import blurDrop from './blur-drop.js';
import focusPull from './focus-pull.js';
import lightsOut from './lights-out.js';
import litFromDark from './lit-from-dark.js';

export default [blurDrop, focusPull, lightsOut, litFromDark];
