---
description: Container query craft — component layout morphing, adaptive typography with cqi units, style queries, and when NOT to use container queries
tldr: "Use `@container` when a reusable component needs to change its layout based on the space its container gives it. Use `@media` for page-level structure, device preferences (dark mode, reduced motion), and print styles."
---

# Container Query Craft

## When to Use
When a reusable component — a card, sidebar widget, product tile, dashboard panel — needs to change its own layout based on the space its *container* gives it, not the viewport. Use this section for the **design craft**: how components morph, how typography adapts, how decoration shifts, and when NOT to reach for container queries at all.

For **feature syntax, `container-type` values, and browser support**, see [modern-css — Container Queries](../modern-css/container-queries.md).
For **unit reference (cqi, cqw, cqb, cqmin, cqmax)**, see [modern-css — Container Query Units](../modern-css/container-units.md).

## Decision: Container Queries vs Media Queries

| If you need... | Use... | Why |
|---|---|---|
| Component in sidebar AND main column, same markup | `@container` | Media query can't tell which column the component is in |
| Page-level column structure | `@media` | Viewport determines macro layout |
| Font size that scales inside a component | `cqi` + `clamp()` | Fluid without breakpoints, container-aware |
| Viewport font size (body copy) | `vw` + `clamp()` or just `rem` | `cqi` makes no sense when the container is the page |
| User preference: dark mode, reduced motion, hover | `@media` | These are device/OS features, not container concerns |
| Same card compact in a narrow slot, expanded in a wide one | `@container` | Container owns this decision |
| Global header / footer responsiveness | `@media` | They span the full viewport — container queries add no value |
| Print styles | `@media print` | Print is a media type, not a container concept |

**The rule of thumb:** Page layout lives in `@media`. Component layout lives in `@container`. Keep them separate.

## Pattern: Layout Morphing — Card Stack to Row

The foundational pattern — a card that stacks vertically in narrow containers and flips horizontal in wide ones:

```css
/* 1. Declare containment on the WRAPPER, not the card itself */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* 2. Base styles: stacked layout (narrow default) */
.card {
  display: grid;
  grid-template-areas: "image" "body" "footer";
  gap: var(--space-md, 1rem);
}

/* 3. Morph to horizontal when the container allows it */
@container card (min-width: 420px) {
  .card {
    grid-template-areas: "image body" "image footer";
    grid-template-columns: 160px 1fr;
  }
}
```

**The wrapper rule is non-negotiable.** A container cannot query itself. The containment context goes on the parent; the query rules target its children.

## Pattern: Adaptive Typography with Container Units

Font sizes that scale smoothly with the component's width — no breakpoint needed:

```css
.card-wrapper {
  container-type: inline-size;
}

.card__title {
  /* Scales from 1rem in narrow containers to 1.75rem in wide ones */
  font-size: clamp(1rem, 3cqi + 0.5rem, 1.75rem);
  line-height: clamp(1.3, 1.2 + 0.5cqi, 1.6);
}

.card__meta {
  /* Secondary text stays proportional */
  font-size: clamp(0.75rem, 2cqi, 1rem);
}
```

