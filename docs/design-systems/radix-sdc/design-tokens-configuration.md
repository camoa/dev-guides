---
description: Radix design tokens configuration — variable override location, SCSS import order, theme settings integration
drupal_version: "11.x"
---

# Design Tokens Configuration in Radix

## When to Use

> Use this after mapping tokens to Bootstrap variables (using Bootstrap Mapping Guide) to know WHERE to put variable overrides in Radix.

## Decision

| Token Category | Bootstrap Variable | Radix Override Location | Implementation |
|----------------|-------------------|------------------------|----------------|
| Colors | `$primary`, `$theme-colors` | `src/scss/base/_variables.scss` | Set before Bootstrap import |
| Typography | `$font-family-base`, `$h1-font-size` | `src/scss/base/_variables.scss` | Set before Bootstrap import |
| Spacing | `$spacer`, `$spacers` map | `src/scss/base/_variables.scss` | Override or extend map |
| Borders/Radius | `$border-radius`, `$box-shadow` | `src/scss/base/_variables.scss` | Set before Bootstrap import |
| Breakpoints | `$grid-breakpoints` | `src/scss/base/_variables.scss` | Override entire map |
| Custom utilities | N/A | `src/scss/base/_utilities.scss` | Use Bootstrap utilities API |

## Pattern

**File: `src/scss/base/_variables.scss`**

```scss
/**
 * Variables
 *
 * Customization:
 * Copy desired variable from node_modules/bootstrap/scss/_variables.scss
 * Change the value and remove the !default flag
 */

// Color tokens
$primary: #194582;
$secondary: #6c757d;

// Typography tokens
$font-family-base: system-ui, -apple-system, "Segoe UI", sans-serif;
$font-size-base: 1rem;
$line-height-base: 1.5;

// Border/radius tokens
$border-radius: 0.375rem;
$border-radius-sm: 0.25rem;
$border-radius-lg: 0.5rem;

// Shadow tokens
$box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
```

**CRITICAL:** This file is imported BEFORE Bootstrap in `_init.scss`, so variables override Bootstrap defaults.

**Design Token Approach Selection:**

| Approach | Use When | Example |
|----------|----------|---------|
| **SCSS Variables** | Design tokens (colors, spacing, typography) | `$primary: #194582;` |
| **Drupal Theme Settings** | User-configurable options | Logo upload, site name toggle |
| **CSS Custom Properties** | Runtime theming (dark mode toggle) | `--bs-primary: #194582;` |

## Common Mistakes

- **Wrong**: Setting variables after Bootstrap import → **Right**: Must be BEFORE
- **Wrong**: Using `!default` flag in custom variables → **Right**: Remove it (only Bootstrap uses `!default`)
- **Wrong**: Hardcoding values in components → **Right**: Use variables for consistency
- **Wrong**: Modifying `_init.scss` directly → **Right**: Override in `base/_variables.scss` instead
- **Wrong**: Expecting theme settings to control tokens → **Right**: Tokens are compile-time (SCSS)
- **Wrong**: Overusing runtime customization → **Right**: Most tokens should be compile-time for performance

## See Also

- [Sub-Theme Architecture](sub-theme-architecture.md)
- [Atoms SDC Components](atoms-sdc-components.md)
- Bootstrap Mapping Guide: Section 2 (Design Tokens → Bootstrap Variables)
- Bootstrap Mapping Guide: Section 8 (SCSS Integration Order)
