---
description: Bento grid layouts — asymmetric CSS grid tiles, named areas, dense auto-fill, and responsive collapse patterns
---

# Bento Grid Layouts

## When to Use

> Use CSS Grid with `span` values or `grid-template-areas` for bento layouts. Asymmetry (varying tile sizes) is what defines bento — equal-sized tiles are just a grid.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Apple-style feature grid | CSS Grid with `grid-template-areas` | Named areas for clarity |
| Asymmetric tile layout | CSS Grid with `span` values | Flexible column/row spanning |
| Responsive bento (collapse to stack) | Grid areas + media query | Areas redefine per breakpoint |
| Interactive bento (hover effects) | Grid + card hover patterns | See [Hover Effects Collection](hover-effects-collection.md) |
| Auto-filling bento | `grid-auto-flow: dense` | Fills gaps automatically |

## Pattern

```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
.bento__item {
  background: var(--color-surface);
  border-radius: 16px; padding: 2rem; overflow: hidden;
}
.bento__item--hero { grid-column: span 2; grid-row: span 2; }
.bento__item--wide { grid-column: span 2; }
.bento__item--tall { grid-row: span 2; }

/* Named areas variant */
.bento--named {
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 300px 200px;
  grid-template-areas:
    "hero   hero   feat1  feat2"
    "feat3  feat4  feat4  feat2";
}
.bento__hero  { grid-area: hero; }
.bento__feat1 { grid-area: feat1; }

/* Responsive */
@media (width < 1024px) {
  .bento { grid-template-columns: repeat(2, 1fr); }
}
@media (width < 640px) {
  .bento { grid-template-columns: 1fr; }
  .bento__item--hero,
  .bento__item--wide { grid-column: span 1; }
}
```

**Styling conventions:** Border radius 12–24px. Gap 8–16px. Always `overflow: hidden` on tiles. Limit to 3–4 tile size variants (1×1, 2×1, 1×2, 2×2).

## Common Mistakes

- **Equal-sized tiles** — bento is defined by asymmetry; use varying spans
- **Too many tile sizes** — more than 4 variants becomes hard to manage
- **No responsive fallback** — bento MUST collapse gracefully on mobile
- **Heavy content in small tiles** — small tiles should have minimal content (icon + label)

## See Also

- [Container Query Craft](container-queries-craft.md) → tiles that adapt to their own size
- [Hover Effects Collection](hover-effects-collection.md) → card hover patterns for tiles
- [Elevation and Shadows](elevation-and-shadows.md) → shadow system for tiles
