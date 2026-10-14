import type { SlideLayout } from "../../../themes/types.js";

export const twoColumnLayout: SlideLayout = {
  name: "two-column",
  description: "Two-panel layout with violet top borders, ideal for comparing options or features",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    leftTitle: {
      type: "string",
      description: "Left panel title (e.g. 'Option A', 'Before')",
      required: false,
      maxLength: 60,
    },
    leftList: {
      type: "array",
      description: "Left panel list items (max 6 items)",
      required: false,
      maxItems: 6,
    },
    rightTitle: {
      type: "string",
      description: "Right panel title (e.g. 'Option B', 'After')",
      required: false,
      maxLength: 60,
    },
    rightList: {
      type: "array",
      description: "Right panel list items (max 6 items)",
      required: false,
      maxItems: 6,
    },
  },
  template: (params) => {
    const renderPanel = (title: unknown, items: unknown) => {
      let html = `<div class="tech-2col-panel">`;
      if (title) {
        html += `\n<p class="tech-2col-panel-title">${title}</p>`;
      }
      if (Array.isArray(items) && items.length > 0) {
        html += `\n<ul>\n${(items as string[]).map((i) => `<li>${i}</li>`).join("\n")}\n</ul>`;
      }
      html += `\n</div>`;
      return html;
    };

    const left = renderPanel(params.leftTitle, params.leftList);
    const right = renderPanel(params.rightTitle, params.rightList);
    return `## ${params.heading}\n\n<div class="tech-2col">\n${left}\n${right}\n</div>`;
  },
};
