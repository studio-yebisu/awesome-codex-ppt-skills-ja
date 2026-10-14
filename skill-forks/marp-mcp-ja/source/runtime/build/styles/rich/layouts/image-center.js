export const imageCenterLayout = {
    name: "image-center",
    description: "Rich centered image slide with rounded corners and shadow",
    className: "rich-image-center",
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
        caption: {
            type: "string",
            description: "Image caption displayed below",
            required: false,
            maxLength: 120,
        },
        citations: {
            type: "string",
            description: "Citation (no line break)",
            required: false,
            maxLength: 130,
        },
    },
    template: (params) => {
        let slide = `<!-- _class: rich-image-center -->\n\n`;
        if (params.heading) {
            slide += `## ${params.heading}\n\n`;
        }
        slide += `<div class="image-center-wrap">\n\n![h:400](${params.imagePath})\n\n</div>`;
        if (params.caption) {
            slide += `\n\n<p class="image-caption">${params.caption}</p>`;
        }
        if (params.description) {
            slide += `\n\n${params.description}`;
        }
        if (params.citations) {
            slide += `\n\n<!-- _footer: ${params.citations} -->`;
        }
        return slide;
    },
};
