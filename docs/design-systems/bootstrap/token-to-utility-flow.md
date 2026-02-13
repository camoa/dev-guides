---
description: Token to Utility Flow — how Bootstrap generates utility classes from tokens and how to extend the utility system
---

# Token to Utility Flow

## When to Use

> Use when understanding how Bootstrap generates utility classes from tokens, or when extending Bootstrap's utility system with design system tokens.

## Decision

| Scenario | Bootstrap Has | Strategy | Implementation |
|----------|--------------|----------|----------------|
| Need `.text-brand` class | Extensible `$theme-colors` map | EXTEND | Add to `$theme-colors` |
| Need `.p-3xs` micro-spacing | Extensible `$spacers` map | EXTEND | Add to `$spacers` |
| Need `.cursor-pointer` | No cursor utilities | CREATE | Add to `$utilities` map |
| Need responsive cursor | Utility API supports it | CREATE + responsive | Set `responsive: true` |
| Need custom elevation | No elevation system | CREATE | Custom utility definition |

## Pattern

**Utility Flow Understanding**:
```scss
// Step 1: Define token in SCSS variable
$primary: #0066cc;

// Step 2: Add to Bootstrap map
$theme-colors: map-merge($theme-colors, (
  "primary": $primary,
));

// Step 3-5: Bootstrap imports and processes
@import "bootstrap/scss/maps";
@import "bootstrap/scss/utilities";

// Result: .text-primary, .bg-primary, .btn-primary, .border-primary auto-generated
```

**Add New Utility**:
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

**Extend Existing Utility**:
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

- **Wrong**: Expecting manual class creation → **Right**: Bootstrap auto-generates utilities from maps
- **Wrong**: Maps merged AFTER Bootstrap import → **Right**: Merge BEFORE Bootstrap imports
- **Wrong**: Not importing utilities/api → **Right**: Custom utilities require `@import "bootstrap/scss/utilities/api"`
- **Wrong**: Adding utilities Bootstrap already has → **Right**: Research first (see Bootstrap Accommodation Decision Framework)
- **Wrong**: Not setting `responsive: true` → **Right**: Set for breakpoint variants

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [Design Tokens to Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Reference: [Bootstrap 5.3 Utility API](https://getbootstrap.com/docs/5.3/utilities/api/)
