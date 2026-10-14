import type { SlideLayout } from "../../../themes/types.js";

export const threeColumnLayout: SlideLayout = {
  name: "three-column",
  description: "Three-column layout with sky-accented panels",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    col1Title: {
      type: "string",
      description: "First column title",
      required: false,
      maxLength: 60,
    },
    col1List: {
      type: "array",
      description: "First column list items",
      required: false,
      maxItems: 6,
    },
    col2Title: {
      type: "string",
      description: "Second column title",
      required: false,
      maxLength: 60,
    },
    col2List: {
      type: "array",
      description: "Second column list items",
      required: false,
      maxItems: 6,
    },
    col3Title: {
      type: "string",
      description: "Third column title",
      required: false,
      maxLength: 60,
    },
    col3List: {
      type: "array",
      description: "Third column list items",
      required: false,
      maxItems: 6,
    },
  },
  template: (params) => {
    const renderPanel = (title: unknown, items: unknown) => {
      let html = `<div class="corp-3col-panel">`;
      if (title) {
        html += `\n<h3>${title}</h3>`;
      }
      if (Array.isArray(items) && items.length > 0) {
        html += `\n<ul>\n${items.map((item) => `<li>${item}</li>`).join("\n")}\n</ul>`;
      }
      html += `\n</div>`;
      return html;
    };

    const col1 = renderPanel(params.col1Title, params.col1List);
    const col2 = renderPanel(params.col2Title, params.col2List);
    const col3 = renderPanel(params.col3Title, params.col3List);

    return `## ${params.heading}\n\n<div class="corp-3col">\n${col1}\n${col2}\n${col3}\n</div>`;
  },
};
