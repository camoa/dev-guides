---
description: Pixelmatch Node.js API — signature, parameter types, return value, and patterns for full diff output and count-only mode.
tldr: Call pixelmatch(img1, img2, output, width, height, options) with decoded RGBA Uint8Array buffers — not PNG file bytes. Pass null as output for count-only mode. Returns an integer count of mismatched pixels.
---

# Pixelmatch API

## When to Use

> Use this when calling pixelmatch from Node code — reference for the function signature and parameter types.

## Decision

| Need | Approach |
|---|---|
| Full diff with visualization PNG | Pass RGBA output buffer as third argument |
| Count only, no diff image | Pass `null` as output |
| Count as percentage | `diffCount / (width * height)` |

## Pattern

```js
import pixelmatch from 'pixelmatch';

const diffCount = pixelmatch(
  img1.data,    // RGBA buffer
  img2.data,    // RGBA buffer
  diff.data,    // RGBA buffer (output) — or null for count-only
  width,
  height,
  { threshold: 0.1 },
);

console.log(`${diffCount} pixels differ`);
```

## Signature

```js
pixelmatch(img1, img2, output, width, height[, options]) → Number
```

| Param | Type | Description |
|---|---|---|
| `img1`, `img2` | `Buffer \| Uint8Array \| Uint8ClampedArray` | RGBA pixel buffers, length `width × height × 4`. Channel order: R, G, B, A |
| `output` | Same as above, or `null` | Same-size RGBA buffer where pixelmatch writes the diff PNG. Pass `null` for count-only |
| `width`, `height` | `number` | Shared dimensions of all three buffers |
| `options` | `object` | Optional — threshold, includeAA, alpha, diffColor, etc. |

## Common Mistakes

- **Wrong**: Passing PNG file paths or raw `Buffer` of PNG bytes — pixelmatch needs decoded RGBA pixels; PNG bytes give garbage results
- **Wrong**: Mismatched channel order (RGB vs RGBA) — pixelmatch always expects RGBA; convert RGB to RGBA first
- **Wrong**: Wrong buffer length — must be `width × height × 4`; runtime error or silently wrong results

## See Also

- [Reading PNGs](pixelmatch-reading-pngs.md) — how to decode PNG files into the RGBA buffers pixelmatch needs
- [Other Options](pixelmatch-other-options.md) — full options reference
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
