/**
 * Default theme - List layout
 */
import { formatLengthPrompt, withLengthPrompt, } from "../../../utils/text-length.js";
export const listLayout = {
    name: "list",
    description: "List slide with bullet points (max 8 items)",
    params: {
        heading: {
            type: "string",
            description: withLengthPrompt("Slide heading", 54),
            required: true,
            maxLength: 54,
        },
        list: {
            type: "array",
            description: `List items (max 10 items, each ${formatLengthPrompt(70)})`,
            required: true,
            maxItems: 10,
            maxLength: 70,
        },
        citations: {
            type: "string",
            description: withLengthPrompt("Citation", 130, {
                note: "no line break",
            }),
            required: false,
            maxLength: 130,
        },
    },
    template: (params) => {
        let slide = "";
        if (params.heading) {
            slide += `## ${params.heading}\n\n`;
        }
        const list = params.list;
        list.forEach((item) => {
            slide += `- ${item}\n`;
        });
        if (params.citations) {
            slide += `\n\n<!-- _footer: ${params.citations} -->`;
        }
        return slide;
    },
};
