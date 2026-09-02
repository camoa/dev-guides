---
description: Type React design system components with ComponentPropsWithoutRef, VariantProps, discriminated unions, and React 19 ref patterns.
tldr: "Use in every design system component. TypeScript is how the system communicates its API to consumers — it's not optional."
---

# TypeScript Patterns

## When to Use

> Any design system component. TypeScript is non-negotiable in a design system — it's how the system communicates its API to consumers.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Extend native HTML element props | `React.ComponentPropsWithoutRef<'button'>` | Gets all valid button props; excludes ref (avoid mismatch) |
| Extend + forward ref (React ≤18) | `React.ComponentPropsWithRef<'button'>` or `React.forwardRef` + explicit ref type | Includes ref in the type |
| Extend + ref (React 19) | Add `ref?: React.Ref<HTMLButtonElement>` directly to interface | React 19 ref is a regular prop; no `forwardRef` wrapper needed |
| Variant props from CVA | `VariantProps<typeof variantFn>` | Type is derived from CVA definition; stays in sync automatically |
| Exclusive prop combinations | Discriminated union with literal discriminator | TypeScript enforces valid combos at compile time |
| Generic component (wraps any element) | Generic function with `T extends React.ElementType` | Caller gets correct element props inferred |
| Component variant as a type | `type ButtonVariant = VariantProps<typeof buttonVariants>['variant']` | Extract single variant dimension for documentation or other components |
| Get component ref type | `React.ComponentRef<typeof Button>` | Extracts ref type from component; replaces deprecated `React.ElementRef` |

## Pattern

Extending native props (standard pattern):
```tsx
// Extend HTMLButtonElement props, add your own, export the type
export interface ButtonProps
  extends React.ComponentPropsWithoutRef<'button'>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;    // your additions
}

// Omit conflicts explicitly when needed
export interface InputProps
  extends Omit<React.ComponentPropsWithoutRef<'input'>, 'size'> {
  size?: 'sm' | 'md' | 'lg'; // shadows HTML 'size' attr (number) with our string type
}
```

Discriminated union (for mutually exclusive prop sets):
```tsx
type WithHref = { href: string; onClick?: never };
type WithOnClick = { href?: never; onClick: () => void };
type ActionProps = (WithHref | WithOnClick) & { children: React.ReactNode };
// TypeScript now errors if both href and onClick are provided
```

## Common Mistakes

- Using `React.FC<Props>` → `React.FC` implicitly adds `children` (pre-React 18), hides displayName issues; use function declarations with explicit return types instead
- Typing children as `JSX.Element` → excludes strings, arrays, null; use `React.ReactNode` for maximum flexibility
- `as any` to solve prop conflicts → masks real type errors; use `Omit<>` or discriminated unions to resolve properly
- Forgetting to export prop interfaces → consumers can't extend or document component APIs
- Mixing interface and type inconsistently → pick one per project (interfaces for component props, types for unions/aliases is a common convention)

## See Also

- [Design Token Consumption](design-token-consumption.md)
- [Accessibility Patterns](accessibility-patterns.md)
- Reference: [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- Reference: [FreeCodeCamp — Polymorphic Components](https://www.freecodecamp.org/news/build-strongly-typed-polymorphic-components-with-react-and-typescript/)
- Reference: [React TypeScript — Patterns by Use Case](https://react-typescript-cheatsheet.netlify.app/docs/advanced/patterns_by_usecase/)
