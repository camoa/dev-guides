---
description: Create, update, or delete terms via code (migrations, imports, install hooks)
drupal_version: "11.x"
---

# Programmatic Term Operations

## When to Use

> Use programmatic approach for migrations, imports, install hooks, drush commands. Complements config-first vocabulary management.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Single term creation | `Term::create()` + `save()` | Simple, direct |
| Update existing term | Load, modify, `save()` | Standard entity pattern |
| Delete term | `load()` + `delete()` or `delete($terms)` | Single or bulk delete |
| Bulk creation (>100 terms) | Batch API or queue workers | Prevents timeouts and memory issues |
| Hierarchical term creation | Set `parent` field array | `['parent' => [$parent_tid]]` |

## Pattern

**Create single term:**
```php
use Drupal\taxonomy\Entity\Term;

$term = Term::create([
  'vid' => 'tags',
  'name' => 'Drupal 11',
  'description' => [
    'value' => 'Posts about Drupal 11',
    'format' => 'basic_html',
  ],
  'weight' => 0,
  'parent' => [0], // Root level
]);
$term->save();
$tid = $term->id();
```

**Update existing term:**
```php
$term_storage = \Drupal::entityTypeManager()->getStorage('taxonomy_term');
$term = $term_storage->load($tid);

$term->setName('Updated Name');
$term->setDescription('New description');
$term->setWeight(10);
$term->save();
```

**Delete term:**
```php
$term = $term_storage->load($tid);
$term->delete();

// Or bulk delete
$terms = $term_storage->loadMultiple($tids);
$term_storage->delete($terms);
```

**Hierarchy manipulation:**
```php
// Add child term
$parent = $term_storage->load($parent_tid);
$child = Term::create([
  'vid' => 'categories',
  'name' => 'Child Category',
  'parent' => [$parent->id()],
]);
$child->save();

// Add multiple parents
$term = $term_storage->load($tid);
$term->set('parent', [$parent1_tid, $parent2_tid]);
$term->save();

// Move term to different parent
$term = $term_storage->load($tid);
$term->set('parent', [$new_parent_tid]);
$term->save();
```

## Common Mistakes

- **Wrong**: Not setting `parent` field → **Right**: Always set `'parent' => [0]` for top-level or `[$parent_tid]` for children
- **Wrong**: Using `create()` in loops without batching → **Right**: Use Batch API or queue workers for >100 terms
- **Wrong**: Forgetting description format → **Right**: Description is formatted text: `['value' => '...', 'format' => 'basic_html']`
- **Wrong**: Saving terms without checking duplicates → **Right**: Use `loadByProperties(['vid' => $vid, 'name' => $name])` first
- **Wrong**: Deleting parent term without handling children → **Right**: Load and re-parent or delete children explicitly
- **Wrong**: Not validating vocabulary exists → **Right**: Check vocabulary entity exists before creating terms
- **Wrong**: Calling `save()` unnecessarily → **Right**: Every save triggers hooks, cache clear, search indexing; only save when changing data

## See Also

- [Term Storage & Querying](term-storage-querying.md)
- [Taxonomy with Entity Reference](entity-reference-taxonomy.md)
- Reference: `/core/modules/taxonomy/src/Entity/Term.php` (lines 137-143)
