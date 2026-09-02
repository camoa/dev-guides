---
description: "Critical SCSS import sequence for Bootstrap customization"
tldr: "Use this when setting up SCSS file structure or troubleshooting variable override issues. Import order is critical for Bootstrap customization."
drupal_version: "11.x"
---

# SCSS Integration Order

## When to Use

> Use this when setting up SCSS file structure or troubleshooting variable override issues. Import order is critical for Bootstrap customization.

- You're setting up your SCSS file structure
- You need to know the correct import order for Bootstrap customization
- You're troubleshooting variable override issues

## Critical Import Sequence

### Decision Table: Import Order Steps

| Step | What to Import | Why This Order | Example |
|------|---------------|----------------|---------|
| 1 | Bootstrap functions | Required for color/math operations | `@import "bootstrap/scss/functions";` |
| 2 | Design system variables | Override Bootstrap defaults | `$primary: #0066cc;` |
| 3 | Bootstrap variables | Loads Bootstrap defaults (with `!default`) | `@import "bootstrap/scss/variables";` |
| 4 | Bootstrap dark mode variables | Loads dark mode defaults | `@import "bootstrap/scss/variables-dark";` |
| 5 | Design system map extensions | Add to Bootstrap maps | `$theme-colors: map-merge(...)` |
| 6 | Bootstrap maps | Loads Bootstrap maps | `@import "bootstrap/scss/maps";` |
| 7 | Bootstrap mixins | Loads Bootstrap mixins | `@import "bootstrap/scss/mixins";` |
| 8 | Bootstrap root | Generates CSS variables | `@import "bootstrap/scss/root";` |
| 9 | Bootstrap components | All components (or selective) | `@import "bootstrap/scss/bootstrap";` |
| 10 | Bootstrap utilities | Utility classes | `@import "bootstrap/scss/utilities";` |
| 11 | Custom utility additions | Extend utility API | `$utilities: map-merge(...)` |
| 12 | Bootstrap utilities API | Generates utilities | `@import "bootstrap/scss/utilities/api";` |
| 13 | Custom components | Your custom SCSS | `@import "custom/components";` |

### Pattern: Complete SCSS Structure

```scss
// File: custom.scss (main entry point)

// Step 1: Import Bootstrap functions (required first)
@import "bootstrap/scss/functions";

// Step 2: Override Bootstrap variables (before Bootstrap imports them)
$primary: #194582;
$secondary: #6c757d;
$font-family-base: system-ui, -apple-system, sans-serif;
$spacer: 1rem;

// Step 3-4: Import Bootstrap variables (including dark mode)
@import "bootstrap/scss/variables";
@import "bootstrap/scss/variables-dark";

// Step 5: Extend Bootstrap maps (after variables loaded)
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

// Step 10: Import all Bootstrap components
@import "bootstrap/scss/bootstrap";
// OR selective imports:
// @import "bootstrap/scss/buttons";
// @import "bootstrap/scss/forms";

// Step 11: Import Bootstrap utilities (before API)
@import "bootstrap/scss/utilities";

// Step 12: Extend utility API (before API import)
$utilities: map-merge($utilities, (
  "cursor": (
    property: cursor,
    class: cursor,
    values: pointer grab
  )
));

// Step 13: Import utilities API to generate utilities
@import "bootstrap/scss/utilities/api";

// Step 14: Your custom components and overrides
@import "custom/components";
@import "custom/utilities";
```

### Common Mistakes

- **Importing Bootstrap before overrides** - Variables must be set BEFORE Bootstrap import
- **Not importing functions first** - Functions are required for color operations
- **Importing utilities/api too early** - Must come after all utility customizations
- **Using `@import "bootstrap"` for everything** - This imports ALL of Bootstrap; use selective imports for smaller bundles
- **Not understanding `!default` flag** - Bootstrap variables use `!default`, so your values take precedence ONLY if set before import

### See Also

- Bootstrap 5.3 Sass Customization: [https://getbootstrap.com/docs/5.3/customize/sass/](https://getbootstrap.com/docs/5.3/customize/sass/)
- [Section 1.4: SCSS Best Practices](scss-best-practices.md) - Bootstrap integration patterns

## File Organization Strategy

### Decision Table: File Structure Options

| Strategy | Use Case | Structure | Pros/Cons |
|----------|----------|-----------|-----------|
| Single file | Simple projects | All customizations in one `custom.scss` | Simple, but harder to maintain |
| Modular | Medium projects | Separate files for variables, maps, components | Organized, easier to maintain |
| Design system aligned | Complex projects | Mirror design system structure (tokens, atoms, etc.) | Clear mapping, scalable |

### Pattern: Modular File Structure

```
scss/
├── custom.scss                        # Main entry point
├── _design-system-variables.scss      # Design system token definitions
├── _bootstrap-variable-overrides.scss # Bootstrap variable overrides
├── _bootstrap-map-extensions.scss     # Additions to Bootstrap maps
├── _custom-utilities.scss             # Custom utility definitions
└── components/
    ├── _buttons.scss                  # Custom button styles
    ├── _forms.scss                    # Custom form styles
    └── _cards.scss                    # Custom card styles
```

**Main Entry Point:**
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
@import "components/cards";
```

### Common Mistakes

- **Not using partials** - SCSS partials (prefix with `_`) prevent direct compilation
- **Circular imports** - Avoid files importing each other
- **Importing Bootstrap multiple times** - Only import Bootstrap once in main entry point
- **Not documenting file structure** - Add comments explaining organization

### See Also

- Sass Guidelines: [https://sass-guidelin.es/#architecture](https://sass-guidelin.es/#architecture)
- [Section 1.4: SCSS Best Practices](scss-best-practices.md) - File organization standards

## See Also

- [Templates → Bootstrap Grid](templates-bootstrap-grid.md)
- [Key Bootstrap SCSS Mechanisms](key-bootstrap-scss-mechanisms.md)
