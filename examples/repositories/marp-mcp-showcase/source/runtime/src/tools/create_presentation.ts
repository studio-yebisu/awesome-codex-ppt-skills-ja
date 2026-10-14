/**
 * Tool: create_presentation
 * Creates a new Marp presentation file with proper frontmatter and optional placeholder slides.
 * Orchestrates set_frontmatter, manage_slide, and generate_slide_ids in a single call.
 */

import { z } from "zod";
import { promises as fs } from "fs";
import { validateFilePath } from "../utils/path-validator.js";
import { setFrontmatter } from "./set_frontmatter.js";
import { manageSlide } from "./manage_slide.js";
import { generateSlideIds } from "./generate_slide_ids.js";
import { createErrorResponse, createSuccessResponse } from "../utils/response.js";
import type { ToolResponse } from "../types/common.js";

export const createPresentationSchema = z.object({
  filePath: z.string().describe(
    "Absolute path where the new .md file should be created. " +
      "The file must NOT already exist — this tool creates it fresh."
  ),
  title: z.string().describe(
    "Presentation title. Used as the title slide heading and as the header text on all slides."
  ),
  subtitle: z.string().optional().describe(
    "Optional subtitle or author/event info displayed on the title slide."
  ),
  paginate: z.boolean().optional().describe(
    "Show slide page numbers (default: true)."
  ),
  slideCount: z
    .number()
    .int()
    .min(0)
    .max(20)
    .optional()
    .describe(
      "Number of blank content placeholder slides to add after the title slide (default: 0). " +
        "Each placeholder uses the 'content' layout with a generic heading."
    ),
});

/**
 * MCP Tool: Creates a new Marp presentation with frontmatter, title slide, and optional placeholders.
 *
 * @param {object} options - Creation options
 * @param {string} options.filePath - Absolute path for the new file (must not exist)
 * @param {string} options.title - Presentation title
 * @param {string} [options.subtitle] - Optional subtitle for the title slide
 * @param {boolean} [options.paginate] - Show page numbers (default: true)
 * @param {number} [options.slideCount] - Number of placeholder slides (default: 0)
 * @returns {Promise<ToolResponse>} Result with file path and slide IDs
 */
export async function createPresentation({
  filePath,
  title,
  subtitle,
  paginate = true,
  slideCount = 0,
}: z.infer<typeof createPresentationSchema>): Promise<ToolResponse> {
  // Validate file path
  const pathError = validateFilePath(filePath);
  if (pathError) {
    return createErrorResponse(pathError);
  }

  // Ensure file does not already exist
  try {
    await fs.access(filePath);
    // If access succeeds, file already exists
    return createErrorResponse(
      `File already exists: ${filePath}. Use manage_slide to edit an existing presentation, or choose a different path.`
    );
  } catch {
    // File does not exist — this is expected; proceed
  }

  // Write minimal stub so set_frontmatter can read it
  try {
    await fs.writeFile(filePath, "---\nmarp: true\n---\n\n", "utf-8");
  } catch (error) {
    return createErrorResponse(
      `Could not create file at ${filePath}: ${error instanceof Error ? error.message : String(error)}`
    );
  }

  // Set frontmatter (injects theme, style CSS, header, paginate)
  const frontmatterResult = await setFrontmatter({
    filePath,
    header: title,
    paginate,
  });
  if (frontmatterResult.isError) {
    return frontmatterResult;
  }

  // Add title slide
  const titleResult = await manageSlide({
    filePath,
    layoutType: "title",
    params: { heading: title, ...(subtitle ? { content: subtitle } : {}) },
    mode: "insert",
    position: "end",
  });
  if (titleResult.isError) {
    return titleResult;
  }

  // Add content placeholder slides
  for (let i = 1; i <= slideCount; i++) {
    const slideResult = await manageSlide({
      filePath,
      layoutType: "content",
      params: {
        heading: `Slide ${i}`,
        body: "Add your content here.",
      },
      mode: "insert",
      position: "end",
    });
    if (slideResult.isError) {
      return slideResult;
    }
  }

  // Generate stable slide IDs for all slides
  const idsResult = await generateSlideIds({ filePath });
  if (idsResult.isError) {
    return idsResult;
  }

  const totalSlides = 1 + slideCount;

  return createSuccessResponse({
    message: `Created presentation with ${totalSlides} slide${totalSlides !== 1 ? "s" : ""}`,
    filePath,
    title,
    totalSlides,
    workflow: [
      "Use list_layouts to see available layouts",
      "Use manage_slide to add or edit slides",
      "Use read_slide to list all slides and their IDs",
      "Use export_slide to export to HTML or PDF",
    ],
  });
}
