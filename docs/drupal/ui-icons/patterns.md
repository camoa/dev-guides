---
description: "Declare icon-typed props on UI Patterns / SDC components via the icon PropType and $ref: ui-patterns://icon."
tldr: "Enable ui_icons_patterns to register the icon PropType (pack_id, icon_id, settings) and four data sources. Reference it with $ref: ui-patterns://icon, or shape an object prop with pack_id/icon_id for implicit typing; render via {{ prop }}."
drupal_version: "11.x"
---

# UI Patterns Integration

## When to Use

> Declaring icon props on UI Patterns components or SDC components used through UI Patterns.

## Pattern

Enable `ui_icons_patterns`. The submodule registers:

**PropType**: `icon` — declares an icon-typed component prop, schema `{pack_id: $ref ui-patterns://identifier, icon_id: string, settings: object}` with `pack_id` and `icon_id` required.

**Data Sources**:

| Source plugin | Use |
|---|---|
| `icon` | Direct `pack_id:icon_id` reference |
| `icon_renderable` | Icon as a renderable array (cacheable, attachable) |
| `link_icon` | Icon stored on a Link field |
| `field_icon` | Icon stored on an `ui_icon` field (experimental) |

**Explicit typing** — reference the PropType by `$ref` in a component definition (`*.component.yml` or pattern):

```yaml
props:
  type: object
  properties:
    leading_icon:
      title: "Leading icon"
      $ref: ui-patterns://icon
```

**Implicit typing** also works: an object prop shaped like the schema is matched to the same PropType by UI Patterns' shape matching (the plugin declares `priority: 10`):

```yaml
props:
  type: object
  properties:
    leading_icon:
      title: "Leading icon"
      type: object
      properties:
        pack_id: {type: string}
        icon_id: {type: string}
```

Either way the component editor sees an icon picker for that prop; it's stored, validated, and rendered through the icon pack's template. Add an `enum` under `pack_id` to restrict which packs the prop accepts.

In the component Twig template, render via `{{ leading_icon }}` — it arrives as a renderable array.

## Common Mistakes

- **Wrong**: writing `type: ui:icon` → **Right**: JSON Schema has no such type keyword; use `$ref: ui-patterns://icon`
- **Wrong**: declaring a flat `type: string` prop for an icon → **Right**: an object prop with `pack_id` and `icon_id` keeps the picker; a flat string loses it
- **Wrong**: hardcoding rendered SVG in the component template → **Right**: render via `{{ leading_icon }}`; hardcoding bypasses settings, cache metadata, and a11y templating

## See Also

- [Field API Integration](field-api.md)
- [Twig Rendering](twig.md)
- Reference: `modules/ui_icons_patterns/src/Plugin/UiPatterns/PropType/IconPropType.php`
- [UI Patterns guide](../ui-patterns/index.md)
