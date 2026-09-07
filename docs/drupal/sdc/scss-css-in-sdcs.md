---
description: "Scoping component CSS with BEM, importing Bootstrap/Radix variables, and using CSS custom properties for theming"
tldr: "Use BEM to scope component CSS and prevent collisions; prefer CSS custom properties for theming values that variants override. Never use @extend or !important — fix selector specificity or use mixins/utility classes instead."
drupal_version: "11.x"
---

# SCSS/CSS in SDCs

## When to Use

> - You're adding styles to a component
> - You need to scope CSS properly
> - You're importing Bootstrap variables in Radix sub-themes

## Decision

See the patterns below for scoping strategy.

## Pattern

**Pattern: BEM Methodology**

Use BEM for component-scoped styles to prevent collisions.

Reference: `/core/themes/olivero/components/teaser/teaser.css`

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

**Pattern: Importing Radix/Bootstrap Variables**

Reference: `/themes/contrib/radix/` structure

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

**Pattern: Custom Properties (CSS Variables)**

Prefer CSS custom properties for theming values.

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

**Common Mistake:** Not scoping CSS with component-specific class.
**WHY:** Global selectors like `.button` or `.card` collide with other components. Always use unique component class as namespace.

**Common Mistake:** Using `@extend` in Sass.
**WHY:** `@extend` creates unexpected selector chains and bloats compiled CSS. Use mixins or utility classes instead.

**Common Mistake:** Using `!important`.
**WHY:** Indicates specificity problems. Fix selector specificity instead of using `!important`.

## See Also

- [Radix Sub-Theme Best Practices](../../design-systems/radix-sdc/radix-sub-theme-best-practices.md)
- [Component File Structure](component-file-structure.md)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/customize/sass/)
