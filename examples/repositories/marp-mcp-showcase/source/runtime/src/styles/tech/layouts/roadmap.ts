import type { SlideLayout } from "../../../themes/types.js";

export const roadmapLayout: SlideLayout = {
  name: "roadmap",
  description:
    "Horizontal milestone timeline with status indicators. Use 'Phase|Label|Status' format. Status: 'done', 'current', or 'future'.",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    milestones: {
      type: "array",
      description:
        "Milestones in 'Phase|Label|Status' format. Status: 'done' (completed, violet), 'current' (active, cyan), 'future' (upcoming, muted). Max 6 milestones.",
      required: true,
      maxItems: 6,
    },
    subtitle: {
      type: "string",
      description: "Optional subtitle or period label shown below the heading",
      required: false,
      maxLength: 100,
    },
  },
  template: (params) => {
    const subtitle = params.subtitle
      ? `\n\n<p style="font-size:0.85em;color:#64748b;margin:0 0 0.5rem">${params.subtitle}</p>`
      : "";

    const milestones = (params.milestones as string[])
      .map((m) => {
        const parts = m.split("|");
        const phase = parts[0]?.trim() ?? "";
        const label = parts[1]?.trim() ?? "";
        const rawStatus = parts[2]?.trim().toLowerCase() ?? "future";
        const validStatuses = ["done", "current", "future"];
        const status = validStatuses.includes(rawStatus) ? rawStatus : "future";
        return (
          `<div class="tech-milestone ${status}">\n` +
          `<div class="tech-milestone-dot"></div>\n` +
          `<span class="tech-milestone-phase">${phase}</span>\n` +
          `<span class="tech-milestone-label">${label}</span>\n` +
          `</div>`
        );
      })
      .join("\n");

    return `## ${params.heading}${subtitle}\n\n<div class="tech-roadmap">\n${milestones}\n</div>`;
  },
};
