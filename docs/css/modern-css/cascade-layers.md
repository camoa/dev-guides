---
description: Control specificity ordering with @layer — tame third-party CSS conflicts
---

# @layer — Cascade Layers

## When to Use

> Use `@layer` when managing specificity conflicts between resets, base styles, third-party CSS (Bootstrap, Drupal base themes), components, and utilities. Use unlayered styles when you need to guarantee an override without `!important`.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Third-party CSS overriding your styles | Declare third-party in a layer | Unlayered styles always beat layered ones |
| Specificity wars between utilities and components | Layer ordering | Layer order determines win, not selector specificity |
| A reset that shouldn't pollute specificity | `@layer reset { * { margin: 0; } }` | Reset stays low-specificity by design |
| `!important` within layers | Be aware of reversal | Lower-ordered layers' `!important` beats higher layers' `!important` |

## Pattern

```css
/* Declare order first — last wins for normal declarations */
@layer reset, base, theme, components, utilities;

/* Third-party CSS goes into a layer — your unlayered styles win */
@import url('bootstrap.css') layer(base);

/* Component styles — always beat base, never fight utilities */
@layer components {
  .btn {
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
  }
}

/* Utilities — final word in the layer stack */
@layer utilities {
  .mt-auto { margin-top: auto; }
}

/* Unlayered styles beat ALL layers regardless of specificity */
.my-special-override { color: red; } /* wins without !important */
```

**Key rules:**
- Styles NOT in any layer always beat layered styles
- Within layers: last declared layer wins (for equal specificity)
- `@layer` with `!important` reverses: earlier layers' `!important` beats later layers' `!important`

**Browser support:** Chrome 99, Firefox 97, Safari 15.4. Widely safe.

## Common Mistakes

- **Wrong**: Declaring layers in the wrong order → **Right**: The `@layer name1, name2` declaration at the top sets precedence; `name2` wins over `name1`
- **Wrong**: Putting your own site styles in layers when third-party CSS is unlayered → **Right**: Unlayered third-party CSS beats your layered styles; always layer third-party first
- **Wrong**: Using `!important` inside layers without understanding the reversal → **Right**: `!important` in layers reverses precedence — earlier layers beat later ones; avoid it
- **Wrong**: Mixing layered and unlayered imports inconsistently → **Right**: Be consistent about what goes into layers across your project

## See Also

- [Subgrid](subgrid.md)
- [@scope — Scoped Styles](css-scope.md)
- Reference: [MDN @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
