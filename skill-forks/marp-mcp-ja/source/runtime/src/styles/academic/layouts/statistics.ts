import type { SlideLayout } from "../../../themes/types.js";

export const statisticsLayout: SlideLayout = {
  name: "statistics",
  description: "Academic statistics display with maroon numbers (use 'Number|Label' format)",
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
      maxItems: 4,
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
          return `<div>\n<div class="acad-stat-number" style="font-size: 2.2em">${number}</div>\n<div class="acad-stat-label" style="font-size: 0.8em">${label}</div>\n</div>`;
        }
        return `<div>\n<div class="acad-stat-number" style="font-size: 2.2em">${stat}</div>\n</div>`;
      })
      .join("\n");
    let slide = `## ${params.heading}\n\n<div class="acad-stat-box">\n${statItems}\n</div>`;
    if (params.caption) {
      slide += `\n\n<p style="text-align:center;color:#475569;font-size:0.85em;">${params.caption}</p>`;
    }
    return slide;
  },
};
