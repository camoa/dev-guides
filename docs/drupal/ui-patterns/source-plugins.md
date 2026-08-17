---
description: "Source plugins — widgets, API sources, and context-switcher sources for component props/slots in UI Patterns 2"
tldr: "Source plugins bridge Drupal data (entity fields, menus, user input) to component props/slots. Three categories — widgets (direct input), API sources (Drupal data), and context switchers (entity_field, entity_reference) that unlock sibling-field sources via a mandatory 3-level colon-keyed YAML nesting."
drupal_version: "11.x"
---

# Source Plugins

## When to Use

> Use source plugins whenever you need to map Drupal data to a component prop or slot. Use context switchers (`entity_field`, `entity_reference`) when you need data from a field that is not the formatter's trigger field.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Manual text/number/boolean input | Widget source (`textfield`, `number`, `checkbox`) | Stores value directly in config |
| Entity field value (same entity, same field) | `field_property:{entity_type}:{field_name}:{column}` | Derived source, no nesting needed |
| Sibling field on same entity (per-item formatter) | `entity_field` context switcher | Scopes context to that field, then nest inner source |
| Referenced entity's fields | `entity_reference` context switcher | Follows the reference, then nest sources |
| Field rendered via a formatter (image, file) | `field_formatter` as inner source inside `entity_field` | Returns renderable slot output |

## Pattern

### Built-in Source Plugins

| Source ID | Category | Prop Types | Context Required | Description |
|---|---|---|---|---|
| `textfield` | Widget | string, identifier | No | Single-line text input |
| `number` | Widget | number | No | Numeric input |
| `checkbox` | Widget | boolean | No | Boolean toggle |
| `select` | Widget | enum | No | Dropdown select |
| `selects` | Widget | enum_list | No | Multiple select |
| `checkboxes` | Widget | enum_set | No | Checkbox group |
| `url` | Widget | url | No | URL input field |
| `attributes` | Widget | attributes | No | Key-value attribute pairs |
| `class_attribute` | Widget | attributes | No | CSS class input |
| `list_textarea` | Widget | list | No | Multi-line list input |
| `wysiwyg` | Widget | slot | No | CKEditor rich text |
| `component` | Source | slot | No | Nested SDC component |
| `block` | Source | slot | No | Drupal block plugin |
| `menu` | Source | links | No | Menu tree |
| `breadcrumb` | Source | links | No | Breadcrumb trail |
| `path` | Source | url, string | No | Current path |
| `token` | Source | string | Entity (optional) | Token replacement |
| `field_property` | Source | (derived) | Entity + Field | Entity field property value |
| `field_formatter` | Source | slot | Entity + Field | Field rendered through formatter |
| `field_label` | Source | string | Entity + Field | Field label text |
| `entity_link` | Source | url, links | Entity | Entity canonical/edit URLs |
| `entity_field` | Source | slot | Entity + Field | Context switcher — field on same entity |
| `entity_reference` | Source | (derived) | Entity + Field | Context switcher — follows reference |

### Context Switcher Sources (`entity_field`, `entity_reference`)

Context switchers don't return values — they change the active context so inner sources can read data from a different field. The structure is **3 levels deep** with an unusual colon-keyed middle nesting that must exactly match `derivable_context`:

```yaml
slots:
  label:
    sources:
      - source_id: entity_field
        source:
          # Level 1: which field to switch context to
          derivable_context: 'field:block_content:hero:field_label'
          # Level 2: key MUST equal derivable_context value (quote it — contains colons)
          'field:block_content:hero:field_label':
            value:
              # Level 3: actual source that produces the value
              sources:
                - source_id: 'field_property:block_content:field_label:value'
                  source:
                    type: value
                  _weight: '0'
        _weight: '0'
```

For image/file fields that need rendered output, use `field_formatter` as the inner source:

```yaml
slots:
  image:
    sources:
      - source_id: entity_field
        source:
          derivable_context: 'field:block_content:hero:field_image'
          'field:block_content:hero:field_image':
            value:
              sources:
                - source_id: 'field_formatter:block_content:field_image'
                  source:
                    type: responsive_image
                    formatter:
                      responsive_image_style: hero_responsive
                  _weight: '0'
        _weight: '0'
```

`entity_reference` uses the same 3-level structure: pick the reference field, repeat the colon-key, then nest sources that read from the referenced entity.

## Common Mistakes

- **Wrong**: Omitting the colon-keyed middle nesting in `entity_field` → **Right**: The literal `'field:entity_type:bundle:field_name'` key is required. Without it, the inner source is never reached and the slot renders empty.
- **Wrong**: Configuring `entity_field` by hand from scratch → **Right**: Configure via Manage Display first, export, then study the YAML.
- **Wrong**: Expecting field sources without entity context → **Right**: Field-based sources only appear when entity context is available (Layout Builder, field formatters, Views with entity base).
- **Wrong**: Mixing UI Patterns prop type IDs with JSON Schema types → **Right**: Source `prop_types` are UI Patterns IDs (`string`, `url`, `boolean`), not JSON Schema types.

## See Also

- [Field Formatters](field-formatters.md) — Source Scoping in Per-Item Formatters
- [Variants](variants.md) — Per-Instance Variants in Layout Builder
- [Creating Custom Source Plugins](creating-custom-source-plugins.md)
- Reference: `ui_patterns/src/Plugin/UiPatterns/Source/`
