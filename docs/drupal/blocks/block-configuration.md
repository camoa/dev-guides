---
description: Add configurable settings to block plugin instances
tldr: "Use when your block plugin needs configurable settings that site builders can set per block instance. Use content block fields instead when editors (not devs) need to manage the values."
drupal_version: "11.x"
---

# Block Configuration Forms

## When to Use

> Your block plugin needs configurable settings that site builders can set per block instance.

## Steps

1. **Define default configuration**
   ```php
   public function defaultConfiguration() {
     return [
       'show_title' => TRUE,
       'items_count' => 5,
     ] + parent::defaultConfiguration();
   }
   ```

2. **Build configuration form**
   ```php
   public function blockForm($form, FormStateInterface $form_state) {
     $form['show_title'] = [
       '#type' => 'checkbox',
       '#title' => $this->t('Show title'),
       '#default_value' => $this->configuration['show_title'],
     ];
     return $form;
   }
   ```

3. **Handle form submission**
   ```php
   public function blockSubmit($form, FormStateInterface $form_state) {
     $this->configuration['show_title'] = $form_state->getValue('show_title');
   }
   ```

4. **Use configuration in build()**
   ```php
   public function build() {
     $show = $this->configuration['show_title'];
     // Use $show to control output
   }
   ```

## Decision Points

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

- Not calling `parent::defaultConfiguration()` → Loses base settings like `label`, `label_display`
- Forgetting to add `+ parent::defaultConfiguration()` → Same as above
- Storing form values without filtering → Use `$form_state->getValue()` to get specific values
- Not validating user input → Implement `blockValidate()` for complex rules
- Changing configuration structure without update path → Breaks existing block instances; provide update hook

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Config Management & Recipes](config-recipes.md)
- Reference: https://www.drupal.org/docs/drupal-apis/form-api
