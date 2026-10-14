import type { SlideLayout } from "../../../themes/types.js";

export const listLayout: SlideLayout = {
  name: "list",
  description: "Bullet list slide with violet arrow markers and thin dividers between items",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    list: {
      type: "array",
      description: "List items (max 8 items, each max 120 chars)",
      required: true,
      maxItems: 8,
      maxLength: 120,
    },
  },
  template: (params) => {
    const items = (params.list as string[])
      .map((item) => `<li>${item}</li>`)
      .join("\n");
    return `## ${params.heading}\n\n<ul class="tech-list">\n${items}\n</ul>`;
  },
};
