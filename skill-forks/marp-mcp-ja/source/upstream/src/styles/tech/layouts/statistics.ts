import type { SlideLayout } from "../../../themes/types.js";

export const statisticsLayout: SlideLayout = {
  name: "statistics",
  description:
    "Large gradient metric numbers with optional trend indicators. Use 'Value|Label|Trend' format (trend is optional).",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    stats: {
      type: "array",
      description:
        "Stats in 'Value|Label|Trend' format. Trend is optional (e.g. '↑ 12%'). Max 4 stats.",
      required: true,
      maxItems: 4,
    },
    caption: {
      type: "string",
      description: "Optional footnote below the stats grid",
      required: false,
      maxLength: 150,
    },
  },
  template: (params) => {
    const stats = (params.stats as string[])
      .map((s) => {
        const parts = s.split("|");
        const value = parts[0]?.trim() ?? "";
        const label = parts[1]?.trim() ?? "";
        const trend = parts[2]?.trim() ?? "";
        return (
          `<div class="tech-stat">` +
          `<span class="tech-stat-value">${value}</span>` +
          `<span class="tech-stat-label">${label}</span>` +
          (trend ? `<span class="tech-stat-trend">${trend}</span>` : "") +
          `</div>`
        );
      })
      .join("\n");

    const caption = params.caption
      ? `\n<p class="tech-stats-caption">${params.caption}</p>`
      : "";

    return `## ${params.heading}\n\n<div class="tech-stats-grid">\n${stats}\n</div>${caption}`;
  },
};
