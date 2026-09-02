---
description: "Hybrid AJAX-HTMX Approach — use AJAX and HTMX together in the same application without conflict"
tldr: "Use AJAX for specific features (dialogs, contrib) and HTMX for new form interactions in the same app. Drupal.attachBehaviors() runs after both AJAX and HTMX swaps, and Drupal.behaviors.htmx initializes HTMX attributes on AJAX-inserted content."
drupal_version: "11.x"
---

# Hybrid AJAX-HTMX Approach

## When to Use

> Use both AJAX and HTMX in the same application when you need AJAX for specific features (dialogs, contrib) but want HTMX for new form interactions. They coexist without conflict.

## Pattern

**AJAX button that inserts HTMX-enabled content:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['ajax_button'] = [
  '#type' => 'button',
  '#value' => t('Load via AJAX'),
  '#ajax' => [
    'callback' => '::ajaxCallback',
    'wrapper' => 'content-wrapper',
  ],
];

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  // Return HTMX-enabled content via AJAX
  $build = [
    '#type' => 'container',
    '#attributes' => ['id' => 'content-wrapper'],
  ];

  // HTMX button inside AJAX-inserted content
  $build['htmx_button'] = [
    '#type' => 'html_tag',
    '#tag' => 'button',
    '#value' => t('Refresh via HTMX'),
    '#attributes' => ['type' => 'button'],
  ];

  (new Htmx())
    ->get(Url::fromRoute('my_module.refresh'))
    ->target('#content-wrapper')
    ->swap('innerHTML')
    ->applyTo($build['htmx_button']);

  return $build;
}
```

**Key integration points:**

1. **Drupal behaviors work for both** — `Drupal.attachBehaviors()` runs after AJAX AND HTMX swaps
2. **HTMX processes AJAX-inserted content** — The `Drupal.behaviors.htmx` behavior initializes HTMX attributes on AJAX content
3. **Both can update same containers** — Just be careful about race conditions

Reference: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php`

## Common Mistakes

- **Using AJAX and HTMX on same element** — Choose one. If `#ajax` exists, HTMX attributes are ignored
- **Not reattaching behaviors** — Always return render arrays from AJAX callbacks so behaviors attach to new content
- **Expecting HTMX to work without behavior** — HTMX needs `Drupal.behaviors.htmx` to process `data-hx-*` attributes. It runs automatically if core HTMX library is loaded
- **Forgetting library dependencies** — AJAX needs `core/drupal.ajax`, HTMX needs `core/drupal.htmx`. Both can be on same page
- **Not testing interaction** — Test AJAX inserting HTMX content, HTMX replacing AJAX content, and both updating shared containers

## See Also

- Previous: [When NOT to Migrate](when-not-to-migrate.md)
- Next: [Migration Strategy Best Practices](migration-strategy-best-practices.md)
- Reference: Hybrid form test at `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php`
