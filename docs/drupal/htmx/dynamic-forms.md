---
description: "Build Drupal forms with HTMX — cascading selects, OOB updates, and browser history management"
tldr: "Use this when building forms with cascading selects, conditional fields, or any form that updates based on user input without full page reload. FormBuilder handles form_build_id automatically via OOB swap."
drupal_version: "11.x"
---

# Dynamic Forms with Dependent Fields

## When to Use

> You're building forms with cascading selects, conditional fields, or any form that updates based on user input without full page reload.

## Pattern: Cascading Selects

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` — Production example with type/name cascading selects

**Step 1: First Select Updates Second Select**

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

public function buildForm(array $form, FormStateInterface $form_state, string $type = '', string $name = '') {
  $form_url = Url::fromRoute('<current>');

  // First select (type)
  $form['type'] = [
    '#type' => 'select',
    '#title' => 'Type',
    '#options' => $this->getTypes(),
    '#default_value' => $type,
  ];

  // Configure HTMX to update name select when type changes
  (new Htmx())
    ->post($form_url)
    ->onlyMainContent()
    ->select('*:has(>select[name="name"])')  // What to extract from response
    ->target('*:has(>select[name="name"])')  // Where to put it
    ->swap('outerHTML')                       // Replace entire wrapper
    ->applyTo($form['type']);

  // Second select (name) - options depend on type
  $default_type = $form_state->getValue('type', $type);
  $form['name'] = [
    '#type' => 'select',
    '#title' => 'Name',
    '#options' => $this->getDependentOptions($default_type),
    '#default_value' => $name,
  ];

  return $form;
}
```

Reference: Lines 92-125 of ConfigSingleExportForm

**Step 2: Handle Trigger Detection**

```php
$trigger = $this->getHtmxTriggerName();

if ($trigger === 'type') {
  // Type changed - update name options
  $form['name']['#options'] = $this->getDependentOptions($default_type);
}
elseif ($trigger === 'name') {
  // Name selected - maybe update another region
}
```

Reference: Lines 136-138 of ConfigSingleExportForm

## Pattern: Out-of-Band (OOB) Updates

Update multiple form regions independently:

```php
// When type changes, also clear a display region
(new Htmx())
  ->swapOob('outerHTML:[data-display-wrapper]')
  ->applyTo($form['display'], '#wrapper_attributes');
```

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 141-143

## Pattern: Browser History Updates

Push URL when form selections change:

```php
if ($this->getHtmxTriggerName() === 'name') {
  $selected_name = $form_state->getValue('name');
  $push_url = Url::fromRoute('my.route', [
    'type' => $default_type,
    'name' => $selected_name,
  ]);

  (new Htmx())
    ->pushUrlHeader($push_url)
    ->applyTo($form);
}
```

Reference: Lines 157-161 of ConfigSingleExportForm

## Pattern: Automatic form_build_id Updates

FormBuilder automatically handles form_build_id for HTMX requests via OOB swap. No action needed.

Reference: `/core/lib/Drupal/Core/Form/FormBuilder.php` lines 782-790

## Common Mistakes

- Hardcoding form URLs — Use `Url::fromRoute('<current>')` or route name
- Not using `onlyMainContent()` — Results in full page responses
- Forgetting to check trigger element — Can't determine which field changed
- Not providing non-HTMX fallback — Form should POST normally without JavaScript
- Using `swap('none')` without OOB — Nothing updates (see test_htmx example using `swapOob('true')`)

## See Also

- Previous: [Request Detection](request-detection.md)
- Next: [HTMX Controllers](htmx-controllers.md)
- Reference: [Complete Production Example](production-example-config-export.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestForm.php`
