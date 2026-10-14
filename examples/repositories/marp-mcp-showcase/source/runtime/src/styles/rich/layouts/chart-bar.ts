import type { SlideLayout } from "../../../themes/types.js";

export const chartBarLayout: SlideLayout = {
  name: "chart-bar",
  description: "Pure CSS horizontal bar chart for data visualization (use 'Label|Value' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    bars: {
      type: "array",
      description: "Bar data in 'Label|Value' format",
      required: true,
      maxItems: 8,
    },
    maxValue: {
      type: "number",
      description: "Maximum value for scale (auto-detected if omitted)",
      required: false,
    },
    caption: {
      type: "string",
      description: "Optional caption below the chart",
      required: false,
      maxLength: 200,
    },
  },
  template: (params) => {
    const bars = params.bars as string[];
    const parsed = bars.map((bar) => {
      const parts = bar.split("|");
      return { label: parts[0]?.trim() || "", value: Number(parts[1]?.trim()) || 0 };
    });
    const max = (params.maxValue as number) || Math.max(...parsed.map((b) => b.value), 1);
    const barItems = parsed
      .map((b) => {
        const pct = Math.min(Math.round((b.value / max) * 100), 100);
        return `<div class="chart-bar-row">\n<span class="chart-bar-label">${b.label}</span>\n<div class="chart-bar-track"><div class="chart-bar-fill" style="width:${pct}%"></div></div>\n<span class="chart-bar-value">${b.value}</span>\n</div>`;
      })
      .join("\n");
    let slide = `## ${params.heading}\n\n<div class="chart-bar-container">\n${barItems}\n</div>`;
    if (params.caption) {
      slide += `\n\n<p class="text-center">${params.caption}</p>`;
    }
    return slide;
  },
};
