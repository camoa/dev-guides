---
description: CSS scoping strategies, BEM methodology, and Bootstrap/Radix integration
drupal_version: "11.x"
---

# SCSS/CSS in SDCs

## When to Use

> Use this when adding styles to components, ensuring proper CSS scoping, or importing Bootstrap variables in Radix sub-themes.

## Decision

| Strategy | Use Case | Pattern |
|----------|----------|---------|
| BEM methodology | Component-scoped styles | `.component__element--modifier` |
| CSS custom properties | Theming values | `--component-padding: 1rem;` |
| Bootstrap imports | Radix sub-theme components | `@import '~bootstrap/scss/mixins';` |
| Scoped selectors | Prevent collisions | Always namespace with component class |

## Pattern

**BEM Methodology:**
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
```

**Importing Radix/Bootstrap Variables:**
```scss
@import '../../../src/scss/base/variables';  // Bootstrap overrides
@import '~bootstrap/scss/functions';
@import '~bootstrap/scss/variables';
@import '~bootstrap/scss/mixins';

.my-component {
  padding: $spacer;
  background: $primary;

  @include media-breakpoint-up(md) {
    padding: $spacer * 2;
  }
}
```

**CSS Custom Properties:**
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

- **Wrong**: Global selectors like `.button` or `.card` → **Right**: Use component-specific namespace (`.my-component__button`)
- **Wrong**: Using `@extend` in Sass → **Right**: Use mixins or utility classes (extends create bloated CSS)
- **Wrong**: Using `!important` → **Right**: Fix selector specificity instead

## See Also

- Reference: `/core/themes/olivero/components/teaser/teaser.css`
- Reference: `/themes/contrib/radix/` structure
- [Component File Structure](component-file-structure.md)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/customize/sass/)
