---
description: Methods for attaching JavaScript libraries via PHP render arrays and hooks
drupal_version: "10.x/11.x"
---

# Library Attachment Methods

## When to Use

> Use when deciding how to attach libraries to pages based on context and conditions.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Global site feature | Theme preprocess hook | Applies to all pages of that template type |
| Form-specific enhancement | Form buildForm method | Scoped to that form only |
| Template-specific feature | Preprocess for that template | Controlled per template type |
| Element-specific behavior | Render element `#attached` | Tightly coupled to element |
| Controller/route response | Controller return array | Associated with that route |

Libraries attach via PHP render arrays using `#attached` property. Choose attachment location based on scope.

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

- **Wrong**: Attaching globally when conditional loading better → **Right**: Use conditional attachment
  - **Why**: Unnecessary JS on every page, poor performance
- **Wrong**: Using drupal_add_js() → **Right**: Use `#attached` render array property
  - **Why**: Drupal 7 API, removed in Drupal 8+
- **Wrong**: Attaching in .info.yml globally → **Right**: Use conditional PHP attachment
  - **Why**: No conditional control, loads everywhere regardless of need
- **Wrong**: Multiple attachments of same library → **Right**: Review architecture
  - **Why**: Drupal deduplicates automatically, indicates architectural issue

## See Also

- [Conditional Loading](conditional-loading.md) - When to attach libraries
- [drupalSettings](drupal-settings.md) - Passing data with library attachment
