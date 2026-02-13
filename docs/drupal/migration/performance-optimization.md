---
description: Memory management and batch processing for large-scale migrations
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

Large migrations (10,000+ nodes) require memory management, batch processing, and query optimization. Monitor PHP memory, database connections, and migration speed.

## Decision

| Performance issue | Solution | Configuration |
|---|---|---|
| PHP memory exhaustion | Increase memory limit, use batching | php.ini memory_limit = 512M |
| Slow migration speed | Disable non-essential modules | Drush migrate with --feedback |
| Database connection timeouts | Increase wait_timeout | MySQL configuration |
| Duplicate processing | Use highwater mark | source: track_changes: true |
| Large image processing | Migrate files first, reference | Separate file migration |

## Pattern

**Batch processing configuration:**

```yaml
# Migration with batch limits
source:
  plugin: d7_node
  node_type: article
  batch_size: 50  # Process 50 items per batch
  track_changes: true  # Use highwater mark for incremental
  highwater_property:
    name: changed
    alias: n

# Drush execution with feedback
drush migrate:import d7_node_article --limit=1000 --feedback=100
# Processes 1000 items, shows progress every 100
```

**Memory optimization:**

```php
// Custom source plugin - yield rows instead of loading all
public function prepareRow(Row $row) {
  // Unset large fields not needed
  $row->setSourceProperty('large_unused_field', NULL);

  // Process external data in batches
  if ($row->getSourceProperty('nid') % 100 == 0) {
    // Periodic cleanup
    drupal_static_reset();
  }

  return parent::prepareRow($row);
}
```

**Reference**: `/core/modules/migrate/src/Plugin/migrate/source/SqlBase.php` for batch processing

## Common Mistakes

- **Wrong**: Not using batch processing → **Right**: Memory exhaustion on large datasets
- **Wrong**: Migrating all content at once → **Right**: Incremental migration enables testing, rollback
- **Wrong**: Not monitoring memory usage → **Right**: drush migrate:status shows progress, not memory
- **Wrong**: Keeping all modules enabled → **Right**: Disable Search API, other heavy modules during migration
- **Wrong**: Not using database indexes → **Right**: Add temporary indexes on D7 source for faster queries

## See Also

- Reference: [Drupal 11 performance enhancements](https://metadesignsolutions.com/migrating-to-drupal-11-a-strategic-roadmap-for-enterprise-security-and-performance/)
