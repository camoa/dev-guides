---
description: "Complete HTMX production example — ConfigSingleExportForm with cascading selects, OOB updates, and history management"
tldr: "Reference this when you want a complete, production-ready HTMX implementation demonstrating cascading selects, OOB updates, and history management — all from Drupal core's ConfigSingleExportForm."
drupal_version: "11.x"
---

# Complete Production Example: ConfigSingleExportForm

## When to Use

> You want to see a complete, production-ready HTMX implementation demonstrating cascading selects, OOB updates, and history management.

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` — Drupal core's configuration export form

## Form Structure

Two cascading selects (type → name) and an export textarea that updates based on selections.

## Implementation Patterns

**1. First Select Updates Second Select** (lines 92-107)

```php
// Config type select updates config name select
(new Htmx())
  ->post($form_url)
  ->onlyMainContent()
  ->select('*:has(>select[name="config_name"])')  // Extract wrapper from response
  ->target('*:has(>select[name="config_name"])')  // Replace wrapper in page
  ->swap('outerHTML')
  ->applyTo($form['config_type']);
```

**2. Second Select Updates Display Region** (lines 117-125)

```php
// Config name select updates export textarea
(new Htmx())
  ->post($form_url)
  ->onlyMainContent()
  ->select('[data-export-wrapper]')
  ->target('[data-export-wrapper]')
  ->swap('outerHTML')
  ->applyTo($form['config_name']);
```

**3. Out-of-Band Update** (lines 141-143)

When type changes, clear the export textarea via OOB swap:

```php
(new Htmx())
  ->swapOob('outerHTML:[data-export-wrapper]')
  ->applyTo($form['export'], '#wrapper_attributes');
```

**4. Trigger Detection** (line 137)

```php
$trigger = $this->getHtmxTriggerName();

if ($trigger == 'config_type') {
  $form = $this->updateConfigurationType($form, $form_state);
  // Clear export
  (new Htmx())
    ->swapOob('outerHTML:[data-export-wrapper]')
    ->applyTo($form['export'], '#wrapper_attributes');
  $pushUrl = Url::fromRoute('config.export_single', [
    'config_type' => $default_type,
    'config_name' => '',
  ]);
}
elseif ($trigger == 'config_name') {
  $default_name = $form_state->getValue('config_name', $config_name);
  $form['export'] = $this->updateExport($form, $default_type, $default_name);
  $pushUrl = Url::fromRoute('config.export_single', [
    'config_type' => $default_type,
    'config_name' => $default_name,
  ]);
}
```

**5. Browser History Management** (lines 157-161)

```php
if ($pushUrl) {
  (new Htmx())
    ->pushUrlHeader($pushUrl)
    ->applyTo($form);
}
```

## Key Techniques Demonstrated

- Cascading dependent form fields
- Out-of-band (OOB) swaps for multiple simultaneous updates
- Browser history push to update URL as selections change
- Trigger detection to handle different field changes
- Wrapper selector patterns using `:has()` pseudo-class
- Progressive enhancement (form POSTs normally without JavaScript)

## Common Mistakes

- Not using `:has()` selector for wrapper targeting — Direct element ID might not exist on initial load
- Forgetting to push URL — Users can't bookmark or share current state
- Not clearing dependent fields when parent changes — Old values persist incorrectly
- Missing OOB swap for related updates — Only primary target updates

## See Also

- Previous: [Production Patterns](production-patterns.md)
- Next: [Best Practices](best-practices.md)
- Reference: [Dynamic Forms](dynamic-forms.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/`
