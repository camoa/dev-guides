---
description: Tailwind best practices and anti-patterns — utility-first philosophy, class organization, security, and when to extract abstractions.
---

# Best Practices & Anti-Patterns

## When to Use

> Reference before code review, architecture decisions, or when evaluating whether a Tailwind implementation is idiomatic.

## Core Philosophy

Utility-first means utilities are the default, and abstractions are earned through genuine reuse. Write utilities in markup until a real pattern emerges across multiple files.

## Development Standards

| Practice | Do | Don't |
|----------|----|----|
| Class organization | Layout → sizing → spacing → typography → color → effects → state | Random order |
| Token usage | All colors/sizes from `@theme` tokens | Raw hex values in reusable components |
| Responsive | Mobile-first with `sm:`, `md:` prefixes | Desktop-first with `max-*` as primary |
| Focus styles | `focus-visible:` for keyboard rings | `focus:` or bare `outline-none` |
| Dynamic values | Static class lookup maps | String interpolation (`bg-${color}-500`) |

## Anti-Patterns

1. **Recreating Bootstrap with @apply** — `@apply` compiles utilities back into CSS. When a color changes, you update the token AND hunt down every `@apply` reference. Use framework components instead.

2. **Fighting the spacing scale** — Using `p-[13px]` consistently signals a mismatch between design and the token system. Fix the token, not the utility.

3. **Inconsistent color references** — Mixing `bg-blue-500`, `bg-[#3b82f6]`, and `bg-primary` for the same color. Pick the token and use it everywhere.

4. **Ignoring the extraction signal** — Copy-pasting 8+ utility classes across files more than twice = create a framework component. The markup IS the component contract.

5. **Arbitrary values for design system values** — `w-[340px]` used consistently means `340px` belongs in `@theme`. Arbitrary values are for truly one-off cases.

6. **Overloading @layer components** — 20+ classes in `@layer components` means you've rebuilt Bootstrap. Step back; these should be framework components or inline utilities.

## Security Standards

- **Never build Tailwind class names from user input** — `bg-${userColorPreference}-500` creates a surface where users can influence what CSS is generated or cached.
- **Sanitize class attributes** — if user-provided data renders as CSS class attributes in HTML, sanitize it; non-existent class names can be used for CSS injection.
- **Validate token values from APIs or CMS** — malformed oklch values won't cause XSS but may break rendering.

## Performance Standards

- Avoid safelisting entire color scales when you only need 3 shades — `@source inline` generates CSS at build time.
- Tailwind's output is already tree-shaken; the developer cost is class-name verbosity, not runtime performance.
- `@container` adds no JavaScript; it's pure CSS.
- Prefer `transition-colors duration-200` over JS-driven class toggling for simple state changes.

## Common Mistakes

- **Wrong**: Using Tailwind like a utility-class version of Bootstrap — the mental model is wrong; utilities are composable primitives. **Right**: Write markup-first, extract only when duplication is proven.
- **Wrong**: Starting with component extraction before seeing real duplication — YAGNI applies.
- **Wrong**: Defining `--color-brand-150` in `@theme` but never using `bg-brand-150`. **Right**: Over-configured tokens add dead weight.

## See Also

- [Accessibility](accessibility.md)
- [Performance Optimization](performance-optimization.md)
- [@apply Guidance](apply-guidance.md)
- Reference: https://www.faraazcodes.com/blog/tailwind-2025-best-practices
