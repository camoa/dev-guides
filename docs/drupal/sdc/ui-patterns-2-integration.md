---
description: "How UI Patterns 2 discovers component.yml directly, its $ref extensions, and the one place default: is actually read"
tldr: "UI Patterns 2 reads component.yml directly — no separate pattern file needed — and exposes SDCs as blocks/layouts/views plugins via sub-modules. It is the one consumer that reads YAML default:, so keep default: in step with the Twig's ?? / |default(); if they disagree, UI-configured and Twig-called instances render differently."
drupal_version: "11.x"
---

# UI Patterns 2 Integration

## When to Use

> Use this when you're building SDCs that will be exposed to site builders via UI Patterns, you want components available as blocks, layouts, or views row/style plugins without custom PHP, or you need to understand how `component.yml` maps to UI Patterns discovery.

## Decision

**The `component.yml` schema used by SDCs IS the UI Patterns schema.** UI Patterns 2 discovers SDC `component.yml` files directly and exposes their props/slots in the admin UI. No separate pattern definition is needed.

| If you need... | UI Patterns provides... | Without UI Patterns you need... |
|---|---|---|
| Component as a block | `ui_patterns_blocks` sub-module auto-registers every SDC as a block plugin | Custom `BlockBase` plugin per component |
| Component as a Layout Builder section layout | `ui_patterns_layouts` sub-module exposes SDCs with slots as layout plugins | Custom `*.layouts.yml` + `LayoutDefault` plugin |
| Component rendering views rows | `ui_patterns_views` sub-module adds style/row plugins | Custom views template overrides |
| Mapping Drupal context to props/slots | `#[Source]` plugins map fields, blocks, menus to component inputs | Custom preprocess or field formatters |

**UI Patterns is the one consumer that does read `default:`.** Core ignores it (see [Component YAML Schema — THE MECHANISM](component-yaml-schema.md)), but UI Patterns seeds an unset source from `$this->propDefinition["default"]` (`/modules/contrib/ui_patterns/src/SourcePluginPropValue.php:62`, `EnumTrait.php:56-57`) and shows it in the prop summary. So a `default:` you write is real in the site-builder UI and inert in Twig — which makes keeping it in step with the template's `??` / `|default()` more important, not less. If they disagree, a component configured through the UI and the same component called from Twig render differently.

## Pattern

**Extended Schema Types** — UI Patterns extends the standard JSON Schema types with `$ref` references for Drupal-specific data:

```yaml
# Standard SDC props (works without UI Patterns)
props:
  type: object
  properties:
    title:
      type: string
    variant:
      type: string
      enum: [primary, secondary]

# UI Patterns enhanced props (requires UI Patterns)
    url:
      $ref: 'ui-patterns://url'        # Drupal URL object
    attributes:
      $ref: 'ui-patterns://attributes'  # Drupal Attribute object
    links:
      $ref: 'ui-patterns://links'       # Array of link objects
```

Components using only standard JSON Schema types work with and without UI Patterns. The `$ref` types add richer Drupal integration when UI Patterns is present.

**Source Plugins** — when a module provides `#[Source]` plugins, those sources can feed SDC props/slots from Drupal context automatically:

- **Field sources** — entity fields mapped to component props.
- **Block sources** — block plugin output mapped to slots.
- **Menu sources** — menu trees mapped to link arrays.
- **Views sources** — view fields mapped to component inputs.

Site builders configure these mappings in the admin UI without writing code.

## Common Mistakes

- **Wrong**: Defining separate pattern YAML files alongside `component.yml` → **Right**: UI Patterns 2 reads `component.yml` directly. Separate pattern definitions create duplicate registrations.
- **Wrong**: Using `$ref` types without checking the UI Patterns dependency → **Right**: Components with `ui-patterns://` refs require the module. Keep standard JSON Schema types for portable components.
- **Wrong**: Not defining complete schemas → **Right**: UI Patterns generates admin forms from your schema. Missing prop titles/descriptions produce poor admin UX.

## See Also

- [Component YAML Schema](component-yaml-schema.md) — base schema definition
- [Component Variants](component-variants.md) — variants also discovered by UI Patterns
- `drupal-ui-patterns.md` — full UI Patterns documentation
