---
description: Choose between picture, srcset, and sizes for responsive images — resolution switching vs art direction, breakpoint strategy, and sizes calculation
tldr: "Use `srcset`+`sizes` on `<img>` when serving the same crop at different sizes. Use `<picture>` with `<source media>` when you need different crops or compositions per breakpoint (art direction)."
---

# Responsive Images Craft

## When to Use

> You need to serve correctly-sized images for different viewports, pixel densities, or art directions. This section covers the full HTML machinery — when to use `<picture>`, `srcset`, and `sizes`, and how to choose image-specific breakpoints.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Same image, different resolutions (1x/2x) | `srcset` with density descriptors (`1x`, `2x`) | Browser picks density match; no math needed |
| Same image, different widths for different viewports | `srcset` with width descriptors (`400w`, `800w`) + `sizes` | Browser picks best width match based on `sizes` hint |
| Completely different crops or compositions per breakpoint | `<picture>` + `<source media="...">` | Forces specific image at specific breakpoint; art direction |
| Format fallback (AVIF → WebP → JPEG) | `<picture>` + `<source type="...">` | Browser picks first supported format |
| Art direction AND format fallback | `<picture>` with both `type` and `media` on `<source>` | Combine both axes |

## Image Breakpoint Strategy

Image breakpoints are **not** the same as CSS layout breakpoints. Choose image breakpoints based on **file size jumps**, not layout changes.

The goal: no image should be more than ~20KB larger than the next smaller variant. Use a responsive breakpoints generator tool or this heuristic:
- Start with your maximum width (e.g., 1920px)
- Work down by ~30% steps: 1920 → 1280 → 900 → 600 → 400
- For hero images: 2560, 1920, 1280, 900, 640
- For card grids: 800, 600, 400, 300
- For thumbnails: 200, 100 (often just one image style suffices)

## Pattern

**Resolution switching** (most common — same crop, different sizes):
```html
<img
  srcset="hero-640.jpg 640w, hero-1280.jpg 1280w, hero-1920.jpg 1920w"
  sizes="(max-width: 640px) 100vw, (max-width: 1280px) 80vw, 1200px"
  src="hero-1280.jpg"
  alt="Descriptive alt text"
  width="1280"
  height="720"
>
```

**Art direction** (different crop or composition per breakpoint):
```html
<picture>
  <source
    media="(max-width: 640px)"
    srcset="hero-mobile-640.jpg 640w, hero-mobile-1280.jpg 1280w"
    sizes="100vw"
  >
  <source
    media="(min-width: 641px)"
    srcset="hero-desktop-1280.jpg 1280w, hero-desktop-1920.jpg 1920w"
    sizes="(max-width: 1280px) 80vw, 1200px"
  >
  <img src="hero-desktop-1280.jpg" alt="..." width="1280" height="720">
</picture>
```

**`sizes` attribute calculation** — describes the image's rendered width at each viewport:
- `100vw` = full-width image
- `(max-width: 768px) 100vw, 50vw` = full-width on mobile, half-width on desktop
- `(max-width: 640px) calc(100vw - 32px), (max-width: 1024px) 50vw, 400px` = accounts for padding

The browser uses `sizes` combined with `srcset` widths to pick the best source. **`sizes` does not control layout** — CSS still controls layout. Mismatching `sizes` and CSS layout wastes bandwidth.

## Named Image Use Cases

The same-crop-different-sizes (`srcset`+`sizes`) vs different-crops-per-breakpoint (`<picture>`+`source media`) decision benefits from being captured **upstream** as a named typed declaration on the design system, not re-decided at every render site.

A design-system-level image atom declaration — `{ name, aspectRatio, maxWidth, purpose, formatPriority? }` — pre-resolves the mode for each use case:

| Declared atom (example) | aspectRatio behaviour | Mode this implies |
|---|---|---|
| `card_thumb` (fixed 4:3 across breakpoints) | Same crop everywhere | `srcset`+`sizes` on `<img>` |
| `hero_full` (16:9 desktop, 4:5 mobile) | Crop changes per breakpoint | `<picture>` + `<source media>` |
| `avatar` (1:1, fixed pixel size) | Same crop, fixed density | `srcset` with density descriptors |

Capturing the use case once at the atom layer means rendering code reads the declaration rather than re-deriving the decision from layout context. Downstream pipelines (CMS responsive image styles, `<picture>` markup generators) consume the same artifact deterministically. See [Atom Recognition — Media Atoms](../../design-systems/recognition/atom-recognition.md).

## Common Mistakes

- Using density descriptors (`2x`) for layout images — use width descriptors (`w`) instead; density descriptors are for fixed-size UI elements only
- Setting `sizes="100vw"` on a card that's actually 33vw on desktop — browser fetches 3x the needed image
- Omitting `width` and `height` attributes — browser cannot reserve space, causing Cumulative Layout Shift (CLS)
- Making image breakpoints match CSS layout breakpoints exactly — images often need more granular steps for file size efficiency
- Using `<picture>` for resolution switching — `srcset`+`sizes` on `<img>` is simpler and equally effective; `<picture>` is for art direction
- Re-deriving the `<picture>` vs `<img>` decision at every render site instead of reading it from a declared atom — the decision is a property of the use case, not the placement

## See Also

- [Atom Recognition — Media Atoms](../../design-systems/recognition/atom-recognition.md) — declare image use cases upstream as typed atoms
- [Image Format Strategy](image-format-strategy.md) — combine `<picture>` `type` sources with format fallbacks
- [Loading and Decode Craft](loading-and-decode-craft.md) — add `loading`, `fetchpriority` after choosing the right element
- [Drupal Media Pipeline](drupal-media-pipeline.md) — how Drupal generates these patterns via responsive image styles
- Reference: [MDN Responsive Images Guide](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images)
- Reference: [web.dev Responsive Images](https://web.dev/learn/design/responsive-images)
