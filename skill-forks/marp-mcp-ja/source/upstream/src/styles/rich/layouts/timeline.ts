import type { SlideLayout } from "../../../themes/types.js";

export const timelineLayout: SlideLayout = {
  name: "timeline",
  description: "Vertical timeline with labeled events (use 'Label: Description' format)",
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
      maxItems: 8,
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
          return `<div class="timeline-item">\n<strong>${label}</strong> <span>${desc}</span>\n</div>`;
        }
        return `<div class="timeline-item">\n<strong>${item}</strong>\n</div>`;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="timeline">\n${timelineItems}\n</div>`;
  },
};
