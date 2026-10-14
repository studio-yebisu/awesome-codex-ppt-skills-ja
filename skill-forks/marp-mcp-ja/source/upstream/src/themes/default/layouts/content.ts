/**
 * Default theme - Content layout
 */

import type { SlideLayout } from "../../types.js";
import { withLengthPrompt } from "../../../utils/text-length.js";

export const contentLayout: SlideLayout = {
  name: "content",
  description:
    "Standard content slide with heading and free-form markdown body (supports bullets with -, bold with **, code with backticks)",
  params: {
    heading: {
      type: "string",
      description: withLengthPrompt("Slide heading", 54),
      required: true,
      maxLength: 54,
    },
    body: {
      type: "string",
      description:
        "Slide body text. Supports markdown: bullets with -, bold with **, inline code with backticks.",
      required: true,
    },
    citations: {
      type: "string",
      description: withLengthPrompt("Citation", 130, { note: "no line break" }),
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = `## ${params.heading}\n\n${params.body}`;
    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }
    return slide;
  },
};
