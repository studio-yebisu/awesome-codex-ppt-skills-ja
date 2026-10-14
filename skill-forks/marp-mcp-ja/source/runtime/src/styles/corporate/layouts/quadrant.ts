import type { SlideLayout } from "../../../themes/types.js";

export const quadrantLayout: SlideLayout = {
  name: "quadrant",
  description: "2x2 matrix for SWOT, risk analysis, or priority grids",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    topLeftTitle: {
      type: "string",
      description: "Top-left quadrant title",
      required: true,
      maxLength: 40,
    },
    topLeftItems: {
      type: "array",
      description: "Top-left quadrant items",
      required: false,
      maxItems: 5,
    },
    topRightTitle: {
      type: "string",
      description: "Top-right quadrant title",
      required: true,
      maxLength: 40,
    },
    topRightItems: {
      type: "array",
      description: "Top-right quadrant items",
      required: false,
      maxItems: 5,
    },
    bottomLeftTitle: {
      type: "string",
      description: "Bottom-left quadrant title",
      required: true,
      maxLength: 40,
    },
    bottomLeftItems: {
      type: "array",
      description: "Bottom-left quadrant items",
      required: false,
      maxItems: 5,
    },
    bottomRightTitle: {
      type: "string",
      description: "Bottom-right quadrant title",
      required: true,
      maxLength: 40,
    },
    bottomRightItems: {
      type: "array",
      description: "Bottom-right quadrant items",
      required: false,
      maxItems: 5,
    },
  },
  template: (params) => {
    const renderQuadrant = (title: unknown, items: unknown, className: string) => {
      let html = `<div class="${className}">\n<h4>${title}</h4>`;
      if (Array.isArray(items) && items.length > 0) {
        html += `\n<ul>\n${items.map((item) => `<li>${item}</li>`).join("\n")}\n</ul>`;
      }
      html += `\n</div>`;
      return html;
    };

    const tl = renderQuadrant(params.topLeftTitle, params.topLeftItems, "corp-quad corp-quad-tl");
    const tr = renderQuadrant(params.topRightTitle, params.topRightItems, "corp-quad corp-quad-tr");
    const bl = renderQuadrant(params.bottomLeftTitle, params.bottomLeftItems, "corp-quad corp-quad-bl");
    const br = renderQuadrant(params.bottomRightTitle, params.bottomRightItems, "corp-quad corp-quad-br");

    return `## ${params.heading}\n\n<div class="corp-quadrant">\n${tl}\n${tr}\n${bl}\n${br}\n</div>`;
  },
};
