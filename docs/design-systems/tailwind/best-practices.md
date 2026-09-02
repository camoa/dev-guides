---
description: Tailwind best practices and anti-patterns — utility-first philosophy, class organization, security, and when to extract abstractions.
tldr: "Reference before code review, architecture decisions, or when evaluating whether a Tailwind implementation is idiomatic."
---

# Best Practices & Anti-Patterns

## When to Use

> Reference before code review, architecture decisions, or when evaluating whether a Tailwind implementation is idiomatic.

## Core Philosophy: Utility-First Means Utilities First

Utility-first doesn't mean "utilities only" — it means utilities are the default, and abstractions are earned through genuine reuse. The wrong instinct is to immediately reach for `@apply` or component classes. The right instinct is to write utilities in markup until a real pattern emerges across multiple files.

## Development Standards

| Practice | Do | Don't |
|----------|----|-------|
| Class organization | Follow order: layout → sizing → spacing → typography → color → effects → state | Random order (maintenance nightmare) |
| Token usage | All colors/sizes from `@theme` tokens | Raw hex values (`bg-[#4f46e5]`) in reusable components |
| Responsive | Mobile-first with `sm:`, `md:` prefixes | Desktop-first with `max-*` as primary |
| Focus styles | `focus-visible:` for keyboard rings | `focus:` (shows on mouse clicks) or `outline-none` alone |
| Dynamic values | Static class lookup maps | String interpolation (`bg-${color}-500`) |

## Anti-Patterns with WHY

1. **Recreating Bootstrap with @apply** — `@apply` compiles utilities back into CSS, destroying the single-source-of-truth benefit. You now maintain class names AND utilities. When a color changes, you change the token AND hunt down every `@apply` reference.

2. **Fighting the spacing scale** — Tailwind's 4px scale (`p-1`=4px, `p-4`=16px, `p-8`=32px) is intentional. Using arbitrary values (`p-[13px]`) constantly signals a mismatch between design and the token system. Fix the token system, not the utilities.

3. **Inconsistent color references** — mixing `bg-blue-500`, `bg-[#3b82f6]`, and `bg-primary` for the same color across a project. Pick one: use the token everywhere. Inconsistency means three places to update when the brand color changes.

4. **Ignoring the component extraction signal** — if you copy-paste the same 8 utility classes more than twice across different files, that's your signal to create a framework component. The markup IS the component contract; don't extract to CSS.

5. **Arbitrary values for design system values** — `w-[340px]` used consistently means `340px` belongs in `@theme`. Arbitrary values are for truly one-off values that will never repeat.

6. **Overloading @layer components** — if you find yourself with 20+ classes in `@layer components`, you've rebuilt Bootstrap. Step back: these should be framework components (React/Vue/Twig/etc.) or they should be inline utilities.

## Security Standards

Tailwind itself has no server-side rendering or XSS vectors, but the surrounding implementation does:

- **Never build Tailwind class names from user input** — `bg-${userColorPreference}-500` used with Tailwind's safelist creates an attack surface where users can influence what CSS is generated or cached
- **Be careful with class injection** — if user-provided data is rendered as CSS class attributes in HTML, sanitize it; even non-existent class names can be used for CSS injection in frameworks that evaluate arbitrary selectors
- **Token values from untrusted sources** — if design tokens are loaded from an API or CMS, validate color values before injecting into `@theme`; malformed oklch values won't cause XSS but may break rendering

## Accessibility Standards

These are non-negotiable minimums — not optional:

- **Always use `focus-visible:` not `focus:`** for keyboard focus rings — `focus:` triggers on mouse clicks, degrading UX; `focus-visible:` only activates for keyboard navigation
- **Never use `outline-none` without a replacement** — `focus-visible:outline-none focus-visible:ring-2` is acceptable; bare `outline-none` makes the page unusable for keyboard users
- **Color contrast** — Tailwind's default palette satisfies WCAG AA at most shade combinations, but verify: `gray-500` on `white` is ~4.4:1 (borderline); `gray-600` on `white` is ~5.5:1 (clear pass)
- **Screen reader utilities** — use `sr-only` for accessible labels on icon-only buttons; use `not-sr-only` to conditionally reveal them
- **Motion** — wrap animations in `motion-safe:` or test with `motion-reduce:hidden`

## Performance Standards

- **Avoid N+1 class generation** — safelisting (`@source inline`) generates CSS at build time; don't safelist entire color scales when you only need 3 shades
- **The real performance cost is CSS size** — Tailwind's output is already tree-shaken; the developer cost is class-name verbosity, not runtime performance
- **Container queries are lightweight** — `@container` adds no JavaScript; it's pure CSS. Use freely.
- **Prefer CSS transitions over JavaScript animations** — `transition-colors duration-200` is faster than JS-driven class toggling for simple state changes

## Common Mistakes

- **Using Tailwind like a utility-class version of Bootstrap** — the mental model is wrong; utilities are composable primitives, not a component library
- **Starting with component extraction before seeing real duplication** — YAGNI applies; inline utilities until duplication is proven
- **Over-configuring `@theme` with values that never generate utilities** — if you define `--color-brand-150` but never use `bg-brand-150`, you've added dead tokens

## See Also

- [Accessibility](accessibility.md)
- [Performance & Optimization](performance-optimization.md)
- Reference: https://www.wisp.blog/blog/best-practices-for-using-tailwind-css-in-large-projects
