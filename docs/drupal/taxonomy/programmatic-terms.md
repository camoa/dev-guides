---
description: "Create, update, or delete terms via code (migrations, imports, install hooks)"
tldr: "Use programmatic approach for migrations, imports, install hooks, drush commands. Complements config-first vocabulary management."
drupal_version: "11.x"
---

# Programmatic Term Operations

## When to Use

> Use this guide when creating, updating, or deleting terms via code (migrations, imports, install hooks, drush commands).

Programmatic approach complements config-first vocabulary management.

## Steps

**Create single term:**

1. **Use Term::create()** — Instantiate term entity
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
   ```

2. **Call save()** — Persist to database
   ```php
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

**Batch creation (>100 terms):**

```php
function mymodule_import_terms_batch($data) {
  $batch = [
    'title' => t('Importing terms'),
    'operations' => [],
    'finished' => 'mymodule_import_terms_finished',
  ];

  foreach ($data as $item) {
    $batch['operations'][] = [
      'mymodule_import_term_operation',
      [$item],
    ];
  }

  batch_set($batch);
}

function mymodule_import_term_operation($item, &$context) {
  Term::create([
    'vid' => 'categories',
    'name' => $item['name'],
    'parent' => [$item['parent_tid']],
  ])->save();

  $context['message'] = t('Imported @name', ['@name' => $item['name']]);
}
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

- Not setting `parent` field → Defaults to root (0), but explicit is better. Always set `'parent' => [0]` for top-level or `[$parent_tid]` for children
- Using `create()` in loops without batching → Causes timeouts and memory issues with >100 terms. Use Batch API or queue workers for bulk operations
- Forgetting description format → Description is formatted text: `['value' => '...', 'format' => 'basic_html']`. Omitting format causes default (plain_text)
- Saving terms without checking duplicates → Use `loadByProperties(['vid' => $vid, 'name' => $name])` to check for existing terms before creating
- Deleting parent term without handling children → Children become orphans or deleted (depending on config). Load and re-parent or delete children explicitly
- Not validating vocabulary exists → Loading non-existent vid fails silently. Check vocabulary entity exists before creating terms
- Calling `save()` unnecessarily in read-only operations → Every save triggers hooks, cache clear, search indexing. Only save when changing data

## See Also

- ← Previous: [Term Storage & Querying](term-storage-querying.md) | Next: [Taxonomy with Entity Reference](entity-reference-taxonomy.md) →
- Reference: `/core/modules/taxonomy/src/Entity/Term.php` (lines 137-143)
