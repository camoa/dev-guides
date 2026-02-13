---
description: Add action links (Edit, Delete) to table rows with operations render element
drupal_version: "11.x"
---

# Operations Implementation

## When to Use

> Use #type operations when adding action links (Edit, Delete, etc.) to table rows in FormBase or customizing operations in ListBuilder.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Standard dropbutton (Edit, Delete) | #type operations | Core rendering, theme integration |
| Modal dialog operations | #type operations + attributes | data-dialog-type attribute triggers modal |
| AJAX operations | #type operations + use-ajax class | Loads operation in AJAX callback |
| Prevent FOUC | CSS visibility hidden + .js override | Dropbutton JS takes time to load |

## Pattern

**FormBase Operations**:
```php
$operations = [];

$operations['edit'] = [
  'title' => $this->t('Edit'),
  'url' => Url::fromRoute('mymodule.item.edit', ['id' => $item_id]),
];

$operations['delete'] = [
  'title' => $this->t('Delete'),
  'url' => Url::fromRoute('mymodule.item.delete', ['id' => $item_id]),
  'attributes' => ['data-dialog-type' => 'modal'], // Opens in modal
];

$row['operations'] = [
  '#type' => 'operations',
  '#links' => $operations,
  '#prefix' => '<div class="mymodule-dropbutton">',
  '#suffix' => '</div>',
];

$form['#attached']['library'][] = 'mymodule/admin'; // Load CSS
```

**CSS** (css/mymodule.admin.css):
```css
/* Prevent flash of unstyled content (FOUC) */
.mymodule-dropbutton .dropbutton-wrapper {
  visibility: hidden;
  min-width: 100px;
}

/* Show after JavaScript loads */
.js .mymodule-dropbutton .dropbutton-wrapper {
  visibility: visible;
}
```

**Library** (mymodule.libraries.yml):
```yaml
admin:
  css:
    theme:
      css/mymodule.admin.css: {}
  dependencies:
    - core/dropbutton
```

**ListBuilder Operations**:
```php
public function getDefaultOperations(EntityInterface $entity) {
  $operations = parent::getDefaultOperations($entity);

  $operations['custom'] = [
    'title' => $this->t('Custom Action'),
    'url' => $entity->toUrl('custom'),
    'weight' => 10, // Controls order
  ];

  return $operations;
}
```

## Common Mistakes

- **Wrong**: Using #markup with <a> tags → **Right**: No theme integration, no AJAX/modal support
- **Wrong**: Not preventing FOUC with CSS → **Right**: Ugly flash before dropbutton renders
- **Wrong**: Not attaching library to form → **Right**: CSS won't load
- **Wrong**: Not depending on core/dropbutton → **Right**: Dropbutton JS won't load
- **Wrong**: Using hard-coded paths instead of Url::fromRoute() → **Right**: Breaks with path aliases

## See Also

- [FormBase Pattern](formbase-pattern.md)
- [ListBuilder Pattern](listbuilder-pattern.md)
- [Security Best Practices](security-best-practices.md)
- Reference: modules/contrib/webform/css/webform.admin.css
- Reference: modules/contrib/entity_browser/src/Form/WidgetsConfig.php
