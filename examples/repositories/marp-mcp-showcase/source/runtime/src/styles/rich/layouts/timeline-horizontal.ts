import type { SlideLayout } from "../../../themes/types.js";

export const timelineHorizontalLayout: SlideLayout = {
  name: "timeline-horizontal",
  description: "Horizontal timeline with labeled events (use 'Label: Description' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    items: {
      type: "array",
      description: "Timeline items in 'Label: Description' format",
      required: true,
      maxItems: 6,
    },
  },
  template: (params) => {
    const items = params.items as string[];
    const timelineItems = items
      .map((item) => {
        const colonIdx = item.indexOf(":");
        if (colonIdx > 0) {
          const label = item.substring(0, colonIdx).trim();
          const desc = item.substring(colonIdx + 1).trim();
          return `<div class="h-timeline-item">\n<div class="h-timeline-dot"></div>\n<strong>${label}</strong>\n<span>${desc}</span>\n</div>`;
        }
        return `<div class="h-timeline-item">\n<div class="h-timeline-dot"></div>\n<strong>${item}</strong>\n</div>`;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="h-timeline">\n<div class="h-timeline-line"></div>\n<div class="h-timeline-items">\n${timelineItems}\n</div>\n</div>`;
  },
};
