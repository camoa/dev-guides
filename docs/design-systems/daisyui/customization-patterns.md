---
description: Extend DaisyUI components with Tailwind utilities, CSS variable overrides, and global layer overrides; know when custom components are correct
tldr: "Extending DaisyUI components with project-specific styles, overriding defaults, and creating custom components that follow DaisyUI conventions. Work through native primitive → composite → custom in order and stop at the first that fits."
---

# Customization Patterns

## When to Use

> Extending DaisyUI components with project-specific styles, overriding defaults, and creating custom components that follow DaisyUI conventions.

## Decision

| If you need to... | Do this | Why |
|-------------------|---------|-----|
| Add spacing/layout to a DaisyUI component | Tailwind utilities on the element | `<div class="card mt-8 w-full">` — composes cleanly |
| Change color on a specific instance | CSS variable override inline | Avoids changing the global theme |
| Create a reusable component variant | CSS custom properties + new class | Avoid `@apply` — use CSS variable overrides |
| Override component globally across the project | `@layer daisyui.l1.l2` in CSS | Matches DaisyUI's layer structure |
| Create a new component using DaisyUI tokens | New CSS class using DaisyUI tokens | Reuses `--color-primary`, `--radius-field`, etc. |

## When Custom Is Correct

Before building anything, work through these tiers in order and stop at the first that fits:

1. **Native primitive** — DaisyUI has a primitive that fits the component's role and interaction model. Use it.
2. **Composite** — no single primitive fits, but composing two or more primitives covers the need without structural workarounds. Use that.
3. **Custom** — no native primitive fits and composing primitives would require fighting their intent. Custom is correct here.

Only fall to custom when tiers 1 and 2 genuinely don't fit — not because custom is faster to prototype.

**Check all component-category guides before concluding no primitive exists:**

| Category | Guide |
|----------|-------|
| Actions — buttons, modals, swap, dropdown | [Actions Components](actions-components.md) |
| Data Display — badge, card, alert, stat, table, avatar, chat, timeline, tooltip | [Data Display Components](data-display-components.md) |
| Navigation — navbar, menu, tabs, breadcrumbs, dock, pagination | [Navigation Components](navigation-components.md) |
| Data Input — input, select, checkbox, toggle, file-input, rating, validator | [Data Input Components](data-input-components.md) |
| Layout — drawer, hero, divider, join, stack, footer, mask | [Layout Components](layout-components.md) |
| Mockup — mockup-browser, mockup-code, mockup-phone, mockup-window | [Mockup Components](mockup-components.md) |
| Feedback — loading, progress, skeleton, radial-progress | [Feedback Components](feedback-components.md) |

**Canonical "custom is correct" categories** — these have no native primitive and resist clean composition:

| Category | Why custom is correct |
|----------|-----------------------|
| Dashboards / widget grids | No dashboard primitive; layout is bespoke; widgets are domain-specific |
| Complex data tables | DaisyUI's `table` is presentational only; sort, filter, inline edit, virtual scroll require custom structure |
| Charts / data visualizations | No native primitive; use a charting library; DaisyUI provides tokens only |
| Kanban / drag-and-drop boards | No native primitive; column-and-card structure is fully bespoke |
| Calendar grids / scheduling UI | No native primitive; grid and event positioning are custom layout problems |
| Brand-signature sections | Bespoke layouts (unique hero, split-screen, full-bleed editorial); no primitive matches |
| Image masonry / unique grid layouts | Beyond what `grid` or `stack` primitives cover |

**Token rule for custom components** — custom components must consume DaisyUI design tokens for color, spacing, and typography:

```css
/* CORRECT — custom markup, DaisyUI tokens */
.my-dashboard-widget {
  background-color: var(--color-base-100);
  border: var(--border) solid var(--color-base-300);
  border-radius: var(--radius-box);
  color: var(--color-base-content);
}

/* WRONG — hardcoded values break theme switching */
.my-dashboard-widget {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  color: #111827;
}
```

## Pattern

### Extending with Tailwind Utilities

```html
<!-- Layout and spacing: Tailwind. Color variant: DaisyUI -->
<button class="btn btn-primary mt-4 w-full max-w-xs">Submit</button>
<div class="card bg-base-100 hidden lg:flex">
  <div class="card-body">...</div>
</div>
```

### CSS Variable Override on a Single Instance

```html
<!-- Override internal --btn-color for a one-off color -->
<button class="btn" style="--btn-color: oklch(0.7 0.2 30);">Custom</button>

<!-- Override radius for this specific card -->
<div class="card" style="--radius-box: 1.5rem;">Rounded card</div>
```

Source: `node_modules/daisyui/components/button/object.js` — `--btn-color` is the primary color variable; `--btn-fg` is foreground.

### Custom Component Using DaisyUI Tokens

```css
.my-status-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-selector);
  border: var(--border) solid currentColor;
  font-size: 0.75rem;
  font-weight: 600;
}
.my-status-chip-active { color: var(--color-success); }
.my-status-chip-inactive { color: var(--color-base-content); opacity: 0.5; }
```

### Global Override in Correct Layer

```css
@layer daisyui.l1.l2 {
  .btn {
    font-weight: 700;
    letter-spacing: 0.025em;
  }
  .card {
    --radius-box: 0.75rem;
  }
}
```

DaisyUI uses `@layer daisyui.l1.l2.l3` — overrides in `daisyui.l1.l2` win over component defaults.

### Prefix for Multi-Library Projects

```css
@plugin "daisyui" {
  prefix: "d-";
}
```

All classes become `d-btn`, `d-card`, `d-modal`. Required when using DaisyUI alongside another library with conflicting class names.

## Common Mistakes

- **Wrong**: `@apply btn btn-primary` in CSS — **Right**: Use the class directly in HTML; `@apply` inlines CSS at build time, breaking modifier classes like `btn-ghost`
- **Wrong**: Overriding DaisyUI without matching the layer — **Right**: Styles outside `@layer daisyui.*` have unpredictable specificity
- **Wrong**: Changing `--color-primary` directly on a component — **Right**: This changes it globally in the current theme scope; use component-level variables (`--btn-color`) instead
- **Wrong**: Building custom when a native primitive fits — **Right**: Work through native → composite → custom in order

## See Also

- [DaisyUI and React](daisyui-react.md)
- [Best Practices](best-practices.md)
- Reference: `design-system-tailwind.md` Section 10.1 — `@apply` guidance
