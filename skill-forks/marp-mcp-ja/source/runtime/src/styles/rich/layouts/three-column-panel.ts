import type { SlideLayout } from "../../../themes/types.js";

export const threeColumnPanelLayout: SlideLayout = {
  name: "three-column-panel",
  description: "Three-column layout with styled panels (use 'Title|Content' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    panels: {
      type: "array",
      description: "Panels in 'Title|Content' format (provide exactly 3)",
      required: true,
      maxItems: 3,
    },
  },
  template: (params) => {
    const panels = params.panels as string[];
    const panelItems = panels
      .map((panel) => {
        const parts = panel.split("|");
        if (parts.length >= 2) {
          const title = parts[0].trim();
          const content = parts.slice(1).join("|").trim();
          return `<div class="panel">\n<h3>${title}</h3>\n<p>${content}</p>\n</div>`;
        }
        return `<div class="panel">\n<p>${panel}</p>\n</div>`;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="grid-3col">\n${panelItems}\n</div>`;
  },
};
