---
description: CSS-only accordions — semantic details/summary, animated height with grid trick, exclusive accordion with name attribute
---

# CSS-Only Accordions

## When to Use

> Use `<details>`/`<summary>` for all accordion patterns — they handle toggle, accessibility, and keyboard for free. Add animation with the grid height trick (cross-browser) or `interpolate-size` (Chrome 129+).

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| FAQ accordion | `<details>` + `<summary>` | Semantic HTML, built-in toggle |
| Animated accordion (all browsers) | `<details>` + grid height trick | Works everywhere |
| Animated accordion (Chrome only) | `<details>` + `interpolate-size` | Smooth expand, one property |
| Exclusive accordion (one open at a time) | `<details name="group">` | HTML attribute, no JS |
| Custom styled accordion marker | `summary::marker` or `list-style: none` + custom | Replace default triangle |

## Pattern

```html
<!-- Exclusive accordion — HTML only -->
<details name="faq">
  <summary>Question one?</summary>
  <div class="details-content">Answer content.</div>
</details>
<details name="faq">
  <summary>Question two?</summary>
  <div class="details-content">Another answer.</div>
</details>
```
```css
/* Grid height trick — cross-browser animation */
details .details-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.35s var(--ease-emphasized-decel);
  overflow: hidden;
}
details[open] .details-content {
  grid-template-rows: 1fr;
}
details .details-content > div { overflow: hidden; }

/* Summary arrow */
summary {
  cursor: pointer; list-style: none;
  display: flex; justify-content: space-between; align-items: center;
  padding: 1rem;
}
summary::after {
  content: '';
  width: 10px; height: 10px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(-45deg);
  transition: transform 0.3s var(--ease-standard);
}
details[open] summary::after { transform: rotate(45deg); }
```

**Browser support:** `<details>` name attribute (exclusive): Chrome 120+, Firefox 130+, Safari 17.2+. `interpolate-size` for height: Chrome 129+ only.

## Common Mistakes

- **Building custom accordion with JS** when `<details>` exists — the semantic element handles toggle, accessibility, and keyboard for free
- **Forgetting `overflow: hidden`** on animated panels — content leaks during transition
- **Not styling `summary::marker`** — the default triangle varies across browsers

## See Also

- [CSS-Only Popovers](css-only-popovers.md) → click-triggered panels
- [CSS-Only Tabs](css-only-tabs.md) → horizontal tab switching
- [Accessibility and Motion](accessibility-and-motion.md) → reduce motion for accordion animations
