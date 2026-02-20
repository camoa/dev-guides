---
description: Detect HTMX requests and access request metadata using HtmxRequestInfoTrait in controllers and forms
drupal_version: "11.x"
---

# Request Detection

## When to Use

> Use this when you need to detect if a request is from HTMX and access metadata (triggering element, target, prompt) in controllers or forms.

## Decision

| Method | Returns | Purpose |
|--------|---------|---------|
| `isHtmxRequest()` | bool | TRUE if `HX-Request` header present |
| `isHtmxBoosted()` | bool | TRUE if `HX-Boosted` header present |
| `getHtmxCurrentUrl()` | string | Value of `HX-Current-URL` header |
| `isHtmxHistoryRestoration()` | bool | TRUE for history restore requests |
| `getHtmxPrompt()` | string | Value from prompt dialog if shown |
| `getHtmxTarget()` | string | Target element ID |
| `getHtmxTrigger()` | string | Triggering element ID |
| `getHtmxTriggerName()` | string | Triggering element name attribute |

`FormBase` includes this trait automatically. Controllers must implement `getRequest()`.

## Pattern

**In forms** (trait included automatically via `FormBase`):

```php
use Drupal\Core\Form\FormBase;

class MyForm extends FormBase {
  public function buildForm(array $form, FormStateInterface $form_state) {
    if ($this->isHtmxRequest()) {
      $trigger = $this->getHtmxTriggerName();
      if ($trigger === 'field_name') {
        // Handle specific field change
      }
    }
    return $form;
  }
}
```

**In controllers** (must implement `getRequest()`):

```php
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Htmx\HtmxRequestInfoTrait;

class MyController extends ControllerBase {
  use HtmxRequestInfoTrait;

  protected function getRequest() {
    return \Drupal::request();
  }

  public function content() {
    if ($this->isHtmxRequest()) {
      return ['#markup' => '<div>Just the content</div>'];
    }
    return $full_page_build;
  }
}
```

**Detecting triggering element via form input:**

```php
$input = $form_state->getUserInput();
$trigger = $input['_triggering_element_name'] ?? '';
```

## Common Mistakes

- **Wrong**: Using `getHtmxTrigger()` for form element names → **Right**: Use `getHtmxTriggerName()` or `getUserInput()['_triggering_element_name']`
- **Wrong**: Not implementing `getRequest()` in controllers → **Right**: Trait methods will fail without it
- **Wrong**: Assuming all requests are HTMX → **Right**: Always check `isHtmxRequest()` before using other trait methods
- **Wrong**: Forgetting to handle non-HTMX fallback → **Right**: Forms should work without JavaScript

## See Also

- [Library Dependencies](library-dependencies.md)
- [Dynamic Forms](dynamic-forms.md)
- [Production Example: ConfigSingleExportForm](production-example-config-export.md)
- Reference: `/core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php`
- Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 136-161
