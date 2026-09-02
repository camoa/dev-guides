---
description: "Map atomic design system components (buttons, inputs, badges) to Bootstrap"
tldr: "Use this to map atomic design system components (buttons, inputs, badges) to Bootstrap's component variables and mixins."
drupal_version: "11.x"
---

# Atoms → Bootstrap Components

## When to Use

> Use this to map atomic design system components (buttons, inputs, badges) to Bootstrap's component variables and mixins.

- You've identified atoms (buttons, inputs, badges) from your design system
- You need to map these atomic components to Bootstrap's component system
- You're implementing the smallest UI building blocks

## Button Atoms

### Decision Table: Button Implementation

| Design System Need | Bootstrap Variable | Bootstrap Mixin | Bootstrap Class | Custom Required |
|-------------------|-------------------|-----------------|-----------------|-----------------|
| Button base styles | `$btn-padding-y`, `$btn-padding-x` | N/A | `.btn` | No |
| Button color variants | `$primary`, `$secondary`, etc. | `button-variant()` | `.btn-primary` | No (if using theme colors) |
| Button sizes | `$btn-padding-y-sm`, `$btn-padding-x-lg` | N/A | `.btn-sm`, `.btn-lg` | No |
| Button border radius | `$btn-border-radius` | N/A | Applied to `.btn` | No |
| Custom button variant | N/A | `button-variant($bg, $border, $color)` | Custom class | Yes (CREATE) |
| Outline buttons | N/A | `button-outline-variant()` | `.btn-outline-primary` | No |

### Pattern: Button Token Mapping

```scss
// 1. Override button base variables
$btn-padding-y: 0.375rem;
$btn-padding-x: 0.75rem;
$btn-border-radius: 0.375rem;
$btn-font-weight: 400;

// 2. Add custom button variant to theme colors
$theme-colors: map-merge($theme-colors, (
  "brand": #0066cc,  // Auto-generates .btn-brand
));

@import "bootstrap";

// 3. Create custom variant if needed (post-Bootstrap)
.btn-custom {
  @include button-variant(
    $background: $custom-bg,
    $border: $custom-border,
    $color: $custom-color,
    $hover-background: darken($custom-bg, 7.5%),
    $hover-border: darken($custom-border, 10%),
    $active-background: darken($custom-bg, 10%)
  );
}
```

### Common Mistakes

- **Using @extend .btn** - Never use `@extend` with Bootstrap classes (see [Section 1.4: SCSS Best Practices](scss-best-practices.md))
- **Hardcoding button padding** - Use `$btn-padding-*` variables
- **Not using button mixins** - Use `button-variant()` for custom colors
- **Ignoring disabled state** - Bootstrap handles `:disabled` automatically
- **Not considering focus states** - Bootstrap focus ring is configurable via `$focus-ring-*` variables

### See Also

- Bootstrap 5.3 Buttons: [https://getbootstrap.com/docs/5.3/components/buttons/](https://getbootstrap.com/docs/5.3/components/buttons/)
- Bootstrap Button Mixins Reference: `/core/scss/mixins/_buttons.scss`

## Form Input Atoms

### Decision Table: Form Input Implementation

| Design System Need | Bootstrap Variable | Bootstrap Class | Custom Required |
|-------------------|-------------------|-----------------|-----------------|
| Input base styles | `$input-padding-y`, `$input-padding-x` | `.form-control` | No |
| Input border | `$input-border-color`, `$input-border-width` | Applied to `.form-control` | No |
| Input border radius | `$input-border-radius` | Applied to `.form-control` | No |
| Input focus state | `$input-focus-border-color`, `$input-focus-box-shadow` | Applied on `:focus` | No |
| Input sizes | `$input-padding-y-sm`, `$input-padding-x-lg` | `.form-control-sm`, `.form-control-lg` | No |
| Input disabled state | `$input-disabled-bg`, `$input-disabled-border-color` | Applied on `:disabled` | No |
| Select inputs | `$form-select-*` variables | `.form-select` | No |
| Checkboxes/radios | `$form-check-*` variables | `.form-check-input` | No |

### Pattern: Form Input Mapping

```scss
// 1. Override input base variables
$input-padding-y: 0.5rem;
$input-padding-x: 0.75rem;
$input-border-color: #ced4da;
$input-border-radius: 0.375rem;
$input-focus-border-color: #86b7fe;
$input-focus-box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);

// 2. Override select-specific variables
$form-select-padding-y: $input-padding-y;
$form-select-padding-x: $input-padding-x;

@import "bootstrap";
```

### Common Mistakes

- **Not using form-control class** - Bootstrap form styles require `.form-control` class
- **Mixing input and select variables** - Selects have separate `$form-select-*` variables
- **Ignoring validation states** - Bootstrap has built-in `.is-valid` and `.is-invalid` styles
- **Not considering floating labels** - Bootstrap 5.3 supports floating labels (`.form-floating`)
- **Hardcoding focus styles** - Use `$input-focus-*` variables for consistency

### See Also

- Bootstrap 5.3 Forms: [https://getbootstrap.com/docs/5.3/forms/overview/](https://getbootstrap.com/docs/5.3/forms/overview/)
- Bootstrap Form Validation: [https://getbootstrap.com/docs/5.3/forms/validation/](https://getbootstrap.com/docs/5.3/forms/validation/)

## Badge/Label Atoms

### Decision Table: Badge Implementation

| Design System Need | Bootstrap Variable | Bootstrap Class | Custom Required |
|-------------------|-------------------|-----------------|-----------------|
| Badge base styles | `$badge-padding-y`, `$badge-padding-x` | `.badge` | No |
| Badge font size | `$badge-font-size` | Applied to `.badge` | No |
| Badge font weight | `$badge-font-weight` | Applied to `.badge` | No |
| Badge border radius | `$badge-border-radius` | Applied to `.badge` | No |
| Badge color variants | Uses `$theme-colors` | `.badge.text-bg-primary` | No |
| Pill badges | N/A | `.rounded-pill` | No (combine classes) |

### Pattern: Badge Mapping

```scss
// Override badge variables
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

### Common Mistakes

- **Using old `.badge-*` color classes** - Bootstrap 5.3 uses `.text-bg-primary` pattern
- **Not using em units** - Badge sizing uses em for scaling with parent font size
- **Creating custom badge variants unnecessarily** - Add colors to `$theme-colors` instead
- **Ignoring pill variant** - Use `.rounded-pill` utility class for pill badges

### See Also

- Bootstrap 5.3 Badges: [https://getbootstrap.com/docs/5.3/components/badge/](https://getbootstrap.com/docs/5.3/components/badge/)
- Bootstrap 5.3 Color Utilities: [https://getbootstrap.com/docs/5.3/utilities/colors/](https://getbootstrap.com/docs/5.3/utilities/colors/)

## See Also

- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- [Molecules → Component Combinations](molecules-component-combinations.md)
