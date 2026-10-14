/**
 * Utilities for describing text length constraints in prompts
 */
const DEFAULT_JAPANESE_RATIO = 0.6;
/**
 * Returns a standardized text snippet like
 * "max 50 chars, ~30 chars for Japanese" plus optional notes.
 */
export const formatLengthPrompt = (maxLength, options = {}) => {
    const ratio = options.japaneseRatio ?? DEFAULT_JAPANESE_RATIO;
    const japaneseMax = Math.max(1, Math.round(maxLength * ratio));
    let prompt = `max ${maxLength} chars, ~${japaneseMax} chars for Japanese`;
    if (options.note) {
        prompt += `, ${options.note}`;
    }
    return prompt;
};
/**
 * Helper to append a standardized length prompt to a base description.
 */
export const withLengthPrompt = (baseDescription, maxLength, options) => {
    return `${baseDescription} (${formatLengthPrompt(maxLength, options)})`;
};
