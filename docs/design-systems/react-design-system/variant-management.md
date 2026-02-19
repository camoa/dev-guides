---
description: Manage component size, color, and state variants with CVA compoundVariants and tailwind-variants slots.
---

# Variant Management with CVA

## When to Use

> Use when a component has multiple dimensions of variation (size, color/intent, state) that combine in predictable ways. CVA makes these combinations type-safe and conflict-free.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Independent size + color variants | CVA `variants` object | Each dimension declared separately; TypeScript infers all combos |
| Special styles for one variant combo | CVA `compoundVariants` | Targets exact combinations without conditional logic in JSX |
| Variant styles across component slots | tailwind-variants `tv()` with slots | CVA is single-element; TV handles multiple DOM nodes per variant |
| Extend a base component's variants | Extract `cva()` call → compose in child | Override specific variants; keep base's defaults |

## Pattern

Full CVA with compound variants:
```tsx
const alertVariants = cva(
  'relative w-full rounded-lg border p-4',
  {
    variants: {
      variant: {
        default: 'bg-background text-foreground',
        destructive: 'border-destructive/50 text-destructive dark:border-destructive',
      },
    },
    compoundVariants: [
      // compoundVariants apply when multiple variant conditions are ALL true
      { variant: 'destructive', className: '[&>svg]:text-destructive' },
    ],
    defaultVariants: { variant: 'default' },
  }
);
```

tailwind-variants with slots (for compound components):
```tsx
import { tv } from 'tailwind-variants';

const card = tv({
  slots: {
    root: 'rounded-lg border bg-card shadow-sm',
    header: 'flex flex-col space-y-1.5 p-6',
    title: 'text-2xl font-semibold leading-none',
    body: 'p-6 pt-0',
  },
  variants: {
    size: {
      sm: { root: 'p-4', title: 'text-lg' },
      lg: { root: 'p-8', title: 'text-3xl' },
    },
  },
});
// Usage: const { root, header, title, body } = card({ size: 'sm' });
```

## Common Mistakes

- **Wrong**: Nesting variant logic in JSX with ternaries → **Right**: Put all variant logic in `cva()`; ternaries in JSX are hard to read and untyped
- **Wrong**: Forgetting `VariantProps<typeof variantFn>` on the interface → **Right**: Always extract types from CVA; without it variant props become untyped `string`
- **Wrong**: Overusing `compoundVariants` → **Right**: If every variant combo needs one, the variant design is wrong; reconsider the structure
- **Wrong**: Using tailwind-variants for simple single-element components → **Right**: CVA is simpler when there are no slots
- **Wrong**: Defining `cva()` calls inside the component function → **Right**: Extract to module scope so they're created once, not on every render

## See Also

- [Tailwind Integration](tailwind-integration.md)
- [Design Token Consumption](design-token-consumption.md)
- Reference: [CVA — Variants](https://cva.style/docs/getting-started/variants)
- Reference: [tailwind-variants — Slots](https://www.tailwind-variants.org/docs/slots)
