/**
 * CLI helper utilities
 */

import { resolve } from "path";
import type { ToolResponse } from "../types/common.js";

/**
 * Resolves a file path to an absolute path.
 * If the path is already absolute, it is returned as-is.
 * Otherwise, it is resolved relative to the current working directory.
 */
export function resolveFilePath(filePath: string): string {
  return resolve(filePath);
}

/**
 * Extracts text from a ToolResponse and outputs it to stdout.
 * If the response text starts with "Error:", exits with code 1.
 */
export function outputResult(response: ToolResponse): void {
  const text = response.content.map((c) => c.text).join("\n");
  const isError = text.startsWith("Error:");

  if (isError) {
    process.stderr.write(text + "\n");
    process.exit(1);
  }

  process.stdout.write(text + "\n");
}
