---
description: "BEF sort widgets — radio buttons, links, sort combine, combine_param, and rewrite syntax for sort labels"
tldr: "Use this guide when you have exposed sort criteria and want to render them as radio buttons or links instead of dropdowns, or want to combine sort_by and sort_order into a single control."
drupal_version: "11.x"
---

# Sort Widgets

## When to Use

> When you have exposed sort criteria and want to render them as radio buttons or links instead of dropdowns, or want to combine sort_by and sort_order into a single control.

## Decision: Available Sort Widgets

| Plugin ID | Class | Title |
|---|---|---|
| `default` | `DefaultWidget` | Default (select dropdown) |
| `bef` | `RadioButtons` | Radio Buttons |
| `bef_links` | `Links` | Links |

All sort widgets are always applicable (`isApplicable()` returns TRUE).

## Decision: Sort Configuration

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Combine sort | `advanced.combine` | FALSE | Merge sort_by and sort_order into one element |
| Combine param | `advanced.combine_param` | 'sort_bef_combine' | Query parameter name for combined sort |
| Combine rewrite | `advanced.combine_rewrite` | '' | Rewrite combined option labels |
| Reset sort | `advanced.reset` | FALSE | Add a "Reset sort" option |
| Reset label | `advanced.reset_label` | '' | Label for the reset option |
| Collapsible | `advanced.collapsible` | FALSE | Wrap in collapsible details element |
| Collapsible label | `advanced.collapsible_label` | 'Sort options' | Details element title |
| Is secondary | `advanced.is_secondary` | FALSE | Move to secondary options panel |

## Pattern: Sort Combine

When `combine` is TRUE, BEF merges `sort_by` and `sort_order` into a single select/radio/links element:

```
# Before combine:
Sort by: [Title] [Date] [Author]
Order:   [Asc]   [Desc]

# After combine (single element):
[Title Asc] [Title Desc] [Date Asc] [Date Desc] [Author Asc] [Author Desc]
```

The combined key format is `{sort_by}_{sort_order}` (e.g., `title_ASC`). On submit, `sortCombineSubmitForm()` unpacks it back to separate `sort_by` and `sort_order` values.

## Pattern: Combine Rewrite

Rewrite combined labels for user-friendly display:
```
Post date Asc|Oldest first
Post date Desc|Newest first
Title Asc|A → Z
Title Desc|Z → A
```

Leave replacement blank to remove an option. Options reorder to match rewrite order.

## Pattern: Multiple BEF Instances

When multiple Views with BEF are on the same page, the `combine_param` prevents query parameter collisions. Change from default `sort_bef_combine` to something unique per View.

## Common Mistakes

- **Combine doesn't work** — "Allow people to choose the sort order" must be enabled in the View's exposed form settings. Without exposed sort order, there's nothing to combine.
- **Reset sort not appearing** — The reset label cannot be blank. Set a label like "Default sort" or "Reset".
- **Collapsible label blank** — If the collapsible label is empty, there's no way to show/hide the sort options. Always provide a label.

## See Also

- [Secondary & Collapsible Options](secondary-collapsible.md) — moving sorts to secondary panel
- [Option Rewriting & Sorting](option-rewriting-sorting.md) — rewrite syntax details
