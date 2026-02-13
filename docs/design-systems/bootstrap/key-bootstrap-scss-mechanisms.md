---
description: Key Bootstrap SCSS Mechanisms — variable override system, map merging, mixins, and CSS custom properties generation
---

# Key Bootstrap SCSS Mechanisms

## When to Use

> Use when understanding Bootstrap's internal architecture, troubleshooting customization issues, or leveraging Bootstrap's built-in systems effectively.

## Decision

| Mechanism | How It Works | When to Use |
|-----------|--------------|-------------|
| `!default` flag | Only sets variable if not already defined | Override Bootstrap variables |
| `map-merge()` | Combines two maps, second overwrites first | Extend Bootstrap maps |
| `map.deep-merge()` | Merges nested maps recursively | Preserve nested values |
| Bootstrap mixins | Reusable style generators | Button variants, media queries |
| CSS custom properties | Generated from SCSS variables | Runtime theming, JavaScript updates |

## Pattern

**Variable Override System**:
```scss
// Your override (before importing Bootstrap)
$primary: #0066cc;

@import "bootstrap/scss/variables";
// Bootstrap sees $primary already defined
// Skips its default due to !default flag
// Result: $primary = #0066cc
```

**Map Merging System**:
```scss
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";

// Merge additions with Bootstrap defaults
$theme-colors: map-merge($theme-colors, (
  "brand": #0066cc,
  "custom": #ff6600,
));

@import "bootstrap/scss/maps";
// Bootstrap now has ALL colors (defaults + yours)
```

**Common Map Operations**:
```scss
// Add to map
$spacers: map-merge($spacers, (
  "3xs": 2px,
));

// Remove from map
$theme-colors: map-remove($theme-colors, "info", "light");

// Get value from map
$primary-color: map-get($theme-colors, "primary");
```

**Bootstrap Mixins**:
```scss
// Color manipulation
$hover-color: tint-color($primary, 20%);   // Lighten 20%
$active-color: shade-color($primary, 20%); // Darken 20%

// Button variant
.btn-custom {
  @include button-variant(
    $background: #0066cc,
    $border: #0066cc,
    $color: #fff,
    $hover-background: darken(#0066cc, 7.5%)
  );
}

// Media query breakpoints
.custom-component {
  font-size: 1rem;

  @include media-breakpoint-up(md) {
    font-size: 1.25rem;  // Tablet and up
  }

  @include media-breakpoint-up(lg) {
    font-size: 1.5rem;   // Desktop and up
  }
}

// Border radius
.custom-box {
  @include border-radius($border-radius);
}
```

**CSS Custom Properties Generation**:
```scss
// SCSS Variables
$primary: #0066cc;

// Bootstrap generates in :root
:root {
  --bs-primary: #0066cc;
  --bs-primary-rgb: 0, 102, 204;
}

// Usage in CSS
.custom-component {
  background: var(--bs-primary);
  color: rgba(var(--bs-primary-rgb), 0.5);
}
```

## Common Mistakes

- **Wrong**: Setting variables after Bootstrap import → **Right**: Before import (`!default` flag)
- **Wrong**: `map-merge()` on nested maps → **Right**: `map.deep-merge()` (preserves nested values)
- **Wrong**: Manual CSS property creation → **Right**: Bootstrap auto-generates from SCSS variables
- **Wrong**: Using CSS variables in media queries → **Right**: Use SCSS variables (CSS spec limitation)
- **Wrong**: Not using Bootstrap mixins → **Right**: Leverage `button-variant()`, `media-breakpoint-up()`, etc.

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- [SCSS Integration Order](scss-integration-order.md)
- Reference: [Sass: sass:map Documentation](https://sass-lang.com/documentation/modules/map/)
- Reference: [Bootstrap 5.3 Mixins](https://getbootstrap.com/docs/5.3/customize/sass/)
