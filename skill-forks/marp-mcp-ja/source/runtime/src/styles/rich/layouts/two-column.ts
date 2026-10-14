import type { SlideLayout } from "../../../themes/types.js";

export const twoColumnLayout: SlideLayout = {
  name: "two-column",
  description: "Simple two-column layout with headings and lists",
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
    const renderCol = (title: unknown, items: unknown, className: string) => {
      let html = `<div class="${className}">`;
      if (title) {
        html += `\n<h3>${title}</h3>`;
      }
      if (Array.isArray(items) && items.length > 0) {
        html += `\n<ul>\n${items.map((item) => `<li>${item}</li>`).join("\n")}\n</ul>`;
      }
      html += `\n</div>`;
      return html;
    };

    const left = renderCol(params.leftTitle, params.leftList, "rich-2col-left");
    const right = renderCol(params.rightTitle, params.rightList, "rich-2col-right");

    return `## ${params.heading}\n\n<div class="rich-2col">\n${left}\n${right}\n</div>`;
  },
};
