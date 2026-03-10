---
description: AI Translate — deprecated module for AI-powered content and interface translation (replaced by standalone project)
drupal_version: "11.x"
---

# AI Translate

## When to Use

> **Status: DEPRECATED** — moving to standalone `drupal/ai_translate` project. This guide covers the module as it exists in AI 1.3.0-rc2. See https://www.drupal.org/node/3570275 for the migration plan.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Translate UI strings | `ai_translate` + locale | AJAX button per string on translation pages |
| Translate content fields | `ai_translate` + `content_translation` | "AI Translations" column on overview |
| Bulk translation | Drush commands | `drush ai:translate-entity` |
| Per-language model | `language_settings` config key | Override model/prompt per target language |

## Config: `ai_translate.settings`

| Key | Default | Description |
|-----|---------|-------------|
| `use_ai_translate` | `true` | Override translate tab with AI links |
| `entity_reference_depth` | `1` | Max recursion for references (0=unlimited) |
| `translation_status` | `keep_original` | `keep_original` or `create_draft` |
| `language_settings` | `{}` | Per-language model/prompt overrides |

## Drush Commands

```bash
drush ai:translate-entity node "1,2,3" en fr  # Translate specific nodes to French
drush ai:translate-text "Hello world" en fr    # Translate a text string
```

## Alter Hook

```php
hook_ai_translate_translation_alter(&$messages, &$provider_id, &$model_id)
```

## Custom FieldTextExtractor

```php
#[FieldTextExtractor(
  id: 'my_field',
  label: new TranslatableMarkup('My Field'),
  field_types: ['my_field_type'],
)]
class MyFieldExtractor extends FieldExtractorBase {
  public function getColumns(): array { return ['value', 'extra']; }
}
```

## Built-in FieldTextExtractor Plugins

| Plugin | Field Types | Translates |
|--------|------------|------------|
| `text` | title, text, string | `value` |
| `text_with_summary` | text_with_summary | `value`, `summary` |
| `link` | link | `title` |
| `image` | image | `alt`, `title` |
| `layout_builder` | layout_section | Inline blocks (symmetric + asymmetric) |
| `entity_reference` | entity_reference | Referenced entities recursively |

## Common Mistakes

- **Wrong**: Setting `entity_reference_depth: 0` without performance testing → **Right**: Unlimited depth can translate the entire entity graph recursively; set conservatively
- **Wrong**: Using `ai_translate` for new projects → **Right**: Module is deprecated; wait for the standalone replacement

## See Also

- [AI Module Core Architecture](core-architecture.md)
- Reference: `web/modules/contrib/ai/modules/ai_translate/`
- Deprecation issue: https://www.drupal.org/node/3570275
