---
description: "Built-in query types that translate facet selections into Search API query conditions by field type"
tldr: "Use this guide when you need to understand how facet selections are translated into search backend queries, or when facets are not filtering correctly for a field type. Query type is auto-detected from the Search API field type."
drupal_version: "11.x"
---

# Query Types

## When to Use

> When you need to understand how facet selections are translated into search backend queries.

## Decision: Built-In Query Types

| ID | Class | Data Types | Query Syntax |
|---|---|---|---|
| `search_api_string` | SearchApiString | text, keyword, entity reference | Exact match conditions |
| `search_api_date` | SearchApiDate | date, timestamp | Date range conditions |
| `search_api_range` | SearchApiRange | integer, decimal | Numeric range conditions |
| `search_api_granular` | SearchApiGranular | integer | Grouped numeric ranges |

## Pattern: How Query Types Execute

```php
// 1. Set facet options on the Search API query
$options['search_api_facets'][$field] = [
  'field' => $field_identifier,
  'limit' => $hard_limit,
  'operator' => 'and' | 'or',
  'min_count' => $min_count,
  'missing' => $show_missing,
];

// 2. Add filter conditions for active items
$filter = $query->createConditionGroup($operator); // AND or OR
foreach ($active_items as $value) {
    $filter->addCondition($field, $value, $exclude ? '<>' : '=');
}
$query->addConditionGroup($filter);
```

## Pattern: Query Type Selection

Query types are auto-detected based on the Search API field type. You rarely need to override this:

| Field Type | Query Type |
|---|---|
| string, fulltext, entity reference | `search_api_string` |
| date | `search_api_date` |
| integer, decimal, float | `search_api_string` (or `search_api_range` with range widget) |

## Common Mistakes

- **Wrong query type for numeric fields** — Numeric fields default to `search_api_string` (exact match). For range filtering, you need `search_api_range` with the range widget sub-module.

## See Also

- [Processing Pipeline](processing-pipeline.md) — query types in the pipeline
- [Range Slider Widget](range-slider.md) — using range query types
- Reference: `src/Plugin/facets/query_type/`
