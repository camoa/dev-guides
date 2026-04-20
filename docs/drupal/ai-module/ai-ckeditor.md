---
description: AI CKEditor module — AI toolbar plugins for CKEditor 5, custom plugin development, and configuration
tldr: "Use this guide when adding AI text-generation capabilities to CKEditor 5. Use [AI Automators](ai-automators.md) for field-level automation outside the editor."
drupal_version: "11.x"
---

# AI CKEditor

## When to Use

> Use this guide when adding AI text-generation capabilities to CKEditor 5. Use [AI Automators](ai-automators.md) for field-level automation outside the editor.

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
    $form['prompt'] = ['#type' => 'textarea', '#title' => $this->t('Instructions')];
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
| `ai_automators_ckeditor` | Run AutomatorChain workflows |

## Configuration Steps

1. Configure text format at `/admin/config/content/formats`
2. Drag the AI Stars widget to the active toolbar
3. Enable desired plugins; choose provider/model
4. For **Tone**: create a "Tone of voice" taxonomy vocabulary
5. For **Translate**: create a "Languages" vocabulary or use site languages
6. Permission: `use ai ckeditor` — required for all CKEditor AI features

## Module Dependencies (Silencing)

The `#[AiCKEditor]` attribute supports `module_dependencies: ['taxonomy']` — the plugin only appears when listed modules are installed. Use this to conditionally hide plugins that require contrib modules.

## Common Mistakes

- **Wrong**: Enabling `ai_ckeditor_tone` without a vocabulary → **Right**: Create a "Tone of voice" vocabulary first
- **Wrong**: Writing the modal form submit logic inside `ajaxGenerate` → **Right**: Use `AiRequestCommand` to delegate to the streaming handler
- **Wrong**: Setting custom prompts only in code → **Right**: Override prompts via `ai_ckeditor.settings.prompts` config to keep them deployable

## See Also

- [AI Automators](ai-automators.md)
- Reference: `web/modules/contrib/ai/modules/ai_ckeditor/`
