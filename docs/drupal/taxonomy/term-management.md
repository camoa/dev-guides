---
description: "Create, edit, or bulk-manage taxonomy terms via UI, Drush, or code"
tldr: "Use UI for manual term creation. Use Drush or code for bulk operations or programmatic term management."
drupal_version: "11.x"
---

# Term Management

## When to Use

> Use this guide when creating, editing, or bulk-managing taxonomy terms.

## Steps

**Via UI:**

1. Navigate to `/admin/structure/taxonomy`
2. Click vocabulary name to manage terms
3. Click "Add term" or edit existing term
4. Fill fields: Name (required), Description, Parent (for hierarchy), Weight
5. Save

**Via Drush:**

```bash
# Create term
drush php:eval '$term = \Drupal\taxonomy\Entity\Term::create(["vid" => "tags", "name" => "Drupal"]); $term->save();'

# Delete term
drush php:eval '\Drupal::entityTypeManager()->getStorage("taxonomy_term")->load(123)->delete();'

# Export terms (requires contrib)
drush migrate:import --tag=term_export
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

- Creating terms in wrong vocabulary → Always verify `vid` matches intended vocabulary. Misplaced terms cause broken references and confusing UI
- Not setting parent field correctly → Parent must be array: `['parent' => [0]]` for root, `['parent' => [$tid]]` for child. Omitting defaults to root
- Using `save()` in loops without batch API → Causes memory issues and timeouts with large datasets. Use Batch API or queue workers for >100 terms
- Forgetting to set description format → Description field is text_long with format. Must specify: `['value' => '...', 'format' => 'basic_html']`
- Deleting vocabulary without handling orphaned term references → Vocabulary deletion cascades to terms but not field values. Orphaned references cause errors

## See Also

- ← Previous: [Hierarchical Taxonomy](hierarchical-taxonomy.md) | Next: [Taxonomy Views Integration](taxonomy-views.md) →
- Reference: `/core/modules/taxonomy/src/Entity/Term.php` (lines 148-227)
