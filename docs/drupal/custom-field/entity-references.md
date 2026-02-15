---
description: Configuring and using entity reference sub-fields with autocomplete, select, radios, and hierarchical widgets.
---

# Entity Reference Sub-Fields

## When to Use

You need to reference entities (taxonomy terms, nodes, users, media) from within a custom field column.

## Pattern

**Configuration**:

```yaml
columns:
  category:
    name: category
    type: entity_reference
    target_type: taxonomy_term
```

**Widget configuration** (field settings):

```php
$settings['field_settings']['category'] = [
  'widget' => 'entity_reference_autocomplete',
  'widget_settings' => [
    'match_operator' => 'CONTAINS',
    'match_limit' => 10,
    'size' => 60,
    'placeholder' => 'Start typing...',
  ],
  // Handler settings filter by bundle, sort
  'handler_settings' => [
    'target_bundles' => ['tags', 'categories'],
    'sort' => ['field' => '_none'],
    'auto_create' => FALSE,
  ],
];
```

**Access in code**:

```php
$term_id = $node->field_custom->category;
$term = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->load($term_id);
```

## Decision

| Widget | When to Use | Settings |
|---|---|---|
| EntityReferenceAutocompleteWidget | Many entities (>20), search needed | match_operator, match_limit, size, placeholder |
| EntityReferenceSelectWidget | Few entities (<20), simple selection | None |
| EntityReferenceRadiosWidget | 2-10 entities, all visible | None |
| HierarchicalSelectWidget | Hierarchical taxonomy, drill-down needed | None |

## Common Mistakes

- **Not configuring handler_settings** -- Without target_bundles, all bundles of target entity type allowed
- **Forgetting access checks in formatter** -- Entity reference doesn't enforce access; check before rendering
- **Using autocomplete for small sets** -- Select or radios better UX for <20 entities
- **Not handling deleted entities** -- If referenced entity deleted, field value is dangling ID; check entity loads before rendering

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/EntityReferenceAutocompleteWidget.php`
