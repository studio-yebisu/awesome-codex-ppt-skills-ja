import type { SlideLayout } from "../../../themes/types.js";

export const agendaLayout: SlideLayout = {
  name: "agenda",
  description: "Agenda slide with numbered items and optional duration (use 'Item name|Duration' format)",
  className: "corp-agenda",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    items: {
      type: "array",
      description: "Agenda items in 'Item name|Duration' format (duration is optional)",
      required: true,
      maxItems: 8,
    },
  },
  template: (params) => {
    const items = (params.items as string[])
      .map((item, i) => {
        const parts = item.split("|");
        const title = parts[0].trim();
        const duration = parts.length > 1 ? parts[1].trim() : null;
        return `<div class="corp-agenda-item">\n<span class="corp-agenda-num">${String(i + 1).padStart(2, "0")}</span>\n<div class="corp-agenda-content"><strong>${title}</strong>${duration ? `<span class="corp-agenda-dur">${duration}</span>` : ""}</div>\n</div>`;
      })
      .join("\n");
    return `## ${params.heading}\n\n<div class="corp-agenda">\n${items}\n</div>`;
  },
};
