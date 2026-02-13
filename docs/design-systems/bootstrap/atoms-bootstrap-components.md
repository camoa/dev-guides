---
description: Atoms to Bootstrap Components — mapping buttons, form inputs, and badges to Bootstrap's component system
---

# Atoms to Bootstrap Components

## When to Use

> Use when mapping atomic design system elements (buttons, inputs, badges) to Bootstrap's component system.

## Decision

| Atom Type | Bootstrap Variable | Bootstrap Mixin | Bootstrap Class | Custom Required |
|-----------|-------------------|-----------------|-----------------|-----------------|
| Button base | `$btn-padding-y`, `$btn-padding-x` | N/A | `.btn` | No |
| Button variants | `$primary`, etc. | `button-variant()` | `.btn-primary` | No (if using theme colors) |
| Form inputs | `$input-padding-y`, `$input-border-color` | N/A | `.form-control` | No |
| Badges | `$badge-padding-y`, `$badge-font-size` | N/A | `.badge` | No |

## Pattern

**Button Atoms**:
```scss
// Override button base variables
$btn-padding-y: 0.375rem;
$btn-padding-x: 0.75rem;
$btn-border-radius: 0.375rem;

// Add custom button variant to theme colors
$theme-colors: map-merge($theme-colors, (
  "brand": #0066cc,  // Auto-generates .btn-brand
));

@import "bootstrap";

// Create custom variant if needed
.btn-custom {
  @include button-variant(
    $background: $custom-bg,
    $border: $custom-border,
    $color: $custom-color,
    $hover-background: darken($custom-bg, 7.5%)
  );
}
```

**Form Input Atoms**:
```scss
$input-padding-y: 0.5rem;
$input-padding-x: 0.75rem;
$input-border-color: #ced4da;
$input-border-radius: 0.375rem;
$input-focus-border-color: #86b7fe;
$input-focus-box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);

@import "bootstrap";
```

**Badge Atoms**:
```scss
$badge-padding-y: 0.35em;
$badge-padding-x: 0.65em;
$badge-font-size: 0.75em;
$badge-font-weight: 700;
$badge-border-radius: 0.375rem;

@import "bootstrap";

// Usage in HTML:
// <span class="badge text-bg-primary">Primary</span>
// <span class="badge rounded-pill text-bg-success">Pill Badge</span>
```

## Common Mistakes

- **Wrong**: `@extend .btn` → **Right**: Use mixins or HTML classes (see SCSS Best Practices)
- **Wrong**: Hardcoding button padding → **Right**: Use `$btn-padding-*` variables
- **Wrong**: Not using `.form-control` class → **Right**: Bootstrap form styles require this class
- **Wrong**: Using old `.badge-*` color classes → **Right**: Bootstrap 5.3 uses `.text-bg-primary` pattern
- **Wrong**: Creating custom variants unnecessarily → **Right**: Add colors to `$theme-colors` instead

## See Also

- [Molecules to Component Combinations](molecules-component-combinations.md)
- [Design Tokens to Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Reference: [Bootstrap 5.3 Buttons](https://getbootstrap.com/docs/5.3/components/buttons/)
- Reference: [Bootstrap 5.3 Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
- Reference: [Bootstrap 5.3 Badges](https://getbootstrap.com/docs/5.3/components/badge/)
