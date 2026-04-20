---
description: Set loading, decoding, and fetchpriority correctly for LCP and below-fold images — the right combination per image position
tldr: "Use `fetchpriority=\"high\"` on the one LCP image. Use `loading=\"lazy\"` + `decoding=\"async\"` on all below-fold images."
---

# Loading and Decode Craft

## When to Use

> Use `fetchpriority="high"` on the one LCP image. Use `loading="lazy"` + `decoding="async"` on all below-fold images. Never combine `loading="lazy"` and `fetchpriority="high"` on the same element.

## Decision

| Image position | `loading` | `decoding` | `fetchpriority` | Notes |
|---|---|---|---|---|
| LCP image (hero, first visible) | omit (default eager) | `async` | `high` | Never lazy-load LCP |
| Above fold, not LCP | omit (default eager) | `async` | omit | Let browser schedule normally |
| Below fold, non-critical | `lazy` | `async` | omit | Defers until ~1250px away |
| Background/decorative image | `lazy` | `async` | omit | Or use CSS `background-image` instead |

## Pattern

**Above-fold LCP image checklist**:
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

**Preload for LCP images in CSS or injected by JS**:
```html
<link rel="preload" as="image"
  href="hero-1280.webp"
  imagesrcset="hero-640.webp 640w, hero-1280.webp 1280w, hero-1920.webp 1920w"
  imagesizes="(max-width: 640px) 100vw, (max-width: 1280px) 80vw, 1200px"
>
```

**LCP optimization steps**:
1. Make the image discoverable in initial HTML — not JS-injected
2. Add `fetchpriority="high"` to the one LCP `<img>` (0.5–2s improvement in real-world tests)
3. Preload via `<link rel="preload">` if image is in CSS or lazy-loaded by frameworks
4. Serve from same origin or fast CDN — cross-origin requests block LCP

**Native lazy loading vs IntersectionObserver**:

| Approach | When to Use | Trade-off |
|---|---|---|
| `loading="lazy"` (native) | All new projects | No JS; threshold not configurable |
| IntersectionObserver | Custom threshold or placeholder transitions needed | JS required; more control |

Native `loading="lazy"` covers all modern browsers (Chrome 77+, Safari 15.4+, Firefox 75+). Use by default.

## Common Mistakes

- **Wrong**: lazy-loading the LCP image → **Right**: this is the most common LCP killer; Lighthouse 2024 flags it explicitly
- **Wrong**: `fetchpriority="high"` on multiple images → **Right**: only apply to the one true LCP image; it loses meaning when overused
- **Wrong**: `loading="lazy"` on the first carousel slide → **Right**: first slide is above fold; only lazy-load non-visible slides
- **Wrong**: omitting `width` and `height` on lazy-loaded images → **Right**: browser cannot reserve space; causes CLS when images load
- **Wrong**: JS lazy loading when native is available → **Right**: native adds zero JS weight

## See Also

- [Placeholder Strategies](placeholder-strategies.md) — what to show while the image loads
- [Responsive Images Craft](responsive-images-craft.md) — `srcset`/`sizes` to go with these attributes
- Reference: [web.dev browser-level image lazy loading](https://web.dev/articles/browser-level-image-lazy-loading)
- Reference: [web.dev Optimize LCP](https://web.dev/articles/optimize-lcp)
- Reference: [MDN Fix Image LCP](https://developer.mozilla.org/en-US/blog/fix-image-lcp/)
