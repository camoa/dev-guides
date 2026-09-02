---
description: Bento grid layouts — asymmetric CSS grid tiles, named areas, dense auto-fill, and responsive collapse patterns
tldr: "Use CSS Grid with `span` values or `grid-template-areas` for bento layouts. Asymmetry (varying tile sizes) is what defines bento — equal-sized tiles are just a grid."
---

# Bento Grid Layouts

## When to Use
When a client asks for "that Apple layout" — an asymmetric grid of tiles/cards with varying sizes, rounded corners, and visual hierarchy. The defining layout pattern of 2024-2026.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Apple-style feature grid | CSS Grid with `grid-template-areas` | Named areas for clarity |
| Asymmetric tile layout | CSS Grid with `span` values | Flexible column/row spanning |
| Responsive bento (collapse to stack) | Grid areas + media query | Areas redefine per breakpoint |
| Interactive bento (hover effects) | Grid + card hover patterns | See [Hover Effects Collection](hover-effects-collection.md) |
| Auto-filling bento | `grid-auto-flow: dense` | Fills gaps automatically |

## Pattern: Classic Bento Grid
```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: auto;
  gap: 1rem;
}

.bento__item {
  background: var(--color-surface);
  border-radius: 16px;
  padding: 2rem;
  overflow: hidden;
}

/* Hero tile: spans 2 columns and 2 rows */
.bento__item--hero {
  grid-column: span 2;
  grid-row: span 2;
}

/* Wide tile */
.bento__item--wide {
  grid-column: span 2;
}

/* Tall tile */
.bento__item--tall {
  grid-row: span 2;
}

/* Responsive: 2-column on tablet, 1-column on mobile */
@media (width < 1024px) {
  .bento { grid-template-columns: repeat(2, 1fr); }
  .bento__item--hero { grid-column: span 2; grid-row: span 1; }
}

@media (width < 640px) {
  .bento { grid-template-columns: 1fr; }
  .bento__item--hero,
  .bento__item--wide { grid-column: span 1; }
}
```

## Pattern: Named Areas Bento
```css
.bento--named {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 300px 200px 200px;
  gap: 1rem;
  grid-template-areas:
    "hero   hero   feat1  feat2"
    "feat3  feat4  feat4  feat2"
    "feat3  feat5  feat6  feat6";
}

.bento__hero   { grid-area: hero; }
.bento__feat1  { grid-area: feat1; }
.bento__feat2  { grid-area: feat2; }
.bento__feat3  { grid-area: feat3; }
.bento__feat4  { grid-area: feat4; }
.bento__feat5  { grid-area: feat5; }
.bento__feat6  { grid-area: feat6; }

/* Responsive override */
@media (width < 768px) {
  .bento--named {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    grid-template-areas:
      "hero" "feat1" "feat2" "feat3"
      "feat4" "feat5" "feat6";
  }
}
```

## Pattern: Dense Auto-Fill Bento
```css
/* Grid fills gaps automatically */
.bento--dense {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-rows: 200px;
  grid-auto-flow: dense;
  gap: 1rem;
}
```

## Pattern: Bento with Hover Effects
```css
.bento__item {
  transition: transform 0.3s var(--ease-standard),
              box-shadow 0.3s var(--ease-standard);
}

.bento__item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px oklch(0% 0 0 / 0.1);
}

/* Image zoom inside bento tile */
.bento__item img {
  transition: transform 0.6s var(--ease-standard);
}

.bento__item:hover img {
  transform: scale(1.05);
}
```

## Styling Conventions
- **Border radius**: 12-24px (Apple uses 16-20px)
- **Gap**: 8-16px (denser = more "bento", wider = more "dashboard")
- **Background**: Subtle surface color, not white on white
- **Content**: Icon + heading + short text, or full-bleed image
- **Overflow**: `hidden` on tiles to clip images and backgrounds

## Common Mistakes
- **Equal-sized tiles** — bento is defined by asymmetry; use varying spans
- **Too many tile sizes** — 3-4 size variants is enough (1x1, 2x1, 1x2, 2x2)
- **No responsive fallback** — bento MUST collapse gracefully on mobile
- **Heavy content in small tiles** — small tiles should have minimal content (icon + label)

## See Also
- [Container Query Craft](container-queries-craft.md) → tiles that adapt to their own size
- [Hover Effects Collection](hover-effects-collection.md) → card hover patterns
- [Elevation and Shadows](elevation-and-shadows.md) → shadow system for tiles
