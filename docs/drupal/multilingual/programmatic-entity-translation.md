---
description: Drupal programmatic entity translation — addTranslation, getTranslation, hasTranslation API, translation metadata
---

# Programmatic Entity Translation

### When to Use
When creating or managing entity translations in code — migrations, import scripts, automated workflows, REST API endpoints.

### Decision: Translation Management Approach

| If you need... | Use... | Why |
|---|---|---|
| Add new translation to entity | `$entity->addTranslation($langcode, $values)` | Creates translation with initial values |
| Access existing translation | `$entity->getTranslation($langcode)` | Returns translation object |
| Check if translation exists | `$entity->hasTranslation($langcode)` | Boolean check before access |
| Remove translation | `$entity->removeTranslation($langcode)` | Deletes translation |
| Check if entity is translatable | `$entity->isTranslatable()` | Verify entity type supports translation |
| Get all translation languages | `$entity->getTranslationLanguages()` | Returns array of Language objects |

### Pattern: Creating Translation

```php
use Drupal\node\Entity\Node;

// Load source entity
$node = Node::load(1);

// Check if translation exists
if (!$node->hasTranslation('es')) {
  // Add Spanish translation
  $translation = $node->addTranslation('es', [
    'title' => 'Título en español',
    'body' => [
      'value' => '<p>Cuerpo del artículo en español.</p>',
      'format' => 'basic_html',
    ],
  ]);

  // Set translation metadata
  $translation->content_translation_source = 'en';
  $translation->content_translation_outdated = FALSE;

  // Save entity (saves all translations)
  $node->save();
}
```

**Explanation**:
- `addTranslation($langcode, $values)` — creates translation, returns translation object
- `$values` — associative array of field values (same structure as entity creation)
- Save source entity, not translation object
- Translation inherits non-translatable field values from source

### Pattern: Accessing Translation

```php
// Get Spanish translation
if ($node->hasTranslation('es')) {
  $spanish = $node->getTranslation('es');
  $title = $spanish->label();
  $body = $spanish->get('body')->value;
}

// Get current language translation (based on negotiation)
$current_language = \Drupal::languageManager()->getCurrentLanguage()->getId();
$translation = $node->getTranslation($current_language);

// Get all translations
$languages = $node->getTranslationLanguages();
foreach ($languages as $langcode => $language) {
  $translation = $node->getTranslation($langcode);
  echo $translation->label() . "\n";
}
```

### Pattern: Updating Translation

```php
// Load and get translation
$node = Node::load(1);
$spanish = $node->getTranslation('es');

// Update translatable fields
$spanish->set('title', 'Nuevo título');
$spanish->set('body', [
  'value' => '<p>Nuevo cuerpo.</p>',
  'format' => 'basic_html',
]);

// Set as outdated if source changed
$spanish->content_translation_outdated = TRUE;

// Save
$node->save();
```

### Pattern: Removing Translation

```php
$node = Node::load(1);

if ($node->hasTranslation('es')) {
  $node->removeTranslation('es');
  $node->save();
}
```

**Warning**: Removal is permanent. No undo unless you have database backups or revision history.

### Pattern: Translation Metadata

Content Translation adds metadata fields to track translation state:

```php
$translation = $node->getTranslation('es');

// Source language
$source = $translation->content_translation_source->value; // 'en'

// Outdated flag
$outdated = $translation->content_translation_outdated->value; // TRUE/FALSE

// Author of translation
$author = $translation->content_translation_uid->target_id;

// Translation created/changed timestamps
$created = $translation->content_translation_created->value;
$changed = $translation->content_translation_changed->value;

// Set metadata
$translation->content_translation_source = 'en';
$translation->content_translation_outdated = FALSE;
$translation->content_translation_uid = $current_user->id();
$node->save();
```

### Common Mistakes

- **Calling save() on translation object** → `$translation->save()` is wrong. Save the source entity: `$node->save()`. Translation is not separate entity
- **Not checking hasTranslation() before getTranslation()** → `getTranslation()` throws exception if translation doesn't exist. Always check first
- **Forgetting to save after addTranslation()** → Translation isn't persisted until you call `$entity->save()`
- **Changing non-translatable fields via translation** → Non-translatable fields share same value. Changing in Spanish translation changes in English too
- **Assuming addTranslation() prevents duplicates** → Calling `addTranslation('es')` twice throws exception. Check `hasTranslation()` first
- **Not setting translation metadata** → Missing `content_translation_source` breaks translation overview UI. Set metadata for UI consistency

### See Also
- → [Translating Content Entities](translating-content-entities.md) — UI workflow
- → [Field Translatability](field-translatability.md) — which fields translate
- → [Translation & Revisions](translation-revisions.md) — revision behavior
- Reference: `core/lib/Drupal/Core/Entity/ContentEntityBase.php` (addTranslation, getTranslation, hasTranslation methods)
- Reference: `core/modules/content_translation/src/ContentTranslationMetadataWrapper.php`
