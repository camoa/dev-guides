---
description: CSS scoping with BEM, Bootstrap/Radix variable imports, and custom properties
drupal_version: "11.x"
---

# SCSS/CSS in SDCs

## When to Use

> Use this when adding styles to a component, scoping CSS properly, or importing Bootstrap variables in Radix sub-themes.

## Decision: CSS Scoping Strategy

| Strategy | Pattern | Purpose |
|----------|---------|---------|
| BEM methodology | `.block__element--modifier` | Prevent collisions, scope to component |
| Custom properties | `--component-padding: 1rem;` | Themeable values, variant overrides |
| Bootstrap imports | `@import '~bootstrap/scss/variables'` | Use design tokens from Radix |

## Pattern

BEM for component-scoped styles:

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

Importing Radix/Bootstrap variables:

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

Custom properties for theming:

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

- **Wrong**: Not scoping CSS with component-specific class → **Right**: Global selectors like `.button` or `.card` collide with other components. Always use unique component class as namespace.
- **Wrong**: Using `@extend` in Sass → **Right**: `@extend` creates unexpected selector chains and bloats compiled CSS. Use mixins or utility classes instead.
- **Wrong**: Using `!important` → **Right**: Indicates specificity problems. Fix selector specificity instead of using `!important`.

## See Also

- Reference: `/core/themes/olivero/components/teaser/teaser.css`
- Reference: `/themes/contrib/radix/` structure
- [Component File Structure](component-file-structure.md)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/customize/sass/)
