---
description: Extend DaisyUI components with Tailwind utilities, CSS variable overrides, and global layer overrides; know when custom components are correct
tldr: "Extending DaisyUI components with project-specific styles, overriding defaults, and creating custom components that follow DaisyUI conventions. Work through native primitive → composite → custom in order and stop at the first that fits."
---

# Customization Patterns

## When to Use

> Extending DaisyUI components with project-specific styles, overriding defaults, and creating custom components that follow DaisyUI conventions.

## Decision: How to Customize

| If you need to... | Do this | Why |
|---|---|---|
| Add spacing/layout to a DaisyUI component | Tailwind utilities on the element | `<div class="card mt-8 w-full">` — utilities compose cleanly |
| Change a color on a specific instance | Tailwind utilities override CSS vars | `<button class="btn [--btn-color:theme(colors.purple.600)]">` |
| Create a reusable component variant | CSS custom properties + new class | Avoid `@apply` — use CSS variable overrides |
| Override component globally across the project | `@layer daisyui.l1.l2` in CSS | Match DaisyUI's layer structure |
| Create a new component following DaisyUI patterns | New CSS class using DaisyUI tokens | Reuse `--color-primary`, `--radius-field`, etc. |

## Pattern: Extending with Tailwind Utilities

DaisyUI component classes and Tailwind utilities compose cleanly:

```html
<!-- Layout and spacing: Tailwind. Color variant: DaisyUI -->
<button class="btn btn-primary mt-4 w-full max-w-xs">
  Submit
</button>

<!-- Combining display utilities with DaisyUI card -->
<div class="card bg-base-100 hidden lg:flex">
  <div class="card-body">...</div>
</div>
```

## Pattern: CSS Variable Override on Instance

DaisyUI v5 components expose internal CSS variables. Override them inline:

```html
<!-- Override the internal --btn-color for a one-off color -->
<button class="btn" style="--btn-color: oklch(0.7 0.2 30);">Custom</button>

<!-- Override radius for this specific card -->
<div class="card" style="--radius-box: 1.5rem;">Rounded card</div>
```

Source: `components/button/object.js` shows `--btn-color` as the primary color variable, `--btn-fg` as foreground.

## Pattern: Custom Component Using DaisyUI Tokens

When creating a component that should honor the active theme:

```css
/* In your app's CSS */
.my-status-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-selector);     /* DaisyUI token */
  border: var(--border) solid currentColor; /* DaisyUI token */
  font-size: 0.75rem;
  font-weight: 600;
}

.my-status-chip-active {
  color: var(--color-success);
}

.my-status-chip-inactive {
  color: var(--color-base-content);
  opacity: 0.5;
}
```

## Pattern: Overriding DaisyUI Globally

```css
/* Override in the correct layer to win specificity battles */
@layer daisyui.l1.l2 {
  .btn {
    font-weight: 700;           /* Heavier weight project-wide */
    letter-spacing: 0.025em;
  }

  .card {
    --radius-box: 0.75rem;      /* Rounder cards project-wide */
  }
}
```

Source: DaisyUI uses `@layer daisyui.l1.l2.l3` — overrides in `daisyui.l1.l2` win over component defaults.

## Pattern: Prefix for Multi-Library Projects

When using DaisyUI alongside another component library with conflicting class names:

```css
@plugin "daisyui" {
  prefix: "d-";
}
```

All classes become `d-btn`, `d-card`, `d-modal`. Add prefix to every DaisyUI class in templates.

## When Custom Is Correct

Before building anything, work through these tiers in order and stop at the first that fits. This is a rule, not a suggestion.

1. **Native primitive** — DaisyUI has a primitive that fits the component's role and interaction model. Use it.
2. **Composite** — no single primitive fits, but composing two or more primitives covers the need without structural workarounds. Use that.
3. **Custom** — no native primitive fits and composing primitives would require fighting the primitives' intent. Custom is correct here.

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

### Canonical "custom is correct" categories

These have no DaisyUI native primitive and resist clean composition from existing ones. Custom is the unambiguous right answer here.

| Category | Why custom is correct |
|---|---|
| Dashboards / widget grids | No dashboard primitive. Layout is bespoke; widgets are domain-specific |
| Complex data tables | DaisyUI's `table` is presentational only. Sort, filter, inline edit, and virtual scroll require custom structure |
| Charts / data visualizations | No native primitive. Use a charting library; DaisyUI provides tokens only |
| Kanban / drag-and-drop boards | No native primitive. Column-and-card structure is fully bespoke |
| Calendar grids / scheduling UI | No native primitive. Grid and event positioning are custom layout problems |
| Brand-signature sections | Bespoke layouts (unique hero, split-screen, full-bleed editorial). No primitive matches |
| Image masonry / unique grid layouts | Beyond what DaisyUI's `grid` or `stack` primitives cover; layout logic is custom |

### Token rule for custom components

Custom components **must** consume DaisyUI design tokens for color, spacing, and typography — not hardcoded values. Direct hex or rgb values bypass theming and break multi-theme support.

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

Custom markup and DaisyUI tokens are not in conflict. The tokens work in any CSS context — no DaisyUI class is required on the element to use `var(--color-primary)`.

## Common Mistakes

- Using `@apply btn btn-primary` in CSS — creates selector bloat and the class no longer responds to `btn-ghost`/`btn-outline` overrides because the CSS was inlined at build time. Use the class directly in HTML
- Overriding DaisyUI without matching layer — styles outside `@layer daisyui.*` have higher or unpredictable specificity
- Changing `--color-primary` directly in a component — this changes it globally in the current theme scope. Use component-level variables (`--btn-color`) instead

## See Also

- [DaisyUI and React](daisyui-react.md) — React CVA patterns with DaisyUI classes
- [Best Practices](best-practices.md)
- Reference: `design-system-tailwind.md` Section 10.1 — `@apply` guidance
