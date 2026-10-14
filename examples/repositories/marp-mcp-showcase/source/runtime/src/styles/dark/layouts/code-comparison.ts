import type { SlideLayout } from "../../../themes/types.js";

export const codeComparisonLayout: SlideLayout = {
  name: "code-comparison",
  description: "Side-by-side code comparison (Before/After or two languages)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    leftTitle: {
      type: "string",
      description: "Left panel title (e.g. 'Before', 'JavaScript')",
      required: true,
      maxLength: 40,
    },
    leftCode: {
      type: "string",
      description: "Left code block content",
      required: true,
    },
    rightTitle: {
      type: "string",
      description: "Right panel title (e.g. 'After', 'TypeScript')",
      required: true,
      maxLength: 40,
    },
    rightCode: {
      type: "string",
      description: "Right code block content",
      required: true,
    },
    language: {
      type: "string",
      description: "Programming language for syntax highlighting (e.g. 'js', 'python')",
      required: false,
    },
  },
  template: (params) => {
    const lang = (params.language as string) || "";
    const leftLines = (params.leftCode as string)
      .split("\\n")
      .map((line) => `<div class="dk-terminal-line">${line}</div>`)
      .join("\n");
    const rightLines = (params.rightCode as string)
      .split("\\n")
      .map((line) => `<div class="dk-terminal-line">${line}</div>`)
      .join("\n");

    return `## ${params.heading}\n\n<div class="dk-code-compare">\n<div class="dk-code-panel">\n<div class="dk-terminal-header">${params.leftTitle}${lang ? ` (${lang})` : ""}</div>\n<div class="dk-terminal-body">\n${leftLines}\n</div>\n</div>\n<div class="dk-code-panel">\n<div class="dk-terminal-header">${params.rightTitle}${lang ? ` (${lang})` : ""}</div>\n<div class="dk-terminal-body">\n${rightLines}\n</div>\n</div>\n</div>`;
  },
};
