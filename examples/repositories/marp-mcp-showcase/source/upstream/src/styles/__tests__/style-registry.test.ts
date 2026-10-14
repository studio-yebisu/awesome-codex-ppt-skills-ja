import { describe, it, expect, beforeEach } from "@jest/globals";
import {
  getActiveStyle,
  setActiveStyle,
  getStyle,
  getAvailableStyleNames,
} from "../index.js";
import { setActiveTheme } from "../../themes/index.js";
import { getLayout, getLayoutNames } from "../../tools/list_layouts.js";

describe("Style Registry", () => {
  beforeEach(() => {
    setActiveStyle("default");
    setActiveTheme("default");
  });

  it("defaults to the 'default' style", () => {
    const style = getActiveStyle();
    expect(style.name).toBe("default");
    expect(style.css).toBe("");
    expect(Object.keys(style.layouts)).toHaveLength(0);
  });

  it("can set active style to 'rich'", () => {
    setActiveStyle("rich");
    const style = getActiveStyle();
    expect(style.name).toBe("rich");
    expect(style.css).not.toBe("");
    expect(Object.keys(style.layouts).length).toBeGreaterThan(0);
  });

  it("getStyle returns the correct style", () => {
    const rich = getStyle("rich");
    expect(rich).toBeDefined();
    expect(rich!.name).toBe("rich");

    const def = getStyle("default");
    expect(def).toBeDefined();
    expect(def!.name).toBe("default");
  });

  it("getStyle returns undefined for unknown styles", () => {
    const unknown = getStyle("nonexistent");
    expect(unknown).toBeUndefined();
  });

  it("getAvailableStyleNames returns all style names", () => {
    const names = getAvailableStyleNames();
    expect(names).toContain("default");
    expect(names).toContain("rich");
    expect(names).toContain("minimal");
    expect(names).toContain("dark");
    expect(names).toContain("corporate");
  });
});

describe("Layout Merge", () => {
  beforeEach(() => {
    setActiveStyle("default");
    setActiveTheme("default");
  });

  it("returns only theme layouts when default style is active", () => {
    const names = getLayoutNames();
    expect(names).toContain("title");
    expect(names).toContain("section");
    expect(names).not.toContain("title-hero");
    expect(names).not.toContain("card-grid");
  });

  it("returns merged layouts when rich style is active", () => {
    setActiveStyle("rich");
    const names = getLayoutNames();
    // Rich style overrides theme layouts
    expect(names).toContain("title");
    expect(names).toContain("section");
    // Rich style specific layouts
    expect(names).toContain("list");
    expect(names).toContain("table");
    expect(names).toContain("image-right");
    expect(names).toContain("image-center");
    expect(names).toContain("image-split");
    expect(names).toContain("timeline");
    expect(names).toContain("card-grid");
    expect(names).toContain("statistics");
    expect(names).toContain("highlight-box");
    expect(names).toContain("two-column-panel");
    expect(names).toContain("three-column-panel");
    expect(names).toContain("image-comparison");
    expect(names).toContain("content");
    expect(names).toContain("quote");
    // Old names should NOT be present
    expect(names).not.toContain("title-hero");
    expect(names).not.toContain("section-divider");
  });

  it("getLayout finds rich style layouts when active", () => {
    setActiveStyle("rich");
    const layout = getLayout("card-grid");
    expect(layout).not.toBeNull();
    expect(layout!.name).toBe("card-grid");
  });

  it("getLayout returns null for unknown layout", () => {
    setActiveStyle("rich");
    const layout = getLayout("nonexistent-layout");
    expect(layout).toBeNull();
  });
});
