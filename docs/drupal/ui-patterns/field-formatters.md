---
description: Field formatters — rendering fields through components at items or per-item granularity
drupal_version: "10.3+ / 11"
---

## Field Formatters

**Sub-module:** `ui_patterns_field_formatters`
**Dependencies:** `ui_patterns`

### What It Does

Provides field formatter plugins that render field output through SDC components. Two formatters are available:

| Formatter | ID | Cardinality | Context |
|---|---|---|---|
| `ComponentFormatter` | `ui_patterns_component` | Multi-value (>1 or unlimited) | `field_granularity:items` |
| `ComponentFormatterSingle` | `ui_patterns_component_per_item` | Any | `field_granularity:item` |

The formatter is registered for `entity_reference` fields but is dynamically made available for **all field types** via `ui_patterns_field_formatters_field_formatter_info_alter()`.

### How It Works

1. Select "Component (UI Patterns)" as the field formatter in Manage Display
2. Choose a component from the component selector
3. Map the field's properties to component props and slots
4. The formatter builds a component render array with entity + field context

The `ComponentFormatterBase` uses `ComponentSettingsFormBuilderTrait` which provides the standard component configuration form. Context includes the entity, bundle, field items, and field index (for per-item rendering).

### Granularity: Items vs Item

- **`ComponentFormatter`** (multi-value) receives all field items at once. The component handles iteration. Best for list components (e.g., an image gallery component that receives all images).
- **`ComponentFormatterSingle`** (per-item) receives one field item at a time. Drupal iterates. Best for simple formatters where each field value gets its own component instance.

### Config YAML

Field formatter configuration is stored in the entity view display. After `drush config:export`, find it in `core.entity_view_display.{entity_type}.{bundle}.{view_mode}.yml` under the `content` key for the field:

```yaml
# In core.entity_view_display.node.article.default.yml
content:
  # Per-item formatter: each field value rendered as a card
  field_image:
    type: ui_patterns_component_per_item
    label: hidden
    settings:
      ui_patterns:
        component_id: 'ui_suite_daisyui:card'
        variant_id:
          source_id: select
          source:
            value: default
        props:
          heading_level:
            source_id: select
            source:
              value: '3'
          size:
            source_id: select
            source:
              value: md
          url:
            source_id: 'field_property:node:article:field_link'
            source:
              type: uri
        slots:
          image:
            sources:
              - source_id: 'field_property:node:article:field_image'
                source:
                  type: entity
                _weight: '0'
          title:
            sources:
              - source_id: 'field_property:node:article:title'
                source:
                  type: value
                _weight: '0'
          text:
            sources:
              - source_id: 'field_property:node:article:body'
                source:
                  type: text_processed
                _weight: '0'
    third_party_settings: {}
    weight: 0
    region: content

  # Multi-value formatter: all items passed to one component
  field_tags:
    type: ui_patterns_component
    label: above
    settings:
      ui_patterns:
        component_id: 'ui_suite_daisyui:badge'
        variant_id:
          source_id: select
          source:
            value: ''
        props: {}
        slots:
          text:
            sources:
              - source_id: 'field_property:node:article:field_tags'
                source:
                  type: entity_label
                _weight: '0'
    third_party_settings: {}
    weight: 5
    region: content
```

Key observations:
- The formatter type is `ui_patterns_component_per_item` (per-item) or `ui_patterns_component` (multi-value).
- Settings follow the standard `field.formatter.settings.ui_patterns` schema: `settings.ui_patterns` maps to `ui_patterns_component`.
- Field property source IDs follow the pattern `field_property:{entity_type}:{bundle}:{field_name}`, with the `source.type` specifying which property to extract (e.g., `value`, `uri`, `entity`, `text_processed`, `entity_label`).
- The outer `label`, `weight`, `region`, `third_party_settings` are standard Drupal field display properties.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Using multi-value formatter on single-cardinality fields | `ComponentFormatter` requires cardinality >1 or unlimited. It will not appear for single-value fields. Use `ComponentFormatterSingle` instead. |
| Expecting non-field sources in the formatter context | The formatter context is scoped to the entity + field. Global sources (menus, paths) are still available, but the primary use case is field property mapping. |

### See Also

- [Source Plugins](#source-plugins)
- Drupal Custom Field Guide