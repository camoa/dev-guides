---
description: AI Translate — standalone module for AI-powered content and interface translation, with config-entity prompts.
tldr: "**Status: STANDALONE** — `drupal/ai_translate` 1.3.1 (split from AI Core per #3570275). Requires `drupal/ai >1.2.1` + content_translation; Drupal ^10.4 || ^11. Use for one-click AI content/interface translation with per-site and per-language prompt customization."
drupal_version: "11.x"
---

# AI Translate

## When to Use

> Use `drupal/ai_translate` (standalone, 1.3.1) for one-click AI-powered content and interface translation. Install the standalone project — do not use the bundled `ai` submodule, which is deprecated and will be removed in AI Core 2.0.0.

**Status:** Standalone project — [`drupal/ai_translate`](https://www.drupal.org/project/ai_translate). Latest stable **1.3.1** (Feb 2026); security-team covered.
**Was:** a bundled `ai` submodule, deprecated and split out per [#3570275](https://www.drupal.org/node/3570275). The bundled copy still ships with AI Core as `lifecycle: deprecated` until AI Core 2.0.0 removes it; new sites install the standalone instead.
**Requires:** `drupal/ai` `>1.2.1`, `drupal:content_translation`. Drupal `^10.4 || ^11`.
**Install:** `composer require 'drupal/ai_translate:^1.3'`

Provides one-click AI-powered content and interface translation. The 1.3.0 release is a near 1-to-1 copy of the former submodule (based on `ai:1.2.1`); 1.3.1 adds bug fixes (HTML-prefix stripping, entity-reference deletion on failure). There is no standalone 1.4.x yet; the `2.0.x-dev` branch tracks AI Core 2.0.x.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Translate UI strings | `ai_translate` + locale | AJAX button per string on translation pages |
| Translate content fields | `ai_translate` + `content_translation` | "AI Translations" column on overview |
| Bulk translation | Drush commands | `drush ai:translate-entity` |
| Per-language prompt | `language_settings` + prompt config entity | Correct way to target specific languages |
| Per-language model switch | `hook_ai_translate_translation_alter` | Per-language model is saved in UI but not applied in 1.3.x |

## Features

- "AI Translations" column on entity translation overview
- Batch field-by-field translation
- Interface (locale) string translation via AJAX button
- Recursive entity reference translation (configurable depth)
- Layout Builder inline block translation
- **Prompt as config entity** — per-site and per-language prompt overrides, editable in the UI
- Drush commands for bulk translation

## Settings

Admin form: **Configuration → Content authoring → AI Translate** (`/admin/config/ai/ai-translate`, permission `manage ai translation prompts`). Config object `ai_translate.settings`:

| Key | Default | Description |
|-----|---------|-------------|
| `use_ai_translate` | `true` | Take over the entity "Translate" tab with AI links. Set `false` when AI Translate is only a backend for another mechanism (e.g. AI TMGMT). |
| `prompt` | `ai_translate__ai_translate_default` | ID of the **default** `ai.ai_prompt` config entity (type `ai_translate`) used when no language-specific prompt is set. |
| `language_settings` | `{}` | Per-language `model` + `prompt` overrides (see prompt section). |
| `reference_defaults` | `{}` | Entity types translated by default when a referencing entity is translated (overridable per entity-reference field). |
| `entity_reference_depth` | `1` | Max recursion for references. UI choices: `0` (Unlimited), `1`, `2`, `5`, `10`. |
| `translation_status` | `keep_original` | `keep_original` or `create_draft`. |
| `redirect_after_create` | `list` | `list` or `edit`. |

Permissions: `manage ai translation prompts` (settings), `create ai content translation`, `create ai interface translation`.

## Customizing & improving translation prompts

Translation quality is driven by the prompt, and the prompt is a **config entity**, not a hardcoded string. The module ships:

- a prompt **type** `ai.ai_prompt_type.ai_translate` (declares the available template variables), and
- a default prompt `ai.ai_prompt.ai_translate__ai_translate_default`.

Edit the default — or select a different prompt entity — in the settings form's **Default translation prompt** field (an `ai_prompt` widget restricted to `ai_translate`-type prompts). Rendered prompts must be at least 50 characters (form validation).

**Template variables.** Available tokens (required: `destLangName`, `inputText`):

| Token | In Twig context? | Meaning |
|-------|------------------|---------|
| `{sourceLang}` / `sourceLang` | ✅ | Source language ID (e.g. `en`) — only when a source language is known |
| `{sourceLangName}` / `sourceLangName` | ✅ | Source language name — only when known |
| `{destLang}` | ❌ | Target language ID |
| `{destLangName}` | ❌ | Target language name (**required**) |
| `{inputText}` | ❌ | Text to translate (**required**) |

The prompt is resolved in two passes: **(1)** Twig `renderInline` with a context containing only `sourceLang` / `sourceLangName`, then **(2)** brace-token string replacement (`strtr`) for all `{...}` tokens. Consequence: **Twig `{% if %}` logic can branch on the source language only** — `destLang` is not in the Twig context, so you cannot `{% if destLang == 'de' %}`. For target-language-specific prompts, use a **per-language prompt override** (below), not Twig.

```twig
You are a professional translator.
{% if sourceLangName %}Translate from {sourceLangName} {% else %}Detect the source language and translate {% endif %}to {destLangName}.
{% if sourceLang == 'sv' %}If the target uses formal/informal register, default to the formal form.{% endif %}
Preserve all HTML; only translate visible text and translatable attributes (alt, title, placeholder, value).
Return only the translation, no commentary.
Text: ``` {inputText} ```
```

**What the shipped default already does (emulate, don't undo):** prompt-injection hardening (ignore instructions embedded in the input past the listed rules), preserve HTML structure while translating only translatable attributes (`alt`/`title`/`placeholder`/`value`/…), allow LTR↔RTL markup adjustments, and "return only the translation." When improving the prompt, keep these guarantees and add your domain guidance (terminology, tone, register) on top.

> **Variable-name trap:** the module's in-app help topic still shows the *old* names (`{{ text }}`, `{{ source_lang_name }}`, `{% if source_lang == 'sv' %}`). Those were renamed — `post_update` migrates existing prompts, but **new prompts must use the camelCase tokens above** (`{inputText}`, `{sourceLangName}`, `sourceLang`).

**Per-language overrides.** In the settings form each enabled language has its own **prompt** (an `ai_prompt` widget) and **model** select:

```yaml
language_settings:
  de:
    prompt: ai_translate__ai_translate_de   # used for → German
    model: ''                               # see caveat
```

The per-language **prompt** is honored: if set, it overrides the default for that target language (this is the correct way to do target-specific instructions). The per-language **model** field is saved but, in 1.3.x, **not applied** — `ChatTranslationProvider` always uses the default `chat` provider/model. Don't rely on per-language model switching until upstream wires it.

**Programmatic control — `hook_ai_translate_translation_alter`.** For glossaries, injected context, tone, or provider/model swaps that the prompt config can't express, alter the assembled chat request before it is sent:

```php
function mymodule_ai_translate_translation_alter(
  \Drupal\ai\OperationType\Chat\ChatInput &$messages,
  string &$providerId,
  string &$modelId,
): void {
  // e.g. prepend a glossary as a system instruction, or force a provider/model.
}
```

It fires once per batch, before the first request. There is no built-in glossary/tone/RAG feature — implement those via the prompt entity, per-language prompts, or this hook.

## Field text extractors

A `FieldTextExtractor` plugin decides which columns of a field type are translatable:

| Plugin | Field Types | Translates |
|--------|------------|------------|
| `text` | title, text, string | `value` |
| `text_with_summary` | text_with_summary | `value`, `summary` |
| `link` | link | `title` |
| `image` | image | `alt`, `title` |
| `file` | file | `description` |
| `layout_builder` | layout_section | Inline blocks via `LbFieldExtractor` (symmetric and asymmetric translation) |
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

## Layout Builder translation

`LbFieldExtractor` extracts translatable text from Layout Builder inline blocks, supporting both symmetric (same layout per language) and asymmetric (different layout per language) translation, configured per field in the entity's translation settings.

## Entity reference translation

Which referenced entities are followed is set globally via `reference_defaults` and overridden per field via the third-party setting `ai_translate:translate_references` on entity-reference fields. When enabled, the translator recurses up to `entity_reference_depth` levels. `entity_reference_depth: 0` (Unlimited) can translate the entire entity graph — set it conservatively.

## How translation runs

The `translate_text` operation is served by a chat-proxy provider (`ChatTranslationProvider`, id `chat_translation`): it resolves the prompt (per-language → default), renders it, sends it to the site's default `chat` provider, and strips code-fence/quote wrapping from the result. This lets any chat provider act as the translation backend. (Per #3570275 this proxy is slated to move into AI Core in the 2.0 line.)

## Drush commands

```bash
drush ai:translate-entity node "1,2,3" en fr  # Translate nodes
drush ai:translate-text "Hello world" en fr     # Translate text
```

## Migration from the bundled submodule

1. `composer require 'drupal/ai_translate:^1.3'` (AI Core stays installed; the standalone requires `ai:>1.2.1`).
2. Enable the standalone module if the bundled one was enabled. When AI Core 2.0.0 lands it removes the bundled submodule.
3. `drush updatedb` — `post_update`/update hooks convert a legacy free-text prompt into the `ai.ai_prompt` config entity, rename old `{{ snake_case }}` variables to the new tokens, migrate per-language prompts to `ai.ai_prompt.ai_translate__ai_translate_<langcode>`, and move flat `<langcode>_model` / `<langcode>_prompt` keys into nested `language_settings`.

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Using the old variable names `{{ text }}` / `{{ source_lang_name }}` in a new prompt | They were renamed; only existing prompts are migrated by `post_update`. New prompts must use `{inputText}`, `{sourceLangName}`, `sourceLang`. |
| Branching on `destLang` in Twig (`{% if destLang == 'de' %}`) | `destLang` is not in the Twig context — use a per-language prompt override instead |
| Setting `entity_reference_depth: 0` without testing | `0` means Unlimited and can translate the entire entity graph |
| Relying on the per-language model select in 1.3.x | It is saved but not applied; force a provider/model via `hook_ai_translate_translation_alter` |

## See Also

- [AI Module Core Architecture](core-architecture.md)
- [Prompt System](prompt-system.md)
- Reference: `web/modules/contrib/ai_translate/` (standalone) or `web/modules/contrib/ai/modules/ai_translate/` (bundled, deprecated)
- Standalone project: https://www.drupal.org/project/ai_translate
- Split issue: https://www.drupal.org/node/3570275
