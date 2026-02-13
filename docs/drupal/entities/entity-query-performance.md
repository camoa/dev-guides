---
description: Entity query optimization for large datasets and high-traffic scenarios
drupal_version: "11.x"
---

# Entity Query Performance

## When to Use

When optimizing entity queries for large datasets, high-traffic scenarios, or complex filtering requirements, requiring careful query construction and caching.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Paginated results | range() | Limit database load and memory |
| Count-only query | count()->execute() | Avoid entity loading overhead |
| Field-based filtering | Indexed field columns | Fast WHERE clauses |
| Large result sets | Batch API or queue | Avoid memory exhaustion |
| Repeated queries | Cache API | Avoid redundant database queries |

## Pattern

Optimized query with caching:

```php
use Drupal\Core\Cache\CacheBackendInterface;

public function getArticleIds($category, $page = 0) {
  $cid = "my_module:articles:$category:$page";

  // Check cache first
  if ($cache = $this->cache->get($cid)) {
    return $cache->data;
  }

  // Build efficient query
  $query = $this->entityTypeManager->getStorage('node')->getQuery()
    ->accessCheck(TRUE)
    ->condition('type', 'article')
    ->condition('status', 1)
    ->condition('field_category', $category)
    ->sort('created', 'DESC')
    ->range($page * 20, 20);  // Pagination

  $nids = $query->execute();

  // Cache for 1 hour, invalidate on node list changes
  $this->cache->set($cid, $nids, time() + 3600, ['node_list']);

  return $nids;
}
```

Batch processing for large datasets:

```php
public function processManyNodes() {
  $batch = [
    'operations' => [],
    'finished' => [$this, 'batchFinished'],
  ];

  // Query in chunks
  $query = $this->entityTypeManager->getStorage('node')->getQuery()
    ->accessCheck(FALSE)  // Batch process, admin operation
    ->condition('type', 'article');

  $nids = $query->execute();

  // Process in batches of 50
  foreach (array_chunk($nids, 50) as $chunk) {
    $batch['operations'][] = [[$this, 'processBatch'], [$chunk]];
  }

  batch_set($batch);
}

public function processBatch($nids, &$context) {
  $nodes = $this->entityTypeManager->getStorage('node')->loadMultiple($nids);
  foreach ($nodes as $node) {
    // Process node
  }
}
```

Reference: `/core/lib/Drupal/Core/Entity/Query/Sql/Query.php`

## Common Mistakes

- **Wrong**: Loading full entities when only field values needed → **Right**: Use query, not loadMultiple()
- **Wrong**: Not using range() on large datasets → **Right**: Load thousands of entities; memory exhaustion
- **Wrong**: Querying in loops → **Right**: N+1 problem; query once with IN condition
- **Wrong**: Not caching repeated queries → **Right**: Redundant database hits
- **Wrong**: Missing cache tags → **Right**: Stale cache after entity changes
- **Wrong**: Sorting by unindexed fields → **Right**: Slow queries on large tables
- **Wrong**: Using OR conditions unnecessarily → **Right**: Creates complex joins; refactor if possible

**Performance Best Practices**:

**Query Construction**:
- Use range() for pagination. Limit results at database level.
- Query base properties (status, type, created) instead of fields when possible.
- Minimize field conditions. Each field condition adds a JOIN.
- Use IN condition instead of OR for same-field matching.

**Indexing**:
- Add indexes to field storage for commonly filtered/sorted fields.
- Index definition: `indexes: {value: [value]}` in field.storage.*.yml
- Database indexes essential for large tables (>10k rows).

**Caching**:
- Cache query results with appropriate cache tags.
- Use 'node_list', 'user_list', etc. tags for entity lists.
- Invalidate cache on entity CRUD via cache tag invalidation.
- Cache count() results separately from full queries.

**Loading Optimization**:
- Load entities only when needed. IDs often sufficient.
- Use loadMultiple() once instead of load() in loop.
- Use entity view builder for rendering; it handles caching.

**Recent Performance Improvements** (Drupal 10.5/11.2):
- Fixed regression affecting sites with large revision counts
- Optimized latest revision calculation (Content Moderation, JSON:API)
- Entity reference improvements save hundreds of queries on complex pages
- See: https://www.drupal.org/project/drupal/releases/11.2.6

**Thresholds**:
- < 100 results: Direct loading acceptable
- 100-1000 results: Use range() pagination
- > 1000 results: Use Batch API or Queue API
- Repeated queries (>3 times/request): Cache results

## See Also

- [Field Access Control](field-access-control.md)
- [Field Validation Patterns](field-validation-patterns.md)
- Reference: [Performance improvements in Drupal 11.3](https://www.md-systems.ch/en/blog/2025-12-16/performance-improvements-drupal-11-3)
