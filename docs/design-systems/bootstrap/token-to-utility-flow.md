---
description: How Bootstrap generates utility classes from SCSS tokens and maps
---

# Token to Utility Flow

## When to Use

> Use this to understand how Bootstrap auto-generates utility classes from tokens and how to extend the utility system with custom maps.

## Utility Generation Flow

**Key Concept:** SCSS Variable → SCSS Map → Bootstrap Import → Utility API → Generated Classes

| SCSS Input | Utility API | Generated Output | Usage |
|-----------|------------|------------------|-------|
| `$spacers` map | `"margin"` utility | `.m-0`, `.m-1`, `.m-2` | `<div class="m-3">` |
| `$theme-colors` map | `"color"` utility | `.text-primary`, `.text-success` | `<p class="text-primary">` |
| `$theme-colors` map | `"background-color"` | `.bg-primary`, `.bg-success` | `<div class="bg-primary">` |
| `$grid-breakpoints` map | Responsive utilities | `.d-sm-block`, `.d-md-flex` | `<div class="d-lg-none">` |

## Pattern

```scss
// Step 1: Define token
$primary: #0066cc;

// Step 2: Add to Bootstrap map
$theme-colors: map-merge($theme-colors, (
  "primary": $primary,
));

// Step 3-5: Bootstrap imports and processes
@import "bootstrap/scss/maps";
@import "bootstrap/scss/utilities";

// Result: .text-primary, .bg-primary, .btn-primary, .border-primary
```

## Extending Utilities

| Scenario | Bootstrap Has | Strategy | Implementation |
|----------|--------------|----------|----------------|
| Need `.text-brand` | Extensible `$theme-colors` | EXTEND | Add to `$theme-colors` |
| Need `.p-3xs` | Extensible `$spacers` | EXTEND | Add to `$spacers` |
| Need `.cursor-pointer` | No cursor utilities | CREATE | Add to `$utilities` map |
| Need `.w-10` width | Extensible "width" utility | EXTEND | Modify values |

### Pattern: Add New Utility

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
// Generates: .cursor-pointer, .cursor-grab, .cursor-md-pointer
```

### Pattern: Extend Existing Utility

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
// Adds: .w-10, .w-15, .w-20
```

## Common Mistakes

- **Wrong**: Expecting manual class creation → **Right**: Bootstrap auto-generates from maps
- **Wrong**: Merging maps after Bootstrap import → **Right**: Merge BEFORE Bootstrap imports
- **Wrong**: Adding utilities Bootstrap has → **Right**: Research Bootstrap capabilities first
- **Wrong**: Not importing utilities/api → **Right**: Import `bootstrap/scss/utilities/api` for custom utilities
- **Wrong**: Ignoring responsive needs → **Right**: Set `responsive: true` for breakpoint variants

## See Also

- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md) - EXTEND category
- Reference: [Bootstrap Utility API](https://getbootstrap.com/docs/5.3/utilities/api/)
