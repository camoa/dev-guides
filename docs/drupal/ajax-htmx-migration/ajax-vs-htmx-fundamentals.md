---
description: Core architectural differences between Drupal AJAX API and HTMX — choose the right approach before migrating
drupal_version: "11.x"
---

# AJAX vs HTMX Fundamentals

## When to Use

> Use AJAX when you need command sequences, modal dialogs, or contrib integration. Use HTMX when you want declarative form interactions, CSS selector targeting, or built-in browser history support.

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

## Common Mistakes

- **Using `#ajax` and `Htmx` together** → Choose one approach per element. They conflict and HTMX will be ignored if `#ajax` exists
- **Creating callback methods for HTMX** → HTMX rebuilds the form directly in `buildForm()`. Check `$this->getHtmxTriggerName()` instead of creating callbacks
- **Using wrapper IDs instead of CSS selectors** → HTMX targets via CSS selectors like `'#id'`, `'.class'`, `'[data-attr]'`. More flexible than AJAX wrapper IDs
- **Returning AjaxResponse objects** → HTMX controllers return render arrays. The `HtmxRenderer` converts them to HTML automatically
- **Forgetting to add wrapper attributes** → HTMX needs CSS-selectable targets. Use `'#wrapper_attributes'` on form elements or `'#attributes'` on containers

## See Also

- Next: [AJAX Command to HTMX Equivalents](ajax-command-to-htmx-equivalents.md)
- Reference: [Drupal HTMX Change Record](https://www.drupal.org/node/3539472)
- Source: `/core/lib/Drupal/Core/Htmx/Htmx.php`
- Related: [Drupal HTMX guides](../htmx/index.md)
