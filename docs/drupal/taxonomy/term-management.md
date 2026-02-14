---
description: Create, edit, or bulk-manage taxonomy terms via UI, Drush, or code
drupal_version: "11.x"
---

# Term Management

## When to Use

> Use UI for manual term creation. Use Drush or code for bulk operations or programmatic term management.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Manual term creation (< 20 terms) | UI at `/admin/structure/taxonomy` | Simple, visual, no code needed |
| One-off term operations | Drush php:eval | Quick command-line access |
| Bulk operations (> 100 terms) | Batch API or queue workers | Prevents timeouts and memory issues |
| Hierarchical term creation | Programmatic with parent field | Set parent array for child terms |

## Pattern

**Via UI:**
1. Navigate to `/admin/structure/taxonomy`
2. Click vocabulary name
3. Click "Add term"
4. Fill fields: Name (required), Description, Parent, Weight
5. Save

**Via Drush:**
```bash
# Create term
drush php:eval '$term = \Drupal\taxonomy\Entity\Term::create(["vid" => "tags", "name" => "Drupal"]); $term->save();'

# Delete term
drush php:eval '\Drupal::entityTypeManager()->getStorage("taxonomy_term")->load(123)->delete();'
```

**Programmatic creation:**
```php
use Drupal\taxonomy\Entity\Term;

$term = Term::create([
  'vid' => 'tags',
  'name' => 'Drupal 11',
  'description' => [
    'value' => 'Articles about Drupal 11',
    'format' => 'basic_html',
  ],
  'weight' => 10,
  'parent' => [0], // 0 = root, or array of parent tids
]);
$term->save();
```

**Bulk operations:**
```php
// Create multiple terms
$terms_data = ['PHP', 'JavaScript', 'CSS', 'HTML'];
foreach ($terms_data as $name) {
  Term::create(['vid' => 'technologies', 'name' => $name])->save();
}

// Update existing terms
$term_storage = \Drupal::entityTypeManager()->getStorage('taxonomy_term');
$terms = $term_storage->loadByProperties(['vid' => 'tags']);
foreach ($terms as $term) {
  $term->setWeight(0)->save();
}
```

## Common Mistakes

- **Wrong**: Creating terms in wrong vocabulary → **Right**: Always verify `vid` matches intended vocabulary
- **Wrong**: Not setting parent field correctly → **Right**: Parent must be array: `['parent' => [0]]` for root, `['parent' => [$tid]]` for child
- **Wrong**: Using `save()` in loops without batch API → **Right**: Use Batch API or queue workers for >100 terms
- **Wrong**: Forgetting to set description format → **Right**: Must specify: `['value' => '...', 'format' => 'basic_html']`
- **Wrong**: Deleting vocabulary without handling orphaned term references → **Right**: Orphaned references cause errors; clean up first

## See Also

- [Hierarchical Taxonomy](hierarchical-taxonomy.md)
- [Taxonomy Views Integration](taxonomy-views.md)
- Reference: `/core/modules/taxonomy/src/Entity/Term.php` (lines 148-227)
