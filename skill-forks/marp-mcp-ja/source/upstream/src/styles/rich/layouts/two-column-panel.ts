import type { SlideLayout } from "../../../themes/types.js";

export const twoColumnPanelLayout: SlideLayout = {
  name: "two-column-panel",
  description: "Two-column layout with styled panels, optional accent highlight on one panel",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    panel1Title: {
      type: "string",
      description: "Left panel title",
      required: false,
      maxLength: 60,
    },
    panel1List: {
      type: "array",
      description: "Left panel list items",
      required: false,
      maxItems: 8,
    },
    panel2Title: {
      type: "string",
      description: "Right panel title",
      required: false,
      maxLength: 60,
    },
    panel2List: {
      type: "array",
      description: "Right panel list items",
      required: false,
      maxItems: 8,
    },
    accentPanel: {
      type: "string",
      description: "Which panel gets accent styling: 'left', 'right', or 'none' (default: 'none')",
      required: false,
    },
  },
  template: (params) => {
    const accent = (params.accentPanel as string) || "none";
    const panel1Class = accent === "left" ? "panel panel-accent" : "panel";
    const panel2Class = accent === "right" ? "panel panel-accent" : "panel";

    const renderPanel = (title: unknown, items: unknown, className: string) => {
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

    const panel1 = renderPanel(params.panel1Title, params.panel1List, panel1Class);
    const panel2 = renderPanel(params.panel2Title, params.panel2List, panel2Class);

    return `## ${params.heading}\n\n<div class="grid-2col">\n${panel1}\n${panel2}\n</div>`;
  },
};
