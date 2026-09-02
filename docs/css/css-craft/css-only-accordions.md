---
description: CSS-only accordions — semantic details/summary, animated height with grid trick, exclusive accordion with name attribute
tldr: "Use `<details>`/`<summary>` for all accordion patterns — they handle toggle, accessibility, and keyboard for free. Add animation with the grid height trick (cross-browser) or `interpolate-size` (Chrome 129+)."
---

# CSS-Only Accordions

## When to Use
When a client needs expandable/collapsible sections, FAQ accordions, or show/hide panels — without JavaScript toggle libraries.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| FAQ accordion | `<details>` + `<summary>` | Semantic HTML, built-in toggle |
| Animated accordion (height auto) | `<details>` + `interpolate-size` (Chrome) | Smooth expand with CSS only |
| Animated accordion (cross-browser) | `<details>` + `grid` height trick | Works in all browsers |
| Exclusive accordion (one open at a time) | `<details name="group">` | HTML attribute, no JS |
| Custom styled accordion marker | `summary::marker` or `list-style: none` + custom | Replace default triangle |

## Pattern: Semantic Accordion
```html
<details name="faq">
  <summary>Question one?</summary>
  <div class="details-content">Answer content here.</div>
</details>
<details name="faq">
  <summary>Question two?</summary>
  <div class="details-content">Another answer.</div>
</details>
```

## Pattern: Animated Accordion (Chrome 129+)
```css
:root { interpolate-size: allow-keywords; }

details {
  border: 1px solid oklch(90% 0 0);
  border-radius: 8px;
  overflow: hidden;
}

details .details-content {
  height: 0;
  overflow: hidden;
  transition: height 0.35s var(--ease-emphasized-decel),
              padding 0.35s var(--ease-emphasized-decel);
  padding: 0 1rem;
}

details[open] .details-content {
  height: auto;
  padding: 1rem;
}

/* Custom arrow rotation */
summary {
  cursor: pointer;
  padding: 1rem;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

summary::after {
  content: '';
  width: 10px;
  height: 10px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(-45deg);
  transition: transform 0.3s var(--ease-standard);
}

details[open] summary::after {
  transform: rotate(45deg);
}
```

## Pattern: Grid Height Trick (Cross-Browser)
```css
/* Works in all browsers — no interpolate-size needed */
details .details-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.35s var(--ease-emphasized-decel);
  overflow: hidden;
}

details[open] .details-content {
  grid-template-rows: 1fr;
}

details .details-content > div {
  overflow: hidden;
}
```

## Pattern: Exclusive Accordion (HTML only)
```html
<!-- name attribute = only one can be open at a time -->
<details name="accordion-group" open>
  <summary>Section 1</summary>
  <p>Content 1</p>
</details>
<details name="accordion-group">
  <summary>Section 2</summary>
  <p>Content 2</p>
</details>
```

**Browser support:** `<details>`/`<summary>`: all browsers. `name` attribute for exclusive: Chrome 120+, Firefox 130+, Safari 17.2+. `interpolate-size`: Chrome 129+ only.

## Common Mistakes
- **Building custom accordion with JS** when `<details>` exists — the semantic element handles toggle, accessibility, and keyboard for free
- **Forgetting `overflow: hidden`** on animated panels — content leaks during transition
- **Not styling `summary::marker`** — the default triangle varies across browsers

## See Also
- [Modern CSS: interpolate-size](../modern-css/interpolate-size.md) → animate to `height: auto`
- [Accessibility and Motion](accessibility-and-motion.md) → reduce motion for accordion animations
- [CSS-Only Tabs](css-only-tabs.md) → horizontal tab switching
