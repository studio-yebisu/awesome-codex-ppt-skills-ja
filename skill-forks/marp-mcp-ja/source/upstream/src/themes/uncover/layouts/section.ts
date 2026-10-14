/**
 * Uncover theme - Section layout
 */

import type { SlideLayout } from "../../types.js";
import { withLengthPrompt } from "../../../utils/text-length.js";

export const sectionLayout: SlideLayout = {
  name: "section",
  description: "Section break slide with centered title and subtitle",
  params: {
    title: {
      type: "string",
      description: withLengthPrompt("Section title", 24),
      required: true,
      maxLength: 24,
    },
    subtitle: {
      type: "string",
      description: withLengthPrompt("Section subtitle", 28),
      required: false,
      maxLength: 28,
    },
  },
  template: (params) => {
    let slide = `# ${params.title}\n`;
    if (params.subtitle) {
      slide += `## ${params.subtitle}\n`;
    }
    return slide;
  },
};
