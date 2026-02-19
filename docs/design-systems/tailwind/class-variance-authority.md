---
description: Use Class Variance Authority (CVA) to manage component variants with type-safe, structured class generation.
---

# Class Variance Authority (CVA)

## When to Use

> Use CVA when a component has 2+ orthogonal variant dimensions, needs compound variants, or requires TypeScript autocompletion on variant props.

## Decision

| Situation | Use CVA? | Why |
|-----------|----------|-----|
| Component with 2+ variant dimensions (size + intent) | Yes | Structured; prevents combinatorial class explosion |
| Compound variants (specific combo = extra styles) | Yes | CVA handles this natively |
| TypeScript autocompletion on variant props | Yes | `VariantProps` type helper |
| Single boolean variant | Maybe | `cx` from CVA may be enough |
| Data-driven values (dynamic width, runtime colors) | No | Use inline `style={}` for truly dynamic values |

## Pattern

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
      { intent: 'danger', size: 'sm', class: 'ring-1 ring-red-400' },
    ],
    defaultVariants: {
      intent: 'primary',
      size: 'md',
    },
  }
);

type ButtonProps = VariantProps<typeof button>;

// Both 'class' and 'className' props are valid
<button class={button({ intent: 'ghost', size: 'sm' })}>Cancel</button>
<button className={button({ intent: 'primary' })}>Submit</button>
```

## CVA Exports (v0.7.1)

| Export | Purpose |
|--------|---------|
| `cva` | Creates a variant-aware class generator function |
| `cx` | Re-export of `clsx`; use for ad-hoc class merging without variant logic |
| `VariantProps` | TypeScript type helper for inferring prop types from a CVA definition |

## cx for Ad-hoc Composition

```ts
import { cx } from 'class-variance-authority';

const cls = cx('base-class', isActive && 'bg-brand-500', { 'font-bold': isPrimary });
```

## Common Mistakes

- **Wrong**: Dynamic class string construction inside CVA — `bg-${color}-500` is invisible to Tailwind's scanner. **Right**: Always use complete class strings in lookup objects.
- **Wrong**: Creating CVA variants for styles that aren't real design variants. **Right**: `style={{ width: dynamicWidth }}` is correct for data-driven values.
- **Wrong**: Using `@apply` to build a class system when you have React/Vue/Twig components available. **Right**: The component IS the abstraction; use CVA inside the component.

## See Also

- [tailwind-merge & clsx](tailwind-merge-clsx.md)
- [Component Patterns](component-patterns.md)
- Reference: https://cva.style/docs
- Reference: https://cva.style/docs/getting-started/variants
