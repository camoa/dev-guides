---
description: Using pixelmatch in custom Node scripts outside Playwright — ad-hoc diff scripts, Puppeteer captures, and URL-vs-URL uptime checks.
tldr: Build standalone diff scripts with pngjs for PNG decoding and pixelmatch for the comparison. Always guard against dimension mismatches explicitly — pixelmatch throws. For Puppeteer or other captures, pin viewport and DPR consistently across baseline and current captures.
---

# Pixelmatch Standalone Use

## When to Use

> Use this when Playwright isn't the test runner — custom diff scripts, Puppeteer/Selenium captures, or CI uptime checks that compare a live URL against a stored reference.

## Decision

| Scenario | Pattern |
|---|---|
| Ad-hoc PNG diff from CLI args | Script with pngjs + pixelmatch |
| Non-Playwright captures (Puppeteer, Selenium) | Capture tool → pngjs decode → pixelmatch |
| URL-vs-URL change detection | Playwright launch (no test runner) → pngjs → pixelmatch |

## Pattern: ad-hoc PNG diff script

```js
// scripts/diff.mjs
import fs from 'node:fs';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

const [, , a, b, out = 'diff.png', thresholdArg = '0.1'] = process.argv;
const threshold = parseFloat(thresholdArg);

const img1 = PNG.sync.read(fs.readFileSync(a));
const img2 = PNG.sync.read(fs.readFileSync(b));
const { width, height } = img1;
const diff = new PNG({ width, height });

const count = pixelmatch(img1.data, img2.data, diff.data, width, height, { threshold });
fs.writeFileSync(out, PNG.sync.write(diff));

console.log(`${count} pixels differ (${(count / (width * height) * 100).toFixed(2)}%)`);
process.exit(count > 0 ? 66 : 0);
```

```bash
node scripts/diff.mjs baseline.png current.png diff.png 0.1
```

## Pattern: diff non-Playwright captures

```js
import puppeteer from 'puppeteer';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';
import fs from 'node:fs';

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto('https://example.com');
await page.screenshot({ path: 'current.png' });
await browser.close();

const baseline = PNG.sync.read(fs.readFileSync('baseline.png'));
const current = PNG.sync.read(fs.readFileSync('current.png'));
const diff = new PNG({ width: baseline.width, height: baseline.height });
const count = pixelmatch(
  baseline.data, current.data, diff.data,
  baseline.width, baseline.height,
  { threshold: 0.1 },
);
console.log(`Diff: ${count}px`);
```

## Common Mistakes

- **Wrong**: Ignoring the size-mismatch check — pixelmatch throws; guard it explicitly before calling
- **Wrong**: Capturing in one tool's defaults and diffing against another tool's defaults — different DPR and fonts cause baseline drift
- **Wrong**: Running captures on different machines — same problem as Playwright determinism; pin the environment

## See Also

- [Reading PNGs](pixelmatch-reading-pngs.md) — pngjs and sharp decoder patterns
- [Same-Size Constraint](pixelmatch-same-size.md) — handling dimension mismatches
- [CLI](pixelmatch-cli.md) — shell-script diffing without writing Node
