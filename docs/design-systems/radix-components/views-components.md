---
description: "Components for displaying Views output with various formatters (grid, table, unformatted lists)"
tldr: "Components for displaying Views output with various formatters (grid, table, unformatted lists). These components are automatically used when Radix preprocesses Views templates, but can also be included manually for custom Views styling."
---

# Views Components

## When to Use

> Components for displaying Views output with various formatters (grid, table, unformatted lists). These components are automatically used when Radix preprocesses Views templates, but can also be included manually for custom Views styling.

## Items

### views-view
**Description:** Implementation for main view component.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `content` | string |  | **Dead — not honoured by `views-view.twig`.** The template never outputs `content`; rows come from `rows` and `empty`. |
| `views_attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `views-view.twig`.** Line 33 overwrites it with `attributes ?: create_attribute()`. Pass `attributes` instead. The other `views_*_attributes` props below all use `X ?: create_attribute()` and *are* honoured. |
| `views_title_attributes` | Drupal\Core\Template\Attribute |  | Views title attributes |
| `views_header_attributes` | Drupal\Core\Template\Attribute |  | Views header attributes |
| `views_filters_attributes` | Drupal\Core\Template\Attribute |  | Views filters attributes |
| `views_rows_attributes` | Drupal\Core\Template\Attribute |  | Views rows attributes |
| `views_empty_attributes` | Drupal\Core\Template\Attribute |  | Views empty attributes |
| `views_footer_attributes` | Drupal\Core\Template\Attribute |  | Views footer attributes |
| `views_attachment_before_attributes` | Drupal\Core\Template\Attribute |  | Views attachment before attributes |
| `views_attachment_after_attributes` | Drupal\Core\Template\Attribute |  | Views attachment after attributes |
| `views_pager_attributes` | Drupal\Core\Template\Attribute |  | Views pager attributes |
| `views_more_attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `views-view.twig`.** Line 43 accepts it, but the `views_more` block at line 189 renders the link with `more|add_class(views_more_classes)` and never prints these attributes. Use `views_more_utility_classes` for classes. |
| `views_feed_icons_attributes` | Drupal\Core\Template\Attribute |  | Views feed icons attributes |
| `view_view_utility_classes` | array | [] | Utility classes for the outer `.view` wrapper (`views-view.twig:54`). Note the singular `view_view_` prefix, not `views_view_`. Absent from the YAML. |
| `views_title_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_header_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_filters_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_rows_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_empty_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_footer_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_attachment_before_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_attachment_after_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_pager_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_more_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |
| `views_feed_icons_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes. |

**Slots:**
| Slot | Description |
|------|-------------|
| `views_view_wrapper` | The wrapper for the view. |
| `views_view_title` | The title for the view. |
| `views_header` | The header for the view. |
| `views_filters` | The filters for the view. |
| `views_attachment_before` | The attachment before the view. |
| `views_rows` | The rows for the view. |
| `views_pager` | The pager for the view. |
| `views_attachment_after` | The attachment after the view. |
| `views_more` | The more link for the view. |
| `views_footer` | The footer for the view. |
| `views_feed_icons` | The feed icons for the view. |

**Usage Example:**
```twig
{%
  include 'radix:views-view' with {
    title: title,
    header: header,
    rows: rows,
    empty: empty,
    pager: pager,
    views_title_utility_classes: ['h2', 'mb-4'],
    views_rows_utility_classes: ['row', 'g-4'],
    views_pager_utility_classes: ['mt-5']
  }
%}
```

**Gotchas:**
- Each section (title, header, filters, rows, etc.) has separate `*_attributes` and `*_utility_classes` props
- The `content` prop is declared in the YAML but `views-view.twig` never prints it — it is dead in both directions. Row output comes from `rows` (or `empty` when there are none)
- Use preprocess functions to modify `*_utility_classes` arrays for views-wide styling patterns

### views-view--grid
**Description:** Component implementation for views to display rows in a grid.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `content` | string |  | **Dead — not honoured by `views-view--grid.twig`.** The template never prints a top-level `content`; it iterates `items` and prints `row.content` / `column.content`. |
| `attributes` | Drupal\Core\Template\Attribute |  | Honoured — `views-view--grid.twig:47` calls `attributes.addClass(classes)` on the grid wrapper. |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:views-view--grid' with {
    title: title,
    items: items,
    options: options,
    view_view__grid_utility_classes: ['row', 'row-cols-1', 'row-cols-md-3', 'g-4']
  }
