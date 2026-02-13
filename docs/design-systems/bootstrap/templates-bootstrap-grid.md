---
description: Map template-level page layouts to Bootstrap's grid system
---

# Templates → Bootstrap Grid

## When to Use

> Use this for mapping templates (page layouts, content structures) to Bootstrap's grid system for responsive page structures.

## Grid Configuration

| Design System Need | Bootstrap Variable | Bootstrap Map | Generated Classes |
|-------------------|-------------------|---------------|-------------------|
| Column count | `$grid-columns` | N/A | `.col-*` (default 12) |
| Gutter width | `$grid-gutter-width` | N/A | Applied to `.row` |
| Container widths | N/A | `$container-max-widths` | `.container` breakpoint widths |
| Breakpoints | N/A | `$grid-breakpoints` | `.col-sm-*`, `.col-md-*`, etc. |
| Row columns | N/A | N/A | `.row-cols-*` utilities |
| Gutters (custom) | N/A | `$gutters` map | `.g-*`, `.gx-*`, `.gy-*` utilities |

## Pattern

```scss
// 1. Override grid fundamentals
$grid-columns: 12;              // Keep Bootstrap default
$grid-gutter-width: 1.5rem;     // 24px gutter

// 2. Customize container widths
$container-max-widths: (
  sm: 540px,
  md: 720px,
  lg: 960px,
  xl: 1140px,
  xxl: 1320px
);

// 3. Add custom gutter sizes if needed
$gutters: map-merge($gutters, (
  6: 4rem,   // Add larger gutter option
));

@import "bootstrap";
```

## Usage

```html
<!-- Basic 2-column layout -->
<div class="container">
  <div class="row">
    <div class="col-md-8">Main content</div>
    <div class="col-md-4">Sidebar</div>
  </div>
</div>

<!-- Responsive 3-column grid -->
<div class="container">
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
    <div class="col"><div class="card">...</div></div>
    <div class="col"><div class="card">...</div></div>
    <div class="col"><div class="card">...</div></div>
  </div>
</div>

<!-- Custom gutters -->
<div class="container">
  <div class="row gx-5 gy-3">
    <div class="col-md-6">Content</div>
    <div class="col-md-6">Content</div>
  </div>
</div>
```

## Common Mistakes

- **Wrong**: Changing column count from 12 → **Right**: Keep 12 columns (standard in design systems)
- **Wrong**: Not using responsive column classes → **Right**: Use .col-sm-*, .col-md-* for responsive layouts
- **Wrong**: Forgetting mobile-first approach → **Right**: Start with mobile (.col-*), then add breakpoint classes
- **Wrong**: Not using gutter utilities → **Right**: Use .g-*, .gx-*, .gy-* for custom spacing
- **Wrong**: Creating custom grid systems → **Right**: Extend Bootstrap's grid instead

## See Also

- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md) - Breakpoint tokens
- [Organisms → Layout + Components](organisms-layout-components.md)
- Reference: [Bootstrap Grid](https://getbootstrap.com/docs/5.3/layout/grid/)
- Reference: [Bootstrap Columns](https://getbootstrap.com/docs/5.3/layout/columns/)
- Reference: [Bootstrap Gutters](https://getbootstrap.com/docs/5.3/layout/gutters/)
