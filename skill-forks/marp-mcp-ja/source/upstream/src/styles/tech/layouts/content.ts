import type { SlideLayout } from "../../../themes/types.js";

export const contentLayout: SlideLayout = {
  name: "content",
  description: "Standard content slide with heading and free-form markdown body, accented with a violet left border",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    body: {
      type: "string",
      description:
        "Slide body text. Supports markdown: bullets with -, bold with **, inline code with backticks.",
      required: true,
    },
  },
  template: (params) =>
    `## ${params.heading}\n\n<div class="tech-content">\n\n${params.body}\n\n</div>`,
};
