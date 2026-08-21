---
description: Pixelmatch's strict same-dimension requirement — causes, failure behavior, and how to handle size variation before calling pixelmatch.
tldr: Pixelmatch requires both buffers to be identical dimensions — it has no resize, pad, or align logic. The API throws and the CLI exits 65, but Playwright pads both images and fails regardless of tolerance — no threshold, maxDiffPixels, or maxDiffPixelRatio can absorb a size change. Fix capture conditions so images match natively; resizing introduces interpolation artifacts that produce false diffs.
---

# Pixelmatch Same-Size Constraint

## When to Use

> Use this when the two images you want to diff have different dimensions — or when preventing that situation.

## Decision

| Cause | Fix |
|---|---|
| Different viewport size between captures | Capture at the same viewport |
| **Content growth changes total page height** — the common one under `fullPage: true` | Cap what grows (a pager, an items-per-page limit) or capture a surface that does not embed an uncapped listing |
| Lazy-loaded content changes total page height | Force-load lazy content; use `fullPage: true` consistently |
| Zoom level / DPR difference | Pin `deviceScaleFactor` and `scale` |
| Genuinely different content sizes | Normalize before pixelmatch — resize or pad to a target size |

Under `fullPage: true` the image is as tall as the document — Playwright takes the largest of `body`/`documentElement` `scrollHeight`, `offsetHeight`, and `clientHeight` — so one new row in an uncapped listing changes the image height and every baseline for that surface stops comparing. Masking does not help: a mask paints over a region at its current size, it does not fix the size.

## Pattern: resize to common size

```js
import sharp from 'sharp';

const target = { width: 1440, height: 900 };

const img1 = await sharp('img1.png').resize(target).raw().toBuffer({ resolveWithObject: true });
const img2 = await sharp('img2.png').resize(target).raw().toBuffer({ resolveWithObject: true });

const diff = Buffer.alloc(target.width * target.height * 4);
pixelmatch(img1.data, img2.data, diff, target.width, target.height, { threshold: 0.1 });
```

Note: resizing introduces interpolation; the diff result is no longer pixel-faithful. Prefer fixing the capture so dimensions match natively.

## Behavior on Mismatch

| Caller | Behavior |
|---|---|
| CLI | Prints `Image dimensions do not match: WxH vs WxH` and exits `65` — no diff written |
| API | Throws `Error('Image sizes do not match. Image 1 size: …, image 2 size: …')` — no diff written |
| Playwright `toHaveScreenshot()` | Pads both images to the larger of the two sizes, runs the diff, writes a diff PNG — and fails **regardless of tolerance** |

**No tolerance applies to a size change.** Playwright reports the size mismatch unconditionally, alongside any pixel mismatch, so `threshold`, `maxDiffPixels`, and `maxDiffPixelRatio` have no bearing on the outcome — a reader who has just tuned a tolerance will otherwise not understand why it did nothing. The diff PNG it writes is not much help either: the shorter image is padded with transparent black, so the whole extra height shows as difference. It tells you the page grew, not what changed.

## Common Mistakes

- **Wrong**: Resizing to a smaller-than-source dimension and expecting precise diffs — interpolation creates artifacts that pixelmatch interprets as differences
- **Wrong**: Trying to diff against a screenshot that grew because of new content — the diff is meaningless; the test should fail at the capture stage
- **Wrong**: Padding with arbitrary color where only one image is padded — the padded region adds artificial diff signal
- **Wrong**: Raising a tolerance to get past a size mismatch — it cannot work; the size error is reported regardless of every tolerance key

## See Also

- [Reading PNGs](pixelmatch-reading-pngs.md) — how to decode images with sharp for resizing
- [Standalone Use](pixelmatch-standalone.md) — includes a dimension-mismatch guard example
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
