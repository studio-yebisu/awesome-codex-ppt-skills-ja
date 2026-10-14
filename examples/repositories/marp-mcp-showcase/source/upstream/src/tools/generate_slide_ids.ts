/**
 * Tool: generate_slide_ids
 * Ensures every slide in a Marp markdown file has a slide ID comment.
 * This tool intentionally does not modify frontmatter.
 */

import { z } from "zod";
import { promises as fs } from "fs";
import { ensureAllSlideIds } from "../utils/slide-id.js";
import { validateFilePath } from "../utils/path-validator.js";
import { parseFrontmatter, splitSlides, joinSlides } from "../utils/frontmatter.js";
import { MAX_FILE_SIZE } from "../utils/constants.js";
import { createErrorResponse, createSuccessResponse } from "../utils/response.js";
import type { ToolResponse } from "../types/common.js";

export const generateSlideIdsSchema = z.object({
  filePath: z
    .string()
    .describe(
      "Absolute path to the Marp markdown file (must end in .md). " +
        "This tool adds '<!-- slide-id: UUID -->' comments to any slides that lack them. " +
        "Safe to call multiple times — existing IDs are never changed."
    ),
});

/**
 * Generates unique slide IDs for all slides in a Marp markdown file.
 *
 * @param {object} options - The generation options
 * @param {string} options.filePath - Absolute path to the Marp markdown file
 * @returns {Promise<ToolResponse>} Operation result with generated IDs
 */
export async function generateSlideIds({
  filePath,
}: z.infer<typeof generateSlideIdsSchema>): Promise<ToolResponse> {
  // Validate file path
  const pathError = validateFilePath(filePath);
  if (pathError) {
    return createErrorResponse(pathError);
  }

  try {
    // Read existing file
    let existingContent: string;
    try {
      existingContent = await fs.readFile(filePath, "utf-8");
    } catch (error) {
      return createErrorResponse(
        `Could not read file at ${filePath}: ${error instanceof Error ? error.message : String(error)}`
      );
    }

    // Check file size
    if (existingContent.length > MAX_FILE_SIZE) {
      return createErrorResponse(
        `File too large (${existingContent.length} bytes, max ${MAX_FILE_SIZE} bytes)`
      );
    }

    const { frontmatter, body } = parseFrontmatter(existingContent);
    const slides = splitSlides(body);

    // Ensure all slides have IDs
    const { slides: updatedSlides, idToIndex } = ensureAllSlideIds(slides);

    // Check if any changes were made
    const slidesChanged = slides.some((slide, index) => slide !== updatedSlides[index]);
    if (!slidesChanged) {
      return createSuccessResponse({
        message: "All slides already have IDs",
        totalSlides: slides.length,
        file: filePath,
      });
    }

    // Write updated content
    const newContent = joinSlides(frontmatter, updatedSlides);
    await fs.writeFile(filePath, newContent, "utf-8");

    // Create ID summary
    const idSummary = Array.from(idToIndex.entries()).map(([id, index]) => ({
      position: index + 1,
      slideId: id,
    }));

    return createSuccessResponse({
      message: "Generated slide IDs successfully",
      totalSlides: updatedSlides.length,
      idsGenerated: idSummary.length,
      file: filePath,
    });
  } catch (error) {
    return createErrorResponse(
      `Error generating slide IDs: ${error instanceof Error ? error.message : String(error)}`
    );
  }
}
