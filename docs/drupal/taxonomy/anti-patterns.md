---
description: "Identify and fix problematic taxonomy implementation patterns"
tldr: "Use this guide when reviewing taxonomy implementations to identify and fix problematic patterns."
drupal_version: "11.x"
---

# Anti-Patterns & Common Mistakes

## When to Use

> Use this guide when reviewing taxonomy implementations to identify and fix problematic patterns.

## Decision

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|--------------|------------------|
| **Using taxonomy as content type** | Terms lack field flexibility, revision control, view modes that content types provide | Use content type with entity reference when you need >3 fields or rich content |
| **Creating terms programmatically on every request** | Database writes on every page load; orphaned terms pile up | Create terms during content save; use auto_create in field config, not custom code |
| **Loading entire term tree on every page** | Memory bloat, slow page loads, especially with >1k terms | Cache term tree; load on-demand; use entity query with parent filter for subtrees |
| **Deep hierarchies (>5 levels)** | Unusable UI, poor performance, cognitive overload | Flatten to 2-3 levels max; consider entity reference to another content type for complex relationships |
| **Vocabulary per content type** | Prevents cross-content categorization, creates taxonomy sprawl | Use shared vocabularies; restrict with field handler_settings if needed |
| **Not restricting target_bundles in fields** | Widget shows terms from ALL vocabularies, confusing users | Always set target_bundles to specific vocabulary in field config |
| **Calling loadTree() with load_entities = TRUE on large vocabs** | Out-of-memory errors, timeouts | Use load_entities = FALSE, load specific entities afterward: `$term_storage->loadMultiple($tids)` |
| **Deleting terms without checking references** | Broken entity references, "missing term" in displays | Query for term usage in entity reference fields first; unpublish instead of delete if used |
| **Auto-creating terms without validation** | Spam, typos, duplicates ("Drupal", "drupal", "Drupla") | Implement hook_taxonomy_term_presave() to validate name, merge duplicates |
| **Using 'administer taxonomy' for content editors** | Allows vocabulary deletion, structure changes | Use per-vocabulary permissions: `edit terms in VOCAB` |
| **Hierarchical taxonomy for simple tags** | Unnecessary complexity, parent UI clutter | Use flat vocabulary for tag-style categorization |
| **Multiple vocabularies instead of hierarchy** | "Product Categories", "Product Subcategories" as separate vocabs | Use single hierarchical vocabulary with parent-child terms |

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
  'field_sku' => 'WID-001',
  'field_category' => ['target_id' => $category_term_id], // Reference taxonomy term
  // ... unlimited fields
]);
```

## Common Mistakes

- **Not caching loadTree() results** → Every call queries database, joins parent table, sorts by weight. Cache in static variable or cache bin; invalidate on term save
- **Using taxonomy_index table for non-node entities** → taxonomy_index only tracks nodes. For custom entities, query entity reference fields directly or build custom index
- **Assuming term order is stable** → Terms sort by weight then name by default, but loadMultiple() doesn't guarantee order. Always sort explicitly if order matters
- **Creating vocabulary in update hook without checking existence** → Re-running update hook fails. Use `\Drupal::entityTypeManager()->getStorage('taxonomy_vocabulary')->load($vid)` to check first
- **Not handling term deletion in field references** → Orphaned references show as "- Restricted access -" or cause errors. Implement hook_taxonomy_term_delete() to clean up or prevent deletion
- **Using fixed term IDs in code** → Term IDs vary across environments. Reference by name or use config entities to map names to IDs

## See Also

- ← Previous: [Best Practices & Patterns](best-practices.md) | Next: [Security & Performance](security-performance.md) →
- Reference: [Wishdesk: Architectural Patterns That Scale Complex Drupal Taxonomies](https://wishdesk.com/blog/7-game-changing-architectural-patterns-that-scale-complex-drupal-taxonomies-without-killing-performance)
