import { describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { promises as fs } from "fs";
import os from "os";
import path from "path";
import { readSlide } from "../read_slide.js";
import { setActiveTheme } from "../../themes/index.js";

const FRONTMATTER = ["---", "marp: true", "theme: default", "---", ""].join("\n");

describe("readSlide", () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "marp-read-slide-"));
    setActiveTheme("default");
  });

  afterEach(async () => {
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  it("returns all slides when no slideId is provided", async () => {
    const filePath = path.join(tempDir, "all.md");
    const content = [
      FRONTMATTER,
      "<!-- slide-id: aaa-111 -->",
      "",
      "# Slide 1",
      "",
      "---",
      "",
      "<!-- slide-id: bbb-222 -->",
      "",
      "# Slide 2",
    ].join("\n");
    await fs.writeFile(filePath, content, "utf-8");

    const result = await readSlide({ filePath });
    const data = JSON.parse(result.content[0].text);

    expect(data.success).toBe(true);
    expect(data.totalSlides).toBe(2);
    expect(data.slides).toHaveLength(2);
    expect(data.slides[0].slideId).toBe("aaa-111");
    expect(data.slides[0].position).toBe(1);
    expect(data.slides[1].slideId).toBe("bbb-222");
    expect(data.slides[1].position).toBe(2);
  });

  it("returns a specific slide by ID", async () => {
    const filePath = path.join(tempDir, "specific.md");
    const content = [
      FRONTMATTER,
      "<!-- slide-id: aaa-111 -->",
      "",
      "# Slide 1",
      "",
      "---",
      "",
      "<!-- slide-id: bbb-222 -->",
      "",
      "# Slide 2",
    ].join("\n");
    await fs.writeFile(filePath, content, "utf-8");

    const result = await readSlide({ filePath, slideId: "bbb-222" });
    const data = JSON.parse(result.content[0].text);

    expect(data.success).toBe(true);
    expect(data.slideId).toBe("bbb-222");
    expect(data.position).toBe(2);
    expect(data.content).toContain("# Slide 2");
  });

  it("returns error for non-existent slide ID", async () => {
    const filePath = path.join(tempDir, "missing.md");
    const content = [
      FRONTMATTER,
      "<!-- slide-id: aaa-111 -->",
      "",
      "# Slide 1",
    ].join("\n");
    await fs.writeFile(filePath, content, "utf-8");

    const result = await readSlide({ filePath, slideId: "non-existent" });
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("not found");
  });

  it("returns error for invalid file path", async () => {
    const result = await readSlide({ filePath: "relative/path.md" });
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("absolute");
  });

  it("returns error for non-existent file", async () => {
    const filePath = path.join(tempDir, "nonexistent.md");
    const result = await readSlide({ filePath });
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("Could not read file");
  });
});
