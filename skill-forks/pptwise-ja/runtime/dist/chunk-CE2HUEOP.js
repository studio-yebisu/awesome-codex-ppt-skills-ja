import {
  findRemoteAssetRef,
  installPlatform
} from "./chunk-RHKPZSTM.js";

// src/platform/node.ts
import { createRequire } from "module";
import { DOMParser as LinkedomDOMParser } from "linkedom";

// src/cli/proxy-fetch.ts
import { EnvHttpProxyAgent, fetch as undiciFetch } from "undici";
var CONNECT_CODES = /* @__PURE__ */ new Set([
  "UND_ERR_CONNECT_TIMEOUT",
  "ECONNREFUSED",
  "ECONNRESET",
  "ENOTFOUND",
  "EHOSTUNREACH",
  "ENETUNREACH",
  "ETIMEDOUT"
]);
function hasProxyEnv(env) {
  return Boolean(env.HTTPS_PROXY || env.https_proxy || env.HTTP_PROXY || env.http_proxy);
}
function connectFailureHint(error, url) {
  const cause = error instanceof Error ? error.cause : void 0;
  if (!cause?.code || !CONNECT_CODES.has(cause.code)) return null;
  let host;
  try {
    host = new URL(url).host;
  } catch {
    return null;
  }
  return `Could not connect to ${host} (${cause.code}). The request never reached the network. If this machine reaches the internet through a proxy, set HTTPS_PROXY/HTTP_PROXY.`;
}
function requestUrl(input) {
  if (typeof input === "string") return input;
  if (input instanceof URL) return input.href;
  return input.url;
}
async function proxyFetch(input, init) {
  if (!hasProxyEnv(process.env)) {
    return await fetch(input, init);
  }
  const dispatcher = new EnvHttpProxyAgent();
  try {
    const response = await undiciFetch(requestUrl(input), {
      ...init,
      dispatcher
    });
    const buffered = Buffer.from(await response.arrayBuffer());
    await dispatcher.close();
    return new Response(buffered, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers
    });
  } catch (error) {
    await dispatcher.close().catch(() => {
    });
    const hint = connectFailureHint(error, requestUrl(input));
    throw hint ? new Error(hint, { cause: error }) : error;
  }
}

// src/platform/node.ts
function isMissingModuleError(e) {
  const err = e;
  return err?.code === "ERR_MODULE_NOT_FOUND" || /Cannot find/.test(err?.message ?? "");
}
async function loadSharp(missingDepContext) {
  try {
    return (await import("sharp")).default;
  } catch (e) {
    if (isMissingModuleError(e)) {
      throw new Error(`${missingDepContext} requires the optional dependency "sharp" (npm i sharp)`);
    }
    throw e;
  }
}
async function recodeWithSharp(dataUrl) {
  const sharpMod = await loadSharp("Re-encoding non-PNG/JPEG/GIF images");
  const base64 = dataUrl.slice(dataUrl.indexOf(",") + 1);
  const png = await sharpMod(Buffer.from(base64, "base64")).png().toBuffer();
  return `data:image/png;base64,${png.toString("base64")}`;
}
async function rasterizeWithSharp(svgMarkup, width, height) {
  const remoteRef = findRemoteAssetRef(svgMarkup);
  if (remoteRef) {
    throw new Error(
      `rasterizeSvg: refusing to rasterize an SVG that references a remote image (${remoteRef}) \u2014 only data-URI (or other local) assets are supported, pptwise audit never makes a network request`
    );
  }
  const sharpMod = await loadSharp("Pixel-contrast auditing (--pixels)");
  const { data, info } = await sharpMod(Buffer.from(svgMarkup, "utf-8")).resize(width, height, { fit: "fill" }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  return {
    width: info.width,
    height: info.height,
    data: new Uint8ClampedArray(data.buffer, data.byteOffset, data.byteLength)
  };
}
var DECODE_PROBE_PX = 16;
async function decodeImageWithSharp(bytes) {
  const sharpMod = await loadSharp("Verifying image assets before export");
  const input = Buffer.from(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const meta = await sharpMod(input).metadata();
  if (!meta.width || !meta.height) {
    throw new Error("image header carries no pixel size");
  }
  await sharpMod(input).resize({ width: DECODE_PROBE_PX, height: DECODE_PROBE_PX, fit: "inside", withoutEnlargement: true }).raw().toBuffer();
  return { width: meta.width, height: meta.height };
}
function sharpIsResolvable() {
  try {
    createRequire(import.meta.url).resolve("sharp");
    return true;
  } catch {
    return false;
  }
}
function installNodePlatform() {
  installPlatform({
    domParser: LinkedomDOMParser,
    recodeImageToPng: recodeWithSharp,
    rasterizeSvg: rasterizeWithSharp,
    decodeImage: sharpIsResolvable() ? decodeImageWithSharp : void 0,
    fetch: proxyFetch
  });
}

export {
  proxyFetch,
  isMissingModuleError,
  installNodePlatform
};
//# sourceMappingURL=chunk-CE2HUEOP.js.map