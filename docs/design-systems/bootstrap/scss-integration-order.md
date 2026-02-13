---
description: Critical SCSS import sequence for Bootstrap customization
---

# SCSS Integration Order

## When to Use

> Use this when setting up SCSS file structure or troubleshooting variable override issues. Import order is critical for Bootstrap customization.

## Critical Import Sequence

| Step | What to Import | Why This Order |
|------|---------------|----------------|
| 1 | Bootstrap functions | Required for color/math operations |
| 2 | Design system variables | Override Bootstrap defaults |
| 3 | Bootstrap variables | Loads Bootstrap defaults (`!default`) |
| 4 | Bootstrap dark mode variables | Loads dark mode defaults |
| 5 | Design system map extensions | Add to Bootstrap maps |
| 6 | Bootstrap maps | Loads Bootstrap maps |
| 7 | Bootstrap mixins | Loads Bootstrap mixins |
| 8 | Bootstrap root | Generates CSS variables |
| 9 | Bootstrap components | All components (or selective) |
| 10 | Bootstrap utilities | Utility classes |
| 11 | Custom utility additions | Extend utility API |
| 12 | Bootstrap utilities API | Generates utilities |
| 13 | Custom components | Your custom SCSS |

## Pattern

```scss
// File: custom.scss (main entry point)

// Step 1: Import Bootstrap functions (required first)
@import "bootstrap/scss/functions";

// Step 2: Override Bootstrap variables
$primary: #194582;
$secondary: #6c757d;
$font-family-base: system-ui, -apple-system, sans-serif;
$spacer: 1rem;

// Step 3-4: Import Bootstrap variables
@import "bootstrap/scss/variables";
@import "bootstrap/scss/variables-dark";

// Step 5: Extend Bootstrap maps
$theme-colors: map-merge($theme-colors, (
  "brand": #0066cc,
));

$spacers: map-merge($spacers, (
  "3xs": 2px,
));

// Step 6-9: Import Bootstrap core
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";

// Step 10: Import Bootstrap components
@import "bootstrap/scss/bootstrap";
// OR selective imports for smaller bundles:
// @import "bootstrap/scss/buttons";
// @import "bootstrap/scss/forms";

// Step 11: Import utilities
@import "bootstrap/scss/utilities";

// Step 12: Extend utility API
$utilities: map-merge($utilities, (
  "cursor": (
    property: cursor,
    class: cursor,
    values: pointer grab
  )
));

// Step 13: Import utilities API
@import "bootstrap/scss/utilities/api";

// Step 14: Your custom components
@import "custom/components";
@import "custom/utilities";
```

## Common Mistakes

- **Wrong**: Importing Bootstrap before overrides → **Right**: Set variables BEFORE Bootstrap import
- **Wrong**: Not importing functions first → **Right**: Functions required for color operations
- **Wrong**: Importing utilities/api too early → **Right**: Must come after all utility customizations
- **Wrong**: Using `@import "bootstrap"` for everything → **Right**: Use selective imports for smaller bundles
- **Wrong**: Not understanding `!default` flag → **Right**: Your values take precedence ONLY if set before import

## See Also

- [SCSS Best Practices](scss-best-practices.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md) - Import order details
- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Reference: [Bootstrap Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
