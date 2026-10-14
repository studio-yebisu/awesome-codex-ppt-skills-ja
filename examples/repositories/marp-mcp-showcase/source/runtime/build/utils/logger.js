/**
 * Structured logging utilities
 */
/**
 * Gets the log level from environment variable.
 * Defaults to 'info' if not set or invalid.
 */
function getLogLevel() {
    const envLevel = process.env.MCP_LOG_LEVEL?.toLowerCase();
    const validLevels = ["debug", "info", "warn", "error"];
    return validLevels.includes(envLevel)
        ? envLevel
        : "info";
}
const LOG_LEVELS = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3,
};
const currentLogLevel = getLogLevel();
/**
 * Logs a structured message to stderr.
 *
 * @param level - Log level
 * @param message - Log message
 * @param metadata - Additional metadata to include in the log entry
 */
export function log(level, message, metadata) {
    // Only log if the message level is at or above the current log level
    if (LOG_LEVELS[level] < LOG_LEVELS[currentLogLevel]) {
        return;
    }
    const entry = {
        level,
        message,
        timestamp: new Date().toISOString(),
        ...metadata,
    };
    console.error(JSON.stringify(entry));
}
/**
 * Logs a debug message.
 */
export function debug(message, metadata) {
    log("debug", message, metadata);
}
/**
 * Logs an info message.
 */
export function info(message, metadata) {
    log("info", message, metadata);
}
/**
 * Logs a warning message.
 */
export function warn(message, metadata) {
    log("warn", message, metadata);
}
/**
 * Logs an error message.
 */
export function error(message, metadata) {
    log("error", message, metadata);
}
