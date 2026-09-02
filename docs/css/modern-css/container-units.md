---
description: "Size elements relative to their container with cqi, cqw, cqb units"
tldr: "Use container query units when you need to size elements relative to their container, not the viewport — fluid typography or scaling elements inside components without any breakpoints."
---

# Container Query Units

## When to Use

> When you need to size elements relative to their container, not the viewport — fluid typography or scaling elements inside components without any breakpoints.

## Decision

| If you need... | Use... | Notes |
|---|---|---|
| Font size that scales with component width | `font-size: clamp(1rem, 4cqi, 2rem)` | `cqi` = 1% of container inline size |
| Icon that scales with its component | `width: 10cqi` | Proportional to container |
| Padding proportional to container | `padding: 2cqw` | `cqw` = 1% of container width |
| Smallest container dimension | `cqmin` | Like `vmin` but for container |
| Largest container dimension | `cqmax` | Like `vmax` but for container |

## Pattern

Fluid typography inside a card component — scales smoothly between container sizes with no `@container` breakpoints needed:

```css
.card-wrapper {
  container-type: inline-size;
}

.card__title {
  /* Scales from 1rem at narrow containers to 2rem at wide ones */
  font-size: clamp(1rem, 4cqi + 0.5rem, 2rem);
}

.card__icon {
  width: clamp(1.5rem, 8cqi, 3rem);
}
```

**Unit reference:**

| Unit | Meaning |
|---|---|
| `cqi` | 1% of container inline size |
| `cqb` | 1% of container block size |
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqmin` | Smaller of `cqi` or `cqb` |
| `cqmax` | Larger of `cqi` or `cqb` |

**Browser support:** Chrome 105, Firefox 110, Safari 16. Same as container size queries. Safe to use.

## Common Mistakes

- Using `cqi` when there is no ancestor with `container-type` — falls back to viewport units, which may or may not be what you want; always verify containment is set
- Preferring `cqw` over `cqi` — `cqi` is direction-aware and the more correct choice in most cases

## See Also

- ← [Container Queries](container-queries.md) | [Subgrid](subgrid.md) →
- Reference: [MDN Container query length units](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries#container_query_length_units)
