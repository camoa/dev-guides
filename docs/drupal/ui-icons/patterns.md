---
description: Declare icon props on UI Patterns or SDC components using the ui:icon PropType.
tldr: Enable ui_icons_patterns to register the ui:icon PropType and four data sources (icon, icon_renderable, link_icon, field_icon). Declare icon props as type: ui:icon in component YAML to get a picker; rendering via {{ leading_icon }} outputs a cacheable renderable array.
drupal_version: "11.x"
---

# UI Patterns Integration

## When to Use

> Declaring icon props on UI Patterns components or SDC components used through UI Patterns.

## Pattern

Enable `ui_icons_patterns`. The submodule registers:

**PropType**: `icon` — declares an icon-typed component prop.

**Data Sources**:

| Source plugin | Use |
|---|---|
| `icon` | Direct `pack_id:icon_id` reference |
| `icon_renderable` | Icon as a renderable array (cacheable, attachable) |
| `link_icon` | Icon stored on a Link field |
| `field_icon` | Icon stored on a `ui_icon` field (experimental) |

In a component definition (`*.component.yml`):

```yaml
props:
  type: object
  properties:
    leading_icon:
      type: ui:icon          # PropType registered by ui_icons_patterns
      title: "Leading icon"
```

The component editor shows an icon picker for that prop; it's stored, validated, and rendered through the icon pack's template.

In the component Twig template, render via `{{ leading_icon }}` — it arrives as a renderable array.

## Common Mistakes

- **Wrong**: declaring `type: object` for icon props → **Right**: use `type: ui:icon` to get the picker UX and proper validation
- **Wrong**: hardcoding rendered SVG in the component template → **Right**: render via `{{ leading_icon }}`; hardcoding bypasses settings, cache metadata, and a11y templating

## See Also

- [Field API Integration](field-api.md)
- [Twig Rendering](twig.md)
- Reference: `modules/ui_icons_patterns/src/Plugin/UiPatterns/PropType/IconPropType.php`
- [UI Patterns guide](../ui-patterns/index.md)
