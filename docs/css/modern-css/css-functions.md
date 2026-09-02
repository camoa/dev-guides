---
description: "Native CSS @function, if(), and @mixin — reusable logic without a preprocessor (Chromium-first)"
tldr: "Use `@function` (Chrome 141+) for reusable computed values, `if()` (Chrome 137+) for inline conditionals. Both are Chromium-only."
---

# CSS @function, if(), and Upcoming Mixins

## When to Use

> When you need reusable CSS logic — custom functions for computed values, conditional values based on context, or shared style blocks — without a preprocessor.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Reusable calculated value | `@function` (Chrome 141+) | Native CSS function, no build step |
| Conditional value based on media/container/style | `if()` (Chrome 137+) | Inline conditional without custom property workaround |
| Shared block of declarations | `@mixin` / `@apply` (experimental) | Replaces Sass mixins — not yet in stable browsers |
| Cross-browser reusable values today | Custom properties + `calc()` | Universally supported pattern |

## Pattern

```css
/* @function — Chrome 141+ */
@function --fluid-size(--min, --max, --min-vw: 320px, --max-vw: 1200px) {
  --slope: (var(--max) - var(--min)) / (var(--max-vw) - var(--min-vw));
  --intercept: var(--min) - var(--slope) * var(--min-vw);
  result: clamp(var(--min), var(--intercept) + var(--slope) * 100vw, var(--max));
}

h1 { font-size: --fluid-size(1.5rem, 3rem); }
h2 { font-size: --fluid-size(1.25rem, 2rem); }

/* if() — Chrome 137+ */
.container {
  padding: if(
    media(width >= 768px): 2rem;
    else: 1rem;
  );
}

.card {
  background: if(
    style(--theme: dark): oklch(25% 0 0);
    style(--theme: light): oklch(98% 0 0);
    else: white;
  );
}

/* @mixin / @apply — experimental (Chrome Canary only) */
@mixin --flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero { @apply --flex-center; }
.modal { @apply --flex-center; }
```

**`if()` condition types:**
- `media(...)` — media query condition
- `style(...)` — style query (custom property check)
- `supports(...)` — feature query
- `else` — fallback

**Browser support:**
- `@function`: Chrome 141+. No Firefox/Safari yet.
- `if()`: Chrome 137+. No Firefox/Safari yet.
- `@mixin`/`@apply`: Chrome Canary only (behind flag). Very early.

All three are Chromium-first. Use custom properties + `calc()` for cross-browser until support widens.

## Common Mistakes

- Using `@function` to return multiple declarations — functions return a single value via `result:`, not a block of properties (that's what `@mixin` is for)
- Nesting `if()` inside `if()` — not supported; use multiple conditions with semicolons
- Assuming these replace Sass today — Chromium-only means you still need Sass/PostCSS for production cross-browser code

## See Also

- [@property](at-property.md) → for typed custom properties used with functions
- [Native Nesting](native-nesting.md) → another Sass-replacement feature that IS cross-browser
- Reference: [Chrome: CSS Functions](https://developer.chrome.com/blog/css-functions)
- Reference: [Chrome: CSS if()](https://developer.chrome.com/blog/if-article)
- Reference: [MDN: @function](https://developer.mozilla.org/en-US/docs/Web/CSS/@function)
