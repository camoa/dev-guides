---
description: Convert JSX conditional expressions to Twig if/else
drupal_version: "11.x"
---

# Conditional Rendering

## When to Use

> Use this when converting JSX conditional expressions to Twig. React uses JavaScript expressions inside JSX; Twig uses `{% if %}` tags and filters.

## Decision

| JSX Pattern | Twig Equivalent | Notes |
|---|---|---|
| `{show && <Element />}` | `{% if show %}<element>{% endif %}` | Direct boolean check |
| `{cond ? <A /> : <B />}` | `{% if cond %}<a>{% else %}<b>{% endif %}` | Ternary maps to if/else |
| `{items.length > 0 && <List />}` | `{% if items is not empty %}` | Twig `is not empty` checks both null and length |
| `{count > 3 && <More />}` | `{% if count > 3 %}` | Numeric comparisons work the same |
| `{!hidden && <Element />}` | `{% if not hidden %}` | Negation with `not` keyword |
| `{value ?? 'default'}` | `{{ value\|default('default') }}` | Null coalescing -- `default` filter is the Twig equivalent |
| `{value \|\| 'fallback'}` | `{{ value ?: 'fallback' }}` | Falsy fallback -- Twig's `?:` operator (PHP shorthand ternary) |
| `{type === 'link' ? <a> : <button>}` | `{% if url %}<a>{% else %}<button>{% endif %}` | Dynamic tag selection |
| `{items?.map(...)}` | `{% if items %}{% for ... %}{% endif %}` | Optional chaining has no Twig equivalent; guard with `{% if %}` |
| `{isOpen && createPortal(<Modal />, document.body)}` | Render `<dialog>` in place | No portal system in Twig; use HTML `<dialog>` or Drupal off-canvas |

## Pattern: Conditional Classes

**React (with cn/clsx)**
```jsx
<div className={cn(
  'card',
  variant === 'compact' && 'card-compact',
  bordered && 'card-bordered'
)}>
```

**Twig equivalent**
```twig
{% set classes = [
  'card',
  variant == 'compact' ? 'card-compact',
  bordered ? 'card-bordered',
] %}
<div {{ attributes.addClass(classes) }}>
```

Drupal's `addClass()` method filters out falsy values from the array, so conditional entries that evaluate to `false` or `null` are automatically excluded at render time.

## Common Mistakes

- **Wrong**: Using `{% if items|length > 0 %}` → **Right**: Use `{% if items is not empty %}` (cleaner and handles null)
- **Wrong**: Using `{{ variable ?? 'default' }}` (PHP syntax) → **Right**: Use `{{ variable|default('default') }}` in Twig
- **Wrong**: Forgetting that `0` is falsy in Twig → **Right**: Be explicit with `is not empty` or `!= 0` checks

## See Also

- [Loops & Iteration](loops-iteration.md)
- [Styling Translation](styling.md)
- Reference: [Twig Tests](https://twig.symfony.com/doc/3.x/tests/index.html)
