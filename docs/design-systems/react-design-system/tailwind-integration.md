---
description: Use cn() (clsx + tailwind-merge) and CVA for class merging and variant definitions in every Tailwind-based component.
---

# Tailwind Integration — cn() and CVA

## When to Use

> Use `cn()` and CVA in every component that uses Tailwind classes. `cn()` handles merging; CVA handles variant definitions. Both are foundational — not optional.

> **Tailwind v4 note (verified):** This project uses Tailwind CSS 4.2.0. In v4, there is no `tailwind.config.ts`. All configuration is CSS-first using `@import "tailwindcss"` and `@theme inline { }` in your CSS file.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Merge static + conditional classes | `cn()` (clsx + tailwind-merge) | Resolves Tailwind class conflicts; removes duplicates |
| Accept `className` override from caller | `cn(internalClasses, props.className)` | Last-wins; caller overrides base styles cleanly |
| Define size/color/state variants | CVA `cva()` | Type-safe variant map; generates correct class set per variant combo |
| Style multi-slot compound components | tailwind-variants `tv()` | Supports per-slot variants; CVA doesn't handle slots natively |
| Simple conditional class (no variants) | `cn('base', condition && 'conditional')` | Inline; no CVA needed for one-off conditions |

## Pattern

The `cn()` utility (define once, use everywhere):
```ts
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
// clsx 2.1.1: handles strings, arrays, objects, conditionals → string
// tailwind-merge 3.5.0: resolves conflicting class groups (e.g. p-2 p-4 → p-4)
```

CVA 0.7.1 — verified exports and usage:
```tsx
// CVA exports: cva, cx (= clsx re-export), VariantProps (type only)
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: { primary: 'bg-primary text-primary-foreground', ghost: 'hover:bg-accent' },
      size: { sm: 'h-8 px-3 text-sm', md: 'h-10 px-4', lg: 'h-12 px-8 text-lg' },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  }
);

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {}

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
// cn() wraps CVA output — CVA uses clsx internally but NOT tailwind-merge
// passing className last ensures caller overrides win via tailwind-merge
```

## Common Mistakes

- **Wrong**: Template literals for conditional classes → **Right**: Always use `cn()`; template literals break tailwind-merge conflict resolution
- **Wrong**: Installing `clsx` without `tailwind-merge` → **Right**: clsx alone doesn't resolve Tailwind conflicts (e.g., `p-2 p-4` both survive)
- **Wrong**: Calling `cn()` outside the component → **Right**: `cn()` must be called during render; result won't update on prop changes otherwise
- **Wrong**: Mixing CVA output and ad-hoc classes with string concatenation → **Right**: Always `cn(cvaOutput, className)`; CVA uses clsx but NOT tailwind-merge internally
- **Wrong**: Omitting `defaultVariants` in CVA → **Right**: Without defaults, all variant props become required
- **Wrong**: Using `cx` from CVA instead of `cn` → **Right**: CVA's `cx` is just clsx, not tailwind-merge; use your `cn()` utility

## See Also

- [Variant Management](variant-management.md)
- [Composition Patterns](composition-patterns.md)
- Reference: [CVA docs](https://cva.style/docs/getting-started/installation)
- Reference: [tailwind-merge](https://github.com/dcastil/tailwind-merge)
- Reference: [shadcn/ui utils](https://ui.shadcn.com/docs/installation/manual)
- Reference: [tailwind-variants vs CVA](https://www.tailwind-variants.org/docs/comparison)
