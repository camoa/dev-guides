---
description: Align nested grid items to parent tracks — card footer alignment without JS
---

# CSS Subgrid

## When to Use

> Use `subgrid` when children of a grid item need to align to the parent grid's tracks. Use regular grid when layout is single-level with no nested alignment requirements.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Card footers aligned across a row | `subgrid` on `grid-template-rows` | Cards inherit parent row tracks |
| Form labels aligned across nested items | `subgrid` on `grid-template-columns` | Nested columns align to parent grid |
| Consistent internal alignment in a component | `subgrid` | Replaces JS height equalization |
| Simple single-level grid layout | Regular grid | Subgrid adds complexity without benefit |

## Pattern

The card alignment use case — each card has three internal zones (header, body, footer) that align perfectly across a row:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-template-rows: auto 1fr auto; /* header | body | footer */
  gap: 1rem;
}

.card {
  grid-row: span 3;        /* Span all three row tracks */
  display: grid;
  grid-template-rows: subgrid; /* Inherit the parent's row tracks */
  gap: 0;
}

/* Each zone now aligns with its counterpart in other cards */
.card__header { /* row 1 — always same height across row */ }
.card__body    { /* row 2 — flexible, auto stretches to fill */ }
.card__footer  { /* row 3 — always pinned to bottom */ }
```

This replaces `display: flex; margin-top: auto` on footers, JavaScript height equalization, and fixed-height hacks.

**Browser support:** Chrome 117, Firefox 71, Safari 16. Safe to use. (Firefox had subgrid first, in 2019.)

## Common Mistakes

- **Wrong**: Forgetting `grid-row: span N` on the grid item → **Right**: The card must span the same number of rows as the parent defines, otherwise `subgrid` has nothing to inherit
- **Wrong**: Keeping `gap` on the subgrid element → **Right**: The subgrid element inherits parent gaps by default; set `gap: 0` to prevent double-gapping
- **Wrong**: Using subgrid for column alignment when columns are on a different containing block → **Right**: Subgrid only inherits tracks from the direct grid parent

## See Also

- [Container Queries (@container)](container-queries.md)
- [@layer — Cascade Layers](cascade-layers.md)
- Reference: [MDN Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid)
