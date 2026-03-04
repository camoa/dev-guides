---
description: CSS image effects — object-fit cropping, zoom on hover, reveal animations, before/after sliders, and native dialog lightbox
---

# Image Effects Craft

## When to Use

> Use `object-fit: cover` with an explicit container height for card and hero images. Use `transform: scale(1.05)` for hover zoom — keep scale under 1.06. Use `<dialog>` for lightbox — no library needed for basic implementation.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Image fills container without distortion | `object-fit: cover` | Crops to fit; no whitespace |
| Image must show fully, no crop | `object-fit: contain` | Letterboxes inside container |
| Image zoom effect on hover | `transform: scale(1.03–1.06)` on `<img>`, `overflow: hidden` on wrapper | GPU-composited; stays sharp |
| Image wipes in on scroll | `clip-path: inset()` animated by `IntersectionObserver` | Clean GPU-composited reveal |
| Before/after comparison | Range input over stacked images | Accessible; no library needed |
| Full-size image lightbox | `<dialog showModal()>` | Built-in focus trap, `Esc` close, ARIA |

## Pattern

**`object-fit` with focal position**:
```css
.card-image {
  width: 100%;
  height: 240px;
  object-fit: cover;
  object-position: center top; /* Favor top — shows faces */
}
```

**Zoom on hover** (keep scale ≤ 1.06 to avoid pixelation):
```css
.image-wrapper { overflow: hidden; border-radius: 8px; }
.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.2, 0, 0, 1);
}
.image-wrapper:hover img,
.image-wrapper:focus-within img { transform: scale(1.05); }
@media (prefers-reduced-motion: reduce) { .image-wrapper img { transition: none; } }
```

**Clip-path wipe reveal** (trigger with IntersectionObserver):
```css
.img-reveal { clip-path: inset(0 100% 0 0); transition: clip-path 0.6s cubic-bezier(0.05, 0.7, 0.1, 1); }
.img-reveal.visible { clip-path: inset(0 0% 0 0); }
```

**Native dialog lightbox**:
```html
<button class="img-trigger" data-target="lightbox-1" aria-haspopup="dialog">
  <img src="thumb.jpg" alt="Open full view: Mountain landscape">
</button>
<dialog id="lightbox-1" class="lightbox" aria-label="Image lightbox">
  <button class="lightbox-close" autofocus aria-label="Close lightbox">&#215;</button>
  <img src="full.jpg" alt="Mountain landscape" loading="lazy">
</dialog>
```
```js
document.querySelectorAll('.img-trigger').forEach(btn => {
  btn.addEventListener('click', () =>
    document.getElementById(btn.dataset.target).showModal()
  );
});
document.querySelectorAll('.lightbox-close').forEach(btn => {
  btn.addEventListener('click', () => btn.closest('dialog').close());
});
document.querySelectorAll('.lightbox').forEach(dialog => {
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
});
```

`<dialog>` provides focus trapping, backdrop rendering, `Escape` key to close, and ARIA role semantics built in.

**Before/after slider** (range input over stacked images):
```html
<div class="comparison" style="position: relative; aspect-ratio: 16/9;">
  <img class="img-after" src="after.jpg" alt="After"
    style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">
  <div class="img-before-clip" style="position: absolute; inset: 0; overflow: hidden; width: 50%;">
    <img src="before.jpg" alt="Before" style="width: 100%; height: 100%; object-fit: cover; min-width: 100vw;">
  </div>
  <input type="range" min="0" max="100" value="50" aria-label="Before/after comparison"
    style="position: absolute; width: 100%; top: 50%; transform: translateY(-50%);">
</div>
```
```js
const slider = document.querySelector('input[type="range"]');
const clip = document.querySelector('.img-before-clip');
slider.addEventListener('input', e => { clip.style.width = e.target.value + '%'; });
```

## Common Mistakes

- **Wrong**: `object-fit: cover` without a container height → **Right**: container needs a defined height; `<img>` with only `width: 100%` will not constrain
- **Wrong**: `transform: scale(1.2)` on hover zoom → **Right**: visible pixelation on high-DPI screens; keep scale ≤ 1.06
- **Wrong**: `overflow: hidden` on `<img>` directly → **Right**: `overflow` applies to block elements with children; wrap the image
- **Wrong**: custom lightbox without focus trapping → **Right**: use `<dialog>` or a tested library; keyboard users get stranded
- **Wrong**: image reveal animations on already-visible elements → **Right**: use `IntersectionObserver` with threshold > 0

## See Also

- [Placeholder Strategies](placeholder-strategies.md) — blur-up on load pairs with image reveal
- Reference: `css-craft.md` → `clip-path-and-masks` for clip-path animation techniques
- Reference: `css-craft.md` → `blend-modes-and-visual-effects` for overlay effects on images
- Reference: [MDN `<dialog>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog)
