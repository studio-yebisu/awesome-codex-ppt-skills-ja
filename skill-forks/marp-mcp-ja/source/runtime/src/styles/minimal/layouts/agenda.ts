import type { SlideLayout } from "../../../themes/types.js";

export const agendaLayout: SlideLayout = {
  name: "agenda",
  description:
    "Clean agenda slide with numbered items and optional time durations (use 'Item name|Duration' format)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    items: {
      type: "array",
      description:
        "Agenda items in 'Item name|Duration' format (duration is optional). Max 8 items.",
      required: true,
      maxItems: 8,
    },
    subtitle: {
      type: "string",
      description: "Optional subtitle displayed below the heading",
      required: false,
      maxLength: 120,
    },
  },
  template: (params) => {
    const subtitle = params.subtitle ? `\n\n<p class="min-agenda-subtitle">${params.subtitle}</p>` : "";
    const items = (params.items as string[])
      .map((item, i) => {
        const parts = item.split("|");
        const title = parts[0].trim();
        const duration = parts.length > 1 ? parts[1].trim() : null;
        const num = String(i + 1).padStart(2, "0");
        return (
          `<div class="min-agenda-item">\n` +
          `<span class="min-agenda-num">${num}</span>\n` +
          `<span class="min-agenda-title">${title}</span>\n` +
          (duration ? `<span class="min-agenda-dur">${duration}</span>\n` : "") +
          `</div>`
        );
      })
      .join("\n");
    return `## ${params.heading}${subtitle}\n\n<div class="min-agenda">\n${items}\n</div>`;
  },
};
