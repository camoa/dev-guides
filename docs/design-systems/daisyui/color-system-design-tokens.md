---
description: Reference for DaisyUI CSS variables, semantic color tokens, and how to use them as Tailwind utility classes
tldr: "Use this guide when you need to understand which CSS variables control which visual properties, and how to use DaisyUI semantic colors as Tailwind utility classes."
---

# Color System and Design Tokens

## When to Use

> Understanding which CSS variables control which visual properties, and how to use DaisyUI colors as Tailwind utility classes.

## Decision: Which Token for Which Job

| Situation | Use | Why |
|-----------|-----|-----|
| Page/card background | `bg-base-100` | Primary background token |
| Secondary background (table rows, sidebar) | `bg-base-200` | One step down from page background |
| Default text | `text-base-content` | Always readable on base backgrounds |
| Brand/CTA elements | `bg-primary` / `text-primary-content` | Semantic — adapts to all themes |
| Status/state indication | `bg-error` / `bg-success` / `bg-warning` | Semantic state colors |
| Shade suffixes like `bg-primary-500` | Never | DaisyUI colors have no shade suffixes |

## CSS Variables Reference

DaisyUI registers these variables per theme (source: `node_modules/daisyui/functions/variables.js`).

### Surface Colors (backgrounds, text, borders)

| Variable | Role | Light default |
|----------|------|---------------|
| `--color-base-100` | Primary background (page, cards) | `oklch(100% 0 0)` (white) |
| `--color-base-200` | Secondary background (table rows, sidebar) | `oklch(98% 0 0)` |
| `--color-base-300` | Tertiary background (borders, dividers) | `oklch(95% 0 0)` |
| `--color-base-content` | Default text color on base backgrounds | `oklch(21% 0.006 285)` |

### Semantic Colors

| Variable | Role |
|----------|------|
| `--color-primary` / `--color-primary-content` | Brand/CTA — buttons, links |
| `--color-secondary` / `--color-secondary-content` | Secondary brand accent |
| `--color-accent` / `--color-accent-content` | Third brand color, highlights |
| `--color-neutral` / `--color-neutral-content` | Dark, saturated — active menu items |
| `--color-info` / `--color-info-content` | Informational states (blue) |
| `--color-success` / `--color-success-content` | Positive/success states (green) |
| `--color-warning` / `--color-warning-content` | Warning states (amber) |
| `--color-error` / `--color-error-content` | Error/danger states (red) |

### Shape and Depth Tokens

| Variable | Role | Light default |
|----------|------|---------------|
| `--radius-box` | Border radius for cards, modals | `0.5rem` |
| `--radius-field` | Border radius for inputs, buttons | `0.25rem` |
| `--radius-selector` | Border radius for checkboxes, badges | `0.5rem` |
| `--border` | Default border width | `1px` |
| `--depth` | Shadow/3D depth intensity (0=flat) | `1` |
| `--noise` | Texture noise intensity (0=none) | `0` |

## Using DaisyUI Colors as Tailwind Classes

DaisyUI extends Tailwind's color palette so all semantic colors work as utility classes:

```html
<!-- These all work as standard Tailwind utilities -->
<div class="bg-base-200 text-base-content border-base-300">
  <p class="text-primary">Primary colored text</p>
  <span class="bg-error text-error-content">Error state</span>
</div>
```

The Tailwind extension is defined in `node_modules/daisyui/functions/variables.js`:

```js
colors: {
  "base-100": "var(--color-base-100)",
  "primary": "var(--color-primary)",
  // ... all 22 color tokens
},
borderRadius: {
  "selector": "var(--radius-selector)",
  "field": "var(--radius-field)",
  "box": "var(--radius-box)",
}
```

## Common Mistakes

- Using `bg-primary-500` style suffixes — DaisyUI colors have no shade suffixes. It's `bg-primary`, not `bg-primary-500`
- Hardcoding `oklch(...)` values in Tailwind utilities instead of using the semantic tokens — defeats theming
- Using the `-content` color on the wrong background — `primary-content` is readable on `primary` backgrounds only, not on `base-100`

## See Also

- [Theming System](theming-system.md) — how to define custom theme values
- [Customization Patterns](customization-patterns.md)
- Reference: `design-system-tailwind.md` Section 5 — Tailwind design token mapping
