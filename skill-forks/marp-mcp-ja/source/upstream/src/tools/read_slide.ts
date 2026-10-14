/**
 * Tool: read_slide
 * Reads slide content from a Marp presentation file by slide ID or returns all slides.
 */

import { z } from "zod";
import { promises as fs } from "fs";
import { extractSlideId, ensureSlideId } from "../utils/slide-id.js";
import { validateFilePath } from "../utils/path-validator.js";
import { parseFrontmatter, splitSlides } from "../utils/frontmatter.js";
import { MAX_FILE_SIZE } from "../utils/constants.js";
import { createErrorResponse, createSuccessResponse } from "../utils/response.js";
import type { ToolResponse } from "../types/common.js";

export const readSlideSchema = z.object({
  filePath: z.string().describe("Absolute path to the Marp markdown file (must end in .md)"),
  slideId: z
    .string()
    .optional()
    .describe(
      "The UUID slide ID from a '<!-- slide-id: ... -->' comment. " +
        "Omit to list all slides with their IDs and positions. " +
        "Use the returned slideId values with manage_slide for replace/delete/after/before operations."
    ),
});

/**
 * MCP Tool: Reads slide content from a Marp presentation file.
 * Returns a specific slide by ID, or all slides with their IDs and positions.
 *
 * @param {object} options - The read options
 * @param {string} options.filePath - Absolute path to the Marp markdown file
 * @param {string} [options.slideId] - Optional slide ID to read a specific slide
 * @returns {Promise<ToolResponse>} Slide content with metadata
 */
export async function readSlide({
  filePath,
  slideId,
}: z.infer<typeof readSlideSchema>): Promise<ToolResponse> {
  // Validate file path
  const pathError = validateFilePath(filePath);
  if (pathError) {
    return createErrorResponse(pathError);
  }

  let existingContent: string;
  try {
    existingContent = await fs.readFile(filePath, "utf-8");
  } catch (error) {
    return createErrorResponse(
      `Could not read file at ${filePath}: ${error instanceof Error ? error.message : String(error)}`
    );
  }

  if (existingContent.length > MAX_FILE_SIZE) {
    return createErrorResponse(
      `File too large (${existingContent.length} bytes, max ${MAX_FILE_SIZE} bytes)`
    );
  }

  const { frontmatter, body } = parseFrontmatter(existingContent);
  const slides = splitSlides(body);

  // Ensure all slides have IDs (for consistent output)
  const slidesWithIds = slides.map(slide => ensureSlideId(slide));

  if (slideId) {
    // Find specific slide by ID
    const found = slidesWithIds.find(s => s.id === slideId);
    if (!found) {
      return createErrorResponse(`Slide with ID "${slideId}" not found`);
    }

    const position = slidesWithIds.findIndex(s => s.id === slideId) + 1;

    return createSuccessResponse({
      slideId,
      position,
      totalSlides: slidesWithIds.length,
      content: found.content,
      file: filePath,
    });
  }

  // Return all slides
  const allSlides = slidesWithIds.map((s, index) => ({
    slideId: s.id,
    position: index + 1,
    content: s.content,
  }));

  return createSuccessResponse({
    totalSlides: allSlides.length,
    slides: allSlides,
    file: filePath,
  });
}
