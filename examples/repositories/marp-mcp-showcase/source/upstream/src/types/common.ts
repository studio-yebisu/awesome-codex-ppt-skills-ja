/**
 * Common type definitions used across the MCP server
 */

/**
 * Standard response format for MCP tools
 */
export interface ToolResponse {
  [x: string]: unknown;
  content: Array<{
    type: "text";
    text: string;
  }>;
}
