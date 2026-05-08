---
description: How to load PNG files into pixelmatch's required RGBA buffer format using pngjs or sharp.
tldr: Use pngjs as the default PNG decoder — PNG.sync.read() returns an object with a .data RGBA Buffer that pixelmatch expects directly. For multi-format support (JPEG, WebP) or faster processing, use sharp with .raw().ensureAlpha() to guarantee the RGBA channel order.
---

# Reading PNGs into Pixelmatch

## When to Use

> Use this when loading PNG (or other image) files into the RGBA buffer format pixelmatch requires.

## Decision

| Decoder | When |
|---|---|
| `pngjs` | Default — battle-tested, sync API, ships with pixelmatch examples |
| `sharp` | Multi-format support (JPEG, WebP, etc.), faster, native bindings |
| Browser `Canvas` API | Browser-side comparisons (`ctx.getImageData()`) |

## Pattern: pngjs canonical snippet

```js
import fs from 'fs';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

const img1 = PNG.sync.read(fs.readFileSync('img1.png'));
const img2 = PNG.sync.read(fs.readFileSync('img2.png'));
const { width, height } = img1;
const diff = new PNG({ width, height });

pixelmatch(img1.data, img2.data, diff.data, width, height, { threshold: 0.1 });

fs.writeFileSync('diff.png', PNG.sync.write(diff));
```

```bash
npm install pngjs pixelmatch
```

## Pattern: with sharp (multi-format)

```js
import sharp from 'sharp';
import pixelmatch from 'pixelmatch';

const img1 = await sharp('img1.jpg').raw().ensureAlpha().toBuffer({ resolveWithObject: true });
const img2 = await sharp('img2.jpg').raw().ensureAlpha().toBuffer({ resolveWithObject: true });

const diff = Buffer.alloc(img1.info.width * img1.info.height * 4);
const diffCount = pixelmatch(
  img1.data, img2.data, diff,
  img1.info.width, img1.info.height,
  { threshold: 0.1 },
);
```

## Common Mistakes

- **Wrong**: Forgetting `.ensureAlpha()` with sharp — produces RGB output; pixelmatch needs RGBA
- **Wrong**: Mixing decoders between `img1` and `img2` — possible buffer alignment differences; stick to one
- **Wrong**: Passing raw PNG file bytes to pixelmatch — must decode first; `PNG.sync.read()` handles that

## See Also

- [API](pixelmatch-api.md) — the pixelmatch function signature and parameter types
- [Same-Size Constraint](pixelmatch-same-size.md) — handling dimension mismatches before calling pixelmatch
- Reference: [pngjs on npm](https://www.npmjs.com/package/pngjs)
