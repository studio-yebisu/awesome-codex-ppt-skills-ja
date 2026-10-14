export const statisticsLayout = {
    name: "statistics",
    description: "Dark statistics display with large indigo numbers (use 'Number|Label' format)",
    params: {
        heading: {
            type: "string",
            description: "Slide heading",
            required: true,
            maxLength: 80,
        },
        stats: {
            type: "array",
            description: "Statistics in 'Number|Label' or 'Number|Label|Trend' format (e.g. '95%|Accuracy|+5% from Q1')",
            required: true,
            maxItems: 5,
        },
        caption: {
            type: "string",
            description: "Optional caption below statistics",
            required: false,
            maxLength: 200,
        },
    },
    template: (params) => {
        const stats = params.stats;
        const statItems = stats
            .map((stat) => {
            const parts = stat.split("|");
            if (parts.length >= 2) {
                const number = parts[0].trim();
                const label = parts[1].trim();
                const trend = parts[2]?.trim();
                let inner = `<div class="dk-stat-number">${number}</div>\n<div class="dk-stat-label">${label}</div>`;
                if (trend) {
                    inner += `\n<div class="dk-stat-trend">${trend}</div>`;
                }
                return `<div>\n${inner}\n</div>`;
            }
            return `<div>\n<div class="dk-stat-number">${stat}</div>\n</div>`;
        })
            .join("\n");
        let slide = `## ${params.heading}\n\n<div class="dk-stat-box">\n${statItems}\n</div>`;
        if (params.caption) {
            slide += `\n\n<p>${params.caption}</p>`;
        }
        return slide;
    },
};
