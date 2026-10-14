#!/usr/bin/env node
/* Short alias for html_to_editable_pptx.js. */

const path = require("path");
const { spawnSync } = require("child_process");

function usage() {
  console.log(`Usage:
  html_to_ppt.js --input <file-or-url> --out-dir <dir> [options]

This is a short alias for html_to_editable_pptx.js. It forwards all options.
Run with --help-converter to see the full converter help.
`);
}

const args = process.argv.slice(2);
if (args.includes("--help") || args.includes("-h")) {
  usage();
  process.exit(0);
}

const forwarded = args.filter((arg) => arg !== "--help-converter");
if (args.includes("--help-converter")) forwarded.push("--help");

const converter = path.join(__dirname, "html_to_editable_pptx.js");
const result = spawnSync(process.execPath, [converter, ...forwarded], {
  stdio: "inherit",
  env: process.env,
});

if (result.error) {
  console.error(result.error.stack || result.error.message || String(result.error));
  process.exit(1);
}

process.exit(result.status == null ? 1 : result.status);
