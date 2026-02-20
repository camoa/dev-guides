---
description: Complete HTMX production example — ConfigSingleExportForm with cascading selects, OOB updates, and history management
drupal_version: "11.x"
---

# Production Example: ConfigSingleExportForm

## When to Use

> Reference this when you want a complete, production-ready HTMX implementation demonstrating cascading selects, OOB updates, and history management — all from Drupal core.

## Decision

| Technique | Where used | Key method |
|-----------|-----------|-----------|
| Cascading selects | type → name | `select('*:has(>select[name="name"])')` |
| OOB update | Clear export on type change | `swapOob('outerHTML:[data-export-wrapper]')` |
| Trigger detection | Route different field changes | `getHtmxTriggerName()` |
| History push | Update URL as selections change | `pushUrlHeader($url)` |

## Pattern

**1. First select updates second select** (lines 92-107):

```php
(new Htmx())
  ->post($form_url)
  ->onlyMainContent()
  ->select('*:has(>select[name="config_name"])')
  ->target('*:has(>select[name="config_name"])')
  ->swap('outerHTML')
  ->applyTo($form['config_type']);
```

**2. Second select updates display region** (lines 117-125):

```php
(new Htmx())
  ->post($form_url)
  ->onlyMainContent()
  ->select('[data-export-wrapper]')
  ->target('[data-export-wrapper]')
  ->swap('outerHTML')
  ->applyTo($form['config_name']);
```

**3. Trigger detection + OOB clear + history push** (lines 136-161):

```php
$trigger = $this->getHtmxTriggerName();

if ($trigger == 'config_type') {
  (new Htmx())
    ->swapOob('outerHTML:[data-export-wrapper]')
    ->applyTo($form['export'], '#wrapper_attributes');
  $pushUrl = Url::fromRoute('config.export_single', ['config_type' => $default_type, 'config_name' => '']);
}
elseif ($trigger == 'config_name') {
  $form['export'] = $this->updateExport($form, $default_type, $default_name);
  $pushUrl = Url::fromRoute('config.export_single', ['config_type' => $default_type, 'config_name' => $default_name]);
}

if ($pushUrl) {
  (new Htmx())->pushUrlHeader($pushUrl)->applyTo($form);
}
```

## Common Mistakes

- **Wrong**: Not using `:has()` selector for wrapper targeting → **Right**: Direct element ID might not exist on initial load
- **Wrong**: Forgetting to push URL → **Right**: Users can't bookmark or share current state
- **Wrong**: Not clearing dependent fields when parent changes → **Right**: Old values persist incorrectly
- **Wrong**: Missing OOB swap for related updates → **Right**: Only primary target updates

## See Also

- [Production Patterns](production-patterns.md)
- [Best Practices](best-practices.md)
- [Dynamic Forms](dynamic-forms.md)
- Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php`
- Reference: `/core/modules/system/tests/modules/test_htmx/`
