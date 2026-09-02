---
description: Design component prop APIs using discriminated unions, polymorphic as props, spread rest, and TypeScript defaults.
tldr: "Use these patterns when defining the public API of a component. Well-designed props prevent breaking changes and communicate intent clearly."
---

# Props Patterns

## When to Use

> When defining the public API of a component. Well-designed props prevent breaking changes and communicate intent clearly.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Multiple exclusive modes (link vs button) | Discriminated union | TypeScript enforces valid combinations; no impossible states |
| Component that renders as any element | Polymorphic `as` + `ComponentPropsWithoutRef` | Caller chooses element; correct HTML semantics |
| Pass unknown extra props to the DOM | Spread `...rest` onto the root element | Allows `data-*`, `aria-*`, event handlers without explicit declarations |
| Optional props with sensible defaults | TypeScript optional + default parameters | Self-documenting; no prop proliferation |
| Required prop that has no safe default | Required (no `?`, no default) | Fails at build time, not runtime |

## Pattern

Discriminated union (button vs link):
```tsx
type ButtonAsButton = { as?: 'button' } & React.ButtonHTMLAttributes<HTMLButtonElement>;
type ButtonAsAnchor = { as: 'a' } & React.AnchorHTMLAttributes<HTMLAnchorElement>;
type ButtonProps = (ButtonAsButton | ButtonAsAnchor) & { variant?: 'primary' | 'ghost' };

export function Button({ as: As = 'button', variant = 'primary', ...props }: ButtonProps) {
  return <As className={cn(buttonVariants({ variant }))} {...props} />;
}
// Usage: <Button as="a" href="/page">Link</Button> — TypeScript enforces href only on 'a'
```

Polymorphic component (generic):
```tsx
type PolymorphicProps<T extends React.ElementType> = {
  as?: T;
} & React.ComponentPropsWithoutRef<T>;

export function Text<T extends React.ElementType = 'p'>({ as, className, ...props }: PolymorphicProps<T>) {
  const Component = as ?? 'p';
  return <Component className={cn('text-base', className)} {...props} />;
}
// Usage: <Text as="h2">Heading</Text> — inherits h2 props; no unnecessary divs
```

## Common Mistakes

- Accepting `className` but not spreading `...rest` → callers can't add `aria-*` or `data-*` without explicit prop declarations
- Using a generic `options: object` prop → kills TypeScript inference; use explicit union types
- Defaulting optional boolean props to `true` → `<Button disabled>` looks like it takes no value; prefer explicit `disabled={false}` defaults or don't add a default
- Over-restricting props to only what you need today → design systems evolve; spread `...rest` for extensibility
- Forgetting that `className` merging needs `cn()` → naive string concatenation breaks Tailwind class precedence

## See Also

- [Component Architecture Decisions](component-architecture-decisions.md)
- [Children and Slot Patterns](children-and-slot-patterns.md)
- Reference: [FreeCodeCamp — Polymorphic Components](https://www.freecodecamp.org/news/build-strongly-typed-polymorphic-components-with-react-and-typescript/)
- Reference: [React TypeScript — Patterns by Use Case](https://react-typescript-cheatsheet.netlify.app/docs/advanced/patterns_by_usecase/)
- Reference: [LogRocket — Polymorphic Components](https://blog.logrocket.com/build-strongly-typed-polymorphic-components-react-typescript/)
