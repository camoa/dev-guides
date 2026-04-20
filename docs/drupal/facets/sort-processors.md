---
description: Facets sort processors — active_widget_order, count_widget_order, display_value_widget_order, raw_value_widget_order, term_weight_widget_order
tldr: "Use this guide when you need to control the order of facet result items."
drupal_version: "11.x"
---

# Sort Processors

## When to Use

> Use this guide when you need to control the order of facet result items.

## Decision

| ID | Title | Weight | Default Enabled | Direction Config |
|---|---|---|---|---|
| `active_widget_order` | Sort by active state | 20 | Yes | ASC = active first |
| `count_widget_order` | Sort by count | 30 | Yes | DESC = highest count first |
| `display_value_widget_order` | Sort by display value | 40 | Yes | ASC = alphabetical |
| `raw_value_widget_order` | Sort by raw value | 50 | No | ASC = lowest first |
| `term_weight_widget_order` | Sort by taxonomy weight | 60 | No | ASC = lightest first |

## Pattern

Processors execute in weight order. Each processor returns a comparison result (-1, 0, 1) for a pair of results. If a processor returns 0 (equal), the next processor in the chain breaks the tie.

**Default order (all three enabled):**
1. Active items first (`active_widget_order`)
2. Then by count descending (`count_widget_order`)
3. Then alphabetically (`display_value_widget_order`)

**`term_weight_widget_order`** — Uses the taxonomy term's weight field for ordering. Respects the manual ordering set in the taxonomy vocabulary UI. Use when you want a specific non-alphabetical order.

## Common Mistakes

- **Wrong**: Expecting a single sort to govern all items when counts differ → **Right**: Sort processors chain. Lower weight wins for items with different values; equal values fall through to the next sorter.
- **Wrong**: Trying to set arbitrary manual order via drag-and-drop → **Right**: Facets doesn't support manual ordering. Use `term_weight_widget_order` with taxonomy weights, or create a custom sort processor.

## See Also

- [Processing Pipeline](processing-pipeline.md) — sort stage in the pipeline
- [Hierarchy](hierarchy.md) — sorting within hierarchy levels
- Reference: `web/modules/contrib/facets/src/Plugin/facets/processor/`
