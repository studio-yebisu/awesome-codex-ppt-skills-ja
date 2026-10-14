import type { SlideLayout } from "../../../themes/types.js";

export const statisticsLayout: SlideLayout = {
  name: "statistics",
  description: "Minimal statistics display with black numbers and thin underline (use 'Number|Label' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    stats: {
      type: "array",
      description: "Statistics in 'Number|Label' format",
      required: true,
      maxItems: 5,
    },
    caption: {
      type: "string",
      description: "Optional caption below statistics",
      required: false,
      maxLength: 200,
    },
  },
  template: (params) => {
    const stats = params.stats as string[];
    const statItems = stats
      .map((stat) => {
        const parts = stat.split("|");
        if (parts.length >= 2) {
          const number = parts[0].trim();
          const label = parts[1].trim();
          return `<div>\n<div class="min-stat-number">${number}</div>\n<div class="min-stat-label">${label}</div>\n</div>`;
        }
        return `<div>\n<div class="min-stat-number">${stat}</div>\n</div>`;
      })
      .join("\n");
    let slide = `## ${params.heading}\n\n<div class="min-stat-box">\n${statItems}\n</div>`;
    if (params.caption) {
      slide += `\n\n<p style="text-align:center;color:#6b7280;font-size:0.9em;">${params.caption}</p>`;
    }
    return slide;
  },
};
