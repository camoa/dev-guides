---
description: "Field formatters — rendering fields through components at items or per-item granularity"
tldr: "Two formatters — ui_patterns_component (multi-value) and ui_patterns_component_per_item (per-item). Per-item scopes sources to the trigger field only; reach sibling fields via entity_field context switcher. field_property source IDs are field_property:{entity_type}:{field_name}:{column} — no bundle segment. For 5+ slots reading different fields, Twig include() is often cleaner."
drupal_version: "11.x"
---

# Field Formatters

## When to Use

> Use `ui_patterns_component_per_item` when a single field value should render as one component instance. Use `ui_patterns_component` when all field items should be passed to one component. Use Twig `include()` instead when the component reads 5+ sibling fields — the 3-level `entity_field` nesting per slot becomes hard to maintain.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Single field value → one component instance | `ui_patterns_component_per_item` | Per-item granularity; Drupal iterates |
| All field values → one component | `ui_patterns_component` | Multi-value; component handles iteration |
| Single-cardinality field | `ui_patterns_component_per_item` | Multi-value formatter won't appear for cardinality = 1 |
| Component reads 5+ sibling fields | Twig `include()` pattern | Each slot needs `entity_field` 3-level nesting; block template is cleaner |
| Per-instance variants needed | Twig `include()` pattern | Formatters cannot read LB block `configuration` array |

## Pattern

Field formatter configuration lives in `core.entity_view_display.{entity_type}.{bundle}.{view_mode}.yml`:

```yaml
content:
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
          url:
            source_id: 'field_property:node:field_link:uri'
            source:
              type: uri
        slots:
          title:
            sources:
              - source_id: 'field_property:node:title:value'
                source:
                  type: value
                _weight: '0'
          # Sibling field — requires entity_field context switcher:
          body:
            sources:
              - source_id: entity_field
                source:
                  derivable_context: 'field:node:article:body'
                  'field:node:article:body':
                    value:
                      sources:
                        - source_id: 'field_property:node:body:value'
                          source:
                            type: text_processed
                          _weight: '0'
                _weight: '0'
```

**`field_property` format**: `field_property:{entity_type}:{field_name}:{column}` — **no bundle segment**. Bundle is implicit from the view display. The `column` (last segment) names which storage property to read (`value`, `uri`, `target_id`, `entity`); `source.type` controls how it's rendered (`value`, `text_processed`, `entity_label`).

### Source Scoping in Per-Item Formatters

`ui_patterns_component_per_item` scopes the source context to the trigger field only:

- `field_property` and `field_formatter` sources appear **only for the trigger field**
- Sibling field sources are **not in the dropdown** — use `entity_field` context switcher to reach them
- Widget sources (`textfield`, `token`, `select`) are always available
- Context-independent sources (`entity_link`, `path`, `breadcrumb`, `menu`) work without field context

## Common Mistakes

- **Wrong**: `field_property:node:article:field_name` (bundle segment) → **Right**: `field_property:node:field_name:value` (field name + column, no bundle)
- **Wrong**: Expecting sibling-field sources in per-item dropdowns → **Right**: Use `entity_field` context switcher (3-level nesting) to reach other fields on the same entity
- **Wrong**: Using multi-value formatter on single-cardinality fields → **Right**: `ComponentFormatter` requires cardinality >1 or unlimited; it will not appear for single-value fields. Use the per-item formatter (`ComponentPerItemFormatter`, id `ui_patterns_component_per_item`) instead — there is no class named `ComponentFormatterSingle`.
- **Wrong**: Per-item formatter for a 6-slot component reading 6 different fields → **Right**: Each slot needs `entity_field` 3-level config — block template with `{% include %}` is usually more maintainable

## See Also

- [Source Plugins](source-plugins.md) — `entity_field` context switcher pattern
- [drupal/ui-suite-daisyui — SDC Rendering Decision](../ui-suite-daisyui/sdc-rendering-decision.md) — trade-off matrix for UI Patterns wiring vs Twig include()
- Drupal Custom Field Guide
