---
description: CSS-only popovers and tooltips — Popover API, anchor positioning, and cross-browser hover tooltip patterns
tldr: "Use the Popover API (`popover` attribute + `popovertarget`) for click-triggered panels with built-in light dismiss and focus trapping. Use CSS `:hover` + `::after` for simple hover tooltips that need to work everywhere."
---

# CSS-Only Popovers & Tooltips

## When to Use
When a client needs tooltips, dropdowns, info popovers, or notification panels — without JavaScript positioning or focus-trap libraries.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Tooltip on hover | `popover=hint` + anchor positioning (Chrome) or CSS `:hover` + absolute | Native tooltip behavior |
| Click-triggered popover | `popover` attribute + `popovertarget` | Built-in light dismiss, focus trap |
| Dropdown menu | `popover` + anchor positioning | Positioned relative to trigger |
| Info popover with arrow | `popover` + `anchor()` + `::before` arrow | Positioned and styled |
| Cross-browser tooltip | `:hover` + `::after` pseudo-element | Works everywhere |

## Pattern: Popover API (All Browsers)
```html
<button popovertarget="info-popup">More info</button>
<div id="info-popup" popover>
  <p>Additional information here.</p>
</div>
```
```css
[popover] {
  border: 1px solid oklch(85% 0 0);
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 4px 16px oklch(0% 0 0 / 0.12);
  max-width: 320px;

  /* Entry animation */
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.2s, transform 0.2s,
              display 0.2s allow-discrete,
              overlay 0.2s allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  transform: translateY(0);
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    transform: translateY(8px);
  }
}

/* Backdrop */
[popover]::backdrop {
  background: oklch(0% 0 0 / 0);
  transition: background 0.2s;
}

[popover]:popover-open::backdrop {
  background: oklch(0% 0 0 / 0.15);
}
```

## Pattern: Anchored Tooltip (Chrome 125+)
```css
.trigger {
  anchor-name: --tooltip-anchor;
}

.tooltip {
  position: fixed;
  position-anchor: --tooltip-anchor;
  position-area: top center;
  margin-bottom: 8px;
  position-try-fallbacks: flip-block;

  /* Styling */
  background: oklch(20% 0 0);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  white-space: nowrap;
}

/* Arrow */
.tooltip::before {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: oklch(20% 0 0);
}
```

## Pattern: Pure CSS Tooltip (Cross-Browser)
```css
.has-tooltip {
  position: relative;
}

.has-tooltip::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: oklch(20% 0 0);
  color: white;
  padding: 0.4rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s;
}

.has-tooltip:hover::after,
.has-tooltip:focus-visible::after {
  opacity: 1;
}
```

## Common Mistakes
- **Using JS libraries for simple tooltips** — CSS `:hover` + `::after` or the Popover API handles most cases
- **Forgetting `popovertarget`** — the button needs `popovertarget="id"` to toggle the popover
- **Not providing keyboard access** — `:hover` tooltips need `:focus-visible` equivalent
- **Missing `position-try-fallbacks`** on anchored elements — without it, tooltips overflow viewport edges

## See Also
- [Modern CSS: Popover API](../modern-css/popover-api.md) → full API syntax
- [Modern CSS: Anchor Positioning](../modern-css/anchor-positioning.md) → positioned relative to trigger
- [Modern CSS: @starting-style](../modern-css/starting-style-transitions.md) → entry animations
