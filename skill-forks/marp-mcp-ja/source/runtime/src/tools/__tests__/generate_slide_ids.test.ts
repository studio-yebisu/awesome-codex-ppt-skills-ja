import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { promises as fs } from "fs";
import os from "os";
import path from "path";
import { generateSlideIds } from "../generate_slide_ids.js";

const SLIDE_SEPARATOR = /\n---\n+/;

describe("generateSlideIds", () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "marp-init-"));
  });

  afterEach(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  it("adds slide IDs without altering frontmatter", async () => {
    const filePath = path.join(tempDir, "slides.md");
    const originalFrontmatter = [
      "---",
      "custom: keep-me",
      "paginate: false",
      "---",
      "",
    ].join("\n");
    await fs.writeFile(
      filePath,
      [
        originalFrontmatter,
        "# Slide 1",
        "",
        "---",
        "",
        "# Slide 2",
      ].join("\n"),
      "utf-8",
    );

    await generateSlideIds({ filePath });

    const content = await fs.readFile(filePath, "utf-8");
    expect(content.startsWith(originalFrontmatter)).toBe(true);

    const body = content.slice(originalFrontmatter.length).trim();
    const slides = body.split(SLIDE_SEPARATOR);
    expect(slides).toHaveLength(2);
    for (const slide of slides) {
      expect(slide).toMatch(/<!--\s*slide-id:/i);
    }
  });

  it("does not inject frontmatter when missing", async () => {
    const filePath = path.join(tempDir, "plain.md");
    await fs.writeFile(
      filePath,
      ["# Slide 1", "", "---", "", "# Slide 2"].join("\n"),
      "utf-8",
    );

    await generateSlideIds({ filePath });

    const content = await fs.readFile(filePath, "utf-8");
    expect(content.startsWith("---\nmarp: true")).toBe(false);

    const slides = content.trim().split(SLIDE_SEPARATOR);
    expect(slides).toHaveLength(2);
    for (const slide of slides) {
      expect(slide).toMatch(/<!--\s*slide-id:/i);
    }
  });

  it("does not modify files already initialized", async () => {
    const filePath = path.join(tempDir, "prepped.md");
    const prepared = [
      "---",
      "marp: true",
      "theme: default",
      "---",
      "",
      "<!-- slide-id: abc -->",
      "",
      "# Slide",
    ].join("\n");
    await fs.writeFile(filePath, prepared, "utf-8");

    await generateSlideIds({ filePath });
    const afterFirst = await fs.readFile(filePath, "utf-8");

    await generateSlideIds({ filePath });
    const afterSecond = await fs.readFile(filePath, "utf-8");

    expect(afterFirst).toBe(prepared);
    expect(afterSecond).toBe(prepared);
  });
});
