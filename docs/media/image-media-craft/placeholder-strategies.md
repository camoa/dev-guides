---
description: Show placeholders while images load — CLS prevention, LQIP blur-up, ThumbHash, skeleton shimmer, and dominant color patterns
---

# Placeholder Strategies

## When to Use

> Use `width`/`height` attributes on every image to prevent CLS — this is non-negotiable. Add LQIP blur-up for editorial photos where perceived performance matters. Use CSS skeleton shimmer for card grids or content where image URLs aren't known at render time.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Prevent CLS with minimal complexity | `width`/`height` + `aspect-ratio` CSS | Browser reserves space; no JS or extra images |
| Smooth blur-up reveal | LQIP (base64 inline + JS swap) | Best perceived performance for photos |
| Compact visual placeholder with color fidelity | ThumbHash | Smaller than LQIP; supports transparency; needs JS decode |
| Purely CSS skeleton for image grids | CSS shimmer animation | No extra requests; works before image URL is known |
| Dominant color background | Single-pixel dominant color | Simplest, no JS; 1 extra request (or inline as base64) |

## Pattern

**CLS prevention — always do this first**:
```html
<!-- Browser computes aspect-ratio from these; CSS can still make it responsive -->
<img src="photo.jpg" width="800" height="600" alt="...">
```
```css
img { width: 100%; height: auto; }
/* Or for unknown dimensions: */
.image-wrapper { aspect-ratio: 16 / 9; overflow: hidden; background: #f0f0f0; }
.image-wrapper img { width: 100%; height: 100%; object-fit: cover; }
```

**LQIP / Blur-up pattern** (base64 tiny image inlined, swapped on load):
```html
<div class="img-wrapper" style="background-color: #a3b2c1;">
  <img class="img-lqip" src="data:image/jpeg;base64,/9j/4AAQ..."
    data-src="photo-full.jpg" alt="..." width="800" height="600" loading="lazy">
</div>
```
```css
.img-lqip { filter: blur(8px); transition: filter 0.4s ease; transform: scale(1.05); }
.img-lqip.loaded { filter: blur(0); transform: scale(1); }
```
```js
document.querySelectorAll('[data-src]').forEach(img => {
  const full = new Image();
  full.onload = () => { img.src = img.dataset.src; img.classList.add('loaded'); };
  full.src = img.dataset.src;
});
```
Generate LQIP at build time: `sharp(input).resize(20).blur(2).toBuffer()` then base64-encode.

**CSS skeleton shimmer** (for unknown image URLs):
```css
.skeleton-image {
  background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  aspect-ratio: 16 / 9;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
```

**ThumbHash**: ~30-char hash decoded client-side to data URI. Preferred over BlurHash: smaller hash, supports alpha. Generate at CMS upload time.

## Common Mistakes

- **Wrong**: LQIP without `width`/`height` → **Right**: space must be reserved first; LQIP alone does not prevent CLS
- **Wrong**: inlining large LQIP thumbnails (> 2KB base64) → **Right**: keep LQIP under 20px wide, heavily blurred; target < 500 bytes base64
- **Wrong**: ThumbHash/BlurHash without fallback → **Right**: requires JS; always have `width`/`height` + background-color as baseline
- **Wrong**: skeleton `aspect-ratio` not matching the actual image → **Right**: causes a visible layout jump when image loads
- **Wrong**: animating `width`/`height` for blur-up → **Right**: animate `filter` and `opacity`; they are GPU-composited

## See Also

- [Loading and Decode Craft](loading-and-decode-craft.md) — `loading="lazy"` pairs with LQIP patterns
- [Image Effects Craft](image-effects-craft.md) — reveal animations when images load
- Reference: `css-craft.md` → `skeleton-and-loading-states` for full shimmer patterns
- Reference: [Mux: Blurry image placeholders on the web](https://www.mux.com/blog/blurry-image-placeholders-on-the-web)
- Reference: [ThumbHash GitHub](https://github.com/evanw/thumbhash)
