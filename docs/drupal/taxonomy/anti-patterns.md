---
description: Identify and fix problematic taxonomy implementation patterns
drupal_version: "11.x"
---

# Anti-Patterns & Common Mistakes

## When to Use

> Use this guide when reviewing taxonomy implementations to identify and fix problematic patterns.

## Decision

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|--------------|------------------|
| **Using taxonomy as content type** | Terms lack field flexibility, revision control, view modes | Use content type with entity reference when you need >3 fields or rich content |
| **Creating terms programmatically on every request** | Database writes on every page load; orphaned terms | Create terms during content save; use auto_create in field config |
| **Loading entire term tree on every page** | Memory bloat, slow page loads | Cache term tree; load on-demand |
| **Deep hierarchies (>5 levels)** | Unusable UI, poor performance | Flatten to 2-3 levels max |
| **Vocabulary per content type** | Prevents cross-content categorization | Use shared vocabularies |
| **Not restricting target_bundles in fields** | Widget shows terms from ALL vocabularies | Always set target_bundles to specific vocabulary |
| **Calling loadTree() with load_entities = TRUE on large vocabs** | Out-of-memory errors, timeouts | Use load_entities = FALSE, load specific entities afterward |
| **Deleting terms without checking references** | Broken entity references | Query for term usage first; unpublish instead of delete if used |
| **Auto-creating terms without validation** | Spam, typos, duplicates | Implement hook_taxonomy_term_presave() to validate |
| **Using 'administer taxonomy' for content editors** | Allows vocabulary deletion, structure changes | Use per-vocabulary permissions |

## Pattern

**Anti-pattern: Loading all terms in widget**
```php
// BAD: Loads all terms, slow with large vocabularies
$terms = $term_storage->loadByProperties(['vid' => 'tags']);
foreach ($terms as $term) {
  $options[$term->id()] = $term->getName();
}
```

**Better: Use autocomplete widget**
```yaml
# Field form display config
type: entity_reference_autocomplete
# Loads terms via AJAX, no page load penalty
```

**Anti-pattern: Term as pseudo-content**
```php
// BAD: Trying to add multiple fields to term
$term = Term::create([
  'vid' => 'products',
  'name' => 'Widget Pro',
  'field_price' => 99.99,
  'field_sku' => 'WID-001',
  'field_description' => 'Long description...',
  'field_images' => [...],
]);
```

**Better: Use content type**
```php
// GOOD: Content type for rich content
$node = Node::create([
  'type' => 'product',
  'title' => 'Widget Pro',
  'field_price' => 99.99,
  'field_category' => ['target_id' => $category_term_id], // Reference taxonomy term
]);
```

## Common Mistakes

- **Wrong**: Not caching loadTree() results → **Right**: Cache in static variable or cache bin; invalidate on term save
- **Wrong**: Using taxonomy_index table for non-node entities → **Right**: taxonomy_index only tracks nodes; query entity reference fields directly for custom entities
- **Wrong**: Assuming term order is stable → **Right**: Always sort explicitly if order matters
- **Wrong**: Creating vocabulary in update hook without checking existence → **Right**: Check if vocabulary exists first
- **Wrong**: Not handling term deletion in field references → **Right**: Implement hook_taxonomy_term_delete() to clean up
- **Wrong**: Using fixed term IDs in code → **Right**: Reference by name or use config entities to map names to IDs

## See Also

- [Best Practices & Patterns](best-practices.md)
- [Security & Performance](security-performance.md)
- Reference: [Wishdesk: Architectural Patterns That Scale Complex Drupal Taxonomies](https://wishdesk.com/blog/7-game-changing-architectural-patterns-that-scale-complex-drupal-taxonomies-without-killing-performance)
