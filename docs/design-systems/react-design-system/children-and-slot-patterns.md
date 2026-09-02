---
description: Choose between children, compound dot-notation slots, asChild (Radix), named slot props, and render props for component content regions.
tldr: "Use when a component needs to render content it doesn't control — layouts, wrappers, trigger+panel pairs."
---

# Children and Slot Patterns

## When to Use

> When a component needs to render content it doesn't control — layouts, wrappers, trigger+panel pairs.

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

How `Slot` merges props — from `mergeProps()` in the source (important nuances):
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

- Using `React.Children.map()` to iterate children for slot identification → fragile; children type changes break it; use compound components or named slot props instead
- Wrapping `asChild` content in an extra div → negates the entire point; `asChild` should merge directly onto the child element
- Expecting Slot to resolve Tailwind class conflicts → Slot joins classNames with a space, not `cn()`; conflicting Tailwind classes (e.g., `p-2` from slot and `p-4` from child) both survive; resolve before passing to Slot
- Deeply nested render props → impossible to read; compound components with Context solve the same problem more declarably
- Forgetting to forward refs when using `asChild` → Radix primitives need refs for positioning; always use `React.forwardRef` (or pass `ref` directly in React 19)
- Adding a second event handler and expecting it to override the Slot's → both fire; this is intentional composition behavior, not a bug

## See Also

- [Props Patterns](props-patterns.md)
- [Composition Patterns](composition-patterns.md)
- Reference: `@radix-ui/react-slot` 1.2.4 — `node_modules/@radix-ui/react-slot/dist/index.js`
- Reference: [Radix UI — Composition (asChild)](https://www.radix-ui.com/primitives/docs/guides/composition)
- Reference: [shadcn/ui Button with asChild](https://ui.shadcn.com/docs/components/base/button)
