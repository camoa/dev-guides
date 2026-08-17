---
description: "The facets processing pipeline from query alteration through PRE_QUERY, POST_QUERY, BUILD, and SORT stages"
tldr: "Use this guide when you need to understand how facets process data from query to rendering, or when debugging unexpected facet behavior. Processor order and locked processors (url_processor_handler, hierarchy_processor) matter."
drupal_version: "11.x"
---

# Processing Pipeline

## When to Use

> When you need to understand how facets process data from query to rendering, or when debugging unexpected facet behavior.

## Decision

| Stage | Interface | When | Purpose | Example Processors |
|---|---|---|---|---|
| **PRE_QUERY** | `PreQueryProcessorInterface` | Before search executes | Parse URL, modify query | `url_processor_handler` |
| **POST_QUERY** | `PostQueryProcessorInterface` | After backend returns results | Transform raw values | `replace` |
| **BUILD** | `BuildProcessorInterface` | Before rendering | Filter, limit, transform for display | `translate_entity`, `count_limit`, `hierarchy_processor` |
| **SORT** | `SortProcessorInterface` | During build | Order results | `count_widget_order`, `display_value_widget_order` |

## Pattern

Execution flow:

```
1. alterQuery($query, $facet_source_id)
   └── Each facet: PRE_QUERY processors (url_processor_handler extracts active items)
   └── Each facet: Query Type builds search conditions

2. [Search API backend executes query, returns raw facet counts]

3. processFacets($facet_source_id)
   └── Each facet: Query Type builds Result objects from raw data
   └── Each facet: POST_QUERY processors (replace values, etc.)

4. build($facet)
   └── BUILD processors in weight order:
       - translate_entity (weight 5) → convert IDs to labels
       - url_processor_handler (weight 15) → build URLs
       - hide_active_items (weight 25) → remove selected items
       - boolean_item (weight 35) → format booleans
       - count_limit (weight 50) → enforce min/max counts
       - hierarchy_processor (weight 100) → nest into tree
   └── SORT processors:
       - active_widget_order (weight 20) → active items first
       - count_widget_order (weight 30) → by result count
       - display_value_widget_order (weight 40) → alphabetical
   └── Widget.build() → render array
```

FacetManager service:

```php
$facet_manager = \Drupal::service('facets.manager');

// Step 1: Alter the search query
$facet_manager->alterQuery($query, $facet_source_id);

// Step 2: Process results after query
$facet_manager->processFacets($facet_source_id);

// Step 3: Build renderable for a specific facet
$build = $facet_manager->build($facet);
```

Each processor has a weight per stage — lower weights execute first. Default weights are defined in the processor annotation/attribute and can be reordered in the facet configuration UI.

## Common Mistakes

- **Wrong**: Assuming processor order doesn't matter → **Right**: If `translate_entity` runs after `exclude_specified_items`, you must use raw values (IDs) in the exclude list, not labels.
- **Wrong**: Trying to disable `url_processor_handler` or `hierarchy_processor` → **Right**: These are locked processors — essential to facet functionality, cannot be disabled.
- **Wrong**: Expecting all processors to always be available → **Right**: Some processors have `supportsFacet()` checks. Hierarchy processors, for example, only appear when `use_hierarchy` is enabled.

## See Also

- [Value Transformation Processors](value-transformation-processors.md) — BUILD stage transformations
- [Result Filtering Processors](result-filtering-processors.md) — BUILD stage filtering
- [Sort Processors](sort-processors.md) — SORT stage ordering
- Reference: `src/FacetManager/DefaultFacetManager.php`
