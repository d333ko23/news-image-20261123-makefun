// Entry runner for news-image-20261123.
//
// The finished artwork is entry.png, drawn by draw_image.py and committed
// next to this file. The harness gives us a writable directory through
// MAKEFUN_OUTPUT_DIR (falling back to /output); our whole job is to place
// an exact copy of the artwork there. Node 22 standard library only, no
// network, no third-party packages.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const artwork = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const destination = join(outDir, "entry.png");

const bytes = readFileSync(artwork);
if (bytes.length === 0 || bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, expected 1..1048576`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(artwork, destination);

const delivered = readFileSync(destination);
if (!delivered.equals(bytes)) {
  throw new Error("delivered entry.png differs from the artwork in this repo");
}
console.log(`entry.png -> ${destination} (${bytes.length} bytes)`);
