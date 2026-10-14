import type { SlideLayout } from "../../../themes/types.js";

export const bentoGridLayout: SlideLayout = {
  name: "bento-grid",
  description: "Bento Box modular grid for mixed content (use 'Size|Title|Content' format, Size: small/medium/large)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    cells: {
      type: "array",
      description: "Grid cells in 'Size|Title|Content' format (Size: small, medium, large)",
      required: true,
      maxItems: 6,
    },
  },
  template: (params) => {
    const cells = params.cells as string[];
    const cellItems = cells
      .map((cell) => {
        const parts = cell.split("|");
        const size = (parts[0]?.trim() || "small").toLowerCase();
        const title = parts[1]?.trim() || "";
        const content = parts[2]?.trim() || "";
        const sizeClass = size === "large" ? "bento-lg" : size === "medium" ? "bento-md" : "bento-sm";
        let inner = "";
        if (title) inner += `<h4>${title}</h4>`;
        if (content) inner += `\n<p>${content}</p>`;
        return `<div class="bento-cell ${sizeClass}">\n${inner}\n</div>`;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="bento-grid">\n${cellItems}\n</div>`;
  },
};
