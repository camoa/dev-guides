---
description: BEF option rewriting and sorting — label find/replace syntax, rewrite by key, sort methods, and helper class reference
tldr: "Use option rewriting when you need to change display labels of filter options or remove options. Use option sorting when you need alphabetical or key-based ordering instead of the default Views order."
drupal_version: "11.x"
---

# Option Rewriting & Sorting

## When to Use

> Use option rewriting when you need to change display labels of filter options or remove options. Use option sorting when you need alphabetical or key-based ordering instead of the default Views order.

## Decision

**Option rewriting** — available for all filters except ungrouped `StringFilter` and `NumericFilter`:

| Config | Key | Default |
|---|---|---|
| Rewrite values | `advanced.rewrite.filter_rewrite_values` | '' |
| Rewrite by key | `advanced.rewrite.filter_rewrite_values_key` | FALSE |

Format (one per line): `current_text|replacement_text`

Leave replacement blank to remove the option.

**Option sorting:**

| Config Key | Default | Options |
|---|---|---|
| `advanced.sort_options` | FALSE | Enable custom sorting |
| `advanced.sort_options_method` | 'alphabetical_asc' | 'alphabetical_asc', 'alphabetical_desc', 'key_asc', 'key_desc', 'result_count' |
| `advanced.sort_options_natural` | TRUE | Natural sort algorithm |

**Sorting is NOT available** for entity reference filters (taxonomy terms, users, content references) — these come pre-sorted from entity queries and `isFieldSortingSupported()` excludes them.

## Pattern

```
# Rewrite by label
On|Yes
Off|No
Published|Live

# Remove an option (blank replacement)
Archived|

# Rewrite by key (set filter_rewrite_values_key = TRUE)
1|Active
0|Inactive
```

**Helper methods (`BetterExposedFiltersHelper`):**

| Method | Purpose |
|---|---|
| `rewriteOptions()` | Apply label rewrites |
| `sortOptionsCustom()` | Enhanced sort with method/direction |
| `sortOptionsAlphabetical()` | Alphabetical with direction control |
| `sortNestedOptions()` | Sort hierarchical options by level |

**"- Any -" preservation:** BEF always keeps the "- Any -" option at position 0 regardless of sort order, removing it before sorting and re-adding it after.

**For hierarchical taxonomy:** Do NOT include leading hyphens in the current text — BEF strips them before matching.

## Common Mistakes

- **Wrong**: Rewrite string not matching because of trailing spaces or capitalization → **Right**: The match is exact. Copy the option text directly from the rendered filter.
- **Wrong**: Attempting custom sorting on taxonomy or user reference filters → **Right**: Entity reference options are excluded from custom sorting (`isFieldSortingSupported()` returns FALSE). Hierarchy would break.
- **Wrong**: Expecting rewrite order to determine display order when sort is also enabled → **Right**: When `sort_options` is enabled, sort overrides rewrite order.

## See Also

- [Sort Widgets](sort-widgets.md)
- [Hooks & Alter Functions](hooks-alter.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/BetterExposedFiltersHelper.php`
