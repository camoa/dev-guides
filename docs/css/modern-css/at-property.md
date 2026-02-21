---
description: Register custom properties with @property — animate CSS variables, enforce types
---

# @property — Registered Custom Properties

## When to Use

> Use `@property` when you need to animate a custom property, enforce a type, prevent inheritance, or guarantee an initial value. Use a regular `--var: value` for non-animated custom properties.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Animate a gradient via a custom property | `@property` with `syntax: '<angle>'` or `'<number>'` | Browser can interpolate typed values, not strings |
| Prevent a custom property from inheriting | `inherits: false` | Each element gets its own initial value |
| Type-check a custom property | `syntax: '<color>'` / `'<length>'` / `'<percentage>'` | Invalid values fall back to `initial-value` |
| Animated counter or progress indicator | `@property --progress { syntax: '<number>'; }` | Smooth interpolation between numeric values |
| Standard non-animated custom property | Regular `--var: value` | `@property` adds overhead for no benefit |

## Pattern

Animating a conic-gradient rotation via a typed `<angle>` property:

```css
@property --angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

.spinner {
  background: conic-gradient(var(--brand) var(--angle), transparent 0);
  animation: spin 2s linear infinite;
}

@keyframes spin {
  to { --angle: 360deg; }
}
```

Animated progress bar width:

```css
@property --progress {
  syntax: '<percentage>';
  inherits: false;
  initial-value: 0%;
}

.progress-bar {
  width: var(--progress);
  transition: --progress 0.4s ease;
}
/* Setting --progress via inline style triggers smooth transition */
```

**Required descriptors:**
- `syntax` — required; use `'*'` for universal (accepts anything)
- `inherits` — required; `true` or `false`
- `initial-value` — required when `syntax` is not `'*'`; must be computationally independent (no `em`, `%` that depend on context)

**Browser support:** Chrome 85, Firefox 128, Safari 16.4. Firefox 128 (July 2024) completed cross-browser support. Safe to use.

## Common Mistakes

- **Wrong**: Omitting `initial-value` when `syntax` is not `'*'` → **Right**: The entire `@property` rule is silently ignored without it
- **Wrong**: Using `em` or context-dependent values as `initial-value` → **Right**: Only absolute values allowed (`px`, `deg`, `0`, etc.)
- **Wrong**: Trying to register standard CSS properties like `color` → **Right**: Only register custom properties (prefixed with `--`)
- **Wrong**: Expecting `CSS.registerProperty()` and `@property` to merge → **Right**: If both exist for the same property, the JS call takes precedence

## See Also

- [Native CSS Nesting](native-nesting.md)
- [oklch() / oklab() — Modern Color Spaces](oklch-color.md)
- Reference: [MDN @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
