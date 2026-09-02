---
description: "How Bootstrap generates utility classes from SCSS tokens and maps"
tldr: "Use this to understand how Bootstrap auto-generates utility classes from tokens and how to extend the utility system with custom maps."
drupal_version: "11.x"
---

# Token to Utility Flow

## When to Use

> Use this to understand how Bootstrap auto-generates utility classes from tokens and how to extend the utility system with custom maps.

- You need to understand how Bootstrap generates utility classes from tokens
- You're extending Bootstrap's utility system with design system tokens
- You want to auto-generate classes from your custom token maps

## Utility API Basics

### Decision Table: Understanding Utility Generation

| SCSS Input | Utility API Processing | Generated Output | Usage |
|-----------|----------------------|------------------|-------|
| `$spacers` map | `"margin"` utility definition | `.m-0`, `.m-1`, `.m-2`, etc. | `<div class="m-3">` |
| `$theme-colors` map | `"color"` utility definition | `.text-primary`, `.text-success` | `<p class="text-primary">` |
| `$theme-colors` map | `"background-color"` utility | `.bg-primary`, `.bg-success` | `<div class="bg-primary">` |
| `$grid-breakpoints` map | Applied to responsive utilities | `.d-sm-block`, `.d-md-flex` | `<div class="d-lg-none">` |
| Custom map | Custom utility definition | Custom classes | Custom implementation |

### Pattern: Utility Flow Understanding

```scss
// Step 1: Define token in SCSS variable
$primary: #0066cc;

// Step 2: Add to Bootstrap map
$theme-colors: map-merge($theme-colors, (
  "primary": $primary,  // Bootstrap merges this
));

// Step 3: Bootstrap imports the map
@import "bootstrap/scss/maps";

// Step 4: Utility API processes map
@import "bootstrap/scss/utilities";

// Step 5: Utilities auto-generated
// Result: .text-primary, .bg-primary, .btn-primary, .border-primary
```

**Key Concept:** SCSS Variable → SCSS Map → Bootstrap Import → Utility API → Generated Classes

### Common Mistakes

- **Expecting manual class creation** - Bootstrap auto-generates utilities from maps
- **Not understanding map-merge timing** - Maps must be merged BEFORE Bootstrap imports them
- **Ignoring utility API documentation** - Many customizations are possible via `$utilities` map
- **Assuming all variables generate utilities** - Only variables in specific maps generate utilities

### See Also

- Bootstrap 5.3 Utility API: [https://getbootstrap.com/docs/5.3/utilities/api/](https://getbootstrap.com/docs/5.3/utilities/api/)
- [Section 1.3: Bootstrap Research Methodology](bootstrap-accommodation-decision-framework.md) - Map examination process

## Extending Utilities

### Decision Table: When to Extend vs Create

| Scenario | Bootstrap Has | Strategy | Implementation |
|----------|--------------|----------|----------------|
| Need `.text-brand` class | Extensible `$theme-colors` map | EXTEND | Add to `$theme-colors` |
| Need `.p-3xs` micro-spacing | Extensible `$spacers` map | EXTEND | Add to `$spacers` |
| Need `.cursor-pointer` | No cursor utilities | CREATE | Add to `$utilities` map |
| Need responsive cursor | Utility API supports it | CREATE + responsive | Set `responsive: true` |
| Need `.w-10` width | Extensible `$utilities` "width" | EXTEND | Modify "width" utility values |
| Need custom elevation | No elevation system | CREATE | Custom utility definition |

### Pattern: Extending Utility API

**Add New Utility:**
```scss
$utilities: map-merge($utilities, (
  "cursor": (
    property: cursor,
    class: cursor,
    responsive: true,
    values: auto pointer grab not-allowed
  )
));

@import "bootstrap/scss/utilities/api";
// Generates: .cursor-pointer, .cursor-grab, .cursor-md-pointer, etc.
```

**Extend Existing Utility:**
```scss
$utilities: map-merge($utilities, (
  "width": map-merge(
    map-get($utilities, "width"),
    (
      values: map-merge(
        map-get(map-get($utilities, "width"), "values"),
        (10: 10%, 15: 15%, 20: 20%)
      )
    )
  )
));

@import "bootstrap/scss/utilities/api";
// Adds: .w-10, .w-15, .w-20 to existing width utilities
```

### Common Mistakes

- **Not importing utilities/api** - Custom utilities require `@import "bootstrap/scss/utilities/api"` at the end
- **Merging maps in wrong order** - Use `map-merge()` to preserve Bootstrap defaults
- **Adding utilities Bootstrap already has** - Research first (see [Section 1.3: Bootstrap Research Methodology](bootstrap-accommodation-decision-framework.md))
- **Not considering responsive needs** - Set `responsive: true` for breakpoint variants
- **Forgetting `!important`** - Bootstrap utilities use `!important` by default (controlled by `$enable-important-utilities`)

### See Also

- Bootstrap 5.3 Utility API Full Documentation: [https://getbootstrap.com/docs/5.3/utilities/api/](https://getbootstrap.com/docs/5.3/utilities/api/)
- [Section 1.2: EXTEND Category](bootstrap-accommodation-decision-framework.md) - Implementation strategy for extensions

## See Also

- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md) - EXTEND category
