---
description: Bootstrap's internal SCSS architecture including !default flag, map merging, and mixins
---

# Key Bootstrap SCSS Mechanisms

## When to Use

> Use this to understand Bootstrap's internal architecture, troubleshoot customization issues, and leverage built-in systems effectively.

## Variable Override System

### How Bootstrap's `!default` Flag Works

**Bootstrap Variables (in `_variables.scss`):**

```scss
$primary: #0d6efd !default;
$secondary: #6c757d !default;
```

**Your Override (before importing Bootstrap):**

```scss
$primary: #0066cc;  // Your value (no !default)

@import "bootstrap/scss/variables";
// Bootstrap sees $primary is already defined
// Skips its default due to !default flag
// Result: $primary = #0066cc
```

**Key Concept:** The `!default` flag means "only set this variable if it doesn't already exist."

## Map Merging System

### Pattern: Safe Map Extension

**Bootstrap Map (in `_maps.scss`):**

```scss
$theme-colors: (
  "primary": $primary,
  "secondary": $secondary,
  // ... other colors
) !default;
```

**Your Extension:**

```scss
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";

// Merge your additions with Bootstrap defaults
$theme-colors: map-merge($theme-colors, (
  "brand": #0066cc,      // Add new color
  "custom": #ff6600,     // Add another color
));

@import "bootstrap/scss/maps";
// Bootstrap now has ALL colors (defaults + yours)
```

### Common Map Operations

```scss
// Add to map
$spacers: map-merge($spacers, (
  "3xs": 2px,
));

// Remove from map
$theme-colors: map-remove($theme-colors, "info", "light");

// Get value from map
$primary-color: map-get($theme-colors, "primary");

// Nested map merge (for utilities)
$utilities: map-merge($utilities, (
  "width": map-merge(
    map-get($utilities, "width"),
    ( responsive: true )
  )
));
```

## Mixin Usage System

### Common Bootstrap Mixins

**Color Manipulation:**

```scss
@import "bootstrap/scss/functions";

$hover-color: tint-color($primary, 20%);   // Lighten by 20%
$active-color: shade-color($primary, 20%); // Darken by 20%
```

**Button Variant:**

```scss
@import "bootstrap/scss/mixins/buttons";

.btn-custom {
  @include button-variant(
    $background: #0066cc,
    $border: #0066cc,
    $color: #fff,
    $hover-background: shade-color(#0066cc, 10%),
    $hover-border: shade-color(#0066cc, 12%),
    $active-background: shade-color(#0066cc, 15%)
  );
}
```

**Media Query Mixins:**

```scss
@import "bootstrap/scss/mixins/breakpoints";

.custom-component {
  @include media-breakpoint-up(md) {
    // Styles for md and larger
  }

  @include media-breakpoint-down(sm) {
    // Styles for sm and smaller
  }
}
```

**Gradient Mixins:**

```scss
@import "bootstrap/scss/mixins/gradients";

.gradient-component {
  @include gradient-directional(#0066cc, #00cc66, 45deg);
}
```

## Utility API System

### How Utilities Are Generated

```scss
// Bootstrap's utility definition
$utilities: (
  "margin": (
    property: margin,
    class: m,
    values: map-merge($spacers, (auto: auto))
  ),
);

// Generates: .m-0, .m-1, .m-2, etc.
```

### Extending Utilities

```scss
$utilities: map-merge($utilities, (
  "opacity": (
    property: opacity,
    values: (
      0: 0,
      25: 0.25,
      50: 0.5,
      75: 0.75,
      100: 1,
    )
  )
));
```

## Common Mistakes

- **Wrong**: Not using !default for own variables → **Right**: Use !default for variables you want to be overridable
- **Wrong**: map-replace() instead of map-merge() → **Right**: Use map-merge() to preserve Bootstrap defaults
- **Wrong**: Using mixins without importing them → **Right**: Import specific mixin files first
- **Wrong**: Modifying Bootstrap source files → **Right**: Override via SCSS variables and maps

## See Also

- [SCSS Best Practices](scss-best-practices.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- [SCSS Integration Order](scss-integration-order.md)
- [Token to Utility Flow](token-to-utility-flow.md)
- Reference: [Bootstrap Sass Documentation](https://getbootstrap.com/docs/5.3/customize/sass/)
