import type { SlideLayout } from "../../../themes/types.js";

export const twoColumnLayout: SlideLayout = {
  name: "two-column",
  description: "Two-column layout with a thin divider line",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    leftTitle: {
      type: "string",
      description: "Left column title",
      required: false,
      maxLength: 60,
    },
    leftList: {
      type: "array",
      description: "Left column list items",
      required: false,
      maxItems: 8,
    },
    rightTitle: {
      type: "string",
      description: "Right column title",
      required: false,
      maxLength: 60,
    },
    rightList: {
      type: "array",
      description: "Right column list items",
      required: false,
      maxItems: 8,
    },
  },
  template: (params) => {
    const renderCol = (title: unknown, items: unknown) => {
      let html = ``;
      if (title) {
        html += `<h3>${title}</h3>`;
      }
      if (Array.isArray(items) && items.length > 0) {
        html += `<ul>\n${items.map((item) => `<li>${item}</li>`).join("\n")}\n</ul>`;
      }
      return html;
    };

    const left = renderCol(params.leftTitle, params.leftList);
    const right = renderCol(params.rightTitle, params.rightList);

    return `## ${params.heading}\n\n<div class="min-2col">\n<div class="min-2col-left">\n${left}\n</div>\n<div class="min-2col-right">\n${right}\n</div>\n</div>`;
  },
};
