/**
 * Slide ID utilities
 * Manages unique IDs for Marp slides using UUID v4
 */

import { randomUUID } from 'crypto';

const SLIDE_ID_REGEX = /<!--\s*slide-id:\s*([a-f0-9-]+)\s*-->/i;

/**
 * Generates a new unique slide ID using UUID v4
 */
export function generateSlideId(): string {
  return randomUUID();
}

/**
 * Extracts slide ID from slide content by searching for the slide-id HTML comment.
 *
 * @param slideContent - The slide content to search
 * @returns The slide ID if found, null otherwise
 */
export function extractSlideId(slideContent: string): string | null {
  const match = slideContent.match(SLIDE_ID_REGEX);
  return match ? match[1] : null;
}

/**
 * Ensures a slide has a unique ID by adding one if it doesn't exist.
 *
 * @param slideContent - The slide content to process
 * @returns Object containing the updated content and the slide ID
 */
export function ensureSlideId(slideContent: string): { content: string; id: string } {
  const existingId = extractSlideId(slideContent);

  if (existingId) {
    return { content: slideContent, id: existingId };
  }

  const newId = generateSlideId();
  const trimmedContent = slideContent.trim();
  const contentWithId = `<!-- slide-id: ${newId} -->\n\n${trimmedContent}`;

  return { content: contentWithId, id: newId };
}

/**
 * Ensures all slides in an array have unique IDs.
 *
 * @param slides - Array of slide content strings
 * @returns Object containing updated slides and a map of slide IDs to indices
 */
export function ensureAllSlideIds(slides: string[]): {
  slides: string[];
  idToIndex: Map<string, number>;
} {
  const updatedSlides: string[] = [];
  const idToIndex = new Map<string, number>();

  slides.forEach((slide, index) => {
    const { content, id } = ensureSlideId(slide);
    updatedSlides.push(content);
    idToIndex.set(id, index);
  });

  return { slides: updatedSlides, idToIndex };
}

/**
 * Finds the index of a slide by its ID.
 *
 * @param slides - Array of slide content strings
 * @param slideId - The slide ID to search for
 * @returns The index of the slide, or -1 if not found
 */
export function findSlideIndexById(slides: string[], slideId: string): number {
  return slides.findIndex(slide => {
    const id = extractSlideId(slide);
    return id === slideId;
  });
}
