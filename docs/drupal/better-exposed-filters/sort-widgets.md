---
description: BEF sort widgets — radio buttons, links, sort combine, combine_param, and rewrite syntax for sort labels
drupal_version: "11.x"
---

# Sort Widgets

## When to Use

> Use this guide when you have exposed sort criteria and want radio buttons or links instead of dropdowns, or want to combine sort_by and sort_order into a single control.

## Decision

| Plugin ID | Class | Title |
|---|---|---|
| `default` | `DefaultWidget` | Default (select dropdown) |
| `bef` | `RadioButtons` | Radio Buttons |
| `bef_links` | `Links` | Links |

All sort widgets are always applicable — `isApplicable()` returns TRUE for all filter types.

**Sort configuration:**

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Combine sort | `advanced.combine` | FALSE | Merge sort_by and sort_order into one element |
| Combine param | `advanced.combine_param` | 'sort_bef_combine' | Query parameter name for combined sort |
| Combine rewrite | `advanced.combine_rewrite` | '' | Rewrite combined option labels |
| Reset sort | `advanced.reset` | FALSE | Add a "Reset sort" option |
| Reset label | `advanced.reset_label` | '' | Label for the reset option |
| Collapsible | `advanced.collapsible` | FALSE | Wrap in collapsible details element |
| Is secondary | `advanced.is_secondary` | FALSE | Move to secondary options panel |

## Pattern

```
# Sort combine — before:
Sort by: [Title] [Date] [Author]
Order:   [Asc]   [Desc]

# Sort combine — after (single element):
[Title Asc] [Title Desc] [Date Asc] [Date Desc] [Author Asc] [Author Desc]
```

Combined key format: `{sort_by}_{sort_order}` (e.g., `title_ASC`). BEF unpacks it on submit.

**Combine rewrite format** — one per line, `current_label|new_label`:
```
Post date Asc|Oldest first
Post date Desc|Newest first
Title Asc|A → Z
Title Desc|Z → A
```

Leave replacement blank to remove an option. Options reorder to match rewrite order.

**Multiple BEF Views on same page:** Change `combine_param` from default `sort_bef_combine` to a unique value per View to prevent query parameter collisions.

## Common Mistakes

- **Wrong**: Enabling sort combine without exposed sort order → **Right**: "Allow people to choose the sort order" must be enabled in the View's exposed form settings.
- **Wrong**: Leaving reset label blank → **Right**: The reset label cannot be blank. Set a label like "Default sort" or "Reset".
- **Wrong**: Using default `sort_bef_combine` for multiple Views on the same page → **Right**: Change `combine_param` to a unique value per View.

## See Also

- [Secondary & Collapsible Options](secondary-collapsible.md)
- [Option Rewriting & Sorting](option-rewriting-sorting.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/sort/`
