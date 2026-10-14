import type { SlideLayout } from "../../../themes/types.js";

export const terminalLayout: SlideLayout = {
  name: "terminal",
  description: "Terminal-style command display on dark background (prefix lines with '$ ' for commands)",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 80,
    },
    terminalTitle: {
      type: "string",
      description: "Terminal window title (default: 'Terminal')",
      required: false,
      maxLength: 60,
    },
    lines: {
      type: "array",
      description: "Terminal lines; prefix with '$ ' for command lines, plain text for output",
      required: true,
      maxItems: 15,
    },
  },
  template: (params) => {
    const lines = (params.lines as string[])
      .map((l) => `<div class="dk-terminal-line">${l}</div>`)
      .join("\n");
    const title = (params.terminalTitle as string) || "Terminal";
    return `## ${params.heading}\n\n<div class="dk-terminal-box">\n<div class="dk-terminal-header">${title}</div>\n<div class="dk-terminal-body">\n${lines}\n</div>\n</div>`;
  },
};
