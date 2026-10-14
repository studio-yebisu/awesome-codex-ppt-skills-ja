import { describe, expect, it, afterAll } from "@jest/globals";
import { promises as fs } from "fs";
import path from "path";
import {
  getAvailableThemeNames,
  getTheme,
  setActiveTheme,
} from "../index.js";
import type { SlideLayout, ThemeDefinition, ThemeName } from "../types.js";

const examplesDir = path.resolve(process.cwd(), "assets/examples");
const examplesMarkdownDir = path.resolve(examplesDir, "md");

type SampleParamsBuilder = (themeName: ThemeName) => Record<string, unknown>;

const SAMPLE_IMAGE = "https://picsum.photos/1280/720";

const sampleParams: Record<string, SampleParamsBuilder> = {
  title: () => ({
    heading: "Sample Presentation",
    content: "Author Name · Example Org",
  }),
  section: () => ({
    title: "Section Header",
    subtitle: "Supporting message",
  }),
  list: () => ({
    heading: "Key Points",
    list: ["Background context", "Insights discovered", "Next steps"],
    citations: "Source: Sample Dataset",
  }),
  table: () => ({
    heading: "Data Overview",
    tableMarkdown: [
      "| Item | Value |",
      "| ---- | ----- |",
      "| Alpha | 42 |",
      "| Beta | 37 |",
      "| Gamma | 58 |",
      "| Delta | 21 |",
      "| Epsilon | 73 |",
    ].join("\n"),
    description: "Higher is better.",
    citations: "Source: Sample Stats",
  }),
  "two-column": () => ({
    heading: "Strategy Comparison",
    column1Heading: "Option A",
    column1List: ["Predictable", "Lower risk", "Gradual growth"],
    column2Heading: "Option B",
    column2List: ["Experimental", "Higher upside", "Needs research"],
    citations: "Source: Sample Playbook",
  }),
  "image-right": () => ({
    heading: "Architecture Diagram",
    list: ["Ingest", "Process", "Serve"],
    imagePath: SAMPLE_IMAGE,
    citations: "Diagram credit: picsum.photos",
  }),
  "image-center": () => ({
    heading: "Workflow Snapshot",
    imagePath: SAMPLE_IMAGE,
    description: "Step-by-step overview.",
    citations: "Figure 1",
  }),
  content: () => ({
    heading: "Summary",
    body: "This is a **free-form** markdown slide.\n\n- Key point one\n- Key point two\n- Key point three",
    citations: "Source: Sample Report",
  }),
};

describe("theme example generator", () => {
  afterAll(() => {
    setActiveTheme("default");
  });

  it("writes markdown examples for every theme", async () => {
    await fs.mkdir(examplesMarkdownDir, { recursive: true });
    const themeNames = getAvailableThemeNames();

    for (const themeName of themeNames) {
      const markdown = buildExampleMarkdown(themeName);
      const filePath = path.join(
        examplesMarkdownDir,
        `example-${themeName}-theme.md`,
      );
      await fs.writeFile(filePath, markdown, "utf-8");
      const savedMarkdown = await fs.readFile(filePath, "utf-8");
      expect(savedMarkdown).toBe(markdown);
    }
  }, 30000);
});

function buildExampleMarkdown(themeName: ThemeName): string {
  setActiveTheme(themeName);
  const theme = getTheme(themeName);

  if (!theme) {
    throw new Error(`Theme "${themeName}" not found`);
  }

  const slides = Object.entries(theme.layouts).map(([layoutName, layout]) =>
    buildSlideMarkup(theme, layoutName, layout, themeName),
  );

  return [
    "---",
    "marp: true",
    `theme: ${themeName}`,
    `header: ${buildHeaderDirective(themeName)}`,
    `paginate: true`,
    "---",
    "",
    slides.join("\n\n---\n\n"),
    "",
  ].join("\n");
}

function buildSlideMarkup(
  theme: ThemeDefinition,
  layoutName: string,
  layout: SlideLayout,
  themeName: ThemeName,
): string {
  const paramsFactory = sampleParams[layoutName];

  if (!paramsFactory) {
    throw new Error(
      `Missing sample params for layout "${layoutName}" in theme "${theme.name}"`,
    );
  }

  const content = layout.template(paramsFactory(themeName));
  return `<!-- layout: ${layoutName} -->\n${content.trim()}`;
}

function buildHeaderDirective(themeName: ThemeName): string {
  return `Example Labs | ${themeName} walkthrough`;
}
