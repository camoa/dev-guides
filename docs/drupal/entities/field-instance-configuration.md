---
description: Field instance — bundle-specific field settings and configuration
drupal_version: "11.x"
---

# Field Instance Configuration

## When to Use

When attaching a field storage to a specific bundle with bundle-specific settings (label, description, required status, default values, widget/formatter settings).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Required field | required: true | Force users to provide value before saving |
| Optional field | required: false | Allow empty values |
| Default value | default_value | Static default (array of values) |
| Dynamic default | default_value_callback | Callback function for computed defaults |
| Field help text | description | Guide users on expected input |
| Bundle-specific settings | settings | Override storage settings per bundle |

## Pattern

Field instance in `config/install/field.field.node.article.field_tags.yml`:

```yaml
langcode: en
status: true
dependencies:
  config:
    - field.storage.node.field_tags
    - node.type.article
    - taxonomy.vocabulary.tags
  module:
    - taxonomy
id: node.article.field_tags
field_name: field_tags
entity_type: node
bundle: article
label: 'Tags'
description: 'Enter comma-separated tags. Example: Drupal, PHP, Web Development'
required: false
translatable: true
default_value: []
default_value_callback: ''
settings:
  handler: 'default:taxonomy_term'
  handler_settings:
    target_bundles:
      tags: tags
    sort:
      field: name
      direction: asc
    auto_create: true           # Create new terms on the fly
    auto_create_bundle: ''
field_type: entity_reference
```

**Dependencies** are critical:
- `config`: Field storage, bundle, referenced entities (vocabularies, etc.)
- `module`: Modules providing handlers or functionality

Reference: `/core/modules/field/src/Entity/FieldConfig.php`

## Common Mistakes

- **Wrong**: Missing config dependencies → **Right**: Broken installs when dependencies not present
- **Wrong**: Hardcoding default_value instead of using callback → **Right**: Static values don't respect current user/date/context
- **Wrong**: Not translating field instances → **Right**: Even if storage is translatable, instances need translatable: true
- **Wrong**: Wrong handler settings → **Right**: Entity reference handlers vary by target type; check available options
- **Wrong**: Skipping description → **Right**: Content creators need guidance; always add helpful descriptions
- **Wrong**: Setting auto_create without validation → **Right**: Users can spam new terms; consider approval workflow

**Security**:
- auto_create: true on entity_reference allows users to create entities. Validate permissions carefully.
- Entity reference handlers MUST validate access. Use 'default' handler with target_bundles restriction.
- Never allow unrestricted entity reference. Always set target_bundles to limit scope.

**Performance**:
- Limit handler_settings.sort operations. Sorting large vocabularies is expensive.
- Use Views-based selection handler for complex filtering instead of loading all options.

## See Also

- [Field Storage Configuration](field-storage-configuration.md)
- [Custom Field Type Development](custom-field-type-development.md)
- Reference: [Field configuration](https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters)
