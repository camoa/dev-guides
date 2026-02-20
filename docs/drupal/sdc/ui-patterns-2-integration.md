---
description: UI Patterns 2 integration with SDC component.yml schema
drupal_version: "11.x"
---

# UI Patterns 2 Integration

## When to Use

> Use this when building SDCs that will be exposed to site builders via UI Patterns, making components available as blocks/layouts/views without custom PHP, or understanding how `component.yml` maps to UI Patterns discovery.

## Decision

| If you need | UI Patterns provides | Without UI Patterns you need |
|-------------|----------------------|------------------------------|
| Component as block | `ui_patterns_blocks` auto-registers every SDC | Custom `BlockBase` plugin per component |
| Layout Builder section | `ui_patterns_layouts` exposes SDCs with slots | Custom `*.layouts.yml` + `LayoutDefault` plugin |
| Views row rendering | `ui_patterns_views` adds style/row plugins | Custom views template overrides |
| Field → prop mapping | `#[Source]` plugins map fields to props | Custom preprocess or field formatters |

## Pattern

**The `component.yml` schema used by SDCs IS the UI Patterns schema.** UI Patterns 2 discovers SDC `component.yml` files directly.

**Standard SDC Props (works without UI Patterns):**
```yaml
props:
  type: object
  properties:
    title:
      type: string
    variant:
      type: string
      enum: [primary, secondary]
```

**UI Patterns Enhanced Props (requires UI Patterns):**
```yaml
props:
  type: object
  properties:
    url:
      $ref: 'ui-patterns://url'        # Drupal URL object
    attributes:
      $ref: 'ui-patterns://attributes'  # Drupal Attribute object
    links:
      $ref: 'ui-patterns://links'       # Array of link objects
```

**Source Plugins:**
When a module provides `#[Source]` plugins, sources can feed SDC props/slots from Drupal context:
- Field sources — entity fields mapped to component props
- Block sources — block plugin output mapped to slots
- Menu sources — menu trees mapped to link arrays
- Views sources — view fields mapped to component inputs

Site builders configure mappings in admin UI without code.

## Common Mistakes

- **Wrong**: Defining separate pattern YAML files alongside `component.yml` → **Right**: UI Patterns 2 reads `component.yml` directly
- **Wrong**: Using `ui-patterns://` refs without checking dependency → **Right**: Keep standard JSON Schema types for portable components
- **Wrong**: Incomplete schemas → **Right**: UI Patterns generates admin forms from schema; missing titles/descriptions produce poor UX

## See Also

- [Component YAML Schema](component-yaml-schema.md)
- [Component Variants](component-variants.md)
