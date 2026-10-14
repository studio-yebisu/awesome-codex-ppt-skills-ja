import type { SlideLayout } from "../../../themes/types.js";

export const comparisonLayout: SlideLayout = {
  name: "comparison",
  description:
    "Side-by-side comparison with explicit left/right titles and list items, separated by a thin divider",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    leftTitle: {
      type: "string",
      description: "Left panel title (e.g., 'Before', 'Option A', 'Pros')",
      required: true,
      maxLength: 50,
    },
    leftList: {
      type: "array",
      description: "Left panel list items. Max 6 items.",
      required: true,
      maxItems: 6,
    },
    rightTitle: {
      type: "string",
      description: "Right panel title (e.g., 'After', 'Option B', 'Cons')",
      required: true,
      maxLength: 50,
    },
    rightList: {
      type: "array",
      description: "Right panel list items. Max 6 items.",
      required: true,
      maxItems: 6,
    },
  },
  template: (params) => {
    const renderPanel = (title: unknown, items: unknown) => {
      let html = `<div class="min-compare-panel">`;
      html += `\n<h3 class="min-compare-title">${title}</h3>`;
      if (Array.isArray(items) && items.length > 0) {
        html += `\n<ul>\n${(items as string[]).map((item) => `<li>${item}</li>`).join("\n")}\n</ul>`;
      }
      html += `\n</div>`;
      return html;
    };

    const left = renderPanel(params.leftTitle, params.leftList);
    const right = renderPanel(params.rightTitle, params.rightList);

    return `## ${params.heading}\n\n<div class="min-compare">\n${left}\n${right}\n</div>`;
  },
};
