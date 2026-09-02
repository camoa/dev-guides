---
description: Implement accessible focus rings, screen reader utilities, reduced motion, ARIA state variants, and color contrast in Tailwind.
tldr: "Apply to every interactive component. Accessibility is a correctness requirement, not an optional feature."
---

# Accessibility

## When to Use

> Every component that involves interaction, visual presentation, or dynamic state. Accessibility isn't a feature — it's a correctness requirement.

## Decision

| A11y need | Tailwind approach |
|-----------|--------------------|
| Keyboard focus rings | `focus-visible:outline-2 focus-visible:outline-brand-500 focus-visible:outline-offset-2` |
| Remove default outline (replace it) | `focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500` |
| Visually hidden but screen-reader accessible | `sr-only` |
| Show element only when focused | `sr-only focus:not-sr-only` |
| Skip link (keyboard navigation) | `sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4` |
| Reduced motion | `motion-reduce:transition-none` or `motion-safe:animate-spin` |
| High contrast mode | `contrast-more:border-gray-600 contrast-more:text-gray-900` |
| Forced colors (Windows HCM) | `forced-colors:appearance-auto` |
| ARIA state → style | `aria-expanded:rotate-180`, `aria-pressed:bg-brand-700` |
| Disabled state | `disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none` |

## Pattern — Accessible Button with All States

```html
<button
  type="button"
  class="
    inline-flex items-center gap-2 px-4 py-2
    bg-brand-500 text-white rounded-lg font-semibold
    hover:bg-brand-600
    focus:outline-none
    focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
    active:scale-95
    disabled:opacity-50 disabled:cursor-not-allowed
    transition-colors duration-150
    motion-reduce:transition-none
    aria-pressed:bg-brand-700
  "
>
  <span class="sr-only">Toggle sidebar</span>
  <svg aria-hidden="true" class="size-5">...</svg>
</button>
```

## Pattern — Skip Navigation Link

```html
<!-- First element in <body> -->
<a
  href="#main-content"
  class="
    sr-only
    focus:not-sr-only
    focus:absolute focus:top-4 focus:left-4 focus:z-50
    focus:bg-white focus:px-4 focus:py-2 focus:rounded focus:shadow-lg
    focus:text-brand-500 focus:font-semibold
  "
>
  Skip to main content
</a>
```

## Pattern — Icon-Only Action

```html
<!-- Screen readers read the sr-only text; sighted users see only the icon -->
<button type="button" class="p-2 rounded hover:bg-gray-100 focus-visible:ring-2">
  <span class="sr-only">Close dialog</span>
  <svg aria-hidden="true" class="size-5 text-gray-600">...</svg>
</button>
```

## Color Contrast Reference

Tailwind default palette passing WCAG AA (4.5:1 for normal text):

| Background | Text | Ratio | Status |
|------------|------|-------|--------|
| `white` | `gray-700` | 10.0:1 | AAA |
| `white` | `gray-500` | 4.4:1 | AA (borderline) |
| `brand-500` | `white` | Verify with tool | Depends on brand color |
| `gray-900` | `gray-100` | 17.7:1 | AAA |

**Always verify brand colors** with a contrast checker — oklch color values don't map predictably to WCAG ratios without measurement. Use [Colour Contrast Checker](https://colour-a11y.vercel.app/) for Tailwind-aware checking.

## ARIA State Variants

```html
<!-- Tab pattern — ARIA state drives visual indicator -->
<button
  role="tab"
  aria-selected="true"
  class="
    px-4 py-2 font-medium
    aria-selected:border-b-2 aria-selected:border-brand-500 aria-selected:text-brand-500
    not-aria-selected:text-gray-600
  "
>
  Overview
</button>
```

Built-in ARIA variants: `aria-checked:`, `aria-disabled:`, `aria-expanded:`, `aria-hidden:`, `aria-pressed:`, `aria-readonly:`, `aria-required:`, `aria-selected:`

## Common Mistakes

- **`outline-none` with no replacement focus style** — fails WCAG 2.4.7; keyboard users cannot determine focus position
- **Using color alone to convey state** — color-blind users need shape, text, or icon cues alongside color changes
- **Animating elements without `motion-reduce:`** — some users have vestibular disorders; spinning/sliding elements trigger physical symptoms
- **`disabled:opacity-50` without `disabled:pointer-events-none`** — cursor still shows pointer, confusing users

## See Also

- [Best Practices & Anti-Patterns](best-practices.md)
- Design System Recognition Guide (element identification)
- [Utility Class Reference](utility-class-reference.md)
- Reference: https://tailwindcss.com/docs/hover-focus-and-other-states
- Reference: https://accreditly.io/articles/make-the-web-accessible-with-tailwind-css
