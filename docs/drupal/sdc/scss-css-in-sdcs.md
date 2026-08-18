---
description: "Scoping component CSS with BEM, importing Bootstrap/Radix variables, and using CSS custom properties for theming"
tldr: "Use BEM to scope component CSS and prevent collisions; prefer CSS custom properties for theming values that variants override. Never use @extend or !important — fix selector specificity or use mixins/utility classes instead."
drupal_version: "11.x"
---

# SCSS/CSS in SDCs

## When to Use

> Use this when you're adding styles to a component, you need to scope CSS properly, or you're importing Bootstrap variables in Radix sub-themes.

## Decision

Use BEM for component-scoped styles to prevent collisions. Prefer CSS custom properties for theming values.

## Pattern

**BEM Methodology** — Reference: `/core/themes/olivero/components/teaser/teaser.css`

```css
/* Block */
.teaser {
  display: flex;
  flex-direction: column;
}

/* Element */
.teaser__meta {
  font-size: 0.875rem;
  color: var(--color-text-neutral-soft);
}

/* Modifier */
.teaser--featured {
  border: 2px solid var(--color-accent);
}

/* Modifier + Element */
.teaser--featured .teaser__title {
  font-weight: bold;
}
```

**Importing Radix/Bootstrap Variables** — Reference: `/themes/contrib/radix/` structure

```scss
/* In component SCSS file */
@import '../../../src/scss/base/variables';  // Bootstrap overrides
@import '~bootstrap/scss/functions';
@import '~bootstrap/scss/variables';
@import '~bootstrap/scss/mixins';

.my-component {
  padding: $spacer;
  background: $primary;
  border-radius: $border-radius;

  @include media-breakpoint-up(md) {
    padding: $spacer * 2;
  }
}
```

**Custom Properties (CSS Variables)**

```css
.component {
  --component-padding: 1rem;
  --component-bg: #fff;

  padding: var(--component-padding);
  background: var(--component-bg);
}

/* Override in variants */
.component--large {
  --component-padding: 2rem;
}
```

## Common Mistakes

- **Wrong**: Not scoping CSS with a component-specific class → **Right**: Global selectors like `.button` or `.card` collide with other components. Always use a unique component class as namespace.
- **Wrong**: Using `@extend` in Sass → **Right**: `@extend` creates unexpected selector chains and bloats compiled CSS. Use mixins or utility classes instead.
- **Wrong**: Using `!important` → **Right**: Indicates specificity problems. Fix selector specificity instead of using `!important`.

## See Also

- Reference: `/core/themes/olivero/components/teaser/teaser.css`
- Reference: `/themes/contrib/radix/` structure
- [Component File Structure](component-file-structure.md)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/customize/sass/)
