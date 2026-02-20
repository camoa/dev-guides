---
description: Migrate multiple dependent selects with browser URL sync — bookmarkable state via pushUrlHeader and swapOob
drupal_version: "11.x"
---

# Cascading Selects with URL Migration

## When to Use

> Use this when migrating multiple dependent selects where each selection updates the next dropdown AND the browser URL (bookmarkable state).

## Decision

| Step | Action |
|---|---|
| 1 | Add route parameters for each selection to make state bookmarkable |
| 2 | Replace `#ajax` with `Htmx` on each select — each updates the next in chain |
| 3 | Use `swapOob()` for downstream updates when parent changes |
| 4 | Use `pushUrlHeader()` to keep browser history in sync |
| 5 | Handle route parameters as `#default_value` for direct URL access |

## Pattern

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

// Route: path: '/config/export/{type}/{name}'
public function buildForm(array $form, FormStateInterface $form_state, $type = '', $name = '') {
  $form_url = Url::fromRoute('<current>');

  $form['type'] = ['#type' => 'select', '#options' => $this->getTypes(), '#default_value' => $type];
  (new Htmx())
    ->post($form_url)->onlyMainContent()
    ->select('*:has(>select[name="name"])')
    ->target('*:has(>select[name="name"])')
    ->swap('outerHTML')
    ->applyTo($form['type']);

  $form['name'] = ['#type' => 'select', '#options' => $this->getNameOptions($form_state->getValue('type', $type)), '#default_value' => $name];
  (new Htmx())
    ->post($form_url)->onlyMainContent()
    ->select('[data-export-wrapper]')->target('[data-export-wrapper]')
    ->swap('outerHTML')
    ->applyTo($form['name']);

  $form['export'] = ['#type' => 'textarea', '#wrapper_attributes' => ['data-export-wrapper' => TRUE]];

  $trigger = $this->getHtmxTriggerName();
  $pushUrl = FALSE;

  if ($trigger === 'type') {
    $form['name']['#options'] = $this->getNameOptions($form_state->getValue('type'));
    (new Htmx())->swapOob('outerHTML:[data-export-wrapper]')->applyTo($form['export'], '#wrapper_attributes');
    $pushUrl = Url::fromRoute('config.export_single', ['type' => $form_state->getValue('type'), 'name' => '']);
  }
  elseif ($trigger === 'name') {
    $selectedType = $form_state->getValue('type', $type);
    $selectedName = $form_state->getValue('name');
    $form['export']['#value'] = $this->getExportData($selectedType, $selectedName);
    $pushUrl = Url::fromRoute('config.export_single', ['type' => $selectedType, 'name' => $selectedName]);
  }
  elseif ($type && $name) {
    $form['export']['#value'] = $this->getExportData($type, $name);
  }

  if ($pushUrl) {
    (new Htmx())->pushUrlHeader($pushUrl)->applyTo($form);
  }
  return $form;
}
```

**Routing:**
```yaml
config.export_single:
  path: '/admin/config/development/configuration/single/export/{config_type}/{config_name}'
  defaults:
    _form: '\Drupal\config\Form\ConfigSingleExportForm'
    config_type: ''
    config_name: ''
```

## Common Mistakes

- **Not using `swapOob()` for clearing downstream fields** → When parent changes, clear child fields via out-of-band swaps to avoid stale state
- **Forgetting `pushUrlHeader()`** → Without this, the URL doesn't update and users can't bookmark the current state
- **Not handling route parameters in defaults** → Use route parameters as `#default_value` to support direct URL access
- **Using simple IDs instead of attribute selectors** → Use `'*:has(>select[name="field"])'` to reliably target a form element's wrapper
- **Not clearing intermediate selections** → When parent changes, reset all downstream fields

## See Also

- Previous: [Dependent Dropdown Migration](dependent-dropdown-migration.md)
- Next: [Button-Triggered Content Load Migration](button-triggered-content-load-migration.md)
- Source: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 80–180
- Reference: `Htmx::swapOob()` at `/core/lib/Drupal/Core/Htmx/Htmx.php`
