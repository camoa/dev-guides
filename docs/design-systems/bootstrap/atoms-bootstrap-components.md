---
description: Map atomic design system components (buttons, inputs, badges) to Bootstrap
---

# Atoms → Bootstrap Components

## When to Use

> Use this to map atomic design system components (buttons, inputs, badges) to Bootstrap's component variables and mixins.

## Button Atoms

| Design System Need | Bootstrap Variable | Bootstrap Mixin | Bootstrap Class |
|-------------------|-------------------|-----------------|-----------------|
| Button base styles | `$btn-padding-y`, `$btn-padding-x` | N/A | `.btn` |
| Button color variants | `$primary`, `$secondary` | `button-variant()` | `.btn-primary` |
| Button sizes | `$btn-padding-y-sm`, `$btn-padding-x-lg` | N/A | `.btn-sm`, `.btn-lg` |
| Button border radius | `$btn-border-radius` | N/A | Applied to `.btn` |
| Custom button variant | N/A | `button-variant()` | Custom class |
| Outline buttons | N/A | `button-outline-variant()` | `.btn-outline-primary` |

### Pattern

```scss
// 1. Override button base variables
$btn-padding-y: 0.375rem;
$btn-padding-x: 0.75rem;
$btn-border-radius: 0.375rem;
$btn-font-weight: 400;

// 2. Add custom variant to theme colors
$theme-colors: map-merge($theme-colors, (
  "brand": #0066cc,  // Auto-generates .btn-brand
));

@import "bootstrap";

// 3. Create custom variant if needed
.btn-custom {
  @include button-variant(
    $background: $custom-bg,
    $border: $custom-border,
    $color: $custom-color
  );
}
```

## Form Input Atoms

| Design System Need | Bootstrap Variable | Bootstrap Class |
|-------------------|-------------------|-----------------|
| Input base styles | `$input-padding-y`, `$input-padding-x` | `.form-control` |
| Input border | `$input-border-color`, `$input-border-width` | Applied to `.form-control` |
| Input border radius | `$input-border-radius` | Applied to `.form-control` |
| Input focus state | `$input-focus-border-color`, `$input-focus-box-shadow` | Applied on `:focus` |
| Input sizes | `$input-padding-y-sm`, `$input-padding-x-lg` | `.form-control-sm`, `.form-control-lg` |
| Select inputs | `$form-select-*` variables | `.form-select` |
| Checkboxes/radios | `$form-check-*` variables | `.form-check-input` |

### Pattern

```scss
$input-padding-y: 0.5rem;
$input-padding-x: 0.75rem;
$input-border-color: #ced4da;
$input-border-radius: 0.375rem;
$input-focus-border-color: #86b7fe;
$input-focus-box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);

// Select-specific
$form-select-padding-y: $input-padding-y;
$form-select-padding-x: $input-padding-x;

@import "bootstrap";
```

## Badge/Label Atoms

| Design System Need | Bootstrap Variable | Bootstrap Class |
|-------------------|-------------------|-----------------|
| Badge base styles | `$badge-padding-y`, `$badge-padding-x` | `.badge` |
| Badge font size | `$badge-font-size` | Applied to `.badge` |
| Badge font weight | `$badge-font-weight` | Applied to `.badge` |
| Badge border radius | `$badge-border-radius` | Applied to `.badge` |
| Badge color variants | Uses `$theme-colors` | `.badge.text-bg-primary` |
| Pill badges | N/A | `.rounded-pill` |

### Pattern

```scss
$badge-padding-y: 0.35em;
$badge-padding-x: 0.65em;
$badge-font-size: 0.75em;
$badge-font-weight: 700;
$badge-border-radius: 0.375rem;

@import "bootstrap";

// Usage:
// <span class="badge text-bg-primary">Primary</span>
// <span class="badge rounded-pill text-bg-success">Pill</span>
```

## Common Mistakes

- **Wrong**: Using @extend .btn → **Right**: Use button-variant() mixin or Bootstrap variables
- **Wrong**: Hardcoding button padding → **Right**: Use $btn-padding-* variables
- **Wrong**: Not using .form-control class → **Right**: Bootstrap form styles require class
- **Wrong**: Using old .badge-* color classes → **Right**: Bootstrap 5.3 uses .text-bg-primary pattern
- **Wrong**: Hardcoding focus styles → **Right**: Use $input-focus-* variables

## See Also

- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- [Molecules → Component Combinations](molecules-component-combinations.md)
- Reference: [Bootstrap Buttons](https://getbootstrap.com/docs/5.3/components/buttons/)
- Reference: [Bootstrap Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
- Reference: [Bootstrap Badges](https://getbootstrap.com/docs/5.3/components/badge/)
