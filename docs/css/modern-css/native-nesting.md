---
description: "Native CSS nesting without Sass — & selector, nested @media, differences from Sass"
tldr: "Use native CSS nesting when you want Sass-style nesting without a build step. Keep Sass when you need `@extend`, `@mixin`, or functions — native CSS does not cover these."
---

# Native CSS Nesting

## When to Use

> When you want Sass-style nesting without a build step or preprocessor. Nesting is now the primary Sass feature covered natively, and the primary reason many projects added Sass.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Readable component CSS with related rules grouped | Native nesting | No preprocessor needed |
| `@media` queries scoped to a component | Nested `@media` inside rule | Works natively in CSS |
| BEM `&__element` pattern | `&` prefix required | `&__element` concatenates correctly |
| BEM `&--modifier` pattern | `&.--modifier` or `&--modifier` | Works with `&` |
| Sass `@extend` or `@mixin` | Still needs Sass | Native CSS does not cover these |

## Pattern

Component with nested states and a scoped media query:

```css
.card {
  padding: 1rem;
  background: var(--card-bg);

  /* Nested pseudo-class */
  &:hover {
    background: var(--card-bg-hover);
  }

  /* Nested modifier */
  &.is-featured {
    border: 2px solid var(--accent);
  }

  /* Nested element (BEM style) */
  &__title {
    font-size: 1.25rem;
  }

  /* Nested media query — scoped to this component */
  @media (width >= 768px) {
    padding: 2rem;
    display: flex;
    gap: 1rem;
  }
}
```

**`&` placement matters:**
- `& .child` — descendant (space required in original spec)
- `&:hover` — pseudo-class (no space)
- `&__element` — string concatenation (works for BEM)
- `.parent &` — ancestor context (valid, reverses nesting)

**Relaxed parsing (Chrome 120+, Firefox 117+, Safari 17.2+):** Type selectors work without `&`:
```css
.card {
  h2 { font-size: 1.5rem; } /* Works in relaxed parsing */
}
```
For maximum compatibility, always use `&` prefix.

**Browser support:** Strict (`&` required) — Chrome 112, Firefox 117, Safari 16.5. Relaxed (type selectors without `&`) — Chrome 120, Firefox 117, Safari 17.2. Safe to use with `&` prefix.

## Common Mistakes

- Dropping `&` on type selectors expecting them to work — they do in Chrome 120+ but break in Chrome 112–119 and older Safari; always use `&`
- Nesting `@keyframes` inside a rule — this is not supported; keyframes must remain at the top level
- Using `@extend` patterns and expecting similar output — native nesting does not merge selectors like `@extend` does; each nested rule generates its own selector
- Deep nesting (more than 3 levels) — generates deeply specific selectors that are hard to override; keep nesting shallow

## See Also

- ← [@scope Scoped Styles](css-scope.md) | [CSS Subgrid](subgrid.md) →
- [@layer Cascade Layers](cascade-layers.md) → for managing specificity from generated selectors
- Reference: [MDN CSS Nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting)
