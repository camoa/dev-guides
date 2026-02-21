---
description: Declare light and dark values in one line with light-dark() — no media query duplication
---

# light-dark() Function

## When to Use

> Use `light-dark()` to declare both light and dark color values in a single declaration — eliminating duplicated `@media (prefers-color-scheme: dark)` blocks. Use `@media` for non-color properties that change in dark mode.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| One-line light/dark color token | `light-dark(light-value, dark-value)` | No media query duplication |
| Non-color properties that change in dark mode | `@media (prefers-color-scheme: dark)` | `light-dark()` is color-only |
| Component themes controlled by a class | `color-scheme` on parent + `light-dark()` | Class changes `color-scheme`, function responds |
| Custom dark mode toggle (not OS preference) | Set `color-scheme: dark` via JavaScript on `:root` | Function reads the computed `color-scheme` |

## Pattern

```css
/* Required: declare that both schemes are supported */
:root {
  color-scheme: light dark;
}

.card {
  background: light-dark(#ffffff, #1a1a2e);
  color: light-dark(#111827, #f0f4f8);
  border-color: light-dark(oklch(85% 0.05 240), oklch(30% 0.05 240));
  box-shadow: 0 2px 8px light-dark(
    oklch(0% 0 0 / 0.1),
    oklch(0% 0 0 / 0.4)
  );
}
```

**Replaces this pattern:**
```css
/* Without light-dark() — must duplicate all color declarations */
.card { background: #fff; color: #111; }
@media (prefers-color-scheme: dark) {
  .card { background: #1a1a2e; color: #f0f4f8; }
}
```

**JS toggle pattern:**
```js
document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
```
`light-dark()` reads the computed `color-scheme` value, so this changes which value is applied.

**Browser support:** Chrome 123, Firefox 120, Safari 17.5. Baseline newly available since May 2024. Safe to use.

## Common Mistakes

- **Wrong**: Omitting `color-scheme: light dark` on `:root` → **Right**: Without it, the function uses the default scheme (usually light) and the dark value is never applied
- **Wrong**: Using `light-dark()` for non-color properties like `font-size` → **Right**: It only works for color values
- **Wrong**: Expecting `light-dark()` to respond to a `.dark` class → **Right**: It reads `color-scheme`; set `color-scheme: dark` on the element or ancestor for class-based toggling

## See Also

- [Relative Color Syntax](relative-color.md)
- [oklch() / oklab() — Modern Color Spaces](oklch-color.md)
- Reference: [MDN light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark)
