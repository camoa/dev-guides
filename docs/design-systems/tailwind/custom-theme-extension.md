---
description: Add custom utilities, variants, animations, and shared themes beyond what design tokens alone provide in Tailwind v4.
tldr: "Use when adding project-specific utilities, custom variants, animations, or sharing a theme across a monorepo."
---

# Custom Theme Extension

## When to Use

> Adding project-specific utilities, variants, animations, or extending beyond what design tokens alone provide.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| New CSS property Tailwind doesn't cover | `@utility` directive | Participates in Tailwind's variant system |
| Brand animation | `@theme { --animate-* }` with `@keyframes` inside | Generates `animate-` utilities |
| Multi-theme (admin vs. public) | `@custom-variant` | Creates scoped variants without duplicating utility classes |
| One-off value | Arbitrary syntax `w-[340px]` | Zero config cost; fine for one-off values |
| Repeated one-off value (>3 times) | Add to `@theme` | Converts arbitrary to token; enforces consistency |
| Plugin (v3) | `plugins: [require('@tailwindcss/forms')]` | Third-party style integration |

## Pattern — Custom Utilities and Variants

```css
@import "tailwindcss";

/* Custom utility — participates in hover:, md:, etc. */
@utility content-auto {
  content-visibility: auto;
}

/* Functional utility with value from theme */
@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
}
@utility tab-* {
  tab-size: --value(--tab-size-*);
}

/* Custom animation with keyframes inside @theme */
@theme {
  --animate-slide-up: slide-up 0.3s var(--ease-spring) both;

  @keyframes slide-up {
    from { transform: translateY(0.5rem); opacity: 0; }
    to   { transform: translateY(0); opacity: 1; }
  }
}

/* Custom variant — theme toggle via data attribute */
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
```

## Pattern — Sharing Theme Across Projects (Monorepo)

```css
/* packages/brand/theme.css */
@theme {
  --color-brand-500: oklch(0.65 0.18 260);
  --font-display: "Inter", sans-serif;
}
```
```css
/* apps/website/styles.css */
@import "tailwindcss";
@import "@company/brand/theme.css";

/* Project-specific extensions */
@theme {
  --color-sidebar-bg: var(--color-brand-50);
}
```

## @layer in v4 (for non-utility custom CSS)

```css
/* Base styles — unscoped element styles */
@layer base {
  *, *::before, *::after { box-sizing: border-box; }
  h1 { font-size: var(--text-2xl); font-weight: var(--font-weight-bold); }
}

/* Component classes — use sparingly, prefer framework components */
@layer components {
  .prose-content {
    color: var(--color-gray-700);
    line-height: var(--leading-relaxed);
  }
}
```

## Common Mistakes

- **Writing `@layer utilities` for custom utilities in v4** — use `@utility` directive; `@layer utilities` still works but `@utility` integrates properly with variants
- **Putting animation `@keyframes` outside `@theme` and expecting `animate-` utilities** — keyframes inside `@theme` are co-located with the token that uses them
- **Creating shared themes via JavaScript object spreading instead of CSS `@import`** — the CSS approach works across any stack; JS sharing requires a JS build chain

## See Also

- [Component Patterns](component-patterns.md)
- Reference: https://tailwindcss.com/docs/adding-custom-styles
