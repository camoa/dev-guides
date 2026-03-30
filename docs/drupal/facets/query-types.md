---
description: Facets query types — search_api_string, search_api_date, search_api_range, search_api_granular, and how they execute
drupal_version: "11.x"
---

# Query Types

## When to Use

> Use this guide when you need to understand how facet selections are translated into search backend queries, or when facets are not filtering correctly for a field type.

## Decision

| ID | Class | Data Types | Query Syntax |
|---|---|---|---|
| `search_api_string` | SearchApiString | text, keyword, entity reference | Exact match conditions |
| `search_api_date` | SearchApiDate | date, timestamp | Date range conditions |
| `search_api_range` | SearchApiRange | integer, decimal | Numeric range conditions |
| `search_api_granular` | SearchApiGranular | integer | Grouped numeric ranges |

**Field type to query type mapping:**

| Field Type | Query Type |
|---|---|
| string, fulltext, entity reference | `search_api_string` |
| date | `search_api_date` |
| integer, decimal, float | `search_api_string` (or `search_api_range` with range widget) |

Query types are auto-detected based on the Search API field type. Manual override is rarely needed.

## Pattern

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

## Common Mistakes

- **Wrong**: Expecting exact-match filtering on numeric fields with the default query type → **Right**: Numeric fields default to `search_api_string` (exact match). For range filtering, you need `search_api_range` combined with the `facets_range_widget` sub-module.

## See Also

- [Processing Pipeline](processing-pipeline.md) — query types in the pipeline
- [Range Slider Widget](range-slider.md) — using range query types
- Reference: `web/modules/contrib/facets/src/Plugin/facets/query_type/`
