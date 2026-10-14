#!/usr/bin/env node
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
import { spawnSync } from "node:child_process";

const target = process.argv[2];

if (!target) {
  console.error("Usage: node scripts/browser-qa.mjs path/to/index.html");
  process.exit(2);
}

const indexFile = path.resolve(target);
if (!fs.existsSync(indexFile)) {
  console.error("Deck not found: " + indexFile);
  process.exit(2);
}

function commandPath(command) {
  const lookup = process.platform === "win32" ? "where.exe" : "which";
  const result = spawnSync(lookup, [command], { encoding: "utf8", windowsHide: true });
  if (result.status === 0) {
    const first = result.stdout.split(/\r?\n/).find(Boolean);
    return first ? first.trim() : null;
  }
  return null;
}

function findBrowser() {
  const candidates = [];
  if (process.env.CHROME_PATH) {
    candidates.push(process.env.CHROME_PATH);
  }
  if (process.platform === "win32") {
    for (const base of [process.env.PROGRAMFILES, process.env["PROGRAMFILES(X86)"], process.env.LOCALAPPDATA]) {
      if (base) {
        candidates.push(path.join(base, "Microsoft", "Edge", "Application", "msedge.exe"));
      }
    }
    for (const base of [process.env.PROGRAMFILES, process.env["PROGRAMFILES(X86)"], process.env.LOCALAPPDATA]) {
      if (base) {
        candidates.push(path.join(base, "Google", "Chrome", "Application", "chrome.exe"));
      }
    }
  } else if (process.platform === "darwin") {
    candidates.push("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome");
    candidates.push("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge");
    candidates.push("/Applications/Chromium.app/Contents/MacOS/Chromium");
  }
  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) {
      return candidate;
    }
  }
  for (const command of ["google-chrome", "chrome", "chromium", "chromium-browser", "msedge"]) {
    const found = commandPath(command);
    if (found) {
      return found;
    }
  }
  return null;
}

function loadPlaywright() {
  const require = createRequire(import.meta.url);
  const packageNames = [];
  if (process.env.PLAYWRIGHT_PATH) {
    packageNames.push(process.env.PLAYWRIGHT_PATH);
  }
  packageNames.push("playwright-core", "playwright");
  for (const packageName of packageNames) {
    try {
      return require(packageName);
    } catch {
      continue;
    }
  }
  return null;
}

const browserPath = findBrowser();
if (!browserPath) {
  console.error("No Chrome, Edge, or Chromium executable found. Set CHROME_PATH and retry.");
  process.exit(2);
}

const root = path.dirname(indexFile);
const missingRequests = [];
const mime = {
  ".html": "text/html; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".woff2": "font/woff2",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".js": "text/javascript; charset=utf-8"
};

const qaClient = String.raw`<script>
(async function () {
  if (window.__setStaticMode) window.__setStaticMode(true);
  await new Promise(function (resolve) { requestAnimationFrame(function () { requestAnimationFrame(resolve); }); });
  await Promise.race([
    document.fonts.ready,
    new Promise(function (resolve) { setTimeout(resolve, 4000); })
  ]);

  const slides = Array.from(document.querySelectorAll('section.slide'));
  const issues = [];
  slides.forEach(function (slide, index) {
    const frame = slide.querySelector('.canvas-card') || slide;
    const overflowX = frame.scrollWidth - frame.clientWidth;
    const overflowY = frame.scrollHeight - frame.clientHeight;
    if (overflowX > 2) {
      issues.push({ slide: index + 1, kind: 'overflow-x', detail: frame.scrollWidth + ' > ' + frame.clientWidth });
    }
    if (overflowY > 2) {
      issues.push({ slide: index + 1, kind: 'overflow-y', detail: frame.scrollHeight + ' > ' + frame.clientHeight });
    }
  });

  const coverText = (document.querySelector('.cover-title') || {}).textContent || '飞泉绿';
  try { await document.fonts.load('48px "Zhongguose Cover"', coverText); } catch {}
  const coverFontLoaded = Array.from(document.fonts).some(function (face) {
    return face.family.replace(/["']/g, '') === 'Zhongguose Cover' && face.status === 'loaded';
  });
  const report = {
    viewport: innerWidth + 'x' + innerHeight,
    slideCount: slides.length,
    issues: issues,
    coverFontLoaded: coverFontLoaded
  };
  const meta = document.createElement('meta');
  meta.id = 'qa-result';
  meta.setAttribute('data-json', encodeURIComponent(JSON.stringify(report)));
  document.head.appendChild(meta);
})();
</script>`;

