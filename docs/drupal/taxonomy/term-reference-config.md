---
description: "Add taxonomy term reference fields to content types via config"
tldr: "Use this workflow to add taxonomy term reference fields to content types, users, or other entities using the config-first approach."
drupal_version: "11.x"
---

# Term Reference Field Configuration

## When to Use

> Use this workflow when adding taxonomy term reference fields to content types, users, or other entities.

This workflow shows the config-first approach to field creation.

## Steps

1. **Create field storage** — Defines the field's data structure (cardinality, target type)

   File: `field.storage.ENTITY_TYPE.FIELD_NAME.yml`
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
   indexes: {}
   persist_with_no_fields: false
   custom_storage: false
   ```

2. **Create field instance** — Attaches field to specific bundle with label, handler settings

   File: `field.field.ENTITY_TYPE.BUNDLE.FIELD_NAME.yml`
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

3. **Configure form display** — Set widget (autocomplete, select, checkboxes)

   File: `core.entity_form_display.ENTITY_TYPE.BUNDLE.DISPLAY_MODE.yml` (use recipe actions or UI)
   ```yaml
   # In recipe.yml actions:
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

4. **Configure view display** — Set formatter (label, rendered entity, RSS category)
   ```yaml
   # In recipe.yml or entity_view_display config:
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

- Forgetting `target_bundles` in handler_settings → Field allows terms from ALL vocabularies. Always restrict to specific vocabulary unless intentionally multi-vocab
- Setting `cardinality: 1` for tags → Users expect multiple tags. Use `-1` (unlimited) or specific number > 1 for tag-style fields
- Not enabling `auto_create: true` for tag fields → Users can't create terms on-the-fly. Set to true for tag autocomplete widgets
- Using entity reference field without target_type → Must specify `target_type: taxonomy_term` in field storage settings
- Mismatched dependencies → Field instance must depend on field storage, vocabulary, and bundle. Missing dependencies cause import failures

## See Also

- ← Previous: [Creating Vocabularies via Config](creating-vocabularies-config.md) | Next: [Hierarchical Taxonomy](hierarchical-taxonomy.md) →
- Reference: `/core/recipes/article_tags/config/field.field.node.article.field_tags.yml`
- Reference: `/core/recipes/article_tags/config/field.storage.node.field_tags.yml`
