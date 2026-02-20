---
description: Add configurable settings to block plugin instances
drupal_version: "11.x"
---

# Block Configuration Forms

## When to Use

> Use when your block plugin needs configurable settings that site builders can set per block instance. Use content block fields instead when editors (not devs) need to manage the values.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 1 (defaults) | Configuration is complex | Use nested arrays, document structure |
| Step 2 (form) | Need validation | Implement `blockValidate($form, $form_state)` |
| Step 2 (form) | Settings affect caching | Update `getCacheContexts()` or `getCacheTags()` |
| Step 3 (submit) | Values need transformation | Process in `blockSubmit()` before storing |

## Pattern

Complete configuration example:

```php
public function defaultConfiguration() {
  return [
    'items_count' => 10,
    'show_images' => TRUE,
  ] + parent::defaultConfiguration();
}

public function blockForm($form, FormStateInterface $form_state) {
  $form['items_count'] = [
    '#type' => 'number',
    '#title' => $this->t('Number of items'),
    '#default_value' => $this->configuration['items_count'],
    '#min' => 1,
    '#max' => 50,
  ];
  $form['show_images'] = [
    '#type' => 'checkbox',
    '#title' => $this->t('Show images'),
    '#default_value' => $this->configuration['show_images'],
  ];
  return $form;
}

public function blockSubmit($form, FormStateInterface $form_state) {
  $this->configuration['items_count'] = $form_state->getValue('items_count');
  $this->configuration['show_images'] = $form_state->getValue('show_images');
}
```

**Reference:** `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` (lines 60-140)

## Common Mistakes

- **Wrong**: Not calling `parent::defaultConfiguration()` → **Right**: Loses base settings like `label`, `label_display`
- **Wrong**: Forgetting `+ parent::defaultConfiguration()` → **Right**: Same as above
- **Wrong**: Storing form values without filtering → **Right**: Use `$form_state->getValue()` to get specific values
- **Wrong**: Not validating user input → **Right**: Implement `blockValidate()` for complex rules
- **Wrong**: Changing configuration structure without update path → **Right**: Breaks existing block instances; provide update hook

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Config Management & Recipes](config-recipes.md)
- Reference: https://www.drupal.org/docs/drupal-apis/form-api
