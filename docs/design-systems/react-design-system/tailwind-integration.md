---
description: Use cn() (clsx + tailwind-merge) and CVA for class merging and variant definitions in every Tailwind-based component.
tldr: "Use `cn()` and CVA in every component that uses Tailwind classes. `cn()` handles merging; CVA handles variant definitions."
---

# Tailwind Integration — cn() and CVA

## When to Use

> Every component that uses Tailwind classes. The `cn()` utility and CVA are the two foundational tools — `cn()` for merging, CVA for variant definitions.

> **Tailwind v4 note (verified):** This project uses Tailwind CSS 4.2.0. In v4, there is no `tailwind.config.ts`. All configuration is CSS-first using `@import "tailwindcss"` and `@theme inline { }` in your CSS file. See Section 7 for design token integration with v4.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Merge static + conditional classes | `cn()` (clsx + tailwind-merge) | Resolves Tailwind class conflicts; removes duplicates |
| Accept `className` override from caller | `cn(internalClasses, props.className)` | Last-wins; caller overrides base styles cleanly |
| Define size/color/state variants | CVA `cva()` | Type-safe variant map; generates correct class set per variant combo |
| Style multi-slot compound components | tailwind-variants `tv()` | Supports per-slot variants; CVA doesn't handle slots natively |
| Simple conditional class (no variants) | `cn('base', condition && 'conditional')` | Inline; no CVA needed for one-off conditions |

## Pattern

The `cn()` utility (define once, use everywhere) — verified pattern:
```ts
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
// clsx 2.1.1: handles strings, arrays, objects, conditionals → string
// tailwind-merge 3.5.0: resolves conflicting class groups (e.g. p-2 p-4 → p-4)
// tailwind-merge uses a prefix-trie class group system — last class in a conflict group wins
```

CVA 0.7.1 — verified exports and usage:
```tsx
// CVA exports: cva, cx (= clsx re-export), VariantProps (type only)
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors', // base
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
// cn() wraps the CVA output — CVA uses clsx internally but does NOT use tailwind-merge
// passing className last ensures caller overrides win via tailwind-merge
```

## Common Mistakes

- Using string template literals for conditional classes → `${isActive ? 'bg-blue-500' : 'bg-gray-500'}` breaks tailwind-merge conflict resolution; always use `cn()`
- Not installing `tailwind-merge` alongside `clsx` → clsx alone doesn't resolve Tailwind conflicts (e.g., `p-2 p-4` both stay in the output)
- Putting `cn()` calls outside the component → result won't update on prop changes; `cn()` must be called during render
- Mixing CVA and ad-hoc conditional classes without `cn()` → CVA output is a string; merge it with `cn(cvaOutput, className)` not string concatenation; CVA uses clsx but NOT tailwind-merge internally
- Omitting `defaultVariants` in CVA → variant props become required; always provide defaults so callers don't have to specify every variant
- Using `cx` from CVA instead of `cn` → CVA's `cx` is just clsx, not tailwind-merge; use your `cn()` utility for conflict resolution

## See Also

- [Composition Patterns](composition-patterns.md)
- [Variant Management](variant-management.md)
- Reference: CVA 0.7.1 source — `node_modules/class-variance-authority/dist/index.js`
- Reference: tailwind-merge 3.5.0 — `node_modules/tailwind-merge/dist/bundle-cjs.js`
- Reference: [CVA docs](https://cva.style/)
- Reference: [tailwind-merge](https://github.com/dcastil/tailwind-merge)
- Reference: [shadcn/ui utils](https://ui.shadcn.com/docs/installation/manual)
- Reference: [CVA — installation](https://cva.style/getting-started/installation/)
- Reference: [tailwind-variants — Introduction](https://www.tailwind-variants.org/docs/introduction)
