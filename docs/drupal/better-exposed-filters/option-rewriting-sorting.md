---
description: "BEF option rewriting and sorting — label find/replace syntax, rewrite by key, sort methods, and helper class reference"
tldr: "Use option rewriting to change display labels of filter options, remove options, or control the order of options; use option sorting for alphabetical, by-key, or natural sort order."
drupal_version: "11.x"
---

# Option Rewriting & Sorting

## When to Use

> When you need to change the display labels of filter options, remove options, or control the order of options.

## Decision: Option Rewriting

Available for all filters except StringFilter and NumericFilter (unless grouped).

**Config key:** `advanced.rewrite.filter_rewrite_values`

**Format:** One replacement per line, `current_text|replacement_text`:
```
On|Yes
Off|No
Published|Live
Unpublished|Draft
```

Leave replacement blank to remove an option:
```
Archived|
```

**Rewrite by key:** Set `advanced.rewrite.filter_rewrite_values_key` to TRUE to match by option key instead of display text:
```
1|Active
0|Inactive
```

For hierarchical taxonomy filters, do NOT include leading hyphens in the current text — BEF strips them before matching.

## Decision: Option Sorting

**Config keys:**
| Key | Default | Options |
|---|---|---|
| `advanced.sort_options` | FALSE | Enable custom sorting |
| `advanced.sort_options_method` | 'alphabetical_asc' | 'alphabetical_asc', 'alphabetical_desc', 'key_asc', 'key_desc', 'result_count' |
| `advanced.sort_options_natural` | TRUE | Use natural sort algorithm (e.g., "Item 2" before "Item 10") |

**Limitation:** Custom sorting is NOT available for entity reference filters (taxonomy terms, users, content references). These are excluded in `FilterWidgetBase::isFieldSortingSupported()`.

Supported filter types:
- `InOperator` (list fields, boolean)
- `BooleanOperator`
- `StringFilter` with in/or/and/not operators
- Grouped filters

## Pattern: Helper Methods

`BetterExposedFiltersHelper` provides the sorting/rewriting logic:

| Method | Purpose |
|---|---|
| `rewriteOptions($options, $rewrite_settings, $reorder, $rewrite_by_key)` | Apply label rewrites |
| `flattenOptions($options, $preserve_keys)` | Convert mixed option formats to simple scalars |
| `sortOptions($options)` | Alphabetical sort with transliteration |
| `sortOptionsCustom($options, $method, $direction, $natural)` | Enhanced sort with method/direction |
| `sortOptionsByKey($options, $direction)` | Sort by option key |
| `sortOptionsAlphabetical($options, $direction, $natural)` | Alphabetical with direction control |
| `sortNestedOptions($options, $delimiter)` | Sort hierarchical options by level |

## Pattern: "- Any -" Preservation

BEF preserves the "- Any -" (or "All") option at the top of the list regardless of sort order. The `processCustomSortedOptions()` method detects and removes it before sorting, then re-adds it at position 0.

## Common Mistakes

- **Rewrite not matching** — Check for trailing spaces, capitalization differences. The match is exact.
- **Sorting disabled for taxonomy filters** — This is intentional. Entity reference options come pre-sorted from the entity query. Custom sorting would break hierarchical display.
- **Rewrite + sort interaction** — When both are active and `sort_options` is disabled, rewrite order determines display order. When `sort_options` is enabled, sort overrides rewrite order.

## See Also

- [Sort Widgets](sort-widgets.md) — sort combine rewrite
- [Hooks & Alter Functions](hooks-alter.md) — programmatic option manipulation
- Reference: `web/modules/contrib/better_exposed_filters/src/BetterExposedFiltersHelper.php`
