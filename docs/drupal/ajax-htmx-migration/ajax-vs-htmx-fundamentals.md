---
description: "AJAX vs HTMX Fundamentals — core architectural differences between Drupal AJAX and HTMX before starting a migration"
tldr: "Read this before starting a migration to understand the architectural differences between #ajax callbacks and the declarative Htmx class. Never mix #ajax and Htmx attributes on the same element — they conflict and HTMX is ignored."
drupal_version: "11.x"
---

# AJAX vs HTMX Fundamentals

## When to Use

> When you need to understand the core architectural differences between Drupal AJAX and HTMX before starting a migration. This is essential background for choosing the right approach.

## Decision

| If you need... | AJAX Approach | HTMX Approach | Why |
|---|---|---|---|
| Form element interaction | `#ajax` property with callback | `Htmx` class attributes | HTMX is declarative, no callback methods |
| Response format | JSON command arrays | HTML render arrays | HTMX uses server-rendered HTML |
| DOM targeting | Single wrapper ID | CSS selectors | HTMX can target multiple elements |
| JavaScript control | Command-based callbacks | Event-based triggers | HTMX is more declarative |
| Browser history | Manual handling | Built-in `pushUrl()` | HTMX integrates with history API |

## Pattern

**AJAX Approach (Legacy):**
```php
$form['field'] = [
  '#type' => 'select',
  '#ajax' => [
    'callback' => '::myCallback',
    'wrapper' => 'result-wrapper',
  ],
];

public function myCallback(array &$form, FormStateInterface $form_state) {
  return $form['result'];
}
```

**HTMX Approach (Drupal 11.3+):**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['field'] = [
  '#type' => 'select',
  // No #ajax property
];

(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->select('#result-wrapper')
  ->target('#result-wrapper')
  ->swap('outerHTML')
  ->applyTo($form['field']);

// No callback method — logic goes in buildForm()
```

Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` (class documentation)

## Common Mistakes

- **Using `#ajax` and `Htmx` together** → Choose one approach per element. They conflict and HTMX will be ignored if `#ajax` exists
- **Creating callback methods for HTMX** → HTMX rebuilds the form directly in `buildForm()`. Check `$this->getHtmxTriggerName()` instead of creating callbacks
- **Using wrapper IDs instead of CSS selectors** → HTMX targets via CSS selectors like `'#id'`, `'.class'`, `'[data-attr]'`. This is more flexible than AJAX wrapper IDs
- **Returning AjaxResponse objects** → HTMX controllers return render arrays. The `HtmxRenderer` converts them to HTML automatically
- **Forgetting to add wrapper attributes** → HTMX needs CSS-selectable targets. Use `'#wrapper_attributes'` on form elements or `'#attributes'` on containers

## See Also

- Next: [AJAX Command to HTMX Equivalents](ajax-command-to-htmx-equivalents.md) — Quick reference for converting commands
- Reference: [Drupal HTMX Change Record](https://www.drupal.org/node/3539472)
- Related: `drupal-htmx-implementation-guide.md` — Full HTMX implementation guide
