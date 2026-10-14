import type { SlideLayout } from "../../../themes/types.js";

export const imageCenterLayout: SlideLayout = {
  name: "image-center",
  description: "Dark centered image slide",
  className: "dk-img-center",
  params: {
    heading: {
      type: "string",
      description: "Slide heading",
      required: true,
      maxLength: 54,
    },
    imagePath: {
      type: "string",
      description: "Image file path or URL",
      required: true,
    },
    description: {
      type: "string",
      description: "Image description below image",
      required: false,
      maxLength: 75,
    },
    citations: {
      type: "string",
      description: "Citation (no line break)",
      required: false,
      maxLength: 130,
    },
  },
  template: (params) => {
    let slide = `<!-- _class: dk-img-center -->\n\n`;
    if (params.heading) {
      slide += `## ${params.heading}\n\n`;
    }

    slide += `<div class="dk-image-center-wrap">\n\n![h:400](${params.imagePath})\n\n</div>`;

    if (params.description) {
      slide += `\n\n${params.description}`;
    }

    if (params.citations) {
      slide += `\n\n<!-- _footer: ${params.citations} -->`;
    }

    return slide;
  },
};
