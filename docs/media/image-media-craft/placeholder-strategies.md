---
description: Show placeholders while images load — CLS prevention, LQIP blur-up, ThumbHash, skeleton shimmer, and dominant color patterns
tldr: "Use `width`/`height` attributes on every image to prevent CLS — this is non-negotiable. Add LQIP blur-up for editorial photos where perceived performance matters."
---

# Placeholder Strategies

## When to Use

> You need to show something while a large image loads — to prevent CLS, improve perceived performance, or provide visual feedback. Choose based on context: content images in editorial layouts need CLS prevention; hero images benefit from visual richness during load; lazy-loaded cards need skeleton states.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Prevent CLS with minimal complexity | `width`/`height` + `aspect-ratio` CSS | Browser reserves space; no JS or extra images |
| Smooth blur-up reveal (full quality image replaces blurred thumb) | LQIP (base64 inline + JS swap) | Best perceived performance for photos |
| Compact visual placeholder with color fidelity | ThumbHash | Smaller than LQIP; supports transparency; needs JS decode |
| Purely CSS skeleton for image grids/cards | CSS shimmer animation | No extra requests; works before image URL is known |
| Dominant color background | Single-pixel dominant color | Simplest, no JS; 1 extra request (or inline as base64) |

## Preventing CLS — The Non-Negotiable Foundation

Every image needs reserved space before it loads. Two ways:

**Option 1: `width` and `height` attributes** (always do this):
```html
<!-- Browser computes aspect-ratio from these; CSS can still make it responsive -->
<img src="photo.jpg" width="800" height="600" alt="...">
```
```css
img { width: 100%; height: auto; } /* Responsive, but aspect-ratio preserved */
```

**Option 2: `aspect-ratio` CSS** (when you don't know the exact dimensions):
```css
.image-wrapper {
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #f0f0f0; /* Placeholder color while loading */
}
.image-wrapper img { width: 100%; height: 100%; object-fit: cover; }
```

Both approaches prevent layout shift. Use both together for maximum reliability.

## LQIP / Blur-Up Pattern

Tiny (< 1KB) base64-encoded blurred image is inlined in HTML. JavaScript loads the full image and swaps it in on load, transitioning with CSS.

```html
<div class="img-wrapper" style="background-color: #a3b2c1;">
  <img
    class="img-lqip"
    src="data:image/jpeg;base64,/9j/4AAQSkZJRgAB..."
    data-src="photo-full.jpg"
    alt="Mountain landscape"
    width="800"
    height="600"
    loading="lazy"
  >
</div>
```
```css
.img-lqip {
  filter: blur(8px);
  transition: filter 0.4s ease;
  transform: scale(1.05); /* Prevent blur edges showing */
}
.img-lqip.loaded { filter: blur(0); transform: scale(1); }
```
```js
const imgs = document.querySelectorAll('[data-src]');
imgs.forEach(img => {
  const full = new Image();
  full.onload = () => { img.src = img.dataset.src; img.classList.add('loaded'); };
  full.src = img.dataset.src;
});
```

Generate LQIP thumbnails at build time using Sharp: `sharp(input).resize(20).blur(2).toBuffer()` then base64-encode.

## ThumbHash / BlurHash

Compact hash string (~30 chars for ThumbHash) encodes a visual approximation of the image. Decoded client-side to a canvas/data URI used as placeholder.

- **ThumbHash** is preferred over BlurHash: smaller hash, supports alpha channel, encodes more detail
- Both require JavaScript to decode (no native browser support)
- Ideal for: image galleries, lazy-loaded content feeds, generated at CMS upload time

```html
<!-- ThumbHash placeholder: hash decoded to data URI in JS, used as src -->
<img data-thumbhash="3OcRJYB4d3h/iIeHeEh3..." data-src="photo.jpg" alt="..." width="800" height="600">
```

## Skeleton Placeholder

Use when the image URL or dimensions aren't known yet, or for consistency with skeleton UI patterns.

```css
.skeleton-image {
  background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  aspect-ratio: 16 / 9;
  border-radius: 4px;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
```

Cross-reference: `css-craft.md` → `skeleton-and-loading-states` for full shimmer animation patterns.

## Common Mistakes

- Using LQIP without `width`/`height` attributes — the placeholder prevents CLS but only if space is reserved first
- Inlining large LQIP thumbnails (> 2KB base64) — defeats the purpose; keep LQIP under 20px wide, heavily blurred
- ThumbHash/BlurHash without fallback — requires JS; always have `width`/`height` + background-color as baseline
- Skeleton aspect-ratio not matching actual image — creates a visible layout jump when image loads
- Animating `width`/`height` for the blur-up transition — use `filter` and `opacity` which are GPU-composited

## See Also

- [Loading and Decode Craft](loading-and-decode-craft.md) — `loading="lazy"` pairs with LQIP patterns
- [Image Effects Craft](image-effects-craft.md) — reveal animations for when images load
- Reference: `css-craft.md` → `skeleton-and-loading-states`
- Reference: [Mux: Blurry image placeholders on the web](https://www.mux.com/blog/blurry-image-placeholders-on-the-web)
- Reference: [ThumbHash GitHub](https://github.com/evanw/thumbhash)
