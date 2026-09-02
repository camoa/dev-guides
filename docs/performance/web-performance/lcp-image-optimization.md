---
description: "Maximize LCP score by setting fetchpriority, avoiding lazy-loading, and declaring width/height on all images."
tldr: "Add `fetchpriority=\"high\"` and avoid `loading=\"lazy\"` on the LCP image; always set `width`/`height` to prevent CLS; JS-rendered LCP elements add hundreds of ms — move them to server-rendered HTML."
---

# LCP Image Optimization

## When to Use

> Apply every time the LCP element is an image (hero image, product photo, background image). A single `fetchpriority="high"` combined with avoiding `loading="lazy"` is often the highest-ROI LCP fix available. Pair with `width`/`height` attributes to eliminate CLS.

## Decision

| Scenario | Pattern | Why |
|----------|---------|-----|
| Hero `<img>` directly in HTML | `fetchpriority="high"` + no `loading="lazy"` | Browser's preload scanner discovers it immediately; fetchpriority elevates it above other images |
| LCP is a CSS `background-image` | `<link rel="preload" as="image" fetchpriority="high">` | CSS background images are not discovered by the preload scanner — force early fetch |
| Multiple images above the fold (carousel, grid) | Only LCP gets `fetchpriority="high"`; non-LCP above-fold carousel slides get `fetchpriority="low"` | Carousel slides not initially visible compete with LCP; explicitly demote them |
| LCP element rendered by JavaScript | Move to server-rendered HTML `<img>` | JS-rendered LCP introduces HTML→JS parse→execute→fetch chain; adds hundreds of ms |
| Image format | `<picture>` with AVIF → WebP → JPEG/PNG fallback | AVIF typically 30-50% smaller than WebP; use `<picture>` for format negotiation |
| CLS from images | Always set `width` + `height` HTML attributes | Browser computes aspect-ratio before download; reserves space immediately |

## Pattern

```html
<!-- LCP hero image: all required attributes in one place -->
<picture>
  <source type="image/avif"
    srcset="/hero-400.avif 400w, /hero-800.avif 800w, /hero-1200.avif 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  <source type="image/webp"
    srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">
  <img
    src="/hero-800.jpg"
    alt="Hero banner"
    width="800" height="450"
    fetchpriority="high"
    decoding="sync"
    loading="eager">
</picture>

<!-- Carousel: 2nd+ slides are above-fold but NOT the LCP -->
<img src="/slide-2.webp" alt="Slide 2"
  width="800" height="450"
  fetchpriority="low"
  loading="lazy">

<!-- All below-fold images: lazy only, no fetchpriority override -->
<img src="/product.webp" alt="Product" width="400" height="300" loading="lazy">
```

**For CSS background-image as LCP:**
```html
<link rel="preload" href="/hero-bg.webp" as="image"
  imagesrcset="/hero-bg-400.webp 400w, /hero-bg-800.webp 800w"
  imagesizes="100vw"
  fetchpriority="high">
```

## Resolution-Optimized Pseudo-Element Images

Use `image-set()` in CSS to serve format- and resolution-optimized images from pseudo-elements without extra DOM nodes. **Widely Available** (Baseline since 2023-09-18).

```css
/* Always order formats most-to-least optimized; browser stops at first supported */
.icon-button::before {
  content: image-set(
    url("icon.avif") type("image/avif") 1x,
    url("icon-2x.avif") type("image/avif") 2x,
    url("icon.webp") type("image/webp") 1x,
    url("icon-2x.webp") type("image/webp") 2x,
    url("icon.png") type("image/png") 1x
  );
}
/* Fallback: plain url() before image-set() for browsers without support */
```

## Common Mistakes

- `loading="lazy"` on the LCP image — purposely delays fetch until layout completes; this is the single most common LCP regression
- `fetchpriority="high"` combined with `loading="lazy"` — contradictory; lazy wins and overrides the priority boost
- No `width`/`height` on lazy-loaded images — causes CLS as layout reflows when images load
- Omitting `sizes` attribute with `srcset` — browser assumes `100vw` and downloads the largest available resolution on every device
- `fetchpriority="auto"` explicitly written — omit the attribute entirely for default behavior; `auto` is a no-op and clutters HTML
- Using deprecated `importance` attribute — never implemented consistently; always use `fetchpriority`

## See Also

- [Resource Hints](resource-hints.md) — preload for CSS background-image LCP
- [Core Web Vitals Overview](core-web-vitals-overview.md) — LCP thresholds
- Reference: [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)
- Reference: [web.dev: Fetch Priority](https://web.dev/articles/fetch-priority)
