---
description: "Register custom properties with @property — animate CSS variables, enforce types"
tldr: "Use `@property` when you need to animate a custom property, enforce a type, prevent inheritance, or guarantee an initial value. Use a regular `--var: value` for non-animated custom properties."
---

# @property — Registered Custom Properties

## When to Use

> When you need to animate a custom property, enforce a type on a CSS variable, prevent inheritance, or guarantee an initial value. Unregistered custom properties are opaque strings to the browser — `@property` makes them first-class typed values.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Animate a gradient via a custom property | `@property` with `syntax: '<angle>'` or `'<number>'` | Browser can interpolate typed values, not strings |
| Prevent a custom property from inheriting | `inherits: false` | Each element gets its own initial value |
| Type-check a custom property | `syntax: '<color>'` / `'<length>'` / `'<percentage>'` | Invalid values fall back to initial-value |
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

- Omitting `initial-value` when `syntax` is not `'*'` — the entire `@property` rule is silently ignored
- Using `em` or context-dependent values as `initial-value` — invalid; only absolute values allowed (`px`, `deg`, `0`, etc.)
- Registering a property the browser already knows — `@property --color` is fine, but don't try to register standard properties like `color`
- Expecting `CSS.registerProperty()` (JS) and `@property` (CSS) to merge — if both exist, the JS call takes precedence

## See Also

- ← [Native CSS Nesting](native-nesting.md) | [oklch() Color Space](oklch-color.md) →
- Reference: [MDN @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
