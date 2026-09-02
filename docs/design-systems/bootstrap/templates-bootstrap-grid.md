---
description: "Map template-level page layouts to Bootstrap's grid system"
tldr: "Use this for mapping templates (page layouts, content structures) to Bootstrap's grid system for responsive page structures."
drupal_version: "11.x"
---

# Templates → Bootstrap Grid

## When to Use

> Use this for mapping templates (page layouts, content structures) to Bootstrap's grid system for responsive page structures.

- You've identified templates (page layouts, content structures) from your design system
- You need to implement responsive page structures
- You're mapping layout patterns to Bootstrap's grid system

## Grid System Mapping

### Decision Table: Grid Configuration

| Design System Need | Bootstrap Variable | Bootstrap Map | Generated Classes |
|-------------------|-------------------|---------------|-------------------|
| Column count | `$grid-columns` | N/A | `.col-*` (default 12) |
| Gutter width | `$grid-gutter-width` | N/A | Applied to `.row` |
| Container widths | N/A | `$container-max-widths` | `.container` breakpoint widths |
| Breakpoints | N/A | `$grid-breakpoints` | `.col-sm-*`, `.col-md-*`, etc. |
| Row columns | N/A | N/A | `.row-cols-*` utilities |
| Gutters (custom) | N/A | `$gutters` map | `.g-*`, `.gx-*`, `.gy-*` utilities |

### Pattern: Grid System Implementation

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

**HTML Usage Examples:**

Two-column layout using the 12-column grid:
```html
<div class="row">
  <div class="col-md-8">Main content</div>
  <div class="col-md-4">Sidebar</div>
</div>
```

Responsive card grid with `row-cols-*`:
```html
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col"><div class="card">...</div></div>
  <div class="col"><div class="card">...</div></div>
  <div class="col"><div class="card">...</div></div>
</div>
```

Independent horizontal and vertical gutters:
```html
<div class="row gx-5 gy-3">
  <div class="col-md-6">Content</div>
  <div class="col-md-6">Content</div>
</div>
```

### Common Mistakes

- **Changing column count from 12** - Most design systems work with 12 columns; changing breaks ecosystem
- **Not using responsive column classes** - Use `.col-sm-*`, `.col-md-*` for responsive layouts
- **Forgetting mobile-first approach** - Start with mobile (`.col-*`), then add breakpoint-specific classes
- **Not using gutter utilities** - Use `.g-*`, `.gx-*`, `.gy-*` utilities for custom spacing
- **Creating custom grid systems** - Bootstrap's grid is highly flexible; extend it rather than replace it

### See Also

- Bootstrap 5.3 Grid: [https://getbootstrap.com/docs/5.3/layout/grid/](https://getbootstrap.com/docs/5.3/layout/grid/)
- Bootstrap 5.3 Columns: [https://getbootstrap.com/docs/5.3/layout/columns/](https://getbootstrap.com/docs/5.3/layout/columns/)
- Bootstrap 5.3 Gutters: [https://getbootstrap.com/docs/5.3/layout/gutters/](https://getbootstrap.com/docs/5.3/layout/gutters/)

## See Also

- [Organisms → Layout + Components](organisms-layout-components.md)
- [SCSS Integration Order](scss-integration-order.md)
