---
description: Drupal language-aware queries — entity queries by language, Views language filters, known issues with latestRevision
---

# Language-Aware Queries

### When to Use
When querying entities by language — Views filters, entity queries, getting content in specific language.

### Decision: Query Approach

| If you need... | Use... | Why |
|---|---|---|
| Query entities in current language | Views language filter: "Current language" | Automatic, respects negotiation |
| Query entities in specific language | EntityQuery condition on langcode | Programmatic control |
| Query all translations | No langcode condition | Returns all regardless of language |
| Query default translation only | Condition on default_langcode = 1 | Excludes translations |
| Query untranslated content | Condition on langcode = default_langcode | Content without translations |

### Pattern: Entity Query with Language

**Query nodes in current language**:

```php
$current_language = \Drupal::languageManager()->getCurrentLanguage()->getId();

$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('status', 1)
  ->condition('langcode', $current_language)
  ->accessCheck(TRUE);

$nids = $query->execute();
$nodes = \Drupal\node\Entity\Node::loadMultiple($nids);
```

**Query nodes in specific language**:

```php
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('langcode', 'es')
  ->accessCheck(TRUE);

$nids = $query->execute();
```

**Query default translations only** (exclude translations):

```php
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('default_langcode', 1)
  ->accessCheck(TRUE);
```

**Load entity in specific language after query**:

```php
$node = \Drupal\node\Entity\Node::load($nid);
if ($node->hasTranslation('es')) {
  $spanish_node = $node->getTranslation('es');
}
```

### Pattern: Views Language Filters

**Via UI** (`/admin/structure/views/view/VIEW_NAME`):
- Add filter → "Content: Translation language"
- Options:
  - Current user's language
  - Interface language (selected for page)
  - Original language (default translation)
  - Specific language (en, es, fr, etc.)

**Via config YAML** (`views.view.VIEW_NAME.yml`):

```yaml
display:
  default:
    display_options:
      filters:
        langcode:
          id: langcode
          table: node_field_data
          field: langcode
          relationship: none
          operator: in
          value:
            '***LANGUAGE_interface***': '***LANGUAGE_interface***'
          expose:
            operator_id: ''
            label: ''
            identifier: langcode
```

**Language filter options**:
- `***LANGUAGE_interface***` — interface language
- `***LANGUAGE_content***` — content language
- `en`, `es`, `fr` — specific language code

### Pattern: Querying Translatable Fields

**Field conditions work per translation**:

```php
// Query nodes where Spanish translation has specific title
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('title', 'Título en español')
  ->condition('langcode', 'es')
  ->accessCheck(TRUE);
```

**Non-translatable field conditions**:

```php
// Non-translatable fields same across all translations
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('created', strtotime('-1 week'), '>')
  ->accessCheck(TRUE);
// Returns results regardless of langcode
```

### Known Issues & Limitations

**Issue**: `latestRevision()` is NOT language-aware
- Querying for latest revision doesn't filter by language
- Returns latest revision ID across all languages
- If Spanish translation updated recently, querying for latest English revision returns Spanish revision ID

**Issue**: Entity reference relationships in Views don't always join on langcode
- Can cause incorrect results with translated references
- See https://www.drupal.org/project/drupal/issues/2737619

**Issue**: `notExists` condition with translations
- Complex behavior when one translation has field value but others don't
- See https://www.drupal.org/project/drupal/issues/2933202

**Workaround for latest revision per language**: Use custom query or loop through revisions programmatically.

### Common Mistakes

- **Forgetting to filter by langcode** → Query returns entities in all languages mixed together. Users see content in wrong language
- **Assuming latestRevision() is language-aware** → Latest revision query doesn't filter by language. Must handle in code
- **Filtering by langcode without checking translations exist** → Query returns nothing if no translation exists. Use `default_langcode` condition for untranslated content
- **Not considering non-translatable fields** → Querying non-translatable field returns results in all languages because field value is shared
- **Missing access check** → Always include `->accessCheck(TRUE)` or `->accessCheck(FALSE)` explicitly. Modern Drupal requires it

### See Also
- → [Translation & Revisions](translation-revisions.md) — revision behavior with translations
- → [Programmatic Entity Translation](programmatic-entity-translation.md) — getTranslation() API
- → [Security, Performance & Caching](security-performance-caching.md) — language cache contexts
- Reference: https://www.drupal.org/project/drupal/issues/3056602 (langcode filter issue)
- Reference: https://www.drupal.org/project/drupal/issues/3092835 (entity query multilingual issues)
