---
description: Field Widget Actions — framework for attaching AI action buttons to entity form field widgets
tldr: "Use this guide when adding action buttons to field widgets on entity edit forms. The `field_widget_actions` module is AI-agnostic — it provides the framework; other modules provide the actual AI plugins."
drupal_version: "11.x"
---

# Field Widget Actions

## When to Use

> Use this guide when adding action buttons to field widgets on entity edit forms. The `field_widget_actions` module is AI-agnostic — it provides the framework; other modules provide the actual AI plugins.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple action button | `FieldWidgetActionBase` | Direct action on click |
| Multi-step interaction | `FieldWidgetFormActionBase` | Modal dialog with form |
| Fill a text input | `FillSimpleFieldCommand` | Standard AJAX command |
| Fill CKEditor | `FillEditorCommand` | CKEditor-specific AJAX command |
| Deploy via recipe | `setComponentThirdPartySetting` config action | Declarative recipe config |

## Pattern

```php
use Drupal\field_widget_actions\Attribute\FieldWidgetAction;

#[FieldWidgetAction(
  id: 'my_action',
  label: new TranslatableMarkup('AI Suggest'),
  widget_types: ['text_textarea'],
  field_types: ['text_long'],
  category: new TranslatableMarkup('AI'),
  multiple: TRUE,  // Button per delta
)]
class MyAction extends FieldWidgetActionBase {

  public function isAvailable(): bool {
    return $this->providerManager->hasProvidersForOperationType('chat');
  }

  public function singleElementFormAlter(array &$form, FormStateInterface $form_state, array $context = []) {
    parent::singleElementFormAlter($form, $form_state, $context);
    // Parent adds the action button.
  }
}
```

## Modal Form Pattern

```php
// Extend FieldWidgetFormActionBase for multi-step interactions.
public function buildModalForm(array $form, FormStateInterface $form_state, ?ContentEntityInterface $entity): array {
  $form['selection'] = ['#type' => 'radios', '#options' => [...]];
  return $form;
}

protected function submitModalFormFillFields(array $form, FormStateInterface $form_state, AjaxResponse $response): AjaxResponse {
  $response->addCommand(new FillSimpleFieldCommand($selector, $value));
  return $response;
}
```

## Deploy via Recipe

```yaml
config:
  actions:
    core.entity_form_display.node.article.default:
      setComponentThirdPartySetting:
        component: body
        settings:
          bc6795f3-uuid:
            plugin_id: prompt_content_suggestion
            enabled: true
            settings:
              prompt: 'Suggest content'
```

## FORM_ELEMENT_PROPERTY Constant

Override in your plugin for non-standard fields:
- Default: `'value'`
- Entity reference: `'target_id'`
- Image alt: `'alt'`

## Common Mistakes

- **Wrong**: Not implementing `isAvailable()` → **Right**: Button shows even when no provider is configured
- **Wrong**: Using `FillEditorCommand` for a plain textarea → **Right**: Use `FillSimpleFieldCommand` for standard inputs; `FillEditorCommand` is CKEditor-specific

## See Also

- [AI CKEditor](ai-ckeditor.md)
- [AI Automators](ai-automators.md)
- Reference: `web/modules/contrib/ai/modules/field_widget_actions/`
