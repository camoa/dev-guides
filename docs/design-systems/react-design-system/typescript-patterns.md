---
description: Type React design system components with ComponentPropsWithoutRef, VariantProps, discriminated unions, and React 19 ref patterns.
---

# TypeScript Patterns

## When to Use

> Use in every design system component. TypeScript is how the system communicates its API to consumers — it's not optional.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Extend native HTML element props | `React.ComponentPropsWithoutRef<'button'>` | Gets all valid button props; excludes ref (avoid mismatch) |
| Extend + forward ref (React ≤18) | `React.ComponentPropsWithRef<'button'>` or `React.forwardRef` + explicit ref type | Includes ref in the type |
| Extend + ref (React 19) | Add `ref?: React.Ref<HTMLButtonElement>` directly to interface | React 19 ref is a regular prop; no `forwardRef` wrapper needed |
| Variant props from CVA | `VariantProps<typeof variantFn>` | Type is derived from CVA definition; stays in sync automatically |
| Exclusive prop combinations | Discriminated union with literal discriminator | TypeScript enforces valid combos at compile time |
| Generic component (wraps any element) | Generic function with `T extends React.ElementType` | Caller gets correct element props inferred |
| Component variant as a type | `type ButtonVariant = VariantProps<typeof buttonVariants>['variant']` | Extract single variant dimension for docs or other components |
| Get component ref type | `React.ComponentRef<typeof Button>` | Extracts ref type from component; replaces deprecated `React.ElementRef` |

## Pattern

Extending native props (standard pattern):
```tsx
export interface ButtonProps
  extends React.ComponentPropsWithoutRef<'button'>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
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

- **Wrong**: Using `React.FC<Props>` → **Right**: Use function declarations with explicit return types; `React.FC` adds implicit `children` (pre-React 18) and hides `displayName` issues
- **Wrong**: Typing children as `JSX.Element` → **Right**: Use `React.ReactNode` for maximum flexibility; `JSX.Element` excludes strings, arrays, and null
- **Wrong**: `as any` to solve prop conflicts → **Right**: Use `Omit<>` or discriminated unions to resolve properly
- **Wrong**: Forgetting to export prop interfaces → **Right**: Always export; consumers need to extend or document component APIs
- **Wrong**: Mixing `interface` and `type` inconsistently → **Right**: Pick one convention (interfaces for component props, types for unions/aliases is common)

## See Also

- [Design Token Consumption](design-token-consumption.md)
- [Accessibility Patterns](accessibility-patterns.md)
- Reference: [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- Reference: [FreeCodeCamp — Polymorphic Components](https://www.freecodecamp.org/news/build-strongly-typed-polymorphic-components-with-react-and-typescript/)
