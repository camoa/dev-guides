---
description: Build Drupal forms with HTMX — cascading selects, OOB updates, and browser history management
drupal_version: "11.x"
---

# Dynamic Forms with Dependent Fields

## When to Use

> Use this when building forms with cascading selects, conditional fields, or form elements that update based on user input without full page reload.

## Decision

| Need | Pattern | Key method |
|------|---------|------------|
| First select updates second select | Cascading with `select()` + `target()` | `onlyMainContent()` |
| Update multiple regions simultaneously | Out-of-band (OOB) swap | `swapOob()` |
| Push URL as selections change | History management | `pushUrlHeader()` |
| Detect which field triggered update | Trigger detection | `getHtmxTriggerName()` |

## Pattern

**Cascading selects** (type → name):

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form_url = Url::fromRoute('<current>');

$form['type'] = [
  '#type' => 'select',
  '#title' => 'Type',
  '#options' => $this->getTypes(),
  '#default_value' => $type,
];

(new Htmx())
  ->post($form_url)
  ->onlyMainContent()
  ->select('*:has(>select[name="name"])')
  ->target('*:has(>select[name="name"])')
  ->swap('outerHTML')
  ->applyTo($form['type']);

$form['name'] = [
  '#type' => 'select',
  '#options' => $this->getDependentOptions($form_state->getValue('type', $type)),
];
```

**Trigger detection:**

```php
$trigger = $this->getHtmxTriggerName();
if ($trigger === 'type') {
  $form['name']['#options'] = $this->getDependentOptions($default_type);
}
```

**OOB update** (clear a display region when type changes):

```php
(new Htmx())
  ->swapOob('outerHTML:[data-display-wrapper]')
  ->applyTo($form['display'], '#wrapper_attributes');
```

**Browser history push:**

```php
if ($this->getHtmxTriggerName() === 'name') {
  (new Htmx())
    ->pushUrlHeader(Url::fromRoute('my.route', ['type' => $type, 'name' => $name]))
    ->applyTo($form);
}
```

`FormBuilder` automatically handles `form_build_id` for HTMX requests via OOB swap — no action needed.

## Common Mistakes

- **Wrong**: Hardcoding form URLs → **Right**: Use `Url::fromRoute('<current>')` or route name
- **Wrong**: Not using `onlyMainContent()` → **Right**: Without it, responses are full pages
- **Wrong**: Forgetting to check trigger element → **Right**: Can't determine which field changed
- **Wrong**: Not providing non-HTMX fallback → **Right**: Form should POST normally without JavaScript
- **Wrong**: Using `swap('none')` without OOB → **Right**: Nothing updates

## See Also

- [Request Detection](request-detection.md)
- [HTMX Controllers](htmx-controllers.md)
- [Production Example: ConfigSingleExportForm](production-example-config-export.md)
- Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php`
- Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestForm.php`
