---
description: SCSS Integration Order — correct import sequence for Bootstrap customization and file organization strategies
---

# SCSS Integration Order

## When to Use

> Use when setting up SCSS file structure, troubleshooting variable override issues, or organizing Bootstrap customization files.

## Decision

| Step | Import | Why |
|------|--------|-----|
| 1 | Bootstrap functions | Required for color/math operations |
| 2 | Design system variables | Override Bootstrap defaults |
| 3 | Bootstrap variables | Loads Bootstrap defaults (`!default`) |
| 4-7 | Bootstrap core (maps, mixins, root) | Bootstrap foundation |
| 8-9 | Bootstrap components | All or selective imports |
| 10-11 | Custom utilities + utilities API | Extend utility system |
| 12 | Custom components | Your custom SCSS |

## Pattern

**Complete SCSS Structure**:
```scss
// File: custom.scss (main entry point)

// Step 1: Import Bootstrap functions
@import "bootstrap/scss/functions";

// Step 2: Override Bootstrap variables
$primary: #194582;
$secondary: #6c757d;
$font-family-base: system-ui, -apple-system, sans-serif;

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
@import "bootstrap/scss/bootstrap";

// Step 10: Import Bootstrap utilities
@import "bootstrap/scss/utilities";

// Step 11: Extend utility API
$utilities: map-merge($utilities, (
  "cursor": (
    property: cursor,
    class: cursor,
    values: pointer grab
  )
));

// Step 12: Import utilities API
@import "bootstrap/scss/utilities/api";

// Step 13: Your custom components
@import "custom/components";
```

**Modular File Structure**:
```
scss/
├── custom.scss                        # Main entry point
├── _design-system-variables.scss      # Design system tokens
├── _bootstrap-variable-overrides.scss # Bootstrap variable overrides
├── _bootstrap-map-extensions.scss     # Bootstrap map additions
├── _custom-utilities.scss             # Custom utility definitions
└── components/
    ├── _buttons.scss
    ├── _forms.scss
    └── _cards.scss
```

**Main Entry Point** (modular):
```scss
// custom.scss
@import "bootstrap/scss/functions";
@import "design-system-variables";
@import "bootstrap-variable-overrides";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/variables-dark";
@import "bootstrap-map-extensions";
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/root";
@import "bootstrap/scss/bootstrap";
@import "bootstrap/scss/utilities";
@import "custom-utilities";
@import "bootstrap/scss/utilities/api";
@import "components/buttons";
@import "components/forms";
```

## Common Mistakes

- **Wrong**: Bootstrap import before overrides → **Right**: Variables BEFORE Bootstrap import (`!default` flag)
- **Wrong**: Not importing functions first → **Right**: Functions required for color operations
- **Wrong**: utilities/api too early → **Right**: After all utility customizations
- **Wrong**: `@import "bootstrap"` for everything → **Right**: Selective imports for smaller bundles
- **Wrong**: Circular imports → **Right**: Files shouldn't import each other
- **Wrong**: Not using partials → **Right**: SCSS partials (prefix `_`) prevent direct compilation

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- Reference: [Bootstrap 5.3 Sass Customization](https://getbootstrap.com/docs/5.3/customize/sass/)
- Reference: [Sass Guidelines: Architecture](https://sass-guidelin.es/#architecture)
