---
description: AI CKEditor module — AI toolbar plugins for CKEditor 5, custom plugin development, and configuration
tldr: "Use this guide when adding AI text-generation capabilities to CKEditor 5. Use [AI Automators](ai-automators.md) for field-level automation outside the editor."
drupal_version: "11.x"
---

# AI CKEditor

## When to Use

> Use this guide when adding AI text-generation capabilities to CKEditor 5. Use [AI Automators](ai-automators.md) for field-level automation outside the editor.

The `ai_ckeditor` module adds AI text-generation capabilities to CKEditor 5 via a sparkle toolbar button. Each operation is a PHP plugin — no JavaScript authoring needed.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Free-form generation | `ai_ckeditor_completion` | Default open-ended AI text generation |
| Fix spelling/grammar | `ai_ckeditor_spellfix` | Purpose-built prompt |
| Change writing tone | `ai_ckeditor_tone` | Requires a "Tone of voice" taxonomy vocabulary |
| Run automator chain | `ai_automators_ckeditor` | Cross-module plugin from `ai_automators` |
| Custom AI operation | Custom plugin | Extend `AiCKEditorPluginBase` |

## Pattern

```php
use Drupal\ai_ckeditor\Attribute\AiCKEditor;
use Drupal\ai_ckeditor\AiCKEditorPluginBase;

#[AiCKEditor(
  id: 'my_plugin',
  label: new TranslatableMarkup('My Feature'),
  description: new TranslatableMarkup('Does something with selected text.'),
)]
final class MyPlugin extends AiCKEditorPluginBase {

  public function buildCkEditorModalForm(array $form, FormStateInterface $form_state, Editor $editor): array {
    $form['prompt'] = [
      '#type' => 'textarea',
      '#title' => $this->t('Instructions'),
    ];
    return $form;
  }

  public function ajaxGenerate(array &$form, FormStateInterface $form_state) {
    $prompt = $form_state->getValue(['plugin_config', 'prompt']);
    $response = new AjaxResponse();
    $response->addCommand(new AiRequestCommand(
      $prompt,
      $form_state->getValue('editor_id'),
      $this->pluginDefinition['id'],
      'ai-ckeditor-response'
    ));
    return $response;
  }
}
```

## Built-in Plugins

| Plugin ID | Description |
|-----------|-------------|
| `ai_ckeditor_completion` | Free-form AI text generation |
| `ai_ckeditor_spellfix` | Fix spelling/punctuation |
| `ai_ckeditor_summarize` | Summarize selected text |
| `ai_ckeditor_tone` | Change tone (requires taxonomy vocabulary) |
| `ai_ckeditor_translate` | Translate selected text |
| `ai_ckeditor_reformat_html` | Reformat HTML structure |
| `ai_ckeditor_modify_prompt` | Modify with custom prompt |
| `ai_ckeditor_help` | Help/documentation |
| `ai_automators_ckeditor` | Run AutomatorChain workflows (from `ai_automators`) |

The `ai_automators_ckeditor` plugin (provided by `ai_automators`, not `ai_ckeditor`) exposes AutomatorChains as CKEditor operations. It supports configurable inputs, write modes (append/prepend/replace), and require-selection options.

## Plugin Attribute: `module_dependencies`

The `#[AiCKEditor]` attribute has an optional `module_dependencies` array. If specified, the plugin only appears when those modules are installed. For example, `ai_ckeditor_tone` declares `module_dependencies: ['taxonomy']`.

## AJAX Command: AiRequestCommand

The `AiRequestCommand` is a custom AJAX command that triggers the streamed AI request from the dialog form's "Generate" button. It passes the prompt, editor ID, plugin ID, and target wrapper to the JS handler, which initiates the streaming request to `/api/ai-ckeditor/request/{editor}/{plugin}` and renders the response progressively.

## Global Config: `ai_ckeditor.settings`

Customizable prompts per operation type are stored in `ai_ckeditor.settings.prompts`. Each prompt supports Twig-like placeholders (e.g., `{{ modify_prompt }}`, `{{ tone }}`, `{{ lang }}`). Override via config import or settings.php.

## Configuration Steps

1. Configure a text format at `/admin/config/content/formats`
2. Drag the AI Stars widget to the active toolbar
3. In CKEditor plugin settings: enable desired plugins, choose provider/model
4. For **Tone**: create a "Tone of voice" taxonomy vocabulary
5. For **Translate**: create a "Languages" vocabulary or use site languages

## Permission

- `use ai ckeditor` — required for all CKEditor AI features

## Common Mistakes

- **Wrong**: Enabling `ai_ckeditor_tone` without a vocabulary → **Right**: Create a "Tone of voice" vocabulary first
- **Wrong**: Writing the modal form submit logic inside `ajaxGenerate` → **Right**: Use `AiRequestCommand` to delegate to the streaming handler
- **Wrong**: Setting custom prompts only in code → **Right**: Override prompts via `ai_ckeditor.settings.prompts` config to keep them deployable

## See Also

- [AI Automators](ai-automators.md)
- Reference: `web/modules/contrib/ai/modules/ai_ckeditor/`
