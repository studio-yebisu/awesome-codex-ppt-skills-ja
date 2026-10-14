import type { SlideLayout } from "../../../themes/types.js";

export const progressBarLayout: SlideLayout = {
  name: "progress-bar",
  description: "Horizontal progress bars for metrics visualization (use 'Label|Value|MaxValue' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    metrics: {
      type: "array",
      description: "Metrics in 'Label|Value|MaxValue' format (e.g. 'Sales|75|100')",
      required: true,
      maxItems: 6,
    },
    caption: {
      type: "string",
      description: "Optional caption below the bars",
      required: false,
      maxLength: 200,
    },
  },
  template: (params) => {
    const metrics = params.metrics as string[];
    const barItems = metrics
      .map((metric) => {
        const parts = metric.split("|");
        const label = parts[0]?.trim() || "";
        const value = Number(parts[1]?.trim()) || 0;
        const max = Number(parts[2]?.trim()) || 100;
        const pct = Math.min(Math.round((value / max) * 100), 100);
        return `<div class="progress-item">\n<div class="progress-header"><span class="progress-label">${label}</span><span class="progress-value">${value}/${max}</span></div>\n<div class="progress-track"><div class="progress-fill" style="width:${pct}%"></div></div>\n</div>`;
      })
      .join("\n");
    let slide = `## ${params.heading}\n\n<div class="progress-container">\n${barItems}\n</div>`;
    if (params.caption) {
      slide += `\n\n<p class="text-center">${params.caption}</p>`;
    }
    return slide;
  },
};
