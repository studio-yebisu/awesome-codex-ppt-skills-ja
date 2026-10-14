/**
 * Gaia theme - Image-right layout
 */

import type { SlideLayout } from "../../types.js";
import {
  formatLengthPrompt,
  withLengthPrompt,
} from "../../../utils/text-length.js";

export const imageRightLayout: SlideLayout = {
  name: "image-right",
  description:
    "Slide with image on right and content list (allows more explanation than image-center)",
  params: {
    heading: {
      type: "string",
      description: withLengthPrompt("Slide heading", 16),
      required: true,
      maxLength: 16,
    },
    list: {
      type: "array",
      description: `List items (max 8 items, each ${formatLengthPrompt(24)})`,
      required: true,
      maxItems: 8,
      maxLength: 24,
    },
    imagePath: {
      type: "string",
      description:
        "Image file path (local paths supported, e.g., ./attachments/image.png)",
      required: true,
    },
    citations: {
      type: "string",
      description: withLengthPrompt("Citation", 45, {
        note: "no line break",
      }),
      required: false,
      maxLength: 45,
    },
  },
  template: (params) => {
    let slide = "";

    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    const list = params.list as string[];
    list.forEach((item: string) => {
      slide += `- ${item}\n`;
    });

    slide += `\n![bg right:50% contain](${params.imagePath})`;

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
