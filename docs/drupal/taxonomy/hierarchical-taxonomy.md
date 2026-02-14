---
description: Decide between flat or hierarchical taxonomy structures
drupal_version: "11.x"
---

# Hierarchical Taxonomy

## When to Use

> Use flat taxonomy for simple tagging (blog tags, keywords). Use hierarchical taxonomy for categorization with subcategories (Geography: Country > State > City).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple tagging (blog tags, keywords) | Flat taxonomy | Simpler UI, better performance, no hierarchy overhead |
| Categorization with subcategories (Geography: Country > State > City) | Hierarchical taxonomy | Native parent-child support, depth-aware queries |
| Faceted filtering with drill-down | Hierarchical taxonomy | Users navigate from broad to specific (e.g., Electronics > Computers > Laptops) |
| Very large vocabularies (>10k terms) | Flat taxonomy or limited depth hierarchy | `loadTree()` with deep hierarchies causes performance issues |
| Multiple inheritance (term has multiple parents) | Hierarchical taxonomy with multiple parents | Cardinality on parent field supports multiple parents |

## Pattern

**Flat taxonomy** — Terms have no parent (default):
```yaml
# Vocabulary config (same as hierarchical)
vid: tags
```

**Hierarchical taxonomy** — Set parent on term creation:
```php
use Drupal\taxonomy\Entity\Term;

// Parent term
$parent = Term::create([
  'vid' => 'categories',
  'name' => 'Electronics',
]);
$parent->save();

// Child term
$child = Term::create([
  'vid' => 'categories',
  'name' => 'Computers',
  'parent' => [$parent->id()],
]);
$child->save();
```

**Query hierarchy:**
```php
$term_storage = \Drupal::entityTypeManager()->getStorage('taxonomy_term');

// Load all children of a term
$children = $term_storage->loadChildren($parent_tid);

// Load all parents of a term
$parents = $term_storage->loadParents($child_tid);

// Load entire tree (use sparingly)
$tree = $term_storage->loadTree($vid, $parent = 0, $max_depth = NULL, $load_entities = FALSE);
```

## Common Mistakes

- **Wrong**: Using deep hierarchies (>5 levels) → **Right**: Keep hierarchies shallow (2-3 levels max) or use alternative like entity reference to another content type
- **Wrong**: Calling `loadTree()` with `load_entities = TRUE` on large vocabularies → **Right**: Use `load_entities = FALSE` and load selectively
- **Wrong**: Building hierarchies when flat would work → **Right**: If you don't need parent-child relationships for navigation or logic, keep it flat
- **Wrong**: Ignoring MECE principle → **Right**: Terms at same level should be Mutually Exclusive and Collectively Exhaustive

## See Also

- [Term Reference Field Configuration](term-reference-config.md)
- [Term Management](term-management.md)
- Reference: `/core/modules/taxonomy/src/TermStorage.php` (lines 184-303)
- Reference: [Evolvingweb.com Organizing Content With Taxonomies](https://evolvingweb.com/blog/how-organize-your-drupal-content-taxonomies)
