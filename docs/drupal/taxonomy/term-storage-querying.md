---
description: Query taxonomy terms programmatically with TermStorage methods
drupal_version: "11.x"
---

# Term Storage & Querying

## When to Use

> Use TermStorage specialized methods for hierarchy operations. Use entity queries for standard term lookups.

## Decision

| Situation | Use Method | Why |
|-----------|-----------|-----|
| Load entire term tree | `loadTree($vid, 0, NULL, FALSE)` | Gets all terms with hierarchy info; use `load_entities = FALSE` for performance |
| Load only top-level terms | `loadTree($vid, 0, 1)` | Limits depth to 1 level |
| Load direct parents | `loadParents($tid)` | Returns parent Term entities |
| Load all ancestors | `loadAllParents($tid)` | Returns all ancestor entities including term itself |
| Load direct children | `loadChildren($tid)` | Returns child Term entities |
| Check hierarchy type | `getVocabularyHierarchyType($vid)` | Returns DISABLED/SINGLE/MULTIPLE constant |
| Query by name or properties | Entity query | Standard approach for filtering terms |

## Pattern

**loadTree() — Load term tree:**
```php
$term_storage = \Drupal::entityTypeManager()->getStorage('taxonomy_term');

// Load flat list (depth info included)
$tree = $term_storage->loadTree('categories');

// Load only top-level terms
$top_level = $term_storage->loadTree('categories', 0, 1);

// NEVER do this with large vocabularies (>1000 terms):
// $tree_entities = $term_storage->loadTree('categories', 0, NULL, TRUE);
```

**loadParents() — Load direct parents:**
```php
$parents = $term_storage->loadParents($tid);
foreach ($parents as $parent) {
  echo $parent->getName();
}
```

**loadChildren() — Load direct children:**
```php
$children = $term_storage->loadChildren($parent_tid);
foreach ($children as $child) {
  echo $child->getName();
}
```

**Entity query approach:**
```php
$query = \Drupal::entityQuery('taxonomy_term')
  ->accessCheck(TRUE)
  ->condition('vid', 'tags')
  ->condition('name', 'Drupal%', 'LIKE')
  ->sort('weight')
  ->sort('name');

$tids = $query->execute();
$terms = $term_storage->loadMultiple($tids);
```

**Query with parent condition:**
```php
// Find all top-level terms
$query = \Drupal::entityQuery('taxonomy_term')
  ->accessCheck(TRUE)
  ->condition('vid', 'categories')
  ->condition('parent.target_id', 0);
$top_level_tids = $query->execute();
```

## Common Mistakes

- **Wrong**: Using `loadTree($vid, 0, NULL, TRUE)` on large vocabularies → **Right**: Use `load_entities = FALSE` and load specific entities afterward
- **Wrong**: Not caching loadTree results → **Right**: Load once, cache in static variable or state
- **Wrong**: Assuming loadParents includes root → **Right**: Root parent (tid 0) is excluded; empty array means top-level
- **Wrong**: Recursive loadChildren in loops → **Right**: Use loadTree for entire subtree instead (N+1 query problem)
- **Wrong**: Not checking access in entity queries → **Right**: Always use `->accessCheck(TRUE)` unless bypassing access explicitly
- **Wrong**: Forgetting to sort results → **Right**: loadMultiple doesn't sort; sort after loading if order matters

## See Also

- [Taxonomy Permissions & Access](taxonomy-permissions.md)
- [Programmatic Term Operations](programmatic-terms.md)
- Reference: `/core/modules/taxonomy/src/TermStorage.php`
- Reference: [Seth Shaw: Large Vocab loadTree Error](https://seth-shaw-unlv.github.io/2020-09-07/large_vocab_list_error)
