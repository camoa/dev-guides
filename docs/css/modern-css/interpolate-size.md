---
description: "Animate height/width to auto and intrinsic sizing keywords — replacing JavaScript scrollHeight measurement"
tldr: "Use `interpolate-size: allow-keywords` when you need to animate height or width to/from `auto`, `min-content`, `max-content`, or `fit-content`. Use JavaScript `scrollHeight` measurement when cross-browser support is required (Firefox and…"
---

# interpolate-size — Animate to `height: auto`

## When to Use

> When you need to animate an element's height (or width) to/from `auto`, `min-content`, `max-content`, or `fit-content` — the classic "accordion" problem that previously required JavaScript to measure `scrollHeight`.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Accordion expand/collapse with smooth animation | `interpolate-size: allow-keywords` on `:root` | One declaration enables all keyword transitions sitewide |
| Animate to auto height on a single element | `interpolate-size: allow-keywords` on that element | Scoped to just that component |
| Math on intrinsic sizes | `calc-size(auto, size - 20px)` | Subtract/add from the resolved auto value |
| Cross-browser accordion animation now | JavaScript `scrollHeight` measurement | Firefox and Safari don't support `interpolate-size` yet |

## Pattern

```css
/* Enable globally — opt in once */
:root {
  interpolate-size: allow-keywords;
}

/* Accordion panel */
.accordion-panel {
  height: 0;
  overflow: hidden;
  transition: height 0.35s ease;
}

.accordion-panel[open],
.accordion-item.is-open .accordion-panel {
  height: auto; /* Now animatable! */
}

/* Details/summary native accordion */
details {
  overflow: hidden;
  transition: height 0.3s ease;
}
details:not([open]) {
  height: 2.5rem; /* Collapsed: just the summary */
}
details[open] {
  height: auto;
}

/* calc-size for offset from intrinsic */
.sidebar {
  width: calc-size(fit-content, size + 2rem);
  transition: width 0.3s;
}
```

**How it works:** The `interpolate-size: allow-keywords` declaration tells the browser to resolve `auto` (and other sizing keywords) to their computed pixel value for interpolation purposes. The property inherits, so setting it on `:root` enables it everywhere.

**`calc-size()` function:** Allows arithmetic on sizing keywords. `calc-size(auto, size - 20px)` means "the computed auto value minus 20px." The `size` keyword inside refers to the resolved intrinsic size.

**Browser support:** Chrome 129+, Edge 129+. **Not supported** in Firefox or Safari as of April 2026. Use as progressive enhancement — without support, the element snaps to the final state (still functional, not animated).

## Common Mistakes

- Forgetting `overflow: hidden` on the animated element — content will be visible outside the collapsing container
- Using `interpolate-size` without `transition` or `animation` — the property enables interpolation but you still need to declare the transition
- Expecting `calc-size()` to work with `calc()` — they are separate functions; use `calc-size()` specifically for intrinsic keyword math
- Setting `height: 0` without a `min-height` fallback — consider `min-height: 0` to prevent negative height issues

## See Also

- [@starting-style](starting-style-transitions.md) → for elements entering from `display: none`
- [Discrete Animations](discrete-animations.md) → for transitioning the `display` property itself
- Reference: [Chrome: Animate to height: auto](https://developer.chrome.com/docs/css-ui/animate-to-height-auto)