%}
```

**Gotchas:**
- The grid renders from `items`, not `rows` — `views-view--grid.twig:49,59` iterates `items` and nothing reads `rows`. `items` is undeclared in the YAML but is the variable the template needs
- Grid alignment (`horizontal` vs `vertical`) is controlled by Views settings, not component props
- Don't confuse this with Bootstrap's CSS grid; this uses Views' own grid structure

### views-view--table
**Description:** Schema for a view implementation that displays data in a table.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | string |  | Title for this group of rows. |
| `header` | array |  | An array for table header columns. |
| `caption` | string |  | Caption for this table. |
| `rows` | array |  | Table row data. |
| `responsive` | boolean |  | Adds the `.responsive-enabled` class only (`views-view--table.twig:36`). It does **not** control the `.table-responsive` wrapper. |
| `sticky` | boolean |  | Adds `.sticky-header` and suppresses the `.table-responsive` wrapper (`views-view--table.twig:37,43`). |
| `header_style` | string |  | `light` or `dark`; adds `.table-light` / `.table-dark` to the `<thead>` (`views-view--table.twig:63`). Absent from the YAML. |
| `bordered` | boolean |  | Flag whether the table header is styled bordered. |
| `accessibility_description` | string |  | **Dead.** The template reads `description`, not this prop (`views-view--table.twig:54`). |
| `accessibility_summary` | string |  | **Dead.** The template reads `summary`, not this prop (`views-view--table.twig:51`). |
| `caption_needed` | boolean |  | Flag to determine if the caption tag is required. |
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the table element. |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:views-view--table' with {
    title: 'Content Overview',
    header: header,
    rows: rows,
    responsive: true,
    sticky: false,
    bordered: true,
    caption: 'List of all published articles',
    views_view__table_utility_classes: ['table-striped', 'table-hover']
  }
%}
```

**Gotchas:**
- The `.table-responsive` wrapper is emitted whenever `sticky` is falsy (`views-view--table.twig:43`), not by `responsive`. `responsive: true` only adds a `.responsive-enabled` class; `sticky: true` is what removes the scroll wrapper
- The `header` and `rows` arrays are complex structures with nested `attributes` and `content` keys
- `bordered` defaults to true in the template itself (`bordered ?? true`, `views-view--table.twig:39`); pass `bordered: false` to drop `.table-bordered`

### views-view--unformatted
**Description:** Component implementation to display a view of unformatted rows.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `content` | string |  | **Dead — not honoured by `views-view--unformatted.twig`.** The template never prints a top-level `content`; it iterates `rows` and prints `row.content`. |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:views-view--unformatted' with {
    title: 'Recent Posts',
    rows: rows,
    row_utility_classes: ['col-12', 'col-md-6', 'col-lg-4', 'mb-4'],
    default_row_class: false
  }
%}
```

**Gotchas:**
- The `row_utility_classes` applies classes to EVERY row wrapper, making it easy to create Bootstrap grid layouts
- Setting `default_row_class: false` removes Drupal's default `views-row` class
- Each row in the `rows` array has its own `attributes` object that can be manipulated in preprocess

## Common Mistakes
- **Forgetting Views variables are auto-populated**: Variables like `header`, `rows`, `footer`, and `pager` come from Views and shouldn't be manually constructed in template includes
- **Mixing up component-level vs row-level classes**: `views_rows_utility_classes` applies to the rows container wrapper, while `row_utility_classes` (in unformatted views) applies to individual row items
- **Assuming `responsive` creates the scroll wrapper**: it does not. `.table-responsive` is emitted whenever `sticky` is falsy, so leave `sticky` off for wide tables
- **Overriding grid structure manually**: The views-view--grid component expects Views-generated grid data structure; don't try to reconstruct it manually

## See Also
- Pagination Component for views pager styling
- Table Component for standalone table structures
- Card Component for common views row display patterns
- List Group Component for alternative unformatted list styling
