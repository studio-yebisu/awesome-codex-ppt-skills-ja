/**
 * Utilities for describing text length constraints in prompts
 */

interface LengthPromptOptions {
  /**
   * Ratio (0-1) used to estimate the Japanese character limit from the English max length.
   * Defaults to 0.6 (roughly 60%).
   */
  japaneseRatio?: number;
  /**
   * Additional note appended to the length description, e.g., "no line break".
   */
  note?: string;
}

const DEFAULT_JAPANESE_RATIO = 0.6;

/**
 * Returns a standardized text snippet like
 * "max 50 chars, ~30 chars for Japanese" plus optional notes.
 */
export const formatLengthPrompt = (
  maxLength: number,
  options: LengthPromptOptions = {},
): string => {
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
export const withLengthPrompt = (
  baseDescription: string,
  maxLength: number,
  options?: LengthPromptOptions,
): string => {
  return `${baseDescription} (${formatLengthPrompt(maxLength, options)})`;
};