const server = http.createServer(function (request, response) {
  const requestUrl = new URL(request.url || "/", "http://127.0.0.1");
  if (requestUrl.pathname === "/favicon.ico") {
    response.writeHead(204, { "cache-control": "no-store" });
    response.end();
    return;
  }
  const relative = requestUrl.pathname === "/" ? path.basename(indexFile) : decodeURIComponent(requestUrl.pathname.slice(1));
  const candidate = path.resolve(root, relative);
  const rel = path.relative(root, candidate);
  const inside = rel === "" || (!rel.startsWith(".." + path.sep) && rel !== ".." && !path.isAbsolute(rel));
  if (!inside || !fs.existsSync(candidate) || !fs.statSync(candidate).isFile()) {
    missingRequests.push(requestUrl.pathname);
    response.writeHead(404);
    response.end();
    return;
  }
  response.writeHead(200, {
    "content-type": mime[path.extname(candidate).toLowerCase()] || "application/octet-stream",
    "cache-control": "no-store"
  });
  if (path.extname(candidate).toLowerCase() === ".html" && requestUrl.searchParams.get("qa") === "1") {
    const source = fs.readFileSync(candidate, "utf8");
    response.end(source.replace(/<\/body>/i, qaClient + "\n</body>"));
    return;
  }
  fs.createReadStream(candidate).pipe(response);
});

async function runWithPlaywright(playwright, baseUrl) {
  const browser = await playwright.chromium.launch({
    executablePath: browserPath,
    headless: true
  });
  const reports = [];
  try {
    for (const viewport of [[1920, 1080], [1366, 768]]) {
      const width = viewport[0];
      const height = viewport[1];
      const context = await browser.newContext({ viewport: { width: width, height: height } });
      const page = await context.newPage();
      const runtimeErrors = [];
      page.on("pageerror", function (error) {
        runtimeErrors.push("pageerror: " + error.message);
      });
      page.on("console", function (message) {
        if (message.type() === "error" && !message.text().startsWith("Failed to load resource:")) {
          runtimeErrors.push("console: " + message.text());
        }
      });
      await page.goto(baseUrl + "&viewport=" + width + "x" + height, { waitUntil: "networkidle" });
      await page.waitForSelector("#qa-result", { state: "attached", timeout: 10000 });
      const encoded = await page.getAttribute("#qa-result", "data-json");
      if (!encoded) {
        throw new Error("Deck emitted empty QA data at " + width + "x" + height + ".");
      }
      const report = JSON.parse(decodeURIComponent(encoded));
      report.runtimeErrors = runtimeErrors;
      reports.push(report);
      await context.close();
    }
  } finally {
    await browser.close();
  }
  return reports;
}

function runWithBrowserCli(baseUrl) {
  const reports = [];
  for (const viewport of [[1920, 1080], [1366, 768]]) {
    const width = viewport[0];
    const height = viewport[1];
    const profile = fs.mkdtempSync(path.join(os.tmpdir(), "zhongguose-browser-qa-"));
    try {
      const result = spawnSync(browserPath, [
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-scrollbars",
        "--user-data-dir=" + profile,
        "--window-size=" + width + "," + height,
        "--virtual-time-budget=2500",
        "--dump-dom",
        baseUrl + "&viewport=" + width + "x" + height
      ], {
        encoding: "utf8",
        windowsHide: true,
        maxBuffer: 16 * 1024 * 1024
      });
      if (result.status !== 0) {
        throw new Error("Headless browser failed at " + width + "x" + height + ": " + (result.stderr || "unknown error"));
      }
      const match = result.stdout.match(/<meta id="qa-result" data-json="([^"]*)">/i);
      if (!match) {
        throw new Error("Deck did not emit QA data at " + width + "x" + height + ".");
      }
      const report = JSON.parse(decodeURIComponent(match[1]));
      report.runtimeErrors = [];
      reports.push(report);
    } finally {
      fs.rmSync(profile, { recursive: true, force: true });
    }
  }
  return reports;
}

server.listen(0, "127.0.0.1", async function () {
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : 0;
  const baseUrl = "http://127.0.0.1:" + port + "/" + encodeURIComponent(path.basename(indexFile)) + "?qa=1";
  const playwright = loadPlaywright();
  let reports;

  try {
    reports = playwright
      ? await runWithPlaywright(playwright, baseUrl)
      : runWithBrowserCli(baseUrl);
  } catch (error) {
    console.error("Browser QA failed: " + error.message);
    server.close(function () { process.exit(1); });
    return;
  }

  let failed = missingRequests.length > 0;
  for (const report of reports) {
    console.log(report.viewport + ": slides=" + report.slideCount + ", issues=" + report.issues.length + ", coverFont=" + report.coverFontLoaded + ", runtimeErrors=" + report.runtimeErrors.length);
    for (const issue of report.issues) {
      console.error("- slide " + issue.slide + ": " + issue.kind + " (" + issue.detail + ")");
    }
    for (const runtimeError of report.runtimeErrors) {
      console.error("- " + report.viewport + ": " + runtimeError);
    }
    if (!report.coverFontLoaded || report.issues.length > 0 || report.runtimeErrors.length > 0) {
      failed = true;
    }
  }
  if (missingRequests.length > 0) {
    console.error("Missing HTTP resources: " + [...new Set(missingRequests)].join(", "));
  }

  server.close(function () {
    if (failed) {
      process.exit(1);
    }
    console.log("Browser QA passed at 1920x1080 and 1366x768.");
  });
});
