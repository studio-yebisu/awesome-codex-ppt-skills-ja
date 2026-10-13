// 每项的第一个扩展名用于 data: URL 落盘，其余扩展名和 aliases 共享同一格式。
export const MEDIA_FORMATS = [
  { kind: 'image', mime: 'image/png', extensions: ['.png'] },
  { kind: 'image', mime: 'image/jpeg', extensions: ['.jpg', '.jpeg'] },
  { kind: 'image', mime: 'image/webp', extensions: ['.webp'] },
  { kind: 'image', mime: 'image/gif', extensions: ['.gif'] },
  { kind: 'image', mime: 'image/svg+xml', extensions: ['.svg'] },
  { kind: 'image', mime: 'image/avif', extensions: ['.avif'] },
  { kind: 'video', mime: 'video/mp4', extensions: ['.mp4', '.m4v'], aliases: ['video/x-m4v'] },
  { kind: 'video', mime: 'video/webm', extensions: ['.webm'] },
  { kind: 'video', mime: 'video/quicktime', extensions: ['.mov'] },
  { kind: 'video', mime: 'video/ogg', extensions: ['.ogv'] },
];

const byExtension = new Map(MEDIA_FORMATS.flatMap(format => format.extensions.map(extension => [extension, format])));
const byMime = new Map(MEDIA_FORMATS.flatMap(format => [format.mime, ...(format.aliases || [])].map(mime => [mime, format])));

export function mediaFormatForExtension(extension) {
  return byExtension.get(String(extension || '').toLowerCase());
}

export function mediaFormatForMime(mime) {
  return byMime.get(String(mime || '').split(';')[0].trim().toLowerCase());
}
