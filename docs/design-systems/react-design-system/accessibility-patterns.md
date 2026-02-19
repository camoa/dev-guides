---
description: Make React design system components accessible using Radix primitives, ARIA prop forwarding, focus management, and icon-only button patterns.
---

# Accessibility Patterns

## When to Use

> Use in every interactive component. Accessibility is a correctness requirement — a design system that ships inaccessible components ships broken components.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Accessible dialog, menu, tabs, select | Radix UI primitives | WAI-ARIA patterns implemented and tested; keyboard nav included |
| Forward ARIA props to the DOM | Spread `...props` on root element | Callers add `aria-label`, `aria-describedby` as needed |
| Custom interactive component | Reference WAI-ARIA Authoring Practices | Defines keyboard patterns for each widget type |
| Focus management (dialog, menu) | Radix `FocusTrap` or `@radix-ui/react-focus-scope` | Correct focus trap behavior without reimplementing |
| Live region announcements | `aria-live="polite"` on status container | Screen readers announce updates; no JS library needed |
| Icon-only button | `aria-label` required on the button | No visible text → no accessible name → screen reader silent |

## Pattern

Forwarding ARIA props (always do this):
```tsx
// Accept ...props and spread — callers can always add aria-* without changes
export function Button({ className, variant, size, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />;
  // Caller: <Button aria-label="Close dialog" aria-pressed={isOpen}>X</Button>
}
```

Icon-only button:
```tsx
// WRONG: no accessible name
<button onClick={onClose}><XIcon /></button>

// CORRECT: aria-label provides the name
<button onClick={onClose} aria-label="Close dialog"><XIcon aria-hidden="true" /></button>
// aria-hidden on the icon prevents double-reading
```

Ref forwarding for focus management:
```tsx
// Radix requires refs for positioning and focus management
export const Trigger = React.forwardRef<HTMLButtonElement, TriggerProps>(
  ({ children, ...props }, ref) => (
    <button ref={ref} {...props}>{children}</button>
  )
);
Trigger.displayName = 'Trigger';
```

## Common Mistakes

- **Wrong**: Building custom dropdowns/modals without Radix or ARIA patterns → **Right**: Radix handles keyboard nav, focus trap, and Escape key; raw divs do not
- **Wrong**: Relying only on `onClick` for interactivity → **Right**: Keyboard users need `onKeyDown` for Enter/Space; Radix handles this automatically
- **Wrong**: Setting `aria-hidden="true"` on focusable content → **Right**: Remove it from the tab order too (`tabIndex={-1}`) or it's still reachable by keyboard
- **Wrong**: Forgetting `role` on custom interactive elements → **Right**: A `<div>` button without `role="button"` is not announced as interactive
- **Wrong**: Testing a11y only with automated tools → **Right**: axe-core finds ~30-40% of issues; manual keyboard and screen reader testing is required
- **Wrong**: Adding `tabIndex={0}` to non-interactive elements → **Right**: Only focusable elements should be in the tab sequence

## See Also

- [TypeScript Patterns](typescript-patterns.md)
- [Storybook Integration](storybook-integration.md)
- Reference: [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- Reference: [Radix UI accessibility](https://www.radix-ui.com/primitives/docs/overview/introduction)
- Reference: [React Aria — Accessibility](https://react-spectrum.adobe.com/react-aria/accessibility.html)
