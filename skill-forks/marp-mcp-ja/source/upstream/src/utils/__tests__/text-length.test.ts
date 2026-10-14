import { describe, expect, test } from "@jest/globals";
import {
  formatLengthPrompt,
  withLengthPrompt,
} from "../text-length.js";

describe("text-length utils", () => {
  test("formatLengthPrompt returns default ratio text", () => {
    expect(formatLengthPrompt(50)).toBe(
      "max 50 chars, ~30 chars for Japanese",
    );
  });

  test("formatLengthPrompt allows overriding ratio and notes", () => {
    expect(
      formatLengthPrompt(80, {
        japaneseRatio: 0.5,
        note: "no line break",
      }),
    ).toBe("max 80 chars, ~40 chars for Japanese, no line break");
  });

  test("withLengthPrompt prepends base description", () => {
    expect(withLengthPrompt("Slide heading", 40)).toBe(
      "Slide heading (max 40 chars, ~24 chars for Japanese)",
    );
  });
});
