---
description: Drupal field translatability — configuring translatable vs non-translatable fields, field synchronization across translations
---

# Field Translatability

### When to Use
When configuring which fields should have separate values per language vs shared values across all translations.

### Decision: Translatable vs Non-Translatable Fields

| Field type | Translatable? | Why |
|---|---|---|
| Title, body, text fields | Yes | Content varies by language |
| Images, files (media reference) | Usually No | Same media across languages (caption/alt may be translatable) |
| Dates, numbers | Usually No | Facts don't change by language |
| Entity references (taxonomy, node) | Depends | If referenced entity is translatable, field can reference translation |
| Boolean flags | Usually No | Status/settings same across languages |
| Field labels and descriptions | Yes (via config translation) | UI text needs translation |

### Pattern: Configuring Field Translatability

**Via UI**:
- Go to field settings (`/admin/structure/types/manage/article/fields`)
- Edit field → scroll to "Translation" section
- Check/uncheck "Users may translate this field"
- Save

**Via config YAML** — `config/install/field.field.node.article.body.yml`:

```yaml
langcode: en
status: true
dependencies:
  config:
    - field.storage.node.body
    - node.type.article
  module:
    - text
id: node.article.body
field_name: body
entity_type: node
bundle: article
label: Body
translatable: true  # <-- Makes field translatable
```

**Field storage vs field instance**:
- **Field storage** (`field.storage.node.body`) — defines field type, cardinality, shared across bundles
- **Field instance** (`field.field.node.article.body`) — attaches field to bundle, sets `translatable: true`

**Programmatic example**:

```php
$field = \Drupal::entityTypeManager()
  ->getStorage('field_config')
  ->load('node.article.body');

$field->setTranslatable(TRUE)->save();
```

### Pattern: Field Translation Synchronization

Some multi-column fields (like links, images with alt text) can synchronize specific columns across translations while keeping others translatable.

**Via config** — `field.field.node.article.field_link.yml`:

```yaml
third_party_settings:
  content_translation:
    translation_sync:
      uri: uri  # Synchronize URL across translations
      title: '0'  # Don't sync title (translatable)
      options: '0'  # Don't sync options
```

**Use cases**:
- Link field: sync URL, translate title
- Image field: sync file ID, translate alt text
- Paragraph field: typically don't sync (each translation has own paragraphs)

### Common Mistakes

- **Making everything translatable** → Performance cost for translatable fields. Only make fields translatable that actually need different values per language
- **Non-translatable field changes affect all translations** → Changing non-translatable field value in Spanish translation changes it in English too. Users don't expect this
- **Forgetting to translate field labels** → Field instance label ("Body", "Image") is config translation, separate from field content. [Config Translation](config-translation.md)
- **Changing translatability after content exists** → Toggling `translatable` on existing fields can cause data loss or integrity issues. Plan translatability before launch
- **Synchronizing paragraphs incorrectly** → Paragraphs entity reference fields usually shouldn't sync — each translation needs independent paragraphs. Syncing causes translations to share same paragraph entities

### See Also
- → [Translating Content Entities](translating-content-entities.md) — translation workflow
- → [Config Translation](config-translation.md) — translating field labels
- → [Programmatic Entity Translation](programmatic-entity-translation.md) — accessing translated field values
- Reference: `core/modules/content_translation/content_translation.admin.inc` (deprecated in 11.4.0, [Drupal 11 Changes](drupal-11-changes.md))
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide
