---
description: Set loading, decoding, and fetchpriority correctly for LCP and below-fold images — the right combination per image position
tldr: "Use `fetchpriority=\"high\"` on the one LCP image. Use `loading=\"lazy\"` + `decoding=\"async\"` on all below-fold images."
---

# Loading and Decode Craft

## When to Use

> Every `<img>` element needs deliberate loading attributes. The wrong combination kills LCP scores. This section defines exactly which attributes to apply and when, from above-fold hero images through below-fold content.

## Decision

| Image position | `loading` | `decoding` | `fetchpriority` | Notes |
|---|---|---|---|---|
| LCP image (hero, first visible) | omit (default eager) | `async` | `high` | Never lazy-load LCP |
| Above fold, not LCP | omit (default eager) | `async` | omit | Let browser schedule normally |
| Below fold, non-critical | `lazy` | `async` | omit | Defers until 1250px away (4G) |
| Background/decorative image | `lazy` | `async` | omit | Or use CSS `background-image` instead |

**The rule**: `loading="lazy"` and `fetchpriority="high"` are mutually exclusive in intent — never use them together on the same element.

## LCP Optimization Strategy

The LCP target is 2.5 seconds or less for 75% of page visits. For image-based LCP elements:

1. **Make the image discoverable in initial HTML** — not injected by JavaScript after page load. Preloaders cannot find dynamically-injected LCP images.

2. **Add `fetchpriority="high"`** to the LCP `<img>`. This moves the image from low-priority discovery to high-priority fetch, improving LCP by 0.5–2 seconds in real-world tests.

3. **Preload the LCP image** in `<head>` for critical hero images that are in CSS or lazy-loaded by frameworks:
```html
<link rel="preload" as="image"
  href="hero-1280.webp"
  imagesrcset="hero-640.webp 640w, hero-1280.webp 1280w, hero-1920.webp 1920w"
  imagesizes="(max-width: 640px) 100vw, (max-width: 1280px) 80vw, 1200px"
>
```

4. **Serve from the same origin or fast CDN** — cross-origin image requests block LCP.

## Above-Fold Image Checklist

For any image visible without scrolling:
```html
<img
  src="hero-1280.jpg"
  srcset="hero-640.jpg 640w, hero-1280.jpg 1280w, hero-1920.jpg 1920w"
  sizes="(max-width: 640px) 100vw, 80vw"
  alt="Descriptive text"
  width="1280"
  height="720"
  decoding="async"
  fetchpriority="high"
>
<!-- No loading attribute — defaults to eager -->
```

## Native Lazy Loading vs IntersectionObserver

| Approach | When to Use | Trade-off |
|---|---|---|
| `loading="lazy"` (native) | All new projects | No JS; threshold not configurable (1250px on 4G) |
| IntersectionObserver (JS) | Custom threshold control needed; legacy browser support | JS required; more control over load trigger distance |
| JavaScript lazy library | Complex lazy loading with placeholders and effects | Most overhead; only when native is insufficient |

In 2025, native `loading="lazy"` covers all modern browsers (Chrome 77+, Safari 15.4+, Firefox 75+). Use it by default. Only reach for JS-based solutions when you need custom behavior like blur-up transitions.

## `decoding="async"` — Always Use It

`decoding="async"` tells the browser to decode the image off the main thread, allowing other rendering work to continue. There is no downside for below-fold images. For above-fold images, it may delay the image appearing slightly but improves overall page responsiveness. Use it universally unless profiling shows a specific problem.

## Common Mistakes

- Lazy-loading the LCP image — this is the most common LCP killer; Lighthouse 2024 flags it explicitly
- Adding `fetchpriority="high"` to multiple images — it loses meaning; only apply to the one true LCP image
- Using `loading="lazy"` on images inside carousels where the first slide is visible — the first slide is above-fold
- Omitting `width` and `height` attributes — lazy-loaded images without dimensions cause CLS when they load
- Relying on JavaScript lazy loading when native is available — adds unnecessary JS weight

## See Also

- [Placeholder Strategies](placeholder-strategies.md) — how to show something while the image loads
- [Responsive Images Craft](responsive-images-craft.md) — `srcset`/`sizes` to go with these attributes
- Reference: [web.dev browser-level image lazy loading](https://web.dev/articles/browser-level-image-lazy-loading)
- Reference: [web.dev Optimize LCP](https://web.dev/articles/optimize-lcp)
- Reference: [MDN Fix Image LCP](https://developer.mozilla.org/en-US/blog/fix-image-lcp/)
