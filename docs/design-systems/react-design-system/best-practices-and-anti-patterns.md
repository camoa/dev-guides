---
description: Pre-ship checklist and anti-pattern catalog for React design system components covering API design, security, performance, and code review standards.
---

# Best Practices and Anti-Patterns

## When to Use

> Use before shipping a component to design system consumers, and during code review.

## Decision

| Principle | Rule |
|---|---|
| Composition over configuration | Ask: could this prop instead be a slot or composed child? If yes, use a slot. |
| Minimal API surface | Start with fewer props than you think; you can add, you can't remove without a breaking change |
| Consistent naming | `on{Event}`, `is{State}`, `has{Thing}`, variant names match design vocabulary |
| Documentation-driven | Write the Storybook story before the component; if you can't write a clear story, the API isn't clear |

## Security Patterns

| Risk | Avoid | Use instead |
|---|---|---|
| XSS via `dangerouslySetInnerHTML` | `<div dangerouslySetInnerHTML={{ __html: userContent }} />` | Sanitize with DOMPurify first |
| XSS via URL props | `<a href={userHref}>` with no validation | Validate `href` starts with `https://` or `/`; block `javascript:` |
| Sensitive data in props | Logging component props | Never log props; treat form values as sensitive |

```tsx
// WRONG: direct user HTML
<div dangerouslySetInnerHTML={{ __html: post.content }} />

// CORRECT: sanitize before rendering
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(post.content) }} />

// CORRECT: validate URL schemes
function isSafeUrl(url: string) {
  return url.startsWith('https://') || url.startsWith('/') || url.startsWith('#');
}
```

## Performance Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Inline object props to memoized components | New reference every render, defeats memo | Extract to a variable or `useMemo` |
| `useState` per form field in a large form | N re-renders per keystroke | Use react-hook-form |
| Heavy component in default bundle | Delays Time to Interactive | `React.lazy()` + `Suspense` |
| `useEffect` to sync two pieces of state | Double render, potential loops | Derive the value during render instead |
| Context that changes every render | Re-renders all consumers | Split context or memoize the value |

## Development Standards Anti-Patterns

| Anti-pattern | Why it's wrong |
|---|---|
| `!important` in component styles | Impossible to override; breaks the style cascade |
| Inline styles for design token values | Bypasses Tailwind; no dark mode; no responsive; no JIT optimization |
| `@extend` in SCSS | Selector explosion; non-obvious output; impossible to debug |
| Components that import from feature code | Creates circular dependencies; design system must be dependency-free |
| Global CSS side effects in component files | Leaks into other components; impossible to isolate |
| `console.log` left in component code | Performance cost; exposes internal state |

## Senior Dev Code Review Checklist

1. No `forwardRef` on leaf components — "This component can't be used with Radix primitives or focus management"
2. `className` prop not accepted — "Callers can't customize this at all; design system components always accept `className`"
3. Prop named `style` that's a string — "This shadows the HTML `style` attribute; pick a different name"
4. No `displayName` on `forwardRef` components — "React DevTools shows `ForwardRef` everywhere; always set `displayName`"
5. Event handler that doesn't call the prop version — "If I pass `onClick`, it gets ignored; always merge internal + prop handlers"
6. Hard-coded colors that aren't tokens — "This breaks theming; use CSS variables"
7. Missing error/disabled/loading states — "This component isn't production-ready; every interactive component needs all states"

## See Also

- [Testing](testing.md)
- Reference: [Radix UI Primitives](https://www.radix-ui.com/primitives/docs/overview/introduction)
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
