---
description: "Methods for attaching JavaScript libraries via PHP render arrays and hooks"
tldr: "Choose where to attach a library via #attached based on scope: global (hooks), form-specific (form arrays), template-specific (preprocess), or element-specific (render elements). Gotcha: drupal_add_js() was removed in Drupal 8+."
drupal_version: "11.x"
---

# Library Attachment Methods

## When to Use

> Choosing how to attach libraries to pages based on context and conditions.

## Decision

Libraries attach via PHP render arrays using `#attached` property. Choose attachment location based on scope: global (hooks), form-specific (form arrays), template-specific (preprocess), or element-specific (render elements).

## Pattern

**Theme/preprocess attachment**:
```php
function theme_preprocess_page(&$variables) {
  $variables['#attached']['library'][] = 'module/feature';
}
```

**Form attachment**:
```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['#attached']['library'][] = 'module/form-enhancement';
  return $form;
}
```

**Render element attachment**:
```php
$build['element'] = [
  '#markup' => '<div class="enhanced"></div>',
  '#attached' => [
    'library' => ['module/element-behavior'],
  ],
];
```

**Controller/route attachment**:
```php
public function content() {
  return [
    '#markup' => '<div>Content</div>',
    '#attached' => ['library' => ['module/page-feature']],
  ];
}
```

## Common Mistakes

- **Attaching globally when conditional loading better** - WHY: Unnecessary JS on every page, poor performance
- **Using drupal_add_js()** - WHY: Drupal 7 API, removed in Drupal 8+
- **Attaching in .info.yml globally** - WHY: No conditional control, loads everywhere regardless of need
- **Multiple attachments of same library** - WHY: Drupal deduplicates automatically, indicates architectural issue

## See Also

- [Conditional Loading](conditional-loading.md) - When to attach libraries
- [drupalSettings](drupal-settings.md) - Passing data with library attachment
