/**
 * Structured logging utilities
 */

type LogLevel = "debug" | "info" | "warn" | "error";

interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  [key: string]: unknown;
}

/**
 * Gets the log level from environment variable.
 * Defaults to 'info' if not set or invalid.
 */
function getLogLevel(): LogLevel {
  const envLevel = process.env.MCP_LOG_LEVEL?.toLowerCase();
  const validLevels: LogLevel[] = ["debug", "info", "warn", "error"];
  return validLevels.includes(envLevel as LogLevel)
    ? (envLevel as LogLevel)
    : "info";
}

const LOG_LEVELS: Record<LogLevel, number> = {
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
export function log(
  level: LogLevel,
  message: string,
  metadata?: Record<string, unknown>
): void {
  // Only log if the message level is at or above the current log level
  if (LOG_LEVELS[level] < LOG_LEVELS[currentLogLevel]) {
    return;
  }

  const entry: LogEntry = {
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
export function debug(message: string, metadata?: Record<string, unknown>): void {
  log("debug", message, metadata);
}

/**
 * Logs an info message.
 */
export function info(message: string, metadata?: Record<string, unknown>): void {
  log("info", message, metadata);
}

/**
 * Logs a warning message.
 */
export function warn(message: string, metadata?: Record<string, unknown>): void {
  log("warn", message, metadata);
}

/**
 * Logs an error message.
 */
export function error(message: string, metadata?: Record<string, unknown>): void {
  log("error", message, metadata);
}
