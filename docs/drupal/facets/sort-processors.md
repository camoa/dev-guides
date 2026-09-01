---
description: "SORT-stage processors that order facet result items — active state, count, display value, raw value, taxonomy weight"
tldr: "Use this guide when you need to control the order of facet result items. Sort processors run in weight order and each breaks ties for the next; use term_weight_widget_order for manual ordering."
drupal_version: "11.x"
---

# Sort Processors

## When to Use

> When you need to control the order of facet result items.

## Decision: Sort Processors

| ID | Title | Weight | Default Enabled | Direction Config |
|---|---|---|---|---|
| `active_widget_order` | Sort by active state | 20 | Yes | ASC = active first |
| `count_widget_order` | Sort by count | 30 | Yes | DESC = highest count first |
| `display_value_widget_order` | Sort by display value | 40 | Yes | ASC = alphabetical |
| `raw_value_widget_order` | Sort by raw value | 50 | No | ASC = lowest first |
| `term_weight_widget_order` | Sort by taxonomy weight | 60 | No | ASC = lightest first |

## Pattern: Sort Order

Processors execute in weight order. Each processor returns a comparison result (-1, 0, 1) for a pair of results. If a processor returns 0 (equal), the next processor in the chain breaks the tie.

**Default order (all enabled):**

1. Active items first (active_widget_order)
2. Then by count descending (count_widget_order)
3. Then alphabetically (display_value_widget_order)

## Pattern: term_weight_widget_order

Uses the taxonomy term's weight field for ordering. This respects the manual ordering set in the taxonomy vocabulary UI. Useful when you want a specific non-alphabetical order.

## Common Mistakes

- **Conflicting sort processors** — If you enable both `count_widget_order` (DESC) and `display_value_widget_order` (ASC), the one with lower weight wins for items with different counts. Items with the same count fall through to the next sorter.
- **Expecting drag-and-drop sort** — Facets doesn't support arbitrary manual ordering. Use `term_weight_widget_order` with taxonomy weights, or create a custom sort processor.

## See Also

- [Processing Pipeline](processing-pipeline.md) — sort stage in the pipeline
- [Hierarchy](hierarchy.md) — sorting within hierarchy levels
- Reference: `src/Plugin/facets/processor/`
