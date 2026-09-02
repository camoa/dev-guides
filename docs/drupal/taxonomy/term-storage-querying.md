---
description: "Query taxonomy terms programmatically with TermStorage methods"
tldr: "Use TermStorage specialized methods for hierarchy operations. Use entity queries for standard term lookups."
drupal_version: "11.x"
---

# Term Storage & Querying

## When to Use

> Use this guide when querying taxonomy terms programmatically.

Taxonomy provides specialized storage methods for hierarchy operations beyond standard entity queries.

## TermStorage Methods

### loadTree()

**Description:** Load entire term tree for a vocabulary with hierarchy information

**Parameters:**
| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `$vid` | string | — | Vocabulary ID (required) |
| `$parent` | int | `0` | Parent term ID (0 = root, or specific parent) |
| `$max_depth` | int\|null | `NULL` | Maximum depth to load (NULL = unlimited) |
| `$load_entities` | bool | `FALSE` | Load full term entities vs stdClass objects |

**Returns:** Array of term objects with `depth` and `parents` properties

**Usage Example:**
```php
$term_storage = \Drupal::entityTypeManager()->getStorage('taxonomy_term');

// Load flat list (depth info included)
$tree = $term_storage->loadTree('categories');

// Load only top-level terms
$top_level = $term_storage->loadTree('categories', 0, 1);

// Load full entities (WARNING: memory intensive)
$tree_entities = $term_storage->loadTree('categories', 0, NULL, TRUE);
```

**Gotchas:**
- **CRITICAL:** `load_entities = TRUE` with large vocabularies (>1000 terms) causes out-of-memory errors. Always use `FALSE` for large sets and load entities selectively afterward
- Result is cached internally — repeated calls are cheap, but cache key includes all parameters
- Returns stdClass objects by default, not Term entities — access as `$term->tid`, `$term->name`, not entity methods

Reference: `/core/modules/taxonomy/src/TermStorage.php` (lines 208-303)

### loadParents()

**Description:** Load direct parent terms of a term

**Parameters:**
| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `$tid` | int | — | Term ID |

**Returns:** Array of parent Term entities keyed by tid (excludes root parent with id 0)

**Usage Example:**
```php
$parents = $term_storage->loadParents($tid);
foreach ($parents as $parent) {
  echo $parent->getName();
}
```

**Gotchas:**
- Does NOT return root parent (tid 0) — only actual term entities
- Empty array if term has no parents or is top-level
- Loads full entities — safe for small parent sets

Reference: `/core/modules/taxonomy/src/TermStorage.php` (lines 93-106)

### loadAllParents()

**Description:** Load all ancestor terms (parents, grandparents, etc.)

**Parameters:**
| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `$tid` | int | — | Term ID |

**Returns:** Array of all ancestor Term entities including the term itself, keyed by tid

**Usage Example:**
```php
$ancestors = $term_storage->loadAllParents($tid);
// Includes $tid itself as first element
```

**Gotchas:**
- Includes the original term in results — filter it out if needed
- Result is cached per term — efficient for repeated calls

Reference: `/core/modules/taxonomy/src/TermStorage.php` (lines 150-179)

### loadChildren()

**Description:** Load direct child terms of a term

**Parameters:**
| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `$tid` | int | — | Term ID |
| `$vid` | string\|null | `NULL` | (Deprecated, unused) |

**Returns:** Array of child Term entities keyed by tid

**Usage Example:**
```php
$children = $term_storage->loadChildren($parent_tid);
foreach ($children as $child) {
  echo $child->getName();
}
```

**Gotchas:**
- Only direct children, not all descendants — use recursive calls or loadTree for full subtree
- Uses entity query with access checks — unpublished terms excluded unless user is admin

Reference: `/core/modules/taxonomy/src/TermStorage.php` (lines 184-203)

### getVocabularyHierarchyType()

**Description:** Determine hierarchy type of vocabulary (disabled, single, multiple parents)

**Parameters:**
| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `$vid` | string | — | Vocabulary ID |

**Returns:** Integer constant:
- `VocabularyInterface::HIERARCHY_DISABLED` (0) — No hierarchy, all terms are root
- `VocabularyInterface::HIERARCHY_SINGLE` (1) — Single parent per term
- `VocabularyInterface::HIERARCHY_MULTIPLE` (2) — Multiple parents possible

**Usage Example:**
```php
$hierarchy_type = $term_storage->getVocabularyHierarchyType('categories');
if ($hierarchy_type === \Drupal\taxonomy\VocabularyInterface::HIERARCHY_DISABLED) {
  // Flat vocabulary, skip hierarchy UI
}
```

**Gotchas:**
- Calculated from data, not config — slow on first call for large vocabularies
- Result is cached — efficient for repeated checks

Reference: `/core/modules/taxonomy/src/TermStorage.php` (lines 398-430)

## Entity Query Approach

**Standard term query:**
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

- Using `loadTree($vid, 0, NULL, TRUE)` on large vocabularies → Out-of-memory errors. Use `load_entities = FALSE` and load specific entities afterward: `$tids = array_column($tree, 'tid'); $terms = $term_storage->loadMultiple($tids);`
- Not caching loadTree results → Even with internal cache, hitting storage in loops is expensive. Load once, cache in static variable or state
- Assuming loadParents includes root → Root parent (tid 0) is excluded. Check for empty array to determine top-level terms
- Recursive loadChildren in loops → N+1 query problem. Use loadTree for entire subtree instead
- Not checking access in entity queries → Always use `->accessCheck(TRUE)` unless bypassing access explicitly in admin context
- Forgetting to sort results → Entity queries and loadTree sort by weight then name, but loadMultiple doesn't. Sort after loading if order matters

## See Also

- ← Previous: [Taxonomy Permissions & Access](taxonomy-permissions.md) | Next: [Programmatic Term Operations](programmatic-terms.md) →
- Reference: `/core/modules/taxonomy/src/TermStorage.php`
- Reference: [Seth Shaw: Large Vocab loadTree Error](https://seth-shaw-unlv.github.io/2020-09-07/large_vocab_list_error)
