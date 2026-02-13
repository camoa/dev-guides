---
description: Entity query API for efficient database queries with access control
drupal_version: "11.x"
---

# Entity Query Patterns

## When to Use

When querying entities by field values, properties, or relationships, requiring performant database queries with access control and cache invalidation.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Load by field value | Entity query with condition() | Efficient database query, access check |
| Load by property | Query on entity keys | Base table query, no field table joins |
| Complex conditions | conditionAggregate(), orConditionGroup() | AND/OR logic, aggregates |
| Sort by field | sort() | Database-level sorting |
| Count results | count()->execute() | Get count without loading entities |
| Bypass access control | accessCheck(FALSE) | Admin operations only |

## Pattern

Basic entity query:

```php
// Inject entity_type.manager service
$query = $this->entityTypeManager->getStorage('node')->getQuery()
  ->accessCheck(TRUE)  // ALWAYS explicit
  ->condition('type', 'article')
  ->condition('status', 1)
  ->condition('field_tags.entity.name', 'Drupal', 'CONTAINS')
  ->sort('created', 'DESC')
  ->range(0, 10);

$nids = $query->execute();
$nodes = $this->entityTypeManager->getStorage('node')->loadMultiple($nids);
```

Complex query with OR conditions:

```php
$query = $this->entityTypeManager->getStorage('node')->getQuery()
  ->accessCheck(TRUE);

$orGroup = $query->orConditionGroup()
  ->condition('field_category', 'Technology')
  ->condition('field_tags.entity.name', 'Tech', 'CONTAINS');

$query->condition($orGroup)
  ->condition('status', 1)
  ->sort('field_priority', 'DESC')
  ->sort('created', 'DESC');

$nids = $query->execute();
```

Count query:

```php
$count = $this->entityTypeManager->getStorage('node')->getQuery()
  ->accessCheck(TRUE)
  ->condition('type', 'article')
  ->condition('status', 1)
  ->count()
  ->execute();
```

Reference: `/core/lib/Drupal/Core/Entity/Query/QueryInterface.php`

## Common Mistakes

- **Wrong**: Forgetting accessCheck() → **Right**: Exception in Drupal 10+; MUST be explicit (TRUE or FALSE)
- **Wrong**: Using accessCheck(FALSE) without justification → **Right**: Security issue; bypasses access control
- **Wrong**: Loading entities when only IDs needed → **Right**: Performance waste; use count() or return IDs only
- **Wrong**: Querying in loops (N+1 problem) → **Right**: Use single query with IN condition instead
- **Wrong**: Not using range() for large result sets → **Right**: Load thousands of entities; memory exhaustion
- **Wrong**: Sorting by computed fields → **Right**: Not in database; sort after loading or denormalize

**Security**:
- ALWAYS use accessCheck(TRUE) unless you have explicit reason to bypass.
- accessCheck(FALSE) is for admin operations, cron, batch processes only.
- Document WHY when using accessCheck(FALSE). It's a security smell.
- Entity query respects hook_query_TAG_alter(). Be aware of query alterations.

**Performance**:
- Use count()->execute() instead of loading entities when only count needed.
- range() limits results at database level. Use for pagination.
- Sorting by fields requires joins. Sort by base properties (created, changed) when possible.
- Entity reference queries (field_ref.entity.name) create joins. Limit when possible.
- Cache query results using cache API. Invalidate on entity save/delete.

**Performance improvements** (Drupal 10.5/11.2):
- Fixed performance regression for sites with large revision counts
- Optimized latest revision calculation for entity queries
- See: https://www.md-systems.ch/en/blog/2025-12-16/performance-improvements-drupal-11-3

**Development Standards**:
- Inject entity_type.manager service, don't use \Drupal::entityTypeManager()
- Always call accessCheck() explicitly (required in Drupal 10+)
- Use storage methods, not Entity::load() static calls
- Add @todo comment for accessCheck(FALSE) with justification

## See Also

- [Computed Field Patterns](computed-field-patterns.md)
- [Field Access Control](field-access-control.md)
- Reference: [Entity query API](https://www.drupal.org/docs/drupal-apis/entity-api/working-with-the-entity-api)
