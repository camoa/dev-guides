---
description: Build multi-part components with compound components + Context, ref forwarding, Radix wrappers, and use client directives in Next.js App Router.
---

# Composition Patterns

## When to Use

> Use when building multi-part components (select, tabs, accordion, dialog) where sub-components need to share state without prop drilling.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Sub-components sharing parent state | Compound component + Context | Clean API; no prop drilling; scales to any depth |
| Single component needing DOM ref access | `React.forwardRef` (React ≤18) or direct `ref` prop (React 19) | Required for Radix integration, focus management, measurements |
| Component that wraps a Radix primitive | Radix + `asChild` + ref forwarding | Gets accessibility, keyboard nav, ARIA for free |
| Reusable behavior across different UIs | Custom hook | Separates logic from markup; testable independently |
| Theme/config available to a subtree | React Context Provider | Avoids prop threading; use sparingly — prefer composition first |
| Controlled + uncontrolled in same component | `useControllableState` pattern (Radix) | Switches between controlled/uncontrolled; warns on invalid switching |

## Pattern

Compound component with Context:
```tsx
const TabsContext = React.createContext<{ active: string; setActive: (v: string) => void } | null>(null);

export function Tabs({ defaultValue, children }: { defaultValue: string; children: React.ReactNode }) {
  const [active, setActive] = React.useState(defaultValue);
  return <TabsContext.Provider value={{ active, setActive }}>{children}</TabsContext.Provider>;
}
Tabs.List = function TabsList({ children }: { children: React.ReactNode }) {
  return <div role="tablist">{children}</div>;
};
Tabs.Trigger = function TabsTrigger({ value, children }: { value: string; children: React.ReactNode }) {
  const ctx = React.useContext(TabsContext)!;
  return <button role="tab" aria-selected={ctx.active === value} onClick={() => ctx.setActive(value)}>{children}</button>;
};
```

Ref forwarding — React 18 vs React 19:
```tsx
// React 18: forwardRef wrapper required
export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input ref={ref} className={cn('border rounded px-3 py-2', className)} {...props} />
  )
);
Input.displayName = 'Input';

// React 19: ref is a regular prop — no forwardRef needed
export function Input({ className, ref, ...props }: React.InputHTMLAttributes<HTMLInputElement> & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} className={cn('border rounded px-3 py-2', className)} {...props} />;
}
```

### Server vs Client Components (Next.js App Router)

| Component type | Directive | Examples |
|---|---|---|
| Pure display (no interactivity, no state, no hooks) | None (Server Component) | `Badge`, `Container`, `Stack`, `Text` |
| Interactive (state, effects, event handlers, Context, Radix) | `"use client"` | `Button`, `Dialog`, `Tabs`, `Accordion`, `FormField` |
| Uses browser APIs (`window`, `localStorage`) | `"use client"` | `ThemeProvider`, `ToastProvider` |

**Rule**: If a component uses `useState`, `useEffect`, `useContext`, `onClick`, or any Radix primitive → add `"use client"`. If it only renders props and children with `cn()` → it can stay a Server Component.

## Common Mistakes

- **Wrong**: Forgetting `"use client"` on components using Radix primitives → **Right**: All Radix components require this in Next.js App Router
- **Wrong**: Adding `"use client"` to every component "just in case" → **Right**: Only add it when genuinely needed; Server Components have zero JS bundle cost
- **Wrong**: Creating a Context for every compound component → **Right**: Only create Context when sub-components genuinely need shared state
- **Wrong**: Forgetting `displayName` on `forwardRef` components → **Right**: Always set `displayName`; React DevTools shows `ForwardRef` without it
- **Wrong**: Using Context for global design token access → **Right**: CSS custom properties are better for tokens; Context is for behavioral state
- **Wrong**: Mixing controlled and uncontrolled behavior without the `defaultValue`/`value` distinction → **Right**: Use the `useControllableState` pattern

## See Also

- [Children and Slot Patterns](children-and-slot-patterns.md)
- [Tailwind Integration](tailwind-integration.md)
- Reference: [Kent C. Dodds — Compound Components](https://kentcdodds.com/blog/compound-components-with-react-hooks)
- Reference: [React 19 ref as prop](https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop)
- Reference: [Next.js — Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- Reference: `@radix-ui/react-dialog` 1.1.15 — `node_modules/@radix-ui/react-dialog/dist/index.js`
