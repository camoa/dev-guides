---
description: Marquee and infinite scroll — CSS text ribbons, logo tickers, alternating direction rows, and pause-on-hover
tldr: "Use CSS `@keyframes translateX` with duplicated content for seamless infinite scrolling ribbons. Always pause on hover and respect `prefers-reduced-motion`."
---

# Marquee & Infinite Scroll

## When to Use
When a client wants a continuously scrolling text ribbon, logo ticker, or infinite horizontal scroll — the "modern marquee" effect seen on agency sites, fashion brands, and portfolios.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Horizontally scrolling text ribbon | CSS `@keyframes translateX` + duplicate content | Seamless loop, no JS |
| Logo/client ticker | Same technique with images | Horizontal logo parade |
| Reverse direction marquee | Negative translateX values or `animation-direction: reverse` | Alternating rows |
| Pause on hover | `animation-play-state: paused` on `:hover` | Accessible, lets user read |
| Diagonal/vertical marquee | `translateY` or `rotate` + `translateX` | Rotated container |
| Speed controlled by scroll | `animation-timeline: scroll()` on `translateX` | Scroll-driven marquee |

## Pattern: Horizontal Text Marquee
```html
<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <span class="marquee__content">Your text here — </span>
    <span class="marquee__content" aria-hidden="true">Your text here — </span>
  </div>
</div>
```
```css
.marquee {
  overflow: hidden;
  white-space: nowrap;
}

.marquee__track {
  display: inline-flex;
  animation: marquee 20s linear infinite;
}

.marquee__content {
  display: inline-block;
  padding-right: 2rem;
}

@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

/* Pause on hover for accessibility */
.marquee:hover .marquee__track {
  animation-play-state: paused;
}

/* Reduced motion: stop animation */
@media (prefers-reduced-motion: reduce) {
  .marquee__track {
    animation: none;
  }
}
```

## Pattern: Logo Ticker
```css
.logo-ticker {
  overflow: hidden;
  mask-image: linear-gradient(
    to right,
    transparent,
    black 10%,
    black 90%,
    transparent
  );
}

.logo-ticker__track {
  display: flex;
  gap: 3rem;
  align-items: center;
  animation: ticker 30s linear infinite;
}

@keyframes ticker {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.logo-ticker__item {
  flex-shrink: 0;
  height: 40px;
  opacity: 0.6;
  filter: grayscale(1);
  transition: opacity 0.3s, filter 0.3s;
}

.logo-ticker__item:hover {
  opacity: 1;
  filter: grayscale(0);
}
```

## Pattern: Alternating Direction Rows
```css
.marquee--reverse .marquee__track {
  animation-direction: reverse;
}

/* Two-row alternating marquee */
.marquee-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}
```

**Key technique:** The content is duplicated (two identical copies) so when the first copy scrolls away, the second seamlessly takes its place. `translateX(-50%)` moves exactly one copy's width.

**Fade edges:** Use `mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent)` to create smooth fade-in/fade-out at the edges.

## Common Mistakes
- **Not duplicating content** — without a duplicate, there's a visible gap when the animation loops
- **Using `overflow: hidden` on the wrong element** — put it on the outer container, animation on the inner track
- **Forgetting `aria-hidden`** on duplicated content — screen readers should only read the text once
- **Not pausing on hover** — users need to be able to read the scrolling text
- **Fixed animation duration** — longer text needs longer duration; calculate based on content width

## See Also
- [Text Effects](text-effects.md) → gradient text in marquees
- [Accessibility and Motion](accessibility-and-motion.md) → prefers-reduced-motion
