---
description: "Detect HTMX requests and access request metadata using HtmxRequestInfoTrait in controllers and forms"
tldr: "Use this when you need to detect if a request is from HTMX and access metadata (triggering element, target, prompt) in controllers or forms via HtmxRequestInfoTrait's 8 methods."
drupal_version: "11.x"
---

# Request Detection

## When to Use

> You need to detect if a request is from HTMX and access request metadata (triggering element, target, prompt, etc.) in controllers or forms.

## Using HtmxRequestInfoTrait

Forms automatically include this trait via `FormBase`. Controllers need to implement `getRequest()` method.

Reference: `/core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php` — 8 detection methods
Reference: `/core/lib/Drupal/Core/Form/FormBase.php` line 48 — Trait inclusion

## Available Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `isHtmxRequest()` | bool | TRUE if `HX-Request` header present |
| `isHtmxBoosted()` | bool | TRUE if `HX-Boosted` header present |
| `getHtmxCurrentUrl()` | string | Value of `HX-Current-URL` header |
| `isHtmxHistoryRestoration()` | bool | TRUE for history restore requests (cache miss) |
| `getHtmxPrompt()` | string | Value from prompt dialog if shown |
| `getHtmxTarget()` | string | Target element ID |
| `getHtmxTrigger()` | string | Triggering element ID |
| `getHtmxTriggerName()` | string | Triggering element name attribute |

## Pattern: Using in Forms

Forms automatically have access:

```php
use Drupal\Core\Form\FormBase;

class MyForm extends FormBase {
  public function buildForm(array $form, FormStateInterface $form_state) {
    // Detect HTMX request
    if ($this->isHtmxRequest()) {
      // Get triggering element
      $trigger = $this->getHtmxTriggerName();

      if ($trigger === 'field_name') {
        // Handle specific field change
      }
    }

    return $form;
  }
}
```

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 136-161 — Production example

## Pattern: Using in Controllers

Controllers need to implement `getRequest()`:

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
      // Return minimal HTMX response
    }
    return $full_page_build;
  }
}
```

## Pattern: Detecting Triggering Element

HTMX automatically sends triggering element name via `_triggering_element_name` parameter:

```php
// In form buildForm() method
$input = $form_state->getUserInput();
$trigger = $input['_triggering_element_name'] ?? '';

if ($trigger === 'config_type') {
  // Handle type selector change
} elseif ($trigger === 'config_name') {
  // Handle name selector change
}
```

Reference: `/core/misc/htmx/htmx-assets.js` lines 59-62 — JavaScript adds this parameter when `HX-Trigger-Name` header present

## Common Mistakes

- Using `getHtmxTrigger()` for form element names — Use `getHtmxTriggerName()` or `getUserInput()['_triggering_element_name']`
- Not implementing `getRequest()` in controllers — Trait methods will fail
- Assuming all requests are HTMX — Always check `isHtmxRequest()` before using other trait methods
- Forgetting to handle non-HTMX fallback — Forms should work without JavaScript

## See Also

- Previous: [Library Dependencies](library-dependencies.md)
- Next: [Dynamic Forms](dynamic-forms.md)
- Reference: [ConfigSingleExportForm Production Example](production-example-config-export.md)
