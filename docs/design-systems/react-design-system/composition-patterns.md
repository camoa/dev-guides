---
description: Build multi-part components with compound components + Context, ref forwarding, Radix wrappers, and use client directives in Next.js App Router.
tldr: "Use when building multi-part components (select, tabs, accordion, dialog) where sub-components need to share state without prop drilling."
---

# Composition Patterns

## When to Use

> When building multi-part components (select, tabs, accordion, dialog) where sub-components need to share state without prop drilling.

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

Compound component with Context (simplified — your own component):
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

How Radix actually implements compound components (from Dialog/Tabs source):
```tsx
// Radix uses createContextScope() for composable, scoped contexts that survive
// component library merging (avoids context collision when two Radix components nest)
// In your own components, React.createContext is sufficient — createContextScope
// is only needed for library authors building composable primitives
//
// Radix Tabs (verified from react-tabs 1.1.13 source) uses:
// - useControllableState({ prop: valueProp, defaultProp, onChange: onValueChange })
//   → handles controlled (value prop) AND uncontrolled (defaultValue) in one hook
// - Primitive.div/button as the root element (extends Radix's Primitive wrapper)
// - React.forwardRef on every sub-component for ref forwarding
// - 'use client' directive on all components (required for Next.js App Router)
```

Ref forwarding — React 18 vs React 19:
```tsx
// React 18 and earlier: forwardRef wrapper required
export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input ref={ref} className={cn('border rounded px-3 py-2', className)} {...props} />
  )
);
Input.displayName = 'Input'; // Required for React DevTools

// React 19: ref is a regular prop — no forwardRef needed
export function Input({ className, ref, ...props }: React.InputHTMLAttributes<HTMLInputElement> & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} className={cn('border rounded px-3 py-2', className)} {...props} />;
}
// Note: forwardRef still works in React 19 for backward compat; just deprecated
```

## Server Components vs Client Components (Next.js App Router)

In Next.js App Router, components are Server Components by default. Design system components split into two categories:

| Component type | Directive | Examples |
|---|---|---|
| Pure display (no interactivity, no state, no hooks) | None (Server Component) | `Badge`, `Container`, `Stack`, `Text`, `Separator` |
| Interactive (state, effects, event handlers, Context, Radix) | `"use client"` | `Button`, `Dialog`, `Tabs`, `Accordion`, `FormField` |
| Uses browser APIs (`window`, `localStorage`, `IntersectionObserver`) | `"use client"` | `ThemeProvider`, `ToastProvider` |

```tsx
// Button.tsx — needs "use client" because of onClick handling + CVA
"use client";
import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';
// ...
```

```tsx
// Badge.tsx — pure display, NO "use client" needed
import { cn } from '@/lib/utils';
// cn() is a pure function — no hooks — works in Server Components
export function Badge({ children, className }: BadgeProps) {
  return <span className={cn('rounded-full px-2 text-xs', className)}>{children}</span>;
}
```

**Rule of thumb**: If a component uses `useState`, `useEffect`, `useContext`, `onClick`, or any Radix primitive → it needs `"use client"`. If it only renders props and children with `cn()` → it can stay a Server Component.

## Common Mistakes

- Forgetting `"use client"` on components using Radix primitives → all Radix components require this in Next.js App Router; missing it causes Server Component errors
- Adding `"use client"` to every component "just in case" → defeats Server Component benefits (zero JS bundle, streaming, direct data access); only add it when genuinely needed
- Creating a Context for every compound component → Context has render cost; only create one when sub-components genuinely need shared state
- Forgetting `displayName` on `forwardRef` components → React DevTools shows `ForwardRef` instead of component name; always set it
- Using Context for global design token access → CSS custom properties are better for tokens; Context is for behavioral state
- Mixing controlled and uncontrolled behavior in one component without the `defaultValue`/`value` distinction → breaks react-hook-form integration and causes stale state bugs; use the `useControllableState` pattern
- Deep component factory patterns → component factories (functions returning components) obscure the component tree; prefer explicit compound components
- Importing a Client Component into a Server Component layout and expecting it to stay server-side → the `"use client"` boundary propagates; structure your imports to minimize client boundaries

## See Also

- [Children and Slot Patterns](children-and-slot-patterns.md)
- [Tailwind Integration](tailwind-integration.md)
- Reference: `@radix-ui/react-dialog` 1.1.15 — `node_modules/@radix-ui/react-dialog/dist/index.js`
- Reference: `@radix-ui/react-tabs` 1.1.13 — `node_modules/@radix-ui/react-tabs/dist/index.js`
- Reference: [Kent C. Dodds — Compound Components](https://kentcdodds.com/blog/compound-components-with-react-hooks)
- Reference: [React 19 ref as prop](https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop)
- Reference: [Compound Pattern — patterns.dev](https://www.patterns.dev/react/compound-pattern/)
- Reference: [React 19 release blog](https://react.dev/blog/2024/12/05/react-19)
- Reference: [Next.js — Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
