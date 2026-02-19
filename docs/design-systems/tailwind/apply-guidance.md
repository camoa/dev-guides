---
description: Know when @apply is appropriate (CMS content, base elements) versus when it fights the utility-first model.
---

# @apply: When to Use / Avoid

## When to Use

> Use `@apply` only when you don't control the HTML being styled. Avoid it when framework components are available.

## Decision

| Situation | Use @apply? | Why |
|-----------|------------|-----|
| Styling CMS-generated HTML output | Yes | You don't control the markup |
| Base element styles in `@layer base` for prose | Yes | Consistent typography for unclassed HTML |
| Pure HTML partials with no JS framework | Yes | Component abstraction is too heavyweight |
| You have React/Vue/Twig components available | No | Extract into a component instead |
| Recreating Bootstrap-style component classes | No | Fights the utility-first model |
| Multi-state component styles | No | You lose visual clarity of seeing all states in markup |

## Pattern

```css
/* Appropriate @apply — styling CMS-generated content */
@layer base {
  .cms-content h2 { @apply text-2xl font-bold mt-8 mb-4; }
  .cms-content p  { @apply text-base leading-relaxed mb-4; }
  .cms-content a  { @apply text-brand-500 underline hover:text-brand-700; }
}
```

```css
/* Inappropriate @apply — recreating Bootstrap-style classes */
@layer components {
  .btn { @apply inline-flex items-center px-4 py-2 rounded-lg font-medium; }
  .btn-primary { @apply btn bg-brand-500 text-white hover:bg-brand-600; }
  /* Now you maintain class names AND utilities — two things instead of one */
}
```

## Why @apply Creates Problems

`@apply` compiles utility classes back into CSS declarations. When a color token changes, you update the token but must also hunt down every `@apply` reference. The single-source-of-truth benefit of utilities is lost.

## Common Mistakes

- **Wrong**: Using `@apply` to build a class system when you have framework components available — the component IS the abstraction.
- **Wrong**: Using `@apply` for complex multi-state styles — you lose the visual map of all states that inline utilities provide.
- **Wrong**: Using `@apply` inside `.btn` and then composing with `@apply .btn` in `.btn-primary` (v4 removed this). **Right**: Use CVA for variant composition.

## See Also

- [Component Patterns](component-patterns.md)
- [Class Variance Authority](class-variance-authority.md)
- Reference: https://tailwindcss.com/docs/reusing-styles
