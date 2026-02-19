---
description: Choose between children, compound dot-notation slots, asChild (Radix), named slot props, and render props for component content regions.
---

# Children and Slot Patterns

## When to Use

> Use when a component needs to render content it doesn't control — layouts, wrappers, trigger+panel pairs.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple wrapper rendering one block of content | `children: React.ReactNode` | Simplest; no pattern overhead |
| Named regions (header + body + footer) | Compound component dot notation | Caller places slots explicitly in JSX; readable |
| Caller-controlled rendering with access to internal state | Render props / function children | Pass internal state out for advanced customization |
| Unstyled trigger wrapped by Radix primitive | `asChild` prop (Radix pattern) | Merges behavior onto caller's element without wrapper div |
| Multiple optional content areas | Named slot props (`headerSlot?`, `footerSlot?`) | Simple; avoids compound component overhead for 2-3 slots |
| Wrap a lazy-loaded component in a Radix Slot | `Slottable` component | Radix 1.2.x supports lazy component children via React 19 `use` internally |

## Pattern

`asChild` pattern — verified from `@radix-ui/react-slot` 1.2.4 source:
```tsx
import { Slot } from '@radix-ui/react-slot';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
}
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ asChild, className, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return <Comp ref={ref} className={cn(buttonVariants(), className)} {...props} />;
  }
);
// Usage: <Button asChild><Link href="/page">Go</Link></Button>
// Renders a styled <a> — not a <button> wrapping an <a>
```

How `Slot` merges props — from `mergeProps()` in the source:
```tsx
// Slot merges slotProps + childProps with these rules:
// 1. Event handlers: BOTH are called (slot handler runs after child handler)
//    onClick from Slot AND onClick from child both fire — they compose, not override
// 2. style: shallow merge — { ...slotStyle, ...childStyle }
// 3. className: simple string join with space — NOT cn() / tailwind-merge
//    Use cn() in your component before passing to Slot if you need conflict resolution
// 4. All other props: child props win (childProps override slotProps)
```

Named slot props (simple alternative for 2-3 regions):
```tsx
interface DialogProps {
  title: React.ReactNode;
  description?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
}
// Callers: <Dialog title={<h2>Confirm</h2>} footer={<DialogActions />}>content</Dialog>
```

## Common Mistakes

- **Wrong**: `React.Children.map()` to iterate children for slot identification → **Right**: Use compound components or named slot props; `Children.map` breaks on type changes
- **Wrong**: Wrapping `asChild` content in an extra div → **Right**: `asChild` must merge directly onto the child element; the extra div negates it
- **Wrong**: Expecting Slot to resolve Tailwind class conflicts → **Right**: Slot joins classNames with a space; resolve conflicts with `cn()` before passing to Slot
- **Wrong**: Deeply nested render props → **Right**: Compound components with Context solve the same problem more readably
- **Wrong**: Forgetting ref forwarding when using `asChild` → **Right**: Radix primitives need refs for positioning; use `React.forwardRef` (or pass `ref` directly in React 19)
- **Wrong**: Expecting a second event handler to override the Slot's → **Right**: Both fire; this is intentional composition behavior

## See Also

- [Props Patterns](props-patterns.md)
- [Composition Patterns](composition-patterns.md)
- Reference: [Radix UI — Composition (asChild)](https://www.radix-ui.com/primitives/docs/guides/composition)
- Reference: `@radix-ui/react-slot` 1.2.4 — `node_modules/@radix-ui/react-slot/dist/index.js`
- Reference: [shadcn/ui Button with asChild](https://ui.shadcn.com/docs/components/button)
