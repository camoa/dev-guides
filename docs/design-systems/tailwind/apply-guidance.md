---
description: Know when @apply is appropriate (CMS content, base elements) versus when it fights the utility-first model.
tldr: "Use `@apply` only when you don't control the HTML being styled. In Tailwind v4, `@apply` on a class defined in `@layer components` is a hard build failure, not just a style smell."
---

# @apply: When to Use / Avoid

## When to Use

> `@apply` compiles utility classes back into CSS declarations. It has legitimate uses but is widely misused.

## Decision

**Use `@apply` when:**

- Writing styles for HTML you don't control (third-party widgets, CMS output, markdown)
- Creating base element styles in `@layer base` for consistent prose rendering
- The component abstraction is too heavyweight (pure HTML partials, no JS framework)

**Avoid `@apply` when:**

- You have framework components available — extract into a component instead
- You're recreating Bootstrap-style component classes (`btn`, `card`) — this fights the utility-first model
- Composing complex multi-state styles — you lose the visual clarity of seeing all states in markup

## Pattern

```css
/* ✓ Appropriate @apply — styling CMS-generated content */
@layer base {
  .cms-content h2 { @apply text-2xl font-bold mt-8 mb-4; }
  .cms-content p  { @apply text-base leading-relaxed mb-4; }
  .cms-content a  { @apply text-brand-500 underline hover:text-brand-700; }
}
```

## Common Mistakes

```css
/* ✗ Inappropriate @apply — recreating Bootstrap */
@layer components {
  .btn { @apply inline-flex items-center px-4 py-2 rounded-lg font-medium; }
  .btn-primary { @apply btn bg-brand-500 text-white hover:bg-brand-600; }
  /* Now you have a parallel class system — maintain two things instead of one */
}
```

In v4 that second rule does not just read badly — it fails the build. `@apply` accepts utilities only, and a class you defined in `@layer components` is not one, so `@apply btn` aborts compilation with `Cannot apply unknown utility class btn` (verified against tailwindcss 4.2.0). v3 inlined it without complaint (verified against tailwindcss 3.4.19), so this is a breaking change an upgrade surfaces as a build failure. If you need a name you can compose, register it with `@utility btn { ... }` — `@apply btn` then resolves. For variant composition, use CVA instead.

## See Also

- [Component Patterns](component-patterns.md)
- [Class Variance Authority](class-variance-authority.md)
- Reference: https://tailwindcss.com/docs/styling-with-utility-classes#managing-duplication