**Why `cqi` over `cqw`:** `cqi` is writing-mode-aware (inline-size in the document's writing direction). For most western layouts they are equivalent, but `cqi` is the semantically correct choice and handles RTL/vertical writing modes automatically. Prefer `cqi` as default.

**The `clamp()` floor matters.** Without a minimum, text can shrink below readable size in very narrow containers. Always set a `rem`-based floor.

## Pattern: Elevation and Decoration at Container Size

A card that presents more visual richness when it has room for it:

```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Compact: flat, minimal decoration */
.card {
  border-radius: 8px;
  box-shadow: none;
  padding: var(--space-sm, 0.5rem);
}

/* Expanded: elevated, decorative image visible */
@container card (min-width: 320px) {
  .card {
    box-shadow:
      0 1px 2px hsl(var(--shadow-color) / 0.08),
      0 4px 12px hsl(var(--shadow-color) / 0.06);
    padding: var(--space-md, 1rem);
  }

  .card__decorative-image { display: block; }
}

@container card (min-width: 540px) {
  .card {
    box-shadow:
      0 2px 4px hsl(var(--shadow-color) / 0.08),
      0 8px 24px hsl(var(--shadow-color) / 0.07),
      0 16px 40px hsl(var(--shadow-color) / 0.05);
  }
}
```

The shadow system values here are from [Elevation and Shadows](elevation-and-shadows.md). Container queries select *which elevation level* applies to the context.

## Pattern: Style Queries — Intent from Parent to Child

Style queries (`@container style()`) let a parent communicate intent to its children via CSS custom properties. The primary real-world use: a parent sets a flag, descendants react without needing extra classes.

```css
/* Parent sets the variant flag */
.sidebar {
  --layout-density: compact;
}

/* Child reads the flag */
@container style(--layout-density: compact) {
  .card {
    padding: var(--space-xs, 0.25rem);
    font-size: 0.875rem;
  }

  .card__image { display: none; }
  .card__tags  { display: none; }
}
```

**Style queries: progressive enhancement only.** Firefox does not yet support style queries (support expected mid-2026). Always write functional base styles — the style query adds enhancement, not core layout.

**Style queries vs data attributes:** For most cases, a `data-density="compact"` attribute plus CSS `[data-density="compact"] .card {}` is simpler, universally supported, and easier to debug. Use style queries when: (a) the container value originates in CSS and propagating it to HTML is awkward, or (b) server-rendered templates where adding attributes requires template changes.

## Pattern: Sidebar Widget — Real-World Example

A dashboard widget that works in a full-width row, a 3-column grid, and a narrow sidebar without any different markup:

```css
.widget-wrapper {
  container: widget / inline-size;
}

/* Base — compact, single column (sidebar default) */
.widget {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 0.5rem;
  padding: 0.75rem;
}

.widget__chart { aspect-ratio: 2 / 1; }

/* Medium — add a side panel */
@container widget (min-width: 380px) {
  .widget {
    grid-template-columns: 1fr 140px;
    grid-template-rows: auto 1fr;
    gap: 1rem;
    padding: 1.25rem;
  }

  .widget__stats {
    grid-column: 2;
    grid-row: 1 / -1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
}

/* Wide — full layout, legend visible */
@container widget (min-width: 600px) {
  .widget__legend { display: flex; }
  .widget__chart   { aspect-ratio: 16 / 5; }
}
```

## Anti-Patterns

**Adding containment everywhere "just in case"** — `container-type: inline-size` disables percentage-based heights on children (block-size containment side effect). Only add containment where you have a real `@container` rule consuming it.

**Querying the wrong container** — when multiple containers exist in the ancestor chain, `@container` matches the nearest one by default. If you mean a specific ancestor, use `container-name` and query it by name. Unnamed container queries on deeply nested components silently match the wrong container.

**Using container queries for layout that belongs in media queries** — a full-page hero section that changes at 768px is responding to the *viewport*, not the component's context. Using `@container` here adds a meaningless wrapper element and confuses the intent.

**Setting `container-type: size`** without giving the container an explicit height — the container collapses to zero block-size and all size queries involving height fail silently.

**Relying on style queries as primary functionality** — style queries are progressive enhancement (no Firefox). If a compact layout is required, implement it via size queries or class attributes, not style queries alone.

**Deeply nesting containment contexts** — each `container-type` boundary creates an isolated subtree for layout. 5-6 levels of nested containers is rarely justified; diagnose whether a simpler CSS structure removes the need.

## Performance

Container queries are **net-positive for performance** in component architectures. `container-type: inline-size` tells the browser the element's inline size does not depend on its descendants — the browser can isolate layout recalculations to that subtree rather than recalculating the full document.

- Avoid `container-type: size` — querying both axes requires the browser to do more work and forces the container to have an explicit height, which adds layout constraints
- Avoid style queries inside animation loops — style queries recalculate when custom properties change; triggering this from a `@keyframes` or `transition` that affects a custom property can create expensive recalculation chains
- Container query units (`cqi`, `cqw`) are computed at style resolution, not layout — they are cheap. No performance concern with using them in place of `vw`/`vh`

## Common Mistakes
- Putting `container-type` on the element with the `@container` rules — the container and its query targets must be parent/child; a container cannot query itself
- Forgetting `container-name` when there are multiple containers in the ancestor chain — the nearest unnamed container wins, which is often the wrong one
- Using `container-type: size` when only width matters — `inline-size` is almost always sufficient and avoids height-collapse issues
- Breaking percentage heights inside contained elements — `container-type: inline-size` establishes size containment only on the inline axis, but height percentages on children can still be affected; test explicitly
- Writing style queries as the only mechanism for required functionality — they are still Firefox-unsupported; base functionality must not depend on them

## See Also
- ← [Gradient Craft](gradient-craft.md) | [Quick Reference: Recommended Defaults](quick-reference-recommended-defaults.md) →
- Feature syntax and browser support: [modern-css — Container Queries](../modern-css/container-queries.md)
- Unit reference: [modern-css — Container Query Units](../modern-css/container-units.md)
- Shadow values used in elevation patterns: [Elevation and Shadows](elevation-and-shadows.md)
- Reference: [MDN Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)
- Reference: [MDN Container size and style queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries)
- Reference: [Smashing Magazine: What Are CSS Container Style Queries Good For?](https://www.smashingmagazine.com/2024/06/what-are-css-container-style-queries-good-for/)
- Reference: [Josh W. Comeau: Container Queries Unleashed](https://www.joshwcomeau.com/css/container-queries-unleashed/)
- Reference: [LogRocket: Container Queries in 2026](https://blog.logrocket.com/container-queries-2026/)
- Reference: [Modern CSS: Container Query Units and Fluid Typography](https://moderncss.dev/container-query-units-and-fluid-typography/)
