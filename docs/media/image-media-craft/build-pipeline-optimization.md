---
description: Set up automated image optimization with Sharp — tool selection, responsive image generation, compression budgets, and build-time vs CDN decision
tldr: "Use Sharp for any Node.js build pipeline — it is the default choice. Use CDN transforms (Cloudinary, imgix) for user-uploaded CMS media where image dimensions are unpredictable."
---

# Build Pipeline Optimization

## When to Use

> Use Sharp for any Node.js build pipeline — it is the default choice. Use CDN transforms (Cloudinary, imgix) for user-uploaded CMS media where image dimensions are unpredictable. Always generate multiple widths for `srcset`.

## Decision

| Tool | Best For | Speed | Output Formats |
|---|---|---|---|
| **Sharp** | Node.js build pipelines, CI/CD | Very fast (libvips) | JPEG, WebP, AVIF, PNG |
| **libvips** | Server-side, non-Node environments | Fastest | All formats |
| **ImageMagick** | Legacy pipelines, scripting | Slower | All formats |
| **Squoosh CLI** | Experimenting with quality thresholds | Slow | JPEG, WebP, AVIF, JXL |
| **Cloudinary** | CMS/on-demand, no build control | Real-time | Auto-format + transform |
| **imgix** | CDN-native transforms, URL-based | Real-time | Auto-format + transform |
| **Cloudflare Images** | Cloudflare stack | Real-time | Auto-format |

**Build-time vs CDN**:

| | Build-Time | Runtime (CDN) |
|---|---|---|
| When to use | Static site, known image set, CI pipeline | CMS uploads, user-generated content |
| Complexity | Higher setup, zero runtime cost | Low setup, ongoing cost |
| Control | Full quality/format control | URL-parameter control |

## Pattern

**Sharp responsive image generation**:
```js
import sharp from 'sharp';
const widths = [400, 640, 900, 1280, 1920];
const input = 'src/hero.jpg';

await Promise.all(widths.map(async (w) => {
  await sharp(input).resize(w).webp({ quality: 82 }).toFile(`dist/hero-${w}.webp`);
  await sharp(input).resize(w).avif({ quality: 68 }).toFile(`dist/hero-${w}.avif`);
  await sharp(input).resize(w).jpeg({ quality: 85, progressive: true }).toFile(`dist/hero-${w}.jpg`);
}));
```

**Compression budgets**:

| Image type | Target file size | Quality guidance |
|---|---|---|
| Hero / full-bleed (1920px) | < 250KB WebP / < 200KB AVIF | WebP 80–85, AVIF 65–70 |
| Card image (800px) | < 80KB WebP / < 60KB AVIF | WebP 75–80, AVIF 60–68 |
| Thumbnail (300px) | < 20KB WebP | WebP 65–75 |
| SVG icon | < 5KB | SVGO-optimized |
| Background video loop | < 3MB MP4, aim < 1.5MB | H.264, 720p–1080p |

**Progressive JPEG**: Use for images > 10KB. Sharp: `jpeg({ progressive: true })`. Progressive JPEGs are 5–15% smaller and display a blurry full image immediately.

**Audit tools**:
- **Lighthouse**: `Uses efficiently encoded images` audit catches images over 50KB savings potential
- **WebPageTest**: Waterfall view shows per-image load time
- **Squoosh** (browser): Compare compression settings visually before committing

## Common Mistakes

- **Wrong**: single-width image generation → **Right**: always generate multiple widths for `srcset`
- **Wrong**: AVIF quality above 75 → **Right**: at high quality AVIF files can exceed equivalent WebP; stay in the 60–72 range
- **Wrong**: ImageMagick when Sharp is available → **Right**: Sharp is 4–8x faster and uses less memory
- **Wrong**: no JPEG fallback in the pipeline → **Right**: always generate JPEG alongside WebP/AVIF; email and some RSS readers don't support `<picture>`
- **Wrong**: skipping progressive JPEG for above-fold images → **Right**: baseline shows a blank rectangle until fully downloaded; progressive shows blurry full image immediately

## See Also

- [Image Format Strategy](image-format-strategy.md) — quality targets and format selection rationale
- [Drupal Media Pipeline](drupal-media-pipeline.md) — how Drupal handles build-time vs runtime optimization
- Reference: [Sharp documentation](https://sharp.pixelplumbing.com/)
- Reference: [Addy Osmani's Essential Image Optimization](https://images.guide/)
- Reference: [Cloudinary Image Optimization docs](https://cloudinary.com/documentation/image_optimization)
