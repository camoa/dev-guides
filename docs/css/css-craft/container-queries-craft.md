---
description: Container query craft — component layout morphing, adaptive typography with cqi units, style queries, and when NOT to use container queries
tldr: "Use `@container` when a reusable component needs to change its layout based on the space its container gives it. Use `@media` for page-level structure, device preferences (dark mode, reduced motion), and print styles."
---

# Container Query Craft

## When to Use

> Use `@container` when a reusable component needs to change its layout based on the space its container gives it. Use `@media` for page-level structure, device preferences (dark mode, reduced motion), and print styles.

For feature syntax, `container-type` values, and browser support, see [modern-css — Container Queries](../modern-css/container-queries.md).
For unit reference (`cqi`, `cqw`, `cqb`, `cqmin`, `cqmax`), see [modern-css — Container Query Units](../modern-css/container-units.md).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Component in sidebar AND main column, same markup | `@container` | Media query cannot tell which column the component is in |
| Page-level column structure | `@media` | Viewport determines macro layout |
| Font size that scales inside a component | `cqi` + `clamp()` | Fluid without breakpoints, container-aware |
| Viewport font size (body copy) | `vw` + `clamp()` or `rem` | `cqi` makes no sense when the container is the page |
| User preference: dark mode, reduced motion, hover | `@media` | These are device/OS features, not container concerns |
| Same card compact in narrow slot, expanded in wide slot | `@container` | Container owns this decision |
| Global header / footer responsiveness | `@media` | They span the full viewport — container queries add no value |
| Print styles | `@media print` | Print is a media type, not a container concept |

**Rule of thumb:** Page layout lives in `@media`. Component layout lives in `@container`. Keep them separate.

## Pattern

### Layout Morphing — Card Stack to Row

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

The wrapper rule is non-negotiable. A container cannot query itself — containment goes on the parent, query rules target its children.

### Adaptive Typography with Container Units

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
  font-size: clamp(0.75rem, 2cqi, 1rem);
}
```

Prefer `cqi` over `cqw` — `cqi` is writing-mode-aware and handles RTL/vertical writing modes automatically. Always set a `rem`-based floor in `clamp()` to prevent text shrinking below readable size in very narrow containers.

### Elevation and Decoration at Container Size

```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

.card { border-radius: 8px; box-shadow: none; padding: var(--space-sm, 0.5rem); }

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

### Style Queries — Intent from Parent to Child

```css
/* Parent sets the variant flag */
.sidebar { --layout-density: compact; }

/* Child reads the flag */
@container style(--layout-density: compact) {
  .card { padding: var(--space-xs, 0.25rem); font-size: 0.875rem; }
  .card__image { display: none; }
  .card__tags  { display: none; }
}
```

Style queries are progressive enhancement only — Firefox support expected mid-2026. Always write functional base styles; the style query adds enhancement, not core layout. For most cases, `data-density="compact"` + `[data-density="compact"] .card {}` is simpler and universally supported.

### Sidebar Widget — Real-World Example

```css
.widget-wrapper { container: widget / inline-size; }

/* Base — compact, single column */
.widget { display: grid; grid-template-rows: auto 1fr auto; gap: 0.5rem; padding: 0.75rem; }
.widget__chart { aspect-ratio: 2 / 1; }

/* Medium — add a side panel */
@container widget (min-width: 380px) {
  .widget {
    grid-template-columns: 1fr 140px;
    grid-template-rows: auto 1fr;
    gap: 1rem; padding: 1.25rem;
  }
  .widget__stats { grid-column: 2; grid-row: 1 / -1; display: flex; flex-direction: column; gap: 0.5rem; }
}

/* Wide — full layout, legend visible */
@container widget (min-width: 600px) {
  .widget__legend { display: flex; }
  .widget__chart  { aspect-ratio: 16 / 5; }
}
```

## Common Mistakes

- **Wrong**: Adding `container-type: inline-size` everywhere "just in case" → **Right**: Only add containment where you have a real `@container` rule consuming it. Containment disables percentage-based heights on children.
- **Wrong**: Relying on unnamed `@container` in deeply nested components → **Right**: Use `container-name` and query by name so you match the intended ancestor, not the nearest one silently.
- **Wrong**: Using `@container` for a full-page hero that responds to viewport width → **Right**: Use `@media` — it's responding to the viewport, not the component's context.
- **Wrong**: `container-type: size` without an explicit height on the container → **Right**: Give the container an explicit height or the container collapses to zero block-size and height queries fail silently.
- **Wrong**: Style queries as primary layout logic (Firefox unsupported) → **Right**: Implement required layouts via size queries or class attributes; use style queries for progressive enhancement only.

## See Also

- [Elevation and Shadows](elevation-and-shadows.md)
- [Modern CSS Craft Patterns](modern-css-craft-patterns.md)
- Reference: `~/workspace/claude_memory/guides/css-craft.md` — Container Query Craft section
- Reference: MDN — [CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries)
- Reference: MDN — [Container query units](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_size_and_style_queries#container_query_length_units)
