---
description: "Style parents and siblings based on child state — replacing JS class toggling"
tldr: "Use `:has()` when you need to style a parent based on its children or descendants, or a preceding sibling based on what follows — logic that previously required JavaScript class toggling."
---

# :has() — The Parent Selector

## When to Use

> When you need to style a parent based on its children or descendants, or a preceding sibling based on what follows — logic that previously required JavaScript class toggling.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Style a card when it contains an image | `.card:has(img)` | Targets the parent, not the image |
| Change a form layout when a checkbox is checked | `form:has(input:checked)` | Pure CSS state management |
| Style a section with no children | `:not(:has(*))` | Empty state without JS |
| Change a grid when a featured card is present | `.grid:has(.card--featured)` | Layout shifts driven by content |
| Replace JS toggle classes for UI state | `:has(:focus-within)`, `:has(:checked)` | Stateful UI without event listeners |
| Select an element that immediately precedes another | `h2:has(+ .alert)` | Preceding sibling selection |

## Pattern

```css
/* Style a card differently when it contains a video */
.card:has(video) {
  grid-column: span 2;
}

/* Navigation state — label changes when checkbox is checked */
.nav:has(.nav__toggle:checked) .nav__menu {
  display: block;
}

/* Form row highlights when its input has an error */
.form-row:has(input:user-invalid) {
  background: oklch(95% 0.05 30);
}

/* Preceding sibling — add margin to h2 before a note block */
h2:has(+ .callout) {
  margin-bottom: 0.5rem;
}
```

**Specificity rule:** `:has()` takes the specificity of its most specific argument. `:has(.card--featured)` adds class-level specificity (0,1,0), not pseudo-class specificity.

**Browser support:** Chrome 105, Firefox 121, Safari 15.4. Baseline 2023. Safe to use.

## Common Mistakes

- Using `:has(*)` with a broad anchor like `body:has(*)` — the universal selector inside `:has()` triggers expensive full-tree traversal on every DOM mutation; scope it tightly
- Nesting `:has()` inside another `:has()` — invalid, the spec forbids it
- Expecting `:has()` to work inside `@supports` for feature detection — browser support for `:has()` in `@supports` is unreliable; use JS `CSS.supports()` instead
- Forgetting comma-separated arguments are OR logic: `:has(a, b)` matches if either exists

## See Also

- [@scope](css-scope.md) → for scoping styles without affecting specificity broadly
- [:user-valid / :user-invalid](user-valid-invalid.md) → for form state styling
- Reference: [MDN :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has)
