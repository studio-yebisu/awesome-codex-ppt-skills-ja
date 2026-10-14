import type { SlideLayout } from "../../../themes/types.js";

export const featureGridLayout: SlideLayout = {
  name: "feature-grid",
  description:
    "Grid of feature cards, each with an icon, title, and description. Use 'Icon|Title|Description' format.",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    features: {
      type: "array",
      description:
        "Feature cards in 'Icon|Title|Description' format. Icon can be an emoji or short text. Max 5 items.",
      required: true,
      maxItems: 5,
    },
  },
  template: (params) => {
    const cards = (params.features as string[])
      .map((f) => {
        const parts = f.split("|");
        const icon = parts[0]?.trim() ?? "";
        const name = parts[1]?.trim() ?? "";
        const desc = parts[2]?.trim() ?? "";
        return (
          `<div class="tech-feature-card">\n` +
          `<span class="tech-feature-icon">${icon}</span>\n` +
          `<p class="tech-feature-name">${name}</p>\n` +
          `<p class="tech-feature-desc">${desc}</p>\n` +
          `</div>`
        );
      })
      .join("\n");

    return `## ${params.heading}\n\n<div class="tech-feature-grid">\n${cards}\n</div>`;
  },
};
