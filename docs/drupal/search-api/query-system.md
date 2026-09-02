---
description: Search API query system — programmatic queries, parse modes, condition groups, processing levels, and query tags
tldr: "Use this when building Search API queries programmatically or understanding how the query system works."
drupal_version: "11.x"
---

# Query System

## When to Use

> When building Search API queries programmatically or understanding how the query system works.

## Decision: Query Architecture

| Class | Purpose |
|---|---|
| `Query` | Main query object — keywords, conditions, sorts, options |
| `ConditionGroup` | Hierarchical AND/OR condition groups |
| `ResultSet` | Query results — items, count, warnings |
| `Result/Item` | Individual result item with fields and values |

## Pattern: Building Queries Programmatically

```php
$index = Index::load('my_index');
$query = $index->query();

// Set search keywords
$query->keys('drupal search api');

// Set parse mode
$query->setParseMode(\Drupal::service('plugin.manager.search_api.parse_mode')->createInstance('terms'));

// Add conditions
$query->addCondition('status', TRUE);
$query->addCondition('type', 'article');

// OR conditions
$or_group = $query->createConditionGroup('OR');
$or_group->addCondition('field_category', 'tutorials');
$or_group->addCondition('field_category', 'guides');
$query->addConditionGroup($or_group);

// Sorting
$query->sort('search_api_relevance', 'DESC');
$query->sort('created', 'DESC');

// Pagination
$query->range(0, 10); // offset, limit

// Execute
$results = $query->execute();
$total = $results->getResultCount();
foreach ($results->getResultItems() as $item) {
  $entity = $item->getOriginalObject()->getValue();
}
```

## Decision: Parse Modes

| Mode | ID | Behavior | Example Input → Query |
|---|---|---|---|
| **Terms** | `terms` | Multiple words, supports quotes and negation | `drupal "search api" -views` |
| **Phrase** | `phrase` | Entire input as exact phrase | `search api` → "search api" |
| **Direct** | `direct` | Pass directly to backend | Backend-specific syntax |
| **Complex** | `complex` | Keywords with AND/OR/NOT operators | `drupal AND (search OR find)` |

## Pattern: Processing Levels

| Level | Constant | Effect |
|---|---|---|
| None | `PROCESSING_NONE` | No processor execution |
| Basic | `PROCESSING_BASIC` | Basic processing (no facets, highlighting) |
| Full | `PROCESSING_FULL` | All processors execute (default) |

## Pattern: Query Tags

Add tags to queries for conditional processing:
```php
$query->addTag('my_custom_tag');

// In a processor or event subscriber:
if ($query->hasTag('search_api_skip_processor_highlight')) {
  // Skip highlighting for this query
}
```

## See Also

- [Views Integration](views-integration.md) — Views builds queries automatically
- [Events System](events-system.md) — hooking into query execution
