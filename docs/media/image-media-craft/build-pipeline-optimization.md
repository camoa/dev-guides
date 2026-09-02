---
description: Set up automated image optimization with Sharp — tool selection, responsive image generation, compression budgets, and build-time vs CDN decision
tldr: "Use Sharp for any Node.js build pipeline — it is the default choice. Use CDN transforms (Cloudinary, imgix) for user-uploaded CMS media where image dimensions are unpredictable."
---

# Build Pipeline Optimization

## When to Use

> Setting up automated image optimization for a project: choosing tools, defining compression targets, integrating into a build process, and deciding between build-time vs runtime/CDN transforms.

## Tool Decision

| Tool | Best For | Speed | Output Formats | Notes |
|---|---|---|---|---|
| **Sharp** | Node.js build pipelines, CI/CD | Very fast (libvips) | JPEG, WebP, AVIF, PNG, TIFF | De facto standard for Node |
| **libvips** | Server-side, non-Node environments | Fastest | All formats | Sharp is built on it |
| **ImageMagick** | Legacy pipelines, scripting | Slower (process per image) | All formats | Use when already in stack; Sharp preferred |
| **Squoosh CLI** | Experiment with compression settings | Slow | JPEG, WebP, AVIF, JXL | Best for finding quality thresholds |
| **Cloudinary** | CMS/on-demand, no build control | Real-time | Auto-format + transform | SaaS cost; zero build config |
| **imgix** | CDN-native transforms, URL-based | Real-time | Auto-format + transform | SaaS cost; powerful URL API |
| **Cloudflare Images** | Cloudflare stack | Real-time | Auto-format | Cheapest CDN option |

**Sharp is the default choice** for Node-based build pipelines (Vite, webpack, custom scripts). 150M+ npm downloads/month (2024); recommended by AWS Lambda and Google Cloud Functions.

## Responsive Image Generation with Sharp

```js
import sharp from 'sharp';
const widths = [400, 640, 900, 1280, 1920];
const input = 'src/hero.jpg';

await Promise.all(widths.map(async (w) => {
  // WebP
  await sharp(input).resize(w).webp({ quality: 82 }).toFile(`dist/hero-${w}.webp`);
  // AVIF (parallel encoding for speed)
  await sharp(input).resize(w).avif({ quality: 68 }).toFile(`dist/hero-${w}.avif`);
  // JPEG fallback
  await sharp(input).resize(w).jpeg({ quality: 85, progressive: true }).toFile(`dist/hero-${w}.jpg`);
}));
```

## Compression Budgets

| Image type | Target file size | Quality guidance |
|---|---|---|
| Hero / full-bleed (1920px) | < 250KB WebP / < 200KB AVIF | WebP 80–85, AVIF 65–70 |
| Card image (800px) | < 80KB WebP / < 60KB AVIF | WebP 75–80, AVIF 60–68 |
| Thumbnail (300px) | < 20KB WebP | WebP 65–75 |
| SVG icon | < 5KB | SVGO-optimized |
| Animated video (background loop) | < 3MB MP4, aim < 1.5MB | H.264, 720p–1080p |

**Run Lighthouse image audits** (`Uses efficiently encoded images`, `Uses next-gen formats`) to find files over budget. WebPageTest's image analysis waterfall shows per-image load time contribution.

## Build-Time vs Runtime Optimization

| Approach | Build-Time | Runtime (CDN) |
|---|---|---|
| When to use | Static site, known image set, CI pipeline available | CMS uploads, user-generated content, unknown image set |
| Complexity | Higher setup, zero runtime cost | Low setup, ongoing cost |
| Control | Full quality/format control | URL-parameter control |
| Cost | Zero serving cost | Per-transform or per-bandwidth pricing |
| Cache | Committed to repo or CDN | CDN cache with TTL |

**Recommendation**: Use build-time for editorial/designed images. Use CDN transforms (Cloudinary/imgix) for user-uploaded CMS media where image dimensions are unpredictable.

## Progressive JPEG vs Baseline

**Use progressive JPEG** for images > 10KB. Progressive JPEGs:
- Display a blurry full image almost immediately, then sharpen on decode
- Are 5–15% smaller than equivalent baseline JPEG
- Pair naturally with LQIP patterns (viewer sees something early)

Set in Sharp: `jpeg({ progressive: true })` or in Cloudinary with `fl_progressive`.

**Baseline JPEG**: Only use for images < 10KB where decode time difference is imperceptible.

## Audit Tools

- **Lighthouse** (Chrome DevTools): `Uses efficiently encoded images` audit catches images over 50KB savings potential
- **WebPageTest** (`webpagetest.org`): Waterfall view shows per-image load time; image optimization grade
- **Squoosh** (browser): Compare compression settings visually before committing to a quality value

## Common Mistakes

- Single-width image generation — always generate multiple widths for `srcset`; browsers cannot downscale properly without the variants
- AVIF quality above 75 — at high quality, AVIF files can exceed equivalent WebP; stay in the 60–72 range
- Using ImageMagick when Sharp is available — Sharp is 4–8x faster and uses less memory
- No JPEG fallback in the pipeline — always generate JPEG alongside WebP/AVIF; not all environments support `<picture>` (email, some RSS readers)
- Skipping progressive JPEG for above-fold images — baseline images show a blank rectangle until fully downloaded; progressive shows a blurry full image immediately

## See Also

- [Image Format Strategy](image-format-strategy.md) — quality targets and format selection rationale
- [Drupal Media Pipeline](drupal-media-pipeline.md) — how Drupal handles build-time vs runtime optimization
- Reference: [Sharp documentation](https://sharp.pixelplumbing.com/)
- Reference: [Addy Osmani's Essential Image Optimization](https://images.guide/)
- Reference: [Cloudinary Image Optimization docs](https://cloudinary.com/documentation/image_optimization)
