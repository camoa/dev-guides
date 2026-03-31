---
description: Search API query system — programmatic queries, parse modes, condition groups, processing levels, and query tags
drupal_version: "11.x"
---

# Query System

## When to Use

> Use this when building Search API queries programmatically or understanding how the query system works.

## Decision

| Parse Mode | ID | Behavior |
|---|---|---|
| **Terms** | `terms` | Multiple words, supports quotes and negation: `drupal "search api" -views` |
| **Phrase** | `phrase` | Entire input as exact phrase |
| **Direct** | `direct` | Pass directly to backend (backend-specific syntax) |
| **Complex** | `complex` | AND/OR/NOT operators: `drupal AND (search OR find)` |

## Pattern

```php
$index = Index::load('my_index');
$query = $index->query();

// Keywords and parse mode
$query->keys('drupal search api');

// Conditions
$query->addCondition('status', TRUE);
$query->addCondition('type', 'article');

// OR conditions
$or_group = $query->createConditionGroup('OR');
$or_group->addCondition('field_category', 'tutorials');
$or_group->addCondition('field_category', 'guides');
$query->addConditionGroup($or_group);

// Sort and paginate
$query->sort('search_api_relevance', 'DESC');
$query->range(0, 10); // offset, limit

// Execute
$results = $query->execute();
$total = $results->getResultCount();
foreach ($results->getResultItems() as $item) {
  $entity = $item->getOriginalObject()->getValue();
}
```

**Query tags** — add for conditional processing:
```php
$query->addTag('search_api_skip_processor_highlight');
```

**Processing levels:**

| Level | Constant | Effect |
|---|---|---|
| None | `PROCESSING_NONE` | No processor execution |
| Basic | `PROCESSING_BASIC` | Basic processing (no facets, highlighting) |
| Full | `PROCESSING_FULL` | All processors execute (default) |

## Common Mistakes

- **Wrong**: Building conditions on Fulltext fields for faceting → **Right**: Use String fields for conditions/facets. Fulltext fields are tokenized.
- **Wrong**: Forgetting to set relevance sort → **Right**: `$query->sort('search_api_relevance', 'DESC')` must be explicit.

## See Also

- [Views Integration](views-integration.md)
- [Events System](events-system.md)
- Reference: `web/modules/contrib/search_api/src/Query/Query.php`
