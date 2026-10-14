import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { promises as fs } from "fs";
import os from "os";
import path from "path";
import { createPresentation } from "../create_presentation.js";
import { setActiveTheme } from "../../themes/index.js";
import { setActiveStyle } from "../../styles/index.js";

describe("createPresentation", () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "marp-create-"));
    setActiveTheme("default");
    setActiveStyle("default");
  });

  afterEach(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  it("creates a new file with frontmatter and title slide", async () => {
    const filePath = path.join(tempDir, "test.md");

    const result = await createPresentation({
      filePath,
      title: "My Test Presentation",
    });

    expect(result.isError).toBeFalsy();
    const data = JSON.parse(result.content[0].text);
    expect(data.totalSlides).toBe(1);
    expect(data.filePath).toBe(filePath);

    const content = await fs.readFile(filePath, "utf-8");
    expect(content).toContain("marp: true");
    expect(content).toContain("My Test Presentation");
    expect(content).toContain("slide-id:");
  });

  it("creates placeholder slides when slideCount is specified", async () => {
    const filePath = path.join(tempDir, "slides.md");

    const result = await createPresentation({
      filePath,
      title: "Presentation With Slides",
      slideCount: 3,
    });

    expect(result.isError).toBeFalsy();
    const data = JSON.parse(result.content[0].text);
    expect(data.totalSlides).toBe(4); // 1 title + 3 content

    const content = await fs.readFile(filePath, "utf-8");
    // Should have 4 slide separators (one per slide after the first)
    const slideIds = content.match(/slide-id:/g);
    expect(slideIds?.length).toBe(4);
  });

  it("includes subtitle on title slide when provided", async () => {
    const filePath = path.join(tempDir, "with-subtitle.md");

    await createPresentation({
      filePath,
      title: "My Talk",
      subtitle: "Author · Conference 2025",
    });

    const content = await fs.readFile(filePath, "utf-8");
    expect(content).toContain("Author · Conference 2025");
  });

  it("includes paginate in frontmatter", async () => {
    const filePath = path.join(tempDir, "paginated.md");

    await createPresentation({
      filePath,
      title: "Paginated Talk",
      paginate: true,
    });

    const content = await fs.readFile(filePath, "utf-8");
    expect(content).toContain("paginate: true");
  });

  it("returns error when file already exists", async () => {
    const filePath = path.join(tempDir, "existing.md");
    await fs.writeFile(filePath, "# existing", "utf-8");

    const result = await createPresentation({ filePath, title: "New" });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("already exists");
  });

  it("returns error for invalid file path", async () => {
    const result = await createPresentation({
      filePath: "relative/path.md",
      title: "Test",
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("absolute");
  });
});
