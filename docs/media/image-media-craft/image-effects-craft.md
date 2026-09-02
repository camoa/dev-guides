---
description: CSS image effects — object-fit cropping, zoom on hover, reveal animations, before/after sliders, and native dialog lightbox
tldr: "Use `object-fit: cover` with an explicit container height for card and hero images. Use `transform: scale(1.05)` for hover zoom — keep scale under 1.06."
---

# Image Effects Craft

## When to Use

> Applying CSS effects to images: cropping behavior, reveal animations, comparison sliders, zoom on hover, and lightbox patterns. These are visual craft techniques for polished image presentation.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Image fills container without distortion | `object-fit: cover` | Crops to fit; no whitespace |
| Image must show fully, no crop | `object-fit: contain` | Letterboxes inside container |
| Image zoom effect on hover | `transform: scale(1.03–1.06)` on `<img>`, `overflow: hidden` on wrapper | GPU-composited; stays sharp |
| Image wipes in on scroll | `clip-path: inset()` animated by `IntersectionObserver` | Clean GPU-composited reveal |
| Before/after comparison | Range input over stacked images | Accessible; no library needed |
| Full-size image lightbox | `<dialog showModal()>` | Built-in focus trap, `Esc` close, ARIA |

## `object-fit` and `object-position`

Controls how an image fills its container without distortion. Always define an explicit `width` and `height` on the container, not on `<img>` directly when using `object-fit`.

| Value | When to Use | Effect |
|---|---|---|
| `cover` | Cards, hero images, thumbnails with fixed container | Fills container; crops to fit; no whitespace |
| `contain` | Product images, logos, anything that must not crop | Fits inside container; may show letterboxing |
| `fill` | Avoid — distorts image | Stretches to fill; aspect ratio lost |
| `scale-down` | Prevents upscaling of small images | Like `contain` but won't upscale; useful for small icons in large containers |
| `none` | Avoid for regular images | Displays at intrinsic size; may overflow |

```css
.card-image {
  width: 100%;
  height: 240px;       /* Fixed container height */
  object-fit: cover;
  object-position: center top; /* Favor top of image — shows faces */
}
```

**`object-position` strategy**: Use `center top` for portraits (faces at top), `center center` for landscapes (default), `left center` for subjects at left edge. For user-uploaded content where subject position is unknown, implement focal point data (see Drupal section).

## Image Zoom on Hover

```css
.image-wrapper {
  overflow: hidden;
  border-radius: 8px; /* Clip the zoomed image to rounded corners */
}
.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.2, 0, 0, 1);
  transform-origin: center;
}
.image-wrapper:hover img,
.image-wrapper:focus-within img {
  transform: scale(1.05);
}
@media (prefers-reduced-motion: reduce) {
  .image-wrapper img { transition: none; }
}
```

**Why 1.05 not 1.1+**: Larger scale values make the image noticeably pixelated at typical display sizes. 1.03–1.06 is the sweet spot for perceived depth without quality loss.

## Image Reveal Animations

Use when images enter the viewport for the first time. Pair with `IntersectionObserver` or CSS `@keyframes` triggered by a class.

**Clip-path wipe** (image wipes in from left):
```css
.img-reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 0.6s cubic-bezier(0.05, 0.7, 0.1, 1);
}
.img-reveal.visible { clip-path: inset(0 0% 0 0); }
```

**Fade + scale up**:
```css
.img-fade-up {
  opacity: 0;
  transform: scale(0.97);
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.05, 0.7, 0.1, 1);
}
.img-fade-up.visible { opacity: 1; transform: scale(1); }
```

Cross-reference: `css-craft.md` → `entrance-animations` for the full `IntersectionObserver` + `@starting-style` pattern set.

## Before/After Comparison Slider

Pure CSS with the `resize` property is limited (cursor UX is poor). The practical approach uses a range input positioned over two stacked images:

```html
<div class="comparison" style="position: relative; aspect-ratio: 16/9;">
  <img class="img-after" src="after.jpg" alt="After" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">
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
slider.addEventListener('input', e => {
  clip.style.width = e.target.value + '%';
});
```

Accessibility: `aria-label` on the range input is required. Screen reader users cannot perceive the visual comparison, so supplement with descriptive text.

## Lightbox Pattern

Modern lightbox uses the native `<dialog>` element — no library required for basic implementation.

```html
<button class="img-trigger" data-target="lightbox-1" aria-haspopup="dialog">
  <img src="thumb.jpg" alt="Open full view: Mountain landscape">
</button>
<dialog id="lightbox-1" class="lightbox" aria-label="Image lightbox">
  <button class="lightbox-close" autofocus aria-label="Close lightbox">×</button>
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
// Close on backdrop click
document.querySelectorAll('.lightbox').forEach(dialog => {
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
});
```

`<dialog>` provides: focus trapping, backdrop rendering, `Escape` key to close, ARIA role semantics — all built in.

For View Transitions API integration (smooth open/close animation with the thumbnail), see [css-craft.md → modern-css-craft-patterns].

## Common Mistakes

- Using `object-fit: cover` without a height constraint — `<img>` with only `width: 100%` and no height will not constrain; the container needs a defined height
- `transform: scale(1.2)` on hover zoom — visible pixelation and jitter on high-DPI screens; keep scale ≤ 1.06
- Using `overflow: hidden` on `<img>` directly — `overflow` only applies to block elements with children; wrap the image
- Custom lightbox modals without focus trapping — keyboard users get stranded outside the lightbox; use `<dialog>` or a tested library
- Image reveal animations on elements that are already visible on page load — triggers immediately, wasting the effect; use `IntersectionObserver` threshold > 0

## See Also

- [Placeholder Strategies](placeholder-strategies.md) — blur-up on load pairs with image reveal
- Reference: `css-craft.md` → `clip-path-and-masks` for clip-path animation techniques
- Reference: `css-craft.md` → `blend-modes-and-visual-effects` for overlay effects on images
- Reference: [MDN `<dialog>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog)
