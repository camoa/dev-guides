---
description: Add taxonomy term reference fields to content types via config
drupal_version: "11.x"
---

# Term Reference Field Configuration

## When to Use

> Use this workflow to add taxonomy term reference fields to content types, users, or other entities using the config-first approach.

## Decision

| Config File | Purpose | When to Create |
|-------------|---------|----------------|
| `field.storage.ENTITY_TYPE.FIELD_NAME.yml` | Defines field's data structure (cardinality, target type) | Always first — required for field instances |
| `field.field.ENTITY_TYPE.BUNDLE.FIELD_NAME.yml` | Attaches field to specific bundle | After storage exists |
| `core.entity_form_display.*.yml` | Sets widget (autocomplete, select, checkboxes) | For edit forms |
| `core.entity_view_display.*.yml` | Sets formatter (label, rendered entity, RSS category) | For display |

## Pattern

**Field storage** (`field.storage.node.field_tags.yml`):
```yaml
langcode: en
status: true
dependencies:
  module:
    - node
    - taxonomy
id: node.field_tags
field_name: field_tags
entity_type: node
type: entity_reference
settings:
  target_type: taxonomy_term
module: core
locked: false
cardinality: -1
translatable: true
```

**Field instance** (`field.field.node.article.field_tags.yml`):
```yaml
langcode: en
status: true
dependencies:
  config:
    - field.storage.node.field_tags
    - node.type.article
    - taxonomy.vocabulary.tags
id: node.article.field_tags
field_name: field_tags
entity_type: node
bundle: article
label: Tags
description: 'Enter comma-separated tags'
required: false
translatable: true
settings:
  handler: 'default:taxonomy_term'
  handler_settings:
    target_bundles:
      tags: tags
    sort:
      field: _none
    auto_create: true
field_type: entity_reference
```

**Form display** (in recipe.yml actions):
```yaml
core.entity_form_display.node.article.default:
  setComponent:
    name: field_tags
    options:
      type: entity_reference_autocomplete_tags
      weight: 3
      settings:
        match_operator: CONTAINS
        match_limit: 10
        size: 60
        placeholder: ''
```

**View display**:
```yaml
core.entity_view_display.node.article.default:
  setComponent:
    name: field_tags
    options:
      type: entity_reference_label
      label: above
      settings:
        link: true
      weight: 10
```

## Common Mistakes

- **Wrong**: Forgetting `target_bundles` in handler_settings → **Right**: Always restrict to specific vocabulary unless intentionally multi-vocab
- **Wrong**: Setting `cardinality: 1` for tags → **Right**: Use `-1` (unlimited) or specific number > 1 for tag-style fields
- **Wrong**: Not enabling `auto_create: true` for tag fields → **Right**: Set to true for tag autocomplete widgets
- **Wrong**: Using entity reference field without target_type → **Right**: Must specify `target_type: taxonomy_term` in field storage settings
- **Wrong**: Mismatched dependencies → **Right**: Field instance must depend on field storage, vocabulary, and bundle

## See Also

- [Creating Vocabularies via Config](creating-vocabularies-config.md)
- [Hierarchical Taxonomy](hierarchical-taxonomy.md)
- Reference: `/core/recipes/article_tags/config/field.field.node.article.field_tags.yml`
- Reference: `/core/recipes/article_tags/config/field.storage.node.field_tags.yml`
