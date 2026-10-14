/**
 * Shared utilities for parsing and reconstructing Marp markdown files.
 */

/**
 * Parses frontmatter from content, separating it from the body.
 * If no valid frontmatter exists, the entire file is treated as body content.
 */
export function parseFrontmatter(content: string): { frontmatter: string; body: string } {
  const lines = content.split("\n");

  if (lines.length === 0) {
    return { frontmatter: "", body: "" };
  }

  if (lines[0].trim() !== "---") {
    return { frontmatter: "", body: content };
  }

  const endIndex = lines.slice(1).findIndex(line => line.trim() === "---");
  if (endIndex === -1) {
    return { frontmatter: "", body: content };
  }

  const frontmatterLines = lines.slice(0, endIndex + 2);
  const bodyLines = lines.slice(endIndex + 2);

  return {
    frontmatter: frontmatterLines.join("\n"),
    body: bodyLines.join("\n"),
  };
}

/**
 * Splits the body content into individual slides.
 * Handles trailing spaces/tabs after the `---` separator.
 */
export function splitSlides(body: string): string[] {
  const trimmed = body.trim();
  return trimmed ? trimmed.split(/\n---[ \t]*\n/) : [];
}

/**
 * Joins frontmatter and slides back into a single markdown string.
 */
export function joinSlides(frontmatter: string, slides: string[]): string {
  if (slides.length === 0) {
    return frontmatter.trim() ? frontmatter : "";
  }

  const processedSlides = slides
    .map(s => s.trim())
    .filter(s => s !== "");

  if (processedSlides.length === 0) {
    return frontmatter.trim() ? frontmatter : "";
  }

  const slidesContent = processedSlides.join("\n\n---\n\n");

  if (!frontmatter.trim()) {
    return slidesContent;
  }

  const cleanedFrontmatter = frontmatter.replace(/\s+$/, "");
  return `${cleanedFrontmatter}\n\n${slidesContent}`;
}
