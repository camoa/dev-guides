---
description: Form display — widget selection and field ordering in entity edit forms
drupal_version: "11.x"
---

# Form Display Configuration

## When to Use

When controlling how fields appear in entity edit forms, including widget selection, field order, and visibility across different form modes.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Standard edit form | 'default' mode | Main entity edit form |
| Inline editing | Custom form mode | Simplified field subset for quick edits |
| Different widgets | Widget type per mode | Different input methods for different contexts |
| Hide fields | hidden key | Exclude from form mode without deleting field |

## Pattern

Form display in `config/install/core.entity_form_display.node.article.default.yml`:

```yaml
langcode: en
status: true
dependencies:
  config:
    - field.field.node.article.body
    - field.field.node.article.field_tags
    - node.type.article
  module:
    - text
    - taxonomy
id: node.article.default
targetEntityType: node
bundle: article
mode: default
content:
  title:
    type: string_textfield
    weight: -5
    region: content
    settings:
      size: 60
      placeholder: ''
  body:
    type: text_textarea_with_summary
    weight: 0
    region: content
    settings:
      rows: 9
      summary_rows: 3
      placeholder: ''
  field_tags:
    type: entity_reference_autocomplete_tags
    weight: 10
    region: content
    settings:
      match_operator: CONTAINS
      match_limit: 10
      size: 60
      placeholder: ''
hidden:
  created: true
  uid: true
  promote: true
  sticky: true
```

**Key properties**:
- `type`: Widget plugin ID
- `weight`: Display order (lower = higher)
- `region`: Display region (content, footer, etc.)
- `settings`: Widget-specific configuration

Reference: `/core/lib/Drupal/Core/Entity/EntityDisplayRepository.php`

## Common Mistakes

- **Wrong**: Forgetting module dependencies → **Right**: Missing widgets; form display breaks
- **Wrong**: Not setting weights → **Right**: Fields appear in arbitrary order
- **Wrong**: Using wrong widget type → **Right**: Widget not compatible with field type; form breaks
- **Wrong**: Missing field in hidden or content → **Right**: Field shows in default position; no explicit control
- **Wrong**: Hardcoding settings in forms → **Right**: Use form display config; makes site-builder configurable

**Performance**:
- Heavy widgets (WYSIWYG, media library) slow form rendering. Only include when needed.
- Use form modes to create lightweight forms for specific tasks.

**Development Standards**:
- Always set weights explicitly for predictable ordering
- Use proper dependency declarations for config management
- Test form modes across different browsers and devices

## See Also

- [Field Formatter Development](field-formatter-development.md)
- [View Display Configuration](view-display-configuration.md)
- Reference: [Entity form display](https://www.drupal.org/docs/drupal-apis/entity-api/structure-of-a-field)
