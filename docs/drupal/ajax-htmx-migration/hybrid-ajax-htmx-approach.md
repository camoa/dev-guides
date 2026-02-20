---
description: Use AJAX and HTMX together in the same application — coexistence patterns, library dependencies, and integration points
drupal_version: "11.x"
---

# Hybrid AJAX-HTMX Approach

## When to Use

> Use both AJAX and HTMX in the same application when you need AJAX for specific features (dialogs, contrib) but want HTMX for new form interactions. They coexist without conflict.

## Decision

| Scenario | Approach |
|---|---|
| AJAX inserts HTMX-enabled content | Return render array from AJAX callback; HTMX initializes on new content via `Drupal.behaviors.htmx` |
| HTMX replaces AJAX content | Target the AJAX wrapper ID with HTMX `target()` |
| Both update same container | Use carefully — avoid race conditions |
| New features in existing AJAX forms | Add new elements with HTMX; leave existing AJAX elements unchanged |

## Pattern

**AJAX button that inserts HTMX-enabled content:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['ajax_button'] = [
  '#type' => 'button',
  '#value' => t('Load via AJAX'),
  '#ajax' => ['callback' => '::ajaxCallback', 'wrapper' => 'content-wrapper'],
];

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $build = ['#type' => 'container', '#attributes' => ['id' => 'content-wrapper']];

  // HTMX button inside AJAX-inserted content
  $build['htmx_button'] = ['#type' => 'html_tag', '#tag' => 'button', '#value' => t('Refresh via HTMX'), '#attributes' => ['type' => 'button']];

  (new Htmx())
    ->get(Url::fromRoute('my_module.refresh'))
    ->target('#content-wrapper')
    ->swap('innerHTML')
    ->applyTo($build['htmx_button']);

  return $build;
}
```

**Key integration points:**

- `Drupal.attachBehaviors()` runs after both AJAX and HTMX swaps
- `Drupal.behaviors.htmx` initializes HTMX attributes on AJAX-inserted content
- Both systems can update the same containers — avoid concurrent requests to the same target

**Library dependencies:**
```yaml
# AJAX needs:
core/drupal.ajax
# HTMX needs:
core/drupal.htmx
# Both can be loaded on the same page
```

## Common Mistakes

- **Using AJAX and HTMX on the same element** → Choose one. If `#ajax` exists on an element, HTMX attributes are ignored
- **Not returning render arrays from AJAX callbacks** → Always return render arrays so `Drupal.attachBehaviors()` runs and HTMX initializes
- **Expecting HTMX without the library** → HTMX needs `core/drupal.htmx` to be loaded. It does not self-initialize
- **Forgetting library dependencies** → Both `core/drupal.ajax` and `core/drupal.htmx` can be on the same page
- **Not testing interaction** → Test: AJAX inserting HTMX content, HTMX replacing AJAX content, both updating shared containers

## See Also

- Previous: [When NOT to Migrate](when-not-to-migrate.md)
- Next: [Migration Strategy Best Practices](migration-strategy-best-practices.md)
- Source: `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php`
