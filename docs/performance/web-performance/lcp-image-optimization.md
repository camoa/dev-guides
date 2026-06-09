---
description: Maximize LCP score by setting fetchpriority, avoiding lazy-loading, and declaring width/height on all images.
tldr: Add `fetchpriority="high"` and remove `loading="lazy"` on the LCP image; always set `width`/`height` to prevent CLS; JS-rendered LCP elements add hundreds of ms — move them to server-rendered HTML.
---

# LCP Image Optimization

## When to Use

> Apply every time the LCP element is an image (hero image, product photo, background image). A single `fetchpriority="high"` combined with removing `loading="lazy"` is often the highest-ROI LCP fix available. Pair with `width`/`height` attributes to eliminate CLS.

## Decision

| Scenario | Pattern | Why |
|----------|---------|-----|
| Hero `<img>` directly in HTML | `fetchpriority="high"` + no `loading="lazy"` | Preload scanner discovers it immediately; fetchpriority elevates above other images |
| LCP is a CSS `background-image` | `<link rel="preload" as="image" fetchpriority="high">` | CSS background images are not discovered by the preload scanner |
| Multiple images above fold (carousel, grid) | Only LCP gets `fetchpriority="high"`; carousel slides get `fetchpriority="low"` | Carousel slides compete with LCP; explicitly demote them |
| LCP element rendered by JavaScript | Move to server-rendered HTML `<img>` | JS-rendered LCP adds HTML→JS parse→execute→fetch chain — hundreds of ms |
| Image format | `<picture>` with AVIF → WebP → JPEG/PNG fallback | AVIF typically 30–50% smaller than WebP |
| CLS from images | Always set `width` + `height` HTML attributes | Browser reserves space immediately before download |

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

<!-- For CSS background-image as LCP -->
<link rel="preload" href="/hero-bg.webp" as="image"
  imagesrcset="/hero-bg-400.webp 400w, /hero-bg-800.webp 800w"
  imagesizes="100vw"
  fetchpriority="high">
```

```css
/* CSS image-set() for pseudo-element icons — Baseline since 2023-09-18 */
.icon-button::before {
  content: image-set(
    url("icon.avif") type("image/avif") 1x,
    url("icon-2x.avif") type("image/avif") 2x,
    url("icon.webp") type("image/webp") 1x,
    url("icon.png") type("image/png") 1x
  );
}
```

## Common Mistakes

- **Wrong**: `loading="lazy"` on the LCP image → **Right**: Remove it; lazy-loading purposely delays fetch until layout completes — the single most common LCP regression
- **Wrong**: `fetchpriority="high"` combined with `loading="lazy"` → **Right**: Contradictory; lazy wins and overrides the priority boost
- **Wrong**: No `width`/`height` on lazy-loaded images → **Right**: Always set dimensions; missing values cause CLS as layout reflows when images load
- **Wrong**: Omitting `sizes` attribute with `srcset` → **Right**: Browser assumes `100vw` and downloads the largest available resolution on every device
- **Wrong**: Using deprecated `importance` attribute → **Right**: Always use `fetchpriority`

## See Also

- [Resource Hints](resource-hints.md) — preload for CSS background-image LCP
- [Core Web Vitals Overview](core-web-vitals-overview.md) — LCP thresholds
- Reference: [web.dev: Optimize LCP](https://web.dev/articles/optimize-lcp)
- Reference: [web.dev: Fetch Priority](https://web.dev/articles/fetch-priority)
