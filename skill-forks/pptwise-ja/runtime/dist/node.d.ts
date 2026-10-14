export { P as PptwisePlatform, i as installPlatform } from './registry-C9YsvcP8.js';

/** Wire Node implementations (linkedom DOM, sharp image re-encode + SVG
 *  rasterize + real image decode) into the SDK. `decodeImage` is only
 *  installed when Sharp resolves; see {@link sharpIsResolvable}. */
declare function installNodePlatform(): void;

export { installNodePlatform };
