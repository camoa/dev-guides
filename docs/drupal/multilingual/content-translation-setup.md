---
description: Drupal content translation setup — enabling entity translation per bundle for nodes, terms, media, blocks, custom entities
---

# Content Translation Setup

### When to Use
When enabling entity translation for nodes, taxonomy terms, media, blocks, menu links, or custom entities.

### Decision: What to Enable Translation For

| If you need... | Enable translation for... | Via config |
|---|---|---|
| Translate articles, pages | Node entity type, per bundle | `language.content_settings.node.article` |
| Translate taxonomy terms | Taxonomy term entity, per vocabulary | `language.content_settings.taxonomy_term.tags` |
| Translate media (images, videos) | Media entity, per media type | `language.content_settings.media.image` |
| Translate blocks | Block content entity, per block type | `language.content_settings.block_content.basic` |
| Translate menu links | Menu link content entity | `language.content_settings.menu_link_content.menu_link_content` |
| Translate custom entities | Your entity type, per bundle | `language.content_settings.ENTITY_TYPE.BUNDLE` |

### Pattern: Enabling Content Translation via Config

**File**: `config/install/language.content_settings.node.article.yml`

```yaml
langcode: en
status: true
dependencies:
  config:
    - node.type.article
  module:
    - content_translation
id: node.article
target_entity_type_id: node
target_bundle: article
default_langcode: site_default
language_alterable: true
third_party_settings:
  content_translation:
    enabled: true
    bundle_settings:
      untranslatable_fields_hide: false
```

**Explanation**:
- `target_entity_type_id: node` — entity type
- `target_bundle: article` — bundle (content type)
- `default_langcode: site_default` — default language for new entities
- `language_alterable: true` — users can change language when creating/editing
- `third_party_settings.content_translation.enabled: true` — enables translation

**Alternative default language options**:
- `site_default` — site's default language
- `current_interface` — current UI language
- `authors_default` — content author's preferred language
- Specific langcode like `en`, `es`

**Programmatic example**:

```php
use Drupal\language\Entity\ContentLanguageSettings;

$config = ContentLanguageSettings::loadByEntityTypeBundle('node', 'article');
if (!$config) {
  $config = ContentLanguageSettings::create([
    'target_entity_type_id' => 'node',
    'target_bundle' => 'article',
  ]);
}
$config->setDefaultLangcode('site_default')
  ->setLanguageAlterable(TRUE)
  ->setThirdPartySetting('content_translation', 'enabled', TRUE)
  ->save();
```

### Common Mistakes

- **Enabling Content Translation module without configuring per entity** → Module enables infrastructure but doesn't automatically make entities translatable. Must configure per entity type and bundle
- **Forgetting dependencies in config** → Config YAML must declare dependency on entity bundle config (e.g., `node.type.article`) and `content_translation` module
- **Setting language_alterable: false when users need to change language** → Users cannot change entity language on edit form. Set to `true` unless you have specific workflow requiring fixed language
- **Using wrong default_langcode value** → Invalid values cause validation errors. Use `site_default`, `current_interface`, `authors_default`, or valid langcode
- **Not updating field translatability** → Enabling entity translation doesn't automatically make fields translatable. [Field Translatability](field-translatability.md) for field configuration

### See Also
- → [Translating Content Entities](translating-content-entities.md) — creating translations
- → [Field Translatability](field-translatability.md) — configuring translatable fields
- → [Programmatic Entity Translation](programmatic-entity-translation.md) — addTranslation() API
- Reference: `core/modules/content_translation/`
- Reference: https://drupalize.me/tutorial/user-guide/language-content-config
