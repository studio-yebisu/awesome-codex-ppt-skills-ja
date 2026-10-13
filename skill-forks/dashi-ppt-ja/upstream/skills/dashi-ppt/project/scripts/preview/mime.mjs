import path from 'node:path';
import { mediaFormatForExtension } from '../media-formats.mjs';

const MIME_TYPES = {
  '.html': 'text/html;charset=utf-8',
  '.js': 'text/javascript;charset=utf-8',
  '.mjs': 'text/javascript;charset=utf-8',
  '.css': 'text/css;charset=utf-8',
  '.json': 'application/json;charset=utf-8',
  '.mp3': 'audio/mpeg',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.txt': 'text/plain;charset=utf-8',
  '.pdf': 'application/pdf',
};

export function contentType(file) {
  const extension = path.extname(String(file)).toLowerCase();
  return mediaFormatForExtension(extension)?.mime || MIME_TYPES[extension] || 'application/octet-stream';
}
