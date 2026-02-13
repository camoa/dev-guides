---
description: Ensuring WCAG 2.2 Level AA compliance
---

# Accessibility Best Practices

## When to Use

> Ensuring WCAG 2.2 Level AA compliance.

## Best Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| Semantic HTML first | Use `<nav>`, `<main>` before ARIA | Native semantics universal |
| Always alt text | Use `alt` prop; empty for decorative | Screen readers need descriptions |
| Keyboard navigation | All interactive via Tab/Enter/Space | Many users keyboard-only |
| Color contrast | 4.5:1 text, 3:1 UI components | Low vision accessibility |
| Label all inputs | Use `form-element` wrapper | Screen readers announce labels |
| Heading hierarchy | One `<h1>`, `<h2>`-`<h6>` in order | Screen readers build outline |

## Pattern

```twig
{# GOOD: Icon button with label #}
{%
  include 'radix:button' with {
    attributes: create_attribute({'aria-label': 'Close'}),
    content: '<i class="bi bi-x" aria-hidden="true"></i>'
  }
%}

{# BAD: Placeholder as label #}
{%
  include 'radix:input' with {
    placeholder: 'Email'  {# Missing label! #}
  }
%}
```

## See Also

- Reference: https://www.w3.org/WAI/WCAG22/quickref/
