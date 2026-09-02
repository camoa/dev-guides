---
description: "Cascading Selects with URL Migration — multiple dependent selects that also keep the browser URL bookmarkable"
tldr: "Migrate chained dropdowns where each selection updates the next AND the URL. Use swapOob() to clear downstream fields and pushUrlHeader() to keep the URL in sync — without pushUrlHeader() the state isn't bookmarkable."
drupal_version: "11.x"
---

# Cascading Selects with URL Migration

## When to Use

> Migrate multiple dependent selects where each selection updates the next dropdown AND the browser URL (bookmarkable state). Common in configuration forms and filter interfaces.

## Steps

1. **Add route parameters for selections** — Make state bookmarkable
2. **Replace `#ajax` with HTMX on each select** — Each updates the next in chain
3. **Use `swapOob()` for downstream updates** — Update multiple elements in one response
4. **Use `pushUrlHeader()` for browser history** — Keep URL in sync with selections
5. **Handle route parameters as defaults** — Support direct URL access

## BEFORE: AJAX

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['type'] = [
    '#type' => 'select',
    '#title' => t('Type'),
    '#options' => $this->getTypes(),
    '#ajax' => [
      'callback' => '::updateNameOptions',
      'wrapper' => 'name-wrapper',
    ],
  ];

  $form['name'] = [
    '#type' => 'select',
    '#title' => t('Name'),
    '#options' => $this->getNameOptions($form_state->getValue('type')),
    '#prefix' => '<div id="name-wrapper">',
    '#suffix' => '</div>',
    '#ajax' => [
      'callback' => '::updateExport',
      'wrapper' => 'export-wrapper',
    ],
  ];

  $form['export'] = [
    '#type' => 'textarea',
    '#title' => t('Export'),
    '#prefix' => '<div id="export-wrapper">',
    '#suffix' => '</div>',
  ];

  if ($form_state->getValue('type') && $form_state->getValue('name')) {
    $form['export']['#value'] = $this->getExportData(
      $form_state->getValue('type'),
      $form_state->getValue('name')
    );
  }

  return $form;
}

public function updateNameOptions(array &$form, FormStateInterface $form_state) {
  return $form['name'];
}

public function updateExport(array &$form, FormStateInterface $form_state) {
  return $form['export'];
}
```

## AFTER: HTMX

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

// Add route parameters: path: '/config/export/{type}/{name}'
public function buildForm(array $form, FormStateInterface $form_state, $type = '', $name = '') {
  $form_url = Url::fromRoute('<current>');

  // First select
  $form['type'] = [
    '#type' => 'select',
    '#title' => t('Type'),
    '#options' => $this->getTypes(),
    '#default_value' => $type,
  ];

  // HTMX: POST to form, select name wrapper, update it
  (new Htmx())
    ->post($form_url)
    ->onlyMainContent()
    ->select('*:has(>select[name="name"])')
    ->target('*:has(>select[name="name"])')
    ->swap('outerHTML')
    ->applyTo($form['type']);

  // Second select
  $form['name'] = [
    '#type' => 'select',
    '#title' => t('Name'),
    '#options' => $this->getNameOptions($form_state->getValue('type', $type)),
    '#default_value' => $name,
  ];

  // HTMX: POST to form, select export wrapper, update it
  (new Htmx())
    ->post($form_url)
    ->onlyMainContent()
    ->select('[data-export-wrapper]')
    ->target('[data-export-wrapper]')
    ->swap('outerHTML')
    ->applyTo($form['name']);

  // Result area
  $form['export'] = [
    '#type' => 'textarea',
    '#title' => t('Export'),
    '#wrapper_attributes' => ['data-export-wrapper' => TRUE],
  ];

  // Handle triggering element
  $trigger = $this->getHtmxTriggerName();
  $pushUrl = FALSE;

  if ($trigger === 'type') {
    // Type changed - update name options, clear export
    $form['name']['#options'] = $this->getNameOptions($form_state->getValue('type'));

    // Clear export via out-of-band swap
    (new Htmx())
      ->swapOob('outerHTML:[data-export-wrapper]')
      ->applyTo($form['export'], '#wrapper_attributes');

    // Update URL to reflect type selection
    $pushUrl = Url::fromRoute('config.export_single', [
      'type' => $form_state->getValue('type'),
      'name' => '',
    ]);
  }
  elseif ($trigger === 'name') {
    // Name selected - update export and URL
    $selectedType = $form_state->getValue('type', $type);
    $selectedName = $form_state->getValue('name');

    $form['export']['#value'] = $this->getExportData($selectedType, $selectedName);

    $pushUrl = Url::fromRoute('config.export_single', [
      'type' => $selectedType,
      'name' => $selectedName,
    ]);
  }
  elseif ($type && $name) {
    // Initial load with route parameters
    $form['export']['#value'] = $this->getExportData($type, $name);
  }

  // Push URL to browser history
  if ($pushUrl) {
    (new Htmx())
      ->pushUrlHeader($pushUrl)
      ->applyTo($form);
  }

  return $form;
}
```

**Routing configuration:**
```yaml
config.export_single:
  path: '/admin/config/development/configuration/single/export/{config_type}/{config_name}'
  defaults:
    _form: '\Drupal\config\Form\ConfigSingleExportForm'
    config_type: ''
    config_name: ''
  requirements:
    _permission: 'export configuration'
```

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 80-180

## Common Mistakes

- **Not using `swapOob()` for clearing downstream fields** → When parent changes, clear child fields using out-of-band swaps so users see the fields reset
- **Forgetting `pushUrlHeader()`** → Without this, the URL doesn't update and users can't bookmark or share the current state
- **Not handling route parameters in defaults** → Support direct URL access by using route parameters as `#default_value` when present
- **Using simple IDs instead of attribute selectors** → Use `'*:has(>select[name="field"])'` to target the wrapper of a specific form element. More reliable than IDs
- **Not clearing intermediate selections** → When parent changes, clear or reset all downstream fields to avoid stale state

## See Also

- Previous: [Dependent Dropdown Migration](dependent-dropdown-migration.md)
- Next: [Button-Triggered Content Load Migration](button-triggered-content-load-migration.md)
- Reference: `Htmx::swapOob()` documentation in `/core/lib/Drupal/Core/Htmx/Htmx.php`
