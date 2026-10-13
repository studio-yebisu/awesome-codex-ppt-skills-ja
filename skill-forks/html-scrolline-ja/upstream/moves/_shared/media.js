/** Frame-sequence access and seek-safe scrubbing. */
import { driveValue } from './drive.js';

export function frameSeqOf(beat) {
  return beat?.media?.seq ?? beat?.part?.('media')?.[0]?.slSeq ?? null;
}
export function scrubTo(tl, seq, { from, to, at, duration, ease = 'none' }) {
  return driveValue(tl, (p) => seq?.setProgress(p), { from, to, at, duration, ease });
}
