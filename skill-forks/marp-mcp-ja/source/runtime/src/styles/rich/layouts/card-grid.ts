import type { SlideLayout } from "../../../themes/types.js";

export const cardGridLayout: SlideLayout = {
  name: "card-grid",
  description: "Grid of cards with icon, title, and description (use 'Icon|Title|Description' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    cards: {
      type: "array",
      description: "Cards in 'Icon|Title|Description' format",
      required: true,
      maxItems: 5,
    },
  },
  template: (params) => {
    const cards = params.cards as string[];
    const cardItems = cards
      .map((card) => {
        const parts = card.split("|");
        if (parts.length >= 3) {
          const icon = parts[0].trim();
          const title = parts[1].trim();
          const desc = parts[2].trim();
          return `<div class="card">\n<div class="card-icon">${icon}</div>\n<h4>${title}</h4>\n<p>${desc}</p>\n</div>`;
        }
        if (parts.length === 2) {
          const title = parts[0].trim();
          const desc = parts[1].trim();
          return `<div class="card">\n<h4>${title}</h4>\n<p>${desc}</p>\n</div>`;
        }
        return `<div class="card">\n<h4>${card}</h4>\n</div>`;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="card-grid">\n${cardItems}\n</div>`;
  },
};
