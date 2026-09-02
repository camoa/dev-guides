---
description: Make React design system components accessible using Radix primitives, ARIA prop forwarding, focus management, and icon-only button patterns.
tldr: "Use in every interactive component. Accessibility is a correctness requirement — a design system that ships inaccessible components ships broken components."
---

# Accessibility Patterns

## When to Use

> Every interactive component. Accessibility is not an add-on — it's a correctness requirement. A design system that ships inaccessible components ships broken components.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Accessible dialog, menu, tabs, select | Radix UI primitives | WAI-ARIA patterns implemented and tested; keyboard nav included |
| Forward ARIA props to the DOM | Spread `...props` on root element | Callers add `aria-label`, `aria-describedby` as needed |
| Custom interactive component | Reference WAI-ARIA Authoring Practices | Defines keyboard patterns for each widget type |
| Focus management (dialog, menu) | Radix `FocusTrap` or `@radix-ui/react-focus-scope` | Correct focus trap behavior without reimplementing |
| Live region announcements | `aria-live="polite"` on status container | Screen readers announce updates; no JS library needed |
| Icon-only button | `aria-label` required on the button | No visible text → no name → screen reader silent |

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

forwardRef for focus management:
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

- Building custom dropdowns/modals without Radix or ARIA patterns → misses keyboard nav, focus trap, Escape handling; use Radix primitives instead
- Relying only on `onClick` for interactivity → keyboard users need `onKeyDown` for Enter/Space; Radix handles this; raw divs do not
- Setting `aria-hidden="true"` on focusable content → hides it from screen readers but keyboard navigation still reaches it; remove it from the tab order too (`tabIndex={-1}`)
- Forgetting `role` on custom interactive elements → a `<div>` button without `role="button"` is not announced as interactive
- Testing a11y only with automated tools → axe-core finds ~30-40% of accessibility issues; manual keyboard and screen reader testing is required
- Adding `tabIndex={0}` to non-interactive elements unnecessarily → pollutes tab order; only focusable elements should be in the tab sequence

## See Also

- [TypeScript Patterns](typescript-patterns.md)
- [Storybook Integration](storybook-integration.md)
- Reference: [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- Reference: [Radix UI accessibility](https://www.radix-ui.com/primitives/docs/overview/introduction)
- Reference: [Divotion — Accessible by Design](https://www.divotion.com/blog/accessible-by-design)
- Reference: [React Aria — Accessibility](https://react-aria.adobe.com/quality#accessibility)
