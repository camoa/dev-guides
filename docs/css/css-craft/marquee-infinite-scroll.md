---
description: Marquee and infinite scroll — CSS text ribbons, logo tickers, alternating direction rows, and pause-on-hover
tldr: "Use CSS `@keyframes translateX` with duplicated content for seamless infinite scrolling ribbons. Always pause on hover and respect `prefers-reduced-motion`."
---

# Marquee & Infinite Scroll

## When to Use

> Use CSS `@keyframes translateX` with duplicated content for seamless infinite scrolling ribbons. Always pause on hover and respect `prefers-reduced-motion`.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Horizontally scrolling text ribbon | `@keyframes translateX` + duplicate content | Seamless loop, no JS |
| Logo/client ticker | Same with images + fade-edge mask | Horizontal logo parade |
| Reverse direction marquee | `animation-direction: reverse` | Alternating rows |
| Pause on hover | `animation-play-state: paused` on `:hover` | Accessible, lets user read |
| Diagonal/vertical marquee | `translateY` or `rotate` + `translateX` | Rotated container |

## Pattern

```html
<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <span class="marquee__content">Your text here — </span>
    <span class="marquee__content" aria-hidden="true">Your text here — </span>
  </div>
</div>
```
```css
.marquee { overflow: hidden; white-space: nowrap; }
.marquee__track {
  display: inline-flex;
  animation: marquee 20s linear infinite;
}
.marquee__content { display: inline-block; padding-right: 2rem; }
@keyframes marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
.marquee:hover .marquee__track { animation-play-state: paused; }
@media (prefers-reduced-motion: reduce) {
  .marquee__track { animation: none; }
}

/* Logo ticker with fade edges */
.logo-ticker {
  overflow: hidden;
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}

/* Alternating direction */
.marquee--reverse .marquee__track { animation-direction: reverse; }
```

**Key technique:** Duplicate content so when the first copy scrolls away, the second takes its place. `translateX(-50%)` moves exactly one copy's width.

## Common Mistakes

- **Not duplicating content** — without a duplicate, there's a visible gap when the animation loops
- **`overflow: hidden` on wrong element** — put it on the outer container, animation on the inner track
- **Forgetting `aria-hidden`** on duplicated content — screen readers should only read text once
- **Not pausing on hover** — users need to be able to read the scrolling text
- **Fixed animation duration** — longer text needs longer duration; scale duration to content width

## See Also

- [Text Effects](text-effects.md) → gradient text in marquees
- [Accessibility and Motion](accessibility-and-motion.md) → `prefers-reduced-motion`
