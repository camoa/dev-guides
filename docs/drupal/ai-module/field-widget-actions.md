---
description: Field Widget Actions — framework for attaching AI action buttons to entity form field widgets
tldr: "Use this guide when adding action buttons to field widgets on entity edit forms. The `field_widget_actions` module is AI-agnostic — it provides the framework; other modules provide the actual AI plugins."
drupal_version: "11.x"
---

# Field Widget Actions

## When to Use

> Use this guide when adding action buttons to field widgets on entity edit forms.

The `field_widget_actions` module is an AI-agnostic framework for attaching action buttons to field widgets on entity forms. Other modules provide the actual plugins.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple action button | `FieldWidgetActionBase` | Direct action on click |
| Multi-step interaction | `FieldWidgetFormActionBase` | Modal dialog with form |
| Fill a text input | `FillSimpleFieldCommand` | Standard AJAX command |
| Fill CKEditor | `FillEditorCommand` | CKEditor-specific AJAX command |
| Deploy via recipe | `setComponentThirdPartySetting` config action | Declarative recipe config |

## Plugin System

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

For multi-step interactions, extend `FieldWidgetFormActionBase`:

```php
public function buildModalForm(array $form, FormStateInterface $form_state, ?ContentEntityInterface $entity): array {
  $form['selection'] = ['#type' => 'radios', '#options' => [...]];
  return $form;
}

protected function submitModalFormFillFields(array $form, FormStateInterface $form_state, AjaxResponse $response): AjaxResponse {
  $response->addCommand(new FillSimpleFieldCommand($selector, $value));
  return $response;
}
```

## Ajax Commands

| Command | Purpose |
|---------|---------|
| `FillSimpleFieldCommand` | Fill an input/textarea |
| `FillEditorCommand` | Fill a CKEditor instance |

## Config Action for Recipes

| Method | Purpose |
|--------|---------|
| `returnSuggestions($suggestions, $selector)` | Returns an `AjaxResponse` showing suggestions in a modal dialog |
| `getSuggestionsTarget($form, $form_state)` | Returns the CSS selector for the target field element |
| `buildEntity($form, $form_state)` | Reconstructs the entity from form state (for context-aware actions) |
| `processWidgetWithGroup($form, $form_state, $context)` | Processes widget actions grouped by field |

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

## FieldWidgetActionBase Key Methods

| Method | Purpose |
|--------|---------|
| `returnSuggestions($suggestions, $selector)` | Returns an `AjaxResponse` showing suggestions in a modal dialog |
| `getSuggestionsTarget($form, $form_state)` | Returns the CSS selector for the target field element |
| `buildEntity($form, $form_state)` | Reconstructs the entity from form state (for context-aware actions) |
| `processWidgetWithGroup($form, $form_state, $context)` | Processes widget actions grouped by field |

## ImageAltTextActionButtonTrait

Trait for image alt text actions that conditionally shows the button only when an image is uploaded. Uses Drupal `#states` visibility to hide the button until a file is present in the image widget.

## FieldWidgetActionManager Methods

| Method | Purpose |
|--------|---------|
| `getAllowedFieldWidgetActions($widget_type, $field_type)` | Returns plugins applicable to the given widget/field type combination |
| `getFieldWidgetActionFormDefinitions($widget_type, $field_type)` | Returns form element definitions for the "manage form display" settings |

## `FORM_ELEMENT_PROPERTY` Constant

Override in your plugin for non-standard fields:

- Default: `'value'`
- Entity reference: `'target_id'`
- Image alt: `'alt'`

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Not implementing `isAvailable()` | `FieldWidgetActionBase::isAvailable()` defaults to `TRUE` — the button shows even when no provider is configured, unless you override it (e.g., to check `hasProvidersForOperationType()`) |
| Using `FillEditorCommand` for a plain textarea | `FillEditorCommand` is CKEditor-specific; use `FillSimpleFieldCommand` for standard inputs |

## See Also

- [AI CKEditor](ai-ckeditor.md)
- [AI Automators](ai-automators.md)
- Reference: `web/modules/contrib/ai/modules/field_widget_actions/`
