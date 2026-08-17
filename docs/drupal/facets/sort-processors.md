---
description: "SORT-stage processors that order facet result items — active state, count, display value, raw value, taxonomy weight"
tldr: "Use this guide when you need to control the order of facet result items. Sort processors run in weight order and each breaks ties for the next; use term_weight_widget_order for manual ordering."
drupal_version: "11.x"
---

# Sort Processors

## When to Use

> When you need to control the order of facet result items.

## Decision

| ID | Title | Weight | Default Enabled | Direction Config |
|---|---|---|---|---|
| `active_widget_order` | Sort by active state | 20 | Yes | ASC = active first |
| `count_widget_order` | Sort by count | 30 | Yes | DESC = highest count first |
| `display_value_widget_order` | Sort by display value | 40 | Yes | ASC = alphabetical |
| `raw_value_widget_order` | Sort by raw value | 50 | No | ASC = lowest first |
| `term_weight_widget_order` | Sort by taxonomy weight | 60 | No | ASC = lightest first |

## Pattern

Processors execute in weight order. Each returns a comparison result (-1, 0, 1) for a pair of results; if a processor returns 0 (equal), the next processor in the chain breaks the tie.

**Default order (all enabled):**
1. Active items first (`active_widget_order`)
2. Then by count descending (`count_widget_order`)
3. Then alphabetically (`display_value_widget_order`)

`term_weight_widget_order` uses the taxonomy term's weight field, respecting manual ordering set in the taxonomy vocabulary UI — useful for a specific non-alphabetical order.

## Common Mistakes

- **Wrong**: Enabling both `count_widget_order` (DESC) and `display_value_widget_order` (ASC) and expecting one clear order → **Right**: The lower-weight processor wins for items with different counts; items with the same count fall through to the next sorter.
- **Wrong**: Expecting drag-and-drop manual ordering → **Right**: Facets doesn't support arbitrary manual ordering. Use `term_weight_widget_order` with taxonomy weights, or write a custom sort processor.

## See Also

- [Processing Pipeline](processing-pipeline.md) — sort stage in the pipeline
- [Hierarchy](hierarchy.md) — sorting within hierarchy levels
- Reference: `src/Plugin/facets/processor/`
