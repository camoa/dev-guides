---
description: Build Stack, Flex, Grid, and Container layout primitives that standardize spacing and remove repetitive Tailwind class sets from feature code.
---

# Layout Components

## When to Use

> Use when building reusable spacing, flex, and grid primitives. Layout components standardize spacing and remove repetitive Tailwind class sets from feature code.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Vertical or horizontal list with gap | `Stack` component | Abstracts `flex flex-col gap-{n}` or `flex flex-row gap-{n}` |
| Flex container with alignment control | `Flex` component | Wraps `display: flex` with props for `align`, `justify`, `wrap` |
| CSS grid layout | `Grid` component | Wraps `display: grid` with `cols`, `gap` props |
| Responsive max-width wrapper | `Container` component | Consistent page width constraints from design tokens |
| Responsive prop (different value per breakpoint) | Responsive prop object `{ base: 2, md: 4 }` or array | Maps to Tailwind responsive prefixes |

## Pattern

Stack (most common layout primitive):
```tsx
type StackProps = {
  direction?: 'row' | 'col';
  gap?: 1 | 2 | 3 | 4 | 6 | 8 | 10 | 12; // constrain to spacing scale
  align?: 'start' | 'center' | 'end' | 'stretch';
  children: React.ReactNode;
  className?: string;
};

const gapMap = { 1: 'gap-1', 2: 'gap-2', 3: 'gap-3', 4: 'gap-4', 6: 'gap-6', 8: 'gap-8', 10: 'gap-10', 12: 'gap-12' } as const;
const alignMap = { start: 'items-start', center: 'items-center', end: 'items-end', stretch: 'items-stretch' } as const;

export function Stack({ direction = 'col', gap = 4, align = 'stretch', children, className }: StackProps) {
  return (
    <div className={cn('flex', direction === 'col' ? 'flex-col' : 'flex-row', gapMap[gap], alignMap[align], className)}>
      {children}
    </div>
  );
}
// Usage: <Stack direction="row" gap={3} align="center"><Icon /><Text>Label</Text></Stack>
```

Container:
```tsx
export function Container({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn('mx-auto w-full max-w-screen-xl px-4 sm:px-6 lg:px-8', className)}>{children}</div>;
}
```

## Common Mistakes

- **Wrong**: Accepting arbitrary number for `gap` without constraining to spacing scale → **Right**: Constrain to valid spacing values; unlimited gap breaks design system consistency
- **Wrong**: Using `margin` for spacing between layout items → **Right**: Use `gap` on flex/grid containers; margin breaks at edges and doesn't compose
- **Wrong**: Building layout components with CSS-in-JS or style props → **Right**: Tailwind classes are tree-shaken and static; style props bypass optimization
- **Wrong**: Duplicating layout logic in every feature component → **Right**: Extract Stack/Flex/Grid once; 20 components with `flex flex-col gap-4` is a Stack
- **Wrong**: Making layout components too flexible with unlimited responsive prop combinations → **Right**: Constrain to the spacing scale; untested class combinations create visual bugs

## See Also

- [Form Components](form-components.md)
- [Performance](performance.md)
- Reference: [Marmelab — Box, Stack, Grid](https://marmelab.com/react-admin/BoxStackGrid.html)
