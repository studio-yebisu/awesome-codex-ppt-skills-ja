import type { SlideLayout } from "../../../themes/types.js";

export const twoColumnLayout: SlideLayout = {
  name: "two-column",
  description: "Two-column comparison layout with navy-accented panels",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    leftTitle: {
      type: "string",
      description: "Left panel title",
      required: false,
      maxLength: 60,
    },
    leftList: {
      type: "array",
      description: "Left panel list items",
      required: false,
      maxItems: 8,
    },
    rightTitle: {
      type: "string",
      description: "Right panel title",
      required: false,
      maxLength: 60,
    },
    rightList: {
      type: "array",
      description: "Right panel list items",
      required: false,
      maxItems: 8,
    },
  },
  template: (params) => {
    const renderPanel = (title: unknown, items: unknown) => {
      let html = `<div class="corp-2col-panel">`;
      if (title) {
        html += `\n<h3>${title}</h3>`;
      }
      if (Array.isArray(items) && items.length > 0) {
        html += `\n<ul>\n${items.map((item) => `<li>${item}</li>`).join("\n")}\n</ul>`;
      }
      html += `\n</div>`;
      return html;
    };

    const left = renderPanel(params.leftTitle, params.leftList);
    const right = renderPanel(params.rightTitle, params.rightList);

    return `## ${params.heading}\n\n<div class="corp-2col">\n${left}\n${right}\n</div>`;
  },
};
