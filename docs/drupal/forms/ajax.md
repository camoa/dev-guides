---
description: AJAX in forms — dynamic updates without full page reload
drupal_version: "11.x"
---

# AJAX

## When to Use

> Use AJAX when a form element change should update part of the form without a full page reload. Use `#ajax` on the trigger element and return the updated portion.

## Decision

| Situation | Use | Why |
|-----------|-----|-----|
| Dropdown changes available options below | `#ajax` callback | Partial form rebuild |
| Show/hide fields based on selection | `#ajax` callback | Dynamic form sections |
| Real-time validation feedback | `#ajax` callback | Validate as user types |
| Full form submit | Normal submit | No AJAX needed |
| Complex page interaction | Consider HTMX | Simpler for non-form use cases |

## Pattern: Basic AJAX Callback

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['country'] = [
    '#type' => 'select',
    '#title' => $this->t('Country'),
    '#options' => $this->getCountries(),
    '#ajax' => [
      'callback' => '::updateRegions',
      'wrapper' => 'region-wrapper',
    ],
  ];

  $country = $form_state->getValue('country', 'us');
  $form['region'] = [
    '#type' => 'select',
    '#title' => $this->t('Region'),
    '#options' => $this->getRegions($country),
    '#prefix' => '<div id="region-wrapper">',
    '#suffix' => '</div>',
  ];

  return $form;
}

public function updateRegions(array &$form, FormStateInterface $form_state) {
  return $form['region'];
}
```

## Key Rules

| Rule | Detail |
|------|--------|
| `wrapper` must match | The `#ajax` wrapper ID must match the `id` in `#prefix`/`#suffix` |
| Callback returns renderable | Return the form element to replace, not a string |
| Use `::method` syntax | Double-colon for same-class callbacks |
| Rebuild happens automatically | Drupal rebuilds the form before calling the callback |

## Pattern: AjaxResponse with Commands

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;
use Drupal\Core\Ajax\MessageCommand;

public function ajaxSubmit(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  if ($form_state->hasAnyErrors()) {
    $response->addCommand(new MessageCommand($this->t('Fix errors.'), NULL, ['type' => 'error']));
  }
  else {
    $response->addCommand(new ReplaceCommand('#result', $result_markup));
  }
  return $response;
}
```

## Common Mistakes

- **Wrong**: Mismatched `wrapper` ID and element `id` (nothing updates)
- **Wrong**: Returning a string instead of a render array (broken output)
- **Wrong**: Forgetting `#prefix`/`#suffix` with wrapper div (no target to replace)
- **Right**: Always check `$form_state->getValue()` with a default for initial load

## See Also

- [FormBase](form-base.md) — base form pattern
- [Validation](validation.md) — adding validation
