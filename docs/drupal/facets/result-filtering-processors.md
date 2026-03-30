---
description: Facets result filtering processors — count_limit, hide_non_narrowing, hide_active_items, exclude_specified_items, dependent_processor
drupal_version: "11.x"
---

# Result Filtering Processors

## When to Use

> Use this guide when you need to control which facet items are displayed — hiding items with low counts, removing specific values, or showing only narrowing results.

## Decision

| ID | Title | Stage:Weight | Purpose |
|---|---|---|---|
| `count_limit` | Count limit | build:50 | Hide items below/above a count threshold |
| `hide_non_narrowing_result_processor` | Hide non-narrowing results | build:40 | Only show items that would actually filter results |
| `hide_1_result_facet` | Hide facet with 1 result | build:50 | Hide entire facet if only 1 option exists |
| `hide_active_items_processor` | Hide active items | build:25 | Don't show already-selected items in the list |
| `exclude_specified_items` | Exclude specified items | build:50 | Remove specific items by raw value or display text |
| `dependent_processor` | Dependent facet | build:5 | Show facet only when another facet has active selection |
| `combine_processor` | Combine facets | build:5 | Merge results from multiple facets into one display |

## Pattern

**`count_limit` configuration:**

| Setting | Purpose |
|---|---|
| Minimum items | Don't show items with fewer than N results |
| Maximum items | Don't show items with more than N results |

Example: `minimum_items: 2` hides any facet option that would only return 1 result.

**`hide_non_narrowing_result_processor`** — Essential for good UX. Without it, facets show options that wouldn't change the result set (100% of results match that option). With it, only meaningful filter options appear.

**`dependent_processor` configuration:**

| Setting | Purpose |
|---|---|
| Facet | Which facet must be active |
| Negate | Show this facet when the other is NOT active |

Use case: Show "Sub-category" facet only when "Category" has an active selection.

**`exclude_specified_items` configuration:**

| Setting | Purpose |
|---|---|
| Exclude items | List of values to exclude (one per line) |
| Regex | Use regex matching |
| Use display value | Match against display text instead of raw value |

## Common Mistakes

- **Wrong**: Using display text in `exclude_specified_items` when `translate_entity` runs after it → **Right**: If `translate_entity` runs at weight 5 and `exclude_specified_items` at weight 50, you can use display text. If you reorder them, you must use raw values.
- **Wrong**: Expecting `hide_non_narrowing_result_processor` to work identically with OR and AND → **Right**: With OR operator, non-narrowing detection works differently. An item that matches all current results may still be meaningful for OR.

## See Also

- [Processing Pipeline](processing-pipeline.md) — execution order
- [Sort Processors](sort-processors.md) — ordering the remaining items
- Reference: `web/modules/contrib/facets/src/Plugin/facets/processor/`
