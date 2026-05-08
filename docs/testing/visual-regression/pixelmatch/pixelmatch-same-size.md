---
description: Pixelmatch's strict same-dimension requirement — causes, failure behavior, and how to handle size variation before calling pixelmatch.
tldr: Pixelmatch requires both buffers to be identical dimensions — it has no resize, pad, or align logic. The API throws, the CLI exits 65, and Playwright fails the assertion outright. Fix capture conditions so images match natively; resizing introduces interpolation artifacts that produce false diffs.
---

# Pixelmatch Same-Size Constraint

## When to Use

> Use this when the two images you want to diff have different dimensions — or when preventing that situation.

## Decision

| Cause | Fix |
|---|---|
| Different viewport size between captures | Capture at the same viewport |
| Lazy-loaded content changes total page height | Force-load lazy content; use `fullPage: true` consistently |
| Zoom level / DPR difference | Pin `deviceScaleFactor` and `scale` |
| Genuinely different content sizes | Normalize before pixelmatch — resize or pad to a target size |

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
| CLI | Exits `65` |
| API | Throws `Error('Image sizes do not match.')` |
| Playwright `toHaveScreenshot()` | Fails the assertion outright — no normalization |

## Common Mistakes

- **Wrong**: Resizing to a smaller-than-source dimension and expecting precise diffs — interpolation creates artifacts that pixelmatch interprets as differences
- **Wrong**: Trying to diff against a screenshot that grew because of new content — the diff is meaningless; the test should fail at the capture stage
- **Wrong**: Padding with arbitrary color where only one image is padded — the padded region adds artificial diff signal

## See Also

- [Reading PNGs](pixelmatch-reading-pngs.md) — how to decode images with sharp for resizing
- [Standalone Use](pixelmatch-standalone.md) — includes a dimension-mismatch guard example
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
