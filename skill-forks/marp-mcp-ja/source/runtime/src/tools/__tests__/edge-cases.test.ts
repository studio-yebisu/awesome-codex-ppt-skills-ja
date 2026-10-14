import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { promises as fs } from "fs";
import os from "os";
import path from "path";
import { manageSlide } from "../manage_slide.js";
import { setFrontmatter } from "../set_frontmatter.js";
import { generateSlideIds } from "../generate_slide_ids.js";
import { setActiveTheme } from "../../themes/index.js";

describe("Edge Cases", () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "marp-edge-cases-"));
    setActiveTheme("default");
  });

  afterEach(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  describe("Empty files", () => {
    it("should handle empty file in setFrontmatter", async () => {
      const filePath = path.join(tempDir, "empty.md");
      await fs.writeFile(filePath, "", "utf-8");

      const result = await setFrontmatter({ filePath });
      const response = JSON.parse(result.content[0].text);

      expect(response.success).toBe(true);
      expect(response.frontmatter.marp).toBe(true);
    });

    it("should handle empty file in generateSlideIds", async () => {
      const filePath = path.join(tempDir, "empty.md");
      await fs.writeFile(filePath, "", "utf-8");

      const result = await generateSlideIds({ filePath });
      const response = JSON.parse(result.content[0].text);

      expect(response.success).toBe(true);
    });
  });

  describe("File path validation", () => {
    it("should reject relative paths in manageSlide", async () => {
      const result = await manageSlide({
        filePath: "relative/path.md",
        layoutType: "title",
        params: { heading: "Test" },
      });

      expect(result.content[0].text).toContain("File path must be absolute");
    });

    it("should reject non-markdown files in manageSlide", async () => {
      const result = await manageSlide({
        filePath: "/absolute/path/file.txt",
        layoutType: "title",
        params: { heading: "Test" },
      });

      expect(result.content[0].text).toContain("must have one of these extensions");
    });

    it("should reject relative paths in setFrontmatter", async () => {
      const result = await setFrontmatter({
        filePath: "relative/path.md",
      });

      expect(result.content[0].text).toContain("File path must be absolute");
    });

    it("should reject relative paths in generateSlideIds", async () => {
      const result = await generateSlideIds({
        filePath: "relative/path.md",
      });

      expect(result.content[0].text).toContain("File path must be absolute");
    });
  });

  describe("Invalid frontmatter", () => {
    it("should handle malformed frontmatter in setFrontmatter", async () => {
      const filePath = path.join(tempDir, "malformed.md");
      const content = `---
marp: true
theme: default
this is not valid yaml: [unclosed
---

# Slide`;
      await fs.writeFile(filePath, content, "utf-8");

      const result = await setFrontmatter({ filePath });
      // gray-matter will throw an error for invalid YAML
      expect(result.content[0].text).toContain("Error");
    });

    it("should handle missing closing delimiter in frontmatter", async () => {
      const filePath = path.join(tempDir, "no-close.md");
      const content = `---
marp: true
theme: default

# This is actually content`;
      await fs.writeFile(filePath, content, "utf-8");

      const result = await setFrontmatter({ filePath });
      // Should treat entire file as body when no closing delimiter
      expect(result.content[0].text).toBeTruthy();
    });
  });

  describe("Large files", () => {
    it("should reject files exceeding size limit in manageSlide", async () => {
      const filePath = path.join(tempDir, "large.md");
      // Create a file larger than 10MB
      const largeContent = "# Slide\n".repeat(2000000); // ~16MB
      await fs.writeFile(filePath, largeContent, "utf-8");

      const result = await manageSlide({
        filePath,
        layoutType: "title",
        params: { heading: "Test" },
      });

      expect(result.content[0].text).toContain("File too large");
    });

    it("should reject files exceeding size limit in setFrontmatter", async () => {
      const filePath = path.join(tempDir, "large.md");
      // Create a file larger than 10MB
      const largeContent = "# Slide\n".repeat(2000000); // ~16MB
      await fs.writeFile(filePath, largeContent, "utf-8");

      const result = await setFrontmatter({ filePath });

      expect(result.content[0].text).toContain("File too large");
    });

    it("should reject files exceeding size limit in generateSlideIds", async () => {
      const filePath = path.join(tempDir, "large.md");
      // Create a file larger than 10MB
      const largeContent = "# Slide\n".repeat(2000000); // ~16MB
      await fs.writeFile(filePath, largeContent, "utf-8");

      const result = await generateSlideIds({ filePath });

      expect(result.content[0].text).toContain("File too large");
    });
  });

  describe("Non-existent files", () => {
    it("should handle non-existent file in manageSlide", async () => {
      const result = await manageSlide({
        filePath: path.join(tempDir, "nonexistent.md"),
        layoutType: "title",
        params: { heading: "Test" },
      });

      expect(result.content[0].text).toContain("Could not read file");
    });

    it("should handle non-existent file in setFrontmatter", async () => {
      const result = await setFrontmatter({
        filePath: path.join(tempDir, "nonexistent.md"),
      });

      expect(result.content[0].text).toContain("Could not read file");
    });

    it("should handle non-existent file in generateSlideIds", async () => {
      const result = await generateSlideIds({
        filePath: path.join(tempDir, "nonexistent.md"),
      });

      expect(result.content[0].text).toContain("Could not read file");
    });
  });

  describe("Special characters in content", () => {
    it("should handle quotes in header with setFrontmatter", async () => {
      const filePath = path.join(tempDir, "quotes.md");
      await fs.writeFile(filePath, "# Test", "utf-8");

      const result = await setFrontmatter({
        filePath,
        header: 'Header with "quotes" and \'apostrophes\'',
      });

      const response = JSON.parse(result.content[0].text);
      expect(response.success).toBe(true);
      expect(response.frontmatter.header).toContain("quotes");
    });

    it("should handle special YAML characters in header", async () => {
      const filePath = path.join(tempDir, "special.md");
      await fs.writeFile(filePath, "# Test", "utf-8");

      const result = await setFrontmatter({
        filePath,
        header: "Header: with colons & ampersands",
      });

      const response = JSON.parse(result.content[0].text);
      expect(response.success).toBe(true);
    });
  });

  describe("Slide ID edge cases", () => {
    it("should handle slides with existing IDs in generateSlideIds", async () => {
      const filePath = path.join(tempDir, "existing-ids.md");
      const content = `---
marp: true
---

<!-- slide-id: abc123 -->

# Slide 1

---

# Slide 2 without ID`;
      await fs.writeFile(filePath, content, "utf-8");

      const result = await generateSlideIds({ filePath });
      const response = JSON.parse(result.content[0].text);

      expect(response.success).toBe(true);
      expect(response.totalSlides).toBe(2);
    });

    it("should handle delete of non-existent slide ID", async () => {
      const filePath = path.join(tempDir, "delete-missing.md");
      const content = `---
marp: true
---

<!-- slide-id: abc123 -->

# Slide 1`;
      await fs.writeFile(filePath, content, "utf-8");

      const result = await manageSlide({
        filePath,
        mode: "delete",
        slideId: "nonexistent-id",
      });

      expect(result.content[0].text).toContain("not found");
    });
  });
});
