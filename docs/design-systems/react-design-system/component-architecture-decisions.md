---
description: Choose between flat props, compound components, headless, controlled, or polymorphic patterns for a new React component.
tldr: "Use flat props for simple single-purpose UI. Use compound components when the caller needs to place named slots (header/body/footer) in their markup."
---

# Component Architecture Decisions

## When to Use

> When starting a new component or evaluating how to split an existing one. These decisions affect composability, API surface, and long-term maintainability.

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

- Building a compound component when flat props would suffice → adds boilerplate with no flexibility gain
- Making everything controlled → forces callers to manage trivial state (open/closed toggles)
- Mixing headless + styled concerns in one component → limits reuse across themes; separate them
- Using render props where compound components now suffice → render props are a React 2018 pattern; compound components with Context are the modern equivalent
- Choosing composition depth by component complexity alone → complexity of the *caller's* layout needs drives compound vs flat, not internal complexity

## See Also

- [Props Patterns](props-patterns.md)
- Reference: [shadcn/ui Button](https://ui.shadcn.com/docs/components/base/button)
- Reference: [shadcn/ui Card](https://ui.shadcn.com/docs/components/base/card)
- Reference: [Radix UI Primitives](https://www.radix-ui.com/primitives/docs/overview/introduction)
- Reference: [Compound Pattern — patterns.dev](https://www.patterns.dev/react/compound-pattern/)
