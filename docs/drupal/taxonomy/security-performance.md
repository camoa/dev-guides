---
description: Harden taxonomy against security vulnerabilities and optimize for scale
drupal_version: "11.x"
---

# Security & Performance

## When to Use

> Use this guide when hardening taxonomy implementations against security vulnerabilities and optimizing for large-scale performance.

## Decision

### Security

| Situation | Choose | Why |
|-----------|--------|-----|
| Vocabulary-level permissions | Per-vocabulary permissions (`edit terms in $vid`) | Granular control vs overly permissive `administer taxonomy` |
| Term view access | Ensure users have `access content` permission | Terms require published status AND `access content` |
| Auto-create validation | Implement `hook_taxonomy_term_presave()` | Prevent spam/XSS in auto-created terms |
| Custom output | Use `Html::escape($term->getName())` | Prevent XSS attacks |
| CSRF protection | Use Form API | Automatic CSRF token inclusion |

### Performance

| Term Count | Performance Impact | Mitigation |
|------------|-------------------|------------|
| <100 | Negligible | Use default approaches |
| 100-1,000 | loadTree() slows; dropdown widgets lag | Cache trees; use autocomplete widgets |
| 1,000-10,000 | loadTree() with load_entities causes memory issues | Use load_entities = FALSE; paginate admin UI |
| >10,000 | Admin UI fails; exposed filters timeout | Disable overview form; use Search API/Solr for faceting |

## Pattern

**Access control:**
```php
// GOOD: Granular per-vocabulary permissions
$account->hasPermission("edit terms in $vid");

// BAD: Overly permissive
$account->hasPermission('administer taxonomy');
```

**XSS prevention:**
```php
// ALWAYS sanitize term names in custom output
$safe_name = Html::escape($term->getName());

// Twig auto-escapes
{{ term.name }} {# Safe #}
{{ term.name|raw }} {# Dangerous unless sanitized #}
```

**Auto-create validation:**
```php
// Prevent spam/XSS in auto-created terms
function mymodule_taxonomy_term_presave(Term $term) {
  if ($term->isNew()) {
    $name = $term->getName();
    // Enforce max length
    if (strlen($name) > 50) {
      $term->setName(substr($name, 0, 50));
    }
    // Strip HTML tags
    $term->setName(strip_tags($name));
    // Normalize whitespace
    $term->setName(preg_replace('/\s+/', ' ', trim($name)));
  }
}
```

**N+1 query problem:**
```php
// BAD: N+1 queries
foreach ($nodes as $node) {
  $terms = $node->get('field_tags')->referencedEntities();
}

// GOOD: Preload all referenced terms
$tids = [];
foreach ($nodes as $node) {
  foreach ($node->get('field_tags') as $item) {
    $tids[] = $item->target_id;
  }
}
$terms = $term_storage->loadMultiple(array_unique($tids));
```

**loadTree() optimization:**
```php
// BAD: Out-of-memory with 10k+ terms
$tree = $term_storage->loadTree($vid, 0, NULL, TRUE);

// GOOD: Load lightweight objects, cherry-pick entities
$tree = $term_storage->loadTree($vid, 0, NULL, FALSE);
$tids_to_load = array_slice(array_column($tree, 'tid'), 0, 100);
$terms = $term_storage->loadMultiple($tids_to_load);
```

**Caching term trees:**
```php
// Cache tree for 1 hour
$cid = "taxonomy_tree:$vid";
$cache = \Drupal::cache()->get($cid);

if ($cache) {
  $tree = $cache->data;
} else {
  $tree = $term_storage->loadTree($vid);
  \Drupal::cache()->set($cid, $tree, time() + 3600, ["taxonomy_term_list:$vid"]);
}
```

**Large vocabulary strategies:**
- Disable term overview page: `hook_entity_operation_alter()` to remove "List terms" link
- Use autocomplete everywhere: never render full term list
- Consider hierarchical facets in Search API instead of Views exposed filters
- Partition large vocabularies: "US States", "Canadian Provinces" instead of "All Regions"

## Common Mistakes

- **Wrong**: Trusting user input in auto-created terms → **Right**: Always validate and sanitize in presave hook
- **Wrong**: Not setting cache tags on term-dependent data → **Right**: Use `['taxonomy_term:' . $tid]` cache tag
- **Wrong**: Exposing term overview form for large vocabularies → **Right**: Restrict access or provide filtered views
- **Wrong**: Using taxonomy_index for non-nodes → **Right**: Use entity reference queries or build custom index table
- **Wrong**: Not invalidating term tree cache → **Right**: Use cache tag `taxonomy_term_list:$vid`
- **Wrong**: Granting 'administer taxonomy' to untrusted roles → **Right**: Use per-vocabulary permissions

## See Also

- [Anti-Patterns & Common Mistakes](anti-patterns.md)
- [Code Reference Map](code-reference-map.md)
- Reference: [Drupal.org Issue: DB caching for loadTree()](https://www.drupal.org/project/drupal/issues/106015)
- Reference: [Seth Shaw: Large Vocab loadTree Error](https://seth-shaw-unlv.github.io/2020-09-07/large_vocab_list_error)
- Reference: [Drupal.org Permissions by Term module](https://www.drupal.org/project/permissions_by_term)
