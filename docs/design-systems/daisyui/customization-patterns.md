---
description: Extend DaisyUI components with Tailwind utilities, CSS variable overrides, and global layer overrides
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

## See Also

- [DaisyUI and React](daisyui-react.md)
- [Best Practices](best-practices.md)
- Reference: `design-system-tailwind.md` Section 10.1 — `@apply` guidance
