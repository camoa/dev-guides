---
description: AI Translate — standalone module for AI-powered content and interface translation, with config-entity prompts.
tldr: "**Status: STANDALONE** — `drupal/ai_translate` 1.3.1 (split from AI Core per #3570275). Requires `drupal/ai >1.2.1` + content_translation; Drupal ^10.4 || ^11. Use for one-click AI content/interface translation with per-site and per-language prompt customization."
drupal_version: "11.x"
---

# AI Translate

## When to Use

> Use `drupal/ai_translate` (standalone, 1.3.1) for one-click AI-powered content and interface translation. Install the standalone project — do not use the bundled `ai` submodule, which is deprecated and will be removed in AI Core 2.0.0. Requires `drupal/ai >1.2.1` + `content_translation`; Drupal `^10.4 || ^11`.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Translate UI strings | `ai_translate` + locale | AJAX button per string on translation pages |
| Translate content fields | `ai_translate` + `content_translation` | "AI Translations" column on overview |
| Bulk translation | Drush commands | `drush ai:translate-entity` |
| Per-language prompt | `language_settings` + prompt config entity | Correct way to target specific languages |
| Per-language model switch | `hook_ai_translate_translation_alter` | Per-language model is saved in UI but not applied in 1.3.x |

## Install

```bash
composer require 'drupal/ai_translate:^1.3'
```

The bundled `ai` submodule (`modules/ai_translate`) remains as `lifecycle: deprecated` until AI Core 2.0.0. New sites use the standalone; existing sites enable it then run `drush updatedb` to migrate prompts and config keys.

## Config: `ai_translate.settings`

Admin form: `/admin/config/ai/ai-translate` (permission `manage ai translation prompts`).

| Key | Default | Description |
|-----|---------|-------------|
| `use_ai_translate` | `true` | Override entity "Translate" tab with AI links. Set `false` when used as a backend only (e.g. AI TMGMT). |
| `prompt` | `ai_translate__ai_translate_default` | ID of the default `ai.ai_prompt` config entity (type `ai_translate`). |
| `language_settings` | `{}` | Per-language `prompt` + `model` overrides. |
| `reference_defaults` | `{}` | Entity types translated by default when a referencing entity is translated. |
| `entity_reference_depth` | `1` | Max recursion for references. UI choices: `0` (Unlimited), `1`, `2`, `5`, `10`. |
| `translation_status` | `keep_original` | `keep_original` or `create_draft`. |
| `redirect_after_create` | `list` | `list` or `edit`. |

Permissions: `manage ai translation prompts`, `create ai content translation`, `create ai interface translation`.

## Customizing Translation Prompts

Translation quality is driven by a **config entity**, not a hardcoded string. The module ships:

- a prompt **type** `ai.ai_prompt_type.ai_translate` (declares the available template variables), and
- a default prompt `ai.ai_prompt.ai_translate__ai_translate_default`.

Edit the default — or select a different entity — in the settings form's **Default translation prompt** field (an `ai_prompt` widget restricted to `ai_translate`-type prompts). Rendered prompts must be at least 50 characters.

**Template variables** (required: `{destLangName}`, `{inputText}`):

| Token | In Twig context? | Meaning |
|-------|------------------|---------|
| `{sourceLang}` / `sourceLang` | Yes | Source language ID (e.g. `en`) — only when known |
| `{sourceLangName}` / `sourceLangName` | Yes | Source language name — only when known |
| `{destLang}` | No | Target language ID |
| `{destLangName}` | No | Target language name (**required**) |
| `{inputText}` | No | Text to translate (**required**) |

Prompts resolve in two passes: **(1)** Twig `renderInline` with only `sourceLang`/`sourceLangName` in context, then **(2)** `strtr` for all `{...}` brace tokens. Consequence: `{% if %}` logic can only branch on source language — `destLang` is not in the Twig context. Use per-language prompt overrides for target-language-specific instructions.

```twig
You are a professional translator.
{% if sourceLangName %}Translate from {sourceLangName} {% else %}Detect the source language and translate {% endif %}to {destLangName}.
{% if sourceLang == 'sv' %}If the target uses formal/informal register, default to the formal form.{% endif %}
Preserve all HTML; only translate visible text and translatable attributes (alt, title, placeholder, value).
Return only the translation, no commentary.
Text: ``` {inputText} ```
```

