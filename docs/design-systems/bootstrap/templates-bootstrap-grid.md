---
description: Templates to Bootstrap Grid — mapping page layouts and content structures to Bootstrap's grid system
---

# Templates to Bootstrap Grid

## When to Use

> Use when mapping templates (page layouts, content structures) to Bootstrap's grid system for responsive page structures.

## Decision

| Layout Need | Bootstrap Variable | Bootstrap Map | Generated Classes |
|-------------|-------------------|---------------|-------------------|
| Column count | `$grid-columns` | N/A | `.col-*` (default 12) |
| Gutter width | `$grid-gutter-width` | N/A | Applied to `.row` |
| Container widths | N/A | `$container-max-widths` | `.container` breakpoint widths |
| Breakpoints | N/A | `$grid-breakpoints` | `.col-sm-*`, `.col-md-*`, etc. |
| Gutters (custom) | N/A | `$gutters` map | `.g-*`, `.gx-*`, `.gy-*` utilities |

## Pattern

**Grid System Configuration**:
```scss
// Override grid fundamentals
$grid-columns: 12;              // Keep Bootstrap default
$grid-gutter-width: 1.5rem;     // 24px gutter

// Customize container widths
$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 960px,
  xl: 1140px,
  xxl: 1320px
);

// Add custom gutter sizes
$gutters: map-merge($gutters, (
  6: 4rem,   // Larger gutter option
));

@import "bootstrap";
```

**HTML Usage**:
```html
<!-- Responsive grid -->
<div class="container">
  <div class="row">
    <div class="col-12 col-md-6 col-lg-4">Column 1</div>
    <div class="col-12 col-md-6 col-lg-4">Column 2</div>
    <div class="col-12 col-md-6 col-lg-4">Column 3</div>
  </div>
</div>

<!-- Custom gutters -->
<div class="row g-6">
  <div class="col">Large gutter</div>
</div>
```

## Common Mistakes

- **Wrong**: Changing column count from 12 → **Right**: Most design systems work with 12 columns
- **Wrong**: Not using responsive column classes → **Right**: Use `.col-sm-*`, `.col-md-*`
- **Wrong**: Starting with desktop → **Right**: Mobile-first approach (`.col-*` first, then breakpoint-specific)
- **Wrong**: Not using gutter utilities → **Right**: Use `.g-*`, `.gx-*`, `.gy-*` for custom spacing
- **Wrong**: Creating custom grid systems → **Right**: Extend Bootstrap's flexible grid

## See Also

- [Organisms to Layout + Components](organisms-layout-components.md)
- [SCSS Integration Order](scss-integration-order.md)
- Reference: [Bootstrap 5.3 Grid](https://getbootstrap.com/docs/5.3/layout/grid/)
- Reference: [Bootstrap 5.3 Columns](https://getbootstrap.com/docs/5.3/layout/columns/)
- Reference: [Bootstrap 5.3 Gutters](https://getbootstrap.com/docs/5.3/layout/gutters/)
