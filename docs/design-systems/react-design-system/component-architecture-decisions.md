---
description: Choose between flat props, compound components, headless, controlled, or polymorphic patterns for a new React component.
---

# Component Architecture Decisions

## When to Use

> Use flat props for simple single-purpose UI. Use compound components when the caller needs to place named slots (header/body/footer) in their markup. Use headless (Radix primitive) when full styling freedom across themes is required.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple, single-purpose UI (button, badge, icon) | Flat props component | Minimal API; props are the natural contract |
| Multi-slot layout (card with header/body/footer) | Compound components | Slot placement stays in the caller's markup |
| Behavior + styling bundled | Styled component with CVA variants | One import; designer-friendly API |
| Behavior only, consumer supplies styling | Headless component (Radix primitive) | Full styling freedom; reuse across themes |
| Form input needing external control | Controlled component with value/onChange | Integrates with react-hook-form; single source of truth |
| Toggle/disclosure not needing parent state | Uncontrolled with internal state + defaultValue | Simpler caller code when parent doesn't own the state |
| Component renders as different HTML elements | Polymorphic with `as` prop | Correct semantics without wrapper divs |

## Pattern

Flat props (simple):
```tsx
// Button — flat props, CVA variants
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}
export function Button({ variant = 'primary', size = 'md', className, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
```

Compound (card with slots):
```tsx
// Card — compound pattern, slots via dot notation
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn('rounded-lg border bg-card', className)}>{children}</div>;
}
Card.Header = function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="flex flex-col space-y-1.5 p-6">{children}</div>;
};
Card.Body = function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="p-6 pt-0">{children}</div>;
};
```

## Common Mistakes

- **Wrong**: Building a compound component when flat props would suffice → **Right**: Add compound pattern only when the caller's layout genuinely needs named slots
- **Wrong**: Making everything controlled → **Right**: Use uncontrolled with `defaultValue` for trivial toggle/open state
- **Wrong**: Mixing headless + styled concerns in one component → **Right**: Separate them so the component is reusable across themes
- **Wrong**: Using render props where compound components now suffice → **Right**: Compound components with Context are the modern equivalent
- **Wrong**: Choosing composition depth by internal complexity → **Right**: The complexity of the caller's layout needs drives compound vs flat

## See Also

- [Props Patterns](props-patterns.md)
- Reference: [Radix UI Primitives](https://www.radix-ui.com/primitives/docs/overview/introduction)
- Reference: [Compound Pattern — patterns.dev](https://www.patterns.dev/react/compound-pattern/)
- Reference: [shadcn/ui Button](https://ui.shadcn.com/docs/components/button)
- Reference: [shadcn/ui Card](https://ui.shadcn.com/docs/components/card)