**What the shipped default already guarantees (preserve when customizing):** prompt-injection hardening, HTML structure preservation, LTR↔RTL markup adjustments, "return only the translation." Add terminology, tone, and domain guidance on top.

**Per-language prompt overrides** — set in the settings UI or config:

```yaml
language_settings:
  de:
    prompt: ai_translate__ai_translate_de   # used for → German
    model: ''                               # saved but not applied in 1.3.x
```

**Programmatic control** — for glossaries, injected context, or provider/model swaps the prompt can't express:

```php
function mymodule_ai_translate_translation_alter(
  \Drupal\ai\OperationType\Chat\ChatInput &$messages,
  string &$providerId,
  string &$modelId,
): void {
  // Prepend a glossary, force a provider/model, or inject context.
  // Fires once per batch before the first request.
}
```

## Field Text Extractors

`FieldTextExtractor` plugins declare which columns of a field type are translatable.

| Plugin | Field Types | Translates |
|--------|------------|------------|
| `text` | title, text, string | `value` |
| `text_with_summary` | text_with_summary | `value`, `summary` |
| `link` | link | `title` |
| `image` | image | `alt`, `title` |
| `file` | file | `description` |
| `layout_builder` | layout_section | Inline blocks via `LbFieldExtractor` (symmetric + asymmetric) |
| `entity_reference` | entity_reference | Referenced entities recursively |

Custom extractor:

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

## Entity Reference Translation

Which referenced entities are followed is set globally via `reference_defaults` and overridden per field via the third-party setting `ai_translate:translate_references` on entity-reference fields. When enabled, the translator recurses up to `entity_reference_depth` levels. `entity_reference_depth: 0` (Unlimited) can translate the entire entity graph — set it conservatively.

## How Translation Runs

`ChatTranslationProvider` (id `chat_translation`) resolves the active prompt (per-language override → default), renders it, sends it to the site's default `chat` provider, and strips code-fence/quote wrapping from the result. Any chat provider can serve as the translation backend.

## Drush Commands

```bash
drush ai:translate-entity node "1,2,3" en fr  # Translate specific nodes to French
drush ai:translate-text "Hello world" en fr    # Translate a text string
```

## Migration from the Bundled Submodule

1. `composer require 'drupal/ai_translate:^1.3'` (AI Core stays; standalone requires `ai:>1.2.1`)
2. Enable the standalone module.
3. `drush updatedb` — runs `post_update` hooks that:
   - Convert legacy free-text prompts into `ai.ai_prompt` config entities
   - Rename old `{{ snake_case }}` variables to camelCase tokens
   - Migrate per-language prompts to `ai.ai_prompt.ai_translate__ai_translate_<langcode>`
   - Move flat `<langcode>_model`/`<langcode>_prompt` keys into nested `language_settings`

## Common Mistakes

- **Wrong**: Using old variable names `{{ text }}`, `{{ source_lang_name }}` in new prompts → **Right**: Use camelCase tokens: `{inputText}`, `{sourceLangName}`, `sourceLang`. The in-app help topic still shows the old names — ignore it.
- **Wrong**: Setting `entity_reference_depth: 0` without testing → **Right**: `0` means unlimited; it can recursively translate the entire entity graph. Start with `1`.
- **Wrong**: Relying on per-language model switching in 1.3.x → **Right**: The model field is saved but not applied. Use `hook_ai_translate_translation_alter` to force a provider/model.
- **Wrong**: Branching on `destLang` in Twig (`{% if destLang == 'de' %}`) → **Right**: `destLang` is not in the Twig context. Use per-language prompt entities for target-specific instructions.

## See Also

- [AI Module Core Architecture](core-architecture.md)
- Reference: `web/modules/contrib/ai_translate/` (standalone) or `web/modules/contrib/ai/modules/ai_translate/` (bundled, deprecated)
- Standalone project: https://www.drupal.org/project/ai_translate
- Split issue: https://www.drupal.org/node/3570275
