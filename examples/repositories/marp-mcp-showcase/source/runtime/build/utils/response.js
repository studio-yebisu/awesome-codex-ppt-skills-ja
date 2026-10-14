/**
 * Helper functions for creating standardized MCP tool responses
 */
/**
 * Creates an error response with the isError flag set to true.
 */
export function createErrorResponse(message) {
    return {
        isError: true,
        content: [
            {
                type: "text",
                text: `Error: ${message}`,
            },
        ],
    };
}
/**
 * Creates a success response with JSON-formatted data.
 */
export function createSuccessResponse(data) {
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify({ success: true, ...data }, null, 2),
            },
        ],
    };
}
