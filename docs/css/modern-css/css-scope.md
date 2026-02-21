---
description: Scope styles to a subtree with @scope — replace BEM naming conventions
---

# @scope — Scoped Styles

## When to Use

> Use `@scope` when you need styles that only apply within a specific DOM subtree — replacing BEM naming conventions or CSS Modules for visual scoping. Use Shadow DOM when you need behavioral encapsulation and JS isolation.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Style a component without leaking to others | `@scope (.card)` | Styles stay inside `.card` boundary |
| Avoid `.card__title` BEM naming | `@scope` + `.title` | Scoping context replaces naming convention |
| Exclude a nested sub-component | `@scope (.card) to (.widget)` | Donut hole excludes `.widget` descendants |
| Resolve conflicts between overlapping themes | `@scope` proximity | Closest ancestor scope wins, not source order |
| True JS-driven encapsulation | Shadow DOM | `@scope` is CSS-only scoping, not full encapsulation |

## Pattern

```css
/* Basic scope — .title only matches inside .card */
@scope (.card) {
  .title {
    font-size: 1.25rem;
    font-weight: 600;
  }

  /* :scope refers to the scope root itself (.card) */
  :scope {
    border: 1px solid oklch(80% 0.05 240);
    border-radius: 0.5rem;
  }
}

/* Donut hole — scope .card but exclude .widget descendants */
@scope (.card) to (.widget) {
  a {
    color: var(--card-link-color);
    /* Does not affect links inside .widget nested in .card */
  }
}
```

**Proximity behavior:** when two `@scope` rules both match an element, the one with fewer DOM hops to its scope root wins — regardless of source order or specificity. This is a new cascade criterion specific to `@scope`.

**Browser support:** Chrome 118, Firefox 146, Safari 17.4. Became baseline in late 2025. Safe to use with progressive enhancement for older Firefox versions.

## Common Mistakes

- **Wrong**: Treating `@scope (.card) { :scope { } }` as identical to `.card { }` → **Right**: `:scope` inside `@scope` targets the root but behaves differently in cascade weight; they are not equivalent
- **Wrong**: Expecting `@scope` to prevent JavaScript from reading or modifying styles → **Right**: `@scope` is purely a CSS selector scoping mechanism; JS still has full access
- **Wrong**: Expecting the donut hole limit element itself to be styled → **Right**: The limit selector in `@scope (A) to (B)` excludes `B` from the scope entirely

## See Also

- [@layer — Cascade Layers](cascade-layers.md)
- [Native CSS Nesting](native-nesting.md)
- Reference: [MDN @scope](https://developer.mozilla.org/en-US/docs/Web/CSS/@scope)
