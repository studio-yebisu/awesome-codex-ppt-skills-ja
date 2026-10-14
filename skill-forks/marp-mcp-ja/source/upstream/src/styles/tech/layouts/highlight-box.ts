import type { SlideLayout } from "../../../themes/types.js";

export const highlightBoxLayout: SlideLayout = {
  name: "highlight-box",
  description:
    "Alert/callout box with color-coded variants: 'info' (cyan), 'warning' (amber), 'success' (green)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    type: {
      type: "string",
      description: "Box variant: 'info' (default, cyan), 'warning' (amber), 'success' (green)",
      required: false,
      maxLength: 10,
    },
    label: {
      type: "string",
      description: "Small label displayed above the content (e.g. 'NOTE', 'WARNING', 'TIP')",
      required: false,
      maxLength: 40,
    },
    content: {
      type: "string",
      description: "Main content of the callout box",
      required: true,
      maxLength: 400,
    },
    body: {
      type: "string",
      description: "Optional additional content below the highlight box (supports markdown)",
      required: false,
    },
  },
  template: (params) => {
    const boxType = String(params.type || "info");
    const validTypes = ["info", "warning", "success"];
    const safeType = validTypes.includes(boxType) ? boxType : "info";

    const defaultLabels: Record<string, string> = {
      info: "INFO",
      warning: "WARNING",
      success: "SUCCESS",
    };
    const label = params.label ? String(params.label) : defaultLabels[safeType];

    const body = params.body ? `\n\n${params.body}` : "";

    return (
      `## ${params.heading}\n\n` +
      `<div class="tech-highlight-${safeType}">\n` +
      `<p class="tech-highlight-label">${label}</p>\n` +
      `<p class="tech-highlight-content">${params.content}</p>\n` +
      `</div>` +
      body
    );
  },
};
