import type { SlideLayout } from "../../../themes/types.js";

export const codeShowcaseLayout: SlideLayout = {
  name: "code-showcase",
  description:
    "Code block with language badge, optional explanation text, and optional highlight bullet points",
  params: {
    heading: {
      type: "string",
      description: "Slide heading (max 80 chars, ~48 chars for Japanese)",
      required: true,
      maxLength: 80,
    },
    code: {
      type: "string",
      description: "Code content. Use \\n for line breaks within the string.",
      required: true,
    },
    language: {
      type: "string",
      description:
        "Programming language label displayed as a badge (e.g. 'TypeScript', 'Python', 'Rust'). Optional.",
      required: false,
      maxLength: 30,
    },
    explanation: {
      type: "string",
      description: "Optional explanation paragraph displayed below the code block.",
      required: false,
      maxLength: 300,
    },
    highlights: {
      type: "array",
      description:
        "Optional bullet points highlighting key aspects of the code. Max 4 items.",
      required: false,
      maxItems: 4,
    },
  },
  template: (params) => {
    const lang = params.language ? String(params.language) : "";
    const langBadge = lang
      ? `<span class="dk-code-lang-badge">${lang}</span>`
      : "";

    const codeLines = String(params.code)
      .split("\\n")
      .map((line) => `<div class="dk-code-line">${line}</div>`)
      .join("\n");

    let bottom = "";
    if (params.explanation) {
      bottom += `\n<p class="dk-code-explanation">${params.explanation}</p>`;
    }
    if (Array.isArray(params.highlights) && params.highlights.length > 0) {
      const bullets = (params.highlights as string[])
        .map((h) => `<li>${h}</li>`)
        .join("\n");
      bottom += `\n<ul class="dk-code-highlights">\n${bullets}\n</ul>`;
    }

    return (
      `## ${params.heading}\n\n` +
      `<div class="dk-code-showcase">\n` +
      `<div class="dk-code-header">${langBadge}</div>\n` +
      `<div class="dk-code-body">\n${codeLines}\n</div>\n` +
      `</div>` +
      (bottom ? `\n${bottom}` : "")
    );
  },
};
