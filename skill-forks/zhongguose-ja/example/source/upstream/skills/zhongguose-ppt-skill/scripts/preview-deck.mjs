#!/usr/bin/env node
import fs from "node:fs";
import http from "node:http";
import path from "node:path";

const target = process.argv[2];
const portFlag = process.argv.indexOf("--port");
const requestedPort = portFlag >= 0 ? Number(process.argv[portFlag + 1]) : 4173;

if (!target || !Number.isInteger(requestedPort) || requestedPort < 0 || requestedPort > 65535) {
  console.error("Usage: node scripts/preview-deck.mjs path/to/index.html [--port 4173]");
  process.exit(2);
}

const indexFile = path.resolve(target);
if (!fs.existsSync(indexFile)) {
  console.error("Deck not found: " + indexFile);
  process.exit(2);
}

const root = path.dirname(indexFile);
const mime = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8"
};

const server = http.createServer(function (request, response) {
  const requestUrl = new URL(request.url || "/", "http://127.0.0.1");
  const relative = requestUrl.pathname === "/" ? path.basename(indexFile) : decodeURIComponent(requestUrl.pathname.slice(1));
  const candidate = path.resolve(root, relative);
  const rel = path.relative(root, candidate);
  const inside = rel === "" || (!rel.startsWith(".." + path.sep) && rel !== ".." && !path.isAbsolute(rel));

  if (!inside || !fs.existsSync(candidate) || !fs.statSync(candidate).isFile()) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
    return;
  }

  response.writeHead(200, {
    "content-type": mime[path.extname(candidate).toLowerCase()] || "application/octet-stream",
    "cache-control": "no-store"
  });
  fs.createReadStream(candidate).pipe(response);
});

server.listen(requestedPort, "127.0.0.1", function () {
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : requestedPort;
  console.log("Preview ready: http://127.0.0.1:" + port + "/" + encodeURIComponent(path.basename(indexFile)));
  console.log("Press Ctrl+C to stop.");
});

process.on("SIGINT", function () {
  server.close(function () { process.exit(0); });
});
