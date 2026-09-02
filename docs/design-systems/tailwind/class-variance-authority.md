---
description: Use Class Variance Authority (CVA) to manage component variants with type-safe, structured class generation.
tldr: "Use CVA when a component has 2+ orthogonal variant dimensions, needs compound variants, or requires TypeScript autocompletion on variant props."
---

# Class Variance Authority (CVA)

## When to Use

> CVA is a TypeScript utility for defining component variants with structured, type-safe class management. Install: `npm install class-variance-authority`.

## Decision

**Use CVA when:**

- A component has 2+ orthogonal variant dimensions (size + intent, size + shape)
- You need compound variants (specific combination triggers additional styles)
- You want TypeScript autocompletion on variant props

## Verified Exports

(from `node_modules/class-variance-authority/dist/index.js`, v0.7.1)

| Export | Purpose |
|--------|---------|
| `cva` | Creates a variant-aware class generator function |
| `cx` | Re-export of `clsx`; use for ad-hoc class merging without variant logic |
| `VariantProps` | TypeScript type helper for inferring prop types from a CVA definition |

## Pattern — Button with CVA

```ts
import { cva, cx, type VariantProps } from 'class-variance-authority';

const button = cva(
  // Base classes — always applied
  'inline-flex items-center font-semibold rounded-lg transition-colors focus-visible:outline-2',
  {
    variants: {
      intent: {
        primary: 'bg-brand-500 text-white hover:bg-brand-600',
        ghost:   'bg-transparent text-brand-500 hover:bg-brand-50',
        danger:  'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg',
      },
    },
    compoundVariants: [
      // Compound variant: danger + small gets extra visual emphasis
      // Array values also work: { intent: ['danger', 'ghost'], size: 'sm', class: '...' }
      { intent: 'danger', size: 'sm', class: 'ring-1 ring-red-400' },
    ],
    defaultVariants: {
      intent: 'primary',
      size: 'md',
    },
  }
);

type ButtonProps = VariantProps<typeof button>;

// Both 'class' and 'className' props are valid — CVA supports both
<button class={button({ intent: 'ghost', size: 'sm' })}>Cancel</button>
<button className={button({ intent: 'primary' })}>Submit</button>
```

**Important:** CVA requires complete static class names — dynamic string construction breaks Tailwind's class detection scanner. Always use the lookup-object pattern (see Performance section).

## cx for Ad-hoc Composition

(no variant logic needed):

```ts
import { cx } from 'class-variance-authority';  // same as clsx

// Conditionally apply classes — cx handles falsy values
const cls = cx('base-class', isActive && 'bg-brand-500', { 'font-bold': isPrimary });
```

## Common Mistakes

- **Using `@apply` to build a class system when you have React/Vue/Twig components available** — the component IS the abstraction
- **Mixing CVA with dynamic class string construction** — `bg-${color}-500` is invisible to Tailwind's scanner
- **Creating CVA variants for styles that aren't real design variants** — not every prop needs a variant; `style={{ width: dynamicWidth }}` is correct for data-driven values

## See Also

- [Design System Integration](design-system-integration.md)
- [Dark Mode](dark-mode.md)
- [Accessibility](accessibility.md)
- Reference: https://cva.style/
- Reference: https://tailwindcss.com/docs/styling-with-utility-classes#managing-duplication
