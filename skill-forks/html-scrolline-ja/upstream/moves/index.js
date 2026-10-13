/**
 * move registry(CONTRACTS C16, 메인 소유). family index(./<family>/index.js)를 묶어 registry 하나로 만든다.
 * family index는 W3 병합 때 메인이 채운다(plan/WORK-SPLIT-W3.md §병합).
 */
import { createRegistry } from '../engine/index.js';
import assemble from './assemble/index.js';
import camera from './camera/index.js';
import data from './data/index.js';
import emphasis from './emphasis/index.js';
import media from './media/index.js';
import morph from './morph/index.js';
import rail from './rail/index.js';
import reveal from './reveal/index.js';
import type from './type/index.js';

export default createRegistry([...assemble, ...camera, ...data, ...emphasis, ...media, ...morph, ...rail, ...reveal, ...type]);
