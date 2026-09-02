---
description: "Respond to container size with @container — component-level responsive design"
tldr: "Use `@container` when a component needs to adapt to the space available from its container, not the viewport. Use `@media` when you need page-level breakpoints based on viewport size."
---

# Container Queries

## When to Use

> When a component needs to adapt to the space available from its container, not the viewport. This is the solution to component-level responsive design — the same component in a sidebar and in a main column behaves differently because their containers have different widths.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Component layout based on available width | `@container` size query | Reacts to container, not viewport |
| Same component used in sidebar AND main content | `@container` | Media query would be identical for both contexts |
| Page-level breakpoints | `@media` | Still the right tool for viewport-based layout |
| Query a custom property value on an ancestor | Container style query `@container style(--variant: card)` | Lets parent communicate intent to children |
| Fluid sizing inside a component | Container query units (`cqi`, `cqw`) | See [Container Units](container-units.md) |

## Pattern

```css
/* Declare containment context */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Component adapts to its container */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
    gap: 1.5rem;
  }
}

/* Named container — query a specific ancestor */
.sidebar { container: sidebar / inline-size; }

@container sidebar (width < 300px) {
  .widget { font-size: 0.875rem; }
}
```

**Style queries** — pass intent from parent to child via custom properties:

```css
.card { --layout: portrait; }

@container style(--layout: landscape) {
  .card__image { aspect-ratio: 16/9; }
}
```

**`container-type` values:**
- `inline-size` — query the inline dimension (almost always what you want)
- `size` — query both axes (requires explicit height on container)
- `normal` — allows style queries only, no size queries

**Browser support:**
- Size queries: Chrome 105, Firefox 110, Safari 16. Safe to use.
- Style queries: Chrome 111, Safari 18. **Firefox does not yet support style queries (support pending, expected 2026).** Use style queries as progressive enhancement only.

## Common Mistakes

- Forgetting `container-type` — `@container` rules silently have no effect without it
- Setting `container-type: size` without giving the container an explicit height — the container collapses to zero block-size and the query never matches
- Querying an ancestor that is also the element you are styling — a container cannot query itself; you need a wrapper
- Using style queries in Firefox without a fallback — they are silently ignored but the base styles remain

## See Also

- [Container Query Units](container-units.md) → sizing elements relative to their container
- Reference: [MDN Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)
